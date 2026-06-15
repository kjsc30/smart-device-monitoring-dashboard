# Smart Device Monitoring and Alert Dashboard

A full-stack IoT device monitoring MVP built with FastAPI, SQLite, HTML/CSS/JavaScript, and Fetch API.

## Features

- Upload sensor data through a frontend dashboard
- Validate device data with Pydantic models
- Detect device status: normal, alert, and danger
- Store sensor records in SQLite
- View all device records
- View alert records
- View device-level statistics
- Delete individual records
- Generate rule-based inspection reports
- Simulate IoT device data upload with a Python script

## Tech Stack

- Backend: Python, FastAPI, Pydantic
- Database: SQLite, SQL
- Frontend: HTML, CSS, JavaScript, Fetch API
- Other: Uvicorn, CORS, Requests

## Project Structure

```text
test-python/
├── main.py
├── device_simulator.py
├── frontend/
│   └── dashboard.html
├── README.md
└── .gitignore
