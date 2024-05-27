import asyncio
import logging
import yaml
from pymodbus.client import AsyncModbusTcpClient

# Load configuration
with open("config/config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

# Setup logging
logging.basicConfig(filename=config['logging']['file'], level=config['logging']['level'])
logger = logging.getLogger(__name__)


class AsyncRTUConnection:
    def __init__(self, ip, port, timeout, retries):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self.client = None

    async def connect(self):
        try:
            self.client = AsyncModbusTcpClient(host=self.ip, port=self.port)
            await self.client.connect()
            logger.info("Connected to RTU at %s:%s", self.ip, self.port)
            return True
        except Exception as e:
            logger.exception("Exception while connecting to RTU: %s", e)
            return False

    async def close(self):
        if self.client:
            self.client.close()
            logger.info("Connection to RTU at %s:%s closed", self.ip, self.port)


# async def main():
#     rtu_connection = AsyncRTUConnection(
#         ip=config['rtu']['ip'],
#         port=config['rtu']['port'],
#         timeout=config['rtu']['timeout'],
#         retries=config['rtu']['retries']
#     )
#     connected = await rtu_connection.connect()
#     if connected:
#         print("Established secure connection to RTU...")
#         await rtu_connection.close()
#
#
# if __name__ == "__main__":
#     asyncio.run(main())
