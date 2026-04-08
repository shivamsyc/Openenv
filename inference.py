
import asyncio
import os
import textwrap
from typing import List, Optional

from openai import OpenAI
# Change Line 8 to:
from env_module import ExpenseAction, ExpenseEnv



# Environment Configuration
IMAGE_NAME = os.getenv("IMAGE_NAME") or os.getenv("LOCAL_IMAGE_NAME")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")

# API Defaults
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

# Benchmark Configuration
TASK_NAME = os.getenv("MY_ENV_V4_TASK", "echo")
BENCHMARK = os.getenv("MY_ENV_V4_BENCHMARK", "my_env_v4")
MAX_STEPS = 8
TEMPERATURE = 0.7
MAX_TOKENS = 150
SUCCESS_SCORE_THRESHOLD = 0.1  # normalized score in [0, 1]

# Max possible reward calculation for reproducibility/normalization
_MAX_REWARD_PER_STEP = MAX_TOKENS * 0.1
MAX_TOTAL_REWARD = MAX_STEPS * _MAX_REWARD_PER_STEP


def log_start(task: str, env: str, model: str) -> None:
    """Emits the mandated [START] line."""
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    """Emits the mandated [STEP] line with lowercase booleans and 2f floats."""
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    """Emits the mandated [END] line with lowercase booleans and required scoring."""
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    success_val = str(success).lower()
    print(
        f"[END] success={success_val} steps={steps} score={score:.2f} rewards={rewards_str}", 
        flush=True
    )


def build_user_prompt(step: int, last_echoed: str, last_reward: float, history: List[str]) -> str:
    """Builds a structured prompt for the LLM to understand environment state."""
    history_block = "\n".join(history[-4:]) if history else "None"
    return textwrap.dedent(
        f"""
        Step: {step}
        Last echoed message: {last_echoed!r}
        Last reward: {last_reward:.2f}
        Previous steps:
        {history_block}
        Send your next message.
        """
    ).strip()


def get_model_message(client: OpenAI, step: int, last_echoed: str, last_reward: float, history: List[str]) -> str:
    """Calls the required OpenAI Client to get the next environment action."""
    user_prompt = build_user_prompt(step, last_echoed, last_reward, history)
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        text = (completion.choices[0].message.content or "").strip()
        # Clean up any quotes the model might have accidentally wrapped its response in
        return text.strip('"').strip("'") if text else "hello"
    except Exception as exc:
        print(f"[DEBUG] Model request failed: {exc}", flush=True)
        return "hello"


SYSTEM_PROMPT = textwrap.dedent(
    """
    You are interacting with a simple echo environment.
    Each turn you must send a message. The environment will echo it back.
    Reward is proportional to message length: reward = len(message) * 0.1
    Your goal is to maximize total reward by sending meaningful, substantive messages.
    Reply with exactly one message string — no quotes, no prefixes, just the message text.
    """
).strip()


async def main() -> None:
    # Strict requirement: Must use OpenAI client
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    # Initializing the Docker-based OpenEnv environment
    env = await ExpenseEnv.from_docker_image(IMAGE_NAME)


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
    
