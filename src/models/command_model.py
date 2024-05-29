from pydantic import BaseModel


class CommandRequest(BaseModel):
    action: str
    device_id: int
    value: float
