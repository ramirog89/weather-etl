import argparse
from typing import List

from src.application.services import ETLPipeline, CityResolverService
from src.application.usecases.weather import WeatherExtractor, WeatherTransformer
from src.infrastructure.config import settings
from src.infrastructure.http import HTTPClient, OpenMeteoClient, OpenMeteoGeocodingClient
from src.infrastructure.storage.csv import CSVLoader
from src.infrastructure.visualization.matplotlib import MatplotlibWeatherVisualizer

DEFAULT_CITIES = [
    "New York",
    "Tokyo",
    "London",
    "Paris",
    "Berlin",
    "Sydney",
    "Mumbai",
    "Cape Town",
    "Moscow",
    "Rio de Janeiro",
]

def main(city_names: List[str] = None):
    # input data
    target_names = city_names or DEFAULT_CITIES

    # infrastructure
    http_client = HTTPClient()
    open_meteo_client = OpenMeteoClient(
        http_client=http_client,
        base_url=settings.open_meteo_base_url)
    geocoding_adapter = OpenMeteoGeocodingClient(
        http_client=http_client,
        base_url=settings.open_meteo_geocoding_base_url)
    csv_loader = CSVLoader()
    visualizer = MatplotlibWeatherVisualizer()

    # Resolve Cities via Application Service
    city_resolver = CityResolverService(geocoding_adapter=geocoding_adapter)
    cities = city_resolver.resolve_cities(target_names)

    if not cities:
        print("Error: No valid cities resolved. Aborting pipeline.")
        return

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
    parser = argparse.ArgumentParser(
        description="Run Weather ETL Pipeline for specified cities."
    )
    # Allows passing multiple space-separated city names (or quote multi-word names)
    parser.add_argument(
        "--cities",
        nargs="+",
        type=str,
        help="List of city names to fetch weather for. Example: --cities 'Buenos Aires' Madrid 'Rome'",
    )

    args = parser.parse_args()
    main(city_names=args.cities)
