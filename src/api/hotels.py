from fastapi import APIRouter, Query, Body
import logging

from fastapi.openapi.models import Example
from sqlalchemy.dialects.mysql import insert

from src.db import async_session_maker
from src.schemas.hotels import Hotel, HotelPartialData, HotelCreateData
from src.models.hotels import HotelsORM

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/hotels", tags=["Hotels"])

@router.get("/")
async def get_hotels(
        hotel_id: int | None = Query(default=None, description="ID of the hotel"),
        title: str | None = Query(default=None, description="Title of the hotel"),
        location: str | None = Query(default=None, description="Location of the hotel"),
        page: int | None = Query(default=1, description="Page number", ge=1),
        per_page: int | None = Query(default=3, description="Number of items per page", ge=1, le=100),
) -> list[Hotel]:
    """ Get list of hotels """

    async with async_session_maker() as session:
        pass
    hotels = []
    return_data = []
    for hotel in hotels:
        if title and title.lower() not in hotel.name.lower():
            continue
        if hotel_id and hotel_id != hotel.id:
            continue
        if location and location.lower() not in hotel.city.lower():
            continue
        return_data.append(hotel)
    if page and per_page:
        return return_data[(page - 1) * per_page:page * per_page]
    else:
        return return_data


@router.post("/")
async def create_hotel(hotel_data: HotelCreateData = Body(openapi_examples={
    "City 1": Example(
        summary = "The Ritz-Carlton",
        value = {"title": "The Ritz-Carlton", "stars": 5, "locaiton": "New York"}
    ),
    "City 2": Example(
        summary = "The Westin",
        value = {"title": "The Westin", "stars": 4, "locaiton": "San Francisco"}
    )
}) ) -> dict:
    """ Create new hotel in Database"""

    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsORM).values(**hotel_data.model_dump())
        new_hotel_id = await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": 200, "message": f"Hotel {new_hotel_id} created"}


@router.put("/{hotel_id}")
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelCreateData
) -> dict:
    """ Update hotel with full parameters list """

    for hotel in hotels:
        if hotel.id == hotel_id:
            hotel.name = hotel_data.name
            hotel.stars = hotel_data.stars
            hotel.city = hotel_data.city
            return {"status": 200, "message": f"Hotel {hotel_id=} updated", "data": hotel}
        else:
            continue
    return {"status": 404, "message": f"Hotel {hotel_id=} not found"}


@router.patch("/{hotel_id}")
async def update_hotel(
        hotel_id: int,
        hotel_data: HotelPartialData
) -> dict:
    """ Partial Update hotel by ID and partial parameters list """

    for hotel in hotels:
        if hotel.id == hotel_id:
            if hotel_data.name:
                hotel.name = hotel_data.name
            if hotel_data.stars:
                hotel.stars = hotel_data.stars
            if hotel_data.city:
                hotel.city = hotel_data.city
            return {"status": 200, "message": f"Hotel {hotel_id=} updated", "data": hotel}
        else:
            continue
    return {"status": 404, "message": f"Hotel {hotel_id=} not found"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int) -> dict:
    """ Delete hotel by ID """

    for hotel in hotels:
        logger.info(hotel)
        if hotel.id == hotel_id:
            hotels.remove(hotel)
            return {"status": 200, "message": f"Hotel {hotel_id=} deleted"}
        else:
            continue
    return {"status": 404, "message": f"Hotel {hotel_id=} not found"}

