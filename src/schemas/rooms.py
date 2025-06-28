"""
Pydantic schemas for Rooms and Room Types
"""

from typing import Optional, get_type_hints
from pydantic import BaseModel, Field
from src.schemas.facilities import Facilities

# Rooms
class RoomBaseModel(BaseModel):
    room_type_id: int = Field(description="ID of the room type", gt=0)
    number: str = Field(description="Number of the room", min_length=1, max_length=10)
    title: str = Field(description="Title of the room", max_length=100)
    description: Optional[str | None] = Field(description="Description of the room", max_length=200)
    price: int = Field(description="Price of the room", ge=0)

class Room(RoomBaseModel):
    id: int = Field(description="ID of the room")
    hotel_id: int = Field(description="ID of the hotel", gt=0)

class RoomCreateModel(RoomBaseModel):
    hotel_id: int = Field(description="ID of the hotel", gt=0)

class RoomCreateRequest(RoomBaseModel):
    """Room creation Model request for HTTP Request"""
    facilities: list[int] = Field(description="List of facility IDs", default=[]) 

class RoomPartialDataModel(RoomCreateModel):
    number: Optional[get_type_hints(RoomCreateModel)["number"]] = None
    title: Optional[get_type_hints(RoomCreateModel)["title"]] = None
    description: Optional[get_type_hints(RoomCreateModel)["description"]] = None
    price: Optional[get_type_hints(RoomCreateModel)["price"]] = None
    room_type_id: Optional[get_type_hints(RoomCreateModel)["room_type_id"]] = None
    hotel_id: Optional[get_type_hints(RoomCreateModel)["hotel_id"]] = None
    

class RoomPartialDataRequest(RoomPartialDataModel):
    facilities: Optional[list[int]] = None

# Room types
class RoomTypeBaseModel(BaseModel):
    title: str = Field(description="Title of the room type", max_length=100)
    description: Optional[str | None] = Field(description="Description of the room type", max_length=200)

class RoomType(RoomTypeBaseModel):
    id: int = Field(description="ID of the room type")

class RoomTypeCreateData(RoomTypeBaseModel):
    pass

class RoomsWithFacilities(Room):
    facilities: list[Facilities] | None = Field(description="List of facilities")