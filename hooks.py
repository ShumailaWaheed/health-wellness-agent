from openai_agents import RunHooks
from context import UserSessionContext

class CustomRunHooks(RunHooks):
    def on_agent_start(self, agent_name: str, context: UserSessionContext):
        context.progress_logs.append({"event": f"Agent {agent_name} started", "timestamp": "now"})

    def on_agent_end(self, agent_name: str, context: UserSessionContext):
        context.progress_logs.append({"event": f"Agent {agent_name} ended", "timestamp": "now"})

    def on_tool_start(self, tool_name: str, input_data: str, context: UserSessionContext):
        context.progress_logs.append({"event": f"Tool {tool_name} started with input: {input_data}", "timestamp": "now"})

    def on_tool_end(self, tool_name: str, output_data: dict, context: UserSessionContext):
        context.progress_logs.append({"event": f"Tool {tool_name} ended with output: {output_data}", "timestamp": "now"})

    def on_handoff(self, target_agent: str, context: UserSessionContext):
        context.handoff_logs.append(f"Handoff to {target_agent} triggered")