"""
SQLAlchemy models for Rooms and Room Types
"""
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

class RoomsORM(Base):
    __tablename__ = "rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    room_type_id: Mapped[int] = mapped_column(ForeignKey("room_types.id"))
    number: Mapped[str] = mapped_column(String(10))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str | None]]
    price: Mapped[int]
    
    hotel = relationship("HotelsORM", back_populates="rooms")
    room_type = relationship("RoomTypesORM", back_populates="rooms")
    bookings = relationship("BookingsORM", back_populates="room")
    facilities = relationship("RoomsFacilitiesORM", back_populates="room")

class RoomTypesORM(Base):
    __tablename__ = "room_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str | None]]

    rooms = relationship("RoomsORM", back_populates="room_type")