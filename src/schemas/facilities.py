"""
Facilities pydantic schemas
"""

from typing import Optional
from pydantic import BaseModel, Field


class FacilitiesBaseModel(BaseModel):
    title: str = Field(description="Facility title", examples=["Free Wi-Fi"])
    description: Optional[str | None] = Field(description="Facility description", examples=["Free Wi-Fi in the room"])

class Facilities(FacilitiesBaseModel):
    id: int = Field(description="Facility ID", examples=[1])

class FacilitiesCreateRequest(FacilitiesBaseModel):
    pass

class RoomsFacilitiesBaseModel(BaseModel):
    room_id: int = Field(description="Room ID", examples=[1])
    facility_id: int = Field(description="Facility ID", examples=[1])

class RoomsFacilities(RoomsFacilitiesBaseModel):
    id: int = Field(description="Room facility ID", examples=[1])

class RoomsFacilitiesCreateRequest(RoomsFacilitiesBaseModel):
    pass