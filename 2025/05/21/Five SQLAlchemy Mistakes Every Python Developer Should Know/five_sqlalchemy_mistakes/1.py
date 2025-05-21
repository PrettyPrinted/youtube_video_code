# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "sqlalchemy",
# ]
# ///
from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine, ForeignKey, func, select, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session

engine = create_engine("sqlite:///db.sqlite3", echo=True)

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    last_login: Mapped[Optional[datetime]]

    posts: Mapped[list["Post"]] = relationship(back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"

class Post(Base):
    __tablename__ = "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), default="Untitled Post")
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title})"
    
Base.metadata.create_all(engine)

with Session(engine) as session:
    #stmt = select(Post)
    stmt = select(func.count("*")).select_from(Post)
    #result = session.scalars(stmt).all()
    result = session.scalar(stmt)
    #print("Number of posts:", len(result))
    print("Number of posts:", result)