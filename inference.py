import asyncio
from dataclasses import dataclass
from typing import Optional

@dataclass
class ExpenseObservation:
    echoed_message: str

@dataclass
class ExpenseAction:
    message: str

@dataclass
class ExpenseStepResult:
    observation: ExpenseObservation
    reward: float
    done: bool

class ExpenseEnv:
    def __init__(self):
        self.steps = 0
        self.max_steps = 8
        self.done = False

    @classmethod
    async def from_docker_image(cls, image_name: Optional[str] = None):
        return cls()

    async def reset(self) -> ExpenseStepResult:
        self.steps = 0
        self.done = False
        return ExpenseStepResult(
            observation=ExpenseObservation(echoed_message="Welcome!"),
            reward=0.0,
            done=False
        )

    async def step(self, action: ExpenseAction) -> ExpenseStepResult:
        self.steps += 1
        reward = len(action.message) * 0.1
        if self.steps >= self.max_steps:
            self.done = True
        return ExpenseStepResult(
            observation=ExpenseObservation(echoed_message=action.message),
            reward=reward,
            done=self.done
        )

    async def close(self):
        pass
    
