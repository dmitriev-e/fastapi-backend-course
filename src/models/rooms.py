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
    
    hotel_rs = relationship("HotelsORM", back_populates="rooms_rs")
    room_type_rs = relationship("RoomTypesORM", back_populates="rooms_rs")

class RoomTypesORM(Base):
    __tablename__ = "room_types"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str | None]]

    rooms_rs = relationship("RoomsORM", back_populates="room_type_rs")