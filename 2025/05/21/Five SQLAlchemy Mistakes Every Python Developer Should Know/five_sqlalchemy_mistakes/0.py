# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "sqlalchemy",
# ]
# ///
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import create_engine, ForeignKey, String, Text
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
    anthony = User(name="Anthony")
    kim = User(name="Kim", last_login=datetime.now(timezone.utc))
    sarah = User(name="Sarah", last_login=datetime.now(timezone.utc))
    michael = User(name="Michael")
    jessica = User(name="Jessica", last_login=datetime.now(timezone.utc))
    session.add(anthony)
    session.add(kim)
    session.add(sarah)
    session.add(michael)
    session.add(jessica)
    session.commit()

    post1 = Post(title="Anthony's first post", content="Hello world!")
    post2 = Post(title="Kim's first post", content="Hello again!")
    post3 = Post(title="Anthony's second post", content="Hello world!")
    post4 = Post(title="Anthony's third post", content="Hello again!")
    post5 = Post(title="Kim's second post", content="Hello again!")

    post6 = Post(title="Sarah's first post", content="Hello everyone!")
    post7 = Post(title="Michael's first post", content="Nice to meet you all!")
    post8 = Post(title="Jessica's first post", content="Greetings from Jessica!")
    post9 = Post(title="Sarah's second post", content="Another post from Sarah")
    post10 = Post(title="Michael's second post", content="Michael's follow-up post")

    anthony.posts.append(post1)
    anthony.posts.append(post3)
    anthony.posts.append(post4)
    kim.posts.append(post2)
    kim.posts.append(post5)
    sarah.posts.append(post6)
    sarah.posts.append(post9)
    michael.posts.append(post7)
    michael.posts.append(post10)
    jessica.posts.append(post8)

    session.commit()
