from fastapi import FastAPI
from routers import register
from routers import login
from routers import todo

app = FastAPI()

app.include_router(register.router)
app.include_router(login.router)
app.include_router(todo.router)