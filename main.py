import asyncio
from agent import create_main_agent
from context import initialize_context
from utils.streaming import stream_agent_response

async def main():
    print("🔹 Assistant initialized. Awaiting input...")

    agent = create_main_agent()
    context = initialize_context()

    while True:
        user_input = input("🧘 You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye, stay healthy!")
            break

        print("🤖 Assistant: ", end="", flush=True)
        async for step in stream_agent_response(agent, user_input, context):
            print(step.delta or "", end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
