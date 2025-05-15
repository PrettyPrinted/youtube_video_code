# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "sqlalchemy",
# ]
# ///
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import create_engine, String, Text, select, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column, Mapped, Session, relationship

engine = create_engine("sqlite:///db.sqlite3")

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
    session.add(anthony)
    session.add(kim)
    session.commit()

    post1 = Post(title="Anthony's first post", content="Hello world!")
    post2 = Post(title="Kim's first post", content="Hello again!")
    post3 = Post(title="Anthony's second post", content="Hello world!")
    post4 = Post(title="Anthony's third post", content="Hello again!")
    post5 = Post(title="Kim's second post", content="Hello again!")

    anthony.posts.append(post1)
    anthony.posts.append(post3)
    anthony.posts.append(post4)
    kim.posts.append(post2)
    kim.posts.append(post5)

    session.commit()

    stmt = select(User)
    users = session.scalars(stmt).all()
    for user in users:
        print(user)
        for post in user.posts:
            print(f"  {post}")

    anthony = session.get(User, 1)
    if anthony:
        print(f"Found user: {anthony}")

    stmt = select(User).where(User.name == "Kim")
    kim = session.scalars(stmt).first()
    if kim:
        print(f"Found user: {kim}")

    stmt = select(Post).where(Post.user == anthony).order_by(Post.id.desc())
    posts = session.scalars(stmt).all()
    for post in posts:
        print(post)
        print(f"  {post.user}")