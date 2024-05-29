from typing import List

from pydantic import BaseModel


class RegisterMapping(BaseModel):
    name: str
    address: int
    type: str
    data_type: str


class Mapping(BaseModel):
    holding_registers: List[RegisterMapping]
    coils: List[RegisterMapping]


# TODO 1. We can make this more dynamic, probably filling it up from a .csv or .yaml file
mapping = Mapping(
    holding_registers=[
        RegisterMapping(name="phase_a_current", address=0, type="holding", data_type="float"),
        RegisterMapping(name="phase_b_current", address=2, type="holding", data_type="float"),
        RegisterMapping(name="phase_c_current", address=4, type="holding", data_type="float"),
        RegisterMapping(name="neutral_current", address=6, type="holding", data_type="float"),
        RegisterMapping(name="phase_a_voltage", address=20, type="holding", data_type="float"),
        RegisterMapping(name="phase_b_voltage", address=22, type="holding", data_type="float"),
        RegisterMapping(name="phase_c_voltage", address=24, type="holding", data_type="float"),
        RegisterMapping(name="tap_position", address=100, type="holding", data_type="int"),
        RegisterMapping(name="active_power", address=140, type="holding", data_type="float"),
        RegisterMapping(name="reactive_power", address=142, type="holding", data_type="float"),
        RegisterMapping(name="apparent_power", address=144, type="holding", data_type="float"),
        RegisterMapping(name="power_factor", address=146, type="holding", data_type="float"),
        RegisterMapping(name="frequency", address=148, type="holding", data_type="float"),
        RegisterMapping(name="active_energy", address=160, type="holding", data_type="float"),
        RegisterMapping(name="reactive_energy", address=162, type="holding", data_type="float"),
    ],
    coils=[
        RegisterMapping(name="cb_status", address=40, type="coil", data_type="binary"),
        RegisterMapping(name="ds_status", address=60, type="coil", data_type="binary"),
        RegisterMapping(name="es_status", address=80, type="coil", data_type="binary"),
        RegisterMapping(name="capacitor_status", address=120, type="coil", data_type="binary"),
    ]
)
