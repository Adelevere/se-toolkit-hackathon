"""Tasks router — parse and manage tasks."""

from fastapi import APIRouter, HTTPException
from ai_planner.models import ParseRequest, TaskListResponse, TaskItem
from ai_planner.agent import parse_tasks

router = APIRouter()


@router.post("/parse", response_model=TaskListResponse)
async def parse_tasks_endpoint(request: ParseRequest):
    """
    Parse unstructured text into structured, prioritized tasks.

    - **text**: Raw brain dump text from user
    - **user_id**: Optional user identifier (defaults to "anonymous")
    """
    if not request.text or not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        tasks = await parse_tasks(request.text)
        return TaskListResponse(
            tasks=tasks,
            total_count=len(tasks)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mock", response_model=TaskListResponse)
async def get_mock_tasks():
    """Get sample tasks for testing."""
    mock_tasks = [
        TaskItem(
            title="Complete Lab 5 report",
            priority="high",
            subtasks=[
                SubTask(title="Write introduction", completed=True),
                SubTask(title="Add methodology section", completed=False),
                SubTask(title="Include results and analysis", completed=False)
            ],
            deadline="2026-04-10"
        ),
        TaskItem(
            title="Study for midterm exam",
            priority="high",
            subtasks=[
                SubTask(title="Review lecture notes", completed=False),
                SubTask(title="Practice problems", completed=False)
            ],
            deadline="2026-04-12"
        ),
        TaskItem(
            title="Read research paper for seminar",
            priority="medium",
            subtasks=[
                SubTask(title="Read abstract and introduction", completed=False),
                SubTask(title="Analyze methodology", completed=False),
                SubTask(title="Prepare discussion points", completed=False)
            ],
            deadline="2026-04-15"
        ),
        TaskItem(
            title="Update personal portfolio website",
            priority="low",
            subtasks=[
                SubTask(title="Add new project examples", completed=False)
            ],
            deadline=None
        )
    ]

    return TaskListResponse(tasks=mock_tasks, total_count=len(mock_tasks))
