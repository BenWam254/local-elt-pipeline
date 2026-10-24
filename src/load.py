import logging
from pathlib import Path
import duckdb
import polars as pl

DB_PATH = Path("data/warehouse.duckdb")

def load_to_duckdb(df: pl.DataFrame) -> None:
    logging.info(f"Connecting to DuckDB at {DB_PATH}...")
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = duckdb.connect(str(DB_PATH))

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS hourly_weather (
            timestamp TIMESTAMP PRIMARY KEY,
            temperature DOUBLE,
            humidity BIGINT,
            wind_speed DOUBLE,
            temp_category VARCHAR
        );
        """
    )

    conn.register("df_view", df)

    # BY NAME handles column matching automatically
    conn.execute(
        """
        INSERT INTO hourly_weather BY NAME
        SELECT * FROM df_view
        ON CONFLICT (timestamp) DO UPDATE SET
            temperature = excluded.temperature,
            humidity = excluded.humidity,
            wind_speed = excluded.wind_speed,
            temp_category = excluded.temp_category;
        """
    )

    result = conn.execute("SELECT COUNT(*) FROM hourly_weather;").fetchone()
    count = result[0] if result else 0
    logging.info(f"Load complete. Total warehouse records: {count}")
    conn.close()