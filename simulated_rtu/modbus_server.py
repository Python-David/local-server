import asyncio

from pymodbus.datastore import (
    ModbusSlaveContext,
    ModbusSequentialDataBlock,
    ModbusServerContext,
)
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.server import StartAsyncTcpServer


async def run_async_server():
    """
    Initializes and starts an asynchronous Modbus TCP server.

    This server simulates a Modbus RTU for testing purposes, providing
    discrete inputs, coils, holding registers, and input registers.

    Returns:
        server: The running Modbus server instance.
    """
    n_reg = 200

    # initialize data store
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0] * n_reg),  # Discrete Inputs
        co=ModbusSequentialDataBlock(0, [0] * n_reg),  # Coils
        hr=ModbusSequentialDataBlock(0, [0] * n_reg),  # Holding Registers
        ir=ModbusSequentialDataBlock(0, [0] * n_reg),  # Input Registers
    )

    context = ModbusServerContext(slaves=store, single=True)

    # initialize the server information
    identity = ModbusDeviceIdentification(
        info_name={
            "VendorName": "Pymodbus",
            "ProductCode": "PM",
            "VendorUrl": "http://example.com",
            "ProductName": "Pymodbus Server",
            "ModelName": "Simulator RTU",
            "MajorMinorRevision": "1.0",
        }
    )

    # Start Async TCP server

    server = await StartAsyncTcpServer(
        context=context,
        host="localhost",
        identity=identity,
        address=("127.0.0.1", 5020),
    )

    return server


if __name__ == "__main__":
    print("Modbus server started on localhost port 5020")
    asyncio.run(run_async_server())
