from pydantic import BaseModel


class PredictionRequest(BaseModel):
    hour: int
    is_weekday: bool
    is_raining: bool
    has_match: bool
    hours_to_match: int = 0


class PredictionResponse(BaseModel):
    station_id: int
    predicted_passengers: int
    confidence: str
    factors: dict
