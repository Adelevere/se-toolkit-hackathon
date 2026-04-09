# AI Smart Planner

An intelligent task management web application that uses Qwen AI to transform unstructured natural language into a structured, prioritized academic schedule.
## Demo
> "C:\Users\adeli\OneDrive\Pictures\Screenshots\Снимок экрана 2026-04-09 220128.png"
## Project Context
* **End-user:** University students managing multiple academic assignments and tight deadlines.
* **Problem:** Cognitive overload and difficulty prioritizing tasks from unstructured course materials.
* **Solution:** An LLM-powered agent that parses raw text input, categorizes tasks, and provides a prioritized step-by-step checklist.

## Features

### ✅ Implemented
- AI-powered task parsing from natural language input
- Priority assignment (high / medium / low)
- Automatic subtask generation
- Deadline detection from free-form text
- PostgreSQL persistence of tasks and user sessions
- Mark tasks as **Complete** or **Delete** with real-time database updates
- Full containerization with Docker Compose

### 🔜 Not Yet Implemented
- User authentication and personal profiles
- Calendar / schedule view with drag-and-drop
- Email or push notifications for upcoming deadlines
- Export to PDF or `.ics` calendar format


## Usage

1. Open the app in your browser at `http://<your-vm-ip>:8501`
2. In the text area, paste or type your brain dump — any mix of assignments, reminders, or notes, e.g.: I have a data structures exam next Friday, need to review trees and graphs.
Also finish the lab report for physics by Tuesday. Don't forget to email
Prof. Smith about the project extension.
3. Click **"Parse Tasks"**.
4. The AI returns a structured checklist with:
   - Task title and description
   - Priority level (🔴 High / 🟡 Medium / 🟢 Low)
   - Subtasks broken into actionable steps
   - Detected deadlines
5. Use the **✓ Complete** and **🗑 Delete** buttons to manage your task list.
6. Your tasks are saved automatically and will persist across sessions.

### System Requirements
- **OS:** Ubuntu 24.04 LTS
- **RAM:** 2 GB minimum (4 GB recommended)
- **Disk:** 10 GB free space

### Prerequisites

Install the following on the VM:

```bash
# 1. Update packages
sudo apt update && sudo apt upgrade -y

# 2. Install Docker
sudo apt install -y ca-certificates curl gnupg
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 3. Allow running Docker without sudo (optional but recommended)
sudo usermod -aG docker $USER
newgrp docker

# 4. Install Qwen CLI and authenticate
pip install qwen-cli        # or follow official Qwen CLI install instructions
qwen auth
```

### Step-by-Step Deployment

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/se-toolkit-hackathon.git
cd se-toolkit-hackathon

# 2. (Optional) Configure environment variables
cp .env.example .env
# Edit .env if you need to change ports or database credentials
nano .env

# 3. Build and start all services
docker compose up -d

# 4. Verify all containers are running
docker compose ps
```

The application will be available at:

| Service | URL |
|---------|-----|
| **Frontend** (Streamlit) | `http://<your-vm-ip>:8501` |
| **Backend API** (FastAPI) | `http://<your-vm-ip>:8000` |
| **API Docs** (Swagger) | `http://<your-vm-ip>:8000/docs` |


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
