from typing import Optional
from pydantic import BaseModel, Field


class SensorData(BaseModel):
    device_id: str = Field(..., min_length=1, description="device id")
    temperature: float = Field(..., description="temperature")
    humidity: Optional[float] = Field(default=None, ge=0, le=100, description="humidity")
    voltage: Optional[float] = Field(default=None, ge=0, description="voltage")
    location: Optional[str] = Field(default=None, description="location")