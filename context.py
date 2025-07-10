from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class UserSessionContext(BaseModel):
    name: str
    uid: int
    email: Optional[str] = None
    handoff_logs: List[str]
    progress_logs: List[Dict[str, Any]]
    diet_preferences: List[str]
    health_conditions: List[str]
    goal: Optional[str] = None
    meal_plan: Optional[Dict[str, Any]] = None
    workout_plan: Optional[Dict[str, Any]] = None
    injury_notes: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True