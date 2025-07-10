import streamlit as st
import uuid
import re
import os
import pytz
import requests
from datetime import datetime
from dotenv import load_dotenv

from context import UserSessionContext
from utils.user_auth import UserAuth
from utils.profile_manager import ProfileManager
from utils.notifications import send_progress_email
from utils.reminder_scheduler import schedule_reminder
from utils.progress_chart import generate_progress_chart
from utils.feedback import collect_feedback
from utils.export_pdf import generate_progress_report

# Load API keys and configuration from .env
load_dotenv(os.path.join(os.path.dirname(__file__), 'api.env'))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = os.getenv("GEMINI_API_URL")

# Call Gemini API for AI-generated plans
def call_gemini_api(prompt: str) -> str:
    if not GEMINI_API_KEY or not GEMINI_API_URL:
        return "❌ Gemini API configuration missing in .env"

    try:
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(f"{GEMINI_API_URL}?key={GEMINI_API_KEY}", json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response from Gemini")
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Try to extract structured goal info
def parse_goal_input(text: str) -> str:
    pattern = r"(lose|gain)\s*(\d+\.?\d*)\s*(kg|lbs)\s*in\s*(\d+)\s*(months|weeks)"
    match = re.search(pattern, text.lower())
    return f"{match[1]} {match[2]} {match[3]} in {match[4]} {match[5]}" if match else text

# Get current time in PKT
def get_pkt_time() -> str:
    return datetime.now(pytz.timezone('Asia/Karachi')).isoformat()

# ---------- UI Styling ----------
st.markdown("""
    <style>
    .main {
        background-color: #1a1a2e;
        color: #f1f2f6;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    .stButton>button {
        background-color: #2e86de;
        color: white;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 500;
        border: none;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #54a0ff;
        transform: translateY(-2px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .stTextInput>div>input, .stTextArea>div>textarea {
        background-color: #16213e;
        color: #f1f2f6;
        border: 1px solid #2d3436;
        border-radius: 8px;
        padding: 10px;
    }
    h1, h2, h3 {
        color: #2e86de;
        font-weight: 600;
    }
    .stExpander, .stTabs [data-baseweb="tab-list"], .stRadio [role="radiogroup"] {
        background-color: #16213e;
        border-radius: 8px;
        border: 1px solid #2d3436;
    }
    hr {
        border-color: #2d3436;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- Initialize State ----------
if "context" not in st.session_state:
    st.session_state.context = UserSessionContext(
        uid=uuid.uuid4().int & (1 << 31) - 1,
        name="User",
        email="",
        diet_preferences=[],
        health_conditions=[],
        goal=None,
        progress_logs=[],
        handoff_logs=[]
    )
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

# ---------- Services ----------
auth = UserAuth()
profile_manager = ProfileManager()

# ---------- Sidebar ----------
st.sidebar.title("⚕️ SmartCare Health & Wellness Planner")
page = st.sidebar.radio("Navigation", ["Dashboard", "Profile", "Progress Analytics", "Alerts"]) if st.session_state.is_authenticated else "Dashboard"

# ---------- Dashboard ----------
if page == "Dashboard":
    st.title("🌱 SmartCare Health & Wellness Planner")

    if not st.session_state.is_authenticated:
        st.markdown("Log in or register to start your wellness journey.")
        with st.expander("🔐 Authentication", expanded=True):
            action_type, inputs = st.columns([1, 2])
            action = action_type.radio("Choose Action", ["Login", "Register"])

            if action == "Register":
                username = inputs.text_input("Username*", placeholder="JohnDoe")
            else:
                username = None

            email = inputs.text_input("Email*", placeholder="you@example.com")
            password = inputs.text_input("Password*", type="password", placeholder="Your password")

            if st.button("Authenticate"):
                with st.spinner("Processing..."):
                    result = auth.register_user(username, email, password) if action == "Register" else auth.authenticate_user(email, password)

                    if result.get("message"):
                        st.session_state.is_authenticated = True
                        st.session_state.context.uid = result.get("uid", st.session_state.context.uid)
                        st.session_state.context.name = username or result.get("username", "User")
                        st.session_state.context.email = email
                        st.success(f"✅ {result['message']}")
                        st.rerun()
                    else:
                        st.error(f"⚠️ {result.get('error', 'Authentication failed')}")
    else:
        st.markdown("Describe your health goals or ask for a custom plan.")
        with st.expander("🎯 Set Health Goal"):
            st.markdown("Examples: 'Lose 5kg in 3 months', 'What are low-sugar meals?'")
            user_input = st.text_area("Your Goal or Question*", placeholder="E.g., 'Lose 5kg in 3 months with joint pain'")

            if st.button("Generate Plan"):
                if not user_input:
                    st.warning("Please enter something.")
                else:
                    with st.spinner("Generating plan..."):
                        structured_goal = parse_goal_input(user_input)
                        st.session_state.context.goal = structured_goal
                        st.session_state.context.timestamp = get_pkt_time()

                        prompt = (
                            f"User input: {structured_goal}\n"
                            f"Diet: {st.session_state.context.diet_preferences}\n"
                            f"Health Issues: {st.session_state.context.health_conditions}\n"
                            "Generate a detailed weekly health plan including meals, workouts, injury support, and tips."
                        )

                        response = call_gemini_api(prompt)

                        if "Error" not in response:
                            st.markdown("### 🧠 Your AI-Powered Plan")
                            st.markdown(response)
                            st.session_state.context.handoff_logs.append(f"{get_pkt_time()} | {user_input} -> {response}")
                            st.success("✅ Plan Ready!")
                        else:
                            st.error(response)

# ---------- Profile Page ----------
elif page == "Profile":
    st.title("👤 Profile Management")
    with st.expander("🔄 Update Your Profile"):
        col1, col2 = st.columns(2)
        name = col1.text_input("Name*", value=st.session_state.context.name)
        email = col1.text_input("Email*", value=st.session_state.context.email)
        preferences = col2.multiselect("Dietary Preferences", ["Vegetarian", "Vegan", "Gluten-Free", "Keto"], default=st.session_state.context.diet_preferences)
        conditions = col2.multiselect("Health Conditions", ["Diabetes", "Joint Issues", "Hypertension"], default=st.session_state.context.health_conditions)

        if st.button("Save Profile"):
            if name and email:
                pref_str = ", ".join(preferences)
                result = profile_manager.update_profile(st.session_state.context, name, email, pref_str)
                if result.get("message"):
                    st.session_state.context.name = name
                    st.session_state.context.email = email
                    st.session_state.context.diet_preferences = preferences
                    st.session_state.context.health_conditions = conditions
                    st.success(f"✅ {result['message']}")
                else:
                    st.error(f"⚠️ {result.get('error', 'Could not update profile')}")
            else:
                st.error("⚠️ Name and email are required.")

# ---------- Progress Analytics ----------
elif page == "Progress Analytics":
    st.title("📊 Progress Analytics")

    with st.expander("📄 Generate Reports"):
        col1, col2 = st.columns(2)

        if col1.button("Download PDF Report"):
            with st.spinner("Generating report..."):
                st.session_state.context.timestamp = get_pkt_time()
                result = generate_progress_report(st.session_state.context)
                if result.get("message"):
                    st.download_button(
                        label="Download PDF",
                        data=result["content"].encode(),
                        file_name=f"progress_report_{get_pkt_time()}.tex",
                        mime="text/latex"
                    )
                    st.success("📄 Report ready!")
                else:
                    st.error("⚠️ Failed to generate report.")

        if col2.button("Export Logs"):
            st.success("📤 Logs exported successfully (placeholder)")

    with st.tabs(["🗂️ Consultations", "📆 Timeline"]) as (tab1, tab2):
        with tab1:
            if not st.session_state.context.handoff_logs:
                st.info("No consultations yet.")
            else:
                for log in st.session_state.context.handoff_logs:
                    st.markdown(f"<div style='background: #16213e; padding: 10px; border-radius: 8px;'>{log}</div>", unsafe_allow_html=True)
        with tab2:
            if not st.session_state.context.progress_logs:
                st.info("No progress logs.")
            else:
                for log in st.session_state.context.progress_logs:
                    st.markdown(f"<div style='background: #16213e; padding: 10px; border-radius: 8px;'>📅 {log['timestamp']}: {log['event']}</div>", unsafe_allow_html=True)

# ---------- Alerts ----------
elif page == "Alerts":
    st.title("🔔 Notification Center")

    with st.expander("✉️ Email Notifications"):
        col1, col2 = st.columns(2)
        email = col1.text_input("Email*", value=st.session_state.context.email)
        frequency = col1.selectbox("Frequency", ["Weekly", "Bi-Weekly", "Monthly"])
        types = col2.multiselect("Notify About", ["Progress", "Nutrition", "Exercise"])

        if st.button("Save Email Settings"):
            if email:
                result = send_progress_email(st.session_state.context, email, "smtp.gmail.com", 587, "your_email@gmail.com", "your_app_password")
                st.success(f"✉️ {result['message']}")
            else:
                st.error("⚠️ Email is required.")

    with st.expander("⏰ Set Reminder"):
        col1, col2 = st.columns(2)
        reminder_type = col1.selectbox("Type", ["Medication", "Exercise", "Meal"])
        time = col1.time_input("Time")
        days = col2.multiselect("Days", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], default=["Mon", "Wed", "Fri"])
        method = col2.radio("Notify By", ["Email", "In-App"])

        if st.button("Save Reminder"):
            result = schedule_reminder(st.session_state.context, time, email, "smtp.gmail.com", 587, "your_email@gmail.com", "your_app_password")
            st.success(f"⏰ {result['message']}")

# ---------- Footer ----------
st.markdown(f"<div style='text-align: center; color: #a4b0be;'>© {datetime.now().year} HealthSync Wellness | Last updated: {get_pkt_time()}</div>", unsafe_allow_html=True)

# ---------- Sidebar Help ----------
st.sidebar.markdown("""
### 📝 Quick Start Guide
- Log in to get started
- Set health goals for custom plans
- Update your profile for better recommendations
- Set reminders to stay on track
""")
