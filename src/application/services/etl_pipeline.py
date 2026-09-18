import pandas as pd

from src.application.ports.extractor import ExtractorPort
from src.application.ports.transformer import TransformerPort
from src.application.ports.loader import LoaderPort
from src.domain.exceptions import ETLException

class ETLPipeline:
    """
    Orchestrates the sequential ETL workflow.
    
    Relies purely on abstraction ports (Extractor, Transformer, Loader).
    The orchestrator remains agnostic to specific data formats or remote APIs.
    """

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
            # 1. Extract raw payloads from external source
            raw_data = self.extractor.extract()

            # 2. Transform and validate raw structures into domain/pandas models
            df = self.transformer.transform(raw_data)

            # 3. Persist normalized records to target storage
            self.loader.load(df, destination)
            return df

        # Domain exceptions are allowed to propagate up to the caller
        except ETLException as e:
            print(f"[ETL Pipeline Failed] Domain Error: {str(e)}")
            raise e
        except Exception as e:
            print(f"[ETL Pipeline Failed] Critical Unexpected Error: {str(e)}")
            raise ETLException(f"Pipeline failed due to unhandled system error: {str(e)}")
