from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(
        Integer,
        primary_key=True    
    )
    
    title = Column(
        String,
        nullable=False
    )
    
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )