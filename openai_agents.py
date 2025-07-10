
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, AsyncGenerator
from context import UserSessionContext

class Agent(ABC):
    def __init__(self, name: Optional[str] = None, tools: Optional[List[Any]] = None, 
                 handoffs: Optional[Dict[str, Any]] = None, hooks: Optional[Any] = None):
        self.name = name or "Agent"
        self.tools = tools or []
        self.handoffs = handoffs or {}
        self.hooks = hooks

    @abstractmethod
    async def process_input(self, input_text: str, context: UserSessionContext) -> Dict[str, Any]:
        pass  # type: ignore

    @abstractmethod
    async def run_tools(self, input_text: str, context: UserSessionContext) -> Dict[str, Any]:
        pass  # type: ignore

    async def handoff(self, target_agent: str, input_text: str, context: UserSessionContext) -> Dict[str, Any]:
        if target_agent in self.handoffs:
            if self.hooks:
                self.hooks.on_handoff(target_agent, context)
            return await self.handoffs[target_agent].process_input(input_text, context)
        return {"error": f"No such agent: {target_agent}"}

    def on_handoff(self, _target_agent: str, _input_text: str, _context: UserSessionContext) -> None:
        pass  # type: ignore

class Tool(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def should_trigger(self, _input_text: str, _context: UserSessionContext) -> bool:
        pass  # type: ignore

    @abstractmethod
    async def execute(self, _input_text: str, _context: UserSessionContext) -> Any:
        pass  # type: ignore

class Runner:
    @staticmethod
    async def stream(starting_agent: Any, input_text: str, context: UserSessionContext) -> AsyncGenerator[Any, None]:
        class Step:
            def __init__(self, output: str):
                self.pretty_output = output
        response = await starting_agent.process_input(input_text, context)
        yield Step(str(response))

class RunHooks:
    def on_agent_start(self, _agent_name: str, _context: UserSessionContext) -> None:
        pass  # type: ignore

    def on_agent_end(self, _agent_name: str, _context: UserSessionContext) -> None:
        pass  # type: ignore

    def on_tool_start(self, _tool_name: str, _input_data: Any, _context: UserSessionContext) -> None:
        pass  # type: ignore

    def on_tool_end(self, _tool_name: str, _output_data: Any, _context: UserSessionContext) -> None:
        pass  # type: ignore

    def on_handoff(self, _target_agent: str, _context: UserSessionContext) -> None:
        pass  # type: ignore

class AgentHooks:
    def on_start(self, _context: UserSessionContext) -> None:
        pass  # type: ignore

    def on_end(self, _context: UserSessionContext) -> None:
        pass  # type: ignore

    def on_tool_start(self, _tool_name: str, _input_data: Any, _context: UserSessionContext) -> None:
        pass  # type: ignore

    def on_tool_end(self, _tool_name: str, _output_data: Any, _context: UserSessionContext) -> None:
        pass  # type: ignore

    def on_handoff(self, _target_agent: str, _context: UserSessionContext) -> None:
        pass  # type: ignore
