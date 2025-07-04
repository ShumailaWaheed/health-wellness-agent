from openai.agents import Agent

from tools.meal_planner import suggest_meals

nutrition_expert_agent = Agent(
    name="NutritionExpert",
    instructions=(
        "You are a certified nutritionist. Your job is to help users choose healthy meals "
        "based on their dietary preferences and fitness goals. "
        "Provide clear, science-based recommendations and avoid medical advice."
    ),
    tools=[suggest_meals]
)
