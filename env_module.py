import asyncio
from dataclasses import dataclass
from typing import Optional

@dataclass
class ExpenseObservation:
    message: str
    current_total: float
    success: bool

class ExpenseEnv:
    def __init__(self):
        self.total = 0.0
        self.steps = 0
        self.max_steps = 10

    @classmethod
    async def from_docker_image(cls, image_name: Optional[str] = None):
        return cls()

    async def reset(self):
        self.total = 0.0
        self.steps = 0
        # Return a simple dictionary (OpenEnv server converts this for you)
        return {
            "observation": {"message": "System Reset", "current_total": 0.0, "success": True},
            "reward": 0.0,
            "done": False
        }

    async def step(self, action):
        # 'action' comes in as a dictionary from the server
        amount = action.get("amount", 0.0)
        command = action.get("command", "none")
        
        self.steps += 1
        self.total += amount
        
        reward = 0.1 if amount > 0 else 0.05
        done = self.steps >= self.max_steps
        
        return {
            "observation": {"message": f"Executed {command}", "current_total": self.total, "success": True},
            "reward": reward,
            "done": done
        }

    async def close(self):
        pass
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
    
