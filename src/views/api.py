import logging

from fastapi import APIRouter, HTTPException

from config.settings import get_settings
from src.models.command_model import CommandRequest
from src.utils import get_rtu_connection

settings = get_settings()

# Setup logging
logging.basicConfig(
    filename=settings.log_file, level=settings.log_level, format=settings.log_format
)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/execute_command/")
async def execute_command(request: CommandRequest):
    rtu_connection = get_rtu_connection()
    try:
        logger.info(
            f"Executing command: {request.action} on device ID: {request.device_id} with value: {request.value}"
        )
        success = await rtu_connection.execute_command(
            request.action, request.device_id, request.value
        )
        if not success:
            logger.error(
                f"Failed to execute command: {request.action} on device ID: {request.device_id} with value: {request.value}"
            )
            raise HTTPException(status_code=400, detail="Failed to execute command")
        logger.info(
            f"Successfully executed command: {request.action} on device ID: {request.device_id} with value: {request.value}"
        )
        return {"status": "success"}
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e

    except Exception as e:
        logger.exception(f"An error occurred while executing the command: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
