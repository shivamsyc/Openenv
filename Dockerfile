
FROM ghcr.io/meta-pytorch/openenv-core:latest

# Set up user permissions (Hugging Face requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user PATH=/home/user/.local/bin:$PATH
WORKDIR $HOME/app


COPY --chown=user requirements.txt $HOME/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY --chown=user . $HOME/app

# Starting the OpenEnv server on the required port (7860)
CMD ["python", "-m", "openenv.core.server", "--host", "0.0.0.0", "--port", "7860"]
CMD ["python", "inference.py"]
