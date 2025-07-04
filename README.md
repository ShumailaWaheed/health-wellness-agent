# 🧠 Health & Wellness Planner Agent (OpenAI Agents SDK + Streamlit)

This project is a full-stack Health & Wellness Planner built using the **OpenAI Agents SDK**, `pydantic`, and `streamlit`. It includes tools for fitness goals, meal planning, workouts, tracking, and multi-agent escalation support.

---

## 🚀 Features

✅ Fitness goal analysis  
✅ Meal suggestions based on diet  
✅ Workout recommendations by fitness level  
✅ Weekly schedule generator  
✅ Progress + recovery tracker  
✅ Context memory for multi-turn interaction  
✅ Specialized expert agents (Nutrition, Injury, Escalation)  
✅ Live streaming via Streamlit

---

## 📁 Folder Structure

```
health_wellness_agent/
│
├── main.py                  # Main planner agent + tools + context
├── streamlit_app.py         # Streamlit UI frontend
├── requirements.txt         # All dependencies
├── README.md                # This file
│
├── context.py               # Shared RunContextWrapper + BaseModel
├── guardrails.py            # Input/output validators
├── hooks.py                 # Placeholder for tool/agent lifecycle hooks
│
├── tools/
│   ├── goal_analyzer.py
│   ├── meal_planner.py
│   ├── workout_recommender.py
│   ├── scheduler.py
│   └── tracker.py
│
├── agents/
│   ├── nutrition_expert_agent.py
│   ├── injury_support_agent.py
│   └── escalation_agent.py
│
└── utils/
    └── streaming.py
```

---

## 🛠️ Installation & Setup

```bash
# Step 1: Create virtual environment using uv
uv venv

# Step 2: Install dependencies
uv pip install -r requirements.txt

# Step 3: Run the app
streamlit run streamlit_app.py
```

Make sure you have access to the OpenAI SDK and a valid API key if needed.

---

## ✨ Example Queries to Try

- `lose 5kg in 2 months`  
- `vegan diet suggestions`  
- `I'm a beginner, suggest a workout`  
- `track: I completed yoga today`  
- `I feel pain in my left knee, please log it`

---

## 🧩 Powered By

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Streamlit](https://streamlit.io)
- [Pydantic](https://docs.pydantic.dev)

---

## 📬 Contact

For improvements or feedback, open an issue or contribute directly.

---

**License:** MIT
