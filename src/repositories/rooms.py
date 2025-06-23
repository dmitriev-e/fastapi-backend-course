from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM, RoomTypesORM
from src.schemas.rooms import Room, RoomType

class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

class RoomTypesRepository(BaseRepository):
    model = RoomTypesORM
    schema = RoomType