from fastapi import APIRouter, HTTPException, Path, Query, Body, status
import logging
from typing import List

from fastapi.openapi.models import Example

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingCreateRequest, Booking

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/", response_model=List[Booking])
async def get_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    """Get all bookings for a user"""
    bookings = await db.bookings.get_all(user_id=user_id)
    return bookings


@router.post("/", response_model=Booking, status_code=status.HTTP_201_CREATED)
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingCreateRequest = Body(openapi_examples={
        "Booking 1": Example(
            summary="Create a booking",
            value={
                "room_id": 1, 
                "check_in": "2025-07-01", 
                "check_out": "2025-07-02",
            }
        )
    })
):
    """Create a booking"""
    booking_added = await db.bookings.add(BookingAdd(**booking_data.model_dump(), user_id=user_id))  
    await db.commit()
    return booking_added