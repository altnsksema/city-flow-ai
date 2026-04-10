from fastapi import FastAPI

from app.routers import predictions

app = FastAPI(
    title="CityFlow Prediction Service",
    version="0.1.0",
)

app.include_router(predictions.router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "prediction-service"}
