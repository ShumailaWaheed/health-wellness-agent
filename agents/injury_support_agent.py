from datetime import datetime

class InjurySupportAgent:
    def run_tools(self, input_text, context):
        conditions = context.health_conditions if hasattr(context, 'health_conditions') else []
        goal = context.goal if hasattr(context, 'goal') else input_text

        recommendation = "🦵 Recovery Advice:\n"
        recommendation += "- Prioritize rest and avoid strain.\n"
        recommendation += "- Consult a physiotherapist for a personalized plan.\n"

        if "knee" in input_text.lower() or "joint" in input_text.lower() or "joint issues" in [c.lower() for c in conditions]:
            recommendation += "- Try low-impact workouts like swimming or cycling.\n"
            recommendation += "- Do strengthening exercises for your legs (quads/hamstrings).\n"
            recommendation += "- Avoid jumping or high-intensity squats.\n"

        return {
            "message": "🩺 Injury support advice generated",
            "injury_support_plan": {
                "recommendation": recommendation.strip(),
                "timestamp": datetime.now().isoformat()
            }
        }
