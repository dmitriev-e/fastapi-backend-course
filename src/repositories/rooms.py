from datetime import date
from sqlalchemy import and_, or_, select
from sqlalchemy.orm import selectinload
from src.models.bookings import BookingsORM
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsORM, RoomTypesORM
from src.schemas.rooms import RoomType, RoomsWithFacilities

class RoomsRepository(BaseRepository):
    model = RoomsORM
    schema = RoomsWithFacilities

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
            select(self.model)
            .options(selectinload(self.model.facilities))
            .where(
                self.model.id.not_in(
                    select(rooms_booked_cte.c.room_id)
                )
            )
        )

        result = await self.session.execute(available_rooms_query)
        result_scalars = result.scalars().all()
        return [self.schema.model_validate(res, from_attributes=True) for res in result_scalars]

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        return self.schema.model_validate(res, from_attributes=True)

class RoomTypesRepository(BaseRepository):
    model = RoomTypesORM
    schema = RoomType