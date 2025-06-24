"""
SQLAlchemy models for Hotels
"""
from datetime import time
from sqlalchemy import String, Integer, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

class HotelsORM(Base):
    __tablename__ = "hotels"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    stars: Mapped[int]
    location: Mapped[str] = mapped_column(String(200))
    check_in: Mapped[time] = mapped_column(Time, nullable=True, default=time(14, 0))
    check_out: Mapped[time] = mapped_column(Time, nullable=True, default=time(12, 0))

    rooms = relationship("RoomsORM", back_populates="hotel")