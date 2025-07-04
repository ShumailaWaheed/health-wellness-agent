import re
from typing import Any
from pydantic import BaseModel, ValidationError

# Input Guardrails

def validate_goal_input(goal_text: str) -> bool:
    """
    Validates goal format like: 'lose 5kg in 2 months', 'gain 3kg in 6 weeks'.
    Returns True if the format is acceptable.
    """
    pattern = r"(lose|gain)\s+\d+(kg|lbs)\s+in\s+\d+\s+(days|weeks|months)"
    return bool(re.fullmatch(pattern, goal_text.strip().lower()))


def validate_diet_input(diet: str) -> bool:
    """
    Accepts only known dietary preferences (basic demo list).
    """
    allowed = ["vegetarian", "vegan", "keto", "paleo", "mediterranean", "low carb", "high protein"]
    return diet.strip().lower() in allowed


def validate_injury_input(injury_text: str) -> bool:
    """
    Checks if the input mentions valid injury types.
    """
    keywords = ["back", "knee", "shoulder", "sprain", "strain", "fracture", "dislocation"]
    return any(word in injury_text.lower() for word in keywords)

# Output Guardrails

def validate_output_model(output: Any, model_class: type[BaseModel]) -> bool:
    """
    Validates that the tool output is a valid instance of the expected Pydantic model.
    Useful for catching bad responses or missing fields.
    """
    try:
        model_class.parse_obj(output)
        return True
    except ValidationError as e:
        print(f"❌ Output validation failed: {e}")
        return False
