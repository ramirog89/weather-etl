from abc import ABC, abstractmethod
import pandas as pd

class LoaderPort(ABC):
    @abstractmethod
    def load(self, df: pd.DataFrame, destination: str) -> None:
        pass
