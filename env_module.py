import asyncio
from dataclasses import dataclass
from typing import Optional

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

@dataclass
class ExpenseStepResult:
    observation: ExpenseObservation
    reward: float
    done: bool

class ExpenseEnv:
    def __init__(self):
        self.total = 0.0
        self.steps = 0
        self.max_steps = 10

    @classmethod
    async def from_docker_image(cls, image_name: Optional[str] = None):
        return cls()

    async def reset(self) -> ExpenseStepResult:
        self.total = 0.0
        self.steps = 0
        return ExpenseStepResult(
            observation=ExpenseObservation("System Reset", 0.0, True),
            reward=0.0,
            done=False
        )

    async def step(self, action: ExpenseAction) -> ExpenseStepResult:
        self.steps += 1
        self.total += action.amount
        
        # Simple reward logic based on your prompt
        reward = 0.1 if action.amount > 0 else 0.05
        done = self.steps >= self.max_steps
        
        return ExpenseStepResult(
            observation=ExpenseObservation(f"Executed {action.command}", self.total, True),
            reward=reward,
            done=done
        )

    async def close(self):
        pass


async def main() -> None:
    # Strict requirement: Must use OpenAI client
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    # Initializing the Docker-based OpenEnv environment
    env = await MyEnvV4Env.from_docker_image(IMAGE_NAME)

    history: List[str] = []
    rewards: List[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = await env.reset()
        last_echoed = result.observation.echoed_message
        last_reward = 0.0

        for step in range(1, MAX_STEPS + 1):
            if result.done:
                break

            message = get_model_message(client, step, last_echoed, last_reward, history)

            # Take step in the environment
            result = await env.step(MyEnvV4Action(message=message))
            obs = result.observation

            reward = result.reward or 0.0
            done = result.done
            # Assuming 'error' can be extracted if the action fails or returns an error field
            error = getattr(result, 'last_action_error', None) 

            rewards.append(reward)
            steps_taken = step
            last_echoed = obs.echoed_message
            last_reward = reward

            # Mandatory STDOUT emission after step() returns
            log_step(step=step, action=message, reward=reward, done=done, error=error)

            history.append(f"Step {step}: {message!r} -> reward {reward:+.2f}")

            if done:
                break

        # Calculate final normalized score in the range [0.0, 1.0]
        score = sum(rewards) / MAX_TOTAL_REWARD if MAX_TOTAL_REWARD > 0 else 0.0
        score = min(max(score, 0.0), 1.0)
        success = score >= SUCCESS_SCORE_THRESHOLD
        
    except Exception as e:
        print(f"[DEBUG] Runtime execution error: {e}", flush=True)
    finally:
        try:
            # Mandatory cleanup
            await env.close()
        except Exception as e:
            print(f"[DEBUG] env.close() error (container cleanup): {e}", flush=True)
        
        # Mandatory STDOUT emission after env.close()
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)




        # MOVE THE LOOP HERE (Indented to match the lines above)
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
    
