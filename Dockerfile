FROM python:3.12-slim

# System deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install uv (goes to /root/.local/bin)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
    /root/.local/bin/uv --version

WORKDIR /app

# Copy dependency definition
COPY pyproject.toml uv.lock* ./

# Install Python dependencies into system environment (deps only)
RUN /root/.local/bin/uv pip install --system \
    "python-telegram-bot==21.4" \
    "ollama==0.3.3" \
    "psycopg2-binary==2.9.9" \
    "apscheduler==3.10.4" \
    "python-dotenv==1.0.1" \
    "notion-client==2.3.0"

# Copy source code
COPY . .

# Run the bot
CMD ["/root/.local/bin/uv", "run", "python", "bot.py"]
