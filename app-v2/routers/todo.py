from fastapi import APIRouter, Depends, HTTPException
from model import ToDo, User
from auth import verify_access_token, get_user_id
from database import conn, cursor 

router = APIRouter()

@router.get("/todos/{todo_id}")
def get_todo(
    todo_id: int, 
    username: str = Depends(verify_access_token)
    ):
    
    user_id = get_user_id(username)
    
    cursor.execute(
        "SELECT id, title FROM todos WHERE user_id = ? AND id = ?",
        (user_id, todo_id )
    )
    
    row = cursor.fetchone()
    
    if row is None:
        raise HTTPException(
            status_code=404,
            detail="todo not found"
        )

    return {
        "id": row[0],
        "title": row[1]   
    }
    

@router.post("/todos")
def create_todo(
    todo: ToDo, 
    username: str = Depends(verify_access_token)
    ):

    cursor.execute(
        "SELECT id FROM users WHERE username = ?",
        (username,)
    )
    row = cursor.fetchone()
    # database fetch like this (joe,)
    user_id = row[0]

    cursor.execute(
        "INSERT INTO todos (title, user_id) VALUES (?,?)",
        (todo.title, user_id)
    )

    conn.commit()

    return {
        "status": "created"
    }
