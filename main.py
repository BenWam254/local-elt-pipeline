import logging
from src.extract import extract_raw_data
from src.transform import transform_data
from src.load import load_to_duckdb

def run_pipeline():
    logging.info("=== Starting Local-First ELT Pipeline ===")

    raw = extract_raw_data()
    clean_df = transform_data(raw)
    load_to_duckdb(clean_df)

    logging.info("=== ELT Pipeline Completed Successfully ===")

if __name__ == "__main__":
    run_pipeline()