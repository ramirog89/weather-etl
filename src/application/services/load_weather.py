import pandas as pd
from src.application.ports.weather_loader import WeatherLoaderPort


class LoadWeatherService:
    def __init__(self, loader: WeatherLoaderPort):
        self.loader = loader

    def execute(self, df: pd.DataFrame, output_path: str) -> None:
        self.loader.save(df, output_path)
