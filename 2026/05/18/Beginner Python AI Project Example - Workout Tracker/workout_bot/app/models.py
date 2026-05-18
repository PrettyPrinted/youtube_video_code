from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.types import JSON
from pydantic import BaseModel, Field

class Base(DeclarativeBase):
    pass


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int]
    thread_id: Mapped[int]
    data: Mapped[dict] = mapped_column(JSON)


class Workout(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True)
    exercise: Mapped[str] = mapped_column()
    reps: Mapped[int] = mapped_column()
    weight: Mapped[int] = mapped_column()


class Set(BaseModel):
    exercise: str = Field(description='Name of the exercise')
    reps: int = Field(description='Number of repetitions for the workout')
    weight: int = Field(description='Weight used for the workout')


class Output(BaseModel):
    sets: list[Set] = Field(description='Individual set for the workout')
    follow_up: str = Field(description='Follow-up questions if the user needs to clarify other things in workout.')
    to_follow_up: bool = Field(description='Indicates if the workout needs follow-up information.')
