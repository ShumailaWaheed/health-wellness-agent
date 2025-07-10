import re
from pydantic import BaseModel
from agents.decorators import tool
from context import UserSessionContext
from guardrails import validate_goal_input

class Goal(BaseModel):
    goal_type: str     # lose or gain
    quantity: int
    metric: str        # kg or lbs
    duration: int
    duration_unit: str # days, weeks, months

@tool(name="analyze_goal", description="Extract and save user fitness goals from input text.")
async def analyze_goal(
    user_input: str,
    context: dict  # ✅ changed from RunContextWrapper to dict
) -> dict:
    """
    Parses fitness goals from user input and saves them in context.
    Expected format: 'lose 5kg in 2 months'
    """

    # Validate input
    if not validate_goal_input(user_input):
        raise ValueError("❌ Please use a valid goal format like 'lose 5kg in 2 months'.")

    # Regex extract
    pattern = r"(lose|gain)\s+(\d+)(kg|lbs)\s+in\s+(\d+)\s+(days|weeks|months)"
    match = re.fullmatch(pattern, user_input.strip().lower())

    if not match:
        raise ValueError("⚠️ Could not parse goal. Please check your wording.")

    goal_type, quantity, metric, duration, duration_unit = match.groups()
    goal = Goal(
        goal_type=goal_type,
        quantity=int(quantity),
        metric=metric,
        duration=int(duration),
        duration_unit=duration_unit
    )

    # Save in context
    context["goal"] = goal.dict()  # ✅ dict assignment

    return {
        "type": "goal_analysis",
        "data": goal.dict(),
        "message": f"🎯 Goal set: {goal.goal_type} {goal.quantity}{goal.metric} in {goal.duration} {goal.duration_unit}."
    }
