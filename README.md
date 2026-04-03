# se-toolkit-hackathon
An AI-powered academic planner that uses LLM agents to automatically prioritize and organize student tasks
# AI Smart Planner (InnoFocus)

An intelligent task management web application that uses an LLM agent to transform unstructured natural language into a structured, prioritized academic schedule.

## Product Context
* **End users:** University students managing multiple academic assignments and tight deadlines.
* **Problem:** Cognitive overload and difficulty prioritizing tasks from unstructured course materials.
* **Solution:** An LLM-powered agent that parses raw text input, categorizes tasks, and provides a prioritized step-by-step checklist.

## Implementation Plan

### Version 1 (Core Feature)
* **Goal:** A functioning web application that extracts actionable tasks from natural language input.
* **Core Feature:** Natural Language Task Decomposition.
* **Stack:** Python (FastAPI), Streamlit (Frontend).

### Version 2 (Full Product)
* **Goal:** A persistent, production-ready application.
* **Features:**
    * PostgreSQL integration for task persistence and user profiles.
    * "Complete" and "Delete" functionality.
    * Full Dockerization using `docker-compose`.
    * Deployment on university VM.

## Features
- [x] Natural Language Parsing (V1)
- [ ] PostgreSQL Persistence (V2)
- [ ] AI-Powered Task Prioritization (V2)
- [ ] Dockerized Deployment (V2)

## Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **AI:** LangChain / OpenAI API
