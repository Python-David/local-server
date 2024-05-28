import asyncio

from pymodbus.client import AsyncModbusTcpClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder

from src.mapping import mapping


async def modify_and_verify_values():
    client = AsyncModbusTcpClient('127.0.0.1', port=5020)
    await client.connect()

    if not client.connected:
        print("Failed to connect to the server")
        return

    try:
        # Write new values to the Modbus server
        for register in mapping.holding_registers:
            if register.data_type == "float":
                builder = BinaryPayloadBuilder(byteorder=Endian.BIG, wordorder=Endian.BIG)
                builder.add_32bit_float(float(register.address + 1000.0))  # Example value
                payload = builder.to_registers()
                await client.write_registers(register.address, payload)
            else:
                await client.write_register(register.address, register.address + 1000)  # Example value

        for coil in mapping.coils:
            await client.write_coil(coil.address, True)  # Example value to True

        # Read back the values to verify changes
        for register in mapping.holding_registers:
            if register.data_type == "float":
                response = await client.read_holding_registers(register.address, 2)
                if response.isError():
                    print(f"Error reading {register.name} from RTU")
                else:
                    decoder = BinaryPayloadDecoder.fromRegisters(response.registers, byteorder=Endian.BIG,
                                                                 wordorder=Endian.BIG)
                    value = decoder.decode_32bit_float()
                    print(f"{register.name}: {value}")
            else:
                response = await client.read_holding_registers(register.address, 1)
                if response.isError():
                    print(f"Error reading {register.name} from RTU")
                else:
                    print(f"{register.name}: {response.registers[0]}")

        for coil in mapping.coils:
            response = await client.read_coils(coil.address, 1)
            if response.isError():
                print(f"Error reading {coil.name} from RTU")
            else:
                print(f"{coil.name}: {response.bits[0]}")

    except Exception as e:
        print(f"Exception: {e}")

    client.close()


if __name__ == "__main__":
    asyncio.run(modify_and_verify_values())
