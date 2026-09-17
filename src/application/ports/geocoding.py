from abc import ABC, abstractmethod
from typing import Optional
from src.domain import City


class GeocodingPort(ABC):
    @abstractmethod
    def get_city_coordinates(self, city_name: str) -> Optional[City]:
        """Resolves a city name to a City entity containing latitude and longitude."""
        pass
