"""
Bookings Schemas
"""

from datetime import date, datetime
from pydantic import BaseModel, Field

class Booking(BaseModel):
    id: int = Field(description="Booking ID")
    user_id: int = Field(description="User ID")
    room_id: int = Field(description="Room ID")
    check_in: datetime = Field(description="Check-in date")
    check_out: datetime = Field(description="Check-out date")
    total_price: float = Field(description="Total price")

class BookingCreateRequest(BaseModel):
    """
    Booking creation Model request for HTTP Request
    """
    room_id: int = Field(description="Room ID")
    check_in: date = Field(description="Check-in date")
    check_out: date = Field(description="Check-out date")

class BookingAdd(BookingCreateRequest):
    """
    Booking creation Model for Repository
    """
    user_id: int = Field(description="User ID")

class BookingCreateORM(BookingCreateRequest):
    """
    Booking creation Model for ORM model
    """
    user_id: int = Field(description="User ID")
    check_in: datetime = Field(description="Check-in datetime")
    check_out: datetime = Field(description="Check-out datetime")
    total_price: float = Field(description="Total price")