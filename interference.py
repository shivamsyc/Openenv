import asyncio
from env_module import ExpenseEnv, ExpenseAction

async def main():
    # Initialize your new environment
    env = ExpenseEnv("my_expenses.csv")
    env.reset()

    # Example Action: Log Coffee
    action = ExpenseAction(command="log", category="Food", amount=5.50)
    obs, reward, done, info = env.step(action)
    
    print(f"[START] task=log_single_coffee env=ExpenseTracker model=local")
    print(f"[STEP] step=1 action=log_coffee reward={reward:.2f} done={str(done).lower()} error=null")
    print(f"[END] success={str(done).lower()} steps=1 score={reward} rewards={reward:.2f}")

    # Keep the space running
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
  
