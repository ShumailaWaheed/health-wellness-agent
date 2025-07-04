from typing import List, Dict
from pydantic import BaseModel
from openai.agents import tool
from openai.agents.types import RunContextWrapper
from context import UserSessionContext

class DailySchedule(BaseModel):
    day: str
    breakfast: str
    workout: str
    lunch: str
    dinner: str

class WeeklySchedule(BaseModel):
    goal_summary: str
    schedule: List[DailySchedule]


@tool(name="create_schedule", description="Create a weekly health plan based on user's goal, meals, and workouts.")
def create_schedule(
    context: RunContextWrapper[UserSessionContext]
) -> WeeklySchedule:
    """
    Generates a 3-day sample schedule using the goal, meal plan, and workout plan from context.
    """

    # Pull context data
    goal = context.goal or {}
    meals = context.meal_plan or []
    workout_data = context.workout_plan or {}
    workouts = workout_data.get("workouts", [])

    if not goal or not meals or not workouts:
        raise ValueError("❌ Missing data. Make sure goals, meals, and workouts are set before generating a schedule.")

    # Build daily plan
    sample_days = ["Monday", "Wednesday", "Friday"]
    daily_plan = []

    for i, day in enumerate(sample_days):
        daily_plan.append(DailySchedule(
            day=day,
            breakfast=meals[0] if len(meals) > 0 else "Oatmeal",
            workout=workouts[i % len(workouts)],
            lunch=meals[1] if len(meals) > 1 else "Grilled chicken salad",
            dinner=meals[2] if len(meals) > 2 else "Steamed veggies with quinoa"
        ))

    goal_summary = f"{goal.get('goal_type', 'Work')} {goal.get('quantity', '')}{goal.get('metric', '')} in {goal.get('duration', '')} {goal.get('duration_unit', '')}"

    # Save schedule to context (optional)
    context["generated_schedule"] = [d.dict() for d in daily_plan]

    return WeeklySchedule(
        goal_summary=goal_summary,
        schedule=daily_plan
    )
