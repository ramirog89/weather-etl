from pydantic import BaseModel

class Weather(BaseModel):
    temperature: float
    wind_speed: float
    humidity: int
