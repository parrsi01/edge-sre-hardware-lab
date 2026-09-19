# Security Policy and Lab Boundary

## Supported use

This repository is an educational and portfolio lab for systems you own or are explicitly authorized to operate. It is not designed for an internet-facing or production deployment.

## Safe defaults

- Host ports bind to `127.0.0.1`.
- Telemetry is synthetic unless an approved Linux agent is explicitly configured.
- No credentials are required or stored.
- Input validation rejects malformed telemetry.
- Device faults are deliberate, local and reversible.

## Before using a physical host

Obtain approval for the device, network, address/port, collected metrics, operator account, firewall rule, failure drills and any public evidence. Use a restricted service account and key-based access. Do not connect an unmanaged device to a production or office network without approval.

## Prohibited activity

Do not capture another person’s traffic, scan unapproved hosts, test production systems, publish internal addresses, commit secrets or collect personal data. The dashboard/control endpoints have no authentication and must not be exposed to a shared network.

## Reporting a vulnerability

Do not publish live secrets or exploitable private-system details in an issue. Open a GitHub issue only for flaws reproducible in this public lab with synthetic data, or contact the repository owner privately through their GitHub profile.
