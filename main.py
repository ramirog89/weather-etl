from src.domain import City
from src.infrastructure.http.api import HTTPClient
from src.infrastructure.openmeteo import OpenMeteoClient
from src.infrastructure.storage.csv import CSVWeatherLoader
from src.application.services import ExtractWeatherService, TransformWeatherService, LoadWeatherService
from src.application.usecases.weather import WeatherUseCase

def main():
    # input data
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

    # infrastructure
    http_client = HTTPClient()
    open_meteo_client = OpenMeteoClient(http_client=http_client)
    csv_weather_loader = CSVWeatherLoader()

    # application
    extract_weather_service = ExtractWeatherService(provider=open_meteo_client)
    transform_weather_service = TransformWeatherService()
    load_weather_service = LoadWeatherService(loader=csv_weather_loader)

    # use cases
    weather_usecase = WeatherUseCase(
        cities=cities,
        extract_service=extract_weather_service,
        transform_service=transform_weather_service,
        load_service=load_weather_service,
        output_path="weather_data.csv",
    )

    print("--- Executing Weather ETL Use Case ---")
    output = weather_usecase.run()
    print("--- Pipeline Execution Complete ---")
    print(output.to_string())

if __name__ == "__main__":
    main()
