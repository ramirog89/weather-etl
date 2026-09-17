from abc import ABC, abstractmethod
from src.domain import City, Weather


class WeatherProviderPort(ABC):
    @abstractmethod
    def fetch_weather(self, city: City) -> Weather:
        pass
