from pydantic import BaseModel, computed_field

class Weather(BaseModel):
    city_name: str
    temperature_c: float = 0
    wind_speed_mph: float = 0
    humidity: int = 0

    @computed_field
    @property
    def temperature_f(self) -> float:
        """Converts Celsius to Fahrenheit."""
        return round((self.temperature_c * 9 / 5) + 32, 2)

    @computed_field
    @property
    def wind_speed_ms(self) -> float:
        """Converts m/s to mph."""
        return round(self.wind_speed_mph * 0.44704, 2)
