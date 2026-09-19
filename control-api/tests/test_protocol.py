import json

import pytest

from app.main import availability_percent, parse_reading


def test_parse_valid_reading() -> None:
    payload = json.dumps(
        {
            "device_id": "edge-node-01",
            "sequence": 7,
            "temperature_c": 40.2,
            "voltage_v": 12.01,
            "uptime_seconds": 30,
            "status": "ok",
        }
    )
    assert parse_reading(payload)["sequence"] == 7


def test_parse_rejects_fault() -> None:
    with pytest.raises(ValueError, match="simulated_device_fault"):
        parse_reading('{"status":"fault","error":"simulated_device_fault"}')


def test_parse_rejects_missing_fields() -> None:
    with pytest.raises(ValueError, match="missing_fields"):
        parse_reading('{"status":"ok","device_id":"edge-node-01"}')


def test_availability() -> None:
    assert availability_percent(99, 100) == 99.0
    assert availability_percent(0, 0) is None

