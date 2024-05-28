import logging

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import ASYNCHRONOUS
from config.settings import get_settings

# Load settings
settings = get_settings()

# Setup logging
logging.basicConfig(filename=settings.log_file, level=settings.log_level, format=settings.log_format)
logger = logging.getLogger(__name__)


class InfluxDBModel:
    def __init__(self):
        self.client = InfluxDBClient(
            url=settings.influxdb_url,
            token=settings.influxdb_token,
            org=settings.influxdb_org
        )
        self.write_api = self.client.write_api(write_options=ASYNCHRONOUS)
        self.bucket = settings.influxdb_bucket

    async def write_data(self, measurement: str, tags: dict, fields: dict):
        try:
            logger.info(f"Preparing to write data to InfluxDB: {fields}")
            point = Point(measurement).tag("source", "rtu")
            for key, value in tags.items():
                point = point.tag(key, value)
            for key, value in fields.items():
                point = point.field(key, value)
            point = point.time(fields['timestamp'])
            self.write_api.write(bucket=self.bucket, org=settings.influxdb_org, record=point)
            logger.info("Data successfully written to InfluxDB")
        except Exception as e:
            logger.error(f"Error writing data to InfluxDB: {e}", exc_info=True)

    def close(self):
        self.client.close()
