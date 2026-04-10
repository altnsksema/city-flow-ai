from app.routers import stations
from fastapi import FastAPI

app = FastAPI(
    title="CityFlow Station Service",
    version="0.1.0",
)

app.include_router(stations.router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "station-service"}
