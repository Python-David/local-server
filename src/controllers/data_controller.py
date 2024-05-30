import logging

import httpx

from config.settings import get_settings
from src.models.influxdb_model import InfluxDBModel

# Load settings
settings = get_settings()

# Setup logging
logging.basicConfig(
    filename=settings.log_file, level=settings.log_level, format=settings.log_format
)
logger = logging.getLogger(__name__)


async def push_data_to_django_server(data: dict):
    """
    Pushes data to the Django server.

    Parameters:
    data (dict): The data to push to the Django server.

    Returns:
    None

    Exceptions:
    Logs any exceptions encountered during the HTTP request.
    """
    async with httpx.AsyncClient() as client:
        # TODO - This url will come from the settings file and point to our Django app. Remember to implement security
        url = settings.django_api_url
        try:
            response = await client.post(url, json=data, timeout=10.0)
            response.raise_for_status()
            logger.info("Data successfully pushed to mock server")
            logger.info(f"Response: {response.json()}")
        except httpx.HTTPStatusError as e:
            logger.error(
                f"HTTP error occurred while pushing data to mock server: {e.response.text}"
            )
        except Exception as e:
            logger.error(f"An error occurred while pushing data to mock server: {e}")


class DataController:
    """
    DataController handles the processing and storage of data from the RTU.

    Attributes:
    influx_model (InfluxDBModel): The model used to interact with InfluxDB.

    Methods:
    process_data(data: dict): Processes and stores the data in InfluxDB and pushes it to a mock server.
    close(): Closes the InfluxDB client connection.
    """

    def __init__(self):
        """
        Initializes the DataController with an InfluxDB model.
        """
        self.influx_model = InfluxDBModel()

    async def process_data(self, data: dict):
        """
        Processes and stores the data in InfluxDB and pushes it to the django server (mock for now).

        Parameters:
        data (dict): The data to process and store.

        Returns:
        None

        Exceptions:
        Logs any exceptions encountered during the processing and storage of data.
        """
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
        """
        Closes the InfluxDB client connection.

        Returns:
        None

        Exceptions:
        Logs any exceptions encountered while closing the InfluxDB client.
        """
        try:
            self.influx_model.close()
            logger.info("InfluxDB client closed successfully")
        except Exception as e:
            logger.error(f"Error closing InfluxDB client: {e}", exc_info=True)
