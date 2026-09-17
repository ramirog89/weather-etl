import pandas as pd

from typing import Generic, TypeVar
from abc import ABC, abstractmethod

T = TypeVar("T")

class TransformerPort(ABC, Generic[T]):
    @abstractmethod
    def transform(self, data: T) -> pd.DataFrame:
        pass
