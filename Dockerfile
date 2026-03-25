FROM --platform=linux/amd64 python:3.10-slim

ENV HF_HOME=/app/models
# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive
ENV TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=true

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
ffmpeg \
git \
&& rm -rf /var/lib/apt/lists/*

# Upgrade pip 
RUN pip install --upgrade pip

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY config/ config/
COPY sample.wav .
# COPY requirements.txt .

# Install all the dependencies
# RUN pip install whisperx==3.8.2
RUN pip install --no-cache-dir whisperx
RUN pip install --no-cache-dir dotenv
RUN pip install --no-cache-dir pydub

# Install the package
RUN pip install -e .

# Default command and entrypoint
ENTRYPOINT [ "transcriber" ]
CMD [ "--audio", "sample.wav" ]