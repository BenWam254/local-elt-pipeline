import logging
import httpx

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

API_URL = "https://api.open-meteo.com/v1/forecast"
PARAMS = {
    "latitude": -1.286389,
    "longitude": 36.817223,
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "timezone": "Africa/Nairobi",
}

def extract_raw_data() -> dict:
    logging.info("Extracting raw metrics from Open-Meteo API...")
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(API_URL, params=PARAMS)
            response.raise_for_status()
            logging.info("Raw data extraction successful.")
            return response.json()
    except httpx.HTTPError as err:
        logging.error(f"HTTP Extraction failed: {err}")
        raise