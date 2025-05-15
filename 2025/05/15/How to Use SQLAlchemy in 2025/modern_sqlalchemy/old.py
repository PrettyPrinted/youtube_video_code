# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "sqlalchemy",
# ]
# ///
from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, ForeignKey, Integer, Text, String, DateTime
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

engine = create_engine("sqlite:///db.sqlite3")

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    last_login = Column(DateTime)

    posts = relationship("Post", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"
    
class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False, default="Untitled Post")
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    user = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"Post(id={self.id}, title={self.title})"
    
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

anthony = User(name="Anthony")
kim = User(name="Kim", last_login=datetime.now(timezone.utc))

session.add(anthony)
session.add(kim)

session.commit()

post1 = Post(title="Anthony's first post", content="Hello world!")
post2 = Post(title="Kim's first post", content="Hello world!")
post3 = Post(title="Anthony's second post", content="Hello again!")
post4 = Post(title="Anthony's third post", content="Hello again!")
post5 = Post(title="Kim's second post", content="Hello again!")


anthony.posts.append(post1)
anthony.posts.append(post3)
anthony.posts.append(post4)
kim.posts.append(post2)
kim.posts.append(post5)

session.commit()

users = session.query(User).all()
for user in users:
    print(user)
    for post in user.posts:
        print(f"  {post}")

anthony = session.query(User).get(1)
if anthony:
    print(f"Found user: {anthony}")

kim = session.query(User).filter(User.name == "Kim").first()
if kim:
    print(f"Found user: {kim}")

posts = session.query(Post).filter(Post.user == anthony).order_by(Post.id.desc()).all()
for post in posts:
    print(post)
    print(f"  {post.user}")