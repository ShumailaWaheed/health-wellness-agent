# tools/workout_recommender.py

from typing import List
from pydantic import BaseModel
from openai.agents import tool
from openai.agents.types import RunContextWrapper
from context import UserSessionContext


# ✅ Output model for workout recommendations
class WorkoutPlan(BaseModel):
    fitness_level: str
    goal_type: str
    workouts: List[str]


@tool(name="recommend_workout", description="Recommend a workout plan based on user fitness level and goals.")
def recommend_workout(
    user_input: str,
    context: RunContextWrapper[UserSessionContext]
) -> WorkoutPlan:
    """
    Recommends workouts based on user's goal and fitness level.
    Uses context.goal and assumes user_input is fitness level (beginner/intermediate/advanced).
    """

    fitness_level = user_input.strip().lower()
    goal_info = context.goal or {}

    goal_type = goal_info.get("goal_type", "general")

    # Sample recommendations
    workouts = []

    if fitness_level == "beginner":
        if goal_type == "lose":
            workouts = ["30-min walk", "Beginner yoga", "Bodyweight squats"]
        elif goal_type == "gain":
            workouts = ["Light dumbbell curls", "Push-ups", "Resistance band rows"]
        else:
            workouts = ["Stretching", "Light cardio", "Basic strength circuit"]

    elif fitness_level == "intermediate":
        workouts = ["Jogging", "HIIT 20 mins", "Weight lifting (moderate)"]

    elif fitness_level == "advanced":
        workouts = ["Heavy strength training", "CrossFit", "Sprint intervals"]

    else:
        raise ValueError("❌ Unknown fitness level. Try: beginner, intermediate, or advanced.")

    # Save the plan to context
    context.workout_plan = {
        "level": fitness_level,
        "goal_type": goal_type,
        "workouts": workouts
    }

    return WorkoutPlan(
        fitness_level=fitness_level,
        goal_type=goal_type,
        workouts=workouts
    )
