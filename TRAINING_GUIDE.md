# SRE Training Guide for an IP4IT / Geneva Business News Lab

Checked 19 September 2026 (Europe/Zurich).

## Decision

Use this repository as a six-week, evidence-producing SRE training project. Start on the Mac, then replace the simulated device with one centre-approved Linux host. The target is not a certificate or a promise of employment; it is a public body of work that a supervisor and another operator can reproduce.

IP4IT describes an environment for IT specialists’ professional integration, with bilingual daily practice, vocational coaches, virtualized/cloud labs and certification preparation. Geneva Business News separately lists four practice pillars—support, development, systems and networking—plus a weekly IT session, technical presentations, workshops/labs and GLPI, OCS, Nagios and Wireshark. These official pages show programme alignment. They do not confirm an SRE job, a paid placement, a specific device, current seat availability, funding, supervision or work authorization. Those remain **UNKNOWN until IP4IT confirms them**.

Official programme sources: [IP4IT](https://www.ip4it.ch/) and [Geneva Business News IT](https://genevabusinessnews.ch/it/).

## What an SRE does in this proposed training project

An SRE applies software engineering to operations. In this project, that means you would:

1. Define the service and its users: the control plane must obtain valid, fresh device telemetry and remain diagnosable during a device fault.
2. Establish a baseline: build the code, run the tests, record versions and confirm healthy telemetry.
3. Operate the stack: start and stop services, inspect health checks, logs, metrics, network state and process state.
4. Define reliability: use successful polls ÷ total polls as the first service-level indicator; agree on a target and time window before calling it an SLO.
5. Respond to incidents: detect, declare impact, preserve evidence, diagnose by layer, recover, verify a new sample and write a short post-incident record.
6. Reduce toil: automate repeated setup and verification without hiding failures or removing human control.
7. Protect the lab: use a restricted account, synthetic data, localhost-only defaults and only centre-approved network access.
8. Prove recoverability: back up the public project, restore it to a separate location and rerun validation.
9. Communicate: present one technical topic, maintain a runbook and hand the system to another participant.

This is a **proposed supervised project**, not a statement that IP4IT currently employs SREs.

## DevSecOps/SRE extension: Secure Edge Platform

The [DevSecOps/SRE Playbook](DEVSECOPS_SRE_PLAYBOOK.md) adds a second, employment-facing layer to this project. The immediate money-first capability is a bounded, authorized non-production reliability and secure-deployment review: reproduce a Docker deployment, add CI checks, document an SLO, run one controlled failure, and hand over a runbook. It is a potential service package, not guaranteed income and not permission to work without Swiss authorization or a client agreement.

The current Mac evidence is Docker/Compose, Python/FastAPI, C++, Prometheus/Grafana, GitHub Actions, Linux/networking fundamentals and a recovery drill. A supervised centre extension may use VMware/Hyper-V, an approved Linux VM or host, Kubernetes, GitLab CI, Terraform/OpenTofu, Ansible/Puppet, a log platform and approved image/dependency scanners. These are **next-stage tools**, not claims that they are installed or mastered on this Mac.

The practical order is Linux/TCP/IP -> Docker -> Kubernetes/health probes -> CI/IaC -> Prometheus/Grafana/logs -> security gates -> incident response and handover. Read the role matrix and six-week definitions of done in the playbook before asking the centre for access.

## What you would work on each week

| Week | Centre work | Public evidence | Definition of done |
|---|---|---|---|
| 1 — baseline | Rebuild the Mac stack; explain C++, Python, TCP, containers and health checks | Architecture diagram and verified test output | You can start, inspect, fault, recover and stop the stack without prompts |
| 2 — physical host | Deploy `hardware-agent/edge_agent.py` to one approved Linux host as a restricted `systemd` service | Sanitized deployment runbook and real available host metrics | Service survives reboot and the API receives fresh samples |
| 3 — incidents | Run three approved failures: service stop, link interruption and invalid/stale telemetry | Three incident records with timestamp, symptom, diagnosis, action and verification | Recovery is measured and causal evidence is preserved |
| 4 — security | Review exposure, privileges, update process and secret handling | Threat-boundary note and configuration review | No credentials in Git; only approved ports/data; failure is closed by default |
| 5 — reliability | Agree an SLI/SLO window; add an alert; perform backup and restore | SLO worksheet, alert proof and restore report | Numerator, denominator, window and restore result are explicit |
| 6 — handover | Another participant follows the runbook; deliver a five-minute presentation and mock interview | Corrected runbook and independently scored skills matrix | A second person reproduces the demo and records gaps honestly |

Apply to suitable roles during training; do not wait for week six.

## Daily operating loop at the centre

| Minutes | Action |
|---:|---|
| 0–10 | State the user outcome, risk and evidence expected today |
| 10–35 | Make one controlled change or run one drill |
| 35–45 | Run tests; inspect logs, metrics and health |
| 45–55 | Record result, limitation and one remaining gap |
| 55–60 | Commit reviewed changes and choose the next action |

If GLPI is available, record the controlled incident as a ticket. If Nagios is available, compare its check/alert path with Prometheus. Use Wireshark only on your own lab traffic or an explicitly provided capture. Use OCS only if it fits the centre’s approved inventory architecture. Tools serve the reliability objective; installing every named product is not the objective.

## Geneva and Swiss employment evidence

### Verified current Geneva figures

OCSTAT reports:

- Geneva full-time-equivalent employment increased **1.0% quarter-on-quarter in Q2 2026**, seasonally adjusted, excluding the primary sector, extraterritorial activities and domestic services.
- The broader 2024 structural series increased **0.8%** to **363,071 FTE jobs**.
- Secondary-sector FTE employment increased **0.8% in 2024**, while tertiary-sector FTE employment also increased **0.8%**.
- The Geneva **information and communication** branch decreased **1.7% in 2024**.

Source: [OCSTAT, 27 August 2026](https://statistique.ge.ch/actualites/welcome.asp?Actudomaine=06_02&aaaa1=2026&aaaa2=2026&actu=6016&mm1=05/01&mm2=12/31&num=0).

Therefore, the evidence does **not** justify saying that Geneva SRE employment itself rose by a known percentage. OCSTAT measures economic branches, not the SRE occupation, and the latest detailed Geneva information/communication figure moved down.

### Broader Swiss ICT outlook

The 2025 ICT-Berufsbildung Schweiz workforce study, using federal statistics and BAK Economics inputs, starts from about **266,000 ICT workers** and projects through 2033:

- **61,600 additional positions** from economic growth and structural change—about **23.2% of the 2024 base**, spread across the forecast period, not an annual rate.
- **67,000 replacement needs** from retirements and emigration.
- **128,600 gross personnel needs** in total, of which the study estimates 54,400 will remain as an additional domestic education need after expected graduates and immigration.
- Software developers account for the largest projected gross occupational need (**46,200**), followed by systems analysts (**17,600**).
- More than two-thirds of ICT workers are employed outside the core ICT industry, which is why reliable-systems skills can apply in finance, education, public administration, life sciences, logistics and industry.

Source: [ICT-Fachkräftesituation 2033 study](https://www.ict-berufsbildung.ch/resources/BSS-Schlussbericht-ICT-Bildungsbedarf-2033-2025-09_09.pdf), published 2025.

These are national forecasts, not current Geneva vacancies, entry-level conversion rates or a guarantee of work. They support a cross-industry SRE/DevOps portfolio while current applications and authorization checks continue.

## Skills you must be able to demonstrate

| Capability | Evidence in this repository | Physical/supervised proof still needed |
|---|---|---|
| Python service engineering | FastAPI control plane, validation and tests | Independent change and review |
| Modern C++ | TCP device simulator and self-test | Real device/domain integration where available |
| Linux administration | Container runtime and supplied `systemd` unit | Deploy and diagnose on an approved host |
| Networking | TCP protocol, localhost binding and layered runbook | Link/IP/route diagnosis on the lab network |
| Observability | Prometheus metrics and Grafana dashboard | Useful alert reviewed by a supervisor |
| Incident response | Controlled fault and scripted recovery | Three surprise/controlled drills with measured recovery |
| CI/CD | GitHub Actions build and tests | Explain failure modes and fix a broken run |
| Backup/recovery | Restore procedure | Timed, validated restore from approved storage |
| Communication | README, guide and demo script | Independent operator handover |

Use [SKILLS_MATRIX.md](SKILLS_MATRIX.md) to record `NOT STARTED`, `IN PROGRESS`, `BLOCKED` or `DONE` with proof.

## First meeting script

> I prepared a small hardware-aware reliability lab. It polls a C++ device, validates telemetry in Python, exposes metrics, detects a controlled fault and recovers. The local version works and its limits are documented. I would like to replace the simulator with one approved Linux host here, practise three safe service/network failures, define a small SLO and produce a runbook another participant can follow.

Ask for five decisions:

1. Which approved Linux device and isolated network may be used?
2. Who can review one hour per week and witness the final drill?
3. Which existing tool—GLPI, OCS, Nagios or Wireshark—should be integrated first, if any?
4. What data, screenshots and organization names may appear publicly?
5. What participation, funding and work-authorization framework applies?

Definition of meeting done: one named reviewer, one approved host/network boundary, a six-week schedule, a public-evidence decision and explicit participation/authorization information. Interest alone is not a project start.

## Start now

```bash
git clone https://github.com/parrsi01/edge-sre-hardware-lab.git
cd edge-sre-hardware-lab
make setup
make up
make demo
./scripts/verify.sh
```

Then read the [PDF book](docs/assets/SRE_BEGINNER_GUIDE_IP4IT_GENEVA.pdf) and explain the architecture aloud without reading.

## Safety and truth rules

- Operate only systems you own or are explicitly authorized to use.
- Do not expose the current unauthenticated control endpoints to a shared network.
- Do not capture other people’s traffic, scan the office network or publish internal identifiers.
- Never commit credentials, tokens, Wi-Fi details, CVs or personal records.
- Keep this under **Projects**, not Employment, unless a real employment relationship exists.
- A public repository, course or six-week project does not guarantee employment or work authorization.

## Next action

Run `make demo`, then describe the failure, the user impact and the evidence of recovery in five sentences.

Definition of done: the dashboard returns to ready after a fresh successful sample, and your explanation names the SLI numerator, denominator and measurement window.
