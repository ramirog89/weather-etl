from src.domain import City
from src.infrastructure.http.api import HTTPClient
from src.infrastructure.openmeteo import OpenMeteoClient
from src.application.services import ExtractWeatherService, TransformWeatherService

def main():
    # infrastructure
    http_client = HTTPClient()
    open_meteo_client = OpenMeteoClient(http_client=http_client)

    # application
    extract_weather_service = ExtractWeatherService(provider=open_meteo_client)
    transform_service = TransformWeatherService()

    raw_cities = [
        {"City": "New York", "Latitude": 40.7128, "Longitude": -74.0060},
        {"City": "Tokyo", "Latitude": 35.6895, "Longitude": 139.6917},
        {"City": "London", "Latitude": 51.5074, "Longitude": -0.1278},
        {"City": "Paris", "Latitude": 48.8566, "Longitude": 2.3522},
        {"City": "Berlin", "Latitude": 52.5200, "Longitude": 13.4050},
        {"City": "Sydney", "Latitude": -33.8688, "Longitude": 151.2093},
        {"City": "Mumbai", "Latitude": 19.0760, "Longitude": 72.8777},
        {"City": "Cape Town", "Latitude": -33.9249, "Longitude": 18.4241},
        {"City": "Moscow", "Latitude": 55.7558, "Longitude": 37.6173},
        {"City": "Rio de Janeiro", "Latitude": -22.9068, "Longitude": -43.1729}
    ]

    cities = [
        City(
            name=item["City"],
            latitude=item["Latitude"],
            longitude=item["Longitude"],
        )
        for item in raw_cities
    ]

    print("1. Extracting weather data...")
    extracted_weather = extract_weather_service.execute(cities)

    print("2. Transforming weather data with Pandas...")
    weather_df = transform_service.execute(extracted_weather)

    print("\n--- Processed Weather DataFrame ---")
    print(weather_df.to_string())


if __name__ == "__main__":
    main()
