from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # InfluxDB
    influxdb_db: str
    influxdb_admin_user: str
    influxdb_admin_password: str
    influxdb_url: str = "http://localhost:8086"
    influxdb_token: str
    influxdb_org: str
    influxdb_bucket: str

    # PostgreSQL
    postgres_db: str
    postgres_user: str
    postgres_password: str

    # RTU Configuration
    rtu_ip: str = "127.0.0.1"
    rtu_port: int = 5020
    rtu_protocol: str = "Modbus"
    rtu_communication_type: str = "tcp"
    rtu_timeout: int = 10
    rtu_retries: int = 3

    # Cloud Configuration
    cloud_api_url: str
    cloud_api_key: str

    # Logging Configuration
    log_level: str = "INFO"
    log_file: str = "logs/local_server.log"
    log_format: str = "%(asctime)s -%(levelname)s - %(module)s:%(funcName)s::ln.%(lineno)s:: >%(message)s<"

    # App Configuration

    polling_interval: int = 5

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
