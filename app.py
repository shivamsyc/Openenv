from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv
import os
from datetime import datetime
from typing import Dict, Any

app = FastAPI(title="Expense Tracker OpenEnv", version="1.0.0")
CSV_FILE = 'expenses.csv'

# Ensure the CSV exists with headers
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Category', 'Description', 'Amount'])

class StepRequest(BaseModel):
    action: Dict[str, Any]

@app.post("/reset")
async def reset():
    # To reset, we just clear the CSV and start fresh
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Category', 'Description', 'Amount'])
    return {"message": "Environment reset. CSV cleared.", "current_total": 0}

@app.post("/step")
async def step(req: StepRequest):
    try:
        # Instead of input(), we get data from the 'action' dictionary
        action = req.action
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        category = action.get("category", "General")
        description = action.get("description", "No description")
        amount = float(action.get("amount", 0))

        # Write to the CSV file
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, category, description, amount])

        # Calculate the new total for the observation
        total = 0
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                total += float(row['Amount'])

        return {
            "observation": {
                "message": f"Added {description}",
                "current_total": total
            },
            "reward": 1.0,
            "done": False
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
def health():
    return {"status": "ok"}

# Required for the 'server = app:main' entry point in pyproject.toml
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
      
