"""
Bookings Repository
"""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsORM
from src.schemas.bookings import Booking, BookingAdd, BookingCreateORM

class BookingsRepository(BaseRepository):
    model = BookingsORM
    schema = Booking

    async def add(self, booking_data: BookingAdd):
        """Add a booking to the database"""

        from src.models.rooms import RoomsORM

        # Calculate check_in_datetime and check_out_datetime for specific hotel
        check_in_date = booking_data.check_in
        check_out_date = booking_data.check_out

        query = (
            select(RoomsORM)
            .where(RoomsORM.id == booking_data.room_id)
            .options(joinedload(RoomsORM.hotel))
        )
        room = await self.session.execute(query)
        room = room.scalar_one()

        check_in_datetime = datetime.combine(check_in_date, room.hotel.check_in)
        check_out_datetime = datetime.combine(check_out_date, room.hotel.check_out)

        # Calculate the total price of a booking
        total_price = (check_out_date - check_in_date).days * room.price

        return await super().add(BookingCreateORM(
            user_id=booking_data.user_id,
            room_id=booking_data.room_id,
            total_price=total_price, 
            check_in=check_in_datetime, 
            check_out=check_out_datetime
            )
        )
