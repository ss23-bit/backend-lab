from fastapi import APIRouter, HTTPException, status, Depends
from database import conn, cursor
from model import Todo
from auth import verify_access_token

router = APIRouter()



def check_not_found():
    raise HTTPException(
        status_code=404,
        detail="Crud not found"
    )

@router.get("/todo")
def get_todo(user = Depends(verify_access_token)):
    cursor.execute(
        "SELECT * FROM todos WHERE username = ?",
        (user["username"],)
    )

    row = cursor.fetchall()

    if row is None:
        check_not_found()

    return {
        "id": row[0],
        "title": row[1]
    }

@router.post("/todo", status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo, user = Depends(verify_access_token)):
    cursor.execute(
        "INSERT INTO todos (title, username) VALUES (?, ?)",
        (todo.title, user["username"])
    )

    conn.commit()

    return {
        "status": "created"
    }

@router.put("/todo/{todo_id}")
def update_todo(todo_id: int, todo: Todo, user = Depends(verify_access_token)):
    cursor.execute(
        "UPDATE todos SET title = ? WHERE id = ? AND username = ?",
        (todo.title, todo_id, user["username"])
    )

    conn.commit()

    if cursor.rowcount == 0:
        check_not_found()

    return {
        "status": "updated"
    }

@router.delete("/todo/{todo_id}")
def delete_todo(todo_id: int, user = Depends(verify_access_token)):
    cursor.execute(
        "DELETE FROM todos WHERE id = ? AND username = ?",
        (todo_id, user["username"])
    )

    conn.commit()
    
    if cursor.rowcount == 0:
        check_not_found()

    return {
        "status": "deleted"
    }




    