from openai.agents import Agent

from tools.tracker import track_progress

injury_support_agent = Agent(
    name="InjurySupportAgent",
    instructions=(
        "You are an injury support assistant. Help users log recovery notes or track pain, "
        "but do not give medical advice. Only assist with recording symptoms and redirecting to experts when needed."
    ),
    tools=[track_progress]
)
