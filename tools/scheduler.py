from openai_agents import Tool
from context import UserSessionContext
from guardrails import validate_output
import asyncio

class CheckinSchedulerTool(Tool):
    def __init__(self):
        super().__init__(name="CheckinSchedulerTool")

    def should_trigger(self, input_text: str, context: UserSessionContext) -> bool:
        return "schedule" in input_text.lower() or "checkin" in input_text.lower()

    async def execute(self, input_text: str, context: UserSessionContext) -> dict:
        await asyncio.sleep(1)  # Simulate async processing
        schedule = {"checkin": "Weekly progress check scheduled for every Monday"}
        context.progress_logs.append({"event": "Scheduled weekly checkin", "timestamp": "now"})
        return validate_output({"schedule": schedule}, context)