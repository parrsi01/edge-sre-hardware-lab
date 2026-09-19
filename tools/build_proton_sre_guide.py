#!/usr/bin/env python3
"""Build a validity-first beginner guide to Proton SRE work in Geneva."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer

from build_sre_beginner_book import (
    AMBER,
    BODY,
    BOX,
    CODE,
    GREEN,
    H1,
    H2,
    LINE,
    MINT,
    NAVY,
    PALE,
    SMALL,
    WARN,
    ChapterMarker,
    bullets,
    code,
    exercise,
    p,
    table,
    title,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parents[1] / "output" / "pdf" / "PROTON_SRE_GENEVA_BEGINNER_GUIDE.pdf"


def proton_header_footer(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(16 * mm, height - 13 * mm, width - 16 * mm, height - 13 * mm)
    canvas.setFillColor(colors.HexColor("#52625D"))
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(16 * mm, height - 9 * mm, "PROTON SRE IN GENEVA - BEGINNER GUIDE")
    canvas.drawRightString(width - 16 * mm, height - 9 * mm, "VALIDITY FIRST")
    canvas.line(16 * mm, 12 * mm, width - 16 * mm, 12 * mm)
    canvas.drawString(16 * mm, 7 * mm, "Checked 19 September 2026 - role facts may change")
    canvas.drawRightString(width - 16 * mm, 7 * mm, f"{doc.page}")
    canvas.restoreState()


def proton_cover(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, height, stroke=0, fill=1)
    canvas.setFillColor(GREEN)
    canvas.rect(0, 0, 18 * mm, height, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 28)
    canvas.drawString(32 * mm, height - 55 * mm, "PROTON SRE")
    canvas.setFont("Helvetica-Bold", 18)
    canvas.setFillColor(colors.HexColor("#A7F0D1"))
    canvas.drawString(32 * mm, height - 70 * mm, "GENEVA BEGINNER GUIDE")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 11.5)
    text = canvas.beginText(32 * mm, height - 94 * mm)
    text.setLeading(16)
    for line in (
        "Learn the basic components before learning the product names.",
        "Decode Infrastructure Systems and Application Edge SRE work.",
        "Separate current evidence from skills that still need supervision.",
    ):
        text.textLine(line)
    canvas.drawText(text)
    canvas.setFillColor(colors.HexColor("#173B37"))
    canvas.roundRect(32 * mm, height - 178 * mm, 146 * mm, 55 * mm, 4 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(40 * mm, height - 143 * mm, "START WITH THE TRUTH")
    canvas.setFont("Helvetica", 9.7)
    text = canvas.beginText(40 * mm, height - 155 * mm)
    text.setLeading(14)
    for line in (
        "A local lab is not Proton production experience.",
        "A role description is not a qualification certificate.",
        "A six-week plan creates evidence; it does not guarantee a job.",
    ):
        text.textLine(line)
    canvas.drawText(text)
    canvas.setFillColor(colors.HexColor("#A7F0D1"))
    canvas.setFont("Helvetica-Bold", 9.5)
    canvas.drawString(32 * mm, 35 * mm, "SIMON PARRIS  |  19 SEPTEMBER 2026")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(32 * mm, 27 * mm, "Learning guide, not an employment or work-authorization claim")
    canvas.restoreState()


def chapter(story, number, name, promise, content):
    story.extend(title(number, name, promise))
    story.extend(content)
    story.append(PageBreak())


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=18 * mm,
        bottomMargin=17 * mm,
        title="Proton SRE in Geneva - Beginner Guide",
        author="Simon Parris",
        subject="Validity-first SRE fundamentals and Proton Geneva role decoder",
    )
    body_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
    cover_frame = Frame(0, 0, A4[0], A4[1], leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="cover")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=cover_frame, onPage=proton_cover, autoNextPageTemplate="body"),
        PageTemplate(id="body", frames=body_frame, onPage=proton_header_footer),
    ])

    story = [Spacer(1, 1), PageBreak()]

    chapter(story, "0", "Scope and validity", "Use this book to understand Proton SRE work, not to inflate a CV or assume eligibility.", [
        p("This guide uses Proton's official job pages checked 19 September 2026. It explains the role's systems and vocabulary in beginner language. It does not claim that the user has Proton experience, production Kubernetes experience, on-call history, a Swiss permit or a job offer."),
        table([
            ["Fact", "Meaning"],
            ["Official role description", "Evidence of what Proton asks for in that vacancy"],
            ["Public project", "Evidence that code and documentation are accessible"],
            ["Local demonstration", "Evidence limited to the tested local environment"],
            ["Supervised lab proof", "A stronger claim only after an approved reviewer observes it"],
            ["Employment", "A real contract, not a guide, project or course"],
        ], [57*mm, 120*mm]),
        p("The correct learning order is: definitions -> Linux/networking -> containers -> Kubernetes -> CI/IaC -> observability/security -> incident response. Start with the current local lab; add Proton-like tools only when the environment is approved and the result can be reproduced." , WARN),
        exercise("Can this PDF honestly say you are a Proton SRE?", "No. It can help you understand the work and prepare evidence. A job title requires a real employment relationship."),
    ])

    chapter(story, "1", "What an SRE does", "An SRE keeps a useful service reliable by combining software engineering and operations.", [
        p("A service can be running yet unusable. SRE work makes useful behaviour measurable, failures visible and recovery repeatable."),
        table([
            ["Question", "SRE answer"],
            ["What is the user trying to do?", "Define the important operation and its success condition"],
            ["How good is it?", "Measure an SLI and agree an SLO"],
            ["What failed?", "Use metrics, logs, traces and layered diagnosis"],
            ["What should happen now?", "Follow a runbook and preserve evidence"],
            ["How do we improve?", "Automate safe repetition and write a postmortem"],
        ], [63*mm, 114*mm]),
        p("SRE is not only system administration, monitoring, cloud branding or a Kubernetes certificate. Production SRE also includes change risk, communication, access, escalation, capacity, security and the consequences of being wrong."),
        exercise("Why should an SRE care about a failed health check if the process is still running?", "Because liveness and useful readiness are different. Keeping a process alive can preserve diagnostics while readiness prevents traffic from being sent to an instance that cannot complete its function."),
    ])

    chapter(story, "2", "Proton's Geneva production context", "Translate the role description into systems you can reason about.", [
        p("Proton's Infrastructure Systems role is listed for Geneva and Paris. The team provides Kubernetes, VM orchestration and bare-metal provisioning, plus DNS, DHCP, source of truth and monitoring. The description refers to thousands of servers, automation for 99.95%+ uptime, monitoring/alerting, security and on-call troubleshooting."),
        table([
            ["Proton phrase", "What it means for a beginner"],
            ["Kubernetes platform", "A control system that schedules and replaces container workloads"],
            ["VM orchestration", "Automated lifecycle and resource management for virtual machines"],
            ["Bare metal", "Physical servers whose hardware and provisioning are part of the work"],
            ["DNS/DHCP", "Naming and network configuration that many services depend on"],
            ["Source of truth", "A trusted record of intended infrastructure state"],
            ["99.95%+ uptime", "A very high target requiring measurement, redundancy and change discipline"],
            ["On-call", "A staffed response process with escalation, access and runbooks"],
        ], [53*mm, 124*mm]),
        p("Proton's Application Edge role is related but different: it focuses on traffic management and load balancing in hybrid on-premises/cloud environments. It names TCP/IP, DNS, HTTP/HTTPS, HAProxy/Envoy/Traefik, Kubernetes, Python/Rust/Go, recovery and security."),
        p("These descriptions are production context. They are not a promise that a beginner can perform every responsibility after a course." , WARN),
    ])

    chapter(story, "3", "Core definitions", "Memorize the concepts that remain useful even when product names change.", [
        table([
            ["Term", "Definition"],
            ["Availability", "Successful intended operations divided by total intended operations in a stated window"],
            ["Reliability", "Ability to perform the intended function for a stated time and conditions"],
            ["Latency", "Time taken for an operation; use a defined percentile or summary"],
            ["SLI", "A measured indicator of a user-relevant outcome"],
            ["SLO", "A target for an SLI over a defined window"],
            ["SLA", "An external contractual promise with consequences"],
            ["Error budget", "Permitted unreliability under an SLO"],
            ["Observability", "Understanding internal state from metrics, logs and traces"],
            ["Toil", "Repetitive manual work with little lasting value"],
            ["Runbook", "Steps for a known operational task or failure"],
            ["Postmortem", "Evidence-based record of impact, timeline, cause and prevention"],
        ], [42*mm, 135*mm]),
        p("Example", H2),
        p("If 22 of 23 scheduled polls succeed during a drill, the measured availability is 22/23 = 95.652% for that short window. It is not a production SLO, and it must not be presented without the numerator, denominator and window." , BOX),
        exercise("What is an SLO for a Proton-like telemetry service?", "For example: 'At least 99% of scheduled telemetry polls succeed during each 30-minute supervised exercise.' The target is only meaningful after the operation and window are agreed."),
    ])

    chapter(story, "4", "The infrastructure path", "Follow a request from a name to an application and back to evidence.", [
        code("user -> DNS -> load balancer/proxy -> Kubernetes Service -> Pod\n                              |                         |\n                              +-> metrics/logs/alerts   +-> dependency/data store"),
        table([
            ["Layer", "Beginner question"],
            ["DNS", "Does the name resolve to the intended destination?"],
            ["Network", "Can packets take the permitted route?"],
            ["Load balancer", "Is traffic distributed and is the backend considered ready?"],
            ["Kubernetes", "Is the desired number of Pods running and healthy?"],
            ["Application", "Can the useful operation succeed?"],
            ["Dependency", "Can the application reach the service or data it needs?"],
            ["Observability", "Can an operator prove what happened?"],
        ], [44*mm, 133*mm]),
        p("The lowest failing layer is often the fastest path to diagnosis. Do not restart everything first: preserve evidence, identify impact, then take the smallest safe recovery action."),
    ])

    chapter(story, "5", "Linux, containers and Kubernetes", "Understand the building blocks before attempting a cluster.", [
        p("Linux provides processes, filesystems, permissions, networking and the kernel. A container is an isolated process sharing the host kernel; it is not a VM. An image is a package of an application and runtime filesystem. Docker builds/runs images and Compose connects several services for a lab."),
        table([
            ["Kubernetes object", "Purpose"],
            ["Node", "Machine or VM that runs workloads"],
            ["Pod", "Smallest deployable unit, usually one main container"],
            ["Deployment", "Declares desired stateless Pods and manages rollout/replacement"],
            ["Service", "Stable network identity for a group of Pods"],
            ["Readiness probe", "Whether an instance should receive traffic"],
            ["Liveness probe", "Whether an instance should keep running"],
            ["Resource request/limit", "Scheduling expectation and maximum resource use"],
            ["RBAC/NetworkPolicy", "API permissions and Pod traffic restrictions"],
        ], [49*mm, 128*mm]),
        p("Beginner sequence: deploy one image; add probes; add limits; use a restricted service account; observe the rollout; perform a safe rollback. Only use a disposable or explicitly approved environment."),
        exercise("Why can readiness fail while liveness remains healthy?", "The process can be running while a dependency or useful operation is unavailable. Readiness protects traffic; liveness protects process recovery."),
    ])

    chapter(story, "6", "IaC, CI/CD, observability and security", "Treat every change as a reviewed, measurable and reversible operation.", [
        table([
            ["Area", "Core idea", "Example tools in Proton-style roles"],
            ["IaC", "Declare infrastructure and review a plan", "Terraform/OpenTofu"],
            ["Configuration", "Keep machines in intended state", "Ansible, Puppet"],
            ["CI/CD", "Build, test, scan and release changes", "GitLab CI, GitHub Actions, Jenkins"],
            ["GitOps", "Git is desired state; an agent reconciles it", "ArgoCD"],
            ["Metrics", "Collect numeric signals", "Prometheus"],
            ["Dashboards", "Help people inspect trends and state", "Grafana"],
            ["Logs", "Search event records", "ELK/Kibana or an approved equivalent"],
            ["Security", "Reduce attack and change risk", "IAM/RBAC, scans, hardening, network policy"],
        ], [33*mm, 75*mm, 69*mm]),
        p("A sensible security gate checks source/dependencies, builds a minimal non-root image, scans it, creates an SBOM, checks secrets and policy, then deploys only to an approved environment. A missing check is an explicit UNKNOWN or a fail-closed block, not an invented pass." , WARN),
        p("The current lab already demonstrates GitHub Actions, Docker Compose, Prometheus and Grafana. GitLab, Terraform, Ansible, Kubernetes and production security tooling remain next-stage evidence."),
    ])

    chapter(story, "7", "Map the current lab to Proton", "Use the lab as a learning bridge and label every boundary.", [
        table([
            ["Proton theme", "Current lab evidence", "Still required"],
            ["Python automation", "FastAPI polling, validation and tests", "Reviewed operational script on approved host"],
            ["Metrics", "Prometheus counters and Grafana", "Alert owner, threshold, routing and runbook"],
            ["Linux/networking", "TCP protocol and local containers", "Approved Linux host, route/link diagnosis"],
            ["Kubernetes", "Compose service graph", "Deployment, Service, probes, limits and rollback"],
            ["Infrastructure automation", "Documented setup", "Idempotent Terraform/OpenTofu or Ansible plan"],
            ["Incident response", "Controlled fault/recovery", "Three witnessed drills and postmortems"],
            ["Production scale", "Not demonstrated", "Do not claim thousands of servers or Proton systems"],
        ], [39*mm, 65*mm, 73*mm]),
        p("Truthful project statement", H2),
        p("Built a local hardware-aware reliability lab with C++, Python/FastAPI, Docker Compose, Prometheus and Grafana; implemented a controlled fault and recovery drill with automated tests and documented operational boundaries." , BOX),
        p("Do not write 'Site Reliability Engineer at Proton', 'production Kubernetes' or '99.95% uptime' unless those statements are separately true and documented." , WARN),
    ])

    chapter(story, "8", "Six-week practice plan", "Create early-career evidence without pretending six weeks creates seniority.", [
        table([
            ["Week", "Practice", "Definition of done"],
            ["1", "Definitions, current Mac lab, SLI/SLO explanation", "Run and explain the fault/recovery drill"],
            ["2", "Approved Linux VM/host, processes, ports, routes, systemd", "Agent runs within an approved boundary"],
            ["3", "Docker review and Kubernetes probes/limits", "Disposable/approved deployment and rollback"],
            ["4", "CI, dependency/image scan, SBOM and secret checks", "A safe introduced issue is caught before deploy"],
            ["5", "SLO, logs/metrics and three incident drills", "Timeline, impact, cause, recovery and prevention"],
            ["6", "Restore, handover, skills matrix and fit-gated application", "Another person reproduces the runbook"],
        ], [18*mm, 82*mm, 77*mm]),
        p("Ask the business centre for one approved host or VM, an isolated lab network, one reviewer for one hour each week and confirmation of available Kubernetes, VMware/Hyper-V, GitLab, logs and security tools. IP4IT's public information establishes programme alignment only; equipment, supervision, funding, placement and authorization remain UNKNOWN until confirmed."),
        exercise("What is the first action today?", "Run the current lab's `make demo`, explain the user impact, record the result, then read Sections 1-7 aloud. Do not install a production tool or touch a shared network as a substitute for understanding."),
    ])

    chapter(story, "9", "Glossary exercises and interview answers", "Use short, precise answers instead of tool-name lists.", [
        table([
            ["Question", "Good beginner answer"],
            ["What is SRE?", "Software engineering applied to operating reliable services."],
            ["What is DevSecOps?", "Security controls integrated into build, deploy and operate workflows."],
            ["What is a readiness probe?", "Whether an instance should receive traffic."],
            ["What is observability?", "Using signals to understand internal state."],
            ["What is an error budget?", "The permitted unreliability under an SLO."],
            ["What is a runbook?", "Steps for a known task or failure."],
            ["What do you currently prove?", "A local C++/Python/Docker/Prometheus/Grafana lab and a controlled recovery drill."],
            ["What do you not yet prove?", "Proton production systems, fleet scale, independent on-call or production Kubernetes."],
        ], [52*mm, 125*mm]),
        p("Proton's application process asks about location, authorization, salary expectations and management responsibility. Answer using your actual facts. Never use a training plan to fill a work-history field." , WARN),
    ])

    chapter(story, "10", "Sources and recheck gates", "Use primary sources and recheck volatile role details before applying.", [
        *bullets([
            "<link href='https://job-boards.eu.greenhouse.io/proton/jobs/4848439101?gh_src=6b341c62teu'>Proton SRE Infrastructure Systems</link>: Kubernetes, VM orchestration, bare metal, Linux, IaC, Python, HA, Prometheus/Grafana, security and on-call context.",
            "<link href='https://job-boards.greenhouse.io/proton/jobs/4612377101'>Proton SRE Application Edge</link>: traffic management, networking, load balancing, Kubernetes, automation and security.",
            "<link href='https://proton.me/careers'>Proton careers</link>: Geneva headquarters and current employer context.",
            "<link href='https://careers.cern/jobs/devops-engineer-for-large-scale-compute/'>CERN DevOps Engineer for Large Scale Compute</link>: adjacent Geneva early-career stack.",
            "<link href='https://www.ip4it.ch/'>IP4IT</link> and <link href='https://genevabusinessnews.ch/it/'>Geneva Business News IT</link>: programme alignment only.",
            "<link href='https://sre.google/sre-book/table-of-contents/'>Google SRE book</link>: general SRE concepts.",
        ], SMALL),
        p("Recheck before any consequential action: the vacancy is still open, the exact requirements and deadline, Proton's application fields, the user's Swiss work authorization, and the centre's actual equipment/supervision. This guide does not submit an application, send a message, register, purchase or begin paid work." , WARN),
        p("Final validity statement", H2),
        p("This PDF is a beginner explanation and an evidence plan. It is sensible if it helps you understand and safely demonstrate the basics. It becomes stronger only when a real reviewer observes reproducible work in an approved environment." , BOX),
    ])

    if isinstance(story[-1], PageBreak):
        story.pop()
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()

