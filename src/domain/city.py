from pydantic import BaseModel

class City(BaseModel):
    name: str
    latitude: float
    longitude: float
