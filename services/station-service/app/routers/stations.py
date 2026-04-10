from app.models import Station
from fastapi import APIRouter

router = APIRouter(prefix="/stations", tags=["stations"])

FAKE_DB: list[Station] = [
    Station(
        id=1,
        name="Taksim",
        line="M2",
        capacity=2000,
        current_load=87.5,
        latitude=41.0369,
        longitude=28.9850,
    ),
    Station(
        id=2,
        name="Levent",
        line="M2",
        capacity=1800,
        current_load=62.0,
        latitude=41.0829,
        longitude=29.0089,
    ),
]


@router.get("/", response_model=list[Station])
async def get_stations():
    return FAKE_DB


@router.get("/{station_id}", response_model=Station)
async def get_station(station_id: int):
    for station in FAKE_DB:
        if station.id == station_id:
            return station
    from fastapi import HTTPException

    raise HTTPException(status_code=404, detail="İstasyon bulunamadı")
