# Edge SRE Lab — one-page operator tutorial

## Start

```bash
git clone https://github.com/parrsi01/edge-sre-hardware-lab.git
cd edge-sre-hardware-lab
make setup
make up
open http://localhost:8000
```

The Mac uses Colima as its local Linux container runtime; Docker Compose controls the stack.

## Demonstrate

1. Show the healthy dashboard and a fresh telemetry timestamp.
2. Select **Inject fault** and wait about three seconds.
3. Explain that liveness remains available while readiness fails.
4. Inspect the failed poll/error state in the dashboard or Grafana.
5. Select **Recover device** and wait for a fresh successful sample.
6. Run `make demo` for the scripted proof and `./scripts/verify.sh` for the full verification.

Views:

- Dashboard: `http://localhost:8000`
- Grafana: `http://localhost:3000/d/edge-sre-lab`
- Prometheus: `http://localhost:9090`
- API docs: `http://localhost:8000/docs`

Use `make status` for container health, `make logs` for live logs, and `make down` to stop the stack.

## File map

| Location | Purpose |
|---|---|
| `device-simulator/` | C++ TCP device and controlled fault state |
| `control-api/` | Python polling, validation, REST, metrics and web dashboard |
| `observability/` | Prometheus and Grafana configuration |
| `hardware-agent/` | Optional approved Linux-host replacement |
| `scripts/` | Setup, demo, readiness and verification commands |
| `.github/workflows/ci.yml` | Public CI checks |
| `docs/` | Public case study and downloadable book |
| `tools/` | Reproducible guide generators |

## Truthful explanation

“I built and verified a small hardware-aware reliability system. A C++ process represents a networked device. A Python control plane validates telemetry, exposes an API and publishes metrics. I can inject a controlled fault, observe its impact and recover the service. The next supervised step is to replace the simulator with an approved Linux device and have another operator reproduce the runbook.”

Do not claim production, FPGA, physical data-centre or CERN experience from the simulator.
