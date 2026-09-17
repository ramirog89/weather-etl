from abc import ABC, abstractmethod
from typing import Generic, TypeVar

ExtractOutput = TypeVar("ExtractOutput")
TransformOutput = TypeVar("TransformOutput")


class BaseETLPipeline(ABC, Generic[ExtractOutput, TransformOutput]):
    @abstractmethod
    def extract(self) -> ExtractOutput:
        pass

    @abstractmethod
    def transform(self, data: ExtractOutput) -> TransformOutput:
        pass

    @abstractmethod
    def load(self, data: TransformOutput) -> None:
        pass

    def run(self) -> TransformOutput:
        raw_data = self.extract()
        transformed_data = self.transform(raw_data)
        self.load(transformed_data)
        return transformed_data
