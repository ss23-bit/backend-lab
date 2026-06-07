from fastapi import HTTPException
from database import cursor, conn

def raise_error():

    raise HTTPException(
        status_code=404,
        detail="todo not found"
    )

def get_stored_todo(todo_id: int, user_id: int):
    cursor.execute(
            """
            SELECT todos.id, todos.title, users.username
            FROM todos JOIN users ON todos.user_id = users.id
            WHERE todos.id = %s AND todos.user_id = %s
            """,
            (todo_id, user_id)
        )
        
    row = cursor.fetchone()
        
    if row is None:
        raise_error()
    
    title = row[1]
    username = row[2]

    return {
        "id": todo_id,
        "title": title,
        "username": username   
    }

def store_todo(todo: str, user_id: int):

    if not todo:
        raise HTTPException(
            status_code=400,
            detail="title cannot be empty"
        )
     
    cursor.execute(
        "INSERT INTO todos (title, user_id) VALUES (%s, %s)",
        (todo, user_id)
    )

    conn.commit()

    return {
        "status": "created"
    }

def update_stored_todo(todo: str, todo_id: int, user_id: int):
    cursor.execute(
        "UPDATE todos SET title = %s WHERE id = %s AND user_id = %s",
        (todo, todo_id, user_id)
    )
    conn.commit()

    if cursor.rowcount == 0:
        raise_error()

    return {
        "status": "updated"
    }

def delete_stored_todo(todo_id: int, user_id: int):
    cursor.execute(
        "DELETE FROM todos WHERE id = %s AND user_id = %s",
        (todo_id, user_id)
    )
    
    conn.commit()

    if cursor.rowcount == 0:
        raise_error()

    return {
        "status": "deleted"
    }