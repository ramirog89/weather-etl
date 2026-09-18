from typing import Optional

from src.application.ports.geocoding import GeocodingPort
from src.domain import City
from src.domain.exceptions import ExtractionError
from src.infrastructure.http.client import HTTPClient, HTTPClientError


class OpenMeteoGeocodingClient(GeocodingPort):
    def __init__(self, http_client: HTTPClient, base_url: str):
        self.http_client = http_client
        self.base_url = base_url

    def get_city_coordinates(self, city_name: str) -> Optional[City]:
        params = {
          "name": city_name,
          "count": 1,
        }

        try:
            payload = self.http_client.get( f"{self.base_url}/search", params=params)

            if "results" in payload and len(payload["results"]) > 0:
                result = payload["results"][0]
                return City(
                    name=result["name"],
                    latitude=result["latitude"],
                    longitude=result["longitude"],
                )
        except HTTPClientError as err:
            raise ExtractionError(
                f"Network failure while resolving geocoding coordinates for '{city_name}': {err}"
            ) from err
        except KeyError as err:
            raise ExtractionError(
                f"Unexpected API payload structure from Geocoding API for '{city_name}': missing key {err}"
            ) from err

        return None