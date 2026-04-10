from app.database import Base
from pydantic import BaseModel, Field
from sqlalchemy import Boolean, Column, Float, Integer, String


class StationTable(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    line = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    current_load = Column(Float, default=0.0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)


class Station(BaseModel):
    id: int
    name: str
    line: str
    capacity: int
    current_load: float = Field(ge=0, le=100)
    latitude: float
    longitude: float
    is_active: bool = True

    class Config:
        from_attributes = True


class StationCreate(BaseModel):
    name: str
    line: str
    capacity: int
    latitude: float
    longitude: float
