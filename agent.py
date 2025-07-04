from openai.agents import Agent, RunnableAgent, tool
from tools.goal_analyzer import analyze_goal
from tools.meal_planner import suggest_meals
from tools.workout_recommender import recommend_workout
from tools.scheduler import create_schedule
from tools.tracker import track_progress
from agents.nutrition_expert_agent import nutrition_expert_agent
from agents.injury_support_agent import injury_support_agent
from agents.escalation_agent import escalation_agent

def create_main_agent() -> RunnableAgent:
    """
    Create the main Health & Wellness assistant agent.
    It includes tools and sub-agents for nutrition, injuries, and more.
    """
    return Agent(
        name="HealthWellnessAssistant",
        instructions=(
            "You are a helpful and friendly Health & Wellness assistant. "
            "Your job is to help users set goals, plan meals, track progress, recommend workouts, and build routines. "
            "If the request is too specialized, call the appropriate expert agent or escalate."
        ),
        tools=[
            analyze_goal,
            suggest_meals,
            recommend_workout,
            create_schedule,
            track_progress,
        ],
        agents=[
            nutrition_expert_agent,
            injury_support_agent,
            escalation_agent,
        ],
    ).as_runnable()
