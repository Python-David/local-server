import logging

import aiohttp

from config.settings import get_settings
from src.models.influxdb_model import InfluxDBModel

# Load settings
settings = get_settings()

# Setup logging
logging.basicConfig(filename=settings.log_file, level=settings.log_level, format=settings.log_format)
logger = logging.getLogger(__name__)


# async def push_data_to_cloud(self, data: dict):
#     async with aiohttp.ClientSession() as session:
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {self.settings.cloud_api_key}'
#         }
#         async with session.post(self.settings.cloud_api_url, json=data, headers=headers) as response:
#             if response.status != 200:
#                 logger.error(f"Failed to push data to cloud: {await response.text()}")
#             else:
#                 logger.info("Data pushed to cloud successfully")


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
        except Exception as e:
            logger.error(f"Error processing data: {data}, Error: {e}", exc_info=True)

    def close(self):
        try:
            self.influx_model.close()
            logger.info("InfluxDB client closed successfully")
        except Exception as e:
            logger.error(f"Error closing InfluxDB client: {e}", exc_info=True)
