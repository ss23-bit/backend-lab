from pydantic import BaseModel

class Todo(BaseModel):
    title: str

class LoginRequest(BaseModel):
    username: str
    password: str