from fastapi import APIRouter, HTTPException, Path, Query, Body
import logging

from fastapi.openapi.models import Example
from fastapi.responses import JSONResponse

from src.api.dependencies import DBDep
from src.schemas.hotels import HotelPartialData, HotelCreateData

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("/")
async def get_hotels(
    db: DBDep,
    title: str | None = Query(default=None, description="Title of the hotel", min_length=2),
    location: str | None = Query(default=None, description="Location of the hotel", min_length=2),
    page: int | None = Query(default=1, description="Page number", ge=1),
    per_page: int | None = Query(default=3, description="Number of items per page", ge=1, le=100),    
):
    """ Get list of hotels """
    return await db.hotels.get_all( 
            title=title, 
            location=location,
            limit=per_page,
            offset=(page - 1) * per_page
        )


@router.get("/{hotel_id}")
async def get_hotel(
    db: DBDep,
    hotel_id: int = Path(description="ID of the hotel", gt=0),
):
    """ Get hotel by ID """
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel


@router.post("/")
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
    return JSONResponse(status_code=200, content={"detail": "Hotel created", "data": hotel_added.model_dump()})


@router.put("/{hotel_id}")
async def edit_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelCreateData = Body(openapi_examples={
        "Hotel 1": Example(
            summary = "Update hotel with new title",
            value = {"title": "The Grand Hotel", "stars": 5, "location": "Los Angeles"}
        ),
    })
):
    """ Update hotel with full parameters list """

    hotel_edited = await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return JSONResponse(status_code=200, content={"detail": "Hotel updated", "data": hotel_edited.model_dump()})


@router.delete("/{hotel_id}")
async def delete_hotel(
    db: DBDep,
    hotel_id: int,
):
    """ Delete hotel by ID """

    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return JSONResponse(status_code=200, content={"detail": "Hotel deleted"})


@router.patch("/{hotel_id}")
async def update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPartialData = Body(openapi_examples={
            "Hotel 1": Example(
                summary = "Update hotel with new title",
                value = {"title": "The Grand Resort"}
            ),
        })
    ):
    """ Partial Update hotel by ID and partial parameters list """

    hotel_edited = await db.hotels.edit(hotel_data, id=hotel_id, partial_update=True)
    await db.commit()
    return JSONResponse(status_code=200, content={"detail": "Hotel updated", "data": hotel_edited.model_dump()})