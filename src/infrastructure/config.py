from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    open_meteo_base_url: str = "https://api.open-meteo.com/v1/forecast"
    open_meteo_geocoding_base_url: str = "https://geocoding-api.open-meteo.com/v1"
    csv_output_path: str = "weather_data.csv"
    chart_output_path: str = "temperature_chart.png"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
