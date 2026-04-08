


1. Define the Data Models
First, we define the "language" of environment.

from dataclasses import dataclass
from datetime import datetime
from openenv.core.env_server import Action, Observation, State

@dataclass
class ExpenseAction(Action):
    command: str  # "log" or "view_total"
    category: str = "General"
    amount: float = 0.0

@dataclass
class ExpenseObservation(Observation):
    message: str
    current_total: float
    success: bool

@dataclass
class ExpenseState(State):
    filename: str = "expenses.csv"
    last_action_time: str = ""

2. The Environment Class
We wrap your logic into the ExpenseEnv class. Instead of input() and print(), we use the Action object to receive data and the Observation object to send it back.

import csv
import os
from openenv.core.env_server import Environment

class ExpenseEnv(Environment):
    def __init__(self, filename="expenses.csv"):
        super().__init__()
        self._state = ExpenseState(filename=filename)

    
        if not os.path.exists(filename):
            with open(filename, 'w', newline='') as f:
                csv.writer(f).writerow(["Date", "Category", "Amount"])

    def reset(self) -> ExpenseObservation:
        self._state.last_action_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return ExpenseObservation(
            message="Environment Reset. Ready to log expenses.",
            current_total=self._get_total(),
            success=True
        )

        def step(self, action: ExpenseAction):
        self._state.last_action_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        

        
        obs = ExpenseObservation(
            message=f"Logged ${action.amount}",
            current_total=self._get_total(),
            success=True
        )

        # Calculate reward and check if done (Step 2/3 logic)
        reward = 1.0 if obs.success else 0.0
        done = False  # The orchestrator usually decides when the task is finished
        info = {}     # Extra data if needed

        return obs, reward, done, info
        
    def _get_total(self) -> float:
        total = 0.0
        try:
            with open(self._state.filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader) # Skip header
                for row in reader:
                    if row: total += float(row[2])
        except (FileNotFoundError, StopIteration, ValueError):
            pass
        return total

    @property
    def state(self) -> ExpenseState:
        return self._state

3. Running and Testing
You can now interact with your environment programmatically. This is exactly how an AI agent would "play" your expense manager.

# 1. Setup
env = ExpenseEnv("my_expenses.csv")
env.reset()

# 2. Agent takes an action: Log Coffee
action_1 = ExpenseAction(command="log", category="Food", amount=5.50)
obs_1 = env.step(action_1)
print(f"Action 1: {obs_1.message} | New Total: ${obs_1.current_total}")

