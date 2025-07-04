import streamlit as st
import asyncio
from agent import create_main_agent
from context import initialize_context
from utils.streaming import stream_agent_response

# Page configuration
st.set_page_config(page_title="Health & Wellness Planner 💪", layout="centered")
st.title("🧘 Health & Wellness Assistant")
st.markdown("Ask me anything about your health goals, diet, workouts, or wellness routines.")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.chat_input("Type your health or fitness question...")

# If user entered something
if user_input:
    # Display user's message
    with st.chat_message("user"):
        st.markdown(user_input)

    # Store it in chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # Initialize agent and context
    agent = create_main_agent()
    context = initialize_context()

    # Placeholder for assistant's message
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        response_tokens = []

        async def get_response():
            async for step in stream_agent_response(agent, user_input, context):
                response_tokens.append(step.delta or "")
                response_placeholder.markdown("".join(response_tokens) + "▌")

        # Run the async function inside Streamlit
        asyncio.run(get_response())

        # Final assistant message (without the cursor)
        full_response = "".join(response_tokens)
        response_placeholder.markdown(full_response)

        # Save response to chat history
        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
