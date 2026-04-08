# AI Smart Planner

An intelligent task management web application that uses an LLM agent to transform unstructured natural language into a structured, prioritized academic schedule.

## Product Context
* **End-user:** University students managing multiple academic assignments and tight deadlines.
* **Problem:** Cognitive overload and difficulty prioritizing tasks from unstructured course materials.
* **Solution:** An LLM-powered agent that parses raw text input, categorizes tasks, and provides a prioritized step-by-step checklist.

## Architecture

```
Browser → Streamlit Frontend → FastAPI Backend → OpenAI GPT-4o → Structured Tasks
                          ↓
                    PostgreSQL (V2)
```

## Quick Start

### Version 1 (MVP) — Parse tasks with AI

**Prerequisites:**
- Docker & Docker Compose
- OpenAI API key

**Setup:**

1. Clone the repository:
```bash
git clone <your-repo-url>
cd se-toolkit-hackathon
```

2. Create environment file:
```bash
cp .env.docker.example .env.docker.secret
# Edit .env.docker.secret and add your OPENAI_API_KEY
```

3. Start all services:
```bash
docker compose --env-file .env.docker.secret up -d
```

4. Access the application:
- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs

### Version 2 — With database persistence

Same as V1, but tasks are now saved to PostgreSQL and persist across sessions.

## Tech Stack

- **Backend:** FastAPI (Python 3.11)
- **Frontend:** Streamlit
- **Database:** PostgreSQL 16
- **AI:** OpenAI GPT-4o API
- **Deployment:** Docker Compose

## Features

### Version 1
- ✅ Natural language task extraction
- ✅ AI-powered priority assignment (high/medium/low)
- ✅ Automatic subtask generation
- ✅ Deadline detection from text
- ✅ Real-time web interface

### Version 2
- ✅ PostgreSQL persistence
- ✅ Task history and user sessions
- ✅ Mark tasks as complete/delete
- ✅ Full Docker Compose deployment

## API Endpoints

### POST /tasks/parse
Parse unstructured text into structured tasks.

**Request:**
```json
{
  "text": "I need to finish lab report by Friday and study for midterm",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "tasks": [
    {
      "title": "Complete lab report",
      "priority": "high",
      "subtasks": [
        {"title": "Write introduction", "completed": false},
        {"title": "Add results section", "completed": false}
      ],
      "deadline": "2026-04-10"
    }
  ],
  "total_count": 1
}
```

### GET /tasks/mock
Get sample tasks for testing.

### GET /health
Health check endpoint.

## Project Structure

```
se-toolkit-hackathon/
├── backend/
│   ├── src/ai_planner/
│   │   ├── main.py          # FastAPI app
│   │   ├── settings.py       # Configuration
│   │   ├── models.py         # Pydantic schemas
│   │   ├── agent.py          # LLM agent
│   │   └── routers/          # API routes
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── app.py                # Streamlit app
│   └── Dockerfile
├── docker-compose.yml
├── .env.docker.example
└── README.md
```

## Development

### Run locally (without Docker)

**Backend:**
```bash
cd backend
pip install -e ".[dev]"
OPENAI_API_KEY=your-key python -m ai_planner.run
```

**Frontend:**
```bash
pip install streamlit requests
API_BASE_URL=http://localhost:8000 streamlit run frontend/app.py
```

## Troubleshooting

### Backend won't start
- Check logs: `docker compose logs backend`
- Verify OPENAI_API_KEY is set in `.env.docker.secret`

### Frontend can't connect to API
- Ensure backend is running: `curl http://localhost:8000/health`
- Check CORS settings

### PostgreSQL connection issues
- Wait for health check: `docker compose ps`
- Check logs: `docker compose logs postgres`
