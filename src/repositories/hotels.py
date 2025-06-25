from datetime import date
from sqlalchemy import and_, distinct, or_, select

from src.models.bookings import BookingsORM
from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM

from src.schemas.hotels import Hotel
from src.repositories.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsORM
    schema = Hotel
    
    async def get_all(
            self, 
            title: str | None = None,
            location: str | None = None,
            limit: int = 3,
            offset: int = 0
        ):
        query = select(self.model)
        # Filters
        query = query.filter(self.model.title.icontains(title)) if title else query
        query = query.filter(self.model.location.icontains(location)) if location else query
        # LIMIT and OFFSET
        query = query.offset(offset).limit(limit)
        query_result = await self.session.execute(query)
        return [self.schema.model_validate(res, from_attributes=True) for res in query_result.scalars().all()]

    
    async def get_by_room_id(self, room_id: int):
        """Get a hotel by room_id"""
        from src.models.rooms import RoomsORM
        query = select(self.model).join(RoomsORM).where(RoomsORM.id == room_id)
        query_result = await self.session.execute(query)
        return query_result.scalar_one()


    async def get_available_hotels(
        self, 
        check_in: date, 
        check_out: date,
        limit: int = 3,
        offset: int = 0,
        title: str | None = None,
        location: str | None = None
    ):
        query = select(self.model)
        # Filters
        query = query.filter(self.model.title.icontains(title)) if title else query
        query = query.filter(self.model.location.icontains(location)) if location else query
        # LIMIT and OFFSET
        query = query.offset(offset).limit(limit)

        # Define the CTE (Common Table Expression) for rooms_booked
        rooms_hotels_booked = (
            select(
                BookingsORM.id.label("booking_id"), 
                RoomsORM.hotel_id.label("hotel_id"), 
                RoomsORM.id.label("room_id")
            )
            .join(RoomsORM, BookingsORM.room_id == RoomsORM.id)
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
            .cte('rooms_hotels_booked')
        )

        # Define the CTE (Common Table Expression) for available hotels IDs
        available_hotels_id = (
            select(distinct(RoomsORM.hotel_id).label("hotel_id"))
            .where(
                RoomsORM.id.not_in(
                    select(rooms_hotels_booked.c.room_id)
                )
            )
        )

        query = query.where(self.model.id.in_(available_hotels_id))
        query_result = await self.session.execute(query)
        return [self.schema.model_validate(res, from_attributes=True) for res in query_result.scalars().all()]