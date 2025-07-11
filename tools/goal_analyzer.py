import re
from typing import Dict, Any
from context import UserSessionContext

class GoalAnalyzerTool:
    name = "GoalAnalyzerTool"
    description = "Extracts and sets the user's fitness goal."

    def should_trigger(self, input_text: str, context: UserSessionContext) -> bool:
        """
        Trigger if the input mentions weight or fitness goals.
        """
        keywords = ["lose", "gain", "weight", "fat", "muscle"]
        return any(word in input_text.lower() for word in keywords)

    async def execute(self, input_text: str, context: UserSessionContext) -> Dict[str, Any]:
        """
        Parses input like 'lose 5kg in 2 months' and stores the goal in context.
        """
        cleaned = input_text.lower().replace("loss", "lose").strip()

        pattern = (
            r"(lose|gain)\s+"             # lose/gain
            r"(\d+(?:\.\d+)?)\s*"         # number (5 or 5.5)
            r"(kg|kgs|lbs|pounds)?\s*"    # optional unit
            r"(in)?\s*"
            r"(\d+)\s*"
            r"(weeks?|months?)"
        )

        match = re.search(pattern, cleaned)
        if match:
            action, amount, unit, _, duration, duration_unit = match.groups()
            unit = unit or "kg"
            duration_unit = duration_unit.rstrip("s")

            goal_str = f"{action} {amount} {unit} in {duration} {duration_unit}"
            context.goal = goal_str

            return {
                "type": "goal",
                "goal": {
                    "action": action,
                    "amount": amount,
                    "unit": unit,
                    "duration": duration,
                    "duration_unit": duration_unit
                },
                "message": f"🎯 Goal detected: {goal_str}"
            }

        return {
            "error": "❌ No valid goal found. Try: 'I want to lose 5kg in 2 months'."
        }
