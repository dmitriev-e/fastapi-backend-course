from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base

class HotelsORM(Base):
    __tablename__ = "hotels"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    stars: Mapped[int]
    location: Mapped[str] = mapped_column(String(200))