# 🧠 Health & Wellness Agent

An AI-powered assistant that helps users set and achieve their health goals through CLI, Streamlit Dashboard, and Chainlit Chatbot interfaces.

---

## 🔹 Overview

This project simulates a real-world digital wellness coach using the OpenAI Agents SDK and Gemini API, allowing users to:

- Define structured health goals  
- Receive personalized meal and fitness plans  
- Interact via terminal, web UI, or chatbot  
- Be auto-referred to specialists (injury, nutrition, escalation)  
- Generate reports and schedule follow-ups  

---

## 💪 Key Features

- 🎯 Goal Analysis (e.g., “Lose 5kg in 2 months”)  
- 🍱 Personalized Meal & Workout Plans  
- 🛡️ Input/Output Guardrails using Pydantic  
- 🔁 Real-time streaming (CLI & Chat)  
- 👥 Agent handoffs (Nutrition, Injury, Human escalation)  
- ⏰ Weekly reminders & ⬇️ PDF exports  
- 🌐 Interfaces: CLI + Streamlit + Chainlit  
- 🔄 State management using `UserSessionContext`  

---

## 🧭 Interfaces

### CLI Agent
Run:
```bash
python main.py
```
- Natural goal conversation  
- Streamed AI advice  
- Expert agent handoffs  

---

### Streamlit Dashboard
Run:
```bash
streamlit run streamlit_app.py
```
- Log in or register  
- Submit health goals  
- View & download plans  
- Email notifications & reminders  

---

### Chainlit Chatbot
Run:
```bash
chainlit run chainlit_agent.py
```
- Chat in real-time  
- Auto detect queries needing specialist input  
- Smart buttons (e.g., “Schedule Call”)  

---

## 🛠️ Tools Used

- `GoalAnalyzerTool`: Extracts structured goals from user input  
- `MealPlannerTool`: Suggests a weekly meal plan  
- `WorkoutRecommenderTool`: Generates exercise plans  
- `CheckinSchedulerTool`: Logs weekly check-ins  
- `ProgressTrackerTool`: Tracks health improvements  

---

## 👥 Specialized Agents

| Agent                | Trigger Keyword Examples        |
|---------------------|---------------------------------|
| EscalationAgent      | “real trainer”, “talk to someone” |
| NutritionExpertAgent | “diet”, “nutrition”, “vegan”     |
| InjurySupportAgent   | “pain”, “injury”, “knee”         |

---

## 🔒 Input & Output Guardrails

- Input validator checks:
  - Goals like `"Lose 5kg in 2 months"`
  - Keywords like `"vegetarian"`, `"pain"`  
- Output validator ensures structured dicts from all tools  

---

## 📥 Setup Instructions

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\\Scripts\\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
echo "GEMINI_API_KEY=your-api-key" > .env
```

---

## 🧪 Sample Conversations

```
User: I want to lose 5kg in 2 months  
→ GoalAnalyzerTool triggers  

User: I'm vegetarian with diabetes  
→ MealPlannerTool + NutritionExpertAgent triggered  

User: I have knee pain and can't do squats  
→ InjurySupportAgent takes over  

User: I want to talk to a real coach  
→ EscalationAgent connects to human  
```

---

## 🧠 Technologies Used

- Python 3.11+  
- OpenAI Agents SDK  
- Google Gemini API  
- Chainlit  
- Streamlit  
- Pydantic  
- Asyncio  

---

## 📜 License

Educational use only – built for GIAIC AI assignment (Governor Sindh’s Gen AI Initiative).  

---

## 🙋‍♀️ Credits

Created by **Shumaila** with support from OpenAI's guidance and GIAIC curriculum.  
Need help? Email: `Shumailawaheed253@gmail.com`
