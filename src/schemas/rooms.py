from typing import Optional, get_type_hints
from pydantic import BaseModel, Field

# Rooms
class RoomBaseModel(BaseModel):
    hotel_id: int = Field(description="ID of the hotel", gt=0)
    room_type_id: int = Field(description="ID of the room type", gt=0)
    number: str = Field(description="Number of the room", min_length=1, max_length=10)
    title: str = Field(description="Title of the room", max_length=100)
    description: Optional[str | None] = Field(description="Description of the room", max_length=200)
    price: int = Field(description="Price of the room", ge=0)

class Room(RoomBaseModel):
    id: int = Field(description="ID of the room")

class RoomCreateData(RoomBaseModel):
    pass

class RoomPartialData(RoomBaseModel):
    number: Optional[get_type_hints(RoomBaseModel)["number"]] = None
    title: Optional[get_type_hints(RoomBaseModel)["title"]] = None
    description: Optional[get_type_hints(RoomBaseModel)["description"]] = None
    price: Optional[get_type_hints(RoomBaseModel)["price"]] = None
    room_type_id: Optional[get_type_hints(RoomBaseModel)["room_type_id"]] = None
    hotel_id: Optional[get_type_hints(RoomBaseModel)["hotel_id"]] = None


# Room types
class RoomTypeBaseModel(BaseModel):
    title: str = Field(description="Title of the room type", max_length=100)
    description: Optional[str | None] = Field(description="Description of the room type", max_length=200)

class RoomType(RoomTypeBaseModel):
    id: int = Field(description="ID of the room type")

class RoomTypeCreateData(RoomTypeBaseModel):
    pass