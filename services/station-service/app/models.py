from pydantic import BaseModel, Field


class Station(BaseModel):
    id: int
    name: str
    line: str
    capacity: int
    current_load: float = Field(ge=0, le=100)
    latitude: float
    longitude: float
    is_active: bool = True


class StationCreate(BaseModel):
    name: str
    line: str
    capacity: int
    latitude: float
    longitude: float
