from pydantic import BaseModel

class Weather(BaseModel):
    city_name: str
    temperature_c: float = 0
    temperature_f: float = 0
    wind_speed_mph: float = 0
    wind_speed_ms: float = 0
    humidity: int = 0
