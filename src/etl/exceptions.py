class ETLError(Exception):
    """Base ETL Exception"""
    pass


class DatasetNotFoundError(ETLError):
    """Dataset not found."""
    pass


class InvalidSheetError(ETLError):
    """Invalid sheet."""
    pass


class EmptyDatasetError(ETLError):
    """Dataset is empty."""
    pass


class InvalidColumnError(ETLError):
    """Required column missing."""
    pass