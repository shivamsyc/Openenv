---
title: OpenEnv
license: mit
---
---
💰 Expense Tracker OpenEnv

An intelligent reinforcement learning environment for tracking personal expenses using an LLM-powered agent.

Built for the Meta PyTorch Hackathon x Scaler School of Technology 🚀
---

📌 Overview

Expense Tracker OpenEnv simulates a real-world expense management system where an agent interacts with an environment to log expenses, stay within budget, and avoid invalid inputs.

The agent uses a Large Language Model (LLM) to decide optimal actions based on the current state.
---
---
🎯 Key Features

- 🤖 LLM-powered intelligent agent
- 🧠 Custom environment with state, reward, and transitions
- 📊 Budget-aware expense tracking
- ⚖️ Reward shaping for realistic behavior
- 🔁 Multiple task difficulty levels
- ⚡ FastAPI-based environment server
---

🧩 Task Variants

Task| Description
ExpenseTracker-v1| Basic expense tracking
ExpenseTracker-v2| Budget-constrained tracking
ExpenseTracker-v3| Strict budget + invalid input handling
---

🧠 Environment Design

📥 Observation Space

{
  "message": "Last action feedback",
  "current_total": 45.0,
  "budget_remaining": 55.0,
  "last_action_success": true
}
---

🎮 Action Space

{
  "command": "food / travel / coffee / rent",
  "amount": 10.5
}
---

🏆 Reward System

Scenario| Reward
Valid expense| +0.5
Invalid amount| -0.5
Unknown category| -0.2
Budget exceeded| -0.3
---

🏗️ Project Structure

.
├── server/
│   ├── app.py              # FastAPI server
│   └── env_module.py      # Custom environment logic
│
├── inference.py           # LLM agent (submission entrypoint)
├── requirements.txt
├── Dockerfile
└── README.md
---

⚙️ Setup & Installation

🔹 1. Clone the repository

git clone https://huggingface.co/spaces/Shivamsyco/OpenEnv1
cd OpenEnv1

---

🔹 2. Install dependencies

pip install -r requirements.txt

---

🔹 3. Run locally (without Docker)

python server/app.py

Server will start at:

http://localhost:7860

---

🔹 4. Test API

- Health check:

GET /health

- Reset environment:

POST /reset

- Step action:

POST /step

---

🐳 Run with Docker (Recommended)

docker build -t expense-env .
docker run -p 7860:7860 expense-env

---

🤖 Running the Agent

python inference.py

This will:

- Connect to environment
- Use LLM to generate actions
- Log results in required format

---

🔑 Environment Variables (for submission)

These are automatically provided during evaluation:

- "API_BASE_URL"
- "API_KEY"
- "MODEL_NAME"

⚠️ Do NOT hardcode these values.

---

📊 Sample Output

[START] task=ExpenseTracker-v1
[STEP] step=1 reward=0.50 done=false
[STEP] step=2 reward=0.70 done=false
[STEP] step=3 reward=0.90 done=true
[END] task=ExpenseTracker-v1 score=0.90 steps=3

---

🚀 Deployment

The project is deployed on Hugging Face Spaces:

👉 https://huggingface.co/spaces/Shivamsyco/OpenEnv1

---

🧪 Evaluation

- Uses structured logging: "[START]", "[STEP]", "[END]"
- Compatible with OpenEnv validator
- Supports multiple tasks with scoring

---

🏁 Future Improvements

- Smarter financial planning strategies
- Category-based expense analytics
- Multi-user support
- Persistent storage (database integration)

---

---

🏆 Acknowledgements

- Meta PyTorch Hackathon
- Scaler School of Technology
- Hugging Face Spaces

---

⭐ If you like this project, feel free to star the repo!
