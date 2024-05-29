import logging

import httpx

from config.settings import get_settings
from src.models.influxdb_model import InfluxDBModel

# Load settings
settings = get_settings()

# Setup logging
logging.basicConfig(filename=settings.log_file, level=settings.log_level, format=settings.log_format)
logger = logging.getLogger(__name__)


async def push_data_to_django_server(data: dict):
    async with httpx.AsyncClient() as client:
        # TODO - This url will come from the settings file and point to our Django app. Remember to implement security
        url = "https://httpbin.org/post"
        try:
            response = await client.post(url, json=data, timeout=10.0)
            response.raise_for_status()
            logger.info("Data successfully pushed to mock server")
            logger.info(f"Response: {response.json()}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred while pushing data to mock server: {e.response.text}")
        except Exception as e:
            logger.error(f"An error occurred while pushing data to mock server: {e}")


class DataController:
    def __init__(self):
        self.influx_model = InfluxDBModel()

    async def process_data(self, data: dict):
        try:
            logger.info(f"Processing data: {data}")
            fields = data
            tags = {}  # Add any tags if needed
            await self.influx_model.write_data("sensor_data", tags, fields)
            logger.info("Data successfully written to InfluxDB")

            # Push data to mock server
            await push_data_to_django_server(data)

        except Exception as e:
            logger.error(f"Error processing data: {data}, Error: {e}", exc_info=True)

    def close(self):
        try:
            self.influx_model.close()
            logger.info("InfluxDB client closed successfully")
        except Exception as e:
            logger.error(f"Error closing InfluxDB client: {e}", exc_info=True)
