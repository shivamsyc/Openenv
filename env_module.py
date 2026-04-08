import asyncio
from dataclasses import dataclass
from typing import Optional, List

@dataclass
class MyEnvV4Observation:
    echoed_message: str

@dataclass
class MyEnvV4Action:
    message: str

@dataclass
class MyEnvV4StepResult:
    observation: MyEnvV4Observation
    reward: float
    done: bool
    last_action_error: Optional[str] = None

class MyEnvV4Env:
    def __init__(self):
        self.steps = 0
        self.max_steps = 8
        self.done = False

    @classmethod
    async def from_docker_image(cls, image_name: Optional[str] = None):
        """Standard OpenEnv factory method."""
        return cls()

    async def reset(self) -> MyEnvV4StepResult:
        """Resets the environment to initial state."""
        self.steps = 0
        self.done = False
        return MyEnvV4StepResult(
            observation=MyEnvV4Observation(echoed_message="Welcome!"),
            reward=0.0,
            done=False
        )

    async def step(self, action: MyEnvV4Action) -> MyEnvV4StepResult:
        """Processes the LLM's message and returns reward."""
        self.steps += 1
        
        # Logic: Reward is length of message * 0.1
        msg_len = len(action.message)
        reward = msg_len * 0.1
        
        if self.steps >= self.max_steps:
            self.done = True
            
        return MyEnvV4StepResult(
            observation=MyEnvV4Observation(echoed_message=action.message),
            reward=reward,
            done=self.done
        )

    async def close(self):
        """Cleanup logic."""
        print("[DEBUG] Environment closed successfully.")
        
