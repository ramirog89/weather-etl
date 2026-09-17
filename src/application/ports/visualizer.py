from abc import ABC, abstractmethod
import pandas as pd


class WeatherVisualizerPort(ABC):
    @abstractmethod
    def plot_temperature_bar_chart(self, df: pd.DataFrame, output_path: str = "temperature_chart.png") -> str:
        """Generates a bar chart of city temperatures and saves it to a file."""
        pass
