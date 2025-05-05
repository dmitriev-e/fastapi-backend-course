from fastapi import APIRouter, HTTPException, Path, Query, Body
import logging

from fastapi.openapi.models import Example

from src.db import async_session_maker
from src.schemas.hotels import HotelPartialData, HotelCreateData
from src.repositories.hotels import HotelsRepository

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/")
async def get_hotels(
        title: str | None = Query(default=None, description="Title of the hotel", min_length=2),
        location: str | None = Query(default=None, description="Location of the hotel", min_length=2),
        page: int | None = Query(default=1, description="Page number", ge=1),
        per_page: int | None = Query(default=3, description="Number of items per page", ge=1, le=100),
):
    """ Get list of hotels """
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all( 
            title=title, 
            location=location,
            limit=per_page,
            offset=(page - 1) * per_page
        )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int = Path(description="ID of the hotel", gt=0)):
    """ Get hotel by ID """
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).get_one_or_none(id=hotel_id)
        if hotel is None:
            raise HTTPException(status_code=404, detail="Hotel not found")
        return hotel


@router.post("/")
async def create_hotel(hotel_data: HotelCreateData = Body(openapi_examples={
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

    async with async_session_maker() as session:
        hotel_added = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "message": f"Hotel created", "data": hotel_added}


@router.put("/{hotel_id}")
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelCreateData = Body(openapi_examples={
            "Hotel 1": Example(
                summary = "Update hotel with new title",
                value = {"title": "The Grand Hotel", "stars": 5, "location": "Los Angeles"}
            ),
        })
    ):
    """ Update hotel with full parameters list """

    async with async_session_maker() as session:
        hotel_edited = await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK", "message": f"Hotel {hotel_id=} updated", "data": hotel_edited}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    """ Delete hotel by ID """

    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK", "message": f"Hotel {hotel_id=} deleted"}


@router.patch("/{hotel_id}")
async def update_hotel(
        hotel_id: int,
        hotel_data: HotelPartialData = Body(openapi_examples={
            "Hotel 1": Example(
                summary = "Update hotel with new title",
                value = {"title": "The Grand Resort"}
            ),
        })
    ):
    """ Partial Update hotel by ID and partial parameters list """

    async with async_session_maker() as session:
        hotel_edited = await HotelsRepository(session).edit(hotel_data, id=hotel_id, partial_update=True)
        await session.commit()
    return {"status": "OK", "message": f"Hotel {hotel_id=} updated", "data": hotel_edited}