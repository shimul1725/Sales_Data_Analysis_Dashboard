'''initial_audit.py

Script to perform an initial exploratory audit of the raw Superstore dataset.
It uses the helper functions from ``src.data_loader`` and prints a concise
report to the console as well as writes a markdown summary to
``reports/data_quality_report.md``.
'''  

from pathlib import Path
import pandas as pd
import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from src.data_loader import load_csv, data_audit, preview_dataframe

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
FILENAME = "Superstore.csv"
REPORT_PATH = Path(__file__).resolve().parents[1] / "reports" / "data_quality_report.md"

def main():
    # Load dataset
    df = load_csv(FILENAME)
    rows, cols, missing_counts, dup_count = data_audit(df)

    # Basic info strings
    shape_str = f"**Shape:** {rows:,} rows × {cols:,} columns"
    dtypes_str = "**Column data types:**\n" + "\n".join([f"- {c}: {dt}" for c, dt in df.dtypes.items()])
    missing_str = "**Missing values per column:**\n" + "\n".join([f"- {c}: {cnt}" for c, cnt in missing_counts[missing_counts > 0].items()])
    dup_str = f"**Duplicate rows:** {dup_count}"
    # Summary statistics (numeric columns only)
    summary = df.describe(include="all")
    summary_str = "**Summary statistics (numeric columns):**\n" + summary.to_markdown()

    # Build markdown report
    report_md = "# Data Quality Report\n\n" + "\n\n".join([
        shape_str,
        dtypes_str,
        missing_str if not missing_str.endswith(":") else "- None",
        dup_str,
        summary_str,
        "\n---\n",
        "*First 5 rows preview (displayed in console when script runs):*",
    ])

    # Write report to file
    REPORT_PATH.write_text(report_md, encoding="utf-8")
    print(report_md)
    print("\nFirst 5 rows (preview):")
    print(preview_dataframe(df, 5))

if __name__ == "__main__":
    main()
