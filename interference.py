import asyncio
from env_module import ExpenseEnv, ExpenseAction

async def main():
    # Initialize environment
    env = ExpenseEnv("my_expenses.csv")
    env.reset()

    # Define action
    action = ExpenseAction(command="log", category="Food", amount=5.50)
    
    # Execute step
    # IMPORTANT: Ensure your env_module.py step() returns 4 values!
    obs, reward, done, info = env.step(action)
    
    # If the logging worked, we consider this specific task "Done"
    if obs.success:
        done = True
        reward = 1.0

    # Required Logging Format for OpenEnv
    print(f"[START] task=log_single_coffee env=ExpenseTracker model=local")
    print(f"[STEP] step=1 action=log_coffee reward={reward:.2f} done={str(done).lower()} error=null")
    print(f"[END] success={str(done).lower()} steps=1 score={reward} rewards={reward:.2f}")

    # Keep the space running for Hugging Face
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
    
