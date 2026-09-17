from typing import List
import pandas as pd

from src.application.ports.extractor import ExtractorPort
from src.application.ports.transformer import TransformerPort
from src.domain import City, Weather
from src.infrastructure.http.openmeteo import OpenMeteoClient


class WeatherExtractor(ExtractorPort[List[Weather]]):
    def __init__(self, provider: OpenMeteoClient, cities: List[City]):
        self.provider = provider
        self.cities = cities

    def extract(self) -> List[Weather]:
        return [self.provider.extract(c) for c in self.cities]

class WeatherTransformer(TransformerPort[List[Weather]]):
    def transform(self, data: List[Weather]) -> pd.DataFrame:
        if not data:
            return pd.DataFrame()

        records = [w.model_dump() for w in data]
        df = pd.DataFrame(records)
        df = df.sort_values(by="temperature_c", ascending=False).reset_index(drop=True)

        column_mapping = {
            "city_name": "City",
            "temperature_c": "Temperature (C)",
            "temperature_f": "Temperature (F)",
            "humidity": "Humidity (%)",
            "wind_speed_ms": "Wind Speed (m/s)",
            "wind_speed_mph": "Wind Speed (mph)",
        }

        df = df.rename(columns=column_mapping)

        ordered_columns = [
            "City",
            "Temperature (C)",
            "Temperature (F)",
            "Humidity (%)",
            "Wind Speed (m/s)",
            "Wind Speed (mph)",
        ]

        return df[ordered_columns]
