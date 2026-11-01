'''data_loader.py

Utility module to load raw datasets for the Sales Data Analysis project.

Only reads files from the immutable ``data/raw`` folder – the raw data is never
modified in‑place.  All functions raise clear exceptions if the expected file is
missing so that the workflow stops early and the analyst can fix the problem.
'''  

import pathlib
from typing import Tuple
import pandas as pd

# Project‑root is two levels up from this file (src/ -> project root)
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

def get_raw_filepath(filename: str) -> pathlib.Path:
    """Return the absolute path to a raw data file.

    Parameters
    ----------
    filename: str
        Name of the CSV (or any supported pandas‑readable file) located in
        ``data/raw``.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    path = RAW_DATA_DIR / filename
    if not path.is_file():
        raise FileNotFoundError(
            f"Raw dataset '{filename}' not found in {RAW_DATA_DIR}. "
            "Make sure the file is placed there before loading."
        )
    return path

def load_csv(filename: str, **read_kwargs) -> pd.DataFrame:
    """Load a CSV file from the raw data folder.

    Parameters
    ----------
    filename: str
        CSV file name (e.g., ``Superstore.csv``).
    **read_kwargs: dict
        Additional keyword arguments passed to ``pd.read_csv``.

    Returns
    -------
    pd.DataFrame
        The loaded dataframe.
    """
    path = get_raw_filepath(filename)
    df = pd.read_csv(path, **read_kwargs)
    return df

def load_excel(filename: str, sheet_name: str = 0, **read_kwargs) -> pd.DataFrame:
    """Load an Excel workbook from the raw data folder.
    Supports the same semantics as :func:`load_csv`.
    """
    path = get_raw_filepath(filename)
    df = pd.read_excel(path, sheet_name=sheet_name, **read_kwargs)
    return df

def preview_dataframe(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Return the first *n* rows of a dataframe – a tiny helper used in notebooks.
    """
    return df.head(n)

def data_audit(df: pd.DataFrame) -> Tuple[int, int, pd.Series, pd.Series]:
    """Perform a quick audit of a dataframe.

    Returns
    -------
    rows, cols, missing_counts, duplicate_counts
        - rows, cols: shape of the dataframe.
        - missing_counts: ``df.isna().sum()`` Series.
        - duplicate_counts: number of duplicated rows (``df.duplicated().sum()``).
    """
    rows, cols = df.shape
    missing_counts = df.isna().sum()
    duplicate_counts = df.duplicated().sum()
    return rows, cols, missing_counts, duplicate_counts

if __name__ == "__main__":
    # Simple sanity‑check when the module is executed directly.
    try:
        df = load_csv("Superstore.csv")
        print("Loaded dataset with shape:", df.shape)
    except FileNotFoundError as e:
        print(e)
