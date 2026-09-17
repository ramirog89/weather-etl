from src.domain import City

from src.application.services import ETLPipeline
from src.application.usecases.weather import WeatherExtractor, WeatherTransformer

from src.infrastructure.config import settings
from src.infrastructure.http import HTTPClient, OpenMeteoClient
from src.infrastructure.storage.csv import CSVLoader
from src.infrastructure.visualization.matplotlib import MatplotlibWeatherVisualizer

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
    open_meteo_client = OpenMeteoClient(
        http_client=http_client,
        base_url=settings.open_meteo_base_url)
    csv_loader = CSVLoader()
    visualizer = MatplotlibWeatherVisualizer()

    # application
    weather_extractor = WeatherExtractor(provider=open_meteo_client, cities=cities)
    weather_transformer = WeatherTransformer()

    # Weather ETL Pipeline
    pipeline = ETLPipeline(
        extractor=weather_extractor,
        transformer=weather_transformer,
        loader=csv_loader,
    )

    print("--- Executing Weather ETL Use Case ---")
    output = pipeline.run(destination=settings.csv_output_path)
    print("--- Pipeline Execution Complete ---\n")

    print("--- Generating Plot Temperature Bar Chart ---")
    visualizer.plot_temperature_bar_chart(output, output_path=settings.chart_output_path)
    print("--- Done ---")

if __name__ == "__main__":
    main()
