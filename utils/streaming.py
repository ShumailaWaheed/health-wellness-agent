from typing import AsyncGenerator, Any
from openai.agents.runner import Runner
from openai.agents.types import RunStep
from openai.agents import Agent
from openai.agents.types import RunContextWrapper
from context import UserSessionContext

# Stream response helper
async def stream_agent_response(
    agent: Agent,
    user_input: str,
    context: RunContextWrapper[UserSessionContext]
) -> AsyncGenerator[RunStep, Any]:
    """
    Streams the agent's response token by token using OpenAI's Runner.stream().
    Can be used in Streamlit or any async frontend.
    """

    async for step in Runner.stream(
        starting_agent=agent,
        input=user_input,
        context=context
    ):
        yield step
