import asyncio
from datetime import time, datetime
from sqlalchemy import delete

from src.models.hotels import HotelsORM
from src.models.rooms import RoomsORM, RoomTypesORM
from src.models.bookings import BookingsORM
from src.models.users import UsersORM
from src.models.facilities import FacilitiesORM

from src.db import Base, async_session_maker


# Test data for the app

# Facilities
"""
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str | None]] = mapped_column(String(255), nullable=True)
"""
facilities = [
    FacilitiesORM(id=1, title='Free Wi-Fi', description='High-speed wireless internet access throughout the property'),
    FacilitiesORM(id=2, title='Air Conditioning', description='Climate control system for optimal room temperature'),
    FacilitiesORM(id=3, title='Mini Bar', description='In-room refrigerated bar with beverages and snacks'),
    FacilitiesORM(id=4, title='Room Service', description='24/7 in-room dining service available'),
    FacilitiesORM(id=5, title='Flat Screen TV', description='High-definition television with cable channels'),
]

# Hotels
"""
    title: Mapped[str] = mapped_column(String(100))
    stars: Mapped[int]
    location: Mapped[str] = mapped_column(String(200))
    check_in: Mapped[str] = mapped_column(String(10))
    check_out: Mapped[str] = mapped_column(String(10))
"""
hotels = [
    HotelsORM(id=1, title='Ocean View Hotel', stars=5, location='Miami Beach', check_in=time(14, 0), check_out=time(12, 0)),
    HotelsORM(id=2, title='Mountain Retreat', stars=4, location='Aspen', check_in=time(14, 0), check_out=time(12, 0)),
    # HotelsORM(id=3, title='City Center Inn', stars=3, location='New York', check_in=time(14, 0), check_out=time(12, 0)),
    # HotelsORM(id=4, title='Desert Oasis', stars=4, location='Palm Springs', check_in=time(14, 0), check_out=time(11, 0)),
    # HotelsORM(id=5, title='Lakeside Lodge', stars=3, location='Lake Tahoe', check_in=time(14, 0), check_out=time(11, 0)),
    # HotelsORM(id=6, title='Historic Castle', stars=5, location='Scotland', check_in=time(15, 0), check_out=time(12, 0)),
    # HotelsORM(id=7, title='Tropical Paradise', stars=4, location='Hawaii', check_in=time(15, 0), check_out=time(12, 0)),
    # HotelsORM(id=8, title='Business Hub Hotel', stars=3, location='San Francisco', check_in=time(15, 0), check_out=time(11, 0)),
    # HotelsORM(id=9, title='Countryside Escape', stars=4, location='Napa Valley', check_in=time(15, 0), check_out=time(11, 0)),
    # HotelsORM(id=10, title='Luxury Spa Resort', stars=5, location='Bali', check_in=time(15, 0), check_out=time(11, 0))
]

# Room types
room_types = [
    RoomTypesORM(id=1, title='Single Room', description='A room assigned to one person.'),
    RoomTypesORM(id=2, title='Double Room', description='A room assigned to two people.'),
    RoomTypesORM(id=3, title='Suite', description='A luxurious room with additional space and amenities.'),
    RoomTypesORM(id=4, title='Deluxe Room', description='A room with upgraded features and services.'),
    RoomTypesORM(id=5, title='Family Room', description='A room designed to accommodate families.')
]

# Rooms
"""
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    room_type_id: Mapped[int] = mapped_column(ForeignKey("room_types.id"))
    number: Mapped[str] = mapped_column(String(10))
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str | None]]
    price: Mapped[int]
"""
rooms = [
    RoomsORM(id=1, hotel_id=1, room_type_id=1, number='101', title='Ocean View Suite', description='A luxurious suite with ocean views.', price=300),
    RoomsORM(id=2, hotel_id=1, room_type_id=2, number='102', title='Ocean View Double', description='A double room with ocean views.', price=200),
    RoomsORM(id=3, hotel_id=1, room_type_id=3, number='103', title='Ocean View Single', description='A single room with ocean views.', price=150),
    RoomsORM(id=4, hotel_id=1, room_type_id=4, number='104', title='Ocean View Deluxe', description='A deluxe room with ocean views.', price=250),
    RoomsORM(id=5, hotel_id=1, room_type_id=5, number='105', title='Ocean View Family', description='A family room with ocean views.', price=350),
    RoomsORM(id=6, hotel_id=1, room_type_id=1, number='106', title='Ocean View King', description='A king room with ocean views.', price=280),

    RoomsORM(id=7, hotel_id=2, room_type_id=1, number='201', title='Mountain Retreat Suite', description='A luxurious suite in the mountains.', price=320),
    RoomsORM(id=8, hotel_id=2, room_type_id=2, number='202', title='Mountain Retreat Double', description='A double room in the mountains.', price=220),
    RoomsORM(id=9, hotel_id=2, room_type_id=3, number='203', title='Mountain Retreat Single', description='A single room in the mountains.', price=170),
    RoomsORM(id=10, hotel_id=2, room_type_id=4, number='204', title='Mountain Retreat Deluxe', description='A deluxe room in the mountains.', price=270),
    RoomsORM(id=11, hotel_id=2, room_type_id=5, number='205', title='Mountain Retreat Family', description='A family room in the mountains.', price=370),
    RoomsORM(id=12, hotel_id=2, room_type_id=1, number='206', title='Mountain Retreat King', description='A king room in the mountains.', price=300),

    # RoomsORM(id=13, hotel_id=3, room_type_id=1, number='301', title='City Center Suite', description='A luxurious suite in the city center.', price=310),
    # RoomsORM(id=14, hotel_id=3, room_type_id=2, number='302', title='City Center Double', description='A double room in the city center.', price=210),
    # RoomsORM(id=15, hotel_id=3, room_type_id=3, number='303', title='City Center Single', description='A single room in the city center.', price=160),
    # RoomsORM(id=16, hotel_id=3, room_type_id=4, number='304', title='City Center Deluxe', description='A deluxe room in the city center.', price=260),
    # RoomsORM(id=17, hotel_id=3, room_type_id=5, number='305', title='City Center Family', description='A family room in the city center.', price=360),
    # RoomsORM(id=18, hotel_id=3, room_type_id=1, number='306', title='City Center King', description='A king room in the city center.', price=290),

    # RoomsORM(id=19, hotel_id=4, room_type_id=1, number='401', title='Desert Oasis Suite', description='A luxurious suite in the desert.', price=330),
    # RoomsORM(id=20, hotel_id=4, room_type_id=2, number='402', title='Desert Oasis Double', description='A double room in the desert.', price=230),
    # RoomsORM(id=21, hotel_id=4, room_type_id=3, number='403', title='Desert Oasis Single', description='A single room in the desert.', price=180),
    # RoomsORM(id=22, hotel_id=4, room_type_id=4, number='404', title='Desert Oasis Deluxe', description='A deluxe room in the desert.', price=280),
    # RoomsORM(id=23, hotel_id=4, room_type_id=5, number='405', title='Desert Oasis Family', description='A family room in the desert.', price=380),
    # RoomsORM(id=24, hotel_id=4, room_type_id=1, number='406', title='Desert Oasis King', description='A king room in the desert.', price=310),

    # RoomsORM(id=25, hotel_id=5, room_type_id=1, number='501', title='Lakeside Lodge Suite', description='A luxurious suite by the lake.', price=340),
    # RoomsORM(id=26, hotel_id=5, room_type_id=2, number='502', title='Lakeside Lodge Double', description='A double room by the lake.', price=240),
    # RoomsORM(id=27, hotel_id=5, room_type_id=3, number='503', title='Lakeside Lodge Single', description='A single room by the lake.', price=190),
    # RoomsORM(id=28, hotel_id=5, room_type_id=4, number='504', title='Lakeside Lodge Deluxe', description='A deluxe room by the lake.', price=290),
    # RoomsORM(id=29, hotel_id=5, room_type_id=5, number='505', title='Lakeside Lodge Family', description='A family room by the lake.', price=390),
    # RoomsORM(id=30, hotel_id=5, room_type_id=1, number='506', title='Lakeside Lodge King', description='A king room by the lake.', price=320),

    # RoomsORM(id=31, hotel_id=6, room_type_id=1, number='601', title='Historic Castle Suite', description='A luxurious suite in a historic castle.', price=350),
    # RoomsORM(id=32, hotel_id=6, room_type_id=2, number='602', title='Historic Castle Double', description='A double room in a historic castle.', price=250),
    # RoomsORM(id=33, hotel_id=6, room_type_id=3, number='603', title='Historic Castle Single', description='A single room in a historic castle.', price=200),
    # RoomsORM(id=34, hotel_id=6, room_type_id=4, number='604', title='Historic Castle Deluxe', description='A deluxe room in a historic castle.', price=300),
    # RoomsORM(id=35, hotel_id=6, room_type_id=5, number='605', title='Historic Castle Family', description='A family room in a historic castle.', price=400),
    # RoomsORM(id=36, hotel_id=6, room_type_id=1, number='606', title='Historic Castle King', description='A king room in a historic castle.', price=330),

    # RoomsORM(id=37, hotel_id=7, room_type_id=1, number='701', title='Tropical Paradise Suite', description='A luxurious suite in a tropical paradise.', price=360),
    # RoomsORM(id=38, hotel_id=7, room_type_id=2, number='702', title='Tropical Paradise Double', description='A double room in a tropical paradise.', price=260),
    # RoomsORM(id=39, hotel_id=7, room_type_id=3, number='703', title='Tropical Paradise Single', description='A single room in a tropical paradise.', price=210),
    # RoomsORM(id=40, hotel_id=7, room_type_id=4, number='704', title='Tropical Paradise Deluxe', description='A deluxe room in a tropical paradise.', price=310),
    # RoomsORM(id=41, hotel_id=7, room_type_id=5, number='705', title='Tropical Paradise Family', description='A family room in a tropical paradise.', price=410),
    # RoomsORM(id=42, hotel_id=7, room_type_id=1, number='706', title='Tropical Paradise King', description='A king room in a tropical paradise.', price=340),

    # RoomsORM(id=43, hotel_id=8, room_type_id=1, number='801', title='Business Hub Suite', description='A luxurious suite in a business hub.', price=370),
    # RoomsORM(id=44, hotel_id=8, room_type_id=2, number='802', title='Business Hub Double', description='A double room in a business hub.', price=270),
    # RoomsORM(id=45, hotel_id=8, room_type_id=3, number='803', title='Business Hub Single', description='A single room in a business hub.', price=220),
    # RoomsORM(id=46, hotel_id=8, room_type_id=4, number='804', title='Business Hub Deluxe', description='A deluxe room in a business hub.', price=320),
    # RoomsORM(id=47, hotel_id=8, room_type_id=5, number='805', title='Business Hub Family', description='A family room in a business hub.', price=420),
    # RoomsORM(id=48, hotel_id=8, room_type_id=1, number='806', title='Business Hub King', description='A king room in a business hub.', price=350),

    # RoomsORM(id=49, hotel_id=9, room_type_id=1, number='901', title='Countryside Escape Suite', description='A luxurious suite in the countryside.', price=380),
    # RoomsORM(id=50, hotel_id=9, room_type_id=2, number='902', title='Countryside Escape Double', description='A double room in the countryside.', price=280),
    # RoomsORM(id=51, hotel_id=9, room_type_id=3, number='903', title='Countryside Escape Single', description='A single room in the countryside.', price=230),
    # RoomsORM(id=52, hotel_id=9, room_type_id=4, number='904', title='Countryside Escape Deluxe', description='A deluxe room in the countryside.', price=330),
    # RoomsORM(id=53, hotel_id=9, room_type_id=5, number='905', title='Countryside Escape Family', description='A family room in the countryside.', price=430),
    # RoomsORM(id=54, hotel_id=9, room_type_id=1, number='906', title='Countryside Escape King', description='A king room in the countryside.', price=360),

    # RoomsORM(id=55, hotel_id=10, room_type_id=1, number='1001', title='Luxury Spa Resort Suite', description='A luxurious suite in a spa resort.', price=390),
    # RoomsORM(id=56, hotel_id=10, room_type_id=2, number='1002', title='Luxury Spa Resort Double', description='A double room in a spa resort.', price=290),
    # RoomsORM(id=57, hotel_id=10, room_type_id=3, number='1003', title='Luxury Spa Resort Single', description='A single room in a spa resort.', price=240),
    # RoomsORM(id=58, hotel_id=10, room_type_id=4, number='1004', title='Luxury Spa Resort Deluxe', description='A deluxe room in a spa resort.', price=340),
    # RoomsORM(id=59, hotel_id=10, room_type_id=5, number='1005', title='Luxury Spa Resort Family', description='A family room in a spa resort.', price=440),
    # RoomsORM(id=60, hotel_id=10, room_type_id=1, number='1006', title='Luxury Spa Resort King', description='A king room in a spa resort.', price=370),
]

# Bookings
"""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    room_id: Mapped[int] = mapped_column(Integer, ForeignKey("rooms.id"), nullable=False)
    check_in: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    check_out: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    total_price: Mapped[float] = mapped_column(Float, nullable=False)
"""
bookings = [
    BookingsORM(id=1, user_id=7, room_id=1, check_in=datetime(2025, 7, 1, 14, 0), check_out=datetime(2025, 7, 3, 12, 0), total_price=600),
    BookingsORM(id=2, user_id=8, room_id=1, check_in=datetime(2025, 7, 4, 14, 0), check_out=datetime(2025, 7, 8, 12, 0), total_price=500),
    BookingsORM(id=3, user_id=7, room_id=7, check_in=datetime(2025, 7, 5, 14, 0), check_out=datetime(2025, 7, 12, 12, 0), total_price=300),
    BookingsORM(id=4, user_id=7, room_id=10, check_in=datetime(2025, 7, 10, 14, 0), check_out=datetime(2025, 7, 15, 12, 0), total_price=400),
    BookingsORM(id=5, user_id=8, room_id=5, check_in=datetime(2025, 7, 9, 14, 0), check_out=datetime(2025, 7, 10, 12, 0), total_price=500),
    BookingsORM(id=6, user_id=8, room_id=12, check_in=datetime(2025, 7, 12, 14, 0), check_out=datetime(2025, 7, 15, 12, 0), total_price=600),
    BookingsORM(id=7, user_id=8, room_id=6, check_in=datetime(2025, 7, 15, 14, 0), check_out=datetime(2025, 7, 20, 12, 0), total_price=700),
    BookingsORM(id=8, user_id=7, room_id=8, check_in=datetime(2025, 7, 1, 14, 0), check_out=datetime(2025, 7, 15, 12, 0), total_price=500),
    BookingsORM(id=9, user_id=7, room_id=9, check_in=datetime(2025, 7, 10, 14, 0), check_out=datetime(2025, 7, 20, 12, 0), total_price=900),
    BookingsORM(id=10, user_id=8, room_id=11, check_in=datetime(2025, 7, 5, 14, 0), check_out=datetime(2025, 7, 25, 12, 0), total_price=300),
    BookingsORM(id=11, user_id=8, room_id=4, check_in=datetime(2025, 7, 2, 14, 0), check_out=datetime(2025, 7, 20, 12, 0), total_price=400),

]

async def add_data_to_db(data: list, model: Base):
    async with async_session_maker() as session:
        print(f"Adding {model.__tablename__}...")
        for item in data:
            session.add(item)
        await session.commit()

async def delete_db_data(model: Base):
    # Delete all items
    async with async_session_maker() as session:
        print(f"Deleting {model.__tablename__}...")
        await session.execute(delete(model))
        await session.commit()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # Ask where to replace the data
    print("Where to replace the data?")
    print("1. Room types")
    print("2. Rooms")
    print("3. Hotels")
    print("4. Bookings")
    print("5. Facilities")
    print("6. All")
    choice = input("Enter the number of the option: ")
    if choice == "1":
        print("Replacing room types...")
        loop.run_until_complete(delete_db_data(RoomsORM))
        loop.run_until_complete(delete_db_data(RoomTypesORM))
        loop.run_until_complete(add_data_to_db(room_types, RoomTypesORM))
        loop.run_until_complete(add_data_to_db(rooms, RoomsORM))
    elif choice == "2":
        print("Replacing rooms...")
        loop.run_until_complete(delete_db_data(RoomsORM))
        loop.run_until_complete(add_data_to_db(rooms, RoomsORM))
    elif choice == "3":
        print("Replacing hotels...")
        loop.run_until_complete(delete_db_data(RoomsORM))
        loop.run_until_complete(delete_db_data(HotelsORM))
        loop.run_until_complete(add_data_to_db(hotels, HotelsORM))
        loop.run_until_complete(add_data_to_db(rooms, RoomsORM))
    elif choice == "4":
        print("Replacing bookings...")
        loop.run_until_complete(delete_db_data(BookingsORM))
        loop.run_until_complete(add_data_to_db(bookings, BookingsORM))
    elif choice == "5":
        print("Replacing facilities...")
        loop.run_until_complete(delete_db_data(FacilitiesORM))
        loop.run_until_complete(add_data_to_db(facilities, FacilitiesORM))
    elif choice == "6":
        print("Replacing all...")
        loop.run_until_complete(delete_db_data(BookingsORM))
        loop.run_until_complete(delete_db_data(RoomsORM))
        loop.run_until_complete(delete_db_data(RoomTypesORM))
        loop.run_until_complete(delete_db_data(HotelsORM))
        loop.run_until_complete(delete_db_data(FacilitiesORM))
        loop.run_until_complete(add_data_to_db(facilities, FacilitiesORM))
        loop.run_until_complete(add_data_to_db(hotels, HotelsORM))
        loop.run_until_complete(add_data_to_db(room_types, RoomTypesORM))
        loop.run_until_complete(add_data_to_db(rooms, RoomsORM))
        loop.run_until_complete(add_data_to_db(bookings, BookingsORM))
        print("Done!")


"""
Select all rooms that are not booked between 2025-07-01 and 2025-07-20

with rooms_booked as (
	SELECT *
	FROM bookings b
	WHERE b.check_in between date('2025-07-01') and date('2025-07-20')
	or b.check_out between date('2025-07-01') and date('2025-07-20')
)
select *
from rooms r
where r.id not in (select room_id from rooms_booked);
"""
