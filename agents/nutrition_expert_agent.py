from datetime import datetime

class NutritionExpertAgent:
    def run_tools(self, input_text, context):
        preferences = context.diet_preferences if hasattr(context, 'diet_preferences') else []
        health_conditions = context.health_conditions if hasattr(context, 'health_conditions') else []

        recommendation = "🥗 Personalized Nutrition Plan:\n"

        if "vegetarian" in [p.lower() for p in preferences]:
            recommendation += "- Include protein-rich plant foods: lentils, tofu, chickpeas, quinoa.\n"

        if "diabetes" in [c.lower() for c in health_conditions] or "diabetic" in input_text.lower():
            recommendation += "- Prioritize low-glycemic foods: oats, non-starchy vegetables, whole grains.\n"
            recommendation += "- Avoid sugary drinks and processed carbs.\n"

        if not preferences and not health_conditions:
            recommendation += "- Maintain a balanced diet with whole grains, lean proteins, and fresh vegetables.\n"

        return {
            "message": "🍽️ Nutrition guidance ready.",
            "nutrition_plan": {
                "recommendation": recommendation.strip(),
                "timestamp": datetime.now().isoformat()
            }
        }
