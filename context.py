from typing import Optional, List, Dict
from pydantic import BaseModel

class UserSessionContext(BaseModel):
    name: str
    uid: int
    goal: Optional[dict] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[dict] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = []
    progress_logs: List[Dict[str, str]] = []


class SimpleContextWrapper:
    """
    A simplified alternative to RunContextWrapper.
    You can directly access `context.data` to get/set values.
    """
    def __init__(self, context: UserSessionContext):
        self.data = context


def initialize_context() -> SimpleContextWrapper:
    context = UserSessionContext(
        name="Guest",
        uid=0,
        goal=None,
        diet_preferences=None,
        workout_plan=None,
        meal_plan=[],
        injury_notes=None,
        handoff_logs=[],
        progress_logs=[],
    )
    return SimpleContextWrapper(context)
