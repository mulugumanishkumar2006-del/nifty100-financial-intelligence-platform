import pandas as pd

from pathlib import Path

from src.config.settings import RAW_DATA_DIR
from src.utils.logger import logger
from src.etl.normaliser import normalize_column_names


def load_excel(file_name, sheet_name=0):
    """
    Load an Excel file and normalize its column names.
    """

    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(f"{file_name} not found.")

    logger.info(f"Loading {file_name}")

    df = pd.read_excel(
    file_path,
    sheet_name=sheet_name,
    header=1
)

    df.columns = [normalize_column_names(col) for col in df.columns]

    logger.info(f"{file_name} loaded successfully")

    return df


if __name__ == "__main__":

    df = load_excel("companies.xlsx")

    print(df.head())

    print(df.columns)