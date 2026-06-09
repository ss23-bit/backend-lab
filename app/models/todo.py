from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models.user import User

class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(
        primary_key=True    
    )
    
    title: Mapped[str] = mapped_column(
        nullable=False
    )
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="todos"
    )