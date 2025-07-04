from typing import List, Dict
from pydantic import BaseModel
from openai.agents import tool
from openai.agents.types import RunContextWrapper
from context import UserSessionContext
from guardrails import validate_injury_input

class ProgressEntry(BaseModel):
    date: str
    activity: str
    note: str


class ProgressLog(BaseModel):
    entries: List[ProgressEntry]


@tool(name="track_progress", description="Track user progress, logs, or recovery notes.")
def track_progress(
    user_input: str,
    context: RunContextWrapper[UserSessionContext]
) -> ProgressLog:
    """
    Adds a new progress entry based on user input (e.g., 'Ran 2km today', 'Lost 1kg').
    Stores logs in context for review or future schedule adjustment.
    """

    if not user_input or len(user_input.strip()) < 5:
        raise ValueError("❌ Please enter a valid progress note.")

    # Optional: injury-related validation
    if "injury" in user_input.lower() or "pain" in user_input.lower():
        if not validate_injury_input(user_input):
            raise ValueError("⚠️ Please describe the injury more clearly.")

    # Dummy entry — in production, date would be auto-handled
    entry = ProgressEntry(
        date="2025-07-04",  # Static for now; use datetime.now().date().isoformat() in real use
        activity="General Update",
        note=user_input
    )

    if context.progress_logs is None:
        context.progress_logs = []

    context.progress_logs.append(entry.dict())

    return ProgressLog(entries=context.progress_logs)
