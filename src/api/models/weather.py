from datetime import datetime
from pydantic import BaseModel


class WeatherRequest(BaseModel):
    name: str
    latitude: float
    longitude: float


class WeatherData(BaseModel):
    name: str
    latitude: float
    longitude: float
    temperature: float
    wind_speed: float
    time: datetime
