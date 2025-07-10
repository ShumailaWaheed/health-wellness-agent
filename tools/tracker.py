from openai_agents import Tool
from context import UserSessionContext
from guardrails import validate_output
import asyncio
class ProgressTrackerTool(Tool):
    def __init__(self):
        super().__init__(name="ProgressTrackerTool")

    def should_trigger(self, input_text: str, context: UserSessionContext) -> bool:
        return "progress" in input_text.lower() or "update" in input_text.lower()

    async def execute(self, input_text: str, context: UserSessionContext) -> dict:
        await asyncio.sleep(1)  # Simulate async processing
        progress_update = {"update": input_text, "timestamp": "now"}
        context.progress_logs.append(progress_update)
        return validate_output({"progress": progress_update}, context)