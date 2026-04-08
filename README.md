# AI Smart Planner (InnoFocus)

An intelligent task management web application that uses an LLM agent to transform unstructured natural language into a structured, prioritized academic schedule.

## 1. Project Context
* **End-user:** University students managing multiple academic assignments and tight deadlines.
* **Problem:** Cognitive overload and difficulty prioritizing tasks from unstructured course materials.
* **Solution:** An LLM-powered agent that parses raw text input, categorizes tasks, and provides a prioritized step-by-step checklist.

## 2. Implementation Plan

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

## 3. Features
- [x] Natural Language Parsing (V1)
- [ ] PostgreSQL Persistence (V2)
- [ ] AI-Powered Task Prioritization (V2)
- [ ] Dockerized Deployment (V2)

## 4. Tech Stack
- **Frontend:** Streamlit
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **AI:** OpenAI API (GPT-4o)
