-- load_data.sql
-- Reference script for loading data via SQLite CLI.
-- In practice, sql_runner.py handles this automatically via pandas.to_sql.
--
-- If you prefer the CLI approach:
--   sqlite3 data/superstore.db
--   .mode csv
--   .headers on
--   .import data/processed/superstore_clean.csv sales

-- Verify row count after import
SELECT COUNT(*) AS total_rows FROM sales;
