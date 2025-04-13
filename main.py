import uvicorn
from fastapi import FastAPI
from fastapi.params import Query, Body
import logging

logger = logging.getLogger("uvicorn")

app = FastAPI()


# Create dict hotels [{id: star, name: str, city: str, stars: int}]
hotels = [
    {"id": 1, "name": "The Ritz-Carlton", "city": "New York", "stars": 5},
    {"id": 2, "name": "The Westin", "city": "San Francisco", "stars": 4},
    {"id": 3, "name": "The Sheraton", "city": "Los Angeles", "stars": 3},
    {"id": 4, "name": "The Hilton", "city": "Chicago", "stars": 5},
    {"id": 5, "name": "The Holiday Inn", "city": "Miami", "stars": 3},
]

@app.get("/")
async def root():
    return {"message": "Hello World from Uvicorn !!!"}


@app.get("/hotels")
async def get_hotels(
        id: int | None = Query(default=None, description="ID of the hotel"),
        name: str | None = Query(default=None, description="Name of the hotel"),
        city: str | None = Query(default=None, description="City of the hotel"),
) -> list:
    """ Get list of hotels """

    return_data = []
    for hotel in hotels:
        if name and name.lower() not in hotel["name"].lower():
            continue
        if id and id != hotel["id"]:
            continue
        if city and city.lower() not in hotel["city"].lower():
            continue
        return_data.append(hotel)
    return return_data


@app.post("/hotels")
async def create_hotel(
        name: str = Body(embed=True),
        stars: int = Body(embed=True, default=0),
        city: str = Body(embed=True),
) -> dict:
    """ Create new hotel """

    new_hotel = {"id": len(hotels) + 1, "name": name, "stars": stars, "city": city}
    hotels.append(new_hotel)
    return {"status": 200, "message": "Hotel created", "hotel": new_hotel}


@app.put("/hotels/{hotel_id}")
async def edit_hotel(
        hotel_id: int,
        name: str = Body(embed=True),
        stars: int = Body(embed=True),
        city: str = Body(embed=True),
) -> dict:
    """ Update hotel with full parameters list """

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["name"] = name
            hotel["stars"] = stars
            hotel["city"] = city
            return {"status": 200, "message": f"Hotel {hotel_id=} updated", "hotel": hotel}
        else:
            continue
    return {"status": 404, "message": f"Hotel {hotel_id=} not found"}


@app.patch("/hotels/{hotel_id}")
async def update_hotel(
        hotel_id: int,
        name: str | None = Body(embed=True, default=None),
        stars: int | None = Body(embed=True, default=None),
        city: str | None = Body(embed=True, default=None),
) -> dict:
    """ Partial Update hotel by ID and partial parameters list """

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if name:
                hotel["name"] = name
            if stars:
                hotel["stars"] = stars
            if city:
                hotel["city"] = city
            return {"status": 200, "message": f"Hotel {hotel_id=} updated", "hotel": hotel}
        else:
            continue
    return {"status": 404, "message": f"Hotel {hotel_id=} not found"}


@app.delete("/hotels/{hotel_id}")
async def delete_hotel(hotel_id: int) -> dict:
    """ Delete hotel by ID """

    for hotel in hotels:
        logger.info(hotel)
        if hotel["id"] == hotel_id:
            hotels.remove(hotel)
            return {"status": 200, "message": f"Hotel {hotel_id=} deleted"}
        else:
            continue
    return {"status": 404, "message": f"Hotel {hotel_id=} not found"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)