# AI Smart Planner

An intelligent task management web application that uses Qwen LLM to transform unstructured natural language into a structured, prioritized academic schedule.

## Product Context
* **End-user:** University students managing multiple academic assignments and tight deadlines.
* **Problem:** Cognitive overload and difficulty prioritizing tasks from unstructured course materials.
* **Solution:** An LLM-powered agent that parses raw text input, categorizes tasks, and provides a prioritized step-by-step checklist.

## Architecture

```
Browser → Streamlit Frontend → FastAPI Backend → Qwen API → Structured Tasks
                          ↓
                    PostgreSQL (V2)
```

## Quick Start

### Version 1 (MVP) — Parse tasks with AI

**Prerequisites:**
- Docker & Docker Compose
- Qwen API key (from https://portal.qwen.ai)

**Setup:**

1. Clone the repository:
```bash
git clone <your-repo-url>
cd se-toolkit-hackathon
```

2. Create environment file:
```bash
cp .env.docker.example .env.docker.secret
# Edit .env.docker.secret and add your QWEN_API_KEY
```

3. Update your Qwen API key in `.env.docker.secret`:
```bash
QWEN_API_KEY=your-actual-qwen-api-key
```

4. Start all services:
```bash
docker compose --env-file .env.docker.secret up -d
```

5. Access the application:
- **Frontend:** http://localhost:8501
- **Backend API:** http://localhost:8000
- **API docs (Swagger):** http://localhost:8000/docs

### Version 2 — With database persistence

Same as V1, but tasks are now saved to PostgreSQL and persist across sessions.

## Tech Stack

- **Backend:** FastAPI (Python 3.11)
- **Frontend:** Streamlit
- **Database:** PostgreSQL 16
- **AI:** Qwen API (qwen-coder-plus model)
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
│   │   ├── agent.py          # Qwen LLM agent
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
QWEN_API_KEY=your-key python -m ai_planner.run
```

**Frontend:**
```bash
pip install streamlit requests
API_BASE_URL=http://localhost:8000 streamlit run frontend/app.py
```

## Qwen API Configuration

The application uses Qwen's API compatible with OpenAI SDK:

- **API Base URL:** `https://portal.qwen.ai/v1`
- **Default Model:** `qwen-coder-plus`
- **Authentication:** API key via `QWEN_API_KEY` environment variable

To get your Qwen API key:
1. Visit https://portal.qwen.ai
2. Navigate to API settings
3. Generate your API key
4. Add it to `.env.docker.secret`

## Troubleshooting

### Backend won't start
- Check logs: `docker compose logs backend`
- Verify QWEN_API_KEY is set in `.env.docker.secret`

### Frontend can't connect to API
- Ensure backend is running: `curl http://localhost:8000/health`
- Check CORS settings

### PostgreSQL connection issues
- Wait for health check: `docker compose ps`
- Check logs: `docker compose logs postgres`

### API returns 401 error
- Verify your QWEN_API_KEY is valid
- Check that the key has not expired
- Ensure QWEN_API_BASE is set to `https://portal.qwen.ai/v1`
