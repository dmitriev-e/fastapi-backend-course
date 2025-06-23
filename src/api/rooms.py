from fastapi import APIRouter, HTTPException, Path, Query, Body
import logging

from fastapi.openapi.models import Example
from fastapi.responses import JSONResponse

from src.db import async_session_maker
from src.schemas.rooms import RoomCreateData, RoomPartialData
from src.repositories.rooms import RoomsRepository

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/{room_id}")
async def get_room_by_id(
    room_id: int = Path(description="ID of the room", gt=0, openapi_examples={
        "Room ID=1": Example(
            summary = "Get room by ID=1",
            value = 1
        ),
    })    
    ):
    """ Get room by ID """
    logger.info(f"Getting room by ID: {room_id}")
    async with async_session_maker() as session:
        room = await RoomsRepository(session).get_one_or_none(id=room_id)
        if room is None:
            raise HTTPException(status_code=404, detail="Room not found")
        return room

@router.post("/")
async def create_room(room_data: RoomCreateData = Body(openapi_examples={
    "Room 1": Example(
        summary = "Ocean View Hotel - Single Room - Ocean View Suite",
        value = {
            "hotel_id": 1,
            "room_type_id": 1,
            "number": "301",
            "title": "Ocean View Suite",
            "description": "A luxurious suite with ocean views.",
            "price": 100}
    ),
    "Room 2": Example(
            summary = "Ocean View Hotel - Double Room - Ocean View Double",
        value = {
            "hotel_id": 1,
            "room_type_id": 2,
            "number": "302",
            "title": "Ocean View Double",
            "description": "A double room with ocean views.",
            "price": 200}
    )
}) ):
    """ Create new room in Database"""

    async with async_session_maker() as session:
        room_added = await RoomsRepository(session).add(room_data)
        await session.commit()
    return JSONResponse(status_code=200, content={"detail": "Room created", "data": room_added.model_dump()})


@router.put("/{room_id}")
async def edit_room_full_data(
        room_id: int,
        room_data: RoomCreateData = Body(openapi_examples={
            "Room 1": Example(
                summary = "Update room with new title",
                value = {
                    "hotel_id": 1,
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

    async with async_session_maker() as session:
        room_edited = await RoomsRepository(session).edit(room_data, id=room_id)
        await session.commit()
    return JSONResponse(status_code=200, content={"detail": "Room updated", "data": room_edited.model_dump()})


@router.delete("/{room_id}")
async def delete_room_by_id(room_id: int):
    """ Delete room by ID """

    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return JSONResponse(status_code=200, content={"detail": "Room deleted"})


@router.patch("/{room_id}")
async def update_room_partial_data(
        room_id: int,
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

    async with async_session_maker() as session:
        room_edited = await RoomsRepository(session).edit(room_data, id=room_id, partial_update=True)
        await session.commit()
    return JSONResponse(status_code=200, content={"detail": "Room updated", "data": room_edited.model_dump()})
