import chainlit as cl
import uuid
from agent import HealthWellnessAgent
from context import UserSessionContext
from tools.goal_analyzer import GoalAnalyzerTool
from tools.meal_planner import MealPlannerTool
from tools.workout_recommender import WorkoutRecommenderTool
from tools.scheduler import CheckinSchedulerTool
from tools.tracker import ProgressTrackerTool
from agents.escalation_agent import EscalationAgent
from agents.nutrition_expert_agent import NutritionExpertAgent
from agents.injury_support_agent import InjurySupportAgent
from hooks import CustomRunHooks

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("context", UserSessionContext(
        name="Fatima",
        uid=uuid.uuid4().int & (1 << 31) - 1,
        handoff_logs=[],
        progress_logs=[],
        diet_preferences=["Vegetarian"],
        health_conditions=["Joint Issues"],
        goal=None
    ))

    # Tools and agents
    tools = [
        GoalAnalyzerTool(),
        MealPlannerTool(),
        WorkoutRecommenderTool(),
        CheckinSchedulerTool(),
        ProgressTrackerTool()
    ]

    handoff_agents = {
        "escalation": EscalationAgent(),
        "nutrition_expert": NutritionExpertAgent(),
        "injury_support": InjurySupportAgent()
    }

    agent = HealthWellnessAgent(tools=tools, handoffs=handoff_agents, hooks=CustomRunHooks())
    cl.user_session.set("agent", agent)

    await cl.Message(content="🤖 Welcome to the Health & Wellness Planner! Ask your fitness or health-related questions.").send()

# On Each User Message
@cl.on_message
async def on_message(message: cl.Message):
    agent = cl.user_session.get("agent")
    context = cl.user_session.get("context")
    result = await agent.process_input(message.content, context)

    # Handle response
    if "agent_advice" in result:
        await cl.Message(content=result["agent_advice"]).send()
    elif "error" in result:
        await cl.Message(content=f"❌ {result['error']}").send()
    else:
        await cl.Message(content="🤔 I didn’t understand. Try rephrasing.").send()
