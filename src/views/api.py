from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.controllers.data_controller import DataController

app = FastAPI()

data_controller = DataController()


class DataPayload(BaseModel):
    phase_a_current: float
    phase_b_current: float
    phase_c_current: float
    neutral_current: float
    phase_a_voltage: float
    phase_b_voltage: float
    phase_c_voltage: float
    tap_position: int
    active_power: float
    reactive_power: float
    apparent_power: float
    power_factor: float
    frequency: float
    active_energy: int
    reactive_energy: int


@app.post("/api/data")
async def receive_data(data: DataPayload):
    try:
        await data_controller.process_data(data.dict())
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("shutdown")
def shutdown_event():
    data_controller.close()
