import logging
import polars as pl

def transform_data(raw_json: dict) -> pl.DataFrame:
    logging.info("Transforming raw API payload with Polars...")

    hourly_data = raw_json.get("hourly", {})

    df_raw = pl.DataFrame(
        {
            "time_str": hourly_data.get("time", []),
            "temperature": hourly_data.get("temperature_2m", []),
            "humidity": hourly_data.get("relative_humidity_2m", []),
            "wind_speed": hourly_data.get("wind_speed_10m", []),
        }
    )

    df_clean = (
        df_raw.lazy()
        .with_columns(
            pl.col("time_str").str.to_datetime("%Y-%m-%dT%H:%M").alias("timestamp"),
            pl.col("temperature").cast(pl.Float64),
            pl.col("humidity").cast(pl.Int64),
            pl.col("wind_speed").cast(pl.Float64),
        )
        .drop("time_str")
        .filter(pl.col("timestamp").is_not_null())
        .with_columns(
            pl.when(pl.col("temperature") > 25.0)
            .then(pl.lit("Warm"))
            .otherwise(pl.lit("Mild"))
            .alias("temp_category")
        )
        .select("timestamp", "temperature", "humidity", "wind_speed", "temp_category")
        .collect()
    )

    logging.info(f"Transformation complete. Shape: {df_clean.shape}")
    return df_clean