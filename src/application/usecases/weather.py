from typing import List
import pandas as pd

from src.application.usecases.base import BaseETLPipeline
from src.application.services import (
    ExtractWeatherService,
    TransformWeatherService,
    LoadWeatherService,
)
from src.domain import City, Weather


class WeatherUseCase(BaseETLPipeline[List[Weather], pd.DataFrame]):
    def __init__(
        self,
        cities: List[City],
        extract_service: ExtractWeatherService,
        transform_service: TransformWeatherService,
        load_service: LoadWeatherService,
        output_path: str = "weather_data.csv",
    ):
        self.cities = cities
        self.extract_service = extract_service
        self.transform_service = transform_service
        self.load_service = load_service
        self.output_path = output_path

    def extract(self) -> List[Weather]:
        return self.extract_service.execute(self.cities)

    def transform(self, data: List[Weather]) -> pd.DataFrame:
        return self.transform_service.execute(data)

    def load(self, data: pd.DataFrame) -> None:
        self.load_service.execute(data, output_path=self.output_path)
