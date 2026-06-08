from database import engine
from models.todo import Todo 
from models.user import User
from database import Base

Base.metadata.create_all(bind=engine)

