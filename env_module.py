import asyncio
from dataclasses import dataclass
from typing import Optional

# These MUST be imported for the server to recognize them
from openenv.core.env_server import Action, Observation, State

@dataclass
class ExpenseObservation:
    message: str
    current_total: float
    success: bool

@dataclass
class ExpenseAction:
    command: str
    category: str = "General"
    amount: float = 0.0

class ExpenseEnv: # This name MUST match openenv.yaml
    def __init__(self):
        self.total = 0.0
        self.steps = 0
        self.max_steps = 10

    def reset(self):
        self.total = 0.0
        self.steps = 0
        # Return: obs, reward, done, info
        return ExpenseObservation("Reset complete", 0.0, True), 0.0, False, {}

    def step(self, action: ExpenseAction):
        self.steps += 1
        self.total += action.amount
        done = self.steps >= self.max_steps
        obs = ExpenseObservation(f"Logged {action.amount}", self.total, True)
        return obs, 1.0, done, {}
        

    async def close(self):
        """Cleanup logic."""
        print("[DEBUG] Environment closed successfully.")
        
