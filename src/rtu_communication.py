import asyncio
import logging
from datetime import datetime

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder, BinaryPayloadBuilder

from config.settings import get_settings
from mapping import mapping

# Load settings
settings = get_settings()

# Setup logging
logging.basicConfig(filename=settings.log_file, level=settings.log_level, format=settings.log_format)
logger = logging.getLogger(__name__)


class AsyncRTUConnection:
    def __init__(self, ip, port, timeout, retries):
        """
        Initializes the AsyncRTUConnection class with the given parameters.

        Args:
            ip (str): IP address of the RTU.
            port (int): Port number for the RTU.
            timeout (int): Timeout value for the connection.
            retries (int): Number of retries for the connection.
        """
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.retries = retries
        self.client = None

    async def connect(self):
        """
        Establishes a connection to the RTU.

        Returns:
            bool: True if connection is successful, False otherwise.
        """
        try:
            self.client = AsyncModbusTcpClient(host=self.ip, port=self.port)
            await self.client.connect()
            if self.client.connected:
                logger.info("Connected to RTU at %s:%s", self.ip, self.port)
                return True
            else:
                logger.error("Failed to connect to RTU at %s:%s", self.ip, self.port)
                return False
        except Exception as e:
            logger.exception("Exception while connecting to RTU: %s", e)
            return False

    async def poll_data(self):
        """
        Polls data from the RTU based on the configured mapping.

        Returns:
            dict: Dictionary containing the polled data.
        """
        data = {}
        try:
            for register in mapping.holding_registers:
                if register.data_type == "float":
                    # Read two consecutive registers for a 32-bit float
                    response = await self.client.read_holding_registers(register.address, 2)
                    if response.isError():
                        logger.error(f"Error reading {register.name} from RTU")
                    else:
                        decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.BIG,
                                                                     wordorder=Endian.BIG)
                        data[register.name] = decoder.decode_32bit_float()
                else:
                    response = await self.client.read_holding_registers(register.address, 1)
                    if response.isError():
                        logger.error(f"Error reading {register.name} from RTU")
                    else:
                        data[register.name] = response.getRegister(0)

            for coil in mapping.coils:
                response = await self.client.read_coils(coil.address, 1)
                if response.isError():
                    logger.error(f"Error reading {coil.name} from RTU")
                else:
                    data[coil.name] = response.getBit(0)

            data['timestamp'] = datetime.utcnow().isoformat()
            return data

        except asyncio.TimeoutError:
            logger.error("Timeout while polling RTU at %s:%s", self.ip, self.port)
        except Exception as e:
            logger.exception("Exception while polling RTU: %s", e)
        return None

    async def execute_command(self, action, device_id, value):
        """
        Execute a command on the RTU.

        Parameters:
        action (str): The type of action to perform. Supported actions are "write_coil" and "write_register".
        device_id (int): The address of the device to target.
        value (bool or float): The value to write to the device. For "write_coil", this should be a boolean. For "write_register", this should be a float.

        Returns:
        bool: True if the command was executed successfully, False otherwise.

        Exceptions:
        Logs exceptions encountered during the command execution and returns False.
        """
        try:
            if action == "write_coil":
                address = int(device_id)
                await self.client.write_coil(address, bool(value))
            elif action == "write_register":
                address = int(device_id)
                builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
                builder.add_32bit_float(value)
                payload = builder.to_registers()
                await self.client.write_registers(address, payload)
            else:
                logger.error("Unsupported action: %s", action)
                return False
            return True
        except Exception as e:
            logger.exception("Exception while executing command: %s", e)
            return False

    async def close(self):
        """
        Closes the connection to the RTU.
        """
        if self.client:
            self.client.close()
            logger.info("Connection to RTU at %s:%s closed", self.ip, self.port)


async def main():
    rtu_connection = AsyncRTUConnection(
        ip=settings.rtu_ip,
        port=settings.rtu_port,
        timeout=settings.rtu_timeout,
        retries=settings.rtu_retries
    )
    connected = await rtu_connection.connect()
    data = await rtu_connection.poll_data()
    if connected:
        print("Established secure connection to RTU...")
        # await rtu_connection.close()
    if data:
        print(f"Data received: {data}")
        await rtu_connection.close()


if __name__ == "__main__":
    asyncio.run(main())
