# 🎯 InnoFocus

**AI-powered smart planner for university students** — transforms an unstructured to-do list into a prioritized action plan.

## 📋 Project Context

### End Users
University students juggling multiple academic assignments, deadlines, and personal tasks.

### Problem
Cognitive overload and difficulty prioritizing tasks from unstructured course materials. Students get lost between labs, deadlines, projects, and personal life.

### Solution
An LLM-powered web application that parses raw text input (brain dump), categorizes tasks, and provides a prioritized step-by-step checklist with progress tracking.

## ✨ Features

### Implemented (Version 2)
- ✅ **AI Plan Generation** — Enter tasks in natural language, AI structures them and assigns priorities (High/Medium/Low)
- ✅ **Full CRUD** — Create, read, update, and delete tasks
- ✅ **PostgreSQL Persistence** — All tasks are stored in a database
- ✅ **Task Management** — Mark tasks as complete, filter by priority and status
- ✅ **Statistics Dashboard** — Visual task stats (total, completed, by priority)
- ✅ **Dockerized Deployment** — All services containerized, one-command startup
- ✅ **Responsive Web UI** — Modern Streamlit interface with tabs and filters

### Planned (Future Versions)
- 🔲 User authentication & profiles
- 🔲 Deadline tracking & reminders
- 🔲 Calendar export (Google Calendar, iCal)
- 🔲 Mobile app (React Native)
- 🔲 Collaborative task sharing

## 🛠 Tech Stack

- **Frontend:** Streamlit (Python)
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL 15
- **AI/LLM:** Ollama (qwen2.5:7b) / OpenAI-compatible API
- **Deployment:** Docker & Docker Compose
- **Infrastructure:** Health checks, volumes, networking

## 📸 Screenshots

### AI Plan Generator
Enter a "brain dump" — AI returns a structured task list with priorities.

![AI Generator](https://via.placeholder.com/800x400?text=AI+Plan+Generator+Screenshot)

### Task List with Filters
Filter by priority (High/Medium/Low) and status (Active/Completed).

![Task List](https://via.placeholder.com/800x400?text=Task+List+with+Filters)

### Statistics Dashboard
Visual stats: total tasks, completed, in progress, priority breakdown.

![Statistics](https://via.placeholder.com/800x400?text=Statistics+Dashboard)

## 🚀 Usage

### Quick Start (with Ollama on host)

1. **Install Ollama** on the host machine:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull qwen2.5:7b
   ```

2. **Start the project:**
   ```bash
   docker-compose up -d
   ```

3. **Open your browser:**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000/docs (Swagger UI)
   - Backend Health Check: http://localhost:8000/health

### Without Ollama (using OpenAI API)

If you prefer OpenAI over Ollama:

1. Create a `.env` file in the project root:
   ```env
   LLM_BASE_URL=https://api.openai.com/v1
   LLM_MODEL=gpt-4o
   OPENAI_API_KEY=your-api-key-here
   ```

2. Update `backend/requirements.txt` to include `openai` (already included).

3. Start:
   ```bash
   docker-compose up -d
   ```

## 🐳 Deployment

### Requirements
- **OS:** Ubuntu 24.04 (or any OS with Docker support)
- **Docker:** 20.10+
- **Docker Compose:** 2.0+
- **RAM:** at least 4GB (for Ollama + PostgreSQL + app)
- **Ollama** (optional, if not using external OpenAI API)

### Step-by-Step Deployment

#### 1. Clone the repository
```bash
git clone https://github.com/your-username/se-toolkit-hackathon.git
cd se-toolkit-hackathon
```

#### 2. Install Ollama (if needed)
```bash
# Ubuntu/Debian
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:7b

# Verify
ollama list
```

#### 3. Configure environment (optional)
Create a `.env` file for custom settings:
```env
LLM_BASE_URL=http://host.docker.internal:11434/v1
LLM_MODEL=qwen2.5:7b
```

#### 4. Build and start services
```bash
docker-compose up -d --build
```

#### 5. Verify deployment
```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Health check
curl http://localhost:8000/health
```

#### 6. Access the application
- **Frontend (Streamlit):** http://your-vm-ip:8501
- **Backend API Docs:** http://your-vm-ip:8000/docs
- **Backend Health:** http://your-vm-ip:8000/health

### Production Deployment (VM with public IP)

For external access (university VM):

```bash
# Open ports in firewall
sudo ufw allow 8501/tcp
sudo ufw allow 8000/tcp

# Verify services are listening on all interfaces
docker-compose ps
```

Optional: set up a reverse proxy (nginx):

```bash
# Install nginx
sudo apt install nginx

# Configure nginx (example for frontend)
sudo nano /etc/nginx/sites-available/innofocus

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

sudo ln -s /etc/nginx/sites-available/innofocus /etc/nginx/sites-enabled/
sudo systemctl reload nginx
```

## 🔌 Backend API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/generate-plan` | Generate a plan from text (LLM) |
| `GET` | `/tasks` | Get all tasks |
| `GET` | `/tasks/{id}` | Get a task by ID |
| `POST` | `/tasks` | Create a task manually |
| `PUT` | `/tasks/{id}` | Update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |
| `GET` | `/tasks/stats` | Get task statistics |
| `GET` | `/health` | Health check |

Interactive API docs available at: `http://localhost:8000/docs`

## 📁 Project Structure

```
se-toolkit-hackathon/
├── backend/
│   ├── main.py              # FastAPI application, routes
│   ├── database.py          # SQLAlchemy setup, DB connection
│   ├── models.py            # Database models (Task)
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Backend container
├── frontend/
│   ├── app.py               # Streamlit application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile           # Frontend container
├── docker-compose.yml       # Multi-service orchestration
├── README.md                # This file
├── LICENSE                  # MIT License
└── .gitignore               # Git ignore rules
```

## 🧪 Testing

### Manual Testing
1. Open http://localhost:8501
2. Navigate to the "AI Generator" tab
3. Enter text: "Finish OS lab, learn 20 kanji, call mom"
4. Click "Generate Plan"
5. Verify tasks appear in "My Tasks" tab
6. Mark a task as complete
7. Test filters and statistics

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Create task manually
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test task", "priority": "High"}'

# Get all tasks
curl http://localhost:8000/tasks

# Get stats
curl http://localhost:8000/tasks/stats
```

## 📝 Development Workflow

### Local Development (without Docker)

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (in another terminal)
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Rebuilding Docker Containers
```bash
docker-compose down
docker-compose up -d --build
```

### Clear All Data (reset database)
```bash
docker-compose down -v
docker-compose up -d
```

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Your Name**  
University Student  
Email: your.email@university.edu  
Group: XX-XXX

---

**InnoFocus v2.0** — Made with ❤️ for students who want to stay focused.
