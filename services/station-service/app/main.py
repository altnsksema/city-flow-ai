from app.database import Base, engine
from app.routers import stations
from fastapi import FastAPI


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(
    title="CityFlow Station Service",
    version="0.1.0",
)


@app.on_event("startup")
async def startup():
    await create_tables()


app.include_router(stations.router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "station-service"}
