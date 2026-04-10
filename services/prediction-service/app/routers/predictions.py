import numpy as np
from fastapi import APIRouter

from app.models import PredictionRequest, PredictionResponse
from app.predictor import load_or_train_model

router = APIRouter(prefix="/predictions", tags=["predictions"])

model = load_or_train_model()


@router.post("/{station_id}", response_model=PredictionResponse)
async def predict(station_id: int, request: PredictionRequest):
    features = np.array(
        [
            [
                request.hour,
                int(request.is_weekday),
                int(request.is_raining),
                int(request.has_match),
                request.hours_to_match,
            ]
        ]
    )

    predicted = int(model.predict(features)[0])

    factors = {
        "saat_etkisi": "yüksek"
        if 7 <= request.hour <= 9 or 17 <= request.hour <= 19
        else "normal",
        "yagmur_etkisi": "var" if request.is_raining else "yok",
        "mac_etkisi": "var" if request.has_match else "yok",
    }

    confidence = (
        "yüksek" if predicted > 2000 else "orta" if predicted > 1000 else "düşük"
    )

    return PredictionResponse(
        station_id=station_id,
        predicted_passengers=predicted,
        confidence=confidence,
        factors=factors,
    )
