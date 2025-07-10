import asyncio
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

async def main():
    user_context = UserSessionContext(
        name="Fatima",
        uid=uuid.uuid4().int & (1 << 31) - 1,
        handoff_logs=[],
        progress_logs=[],
        diet_preferences=["Vegetarian"],
        health_conditions=["Joint Issues"],
        goal=None
    )

    # Tools
    tools = [
        GoalAnalyzerTool(),
        MealPlannerTool(),
        WorkoutRecommenderTool(),
        CheckinSchedulerTool(),
        ProgressTrackerTool()
    ]

    # Handoff agents
    handoff_agents = {
        "escalation": EscalationAgent(),
        "nutrition_expert": NutritionExpertAgent(),
        "injury_support": InjurySupportAgent()
    }

    # Agent with hooks
    agent = HealthWellnessAgent(
        tools=tools,
        handoffs=handoff_agents,
        hooks=CustomRunHooks()
    )

    print("\n🤖 Welcome to the Health & Wellness CLI Agent")
    print("Type your health question below. Type 'exit' to quit.\n")

    # CLI Interaction Loop
    while True:
        user_input = input("❓ You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        result = await agent.process_input(user_input, user_context)

        if "agent_advice" in result:
            print("\n💡 Agent Advice:\n")
            print(result["agent_advice"])
        elif "error" in result:
            print("❌ Error:", result["error"])
        else:
            print("❓ I didn’t understand. Please rephrase.")


if __name__ == "__main__":
    asyncio.run(main())
