import uvicorn
from fastapi import FastAPI
from fastapi.params import Query, Body

app = FastAPI()


# Create dict hotels [{id: star, name: str}]
hotels = [
    {"id": 1, "name": "The Ritz-Carlton", "stars": 5},
    {"id": 2, "name": "The Westin", "stars": 4},
    {"id": 3, "name": "The Sheraton", "stars": 3},
    {"id": 4, "name": "The Hilton", "stars": 2},
    {"id": 5, "name": "The Holiday Inn", "stars": 1},
]


@app.get("/")
async def root():
    return {"message": "Hello World from Uvicorn !!!"}


@app.get("/hotels")
async def get_hotels(
        id: int | None = Query(default=None, description="ID of the hotel"),
        name: str | None = Query(default=None, description="Name of the hotel"),
) -> list:
    """ Get list of hotels """

    return_data = []
    for hotel in hotels:
        if name and name.lower() not in hotel["name"].lower():
            continue
        if id and id != hotel["id"]:
            continue
        return_data.append(hotel)
    return return_data


@app.post("/hotels")
async def create_hotel(
        name: str = Body(embed=True),
        stars: int = Body(embed=True, default=0),
) -> dict:
    """ Create new hotel """

    new_hotel = {"id": len(hotels) + 1, "name": name, "stars": stars}
    hotels.append(new_hotel)
    return {"status": 200, "message": "Hotel created", "hotel": new_hotel}


@app.delete("/hotels/{hotel_id}")
async def delete_hotel(hotel_id: int) -> dict:
    """ Delete hotel """

    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotels.remove(hotel)
            return {"status": 200, "message": "Hotel deleted"}
        else:
            return {"status": 404, "message": "Hotel not found"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)