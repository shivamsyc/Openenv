FROM python:3.11-slim

# 1. Install 'uv' – the tool your friend is using
RUN pip install --no-cache-dir uv

WORKDIR /code

# 2. Copy your configuration files
COPY pyproject.toml .
COPY requirements.txt .

# 3. Generate the lock file during the build
RUN uv lock

# 4. Install everything using the new lock file
RUN uv pip install --system -r requirements.txt

# 5. Copy the rest of your code
COPY . .

ENV PYTHONPATH=/code

# 6. Launch
CMD ["python3", "app.py"]
