# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "sqlalchemy",
# ]
# ///
from datetime import datetime
from typing import Optional

from sqlalchemy import create_engine, ForeignKey, insert, String, Text
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
    print("Adding users...")
    # for i in range(1, 10):
    #     session.add(User(name=f"User {i}"))

    new_users = []
    for i in range(1, 10):
        new_users.append({"name": f"User {i}"})

    session.execute(
        insert(User),
        new_users,
    )
    session.commit()