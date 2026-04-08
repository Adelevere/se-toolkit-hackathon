# AI Smart Planner

An intelligent task management web application that uses Qwen AI to transform unstructured natural language into a structured, prioritized academic schedule.

## Product

- **End-user:** University students managing multiple academic assignments and deadlines
- **Problem:** Cognitive overload from unstructured course materials
- **Solution:** AI-powered parser that extracts tasks, assigns priorities, and breaks them into subtasks

## Architecture

```
Browser → Streamlit Frontend → FastAPI Backend → Qwen CLI → Structured Tasks
                          ↓
                    PostgreSQL
```

## Tech Stack

- **Backend:** FastAPI (Python 3.11)
- **Frontend:** Streamlit
- **Database:** PostgreSQL 16
- **AI:** Qwen CLI (OAuth)
- **Deployment:** Docker Compose

## Quick Start

**Prerequisites:** Docker & Docker Compose, Qwen CLI authenticated (`qwen auth`)

```bash
git clone <your-repo-url>
cd se-toolkit-hackathon
docker compose up -d
```

- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:8000

## Features

- ✅ AI task parsing from natural language
- ✅ Priority assignment (high/medium/low)
- ✅ Automatic subtask generation
- ✅ Deadline detection
- ✅ PostgreSQL persistence
- ✅ Mark tasks as complete / delete

## Project Structure

```
se-toolkit-hackathon/
├── backend/
│   ├── src/ai_planner/
│   │   ├── main.py          # FastAPI app
│   │   ├── agent.py          # Qwen CLI task parser
│   │   ├── database.py       # SQLModel database layer
│   │   └── routers/          # API routes
│   └── pyproject.toml
├── frontend/
│   └── app.py                # Streamlit web app
├── docker-compose.yml
└── README.md
```
