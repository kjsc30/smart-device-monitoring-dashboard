from models import SensorData


def check_sensor_status(data: SensorData) -> tuple[str, str]:
    if data.temperature >= 80:
        return "danger", "temperature is dangerously high"

    if data.temperature > 60:
        return "alert", "temperature is too high"

    if data.temperature < -10:
        return "alert", "temperature is too low"

    if data.humidity is not None and data.humidity > 90:
        return "alert", "humidity is too high"

    if data.voltage is not None and data.voltage < 3.0:
        return "alert", "voltage is too low"

    return "normal", "数据正常"


def generate_inspection_report(alerts: list[dict]) -> str:
    if not alerts:
        return "当前没有异常报警记录，设备整体运行正常。"

    report_lines = []
    report_lines.append(f"本次巡检共发现 {len(alerts)} 条异常记录。")

    for alert in alerts:
        line = (
            f"设备 {alert['device_id']} 在 {alert['created_at']} 出现 {alert['status']} 状态，"
            f"原因：{alert['message']}。"
        )
        report_lines.append(line)

    report_lines.append("建议优先检查高频报警设备，并重点关注温度、电压和湿度异常。")

    return "\n".join(report_lines)