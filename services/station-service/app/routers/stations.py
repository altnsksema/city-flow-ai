from app.database import get_db
from app.models import Station, StationCreate, StationTable
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/stations", tags=["stations"])


@router.get("/", response_model=list[Station])
async def get_stations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StationTable))
    return result.scalars().all()


@router.get("/{station_id}", response_model=Station)
async def get_station(station_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(StationTable).where(StationTable.id == station_id))
    station = result.scalar_one_or_none()
    if not station:
        raise HTTPException(status_code=404, detail="İstasyon bulunamadı")
    return station


@router.post("/", response_model=Station)
async def create_station(station: StationCreate, db: AsyncSession = Depends(get_db)):
    db_station = StationTable(**station.model_dump())
    db.add(db_station)
    await db.commit()
    await db.refresh(db_station)
    return db_station
