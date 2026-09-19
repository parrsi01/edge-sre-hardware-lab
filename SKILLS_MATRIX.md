# Skills Evidence Matrix

Use only these states: `NOT STARTED`, `RESEARCHED`, `READY`, `IN PROGRESS`, `BLOCKED`, `WAITING`, `DONE`, `ABANDONED`.

| Capability | Current state | Evidence now | Next proof | Definition of done |
|---|---|---|---|---|
| Explain architecture | READY | `README.md`, running local stack | Explain without prompts | Each component and boundary is correct |
| Build/test C++ device | DONE | CMake build and `--self-test` in verification script | Maintain after a change | CI and local self-test pass |
| Test Python protocol | DONE | `control-api/tests/test_protocol.py` | Add one meaningful failure test | All tests pass and purpose is explained |
| Operate Compose stack | DONE | `make up`, health checks, `make down` | Repeat from clean clone | All services become healthy |
| Run incident drill | DONE | `make demo` | Repeat with supervisor | Fault, impact, recovery and fresh sample recorded |
| Define SLI/SLO | READY | Poll counters and guide | Agree target/window | Numerator, denominator, target and window recorded |
| Physical Linux agent | NOT STARTED | Agent and `systemd` unit prepared | Approved host/network | Service survives reboot and emits real available data |
| Layered network diagnosis | READY | TCP boundary and runbook | Approved link/IP drill | Lowest failing layer identified with evidence |
| Security review | READY | Localhost defaults and `SECURITY.md` | Supervisor review | Exposure, privileges, data and secrets approved |
| Backup and restore | NOT STARTED | Procedure documented | Separate approved destination | Restored copy passes verification |
| Independent handover | NOT STARTED | Public guide prepared | Second operator | Another person succeeds and gaps are recorded |

The repository proves code and local operation. Rows remain `NOT STARTED` until physical or independent evidence actually exists.
