from pydantic import BaseModel, Field


class Hotel(BaseModel):
    id: int = Field(description="ID of the hotel")
    name: str = Field(description="Name of the hotel")
    city: str = Field(description="City of the hotel")
    stars: int = Field(description="Stars of the hotel", ge=0, le=5)

class HotelCreateData(BaseModel):
    name: str = Field(description="Name of the hotel")
    city: str = Field(description="City of the hotel")
    stars: int = Field(description="Stars of the hotel", ge=0, le=5)

class HotelPartialData(BaseModel):
    name: str | None = Field(None, description="Name of the hotel")
    city: str | None = Field(None, description="City of the hotel")
    stars: int | None = Field(None, description="Stars of the hotel", ge=0, le=5)
