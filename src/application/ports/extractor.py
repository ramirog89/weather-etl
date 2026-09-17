from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class ExtractorPort(ABC, Generic[T]):
    @abstractmethod
    def extract(self) -> T:
        pass