"""
SQLAlchemy models for Bookings
"""
from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

class BookingsORM(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey("rooms.id"), nullable=False)
    check_in: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    check_out: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)

    user = relationship("UsersORM", back_populates="bookings")
    rooms = relationship("RoomsORM", back_populates="bookings")