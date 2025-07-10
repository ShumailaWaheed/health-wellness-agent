import re
from typing import Dict, Any
from context import UserSessionContext

class GoalAnalyzerTool:
    name = "GoalAnalyzerTool"

    def should_trigger(self, input_text: str, context: UserSessionContext) -> bool:
        """
        Check if the user's message is likely related to a weight or fitness goal.
        """
        keywords = ["lose", "loss", "gain", "weight", "fat", "muscle"]
        return any(word in input_text.lower() for word in keywords)

    async def execute(self, input_text: str, context: UserSessionContext) -> Dict[str, Any]:
        """
        Analyze user input to extract goal-related information like:
        'lose 5kg in 2 months' or 'gain 10 pounds in 6 weeks'
        """

        # Normalize text: fix common typos and clean spacing
        cleaned_text = input_text.lower().replace("loss", "lose").strip()

        # Regex pattern to extract: action, amount, unit, duration, etc.
        pattern = (
            r"(lose|gain)\s+"             # action: lose or gain
            r"(\d+(?:\.\d+)?)\s*"         # amount: number (int or float)
            r"(kg|kgs|lbs|pounds)?\s*"    # unit: optional
            r"(in)?\s*"                   # optional "in"
            r"(\d+)\s*"                   # duration value
            r"(weeks?|months?)"           # duration unit
        )

        match = re.search(pattern, cleaned_text)

        if match:
            action, amount, unit, _, duration, duration_unit = match.groups()
            unit = unit or "kg"
            duration_unit = duration_unit.lower().rstrip("s")  # normalize singular form

            # Format the goal and store in context
            formatted_goal = f"{action} {amount} {unit} in {duration} {duration_unit}"
            context.goal = formatted_goal

            return {
                "message": f"🎯 Goal detected: {formatted_goal}",
                "goal": {
                    "action": action,
                    "amount": amount,
                    "unit": unit,
                    "duration": duration,
                    "duration_unit": duration_unit
                }
            }

        # If no valid goal format is found, return helpful feedback
        return {
            "error": "No valid goal found. Please use a format like: 'lose/gain X kg/lbs in Y months/weeks'.",
            "example": "Example: 'I want to lose 5kg in 2 months'"
        }
import re
from typing import Dict, Any
from context import UserSessionContext

class GoalAnalyzerTool:
    name = "GoalAnalyzerTool"

    def should_trigger(self, input_text: str, context: UserSessionContext) -> bool:
        """
        Check if the user's message is likely related to a weight or fitness goal.
        """
        keywords = ["lose", "loss", "gain", "weight", "fat", "muscle"]
        return any(word in input_text.lower() for word in keywords)

    async def execute(self, input_text: str, context: UserSessionContext) -> Dict[str, Any]:
        """
        Analyze user input to extract goal-related information like:
        'lose 5kg in 2 months' or 'gain 10 pounds in 6 weeks'
        """

        # Normalize text: fix common typos and clean spacing
        cleaned_text = input_text.lower().replace("loss", "lose").strip()

        # Regex pattern to extract: action, amount, unit, duration, etc.
        pattern = (
            r"(lose|gain)\s+"             # action: lose or gain
            r"(\d+(?:\.\d+)?)\s*"         # amount: number (int or float)
            r"(kg|kgs|lbs|pounds)?\s*"    # unit: optional
            r"(in)?\s*"                   # optional "in"
            r"(\d+)\s*"                   # duration value
            r"(weeks?|months?)"           # duration unit
        )

        match = re.search(pattern, cleaned_text)

        if match:
            action, amount, unit, _, duration, duration_unit = match.groups()
            unit = unit or "kg"
            duration_unit = duration_unit.lower().rstrip("s")  # normalize singular form

            # Format the goal and store in context
            formatted_goal = f"{action} {amount} {unit} in {duration} {duration_unit}"
            context.goal = formatted_goal

            return {
                "message": f"🎯 Goal detected: {formatted_goal}",
                "goal": {
                    "action": action,
                    "amount": amount,
                    "unit": unit,
                    "duration": duration,
                    "duration_unit": duration_unit
                }
            }

        # If no valid goal format is found, return helpful feedback
        return {
            "error": "No valid goal found. Please use a format like: 'lose/gain X kg/lbs in Y months/weeks'.",
            "example": "Example: 'I want to lose 5kg in 2 months'"
        }
import re
from typing import Dict, Any
from context import UserSessionContext

class GoalAnalyzerTool:
    name = "GoalAnalyzerTool"

    def should_trigger(self, input_text: str, context: UserSessionContext) -> bool:
        """
        Check if the user's message is likely related to a weight or fitness goal.
        """
        keywords = ["lose", "loss", "gain", "weight", "fat", "muscle"]
        return any(word in input_text.lower() for word in keywords)

    async def execute(self, input_text: str, context: UserSessionContext) -> Dict[str, Any]:
        """
        Analyze user input to extract goal-related information like:
        'lose 5kg in 2 months' or 'gain 10 pounds in 6 weeks'
        """

        # Normalize text: fix common typos and clean spacing
        cleaned_text = input_text.lower().replace("loss", "lose").strip()

        # Regex pattern to extract: action, amount, unit, duration, etc.
        pattern = (
            r"(lose|gain)\s+"             # action: lose or gain
            r"(\d+(?:\.\d+)?)\s*"         # amount: number (int or float)
            r"(kg|kgs|lbs|pounds)?\s*"    # unit: optional
            r"(in)?\s*"                   # optional "in"
            r"(\d+)\s*"                   # duration value
            r"(weeks?|months?)"           # duration unit
        )

        match = re.search(pattern, cleaned_text)

        if match:
            action, amount, unit, _, duration, duration_unit = match.groups()
            unit = unit or "kg"
            duration_unit = duration_unit.lower().rstrip("s")  # normalize singular form

            # Format the goal and store in context
            formatted_goal = f"{action} {amount} {unit} in {duration} {duration_unit}"
            context.goal = formatted_goal

            return {
                "message": f"🎯 Goal detected: {formatted_goal}",
                "goal": {
                    "action": action,
                    "amount": amount,
                    "unit": unit,
                    "duration": duration,
                    "duration_unit": duration_unit
                }
            }

        # If no valid goal format is found, return helpful feedback
        return {
            "error": "No valid goal found. Please use a format like: 'lose/gain X kg/lbs in Y months/weeks'.",
            "example": "Example: 'I want to lose 5kg in 2 months'"
        }
import re
from typing import Dict, Any
from context import UserSessionContext

class GoalAnalyzerTool:
    name = "GoalAnalyzerTool"

    def should_trigger(self, input_text: str, context: UserSessionContext) -> bool:
        """
        Check if the user's message is likely related to a weight or fitness goal.
        """
        keywords = ["lose", "loss", "gain", "weight", "fat", "muscle"]
        return any(word in input_text.lower() for word in keywords)

    async def execute(self, input_text: str, context: UserSessionContext) -> Dict[str, Any]:
        """
        Analyze user input to extract goal-related information like:
        'lose 5kg in 2 months' or 'gain 10 pounds in 6 weeks'
        """

        # Normalize text: fix common typos and clean spacing
        cleaned_text = input_text.lower().replace("loss", "lose").strip()

        # Regex pattern to extract: action, amount, unit, duration, etc.
        pattern = (
            r"(lose|gain)\s+"             # action: lose or gain
            r"(\d+(?:\.\d+)?)\s*"         # amount: number (int or float)
            r"(kg|kgs|lbs|pounds)?\s*"    # unit: optional
            r"(in)?\s*"                   # optional "in"
            r"(\d+)\s*"                   # duration value
            r"(weeks?|months?)"           # duration unit
        )

        match = re.search(pattern, cleaned_text)

        if match:
            action, amount, unit, _, duration, duration_unit = match.groups()
            unit = unit or "kg"
            duration_unit = duration_unit.lower().rstrip("s")  # normalize singular form

            # Format the goal and store in context
            formatted_goal = f"{action} {amount} {unit} in {duration} {duration_unit}"
            context.goal = formatted_goal

            return {
                "message": f"🎯 Goal detected: {formatted_goal}",
                "goal": {
                    "action": action,
                    "amount": amount,
                    "unit": unit,
                    "duration": duration,
                    "duration_unit": duration_unit
                }
            }

        # If no valid goal format is found, return helpful feedback
        return {
            "error": "No valid goal found. Please use a format like: 'lose/gain X kg/lbs in Y months/weeks'.",
            "example": "Example: 'I want to lose 5kg in 2 months'"
        }
