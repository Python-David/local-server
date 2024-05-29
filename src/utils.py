from src.rtu_communication import AsyncRTUConnection

rtu_connection = None


def create_rtu_connection(settings):
    global rtu_connection
    rtu_connection = AsyncRTUConnection(
        ip=settings.rtu_ip,
        port=settings.rtu_port,
        timeout=settings.rtu_timeout,
        retries=settings.rtu_retries
    )
    return rtu_connection


def get_rtu_connection():
    global rtu_connection
    if rtu_connection is None:
        raise Exception("RTU connection is not initialized")
    return rtu_connection
