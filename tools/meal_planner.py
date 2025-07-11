from typing import Dict, Any
from context import UserSessionContext

class MealPlannerTool:
    name = "MealPlannerTool"
    description = "Suggests a vegetarian meal plan based on user preferences."

    def should_trigger(self, input_text: str, context: UserSessionContext) -> bool:
        keywords = ["meal", "diet", "plan", "food", "vegetarian"]
        return any(word in input_text.lower() for word in keywords)

    async def execute(self, user_input: str, context: UserSessionContext) -> Dict[str, Any]:
        if "vegetarian" not in context.diet_preferences:
            return {
                "message": "ℹ️ No specific diet mentioned yet. Set your preference to vegetarian to get a custom meal plan."
            }

        meal_plan = {
            "breakfast": "Oats with almond milk and berries",
            "lunch": "Chickpea salad with olive oil and lemon",
            "dinner": "Grilled tofu with sautéed vegetables and quinoa"
        }

        return {
            "type": "meal_plan",
            "data": meal_plan,
            "message": "🥗 Here's your vegetarian meal plan!"
        }
