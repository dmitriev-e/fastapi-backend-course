from datetime import date
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import selectinload
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM, RoomTypesORM
from src.schemas.rooms import Room, RoomType

class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = Room

    async def get_available_rooms(self, check_in: date, check_out: date):
        # Define the CTE (Common Table Expression) for rooms_booked
        rooms_booked_cte = (
            select(BookingsORM)
            .where(
                or_(
                    and_(
                        BookingsORM.check_in >= check_in,
                        BookingsORM.check_in <= check_out
                    ),
                    and_(
                        BookingsORM.check_out >= check_in,
                        BookingsORM.check_out <= check_out
                    )
                )
            )
            .cte('rooms_booked')
        )
        
        # Main query to get available rooms
        available_rooms_query = (
            select(RoomsORM)
            .where(
                RoomsORM.id.not_in(
                    select(rooms_booked_cte.c.room_id)
                )
            )
        )

        result = await self.session.execute(available_rooms_query)
        return [self.schema.model_validate(res, from_attributes=True) for res in result.scalars().all()]

class RoomTypesRepository(BaseRepository):
    model = RoomTypesORM
    schema = RoomType