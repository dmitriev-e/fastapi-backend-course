"""
Facilities repository
"""

from src.models.facilities import FacilitiesORM, RoomsFacilitiesORM
from src.schemas.facilities import Facilities, RoomsFacilities
from src.repositories.base import BaseRepository

class FacilitiesRepository(BaseRepository):
    model = FacilitiesORM
    schema = Facilities

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomsFacilities