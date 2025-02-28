from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .extensions import db

class File(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(100))
    path: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text())
    summary: Mapped[str] = mapped_column(Text())