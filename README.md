# DSA NagBot

DSA NagBot is a **personal AI-powered Telegram tutor** that plans and tracks a 3‑month learning journey for Data Structures & Algorithms and computer systems, then nags you on Telegram until you actually do the work. [page:1]

It runs as a Dockerized backend using **Python, uv, PostgreSQL, and a local LLM (via Ollama)**, and exports your progress to Notion or Markdown for long‑term tracking. [page:1]

---

## Features

- **Daily DSA tasks**: Arrays, linked lists, stacks, queues, trees, graphs, recursion, and algorithms broken into 5–30 minute tasks. [page:1]  
- **3× daily reminders**: Morning, afternoon, and evening prompts to keep you accountable for each day’s tasks. [page:1]  
- **Adaptive difficulty**: Tasks can ramp up based on your completion and success rate over time. [page:1]  
- **AI coaching**: Free local LLM (via Ollama) generates problems, reviews your code, and gives feedback in chat. [page:1]  
- **Progress tracking**: Stores your schedule, submissions, and streaks in PostgreSQL. [page:1]  
- **Exports to Notion / Markdown**: Monthly summaries of what you actually completed, ready to review or archive. [page:1]  
- **Zero-cost stack**: Runs in GitHub Codespaces with Docker + Ollama + Telegram + Postgres, no paid APIs required. [page:1]

---

## Tech Stack

- **Language**: Python 3.12  
- **Bot Framework**: `python-telegram-bot`  
- **Package Manager**: `uv` (Rust‑based, fast installs and lockfile)  
- **Database**: PostgreSQL  
- **AI**: Ollama (e.g. `llama3.2:3b`) running locally in Docker  
- **Scheduling**: APScheduler (for daily tasks and reminders)  
- **Config**: `.env` + `python-dotenv`  
- **Deployment**: Docker + Docker Compose (optimized for GitHub Codespaces) [page:1]

---

## Core Idea

The goal is simple: *remove all friction from planning and tracking*, so you can just open Telegram and do the next task. [page:1]

The bot:

1. Plans a 90‑day curriculum for:
   - DSA topics (arrays → graphs, plus recursion and classic algorithms).  
   - 75 Grind LeetCode problems.  
   - “Computer Systems: A Programmer’s Perspective” reading bites. [page:1]

2. Sends you **3 micro‑sessions per day** (5–30 minutes each). [page:1]

3. Reminds you up to 3 times per day if you have not completed the tasks. [page:1]

4. Logs completion, AI feedback, and streaks to the database and monthly export. [page:1]

---

## Architecture Overview

High‑level components:

- **Telegram Bot Service (`bot`)**
  - Handles `/start`, `/today`, `/done1`, `/progress`, etc.  
  - Talks to PostgreSQL for user, schedule, and AI‑task state.  
  - Calls Ollama HTTP API to generate problems and review code. [page:1]

- **PostgreSQL**
  - Stores:
    - `users` (chat_id, phase, day_number, streak, solve_rate).  
    - `daily_schedule` (3 tasks per day, completion flags, reminders).  
    - `ai_todo` (AI task descriptions, steps, and context for internal “agents”). [page:1]

- **Ollama**
  - Runs a local LLM model (like `llama3.2:3b`) inside Docker.  
  - Prompts are structured for:
    - DSA problem generation.  
    - Code review (correctness + efficiency + suggestion). [page:1]

- **Export/Reporting**
  - Monthly job or on‑demand command exports progress to:
    - A Markdown file (e.g. `monthly_dsa_log_YYYY_MM.md`).  
    - A Notion database via the official Notion API. [page:1]

---

## Getting Started

### 1. Prerequisites

- GitHub account  
- GitHub Codespaces or a machine with Docker + Docker Compose  
- A Telegram bot token from **@BotFather**  
- Basic knowledge of Python and Docker (for local tweaks) [page:1]

### 2. Clone and Open in Codespaces

```
bash 
git clone https://github.com/<your-username>/dsa-nagbot.git
cd dsa-nagbot
```
Open in Codespaces or VS Code with devcontainer
text

### 3. Environment Variables

Create a `.env` file:

TELEGRAM_TOKEN=your_telegram_bot_token
OLLAMA_URL=http://ollama:11434
DB_URL=postgresql://postgres:password@postgres:5432/dsanagbot

text

These values should match what is used in `docker-compose.yml` and `bot.py`. [page:1]

### 4. Build and Run with Docker

From the project root:

uv lock # ensure uv.lock exists
docker compose up -d # start postgres, ollama, and bot
docker compose ps # check that all services are healthy

text

If you use Codespaces, this runs inside the remote container and exposes the bot via Telegram, not HTTP. [page:1]

### 5. Initialize Database (if needed)

python db.py

text

This creates core tables: `users`, `daily_schedule`, and `ai_todo`. [page:1]

### 6. Pull the AI Model

docker exec -it dsa-nagbot-ollama-1 ollama pull llama3.2:3b

text

This downloads the LLM that the bot uses for problem generation and code review. [page:1]

### 7. Start Chatting

In Telegram:

1. Open **@BotFather**, create a bot, and insert the token into `.env`.  
2. Start your bot: search for `@your_dsa_nagbot` and send `/start`.  
3. Use commands:
   - `/start` – initialize your 90‑day plan and Day 1 schedule.  
   - `/today` – see today’s 3 tasks.  
   - `/done1 <code>` – mark task 1 done and get AI feedback.  
   - `/progress` – show your day, streak, and success rate. [page:1]

---

## Development Workflow

With **uv** as the package manager:

- Add a new dependency:

uv add <package-name>

text

- Run the bot locally (without Docker):

uv run python bot.py

text

- Regenerate lockfile after dependency changes:

uv lock

text

Docker builds use `uv` for fast, reproducible installs based on `pyproject.toml` and `uv.lock`. [page:1]

---

## Roadmap / Ideas

- Full 90‑day curriculum generation by the AI (instead of fixed Day 1 tasks). [page:1]  
- Richer `/progress` dashboard (per‑topic accuracy, time spent, streak history). [page:1]  
- Webhook mode deployment behind a reverse proxy (instead of polling) for production. [page:1]  
- Multi‑user support with personalized plans per chat_id. [page:1]  

---

## Why This Project Matters

This project is designed as a **real, opinionated backend portfolio piece**:

- Uses **Docker + Compose + Postgres + uv** in a realistic way.  
- Integrates a **local AI model** instead of relying on paid APIs.  
- Solves a real personal problem: keeping a self‑taught developer on track for a 3‑month DSA grind. 