#!/usr/bin/env python3
"""Drop-in Linux/Raspberry Pi device for the Edge SRE Lab protocol."""

import json
import os
import socketserver
import time
from glob import glob
from pathlib import Path

STARTED_AT = time.monotonic()
SEQUENCE = 0


def read_temperature() -> float | None:
    for candidate in glob("/sys/class/thermal/thermal_zone*/temp"):
        try:
            raw = float(Path(candidate).read_text().strip())
            value = raw / 1000 if raw > 200 else raw
            if -20 <= value <= 130:
                return round(value, 2)
        except (OSError, ValueError):
            continue
    return None


def reading() -> dict[str, object]:
    global SEQUENCE
    SEQUENCE += 1
    return {
        "device_id": os.getenv("EDGE_DEVICE_ID", "linux-edge-node"),
        "sequence": SEQUENCE,
        "temperature_c": read_temperature(),
        "voltage_v": None,
        "uptime_seconds": int(time.monotonic() - STARTED_AT),
        "status": "ok",
    }


class Handler(socketserver.StreamRequestHandler):
    def handle(self) -> None:
        command = self.rfile.readline(256).decode(errors="replace").strip()
        if command == "READ":
            response = reading()
        elif command == "PING":
            response = {"status": "ok", "reply": "PONG"}
        else:
            response = {"status": "error", "error": "unsupported_command"}
        self.wfile.write((json.dumps(response, separators=(",", ":")) + "\n").encode())


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == "__main__":
    with Server(("0.0.0.0", 9101), Handler) as server:
        print("Linux hardware agent listening on TCP 9101")
        server.serve_forever()

