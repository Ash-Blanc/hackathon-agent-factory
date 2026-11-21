"""
Dockerfile for Cloud Autonomous Hackathon Factory
Runs headless in Modal, Fly.io, Railway, or AWS ECS.
Includes Python 3.11, Bun, OpenCode, Hermes, and Agno agent loop.
"""

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install core build dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    unzip \
    build-essential \
    python3 \
    python3-pip \
    python3-venv \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# Install Bun
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:${PATH}"

# Install OpenCode CLI
RUN curl -fsSL https://opencode.ai/install.sh | bash || true
ENV PATH="/root/.opencode/bin:${PATH}"

# Set working directory
WORKDIR /app

# Copy agent factory files
COPY . /app

# Setup Python environment with Agno & dependencies
RUN uv venv && uv pip install -e .

EXPOSE 8080

CMD ["uv", "run", "python", "main.py"]
