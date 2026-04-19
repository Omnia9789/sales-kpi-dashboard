-- schema.sql
-- SQLite table definition for the Superstore sales data.
-- Note: when using sql_runner.py the table is auto-created from the CSV via
-- pandas.to_sql; this file documents the expected schema for reference.

CREATE TABLE IF NOT EXISTS sales (
    row_id          INTEGER,
    order_id        TEXT,
    order_date      TEXT,
    ship_date       TEXT,
    ship_mode       TEXT,
    customer_id     TEXT,
    customer_name   TEXT,
    segment         TEXT,
    country         TEXT,
    city            TEXT,
    state           TEXT,
    postal_code     TEXT,
    region          TEXT,
    product_id      TEXT,
    category        TEXT,
    sub_category    TEXT,
    product_name    TEXT,
    sales           REAL,
    quantity        INTEGER,
    discount        REAL,
    profit          REAL,
    -- derived columns added by clean.py
    order_year      INTEGER,
    order_month     INTEGER,
    order_yearmonth TEXT,
    profit_margin   REAL,
    sales_outlier   INTEGER,   -- 0/1 boolean
    profit_outlier  INTEGER
);
