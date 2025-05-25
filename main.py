import uvicorn
import logging
from fastapi import FastAPI
from src.api.hotels import router as router_hotels
from src.api.auth import router as router_auth

logger = logging.getLogger("uvicorn")

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_hotels)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)