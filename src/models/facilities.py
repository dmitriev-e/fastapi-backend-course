"""
Hotels rooms facilities model
"""

from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db import Base

class FacilitiesORM(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str | None]] = mapped_column(String(255), nullable=True)

    rooms = relationship("RoomsFacilitiesORM", back_populates="facility")


class RoomsFacilitiesORM(Base):
    __tablename__ = "rooms_facilities"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey("rooms.id"))
    facility_id: Mapped[int] = mapped_column(Integer, ForeignKey("facilities.id"))

    room = relationship("RoomsORM", back_populates="facilities")
    facility = relationship("FacilitiesORM", back_populates="rooms")
    