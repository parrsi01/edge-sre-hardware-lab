import asyncio
import json
import logging
import os
import time
from collections import deque
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from prometheus_client import Counter, Gauge, Histogram, make_asgi_app
from pydantic import BaseModel

DEVICE_HOST = os.getenv("DEVICE_HOST", "device")
DEVICE_PORT = int(os.getenv("DEVICE_PORT", "9101"))
POLL_INTERVAL = float(os.getenv("POLL_INTERVAL_SECONDS", "2"))
STATIC_DIR = Path(__file__).parent / "static"

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("edge-sre-control")

poll_total = Counter("edge_device_poll_total", "Device poll attempts", ["result"])
poll_duration = Histogram("edge_device_poll_duration_seconds", "Device poll duration")
device_up = Gauge("edge_device_up", "Whether the device returned a healthy reading")
temperature = Gauge("edge_device_temperature_celsius", "Latest device temperature")
voltage = Gauge("edge_device_voltage_volts", "Latest device voltage")
device_sequence = Gauge("edge_device_sequence", "Latest device sequence number")

samples: deque[dict[str, Any]] = deque(maxlen=120)
state: dict[str, Any] = {
    "connected": False,
    "device_status": "unknown",
    "last_success_unix": None,
    "last_error": None,
    "polls_total": 0,
    "polls_successful": 0,
}


class FaultRequest(BaseModel):
    enabled: bool


def parse_reading(payload: str) -> dict[str, Any]:
    parsed = json.loads(payload)
    if parsed.get("status") != "ok":
        raise ValueError(str(parsed.get("error", "device_not_healthy")))
    required = {"device_id", "sequence", "uptime_seconds"}
    missing = sorted(required - parsed.keys())
    if missing:
        raise ValueError(f"missing_fields:{','.join(missing)}")
    return parsed


def availability_percent(successful: int, total: int) -> float | None:
    if total == 0:
        return None
    return round(successful / total * 100, 3)


async def device_command(command: str, timeout: float = 1.5) -> str:
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    reader, writer = await asyncio.wait_for(
        asyncio.open_connection(DEVICE_HOST, DEVICE_PORT), timeout=timeout
    )
    try:
        writer.write((command + "\n").encode())
        await writer.drain()
        response = await asyncio.wait_for(reader.readline(), timeout=timeout)
        if not response:
            raise ConnectionError("empty_device_response")
        return response.decode().strip()
    finally:
        writer.close()
        await writer.wait_closed()


async def poll_once() -> None:
    started = time.monotonic()
    state["polls_total"] += 1
    try:
        reading = parse_reading(await device_command("READ"))
        reading["observed_at_unix"] = round(time.time(), 3)
        samples.append(reading)
        state.update(
            connected=True,
            device_status="ok",
            last_success_unix=reading["observed_at_unix"],
            last_error=None,
            polls_successful=state["polls_successful"] + 1,
        )
        device_up.set(1)
        if isinstance(reading.get("temperature_c"), (int, float)):
            temperature.set(reading["temperature_c"])
        if isinstance(reading.get("voltage_v"), (int, float)):
            voltage.set(reading["voltage_v"])
        device_sequence.set(reading["sequence"])
        poll_total.labels(result="success").inc()
        logger.info(json.dumps({"event": "device_poll", "result": "success", "sequence": reading["sequence"]}))
    except (OSError, asyncio.TimeoutError, ValueError, json.JSONDecodeError) as error:
        state.update(connected=False, device_status="fault", last_error=str(error))
        device_up.set(0)
        poll_total.labels(result="failure").inc()
        logger.warning(json.dumps({"event": "device_poll", "result": "failure", "error": str(error)}))
    finally:
        poll_duration.observe(time.monotonic() - started)


async def polling_loop() -> None:
    while True:
        await poll_once()
        await asyncio.sleep(POLL_INTERVAL)


@asynccontextmanager
async def lifespan(_: FastAPI):
    task = asyncio.create_task(polling_loop())
    try:
        yield
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="Edge SRE Hardware Control Lab",
    description="A hardware-aware reliability lab using C++, Python, CI/CD and observability.",
    version="1.0.0",
    lifespan=lifespan,
)
app.mount("/assets", StaticFiles(directory=STATIC_DIR), name="assets")
app.mount("/metrics", make_asgi_app())


@app.get("/", include_in_schema=False)
async def dashboard() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/readyz")
async def readyz(response: Response) -> dict[str, str]:
    if not state["connected"]:
        response.status_code = 503
        return {"status": "not_ready", "reason": str(state["last_error"])}
    return {"status": "ready"}


@app.get("/api/status")
async def status() -> dict[str, Any]:
    return {
        **state,
        "availability_percent": availability_percent(state["polls_successful"], state["polls_total"]),
        "latest_sample": samples[-1] if samples else None,
        "sample_count": len(samples),
        "slo_target_percent": 99.0,
    }


@app.get("/api/samples")
async def recent_samples(limit: int = 30) -> dict[str, Any]:
    if limit < 1 or limit > 120:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 120")
    return {"samples": list(samples)[-limit:]}


@app.post("/api/fault")
async def set_fault(request: FaultRequest) -> dict[str, Any]:
    command = "SET_FAIL ON" if request.enabled else "SET_FAIL OFF"
    try:
        result = json.loads(await device_command(command))
    except (OSError, asyncio.TimeoutError, json.JSONDecodeError) as error:
        raise HTTPException(status_code=503, detail=f"device command failed: {error}") from error
    return {"requested_fault": request.enabled, "device_response": result}
