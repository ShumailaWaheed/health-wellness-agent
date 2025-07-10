from datetime import datetime

class EscalationAgent:
    def run_tools(self, input_data, context):
        # Get user ID from context, if available
        if isinstance(context, dict):
            user_id = context.get("user_id", "unknown")
        else:
            user_id = "unknown"

        # Message to inform user that escalation is needed
        message = (
            "⚠️ Your request may require review by a qualified health expert.\n"
            f"User ID: {user_id}\n"
            "Please consult a licensed professional for detailed advice."
        )

        # Prepare the response with escalation details
        response = {
            "message": "Request escalated to human expert.",
            "escalation_id": str(datetime.now().timestamp()),
            "input": input_data,
            "timestamp": datetime.now().isoformat(),
            "details": message
        }

        return response
