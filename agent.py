import os
import logging
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List, Dict, Any
from context import UserSessionContext

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing in your .env file")

    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    logger.info("✅ Gemini Free Model Initialized (gemini-1.5-flash)")

except Exception as e:
    logger.error(f"🚨 Initialization Error: {str(e)}")
    raise


#  Base Agent class
class Agent:
    def __init__(self, name: str, tools: List[Any] = None, handoffs: Dict[str, Any] = None, hooks=None):
        self.name = name
        self.tools = tools or []
        self.handoffs = handoffs or {}
        self.hooks = hooks
        self.model = gemini_model  # Assign globally initialized model

    async def process_input(self, input_text: str, context: UserSessionContext) -> Dict[str, Any]:
        if self.hooks and hasattr(self.hooks, "on_agent_start"):
            self.hooks.on_agent_start(self.name, context)

        # Escalation handoff
        if any(word in input_text.lower() for word in ["real trainer", "talk to someone", "escalate"]):
            return await self.handoff("escalation", input_text, context)

        # Run tools
        result = await self.run_tools(input_text, context)

        # AI-generated advice
        try:
            prompt = f"""
You are a certified health and wellness expert.
User Profile:
- Name: {context.name}
- Diet Preferences: {', '.join(context.diet_preferences) if context.diet_preferences else 'None'}
- Health Conditions: {', '.join(context.health_conditions) if context.health_conditions else 'None'}

User Question:
{input_text}

Respond with a detailed paragraph followed by bullet points. The paragraph should summarize the advice in a friendly tone. The bullet points should provide specific tips, warnings (if any), and motivational suggestions.
"""
            response = await self.model.generate_content_async(prompt)
            result["agent_advice"] = response.text.strip()  # ✅ renamed key
        except Exception as e:
            result["error"] = f"⚠️ Gemini failed: {str(e)}"

        if self.hooks and hasattr(self.hooks, "on_agent_end"):
            self.hooks.on_agent_end(self.name, context)

        return result

    async def run_tools(self, input_text: str, context: UserSessionContext) -> Dict[str, Any]:
        combined_result = {}

        # Run each matching tool
        for tool in self.tools:
            if tool.should_trigger(input_text, context):
                tool_result = await tool.execute(input_text, context)
                combined_result.update(tool_result)

        # Auto-Handoff: Injury Support
        if "knee" in input_text.lower() or "joint" in input_text.lower():
            if "injury_support" in self.handoffs:
                injury_result = self.handoffs["injury_support"].run_tools(input_text, context)
                if asyncio.iscoroutine(injury_result):
                    injury_result = await injury_result
                combined_result["injury_support"] = injury_result

        # Auto-Handoff: Nutrition Expert
        if "diabetic" in input_text.lower() or "diabetes" in input_text.lower():
            if "nutrition_expert" in self.handoffs:
                nutrition_result = self.handoffs["nutrition_expert"].run_tools(input_text, context)
                if asyncio.iscoroutine(nutrition_result):
                    nutrition_result = await nutrition_result
                combined_result["nutrition_expert"] = nutrition_result

        return combined_result

    async def handoff(self, target_agent_name: str, input_text: str, context: UserSessionContext) -> Dict[str, Any]:
        agent = self.handoffs.get(target_agent_name)
        if not agent:
            return {"error": f"No agent found for handoff: {target_agent_name}"}
        result = agent.run_tools(input_text, context)
        if asyncio.iscoroutine(result):
            result = await result
        return result
class HealthWellnessAgent(Agent):
    def __init__(self, tools=None, handoffs=None, hooks=None):
        super().__init__("HealthWellnessAgent", tools, handoffs, hooks)
