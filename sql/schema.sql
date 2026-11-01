-- sql/schema.sql
-- Relational schema for the Superstore sales dataset.
-- Table: sales
-- Each column mirrors the cleaned CSV (snake_case) and uses appropriate SQLite types.

DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    row_id        INTEGER PRIMARY KEY,
    order_id      TEXT    NOT NULL,
    order_date    DATE    NOT NULL,
    ship_date     DATE,
    ship_mode     TEXT,
    customer_id   TEXT,
    customer_name TEXT,
    segment       TEXT,
    country       TEXT,
    city          TEXT,
    state         TEXT,
    postal_code   INTEGER,
    region        TEXT,
    product_id    TEXT,
    category      TEXT,
    sub_category  TEXT,
    product_name  TEXT,
    sales         REAL,
    quantity      INTEGER,
    discount      REAL,
    profit        REAL
);
