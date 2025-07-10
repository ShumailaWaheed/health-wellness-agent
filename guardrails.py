
from pydantic import BaseModel, ValidationError
from typing import Optional
import re
from context import UserSessionContext

class ValidationResult(BaseModel):
    is_valid: bool
    message: Optional[str] = None

def validate_input(input_text: str, context: UserSessionContext) -> ValidationResult:
    # Validate goal format (e.g., "lose 5kg in 2 months")
    goal_pattern = r"^(lose|gain)\s+(\d+\.?\d*)\s*(kg|lbs|pounds)\s*in\s*(\d+)\s*(month|week)s?$"
    if "lose" in input_text.lower() or "gain" in input_text.lower():
        if not re.match(goal_pattern, input_text.lower()):
            return ValidationResult(is_valid=False, message="Goal must be in format: 'lose/gain X kg/lbs in Y months/weeks'")
    
    # Validate dietary preferences
    if "vegetarian" in input_text.lower() or "vegan" in input_text.lower():
        context.diet_preferences = input_text.lower()
    
    # Validate injury notes
    if any(keyword in input_text.lower() for keyword in ["pain", "injury"]):
        context.injury_notes = input_text
    
    return ValidationResult(is_valid=True)

def validate_output(output: dict, context: UserSessionContext) -> dict:
    try:
        # Ensure output is structured (e.g., JSON or Pydantic model)
        if not isinstance(output, dict):
            return {"error": "Output must be a dictionary"}
        return output
    except ValidationError as e:
        return {"error": f"Output validation failed: {str(e)}"}
