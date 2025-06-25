"""
Pydantic schemas for Hotels
"""

from datetime import time
from typing import Optional
from pydantic import BaseModel, Field


class HotelBaseModel(BaseModel):
    title: str = Field(description="Name of the hotel", max_length=100)
    location: str = Field(description="Location of the hotel", max_length=200)
    stars: int = Field(description="Stars of the hotel", ge=0, le=5)
    check_in: time = Field(description="Check-in time", default=time(14, 0))
    check_out: time = Field(description="Check-out time", default=time(12, 0))

class Hotel(HotelBaseModel):
    id: int = Field(description="ID of the hotel")

class HotelCreateData(HotelBaseModel):
    pass

class HotelPartialData(HotelBaseModel):
    title: Optional[str] = None
    location: Optional[str] = None
    stars: Optional[int] = None
    check_in: Optional[time] = None
    check_out: Optional[time] = None
