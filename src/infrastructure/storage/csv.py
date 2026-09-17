import pandas as pd
from src.application.ports.weather_loader import WeatherLoaderPort


class CSVWeatherLoader(WeatherLoaderPort):
    def save(self, df: pd.DataFrame, destination: str) -> None:
        if df.empty:
            raise ValueError("Cannot write an empty DataFrame to CSV.")

        df.to_csv(destination, index=False)
        print(f"Data successfully exported to {destination}")
