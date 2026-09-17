from src.application.ports.extractor import ExtractorPort
from src.domain import City, Weather
from src.infrastructure.http.api import HTTPClient


class OpenMeteoClient(ExtractorPort):

    def __init__(self, http_client: HTTPClient, base_url: str):
        self.http_client = http_client
        self.base_url = base_url

    def extract(self, city: City) -> Weather:
        params = {
            "latitude": city.latitude,
            "longitude": city.longitude,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "wind_speed_unit": "mph",
        }
        
        payload = self.http_client.get(self.base_url, params=params)
        data = payload["current"]

        return Weather(
            city_name=city.name,
            temperature_c=data["temperature_2m"],
            wind_speed_mph=data["wind_speed_10m"],
            humidity=data["relative_humidity_2m"],
        )
