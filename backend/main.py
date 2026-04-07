from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import openai
import os
import json
import models
import database

app = FastAPI(title="InnoFocus API", version="2.0.0")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup
models.Base.metadata.create_all(bind=database.engine)

# LLM configuration (Ollama with qwen2.5)
client = openai.OpenAI(
    base_url=os.getenv("LLM_BASE_URL", "http://host.docker.internal:11434/v1"),
    api_key="token"
)

# === Pydantic schemas ===
class TaskInput(BaseModel):
    content: str

class TaskCreate(BaseModel):
    title: str
    priority: str = "Medium"

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    priority: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    priority: str
    is_completed: bool

    class Config:
        from_attributes = True

class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]
    total: int

# === LLM endpoints ===
@app.post("/generate-plan", response_model=TaskListResponse)
def generate_plan(data: TaskInput, db: Session = Depends(database.get_db)):
    """Generate a structured task plan from unstructured text"""
    prompt = f"""Break down the following text into specific actionable tasks. Return ONLY JSON in this format:
{{"tasks": [{{"title": "task", "priority": "High|Medium|Low"}}]}}

Text: {data.content}

Rules:
- Each task must be a concrete action
- Priority: High (urgent/important), Medium (normal), Low (can wait)
- Maximum 10 tasks
- JSON only, no explanations"""

    try:
        response = client.chat.completions.create(
            model=os.getenv("LLM_MODEL", "qwen2.5:7b"),
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.3
        )

        result = response.choices[0].message.content
        parsed = json.loads(result)

        # Save tasks to database
        created_tasks = []
        for task_data in parsed.get("tasks", []):
            task = models.Task(
                title=task_data["title"],
                priority=task_data.get("priority", "Medium"),
                is_completed=False
            )
            db.add(task)
            created_tasks.append(task)

        db.commit()

        return TaskListResponse(
            tasks=[TaskResponse.model_validate(t) for t in created_tasks],
            total=len(created_tasks)
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan generation error: {str(e)}")

# === CRUD endpoints ===
@app.get("/tasks", response_model=TaskListResponse)
def get_tasks(skip: int = 0, limit: int = 50, db: Session = Depends(database.get_db)):
    """Get all tasks with pagination"""
    tasks = db.query(models.Task).offset(skip).limit(limit).all()
    return TaskListResponse(tasks=tasks, total=len(tasks))

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(database.get_db)):
    """Get a specific task by ID"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(database.get_db)):
    """Create a new task manually"""
    db_task = models.Task(
        title=task.title,
        priority=task.priority,
        is_completed=False
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(database.get_db)):
    """Update a task"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_update.title is not None:
        task.title = task_update.title
    if task_update.priority is not None:
        task.priority = task_update.priority
    if task_update.is_completed is not None:
        task.is_completed = task_update.is_completed

    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    """Delete a task"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

@app.get("/tasks/stats")
def get_task_stats(db: Session = Depends(database.get_db)):
    """Get task statistics"""
    total = db.query(models.Task).count()
    completed = db.query(models.Task).filter(models.Task.is_completed == True).count()
    high = db.query(models.Task).filter(models.Task.priority == "High").count()
    medium = db.query(models.Task).filter(models.Task.priority == "Medium").count()
    low = db.query(models.Task).filter(models.Task.priority == "Low").count()

    return {
        "total": total,
        "completed": completed,
        "pending": total - completed,
        "by_priority": {
            "High": high,
            "Medium": medium,
            "Low": low
        }
    }

@app.get("/health")
def health_check():
    """Service health check"""
    return {"status": "ok"}
