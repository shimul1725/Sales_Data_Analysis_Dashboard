'''data_cleaning.py

Utility functions for cleaning the raw Superstore dataset.
The cleaning steps follow the Phase‑3 requirements:

1. Convert date columns to ``datetime`` objects.
2. Standardise column names to ``snake_case``.
3. Detect and handle missing values.
4. Detect and drop duplicate rows.
5. Save the cleaned DataFrame to ``data/processed``.
6. Produce a Markdown quality‑report in ``reports``.

All functions raise clear exceptions on failure so the workflow stops early
if something unexpected occurs.
'''  

import pathlib
import re
from typing import Tuple
import pandas as pd

# Resolve paths relative to the project root (two levels up from this file)
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Ensure target directories exist
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def _to_snake_case(col: str) -> str:
    """Convert a column name to snake_case.

    - Spaces, hyphens, parentheses are replaced with underscores.
    - Multiple consecutive underscores are collapsed.
    - Upper‑case letters are lower‑cased.
    """
    # Replace non‑alphanumeric characters with underscore
    col = re.sub(r"[\s\-\(\)\%]+", "_", col)
    # Collapse multiple underscores
    col = re.sub(r"_+", "_", col)
    # Strip leading/trailing underscores and lower case
    return col.strip("_").lower()

def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply all cleaning steps and return a new DataFrame.
    The function does **not** modify the input ``df`` in‑place.
    """
    df_clean = df.copy()

    # ---------------------------------------------------
    # 1. Convert date columns to datetime (if they exist)
    # ---------------------------------------------------
    date_cols = [c for c in df_clean.columns if "date" in c.lower()]
    for col in date_cols:
        df_clean[col] = pd.to_datetime(df_clean[col], errors="coerce")

    # ---------------------------------------------------
    # 2. Standardise column names to snake_case
    # ---------------------------------------------------
    new_names = {_to_snake_case(col): col for col in df_clean.columns}
    # ``new_names`` maps new_name -> old_name, we need a rename dict old->new
    rename_map = {old: new for new, old in new_names.items()}
    df_clean = df_clean.rename(columns=rename_map)

    # ---------------------------------------------------
    # 3. Missing values handling
    # ---------------------------------------------------
    # For this dataset we simply report; you could fill or drop later.
    missing = df_clean.isna().sum()
    if missing.any():
        # For demonstration, fill numeric NaNs with 0 and categorical with "unknown"
        for col in df_clean.columns:
            if pd.api.types.is_numeric_dtype(df_clean[col]):
                df_clean[col] = df_clean[col].fillna(0)
            else:
                df_clean[col] = df_clean[col].fillna("unknown")

    # ---------------------------------------------------
    # 4. Duplicate rows handling
    # ---------------------------------------------------
    dup_count = df_clean.duplicated().sum()
    if dup_count > 0:
        df_clean = df_clean.drop_duplicates().reset_index(drop=True)

    return df_clean

def generate_report(df_original: pd.DataFrame, df_clean: pd.DataFrame, report_path: pathlib.Path) -> None:
    """Create a markdown report comparing original vs cleaned data.
    The report includes shape, missing‑value summary, duplicate count and a
    preview of the cleaned dataset.
    """
    # Original audit
    rows_o, cols_o = df_original.shape
    missing_o = df_original.isna().sum()
    dup_o = df_original.duplicated().sum()

    # Cleaned audit
    rows_c, cols_c = df_clean.shape
    missing_c = df_clean.isna().sum()
    dup_c = df_clean.duplicated().sum()

    # Build markdown text
    md = "# Data Quality Report – Cleaned Dataset\n\n"
    md += "## Original raw data\n"
    md += f"**Shape:** {rows_o:,} rows × {cols_o:,} columns\n\n"
    md += "**Missing values per column:**\n"
    md += missing_o[missing_o > 0].to_string() + "\n\n" if missing_o.any() else "- None\n\n"
    md += f"**Duplicate rows:** {dup_o}\n\n"

    md += "## Cleaned data\n"
    md += f"**Shape:** {rows_c:,} rows × {cols_c:,} columns\n\n"
    md += "**Missing values after cleaning:**\n"
    md += missing_c[missing_c > 0].to_string() + "\n\n" if missing_c.any() else "- None\n\n"
    md += f"**Duplicate rows after cleaning:** {dup_c}\n\n"
    md += "**First 5 rows of cleaned data:**\n\n"
    md += df_clean.head().to_markdown() + "\n"

    report_path.write_text(md, encoding="utf-8")

def main():
    # Load raw dataset (expects Superstore.csv in data/raw)
    raw_path = RAW_DATA_DIR / "Superstore.csv"
    if not raw_path.is_file():
        raise FileNotFoundError(f"Raw file not found at {raw_path}")

    df_raw = pd.read_csv(raw_path)
    df_clean = clean_dataframe(df_raw)

    # Save cleaned CSV
    cleaned_path = PROCESSED_DIR / "Superstore_cleaned.csv"
    df_clean.to_csv(cleaned_path, index=False)
    print(f"[DONE] Cleaned dataset saved to {cleaned_path}")

    # Generate report
    report_path = REPORTS_DIR / "data_quality_report_cleaned.md"
    generate_report(df_raw, df_clean, report_path)
    print(f"[DONE] Data quality report saved to {report_path}")

if __name__ == "__main__":
    main()
