from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from utils import ValidationError

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

TASK_TYPES = ["command"]

class Task(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(String(16))
    cmd: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)
    result: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True, default=None)

    def validate(self):
        if self.type is None:
            raise ValidationError("Task must have a type field")
        if self.type not in TASK_TYPES:
            raise ValidationError(f"Incorrect task type: {self.type}")

        if self.type == "command":
            if self.cmd is None:
                raise ValidationError("Task with type command needs to have 'cmd' field")
