import asyncio
import logging

from config.settings import get_settings
from controllers.data_controller import DataController
from rtu_communication import AsyncRTUConnection
from views.api import app

# Load settings
settings = get_settings()

# Setup logging
logging.basicConfig(filename=settings.log_file, level=settings.log_level, format=settings.log_format)
logger = logging.getLogger(__name__)

rtu_connection = AsyncRTUConnection(
    ip=settings.rtu_ip,
    port=settings.rtu_port,
    timeout=settings.rtu_timeout,
    retries=settings.rtu_retries
)

data_controller = DataController()


@app.on_event("startup")
async def startup_event():
    connected = await rtu_connection.connect()
    if connected:
        asyncio.create_task(poll_rtu_data())


async def poll_rtu_data():
    while True:
        try:
            data = await rtu_connection.poll_data()
            if data:
                await data_controller.process_data(data)
        except Exception as e:
            logger.error(f"Error during data polling or processing: {e}")
        await asyncio.sleep(settings.polling_interval)  # Polling interval set to 5 seconds


@app.on_event("shutdown")
async def shutdown_event():
    await rtu_connection.close()
    data_controller.close()

if __name__ == "__main__":
    # TODO - Remember to review this part for production
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
