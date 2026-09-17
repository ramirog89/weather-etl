from abc import ABC, abstractmethod
import pandas as pd


class WeatherLoaderPort(ABC):
    @abstractmethod
    def save(self, df: pd.DataFrame, destination: str) -> None:
        pass
