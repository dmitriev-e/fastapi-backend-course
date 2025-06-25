from datetime import date
from fastapi import APIRouter, HTTPException, Path, Query, Body
import logging

from fastapi.openapi.models import Example
from fastapi.responses import JSONResponse

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomCreateModel, RoomCreateRequest, RoomPartialData

logger = logging.getLogger("uvicorn")

router = APIRouter(tags=["Rooms"])


@router.get("/rooms/available", summary="Get all available rooms")
async def get_available_rooms(
    db: DBDep,
    check_in: date = Query(description="Check-in date", example="2025-07-01"),
    check_out: date = Query(description="Check-out date", example="2025-07-20")
):
    """ Get all available rooms for given check-in and check-out dates """
    rooms = await db.rooms.get_available_rooms(check_in, check_out)
    if not rooms:
        raise HTTPException(status_code=404, detail=f"Rooms not found for check_in: {check_in} and check_out: {check_out}")
    return rooms


@router.get("/hotels/{hotel_id}/rooms/{room_id}", summary="Get room by ID")
async def get_room_by_id(
    db: DBDep,
    hotel_id: int = Path(description="ID of the hotel", gt=0, openapi_examples={
        "Hotel ID=1": Example(
            summary = "Hotel ID=1",
            value = 1
        ),
    }),
    room_id: int = Path(description="ID of the room", gt=0, openapi_examples={
        "Room ID=1": Example(
            summary = "Room ID=1",
            value = 1
        ),
    })    
    ):
    """ Get room by ID """
    logger.info(f"Getting room by ID: {room_id}")
    room = await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.post("/hotels/{hotel_id}/rooms", summary="Create new room in the hotel")
async def create_room(
    db: DBDep,
    hotel_id: int = Path(description="ID of the hotel", gt=0, openapi_examples={
        "Hotel ID=1": Example(
            summary = "Hotel ID=1",
            value = 1
        ),
    }),
    room_data: RoomCreateRequest = Body(openapi_examples={
    "Room 1": Example(
        summary = "Ocean View Hotel - Single Room - Ocean View Suite",
        value = {
            "room_type_id": 1,
            "number": "301",
            "title": "Ocean View Suite",
            "description": "A luxurious suite with ocean views.",
            "price": 100}
    ),
    "Room 2": Example(
            summary = "Ocean View Hotel - Double Room - Ocean View Double",
        value = {
            "room_type_id": 2,
            "number": "302",
            "title": "Ocean View Double",
            "description": "A double room with ocean views.",
            "price": 200}
    )
}) ):
    """ Create new room in Database"""
    _room_data = RoomCreateModel(**room_data.model_dump(), hotel_id=hotel_id)
    room_added = await db.rooms.add(_room_data)
    await db.commit()
    return JSONResponse(status_code=200, content={"detail": "Room created", "data": room_added.model_dump()})


@router.put("/hotels/{hotel_id}/rooms/{room_id}", summary="Update room with full parameters list")
async def edit_room_full_data(
    db: DBDep,
    hotel_id: int = Path(description="ID of the hotel", gt=0),
    room_id: int = Path(description="ID of the room", gt=0, openapi_examples={
        "Room ID=1": Example(
            summary = "Room ID=1",
            value = 1
        ),
    }),
    room_data: RoomCreateRequest = Body(openapi_examples={
        "Room 1": Example(
            summary = "Update room with new title",
            value = {
                "room_type_id": 1,
                "number": "301",
                "title": "The Grand Room",
                "description": "A grand room with a view of the ocean.",
                "price": 100
                }
        ),
    })
    ):
    """ Update room with full parameters list """
    _room_data = RoomCreateModel(**room_data.model_dump(), hotel_id=hotel_id)
    room_edited = await db.rooms.edit(_room_data, id=room_id)
    await db.commit()
    return JSONResponse(status_code=200, content={"detail": "Room updated", "data": room_edited.model_dump()})


@router.delete("/hotels/{hotel_id}/rooms/{room_id}", summary="Delete room by ID in the hotel")
async def delete_room_by_id(
    db: DBDep,
    hotel_id: int = Path(description="ID of the hotel", gt=0),
    room_id: int = Path(description="ID of the room", gt=0),
):
    """ Delete room by ID """

    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return JSONResponse(status_code=200, content={"detail": "Room deleted"})


@router.patch("/hotels/{hotel_id}/rooms/{room_id}", summary="Update room by ID in the hotel with partial parameters list")
async def update_room_partial_data(
    db: DBDep,
    hotel_id: int = Path(description="ID of the hotel", gt=0),
    room_id: int = Path(description="ID of the room", gt=0),
    room_data: RoomPartialData = Body(openapi_examples={
        "Room 1": Example(
            summary = "Change room title, price and description",
            value = {
                "title": "The Biggest Room",
                "description": "A biggest room with a view of the ocean",
                "price": 1000
                }
        ),
    })
    ):
    """ Partial Update room by ID and partial parameters list """

    room_edited = await db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id, partial_update=True)
    await db.commit()
    return JSONResponse(status_code=200, content={"detail": "Room updated", "data": room_edited.model_dump()})
