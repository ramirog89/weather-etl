from typing import List
from src.application.ports.weather_provider import WeatherProviderPort
from src.domain import City, Weather


class ExtractWeatherService:
    def __init__(self, provider: WeatherProviderPort):
        self.provider = provider

    def execute(self, cities: List[City]) -> List[Weather]:
        weather_records: List[Weather] = []
        for city in cities:
            try:
                weather = self.provider.fetch_weather(city)
                weather_records.append(weather)
            except Exception as err:
                print(f"Error extracting weather for {city.name}: {err}")
        
        return weather_records
