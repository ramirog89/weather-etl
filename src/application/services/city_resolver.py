from typing import List
from src.application.ports.geocoding import GeocodingPort
from src.domain import City


class CityResolverService:
    def __init__(self, geocoding_adapter: GeocodingPort):
        self.geocoding_adapter = geocoding_adapter

    def resolve_cities(self, city_names: List[str]) -> List[City]:
        """Resolves a list of city names into domain City entities."""
        resolved_cities: List[City] = []

        print("--- Resolving City Coordinates ---")
        for name in city_names:
            city = self.geocoding_adapter.get_city_coordinates(name)
            if city:
                resolved_cities.append(city)
                print(f"Resolved: {city.name} ({city.latitude}, {city.longitude})")
            else:
                print(f"Warning: Could not resolve coordinates for '{name}'. Skipping.")

        return resolved_cities
