FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set up user
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app

# Install dependencies
RUN pip install --no-cache-dir openenv-core pydantic asyncio

COPY --chown=user requirements.txt $HOME/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user . $HOME/app

# IMPORTANT: This runs the server so the "Reset" POST command works
CMD ["python", "-m", "openenv.core.server", "--host", "0.0.0.0", "--port", "7860"]
