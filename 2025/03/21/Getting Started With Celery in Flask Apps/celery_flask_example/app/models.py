from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

class Base(DeclarativeBase):
    pass


class Images(Base):
    __tablename__ = "images"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    prompt: Mapped[str]