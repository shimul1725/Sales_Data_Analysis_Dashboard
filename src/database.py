'''database.py

Utility module to create the SQLite database for the Sales Data Analysis project,
import the cleaned CSV, and store it in a relational table.

The cleaned CSV is expected at ``data/processed/Superstore_cleaned.csv`` and the
resulting database will be saved as ``data/sales_analysis.db``.
'''  

import pathlib
import pandas as pd
import sqlite3

# Paths (project‑root is two levels up from this file)
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
PROCESSED_CSV = PROJECT_ROOT / "data" / "processed" / "Superstore_cleaned.csv"
DB_PATH = PROJECT_ROOT / "data" / "sales_analysis.db"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"

def create_connection(db_path: pathlib.Path) -> sqlite3.Connection:
    """Create a SQLite connection (will create the file if it does not exist)."""
    conn = sqlite3.connect(str(db_path))
    return conn

def execute_schema(conn: sqlite3.Connection, schema_file: pathlib.Path) -> None:
    """Read the SQL schema file and execute its statements.
    ``sqlite3`` can execute multiple statements separated by ``;``.
    """
    script = schema_file.read_text(encoding="utf-8")
    conn.executescript(script)
    conn.commit()

def load_cleaned_data(conn: sqlite3.Connection, csv_path: pathlib.Path, table_name: str = "sales") -> None:
    """Load the cleaned CSV into the SQLite table.
    Uses pandas ``to_sql`` with ``if_exists='append'`` – the schema must already exist.
    """
    df = pd.read_csv(csv_path)
    # Ensure pandas does not try to create its own index column
    df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
    conn.commit()

def main():
    # Verify cleaned CSV exists
    if not PROCESSED_CSV.is_file():
        raise FileNotFoundError(f"Cleaned CSV not found at {PROCESSED_CSV}")
    # Create DB (or connect if exists)
    conn = create_connection(DB_PATH)
    print(f"[INFO] SQLite DB at {DB_PATH}")
    # Execute schema to create tables
    if not SCHEMA_PATH.is_file():
        raise FileNotFoundError(f"Schema file not found at {SCHEMA_PATH}")
    execute_schema(conn, SCHEMA_PATH)
    print("[INFO] Schema executed.")
    # Load data
    load_cleaned_data(conn, PROCESSED_CSV)
    print("[DONE] Cleaned data loaded into 'sales' table.")
    conn.close()

if __name__ == "__main__":
    main()
