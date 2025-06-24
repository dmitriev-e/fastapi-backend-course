from fastapi import APIRouter, HTTPException, Path, Query, Body, status
import logging
from typing import List, Any
from datetime import datetime

from fastapi.openapi.models import Example

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingCreateRequest, Booking, BookingAdd

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/me", response_model=List[Booking])
async def get_user_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    """Get all bookings for a user"""
    bookings = await db.bookings.get_all(user_id=user_id)
    return bookings

@router.get("/", response_model=List[Booking])
async def get_all_bookings(db: DBDep):
    """Get all bookings for all users"""
    bookings = await db.bookings.get_all()
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
    # Validate dates
    if (
        booking_data.check_out <= booking_data.check_in or 
        booking_data.check_out <= datetime.now().date() or 
        booking_data.check_in <= datetime.now().date()
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out date must be after check-in date and not in the past"
        )
    
    # Check if room exists
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Room with ID {booking_data.room_id} not found"
        )
    
    # Get hotel information for check-in/check-out times  
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel for room {booking_data.room_id} not found"
        )
    
    # Calculate check_in_datetime and check_out_datetime
    check_in_datetime = datetime.combine(booking_data.check_in, hotel.check_in)
    check_out_datetime = datetime.combine(booking_data.check_out, hotel.check_out)
    
    # Calculate the total price of a booking
    total_price = (booking_data.check_out - booking_data.check_in).days * room.price
    
    # Create booking instance directly in database
    booking_orm = BookingAdd(
        user_id=user_id,
        room_id=booking_data.room_id,
        total_price=total_price,
        check_in=check_in_datetime,
        check_out=check_out_datetime
    )
    
    booking_added = await db.bookings.add(booking_orm)
    await db.commit()
    
    # Convert to response schema
    return booking_added