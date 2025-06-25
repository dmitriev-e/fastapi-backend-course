from fastapi import APIRouter, HTTPException, Path, Query, Body, status
import logging
from typing import List, Any
from datetime import datetime

from fastapi.openapi.models import Example

from src.api.dependencies import DBDep
from src.schemas.facilities import Facilities, FacilitiesCreateRequest

logger = logging.getLogger("uvicorn")

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("/", response_model=List[Facilities], summary="Get all facilities")
async def get_facilities(db: DBDep):
    """Get all available facilities"""
    facilities = await db.facilities.get_all()
    return facilities


@router.post("/", response_model=Facilities, status_code=status.HTTP_201_CREATED, summary="Create new facility")
async def create_facility(
    db: DBDep,
    facility_data: FacilitiesCreateRequest = Body(
        openapi_examples={
            "wifi": {
                "summary": "Wi-Fi facility",
                "value": {
                    "title": "Free Wi-Fi",
                    "description": "High-speed wireless internet access"
                }
            },
            "parking": {
                "summary": "Parking facility", 
                "value": {
                    "title": "Free Parking",
                    "description": "Complimentary parking for guests"
                }
            }
        }
    )
):
    """Create a new facility"""
    facility_added = await db.facilities.add(facility_data)
    await db.commit()
    return facility_added