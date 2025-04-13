from fastapi import APIRouter, Query, Body
import logging

from schemas.hotels import Hotel, HotelPartialData, HotelCreateData

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/hotels", tags=["Hotels"])

hotels = [
    Hotel(id=1, name="The Ritz-Carlton", city="New York", stars=5),
    Hotel(id=2, name="The Westin", city="San Francisco", stars=4),
    Hotel(id=3, name="The Sheraton", city="Los Angeles", stars=3),
    Hotel(id=4, name="The Hilton", city="Chicago", stars=5),
    Hotel(id=5, name="The Holiday Inn", city="Miami", stars=3),
    Hotel(id=6, name="The Hyatt Regency", city="Las Vegas", stars=4),
    Hotel(id=7, name="The Park Hyatt", city="Tokyo", stars=5),
    Hotel(id=8, name="The Grand Hyatt", city="Seoul", stars=4),
    Hotel(id=9, name="The InterContinental", city="London", stars=5),
    Hotel(id=10, name="The Sofitel", city="Paris", stars=4),
    Hotel(id=11, name="The Marriott", city="Berlin", stars=4),
    Hotel(id=12, name="The Renaissance", city="Rome", stars=4),
    Hotel(id=13, name="The Courtyard by Marriott", city="Amsterdam", stars=3),
    Hotel(id=14, name="The W Hotel", city="Barcelona", stars=5),
    Hotel(id=15, name="The Sheraton", city="Stockholm", stars=4),
]

@router.get("/")
async def get_hotels(
        hotel_id: int | None = Query(default=None, description="ID of the hotel"),
        name: str | None = Query(default=None, description="Name of the hotel"),
        city: str | None = Query(default=None, description="City of the hotel"),
) -> list[Hotel]:
    """ Get list of hotels """

    return_data = []
    for hotel in hotels:
        if name and name.lower() not in hotel.name.lower():
            continue
        if hotel_id and hotel_id != hotel.id:
            continue
        if city and city.lower() not in hotel.city.lower():
            continue
        return_data.append(hotel)
    return return_data


@router.post("/")
async def create_hotel(hotel_data: HotelCreateData) -> dict:
    """ Create new hotel """

    new_hotel = Hotel(
        id = max([hotel.id for hotel in hotels]) + 1,
        name = hotel_data.name,
        stars = hotel_data.stars,
        city = hotel_data.city,
    )
    hotels.append(new_hotel)
    return {"status": 200, "message": "Hotel created", "data": new_hotel}


@router.put("/{hotel_id}")
async def edit_hotel(
        hotel_id: int,
        hotel_data: HotelCreateData
) -> dict:
    """ Update hotel with full parameters list """

    for hotel in hotels:
        if hotel.id == hotel_id:
            hotel.name = hotel_data.name
            hotel.stars = hotel_data.stars
            hotel.city = hotel_data.city
            return {"status": 200, "message": f"Hotel {hotel_id=} updated", "data": hotel}
        else:
            continue
    return {"status": 404, "message": f"Hotel {hotel_id=} not found"}


@router.patch("/{hotel_id}")
async def update_hotel(
        hotel_id: int,
        hotel_data: HotelPartialData
) -> dict:
    """ Partial Update hotel by ID and partial parameters list """

    for hotel in hotels:
        if hotel.id == hotel_id:
            if hotel_data.name:
                hotel.name = hotel_data.name
            if hotel_data.stars:
                hotel.stars = hotel_data.stars
            if hotel_data.city:
                hotel.city = hotel_data.city
            return {"status": 200, "message": f"Hotel {hotel_id=} updated", "data": hotel}
        else:
            continue
    return {"status": 404, "message": f"Hotel {hotel_id=} not found"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int) -> dict:
    """ Delete hotel by ID """

    for hotel in hotels:
        logger.info(hotel)
        if hotel.id == hotel_id:
            hotels.remove(hotel)
            return {"status": 200, "message": f"Hotel {hotel_id=} deleted"}
        else:
            continue
    return {"status": 404, "message": f"Hotel {hotel_id=} not found"}

