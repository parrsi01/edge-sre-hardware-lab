# DevSecOps and SRE Playbook for Geneva

Checked 19 September 2026 (Europe/Zurich). This is the implementation companion to the [SRE beginner PDF](docs/assets/SRE_BEGINNER_GUIDE_IP4IT_GENEVA.pdf) and the public [Edge SRE Hardware Lab](https://github.com/parrsi01/edge-sre-hardware-lab).

For a zero-DevOps starting point, read [PROTON_SRE_GENEVA_BEGINNER_GUIDE.txt](PROTON_SRE_GENEVA_BEGINNER_GUIDE.txt) first, then use the [Proton Geneva companion PDF](docs/assets/PROTON_SRE_GENEVA_BEGINNER_GUIDE.pdf). The text guide defines each component before the role mapping; the PDF is a printable, validity-first version.

## Executive decision

Build one demonstrable project called **Secure Edge Platform**. It is a small, hardware-aware service that is:

1. packaged with Docker;
2. deployed locally today and to an approved Kubernetes lab later;
3. run through CI with tests and security gates;
4. measured with Prometheus/Grafana and an explicit SLO;
5. operated with an incident runbook, recovery drill and postmortem.

This is the smallest project that connects the user's current C++/Python/Linux/networking work to the recurring DevSecOps/SRE themes in the supplied CERN, Proton, adesso, PostFinance and Pascal Dietrich descriptions. It is evidence of a project, not evidence of senior production experience, a CERN contract, a paid placement or work authorization.

## What is already true, what is next, and what is unknown

| Area | Evidence today | Next supervised proof | Do not claim yet |
|---|---|---|---|
| Service code | C++ device simulator, Python/FastAPI control plane, tests | Replace the simulator with one approved Linux host | Production hardware or CERN DAQ experience |
| Containers | Docker Compose, health checks and a verified recovery drill | Build and sign a Kubernetes image and deployment | Production Kubernetes administration |
| Observability | Prometheus metrics and Grafana dashboard | Add an agreed alert and log/trace correlation | 99.95% production uptime |
| Delivery | GitHub Actions builds C++ and tests Python | Repeat the same gates in centre-approved GitLab CI | Enterprise CI/CD ownership |
| Linux | Mac container runtime and a prepared `systemd` agent | Operate the agent on an approved Linux VM/host | Fleet administration |
| Virtualization | Architecture can run inside a VM | Use a centre-provided VMware/Hyper-V or other approved hypervisor | VMware certification or data-centre operation |
| IaC/configuration | Deployment steps are documented | Add Terraform/OpenTofu and Ansible/Puppet against a disposable lab | Large-scale provisioning |
| Security | Localhost-only defaults and security boundary | Add image, dependency, secret and policy checks | Security clearance or enterprise threat ownership |

The public repository deliberately does not contain the private Personal OS, CVs, credentials, permit records, email data or centre logs.

## Why these tools recur in current Swiss roles

The matrix below is a **representative current scan**, checked 19 September 2026. It combines official live role pages with the user-supplied role descriptions. It is not an exhaustive list of every DevOps vacancy and it does not turn a tool mention into a qualification.

| Capability | Repeated tools or concepts | Seen in current evidence | Priority for the six-week project |
|---|---|---|---|
| Linux and systems | Linux, shell, TCP/IP, DNS, HTTP(S), processes, filesystems, permissions, cgroups/namespaces | CERN, Proton, adesso, Pascal Dietrich | **Now** - explain and diagnose the existing stack |
| Containers and orchestration | Docker, Kubernetes, Helm, OpenShift, container lifecycle | CERN, Proton, adesso, PostFinance, Pascal Dietrich | **Now/next** - Docker now; Kubernetes in an approved lab |
| Configuration and IaC | Terraform/OpenTofu, Ansible, Puppet/OpenVox, Pulumi | CERN, Proton, adesso, PostFinance, Pascal Dietrich | **Next** - provision only disposable lab resources |
| CI/CD and GitOps | Git, GitLab CI, GitHub Actions, Jenkins, ArgoCD, release validation | CERN, Proton, adesso, PostFinance | **Now/next** - GitHub Actions now; GitLab/ArgoCD with centre access |
| Observability | Prometheus, Grafana, Alertmanager, logs, traces, ELK/Kibana, Splunk | CERN, Proton, adesso, PostFinance | **Now/next** - Prometheus/Grafana now; log platform only if approved |
| Security in delivery | image hardening, dependency/SAST/DAST scanning, SBOM, secret scanning, IAM/RBAC, network policy, encryption | Proton, adesso, PostFinance, Pascal Dietrich; DevSecOps wording in supplied roles | **Next** - add non-production gates and explain failures |
| Platform networking | routing, load balancing, firewalls, HAProxy/Envoy/Traefik, Cilium, ACLs, DNS | Proton Application Edge/Network, PostFinance, Pascal Dietrich | **Next** - local TCP boundary first; centre network only with permission |
| Virtualization and compute | VMware/Hyper-V, QEMU/KVM, bare metal, OpenStack, Talos, GPU/HPC | IP4IT, CERN large-scale compute, supplied senior SRE roles | **Next** - use the centre's approved hypervisor; no claim of expertise beforehand |
| Reliability practice | SLI/SLO/error budget, on-call, incident response, RCA, postmortem, backup/restore, DR | All SRE/platform descriptions | **Now** - the current lab already supports a controlled drill |
| Advanced domain tools | Vault, ArgoCD, Cilium, eBPF/ftrace/strace, HTCondor, SLURM, VHDL/Verilog, InfiniBand | CERN, Proton, PostFinance, supplied senior compute/DAQ roles | **Later** - only when a real supervised requirement exists |

### The minimum employable learning order

Do not try to install every tool in the matrix. The sequence is:

1. Linux and TCP/IP diagnosis.
2. Docker image lifecycle and safe configuration.
3. Kubernetes objects, health probes, resource limits and rollback.
4. Git-based CI gates and IaC/configuration basics.
5. Prometheus/Grafana plus logs and alert reasoning.
6. DevSecOps controls: least privilege, image/dependency scanning, SBOM, secret scanning and network policy.
7. Incident response, SLOs and a reproducible handover.

## The Secure Edge Platform demonstration

### Current Mac path

The existing repository is the working baseline:

```text
C++ device simulator -> Python/FastAPI control plane -> dashboard
                                      |
                                      +-> Prometheus -> Grafana
                                      +-> GitHub Actions build and tests
```

Run it with `make setup`, `make up`, `make demo` and `./scripts/verify.sh`. The current demo injects a safe device fault, shows readiness failing while liveness remains available, then verifies a fresh sample after recovery.

### Supervised business-centre path

Only after IP4IT/Geneva Business News approves the host and network:

```text
Mac workstation
  -> approved VMware/Hyper-V Linux VM or physical Linux host
  -> Kubernetes namespace (or a centre-approved equivalent)
  -> Docker image for control plane and agent
  -> GitLab CI or existing approved CI
  -> Prometheus/Grafana + approved logs
  -> SLO, alert, incident record and restore evidence
```

On an Apple-silicon Mac, do not promise VMware or a nested Kubernetes cluster until the centre confirms the supported architecture. Docker/Colima is the current local baseline; the centre may provide a compatible x86/ARM VM, physical host or shared lab cluster. The correct choice is an approved environment, not a particular vendor logo.

### The seven proof points

1. **Build:** a clean clone builds the C++ simulator and installs the Python requirements.
2. **Secure delivery:** CI runs tests, validates configuration, scans the image/dependencies where the centre approves a scanner, and produces an SBOM or records why the scanner is unavailable.
3. **Deploy:** the same image runs locally and in the approved Kubernetes/VM lab with non-root configuration, health probes and resource limits.
4. **Observe:** Prometheus/Grafana show attempts, successes, failures, latency and the current readiness state; logs identify the same incident.
5. **Protect:** secrets stay outside Git, access is least-privilege, and only approved ports/data are exposed.
6. **Recover:** a controlled fault is detected, diagnosed, recovered and verified with a new sample; the postmortem names cause and prevention.
7. **Handover:** another person can reproduce the runbook without the author improvising.

## Money-first work package (lawful and non-guaranteed)

The first potential paid service is not “senior SRE consulting.” It is a bounded, authorized **non-production reliability and secure-deployment review** for a small organization, school lab or open-source project.

### Deliverables

- a reproducible Docker or centre-approved Kubernetes deployment;
- a short architecture and trust-boundary diagram;
- CI checks for tests, configuration and approved security scans;
- a baseline dashboard and one SLI/SLO worksheet;
- one controlled failure drill and a recovery runbook;
- a prioritized findings note with evidence and next steps;
- a handover call or written walk-through.

### Strict guardrails

- Obtain written authorization and a scope before touching any client system.
- Use a non-production environment and synthetic or explicitly approved data.
- Do not promise uptime, compliance, penetration testing, a Swiss permit or a job outcome.
- Confirm the user's Swiss work authorization and contracting/tax position before accepting payment.
- Keep the public portfolio sanitized; never publish client identifiers, secrets, internal topology or personal data.

This package can demonstrate useful work quickly, but it is a proposal for a lawful service, not a guaranteed daily wage. Until authorization and a real client agreement exist, it remains a training exercise.

## Six-week Geneva Business School / IP4IT plan

| Week | Build and study | Evidence to show | Business-centre request | Definition of done |
|---|---|---|---|---|
| 1 - baseline | Rebuild the Mac lab; Linux/TCP diagnosis; read Chapters 1-5 of the PDF | Verified output, architecture diagram, current-vs-gap matrix | Name one supervisor and the approved lab boundary | You can start, inspect, fault, recover and stop the stack without prompts |
| 2 - container/platform | Write a Docker image review; model Kubernetes Deployment/Service/Probe/ConfigMap; use a disposable VM if supplied | Manifest review, resource/probe rationale, rollback note | Confirm VMware/Hyper-V or an alternative supported host | A clean clone deploys to the approved non-production environment |
| 3 - delivery/security | Add CI checks; review Dockerfile; run approved dependency/image scan; produce SBOM; record exceptions | CI log, scan result, threat-boundary note | Confirm whether GitLab CI, scanner and registry are available | The pipeline fails closed on a reproducible high-severity demo issue |
| 4 - observability/incident | Add alert reasoning, logs and an SLO window; run three safe failures | Timeline, impact, diagnosis, recovery and postmortem for each | Choose Prometheus/Grafana plus the centre's approved log tool | Another person can locate the same failure from evidence |
| 5 - automation/recovery | Add Terraform/OpenTofu or Ansible/Puppet only for disposable resources; test backup/restore | IaC plan, idempotence check, restore report | Review permissions and data-retention boundary | Restore is validated separately and no secret enters Git |
| 6 - handover/career | Present the project, score the skills matrix, tailor one truthful CV and apply to fit-gated roles | Five-minute demo, reviewer score, final runbook and application evidence | Ask for a written description of placement/authorization options | A second operator reproduces the demo and all gaps are explicit |

### One-hour daily loop

1. State the outcome, risk and evidence expected.
2. Make one controlled change or run one drill.
3. Run tests and inspect logs/metrics.
4. Record the result, limitation and remaining gap.
5. Commit only reviewed, sanitized project changes.

## One-page proposal to present

> **Project:** Secure Edge Platform - a six-week DevSecOps/SRE evidence lab.
>
> **Objective:** turn an existing C++/Python hardware-aware service into a reproducible, secure and observable platform that another participant can operate.
>
> **What I bring now:** a completed CS MSc, a working public C++/Python/Docker/Prometheus/Grafana lab, Linux/networking fundamentals and a documented failure/recovery drill.
>
> **What I need from the centre:** one approved Linux host or VM, an isolated lab network, one reviewer for one hour per week, and confirmation of which centre tools (VMware/Hyper-V, Kubernetes, GitLab, Kibana/ELK, Nagios, GLPI or Wireshark) may be used.
>
> **Output after six weeks:** a sanitized public repository, CI evidence, a container/Kubernetes or VM deployment, an SLO and dashboard, three incident records, a restore drill and a five-minute handover another participant can reproduce.
>
> **Employment relevance:** the evidence maps to recurring platform/SRE requirements in Geneva and Switzerland. It does not claim seniority, production access, a placement, permanent conversion or work authorization. I will apply only to roles whose experience, nationality and authorization gates I can truthfully satisfy.

### Exact opening demonstration

“I have a working hardware-aware reliability lab. It polls a C++ device, validates telemetry in Python, exposes metrics, detects a controlled fault and verifies recovery. I want to use one approved Linux VM or physical host here to add Kubernetes/container security, a CI gate, an SLO and an independent handover. I am asking for a supervised six-week evidence project, not permission to touch production.”

## Role and technology mapping

### CERN DevOps Engineer for Large Scale Compute

The supplied LinkedIn link resolves to CERN role `IT-CD-CC-2026-223-GRAE`. CERN's official page lists a Geneva hybrid 24-month role closing **8 October 2026 at 23:59 Geneva time**, with a maximum of two years of professional experience since graduation, a Bachelor's or Master's degree, CERN Member/Associate Member nationality, and no prior CERN fellow/graduate contract. It names Linux, Python/Go, Git, Puppet/OpenVox, Ansible, Terraform/OpenTofu, containers, CI/CD and optional HTCondor/SLURM/kueue. It also mentions a 400k+ core fleet, OpenStack and Kubernetes.

The current lab directly supports the Linux/Python/Git/containers/CI and reliability narrative. It does **not** yet prove Puppet/OpenVox, OpenStack, Kubernetes operations at scale, batch/HPC administration or the eligibility gates. Apply only after checking those gates and tailoring the CV truthfully.

### CERN CMS DAQ software role

The supplied CMS/TCDS description adds Python, modern C++, REST/web interfaces, hardware/system programming, CI/CD and optional VHDL/Verilog. The project is a useful software-and-operations foundation, but it is not FPGA, DAQ or accelerator experience.

### Proton, adesso, PostFinance and private-cloud postings

- **Proton Infrastructure Systems:** Kubernetes, VM orchestration, bare metal, Linux internals/networking, Terraform/Ansible/Puppet, Python, HA/distributed systems and Prometheus/Grafana.
- **Proton Application Edge/Network:** TCP/IP, DNS, HTTP(S), Kubernetes, Terraform/Ansible, Python/Go/Rust, proxies and network controls.
- **adesso SRE:** IaC, Linux/networking, AWS/GCP/Azure or hybrid, Python/Bash/Go, Jenkins/GitLab/GitHub Actions, Docker/Kubernetes, Prometheus/Grafana/ELK and incident/on-call practice; official Swiss openings are currently listed in Basel, Bern, St Gallen and Zurich rather than Geneva.
- **PostFinance Kubernetes Engineer (user-supplied listing):** on-prem Kubernetes/Talos, Linux, Go controllers, Grafana/Splunk, Terraform, GitLab CI/CD, GitOps, Cilium, ArgoCD, Vault and AWS EKS. The exact LinkedIn listing was not independently verified on PostFinance's official jobs site, so its current status is **UNKNOWN**.
- **Pascal Dietrich Platform/DevOps (user-supplied listing):** sovereign on-prem private cloud, Linux, L2/L3 networking, Docker/Kubernetes, virtualization, Terraform/Ansible, CI/CD, observability, IAM, encryption and hardening; the listing says Swiss citizenship is required.

These mappings show why the project emphasizes transferable fundamentals before advanced product names. A tool is useful only when you can explain its failure modes, security boundary and operational evidence.

## Senior-role ladder: what six weeks can and cannot do

| Level | Evidence this project can support | Evidence it cannot create in six weeks |
|---|---|---|
| Internship / early-career | reproducible build, containers, basic CI, metrics, runbook, safe incident drill | organizational production ownership |
| Junior platform/SRE | supervised Linux host, health probes, SLO and restore evidence | independent on-call for critical services |
| Mid-level | repeated operations, IaC idempotence, alert quality, RCA and reviews | years of production incidents and change authority |
| Senior / staff | architecture decisions, fleet economics, mentoring, risk ownership and deep domain expertise | seniority by reading or copying a stack |

Use this ladder in interviews. It lets you discuss senior technologies without claiming senior experience.

## Sources and recheck gates

Primary sources checked 19 September 2026:

- [CERN DevOps Engineer for Large Scale Compute](https://careers.cern/jobs/devops-engineer-for-large-scale-compute/)
- [CERN Online Software Developer / CMS DAQ](https://careers.cern/jobs/ep-cms-tdq-2026-153-grap/)
- [CERN Information Technologies vacancies](https://careers.cern/explore-careers/information-technologies/)
- [Proton SRE Infrastructure Systems](https://job-boards.eu.greenhouse.io/proton/jobs/4848439101?gh_src=6b341c62teu)
- [Proton SRE Application Edge](https://job-boards.greenhouse.io/proton/jobs/4612377101)
- [Proton current jobs](https://job-boards.greenhouse.io/proton)
- [adesso Senior SRE](https://www.adesso.ch/de_ch/jobs-karriere/unsere-stellenangebote/Senior-Site-Reliability-Engineer-all-genders-de-j2900.html)
- [adesso Swiss vacancies](https://www.adesso.ch/de_ch/jobs-karriere/unsere-stellenangebote/)
- [PostFinance current technology role evidence](https://jobs.postfinance.ch/offene-stellen/product-owner-continuous-integration-plattformen-w-m-d/4c9a3fca-6325-4494-86e5-19452b333564)
- [IP4IT](https://www.ip4it.ch/) and [Geneva Business News IT](https://genevabusinessnews.ch/it/)
- [OCSTAT Geneva employment](https://statistique.ge.ch/actualites/welcome.asp?Actudomaine=06_02&aaaa1=2026&aaaa2=2026&actu=6016&mm1=05/01&mm2=12/31&num=0)
- [ICT workforce requirements through 2033](https://www.ict-berufsbildung.ch/resources/BSS-Schlussbericht-ICT-Bildungsbedarf-2033-2025-09_09.pdf)

Recheck immediately before applying or presenting: vacancy status and deadline, the centre's equipment and supervision, the user's permit/activity authorization, and whether any client work is legally permitted. No application, registration, purchase, message or external system change is performed by this playbook.
