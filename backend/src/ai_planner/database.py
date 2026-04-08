"""Database connection and models using SQLModel."""

from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional
from datetime import datetime
from ai_planner.settings import settings

DATABASE_URL = f"postgresql+psycopg2://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"

engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    """Create all tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session


class TaskModel(SQLModel, table=True):
    """Task database model."""
    __tablename__ = "tasks"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    priority: str = "medium"
    deadline: Optional[str] = None
    completed: bool = False
    user_id: str = "anonymous"
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    subtasks_json: str = "[]"  # Store subtasks as JSON string
