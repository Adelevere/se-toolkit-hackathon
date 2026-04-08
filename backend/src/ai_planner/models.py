"""AI Smart Planner — models and schemas."""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum
from datetime import datetime


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SubTaskCreate(BaseModel):
    title: str


class SubTask(BaseModel):
    title: str
    completed: bool = False


class TaskCreate(BaseModel):
    title: str
    priority: Priority
    subtasks: List[SubTask] = Field(default_factory=list)
    deadline: Optional[str] = None


class TaskItem(BaseModel):
    id: Optional[int] = None
    title: str
    priority: Priority
    subtasks: List[SubTask] = Field(default_factory=list)
    deadline: Optional[str] = None
    completed: bool = False
    created_at: Optional[str] = None


class TaskListResponse(BaseModel):
    tasks: List[TaskItem]
    total_count: int


class ParseRequest(BaseModel):
    text: str
    user_id: Optional[str] = "anonymous"
