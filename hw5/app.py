# Создать API для добавления нового пользователя в базу данных. Приложение
# должно иметь возможность принимать POST запросы с данными нового
# пользователя и сохранять их в базу данных.

# Создайте модуль приложения и настройте сервер и маршрутизацию.
# Создайте класс user с полями id, name, email и password.
# Создайте список users для хранения пользователей.

# Создать API для обновления информации о пользователе в базе данных.
# Приложение должно иметь возможность принимать PUT запросы с данными
# пользователей и обновлять их в базе данных.

# Создать API для удаления информации о пользователе из базы данных.
# Приложение должно иметь возможность принимать DELETE запросы и
# удалять информацию о пользователе из базы данных.

# Создать веб-страницу для отображения списка пользователей. Приложение
# должно использовать шаблонизатор Jinja для динамического формирования HTML
# страницы.

import logging
from typing import Optional

import uvicorn
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="hw5/templates")


class UserIn(BaseModel):
    name: Optional[str] = None
    email: str
    password: str


class User(UserIn):
    id: int


users = []


@app.get('/users', response_class=HTMLResponse, summary="Вывод списка пользователей", tags=['HTML'])
async def get_users(request: Request):
    logger.info('Отработал GET-запрос на вывод пользователей')
    return templates.TemplateResponse("index.html", {"request": request, "users": users})


@app.post("/users", response_class=HTMLResponse, summary="Удаление пользователя по id", tags=['HTML'])
async def delete_user(request: Request, user_id: int = Form()):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            logger.info(
                f'Отработал DELETE-запрос для задачи user_id = {user_id}')
            break
    return templates.TemplateResponse("index.html", {"request": request, "users": users})


@app.get("/users/add", response_class=HTMLResponse, summary="Добавление пользователя", tags=['HTML'])
def add_user(request: Request):
    return templates.TemplateResponse("add_user.html", {"request": request})


@app.post("/create_user", response_class=HTMLResponse, summary="Создание пользователя", tags=['HTML'])
async def create_user(request: Request):
    data = await request.form()
    id = len(users) + 1
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if name == None:
        name = email
    new_user = User(
        id=id,
        name=name,
        email=email,
        password=password,
    )
    users.append(new_user)
    logger.info(f'Отработал POST-запрос, добавлен пользователь {name}')
    return templates.TemplateResponse('add_sucsess.html', {"request": request})


# API
@app.get('/', response_model=list[User], summary="Вывод списка пользователей", tags=['Users'])
async def all_users():
    logger.info('Отработал GET-запрос на вывод пользователей')
    return users


@app.post("/add_new_user/", response_model=User, summary="Добавление пользователя", tags=['Users'])
async def add_new_user(user: UserIn):
    id = len(users) + 1
    if user.name == None:
        name = user.email
    else:
        name = user.name
    new_user = User(
        id=id,
        name=name,
        email=user.email,
        password=user.password,
    )
    users.append(new_user)
    logger.info(f'Отработал POST-запрос, добавлен пользователь {name}')
    return new_user


@app.get("/{user_id}", response_model=User, summary="Поиск пользователя по id", tags=['Users'])
async def find_user(user_id: int):
    for user in users:
        if user.id == user_id:
            logger.info(f'Отработал find-запрос по id-{user_id}')
            return user


@app.put("/users/{user_id}", response_model=User, summary="Изменение данных пользователя", tags=['Users'])
async def update_user(user_id: int, new_user: UserIn):
    for user in users:
        if user.id == user_id:
            user.name = new_user.name
            user.email = new_user.email
            user.password = new_user.password
            logger.info(f'Отработал PUT-запрос для задачи user_id = {user_id}')
            return user
    raise HTTPException(status_code=404, detail="user not found")


@app.delete("/users/{user_id}", summary="Удаление пользователя", tags=['Users'])
async def delete_user_for_id(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            logger.info(
                f'Отработал DELETE-запрос для задачи user_id = {user_id}')
    return {"user_id": user_id}


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
