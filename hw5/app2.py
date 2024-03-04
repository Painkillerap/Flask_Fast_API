"""
Необходимо создать API для управления списком задач.
Каждая задача должна содержать заголовок и описание.
Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).

API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
Для этого использовать библиотеку Pydantic.
"""
import logging
import random
from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str


tasks_db = []

for i in range(0, 10):
    newTask = Task(
        id=i,
        title=f"Задача № {i}",
        description=f"Описание задачи №{i}",
        status=random.choice(['Done', 'Not completed']))
    tasks_db.append(newTask)


def get_task_by_id(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


# GET /tasks
@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    logger.info(f'Отработал GET запрос.')
    return tasks_db


# GET /tasks/{id}
@app.get("/tasks/{task_id}", response_model=Task)
async def get_task(task_id: int):
    logger.info(f'Отработал GET запрос для task id = {task_id}.')
    return get_task_by_id(task_id)


# POST /tasks
@app.post("/tasks", response_model=Task)
async def create_task(task: Task):
    task.id = len(tasks_db) + 1
    tasks_db.append(task)
    logger.info('Отработал POST запрос.')
    return task


# PUT /tasks/{id}
@app.put("/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, updated_task: Task):
    if get_task_by_id(task_id):
        tasks_db[task_id] = updated_task
        logger.info(f'Отработал PUT запрос для task id = {task_id}.')
        return updated_task
    return HTTPException(status_code=404, detail="Task not found")


# DELETE /tasks/{id}
@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    task = get_task_by_id(task_id)
    tasks_db.remove(task)
    logger.info(f'Отработал DEL запрос для task id = {task_id}.')
    return task if task else HTTPException(status_code=404, detail="Task not found")
