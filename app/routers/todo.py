from fastapi import APIRouter, Depends
from model import ToDo
from auth import verify_access_token
from services.todo_service import get_stored_todo, store_todo, update_stored_todo, delete_stored_todo
from services.user_service import get_user_id


router = APIRouter()

@router.get("/todos/{todo_id}")
def get_todo(
    todo_id: int, 
    username: str = Depends(verify_access_token)
    ):
    
    user_id = get_user_id(username)
    
    return get_stored_todo(todo_id, user_id)
    

@router.post("/todos")
def create_todo(
    todo: ToDo, 
    username: str = Depends(verify_access_token)
    ):

    user_id = get_user_id(username)

    return store_todo(todo.title, user_id) 

@router.put("/todos/{todo_id}")
def update_todo(
    todo: ToDo,
    todo_id: int, 
    username: str = Depends(verify_access_token)
    ):

    user_id = get_user_id(username)

    return update_stored_todo(todo.title, todo_id, user_id)

@router.delete("/todos/{todo_id}")
def delete_todo(
    todo_id: int, 
    username: str = Depends(verify_access_token)
    ):

    user_id = get_user_id(username)

    return delete_stored_todo(todo_id, user_id)
    