# DSA NagBot

DSA NagBot is a personal AI-powered Telegram tutor that plans and tracks a 3‑month learning journey for Data Structures & Algorithms and computer systems, then nudges you on Telegram until you act.

It runs as a Dockerized backend using Python, uv, PostgreSQL, and a local LLM (via Ollama), and exports your progress to Notion or Markdown for long‑term tracking.

---

## Features

- Daily DSA tasks: arrays, linked lists, stacks, queues, trees, graphs, recursion, and algorithms broken into 5–30 minute tasks. 
- Three daily reminders: morning, afternoon, and evening prompts to keep you accountable for each day’s tasks. 
- Adaptive difficulty: tasks can ramp up based on your completion and success rate over time. 
- AI coaching: a local LLM (via Ollama) generates problems, reviews your code, and gives feedback in chat.
- Progress tracking: stores your schedule, submissions, and streaks in PostgreSQL.
- Exports to Notion / Markdown: monthly summaries of what you actually completed, ready to review or archive.   
- Zero-cost stack: runs in GitHub Codespaces with Docker + Ollama + Telegram + Postgres, no paid APIs required.

---

## Tech Stack

- Language: Python 3.12  
- Bot framework: `python-telegram-bot`  
- Package manager: `uv` (Rust‑based, fast installs and a lockfile)  
- Database: PostgreSQL  
- AI: Ollama (e.g. `llama3.2:3b`) running locally in Docker  
- Scheduling: APScheduler (for daily tasks and reminders)  
- Config: `.env` + `python-dotenv`  
- Deployment: Docker + Docker Compose (optimized for GitHub Codespaces)

---

## Core Idea

The goal is simple: remove all friction from planning and tracking, so you can just open Telegram and do the next task.

The bot:

1. Plans a 90‑day curriculum for:
   - DSA topics (arrays → graphs, plus recursion and classic algorithms).  
   - ~75 LeetCode-style problems.  
   - “Computer Systems: A Programmer’s Perspective” reading bites.
2. Sends you three micro‑sessions per day (5–30 minutes each).
3. Reminds you up to three times per day if you have not completed the tasks.
4. Logs completion, AI feedback, and streaks to the database and monthly export.

---

## Architecture Overview

High‑level components:

- Telegram Bot Service (`bot`)
  - Handles commands such as `/start`, `/today`, `/done1`, `/progress`, etc.  
  - Interacts with PostgreSQL for user, schedule, and AI-task state.  
  - Calls the Ollama HTTP API to generate problems and review code.

- PostgreSQL
  - Stores:
    - `users` (chat_id, phase, day_number, streak, solve_rate).  
    - `daily_schedule` (3 tasks per day, completion flags, reminders).  
    - `ai_todo` (AI task descriptions, steps, and context for internal agents).

- Ollama
  - Runs a local LLM model (e.g. `llama3.2:3b`) inside Docker.  
  - Prompts are structured for:
    - DSA problem generation.  
    - Code review (correctness, efficiency, and suggestions).

- Export/Reporting
  - Monthly job or on‑demand command exports progress to:
    - A Markdown file (e.g. `monthly_dsa_log_YYYY_MM.md`).  
    - A Notion database via the Notion API.

---

## Getting Started

### 1. Prerequisites

- GitHub account  
- GitHub Codespaces or a machine with Docker + Docker Compose  
- A Telegram bot token from **@BotFather**  
- Basic knowledge of Python and Docker (for local tweaks)

### 2. Clone and open in Codespaces / VS Code

```bash
git clone https://github.com/<your-username>/dsa-nagbot.git
cd dsa-nagbot
```

Open the repository in GitHub Codespaces or VS Code with the provided devcontainer.

### 3. Environment variables

Create a `.env` file (example):

```
TELEGRAM_TOKEN=your_telegram_bot_token
OLLAMA_URL=http://ollama:11434
DB_URL=postgresql://postgres:password@postgres:5432/dsanagbot
```

These values should match what is used in `docker-compose.yml` and `bot.py`.

### 4. Build and run with Docker

From the project root:

```bash
uv lock                # generate uv.lock if it doesn't exist
docker compose up -d   # start postgres, ollama, and bot
docker compose ps      # check that all services are healthy
```

If you use Codespaces, services run inside the remote container and the bot communicates via Telegram (not HTTP).

### 5. Initialize the database (if needed)

```bash
python db.py
```

This creates core tables: `users`, `daily_schedule`, and `ai_todo`.

### 6. Pull the AI model

```bash
docker exec -it dsa-nagbot-ollama-1 ollama pull llama3.2:3b
```

This downloads the LLM that the bot uses for problem generation and code review.

### 7. Start chatting

1. Create a bot with **@BotFather** and insert the token into `.env`.  
2. Start your bot (search for `@your_dsa_nagbot` on Telegram) and send `/start`.  
3. Useful commands:
   - `/start` – initialize your 90‑day plan and Day 1 schedule.  
   - `/today` – see today’s three tasks.  
   - `/done1 <code>` – mark task 1 done and get AI feedback.  
   - `/progress` – show your day, streak, and success rate.

---

## Development Workflow

With `uv` as the package manager:

- Add a new dependency:

```bash
uv add <package-name>
```

- Run the bot locally (without Docker):

```bash
uv run python bot.py
```

- Regenerate the lockfile after dependency changes:

```bash
uv lock
```

Docker builds use `uv` for reproducible installs based on `pyproject.toml` and `uv.lock`.

---

## Roadmap / Ideas

- Full 90‑day curriculum generation by the AI (instead of fixed Day 1 tasks).  
- Richer `/progress` dashboard (per‑topic accuracy, time spent, streak history).  
- Webhook-mode deployment behind a reverse proxy (instead of polling) for production.  
- Multi‑user support with personalized plans per chat_id.

---

## Why This Project Matters

This project is an opinionated backend portfolio piece that:

- Uses Docker + Compose + Postgres + `uv` in a realistic way.  
- Integrates a local AI model instead of relying on paid APIs.  
- Solves a practical problem: keeping a self‑taught developer on track for a 3‑month DSA grind.
