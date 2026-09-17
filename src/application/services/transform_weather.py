from typing import List
import pandas as pd
from src.domain import Weather


class TransformWeatherService:
    def execute(self, weather_records: List[Weather]) -> pd.DataFrame:
        """Converts domain Weather entities into a Pandas DataFrame and calculates derived fields."""
        if not weather_records:
            return pd.DataFrame()

        records = [record.model_dump() for record in weather_records]
        df = pd.DataFrame(records)
        df = df.sort_values(by="temperature_c", ascending=False).reset_index(drop=True)

        columns = [
            "city_name",
            "temperature_c",
            "temperature_f",
            "humidity",
            "wind_speed_ms",
            "wind_speed_mph",
        ]

        return df[columns]
