# AI Smart Planner

An intelligent task management web application that uses Qwen AI to transform unstructured natural language into a structured, prioritized academic schedule.

## Project Context
* **End-user:** University students managing multiple academic assignments and tight deadlines.
* **Problem:** Cognitive overload and difficulty prioritizing tasks from unstructured course materials.
* **Solution:** An LLM-powered agent that parses raw text input, categorizes tasks, and provides a prioritized step-by-step checklist.

## Implementation Plan

### Version 1 (Core Feature) - MVP
* **Goal:** A functioning web application that extracts actionable tasks from natural language input.
* **Key Functionality:** The user inputs a "brain dump" (text), and the LLM agent returns a structured task list with priority levels and sub-tasks.
* **Tech Stack:** Python (FastAPI), Streamlit (Frontend).
* **Scope:** Real-time parsing without database persistence.

### Version 2 (Full Product)
* **Goal:** A production-ready, persistent application.
* **Key Functionality:**
    * **Data Persistence:** PostgreSQL integration to save user profiles and task history.
    * **Task Management:** Functionality to mark tasks as "Complete" or "Delete" with state updates in the database.
    * **Deployment:** Full containerization of all services using `docker-compose`.
    * **Deployment Target:** University VM accessible via web browser.

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
