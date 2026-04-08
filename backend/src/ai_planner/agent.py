"""LLM Agent for task extraction and prioritization."""

import subprocess
import json
import re
import os
from typing import List
from ai_planner.models import TaskItem, SubTask, Priority

SYSTEM_PROMPT = """You are a JSON-only task extractor. You MUST respond with ONLY a JSON object, nothing else.

The JSON must have this exact structure:
{"tasks": [{"title": "task name", "priority": "high or medium or low", "subtasks": [{"title": "subtask", "completed": false}], "deadline": "YYYY-MM-DD or null"}]}

Rules:
- Extract all tasks from the user input
- Priority: high=urgent/close deadline, medium=important/not urgent, low=nice-to-have
- Create 2-3 subtasks per task
- If no deadline mentioned, use null
- NO markdown, NO code blocks, NO explanations - ONLY JSON"""


async def parse_tasks(text: str) -> List[TaskItem]:
    """Parse unstructured text into structured tasks using Qwen CLI."""
    try:
        # Combine system prompt with user input
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser brain dump to analyze:\n{text}\n\nJSON response:"

        # Write prompt to temp file to avoid shell escaping issues
        prompt_file = "/tmp/qwen_prompt.txt"
        with open(prompt_file, 'w') as f:
            f.write(full_prompt)

        result = subprocess.run(
            f"HOME=/root qwen -p \"$(cat {prompt_file})\"",
            capture_output=True,
            text=True,
            timeout=120,
            shell=True,
            env={**os.environ, "HOME": "/root"}
        )

        # Clean up temp file
        try:
            os.remove(prompt_file)
        except:
            pass

        if result.returncode != 0:
            raise ValueError(f"Qwen CLI error: {result.stderr}")

        content = result.stdout.strip()
        if not content:
            raise ValueError("Empty response from Qwen")

        # Try multiple JSON extraction strategies
        json_str = None

        # Strategy 1: Extract from ```json code block
        json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
        if json_match:
            json_str = json_match.group(1).strip()

        # Strategy 2: Extract from generic ``` code block
        if not json_str:
            json_match = re.search(r'```\s*\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1).strip()

        # Strategy 3: Find JSON object by matching braces
        if not json_str:
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1:
                json_str = content[start:end+1]

        if not json_str:
            raise ValueError(f"No JSON found in response: {content[:300]}")

        # Clean up JSON string
        json_str = json_str.strip()

        # Parse and validate
        data = json.loads(json_str)
        if "tasks" not in data:
            raise ValueError(f"Response missing 'tasks' key: {json_str[:200]}")

        tasks = []
        for task_data in data.get("tasks", []):
            subtasks = [
                SubTask(title=st["title"], completed=st.get("completed", False))
                for st in task_data.get("subtasks", [])
                if "title" in st
            ]

            tasks.append(TaskItem(
                title=task_data.get("title", "Untitled Task"),
                priority=Priority(task_data.get("priority", "medium")),
                subtasks=subtasks,
                deadline=task_data.get("deadline")
            ))

        if not tasks:
            raise ValueError("No tasks extracted from input")

        return tasks

    except Exception as e:
        raise Exception(f"Failed to parse tasks: {str(e)}")
