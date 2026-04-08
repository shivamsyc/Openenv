FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Hugging Face User Setup (Crucial for permissions)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

# 1. Install OpenEnv SDK directly (Ensures no "Module Not Found" error)
RUN pip install --no-cache-dir openenv-core pydantic asyncio uvicorn

# 2. Install your other requirements
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy your project files (env_module.py, openenv.yaml, etc.)
COPY --chown=user . .

# 4. Port for Hugging Face
EXPOSE 7860

# 5. Start the CORRECT server for the Hackathon
CMD ["python", "-m", "openenv.core.server", "--host", "0.0.0.0", "--port", "7860"]
