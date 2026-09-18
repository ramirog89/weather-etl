from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class ExtractorPort(ABC, Generic[T]):
    """
    Inbound Port defining the contract for data extraction.
    
    Concrete infrastructure adapters must implement this port to supply
    data to the pipeline.
    """
    @abstractmethod
    def extract(self) -> T:
        pass