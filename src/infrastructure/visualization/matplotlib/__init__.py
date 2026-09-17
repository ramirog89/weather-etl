import matplotlib.pyplot as plt
import pandas as pd
from src.application.ports.visualizer import WeatherVisualizerPort


class MatplotlibWeatherVisualizer(WeatherVisualizerPort):
    def plot_temperature_bar_chart(self, df: pd.DataFrame, output_path: str = "temperature_chart.png") -> str:
        if df.empty:
            raise ValueError("Cannot plot an empty DataFrame.")

        # Ensure we sort by temperature for a clean bar visual
        chart_df = df.sort_values(by="Temperature (C)", ascending=True)

        # Initialize figure and axis
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create horizontal bar plot
        bars = ax.barh(chart_df["City"], chart_df["Temperature (C)"], color="#2b5c8f", edgecolor="#1e3d59")

        # Add data labels to each bar
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + 0.3,
                bar.get_y() + bar.get_height() / 2,
                f"{width:.1f}°C",
                va="center",
                ha="left",
                fontsize=9,
                fontweight="bold",
            )

        # Styling and annotations
        ax.set_title("Current Temperature by City (°C)", fontsize=14, pad=15, fontweight="bold")
        ax.set_xlabel("Temperature (°C)", fontsize=11, labelpad=10)
        ax.set_ylabel("City", fontsize=11)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.grid(axis="x", linestyle="--", alpha=0.6)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close(fig)

        print(f"Chart successfully saved to {output_path}")
        return output_path
