import pandas as pd

from src.application.ports.loader import LoaderPort
from src.domain.exceptions import LoadingError


class CSVLoader(LoaderPort):
    def load(self, df: pd.DataFrame, destination: str) -> None:
        if df.empty:
            raise ValueError("Cannot write an empty DataFrame to CSV.")

        try:
            df.to_csv(destination, index=False)
            print(f"Data successfully exported to {destination}")
        except PermissionError:
            raise LoadingError(f"Permission denied: Unable to write CSV to '{destination}'.")
        except IOError as e:
            raise LoadingError(f"I/O error while writing CSV to '{destination}': {str(e)}")
        except Exception as e:
            raise LoadingError(f"Unexpected error while saving CSV: {str(e)}")