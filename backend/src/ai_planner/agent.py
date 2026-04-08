"""LLM Agent for task extraction and prioritization."""

from openai import AsyncOpenAI
from typing import List
import json
from ai_planner.settings import settings
from ai_planner.models import TaskItem, SubTask, Priority

SYSTEM_PROMPT = """You are an AI task planner assistant. Your job is to analyze unstructured natural language text and extract actionable tasks with priorities and subtasks.

When given a "brain dump" text, you should:
1. Identify distinct tasks mentioned or implied
2. Assign priority (high/medium/low) based on urgency cues and deadlines
3. Break complex tasks into smaller subtasks
4. Extract any mentioned deadlines or dates

Return ONLY valid JSON in this exact format:
{
  "tasks": [
    {
      "title": "Task title",
      "priority": "high|medium|low",
      "subtasks": [{"title": "Subtask 1", "completed": false}],
      "deadline": "YYYY-MM-DD or null"
    }
  ]
}

Rules:
- Keep task titles concise and action-oriented
- Use "high" for urgent/deadline-driven tasks, "medium" for important but not urgent, "low" for nice-to-have
- Create 2-4 subtasks for complex tasks, 0-1 for simple tasks
- If no deadline is mentioned, set deadline to null
- Do not add extra text outside the JSON"""

client = AsyncOpenAI(api_key=settings.openai_api_key)


async def parse_tasks(text: str) -> List[TaskItem]:
    """Parse unstructured text into structured tasks using LLM."""
    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from LLM")

        data = json.loads(content)
        tasks = []

        for task_data in data.get("tasks", []):
            subtasks = [
                SubTask(title=st["title"], completed=st.get("completed", False))
                for st in task_data.get("subtasks", [])
            ]

            tasks.append(TaskItem(
                title=task_data["title"],
                priority=Priority(task_data.get("priority", "medium")),
                subtasks=subtasks,
                deadline=task_data.get("deadline")
            ))

        return tasks

    except Exception as e:
        raise Exception(f"Failed to parse tasks: {str(e)}")
