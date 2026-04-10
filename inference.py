import asyncio
from openenv.core.client import OpenEnvClient

async def test_run():
    # This connects to the local server we just built
    client = OpenEnvClient("http://localhost:7860")
    
    print("Testing Environment...")
    obs = await client.reset("ExpenseTracker-v1")
    print(f"Initial Observation: {obs}")
    
    # Try one action
    result = await client.step("ExpenseTracker-v1", {"command": "coffee", "amount": 5.50})
    print(f"Action Result: {result}")

if __name__ == "__main__":
    # This is just for local testing; the server runs the Space
    pass
