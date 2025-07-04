from typing import List
from pydantic import BaseModel
from openai.agents import tool
from openai.agents.types import RunContextWrapper
from context import UserSessionContext
from guardrails import validate_diet_input

class MealPlan(BaseModel):
    diet_type: str
    meals: List[str]

@tool(name="suggest_meals", description="Suggest a meal plan based on the user's diet preference.")
def suggest_meals(
    user_input: str,
    context: RunContextWrapper[UserSessionContext]
) -> MealPlan:
    """
    Suggests a simple meal plan based on a recognized dietary preference.
    Also saves the meal plan into context.
    """

    # Validate diet preference
    if not validate_diet_input(user_input):
        raise ValueError("❌ Unsupported diet type. Try vegetarian, vegan, keto, etc.")

    # Example meal suggestions 
    diet = user_input.lower()
    sample_meals = {
        "vegetarian": ["Oats with fruits", "Lentil soup", "Grilled tofu with veggies"],
        "vegan": ["Avocado toast", "Quinoa salad", "Chickpea curry"],
        "keto": ["Egg muffins", "Zucchini noodles", "Grilled salmon"],
        "paleo": ["Scrambled eggs", "Beef stir-fry", "Sweet potato hash"],
        "low carb": ["Greek yogurt", "Chicken salad", "Steak with broccoli"],
        "high protein": ["Protein smoothie", "Tuna bowl", "Boiled eggs"],
        "mediterranean": ["Hummus wrap", "Grilled chicken", "Greek salad"]
    }

    meals = sample_meals.get(diet, [])

    # Build output model
    meal_plan = MealPlan(diet_type=diet, meals=meals)

    context.meal_plan = meals

    return meal_plan
