class ETLException(Exception):
    """Base exception for all ETL pipeline errors."""
    pass

class ExtractionError(ETLException):
    """Raised when fetching external data fails (HTTP errors, timeouts, etc.)."""
    pass

class TransformationError(ETLException):
    """Raised when transforming/validating raw data into structured DataFrames fails."""
    pass

class LoadingError(ETLException):
    """Raised when persisting output files (CSV, Storage I/O) fails."""
    pass
