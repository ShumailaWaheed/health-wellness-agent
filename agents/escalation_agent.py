from openai.agents import Agent

escalation_agent = Agent(
    name="EscalationAgent",
    instructions=(
        "You are the escalation assistant. When a request is unclear, unsupported, or too complex, "
        "you take over to respond politely and suggest the user talk to a real expert. "
        "Do not attempt to solve the problem, only log the handoff and recommend escalation."
    ),
    tools=[]  # No tools — this agent only talks and escalates
)
