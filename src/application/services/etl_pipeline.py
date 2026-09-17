import pandas as pd

from src.application.ports.extractor import ExtractorPort
from src.application.ports.transformer import TransformerPort
from src.application.ports.loader import LoaderPort

class ETLPipeline:
    def __init__(
        self,
        extractor: ExtractorPort,
        transformer: TransformerPort,
        loader: LoaderPort,
    ):
        self.extractor = extractor
        self.transformer = transformer
        self.loader = loader

    def run(self, destination: str) -> pd.DataFrame:
        raw_data = self.extractor.extract()
        df = self.transformer.transform(raw_data)
        self.loader.load(df, destination)
        return df
