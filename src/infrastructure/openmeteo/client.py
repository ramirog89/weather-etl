from src.domain import City, Weather
from src.infrastructure.http.api import HTTPClient


class OpenMeteoClient:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client

    def fetch_weather(self, city: City) -> Weather:
        params = {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        }
        
        payload = self.http_client.get(self.BASE_URL, params=params)
        data = payload["current"]

        return Weather(
            city_name=city.name,
            temperature_f=data["temperature_2m"],
            wind_speed_mph=data["wind_speed_10m"],
            humidity=data["relative_humidity_2m"],
        )
