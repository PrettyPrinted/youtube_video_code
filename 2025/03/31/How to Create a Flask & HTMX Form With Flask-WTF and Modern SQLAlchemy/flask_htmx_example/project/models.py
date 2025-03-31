from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class PhoneNumber(Base):
    __tablename__ = "phone_number"
    id: Mapped[int] = mapped_column(primary_key=True)
    phone_type: Mapped[str] = mapped_column(String(10))
    country_code: Mapped[str] = mapped_column(String(5))
    area_code: Mapped[int]
    number: Mapped[str] = mapped_column(String(10))