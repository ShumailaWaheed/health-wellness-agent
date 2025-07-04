from typing import Any
from context import UserSessionContext
from openai.agents.types import RunContextWrapper
from guardrails import (
    validate_goal_input,
    validate_diet_input,
    validate_injury_input,
    validate_output_model
)
from pydantic import BaseModel

# Hook before tool is called
def before_tool_call(
    tool_name: str,
    user_input: str,
    context: RunContextWrapper[UserSessionContext]
):
    """
    Hook runs before any tool is invoked.
    Use it to validate input and optionally block bad entries.
    """

    print(f"🔍 Validating input before using tool: {tool_name}")

    if tool_name == "analyze_goal" and not validate_goal_input(user_input):
        raise ValueError("❌ Invalid goal format. Use format like 'lose 5kg in 2 months'.")

    if tool_name == "suggest_meals" and not validate_diet_input(user_input):
        raise ValueError("❌ Unsupported diet preference.")

    if tool_name == "track_progress" and not validate_injury_input(user_input):
        raise ValueError("❌ Injury detail seems unclear or unsupported.")

    print(f"✅ Input validated successfully for {tool_name}")


# Hook after tool is called
def after_tool_call(
    tool_name: str,
    result: Any,
    context: RunContextWrapper[UserSessionContext],
    expected_model: type[BaseModel] = None
):
    """
    Hook runs after any tool finishes.
    You can validate output, log events, or update context here.
    """

    print(f"📦 Tool {tool_name} returned: {result}")

    # Optional model validation (if expected_model is passed)
    if expected_model:
        if not validate_output_model(result, expected_model):
            raise ValueError(f"❌ Tool output from {tool_name} failed structure validation.")

    # Record tool usage (audit trail)
    context.handoff_logs.append(f"✅ Tool used: {tool_name}")

    print(f"📝 {tool_name} output validated and logged.")
