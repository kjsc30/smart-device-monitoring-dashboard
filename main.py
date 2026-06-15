from typing import Optional, Annotated

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from models import SensorData
from services import check_sensor_status, generate_inspection_report
from database import (
    init_database,
    save_sensor_data,
    get_sensor_data,
    get_alerts,
    get_devices,
    delete_sensor_data,
)


app = FastAPI(title="Smart Device Data Platform")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_database()


@app.get("/")
def home():
    return {"message": "FastAPI 后端运行成功"}


@app.get("/status")
def status():
    return {
        "system": "smart device platform",
        "status": "running",
    }


@app.post("/upload")
def upload(data: SensorData):
    status_value, message = check_sensor_status(data)
    record_id = save_sensor_data(data, status_value, message)

    return {
        "id": record_id,
        "device_id": data.device_id,
        "temperature": data.temperature,
        "humidity": data.humidity,
        "voltage": data.voltage,
        "location": data.location,
        "status": status_value,
        "message": message,
    }


@app.get("/data")
def data(
    device_id: Annotated[Optional[str], Query(description="filter by device id")] = None,
    status_value: Annotated[
        Optional[str], Query(alias="status", description="filter by status")
    ] = None,
    limit: Annotated[int, Query(ge=1, le=500, description="result limit")] = 50,
):
    records = get_sensor_data(device_id=device_id, status_value=status_value, limit=limit)

    return {
        "count": len(records),
        "data": records,
    }


@app.get("/alerts")
def alerts(
    limit: Annotated[int, Query(ge=1, le=500, description="result limit")] = 50
):
    records = get_alerts(limit=limit)

    return {
        "count": len(records),
        "data": records,
    }


@app.get("/devices")
def devices():
    device_records = get_devices()

    return {
        "count": len(device_records),
        "devices": device_records,
    }


@app.get("/report")
def report():
    alerts_data = get_alerts(limit=10)
    report_text = generate_inspection_report(alerts_data)

    return {
        "report": report_text,
    }


@app.delete("/data/{record_id}")
def delete_data(record_id: int):
    deleted = delete_sensor_data(record_id)

    if not deleted:
        return {
            "success": False,
            "message": f"没有找到 id={record_id} 的数据",
        }

    return {
        "success": True,
        "message": f"已删除 id={record_id} 的数据",
    }