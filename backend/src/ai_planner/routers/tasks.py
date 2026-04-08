"""Tasks router — parse and manage tasks with database persistence."""

import json
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from ai_planner.models import ParseRequest, TaskListResponse, TaskItem, SubTask
from ai_planner.agent import parse_tasks as ai_parse_tasks
from ai_planner.database import TaskModel, get_session

router = APIRouter()


@router.post("/parse", response_model=TaskListResponse)
async def parse_tasks_endpoint(request: ParseRequest, session: Session = Depends(get_session)):
    """
    Parse unstructured text into structured, prioritized tasks.
    New tasks are ADDED to existing tasks, not replacing them.
    """
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        # Parse with AI
        parsed_tasks = await ai_parse_tasks(request.text)
        
        # Save each new task to database
        saved_tasks = []
        for task in parsed_tasks:
            db_task = TaskModel(
                title=task.title,
                priority=task.priority.value,
                deadline=task.deadline,
                user_id=request.user_id,
                subtasks_json=json.dumps([{"title": st.title, "completed": st.completed} for st in task.subtasks])
            )
            session.add(db_task)
            saved_tasks.append(task)
        
        session.commit()
        
        return TaskListResponse(
            tasks=saved_tasks,
            total_count=len(saved_tasks)
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all", response_model=TaskListResponse)
async def get_all_tasks(user_id: str = "anonymous", session: Session = Depends(get_session)):
    """Get all tasks for user (including completed ones)."""
    statement = select(TaskModel).where(TaskModel.user_id == user_id)
    db_tasks = session.exec(statement).all()
    
    tasks = []
    for db_task in db_tasks:
        subtasks_data = json.loads(db_task.subtasks_json) if db_task.subtasks_json else []
        subtasks = [SubTask(title=st["title"], completed=st.get("completed", False)) for st in subtasks_data]
        
        tasks.append(TaskItem(
            id=db_task.id,
            title=db_task.title,
            priority=db_task.priority,
            subtasks=subtasks,
            deadline=db_task.deadline,
            completed=db_task.completed,
            created_at=db_task.created_at
        ))
    
    return TaskListResponse(tasks=tasks, total_count=len(tasks))


@router.get("/active", response_model=TaskListResponse)
async def get_active_tasks(user_id: str = "anonymous", session: Session = Depends(get_session)):
    """Get only active (not completed) tasks."""
    statement = select(TaskModel).where(
        TaskModel.user_id == user_id,
        TaskModel.completed == False
    )
    db_tasks = session.exec(statement).all()
    
    tasks = []
    for db_task in db_tasks:
        subtasks_data = json.loads(db_task.subtasks_json) if db_task.subtasks_json else []
        subtasks = [SubTask(title=st["title"], completed=st.get("completed", False)) for st in subtasks_data]
        
        tasks.append(TaskItem(
            id=db_task.id,
            title=db_task.title,
            priority=db_task.priority,
            subtasks=subtasks,
            deadline=db_task.deadline,
            completed=db_task.completed,
            created_at=db_task.created_at
        ))
    
    return TaskListResponse(tasks=tasks, total_count=len(tasks))


@router.put("/{task_id}/complete")
async def mark_task_complete(task_id: int, session: Session = Depends(get_session)):
    """Mark a task as completed."""
    db_task = session.get(TaskModel, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db_task.completed = True
    session.commit()
    return {"status": "success", "message": f"Task {task_id} marked as complete"}


@router.delete("/{task_id}")
async def delete_task(task_id: int, session: Session = Depends(get_session)):
    """Delete a task."""
    db_task = session.get(TaskModel, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    session.delete(db_task)
    session.commit()
    return {"status": "success", "message": f"Task {task_id} deleted"}


@router.post("/{task_id}/subtasks/{subtask_index}/toggle")
async def toggle_subtask(task_id: int, subtask_index: int, session: Session = Depends(get_session)):
    """Toggle subtask completion status."""
    db_task = session.get(TaskModel, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    subtasks = json.loads(db_task.subtasks_json) if db_task.subtasks_json else []
    if subtask_index >= len(subtasks):
        raise HTTPException(status_code=404, detail="Subtask not found")
    
    subtasks[subtask_index]["completed"] = not subtasks[subtask_index].get("completed", False)
    db_task.subtasks_json = json.dumps(subtasks)
    session.commit()
    
    return {"status": "success", "completed": subtasks[subtask_index]["completed"]}
