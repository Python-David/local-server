import asyncio
import logging

from fastapi import FastAPI

from config.settings import get_settings
from controllers.data_controller import DataController
from src.utils import create_rtu_connection, get_rtu_connection
from views.api import router as api_router

app = FastAPI()

# Include the API router
app.include_router(api_router, prefix="/api")

# Load settings
settings = get_settings()

# Setup logging
logging.basicConfig(
    filename=settings.log_file, level=settings.log_level, format=settings.log_format
)
logger = logging.getLogger(__name__)

create_rtu_connection(settings)
rtu_connection = get_rtu_connection()

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
        await asyncio.sleep(
            settings.polling_interval
        )  # Polling interval set to 5 seconds


@app.on_event("shutdown")
async def shutdown_event():
    await rtu_connection.close()
    data_controller.close()


if __name__ == "__main__":
    # TODO - Remember to review this part for production

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
