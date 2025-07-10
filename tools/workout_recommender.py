from openai_agents import Tool
from context import UserSessionContext
from guardrails import validate_output
import asyncio

class WorkoutRecommenderTool(Tool):
    def __init__(self):
        super().__init__(name="WorkoutRecommenderTool")

    def should_trigger(self, input_text: str, context: UserSessionContext) -> bool:
        return context.goal is not None or "workout" in input_text.lower()

    async def execute(self, input_text: str, context: UserSessionContext) -> dict:
        await asyncio.sleep(1)  # Simulate async processing
        if context.goal:
            workout_plan = {
                "type": "strength_training",
                "days": [
                    {"day": "Monday", "exercises": ["Squats", "Push-ups"]},
                    {"day": "Wednesday", "exercises": ["Deadlifts", "Pull-ups"]},
                    {"day": "Friday", "exercises": ["Bench Press", "Lunges"]}
                ]
            }
            context.workout_plan = workout_plan
            return validate_output({"workout_plan": workout_plan}, context)
        return validate_output({"error": "No goal specified for workout plan"}, context)