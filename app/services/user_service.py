from database import cursor

def get_user_id(username):
    cursor.execute(
        "SELECT id FROM users WHERE username = %s",
        (username,)
    )
    row = cursor.fetchone()
    user_id = row[0]
    return user_id