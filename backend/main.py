from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import openai
import models, database

app = FastAPI()

# Создаем таблицы при запуске
models.Base.metadata.create_all(bind=database.engine)

# Настройка Qwen (замени URL на API провайдера, если не используешь локальную Ollama)
client = openai.OpenAI(
    base_url="http://host.docker.internal:11434/v1", 
    api_key="token"
)

class TaskInput(BaseModel):
    content: str

@app.post("/generate-plan")
def generate_plan(data: TaskInput, db: Session = Depends(database.get_db)):
    prompt = f"Разбей этот список дел на задачи с приоритетами (High, Medium, Low) в формате JSON: {data.content}"
    
    response = client.chat.completions.create(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    # Тут можно добавить логику сохранения в PostgreSQL (models.Task)
    return response.choices[0].message.content
