---
title: OpenEnv
license: mit
---

📊 OpenEnv1: Expense Tracker Environment
This Space provides a Dockerized Reinforcement Learning environment for tracking expenses. It is built using the openenv-core framework and serves as a backend for AI agents to practice structured data logging.

🏗️ Architecture
This project follows a decoupled architecture where the environment (the world) is separated from the inference script (the brain).

Server: Hugging Face Space (Docker)
Framework: openenv-core
Port: 7860
📂 File Structure
Dockerfile: Instructions for building the Python 3.9 environment.
requirements.txt: Lists dependencies (openenv-core, uvicorn, pydantic).
env_module.py: Contains the ExpenseEnv class logic.
openenv.yaml: Configuration that maps the server to the environment class.
🚀 How to use
Once the Space is Running, you can interact with it using an OpenAI-compatible client by pointing it to the Space's direct URL.

Reset the environment to start a new session.
Send actions (commands, categories, and amounts).
Receive rewards and observations.
