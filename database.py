import sqlite3
from pathlib import Path
from datetime import datetime

from models import SensorData


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "sensor_data.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def init_database():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                temperature REAL NOT NULL,
                humidity REAL,
                voltage REAL,
                location TEXT,
                status TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


def row_to_record(row) -> dict:
    return {
        "id": row[0],
        "device_id": row[1],
        "temperature": row[2],
        "humidity": row[3],
        "voltage": row[4],
        "location": row[5],
        "status": row[6],
        "message": row[7],
        "created_at": row[8],
    }


def save_sensor_data(data: SensorData, status: str, message: str) -> int:
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO sensor_data (
                device_id, temperature, humidity, voltage, location,
                status, message, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.device_id,
                data.temperature,
                data.humidity,
                data.voltage,
                data.location,
                status,
                message,
                created_at,
            ),
        )

        return int(cursor.lastrowid)


def get_sensor_data(device_id=None, status_value=None, limit=50) -> list[dict]:
    sql = """
        SELECT id, device_id, temperature, humidity, voltage, location,
               status, message, created_at
        FROM sensor_data
    """

    conditions = []
    params = []

    if device_id:
        conditions.append("device_id = ?")
        params.append(device_id)

    if status_value:
        conditions.append("status = ?")
        params.append(status_value)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    sql += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()

    return [row_to_record(row) for row in rows]


def get_alerts(limit=50) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT id, device_id, temperature, humidity, voltage, location,
                   status, message, created_at
            FROM sensor_data
            WHERE status != 'normal'
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [row_to_record(row) for row in rows]


def get_devices() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT device_id, COUNT(*) AS total, MAX(created_at) AS last_seen
            FROM sensor_data
            GROUP BY device_id
            ORDER BY last_seen DESC
            """
        ).fetchall()

    return [
        {
            "device_id": row[0],
            "total": row[1],
            "last_seen": row[2],
        }
        for row in rows
    ]


def delete_sensor_data(record_id: int) -> bool:
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM sensor_data WHERE id = ?",
            (record_id,),
        )

    return cursor.rowcount > 0