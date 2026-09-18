import pandas as pd

from src.application.ports.extractor import ExtractorPort
from src.application.ports.transformer import TransformerPort
from src.application.ports.loader import LoaderPort
from src.domain.exceptions import ETLException

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
        try:
            raw_data = self.extractor.extract()
            df = self.transformer.transform(raw_data)
            self.loader.load(df, destination)
            return df
        except ETLException as e:
            print(f"[ETL Pipeline Failed] Domain Error: {str(e)}")
            raise e
        except Exception as e:
            print(f"[ETL Pipeline Failed] Critical Unexpected Error: {str(e)}")
            raise ETLException(f"Pipeline failed due to unhandled system error: {str(e)}")
