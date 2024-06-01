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
    Initializes and starts an asynchronous Modbus TCP server with multiple contexts.

    This server simulates multiple Modbus RTUs for testing purposes, providing
    discrete inputs, coils, holding registers, and input registers for each RTU.

    Returns:
        server: The running Modbus server instance.
    """
    n_reg = 200

    # initialize data store for slave 1
    store1 = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [15] * n_reg),
        co=ModbusSequentialDataBlock(0, [16] * n_reg),
        hr=ModbusSequentialDataBlock(0, [17] * n_reg),
        ir=ModbusSequentialDataBlock(0, [18] * n_reg),
    )

    # initialize data store for slave 2
    store2 = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [25] * n_reg),
        co=ModbusSequentialDataBlock(0, [26] * n_reg),
        hr=ModbusSequentialDataBlock(0, [27] * n_reg),
        ir=ModbusSequentialDataBlock(0, [28] * n_reg),
    )

    context = ModbusServerContext(slaves={1: store1, 2: store2}, single=False)

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
