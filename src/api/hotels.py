from datetime import date
from fastapi import APIRouter, HTTPException, Path, Query, Body, status
import logging
from typing import List

from fastapi.openapi.models import Example
from fastapi.responses import JSONResponse

from src.api.dependencies import DBDep
from src.schemas.hotels import HotelPartialData, HotelCreateData, Hotel

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/", response_model=List[Hotel], summary="Get list of available hotels for given check-in and check-out dates")
async def get_hotels(
    db: DBDep,
    title: str | None = Query(default=None, description="Title of the hotel", min_length=2),
    location: str | None = Query(default=None, description="Location of the hotel", min_length=2),
    page: int = Query(default=1, description="Page number", ge=1),
    per_page: int = Query(default=3, description="Number of items per page", ge=1, le=100),
    check_in: date = Query(description="Check-in date", example="2025-07-01"),
    check_out: date = Query(description="Check-out date", example="2025-07-20")
):
    """ Get list of available hotels for given check-in and check-out dates """
    hotels = await db.hotels.get_available_hotels( 
            check_in=check_in,
            check_out=check_out,
            limit=per_page,
            offset=(page - 1) * per_page,
            title=title, 
            location=location
        )
    return hotels


@router.get("/{hotel_id}", response_model=Hotel)
async def get_hotel(
    db: DBDep,
    hotel_id: int = Path(description="ID of the hotel", gt=0),
):
    """ Get hotel by ID """
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    return hotel


@router.post("/", response_model=Hotel, status_code=status.HTTP_201_CREATED)
async def create_hotel(
    db: DBDep,
    hotel_data: HotelCreateData = Body(openapi_examples={
    "City 1": Example(
        summary = "The Ritz-Carlton",
        value = {"title": "The Ritz-Carlton", "stars": 5, "location": "New York"}
    ),
    "City 2": Example(
        summary = "The Westin",
        value = {"title": "The Westin", "stars": 4, "location": "San Francisco"}
    )
}) ):
    """ Create new hotel in Database"""
    hotel_added = await db.hotels.add(hotel_data)
    await db.commit()
    return hotel_added


@router.put("/{hotel_id}", response_model=Hotel)
async def edit_hotel(
    db: DBDep,
    hotel_id: int = Path(description="ID of the hotel", gt=0),
    hotel_data: HotelCreateData = Body(openapi_examples={
        "Hotel 1": Example(
            summary = "Update hotel with new title",
            value = {"title": "The Grand Hotel", "stars": 5, "location": "Los Angeles"}
        ),
    })
):
    """ Update hotel with full parameters list """
    # Check if hotel exists
    existing_hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not existing_hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    hotel_edited = await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return hotel_edited


@router.delete("/{hotel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hotel(
    db: DBDep,
    hotel_id: int = Path(description="ID of the hotel", gt=0),
):
    """ Delete hotel by ID """
    # Check if hotel exists
    existing_hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not existing_hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    await db.hotels.delete(id=hotel_id)
    await db.commit()


@router.patch("/{hotel_id}", response_model=Hotel)
async def update_hotel(
    db: DBDep,
    hotel_id: int = Path(description="ID of the hotel", gt=0),
    hotel_data: HotelPartialData = Body(openapi_examples={
            "Hotel 1": Example(
                summary = "Update hotel with new title",
                value = {"title": "The Grand Resort"}
            ),
        })
    ):
    """ Partial Update hotel by ID and partial parameters list """
    # Check if hotel exists
    existing_hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if not existing_hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hotel with ID {hotel_id} not found"
        )
    
    hotel_edited = await db.hotels.edit(hotel_data, id=hotel_id, partial_update=True)
    await db.commit()
    return hotel_edited