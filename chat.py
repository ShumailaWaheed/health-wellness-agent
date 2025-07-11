import chainlit as cl
import os
import logging
from typing import Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class HealthWellnessAgent:
    def __init__(self):
        self._initialize_gemini()
        self.handoffs = {
            "real trainer": self._handle_escalation,
            "talk to someone": self._handle_escalation,
            "nutrition": self._handle_nutrition,
            "diet": self._handle_nutrition,
            "injury": self._handle_injury,
            "pain": self._handle_injury
        }

    def _initialize_gemini(self):
        """Initialize Gemini with proper error handling"""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                raise ValueError("Missing GEMINI_API_KEY in .env file")

            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini initialized successfully")
        except Exception as e:
            logger.error(f"Gemini initialization failed: {str(e)}")
            raise RuntimeError("Failed to initialize AI services")

    async def _handle_escalation(self, query: str, context: Dict) -> Dict:
        """Handle human expert escalation"""
        return {
            "type": "escalation",
            "content": "I've connected you with a human expert. They'll respond shortly.",
            "actions": [
                {"label": "Continue Chat", "type": "button"},
                {"label": "Schedule Call", "type": "button"}
            ]
        }

    async def _handle_nutrition(self, query: str, context: Dict) -> Dict:
        """Generate nutrition-specific advice"""
        prompt = f"""As a certified nutritionist, provide detailed advice for:
User: {context.get('name', 'User')}
Diet: {context.get('diet_preferences', [])}
Conditions: {context.get('health_conditions', [])}
Query: {query}

Include:
1. Meal suggestions
2. Nutritional targets
3. Supplement guidance
4. Common mistakes to avoid"""
        response = await self._safe_generate(prompt)
        return {
            "type": "nutrition",
            "content": response,
            "references": ["USDA Guidelines", "Academy of Nutrition and Dietetics"]
        }

    async def _handle_injury(self, query: str, context: Dict) -> Dict:
        """Generate injury recovery advice"""
        prompt = f"""As a physical therapist, provide recovery advice for:
User: {context.get('name', 'User')}
Conditions: {context.get('health_conditions', [])}
Query: {query}

Include:
1. Recommended exercises
2. Activity modifications
3. Recovery timeline
4. Warning signs"""
        response = await self._safe_generate(prompt)
        return {
            "type": "injury",
            "content": response,
            "disclaimer": "Consult a healthcare provider before starting any new exercise regimen"
        }

    async def _safe_generate(self, prompt: str) -> str:
        """Safe content generation with error handling"""
        try:
            response = await self.model.generate_content_async(prompt)
            return getattr(response, "text", "⚠️ Gemini gave no text response.")
        except Exception as e:
            logger.error(f"Generation failed: {str(e)}")
            return "⚠️ I couldn't generate a response. Please try rephrasing your question."

    async def process(self, query: str, context: Dict) -> Dict:
        """Main processing method with comprehensive error handling"""
        try:
            query_lower = query.lower()
            for trigger, handler in self.handoffs.items():
                if trigger in query_lower:
                    return await handler(query, context)

            prompt = f"""As a health expert, provide advice for:
User: {context.get('name', 'User')}
Profile: {context}
Query: {query}

Respond with:
1. Professional assessment
2. Actionable steps
3. Safety considerations
4. Follow-up suggestions"""

            content = await self._safe_generate(prompt)
            return {
                "type": "wellness",
                "content": content,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Processing failed: {str(e)}")
            return {
                "type": "error",
                "content": "I encountered an issue processing your request.",
                "resolution": "Please try again or rephrase your question."
            }

# Initialize agent
agent = HealthWellnessAgent()

@cl.on_chat_start
async def init_chat():
    await cl.Message(
        content="""Welcome to HealthBridge! I'm your AI wellness assistant.\nBefore we begin, please confirm:\n1. This is not emergency care\n2. For diagnoses, consult a physician\n3. All advice is general guidance""",
        disable_feedback=False
    ).send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_context = {
        "name": "Alex",
        "diet_preferences": ["Vegetarian"],
        "health_conditions": ["None"],
        "last_checkin": "2023-11-15"
    }

    msg = cl.Message(content="")
    await msg.send()

    try:
        logger.info(f"📨 Incoming message: {message.content}")
        result = await agent.process(message.content, user_context)
        logger.info(f"✅ Result from agent: {result}")

        response_message = cl.Message(
            author="HealthBridge AI",
            parent_id=message.id
        )

        if "type" not in result:
            raise ValueError("Response missing 'type' field")

        if result["type"] == "error":
            response_message.content = "⚠️ " + result["content"]
            if "resolution" in result:
                response_message.content += f"\n\n{result['resolution']}"

        elif result["type"] == "escalation":
            response_message.content = "🔴 " + result["content"]
            if "actions" in result:
                response_message.actions = [
                    cl.Action(name=action["type"], value=action["label"])
                    for action in result["actions"]
                ]

        else:
            response_message.content = result["content"]
            if "disclaimer" in result:
                response_message.content += f"\n\n⚠️ Note: {result['disclaimer']}"

        await response_message.send()

    except Exception as e:
        logger.error(f"Message handling failed: {str(e)}")
        await cl.Message(
            content="""⚠️ Our systems are currently unavailable.\nFor immediate assistance:\n1. Call support: 1-800-HEALTH\n2. Email: help@healthbridge.ai""",
            author="System Alert"
        ).send()

if __name__ == "__main__":
    from chainlit.cli import run_chainlit
    run_chainlit(__file__)
