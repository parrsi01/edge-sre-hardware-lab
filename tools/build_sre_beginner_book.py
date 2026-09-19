#!/usr/bin/env python3
"""Create a practical, source-backed SRE beginner book for the IP4IT project."""

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parents[1] / "output" / "pdf" / "SRE_BEGINNER_GUIDE_IP4IT_GENEVA.pdf"

NAVY = colors.HexColor("#102826")
GREEN = colors.HexColor("#087A55")
MINT = colors.HexColor("#DFF6EB")
PALE = colors.HexColor("#F4F8F6")
BLUE = colors.HexColor("#E8F1FA")
AMBER = colors.HexColor("#FFF2CF")
RED = colors.HexColor("#A13B32")
GREY = colors.HexColor("#52625D")
LINE = colors.HexColor("#B9CDC5")


class ChapterMarker(Flowable):
    def __init__(self, number):
        super().__init__()
        self.number = str(number)
        self.width = 16 * mm
        self.height = 16 * mm

    def draw(self):
        self.canv.setFillColor(GREEN)
        self.canv.circle(8 * mm, 8 * mm, 7 * mm, stroke=0, fill=1)
        self.canv.setFillColor(colors.white)
        self.canv.setFont("Helvetica-Bold", 11)
        self.canv.drawCentredString(8 * mm, 6.4 * mm, self.number)


def header_footer(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(16 * mm, height - 13 * mm, width - 16 * mm, height - 13 * mm)
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(16 * mm, height - 9 * mm, "SRE FOR GENEVA - EDGE SRE HARDWARE LAB")
    canvas.drawRightString(width - 16 * mm, height - 9 * mm, "SIMON PARRIS")
    canvas.line(16 * mm, 12 * mm, width - 16 * mm, 12 * mm)
    canvas.drawString(16 * mm, 7 * mm, "Practical IP4IT training edition - 19 September 2026")
    canvas.drawRightString(width - 16 * mm, 7 * mm, f"{doc.page}")
    canvas.restoreState()


def cover(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, height, stroke=0, fill=1)
    canvas.setFillColor(GREEN)
    canvas.rect(0, 0, 18 * mm, height, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 30)
    canvas.drawString(32 * mm, height - 55 * mm, "SRE FOR GENEVA")
    canvas.setFont("Helvetica-Bold", 19)
    canvas.setFillColor(colors.HexColor("#A7F0D1"))
    canvas.drawString(32 * mm, height - 70 * mm, "A BEGINNER'S PROJECT GUIDE")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 12)
    text = canvas.beginText(32 * mm, height - 94 * mm)
    text.setLeading(17)
    for line in (
        "Build, operate, break and recover a small service",
        "using Linux, Python, C++, Docker, Prometheus and Grafana.",
        "Designed for an in-person IP4IT / Geneva Business News lab.",
    ):
        text.textLine(line)
    canvas.drawText(text)

    canvas.setFillColor(colors.HexColor("#173B37"))
    canvas.roundRect(32 * mm, height - 168 * mm, 146 * mm, 46 * mm, 4 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(40 * mm, height - 137 * mm, "YOUR STARTING POINT")
    canvas.setFont("Helvetica", 10)
    text = canvas.beginText(40 * mm, height - 148 * mm)
    text.setLeading(14)
    for line in (
        "CS MSc and distributed-systems foundation",
        "Python / Linux / networking / full-stack experience to validate",
        "Mac lab ready now; supervised physical-host step next",
    ):
        text.textLine(line)
    canvas.drawText(text)

    canvas.setFillColor(colors.HexColor("#A7F0D1"))
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(32 * mm, 35 * mm, "SIMON PARRIS  |  PRACTICAL EDITION  |  19 SEPTEMBER 2026")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(32 * mm, 27 * mm, "Local project evidence, not a claim of production or CERN experience")
    canvas.restoreState()


styles = getSampleStyleSheet()
BODY = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=10.2, leading=14.2, textColor=NAVY, spaceAfter=3 * mm)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8.7, leading=11.5, spaceAfter=2 * mm)
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=23, leading=27, textColor=NAVY, spaceAfter=5 * mm)
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=14.5, leading=18, textColor=GREEN, spaceBefore=3 * mm, spaceAfter=2.5 * mm)
H3 = ParagraphStyle("H3", parent=styles["Heading3"], fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=NAVY, spaceBefore=2 * mm, spaceAfter=1.5 * mm)
CODE = ParagraphStyle("Code", parent=SMALL, fontName="Courier", fontSize=7.9, leading=10.7, leftIndent=4 * mm, rightIndent=4 * mm, backColor=colors.HexColor("#EEF3F1"), borderPadding=6, spaceAfter=3 * mm)
BOX = ParagraphStyle("Box", parent=BODY, backColor=MINT, borderColor=GREEN, borderWidth=0.8, borderPadding=8, spaceBefore=1 * mm, spaceAfter=3 * mm)
WARN = ParagraphStyle("Warn", parent=BODY, backColor=AMBER, borderColor=colors.HexColor("#C68600"), borderWidth=0.8, borderPadding=8, spaceBefore=1 * mm, spaceAfter=3 * mm)
CAPTION = ParagraphStyle("Caption", parent=SMALL, textColor=GREY, alignment=TA_CENTER, spaceAfter=3 * mm)


def p(text, style=BODY):
    return Paragraph(text, style)


def code(text):
    return Paragraph(escape(text).replace("\n", "<br/>"), CODE)


def title(number, name, promise):
    return [
        Table([[ChapterMarker(number), p(name, H1)]], colWidths=[20 * mm, 150 * mm], style=[("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]),
        p(promise, BOX),
    ]


def bullets(items, style=BODY):
    return [p(f"<bullet>&bull;</bullet>{item}", ParagraphStyle(f"bullet-{i}-{id(items)}", parent=style, leftIndent=5 * mm, firstLineIndent=-4 * mm, bulletIndent=0)) for i, item in enumerate(items)]


def exercise(question, answer):
    return KeepTogether([
        p("Exercise", H3),
        p(question, WARN),
        p("Worked answer", H3),
        p(answer, BOX),
    ])


def table(rows, widths, header=True):
    header_style = ParagraphStyle("TableHeader", parent=SMALL, textColor=colors.white)
    data = []
    for row_index, row in enumerate(rows):
        cell_style = header_style if header and row_index == 0 else SMALL
        data.append([p(str(cell), cell_style) for cell in row])
    t = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        commands += [("BACKGROUND", (0, 0), (-1, 0), NAVY), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white)]
    t.setStyle(TableStyle(commands))
    return t


def chapter(story, number, name, promise, content):
    story.extend(title(number, name, promise))
    story.extend(content)
    story.append(PageBreak())


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=16 * mm, rightMargin=16 * mm,
        topMargin=18 * mm, bottomMargin=17 * mm,
        title="SRE for Geneva - A Beginner's Project Guide",
        author="Simon Parris",
        subject="Practical SRE project guide for IP4IT in Geneva",
    )
    body_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="body")
    cover_frame = Frame(0, 0, A4[0], A4[1], leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0, id="cover")
    doc.addPageTemplates([
        PageTemplate(id="cover", frames=cover_frame, onPage=cover, autoNextPageTemplate="body"),
        PageTemplate(id="body", frames=body_frame, onPage=header_footer),
    ])

    story = [Spacer(1, 1), PageBreak()]

    chapter(story, "0", "How to use this book", "Read Chapters 1-5 today, run the lab, then use one chapter per training session at IP4IT.", [
        p("This book is written for your actual starting point: a completed computer-science master's degree, a distributed-systems foundation and user-reported exposure to Python, Linux, networking and full-stack development. Those are assets, but an employer needs observable proof that you can operate a service, not only build one."),
        p("The project is public at <link href='https://github.com/parrsi01/edge-sre-hardware-lab'>github.com/parrsi01/edge-sre-hardware-lab</link>. It runs locally on a Mac today. At IP4IT, the goal is to replace the simulated device with an approved physical Linux host and have another person reproduce your runbook."),
        table([
            ["Reading mode", "Action", "Definition of done"],
            ["Today", "Chapters 1-5, D, E and the five-minute demo", "You can explain the stack, money boundary and recover the injected fault"],
            ["At IP4IT", "Chapters 6-17 with a supervisor", "Evidence is independently observed and recorded"],
            ["Applications", "Chapters 18-19", "Every CV claim points to a file, test or witnessed exercise"],
        ], [32*mm, 70*mm, 75*mm]),
        p("Truth rule", H2),
        p("The current system is a local simulation. Do not call it production, a data-centre deployment, FPGA work or CERN experience. The physical-host exercise becomes true only after it is completed and verified." , WARN),
    ])

    chapter(story, "1", "What SRE actually is", "SRE is software engineering applied to operations: define reliability, measure it, automate repeatable work and learn from failure.", [
        p("A developer asks whether the feature works. An operator asks whether the service stays useful over time. An SRE combines both views. You write code, but you also decide what 'healthy' means, observe the system, plan for failure and reduce manual work."),
        table([
            ["DevOps idea", "SRE implementation in this lab"],
            ["Shared ownership", "The repository contains service code, deployment and runbook together"],
            ["Automation", "One command starts the complete stack; CI repeats tests"],
            ["Measurement", "Prometheus records polls, failures, availability and telemetry"],
            ["Learning from failure", "A safe device fault is injected and recovered"],
            ["Reduce toil", "Scripts replace repeated manual checks"],
        ], [52*mm, 125*mm]),
        p("The Google SRE material organizes the field around risk, SLOs, toil, monitoring, automation, release engineering, troubleshooting, incident response and postmortems. This book narrows those ideas to a small system you can fully understand."),
        exercise("Someone says, 'SRE is just system administration with a new name.' What is missing?", "System administration is part of the work, but SRE also uses software engineering, measurable service objectives, automated testing and repeatable incident learning. The distinguishing evidence is not the title; it is how the service is defined, measured and improved."),
    ])

    chapter(story, "M", "Read the employment evidence correctly", "The labour-market case is Swiss and cross-industry; it is not evidence of a Geneva-specific SRE hiring boom.", [
        p("Current Geneva evidence", H2),
        table([
            ["Measure", "Latest verified result", "Interpretation"],
            ["Geneva FTE employment, Q2 2026", "+1.0% quarter-on-quarter", "Overall seasonally adjusted growth; excludes specified activities"],
            ["Geneva FTE employment, 2024", "+0.8% to 363,071", "Broad structural series across the canton"],
            ["Geneva secondary sector, 2024", "+0.8%", "Positive, but not a measure of IT occupations"],
            ["Geneva information/communication, 2024", "-1.7%", "Contradicts a simple local IT-boom claim"],
        ], [52*mm, 43*mm, 82*mm]),
        p("OCSTAT reports economic branches, not the Site Reliability Engineer occupation. No authoritative Geneva SRE growth percentage was found. Therefore, this guide does not invent one." , WARN),
        p("Swiss ICT outlook", H2),
        p("The 2025 ICT-Berufsbildung Schweiz study starts from about 266,000 ICT workers and projects 61,600 additional ICT positions through 2033 from economic growth and structural change. That is approximately 23.2% of the 2024 base across the forecast period, not an annual rate. It also projects 67,000 replacement needs, producing 128,600 gross personnel needs. The largest occupational components are software developers (46,200) and systems analysts (17,600)."),
        p("More than two-thirds of Swiss ICT specialists work outside the core ICT industry. This supports portable reliability skills for finance, education, public administration, life sciences, logistics and industry. It does not guarantee a vacancy, interview, permit or junior-level hire."),
        exercise("Can you write 'Geneva SRE jobs increased 23.2%' on a proposal?", "No. The 23.2% is a calculation from a national forecast of additional ICT positions through 2033 divided by the 2024 Swiss ICT workforce base. It is neither Geneva-specific, SRE-specific nor annual. Use the exact scope and period."),
    ])

    chapter(story, "D", "DevSecOps and the current Swiss SRE stack", "Use security controls inside delivery and reliability work, then prove the result with a safe lab exercise.", [
        p("The supplied Proton, CERN, adesso, PostFinance and private-cloud descriptions repeat a practical stack: Linux and networking; Docker and Kubernetes; Terraform or OpenTofu; Ansible, Puppet or similar configuration management; Git and CI/CD; Prometheus/Grafana and logs; security controls; virtualization or bare metal; and incident response. The exact job postings differ, so this is a representative scan checked 19 September 2026, not an exhaustive inventory of every vacancy."),
        table([
            ["Capability", "Common tools", "Your evidence boundary"],
            ["Linux and networking", "Linux, shell, TCP/IP, DNS, HTTP(S), processes, permissions, cgroups/namespaces", "Current container lab and TCP protocol; approved Linux host still needed"],
            ["Containers", "Docker, Kubernetes, Helm, OpenShift", "Docker Compose is demonstrated; Kubernetes is a supervised next step"],
            ["IaC and config", "Terraform/OpenTofu, Ansible, Puppet/OpenVox, Pulumi", "Documented deployment today; disposable-lab exercise next"],
            ["CI/CD and GitOps", "Git, GitLab CI, GitHub Actions, Jenkins, ArgoCD", "GitHub Actions passes now; centre-approved GitLab/ArgoCD later"],
            ["Observability", "Prometheus, Grafana, Alertmanager, ELK/Kibana, Splunk, logs/traces", "Prometheus/Grafana now; log platform only if approved"],
            ["DevSecOps", "image/dependency scanning, SBOM, secret scanning, IAM/RBAC, policy, encryption", "Security boundary is documented; scanner gates are next"],
            ["Virtualization", "VMware/Hyper-V, QEMU/KVM, bare metal, OpenStack, Talos", "Use the centre's approved host; do not claim vendor expertise yet"],
            ["Reliability", "SLI/SLO, error budget, on-call, RCA, postmortem, backup/restore", "Controlled fault and recovery are already demonstrated"],
        ], [37*mm, 66*mm, 74*mm]),
        p("Minimum learning order", H2),
        p("Learn the failure boundary before the product name: Linux/TCP/IP diagnosis, Docker image lifecycle, Kubernetes health probes and limits, Git-based CI, IaC idempotence, metrics/logs, least privilege and incident handover. Do not install every named tool at once. Complexity is not evidence."),
        p("Mac versus centre", H2),
        p("The Mac path uses Docker/Compose, Python/FastAPI, C++, Prometheus, Grafana and GitHub Actions. The centre path may provide VMware or Hyper-V, an approved Linux VM or physical host, Kubernetes, GitLab CI, Terraform/OpenTofu, Ansible/Puppet and a log platform. On Apple silicon, confirm the centre's supported VM architecture before promising nested Kubernetes or VMware. The approved environment matters more than the brand."),
        exercise("Does mentioning Kubernetes, VMware or Terraform on a CV prove SRE ability?", "No. A truthful claim requires a reproducible deployment, a stated boundary, an observed failure and evidence of recovery or review. This guide labels centre-only tools as next-stage work until that evidence exists."),
    ])

    chapter(story, "E", "Secure Edge Platform: a six-week money-first project", "Present one narrow, supervised project that connects the current lab to the work employers buy and hire for.", [
        p("Project outcome", H2),
        p("Turn the existing edge lab into a Secure Edge Platform: a Dockerized, observable service with CI security gates, an approved Kubernetes or VM deployment, an explicit SLO, a controlled incident and a handover another operator can reproduce. This is a portfolio and training proposal. It is not a promise of a job, daily income, seniority, CERN experience or work authorization."),
        code("Mac workstation\n  -> Docker/Compose baseline\n  -> approved VMware/Hyper-V Linux VM or physical host\n  -> Kubernetes namespace or centre-approved equivalent\n  -> GitHub/GitLab CI gates\n  -> Prometheus/Grafana and approved logs\n  -> SLO, incident record and restore evidence"),
        table([
            ["Week", "Work", "Evidence and definition of done"],
            ["1 - baseline", "Rebuild the Mac lab; practise Linux/TCP diagnosis", "Clean clone, architecture diagram and verbal five-minute demo"],
            ["2 - platform", "Review Docker image; model Kubernetes Deployment, Service, probes and limits", "Approved VM/cluster deployment or a reviewed, runnable manifest set"],
            ["3 - delivery/security", "CI tests, config validation, approved image/dependency scan and SBOM", "Pipeline catches a deliberately introduced non-production issue"],
            ["4 - observe/respond", "SLO window, alert reasoning, logs and three safe failures", "Timeline, impact, diagnosis, recovery and postmortem for each"],
            ["5 - automate/recover", "Terraform/OpenTofu or Ansible/Puppet on disposable resources; restore", "Idempotent plan, separate restore and no secrets in Git"],
            ["6 - handover", "Presentation, skills matrix, truthful CV bullet and fit-gated applications", "Second operator reproduces the runbook and gaps are explicit"],
        ], [28*mm, 70*mm, 79*mm]),
        p("Potential lawful service package", H2),
        p("The first possible paid work is a bounded, authorized non-production reliability and secure-deployment review for a small organization, school lab or open-source project. Deliverables are a reproducible Docker/Kubernetes deployment, trust-boundary diagram, CI checks, baseline dashboard, SLI/SLO worksheet, one controlled failure drill, recovery runbook and handover note. Confirm Swiss work authorization, contracting and tax requirements before accepting payment. Never touch a client's system without written scope and authorization." , WARN),
        p("Business-centre opening", H2),
        p("\"I have a working hardware-aware reliability lab. It polls a C++ device, validates telemetry in Python, exposes metrics, detects a controlled fault and verifies recovery. I want to use one approved Linux VM or physical host here to add container security, a CI gate, an SLO and an independent handover. I am asking for a supervised six-week evidence project, not permission to touch production.\"", BOX),
        p("Role mapping", H2),
        table([
            ["Current role evidence", "Repeated technology", "What this project supports / does not support"],
            ["CERN DevOps Engineer for Large Scale Compute", "Linux, Python/Go, Git, Puppet/OpenVox, Ansible, Terraform/OpenTofu, containers, CI/CD, Kubernetes, OpenStack, HTCondor/SLURM", "Supports Linux/Python/Git/containers/CI story; does not yet prove fleet scale, Puppet/OpenVox, OpenStack, batch/HPC or eligibility"],
            ["CERN CMS DAQ software", "Python, modern C++, REST/web UI, hardware interaction, CI/CD, VHDL/Verilog asset", "Supports software/operations foundation; does not prove FPGA, DAQ or accelerator work"],
            ["Proton and private-cloud SRE", "Kubernetes, VMs/bare metal, Linux, Terraform/Ansible/Puppet, Prometheus/Grafana, networking", "Supports the vocabulary and a small recovery demo; production/on-call scale remains unknown"],
            ["adesso/PostFinance platform roles", "Cloud/hybrid, GitLab/Jenkins, Docker/Kubernetes, IaC, logs, GitOps, security", "Supports a staged learning plan; seniority, language, location and experience gates remain"],
        ], [42*mm, 60*mm, 75*mm]),
        p("The supplied LinkedIn link resolves to CERN's official DevOps Engineer for Large Scale Compute role (IT-CD-CC-2026-223-GRAE), Geneva hybrid, closing 8 October 2026 at 23:59 Geneva time. The official page states a maximum of two years of professional experience since graduation, a Bachelor's or Master's degree, CERN Member/Associate Member nationality and no previous CERN fellow/graduate contract. Check those gates before applying."),
        exercise("What is today's money-first action?", "Run the existing demo, save the verification result, read this chapter aloud, and ask the centre for one approved host, network boundary and reviewer. A client or employer should see evidence of safe operation before you discuss a paid scope."),
    ])

    chapter(story, "2", "Your existing hardware and the one optional purchase", "Start with what is already connected. Only buy a physical host if IP4IT cannot lend one.", [
        p("The project is deliberately usable before buying hardware. Begin with a Mac that can run Docker-compatible containers; add an independent Linux host only after the centre confirms the device and network."),
        table([
            ["Asset", "Minimum requirement", "Use in this project"],
            ["Mac", "Docker-compatible Compose, Git, make, Python and CMake", "Runs the simulated lab and acts as operator workstation"],
            ["External drive", "Optional; approved and encrypted if it stores anything sensitive", "Non-sensitive backup and restore drills; not a server"],
            ["Ethernet adapter/cable", "Optional until the physical-host phase", "Connect an approved host on an approved lab network"],
            ["Physical Linux host", "Borrowed mini-PC, old laptop or Raspberry Pi", "Independent boot, network, systemd service and hardware evidence"],
        ], [37*mm, 68*mm, 72*mm]),
        p("Storage rule", H2),
        p("A public repository is not a backup of private data. Keep credentials, CVs, personal records and real organizational logs out of this project. If an external drive is used for sensitive material, verify its encryption and recovery method separately." , WARN),
        p("Optional purchase", H2),
        p("The best-value complete device is the Raspberry Pi 5 4 GB Starter Kit: Pi 5, active-cooled case, official 27 W power supply and 32 GB microSD. Pi-Shop listed it at CHF 146.90 with immediate dispatch. Four gigabytes is enough for this lab. A local Digitec 8 GB board was CHF 179 and required separate accessories; pickup in Geneva and Zurich was shown for Monday, 21 September, not same-day."),
        exercise("Can the external SSD replace a Raspberry Pi for the physical-host phase?", "No. Storage cannot run its own operating system, network stack or service after the Mac is unavailable. Use the SSD for backup and restore evidence. Use a borrowed old laptop, mini-PC or Raspberry Pi as the independent Linux host."),
    ])

    chapter(story, "3", "The system you will operate", "Understand the path from hardware-like telemetry to an operator decision.", [
        table([
            ["C++ device", "TCP/JSON", "Python API", "Prometheus", "Grafana/web"],
            ["Creates readings and faults", "Carries one-line commands and responses", "Polls, validates, stores and reports", "Scrapes time-series metrics", "Shows state and recovery evidence"],
        ], [31*mm, 32*mm, 40*mm, 34*mm, 40*mm]),
        p("The C++ process is intentionally small. It accepts <font name='Courier'>READ</font>, <font name='Courier'>PING</font>, <font name='Courier'>SET_FAIL ON</font> and <font name='Courier'>SET_FAIL OFF</font>. The Python service polls every two seconds. If telemetry is valid, it stores a sample and increments success. If the device reports a fault or cannot be reached, readiness fails but the control API remains alive so an operator can diagnose it."),
        p("Why separate liveness and readiness?", H2),
        p("Liveness answers, 'Is the process running?' Readiness answers, 'Can it currently serve its intended function?' Restarting every unhealthy dependency can create loops. In this lab, the API remains alive during a device fault while readiness accurately reports that the service is not ready."),
        exercise("During a simulated device fault, should the web API disappear completely?", "No. The operator still needs status, metrics and recovery controls. The API stays live, while <font name='Courier'>/readyz</font> reports failure until healthy device telemetry resumes."),
    ])

    chapter(story, "4", "Run it today on the Mac", "By the end of this chapter you will have a working dashboard and a recorded fault-recovery result.", [
        p("Open Terminal and run:"),
        code("git clone https://github.com/parrsi01/edge-sre-hardware-lab.git\ncd edge-sre-hardware-lab\nmake setup\nmake up\nopen http://localhost:8000"),
        p("Then run the scripted drill:"),
        code("make demo"),
        p("Expected sequence", H2),
        table([
            ["Step", "Expected observation"],
            ["Healthy", "connected=true; telemetry is updating"],
            ["Fault injected", "device_status=fault; readiness fails; liveness stays available"],
            ["Recovery", "new successful sample appears; readiness returns"],
            ["Evidence", "availability reflects the failed poll instead of hiding it"],
        ], [38*mm, 139*mm]),
        p("The verified run on 19 September 2026 passed four Python tests, the C++ self-test, API/Prometheus/Grafana checks and the recovery drill. Availability became 95.652% because 22 of 23 polls were successful. That short-window value is evidence of the test, not a production reliability claim."),
        exercise("Why did availability fall sharply after one brief failure?", "The sample window was tiny: one failed poll out of 23 is about 4.35% failure. Over a long window, one failed poll would have less effect. Always state the numerator, denominator and time window."),
    ])

    chapter(story, "5", "Learn the repository", "Be able to point to each component instead of saying that AI built it.", [
        table([
            ["Path", "Responsibility", "Question you must answer"],
            ["device-simulator/src/main.cpp", "Protocol, telemetry and fault state", "How is a client command parsed and answered?"],
            ["control-api/app/main.py", "Polling, state, routes and metrics", "What happens when a poll fails?"],
            ["control-api/tests/", "Protocol tests", "Which invalid inputs are rejected?"],
            ["docker-compose.yml", "Service graph and health checks", "Which service waits for which dependency?"],
            ["observability/", "Prometheus and Grafana", "Where does the dashboard get data?"],
            ["hardware-agent/", "Physical Linux replacement", "Which values are real and which may be null?"],
            ["scripts/", "Operator workflow", "How do you verify readiness before demoing?"],
        ], [53*mm, 62*mm, 62*mm]),
        p("Study method", H2),
        p("For every file: read it, explain it aloud, predict one failure, then confirm the behavior. Change nothing until you can reproduce the baseline. An interview demonstration is strongest when you can diagnose a new fault without relying on a memorized script."),
        exercise("What is the weakest honest answer to 'Did you build this yourself with AI?'", "Do not hide AI assistance. Say: 'I used AI as an implementation assistant, then I ran the builds and tests, fixed packaging and readiness issues, and I can explain and operate every component. Here is the verification evidence and the next independently supervised step.'"),
    ])

    chapter(story, "G", "Use the public GitHub repository", "The public repository synchronizes project code, tests, guides and evidence boundaries without exposing the private Personal OS.", [
        p("Public repository", H2),
        p("Open <link href='https://github.com/parrsi01/edge-sre-hardware-lab'>github.com/parrsi01/edge-sre-hardware-lab</link>. The README is the front door; <font name='Courier'>TRAINING_GUIDE.md</font> describes the work; <font name='Courier'>SKILLS_MATRIX.md</font> distinguishes current proof from future supervised proof; <font name='Courier'>SECURITY.md</font> defines the authorized boundary; and <font name='Courier'>docs/</font> powers the public case-study site."),
        table([
            ["Action", "Command", "What to verify"],
            ["Get a fresh copy", "git clone https://github.com/parrsi01/edge-sre-hardware-lab.git", "The README and all source directories are present"],
            ["See local changes", "git status", "Only intended files are listed"],
            ["Inspect a change", "git diff", "No secret, personal path or unsupported claim"],
            ["Record a reviewed change", "git add FILE; git commit", "Commit states the evidence-producing outcome"],
            ["Synchronize", "git push", "GitHub shows the same commit and CI result"],
        ], [38*mm, 59*mm, 80*mm]),
        p("Private material does not belong here", H2),
        p("Do not synchronize passwords, tokens, Gmail data, CVs, permit records, private Personal OS reports, internal IP addresses or centre logs. 'All tools and skills' means every tool and skill artifact for this lab—not the entire Mac or private account state." , WARN),
        exercise("A file is useful for your job search but contains a home address. Should it be added?", "No. Extract only the non-sensitive technical evidence needed for this project. Keep personal documents in private storage and link only to the public project."),
    ])

    chapter(story, "6", "Metrics without confusion", "Use counters for accumulated events and gauges for current state.", [
        p("Prometheus stores time series: numeric samples over time, identified by metric names and labels. The official guidance recommends measuring attempts, failures and latency for online services, and warns that unbounded labels create too many time series."),
        table([
            ["Type", "Meaning", "Lab example"],
            ["Counter", "Only increases, except reset on restart", "poll attempts and successful polls"],
            ["Gauge", "Current value can rise or fall", "device connected state or temperature"],
            ["Histogram", "Counts observations in buckets", "future poll-latency distribution"],
            ["Summary", "Client-side quantiles/count/sum", "not needed for this first lab"],
        ], [34*mm, 70*mm, 73*mm]),
        p("Useful queries", H2),
        code("edge_sre_device_connected\nedge_sre_polls_total\nedge_sre_poll_success_total\n100 * edge_sre_poll_success_total / edge_sre_polls_total"),
        p("A real SRE would normally calculate rates over a defined window and handle process restarts. The lab's direct ratio is deliberately readable for a first demonstration."),
        exercise("Temperature changes from 39 C to 42 C and back. Counter or gauge? What about total failed polls?", "Temperature is a gauge because it moves in both directions. Total failed polls is a counter because each failure adds one; derive a failure rate over a time window when alerting."),
    ])

    chapter(story, "7", "SLIs, SLOs, SLAs and error budgets", "Define what users care about before choosing alerts.", [
        table([
            ["Term", "Plain meaning", "Lab definition"],
            ["SLI", "Measured indicator", "successful polls divided by total polls"],
            ["SLO", "Internal reliability target", "99% successful polls during the agreed exercise window"],
            ["SLA", "External contractual promise with consequences", "none; this training lab has no SLA"],
            ["Error budget", "Permitted unreliability under the SLO", "1% of polls may fail under a 99% SLO"],
        ], [26*mm, 66*mm, 85*mm]),
        p("An SLO is only useful when its user, indicator, target and window are explicit. '99% reliable' is incomplete. 'At least 99% of scheduled device polls succeed during each 30-minute supervised drill' is measurable."),
        p("Availability arithmetic", H2),
        p("At a 99% SLO over 10,000 polls, the error budget is 100 failed polls. At 99.9%, it is 10. Do not mix poll availability with user-request availability without explaining the difference."),
        exercise("A 30-day service has a 99% availability target. What simple time budget does 1% represent?", "Thirty days is 43,200 minutes. One percent is 432 minutes, or 7 hours 12 minutes. This is a simplified time-based budget; request-based SLOs require request counts instead."),
    ])

    chapter(story, "8", "Incident response", "Respond in a predictable order: observe, contain, diagnose, recover, verify and learn.", [
        table([
            ["Phase", "Operator action in the lab"],
            ["Detect", "Dashboard and readiness show the device fault"],
            ["Declare", "State start time, impact and owner aloud"],
            ["Contain", "Do not make unrelated changes; preserve logs"],
            ["Diagnose", "Check device status, API logs and container health"],
            ["Recover", "Disable the controlled fault or restart only the failed component"],
            ["Verify", "Wait for a new sample and readiness; check metrics"],
            ["Learn", "Write cause, timeline, recovery and one prevention action"],
        ], [35*mm, 142*mm]),
        p("Runbook command sequence", H2),
        code("make status\nmake logs\ncurl -i http://localhost:8000/healthz\ncurl -i http://localhost:8000/readyz\nmake demo"),
        p("Do not randomly restart everything first. That can erase evidence and may restore service without teaching you why it failed."),
        exercise("The API is live, readiness fails and the device container is healthy. What do you check next?", "Read the API status and logs for a protocol-level fault. A healthy process can still return an application fault. In this lab, check <font name='Courier'>device_status</font> and <font name='Courier'>last_error</font>, then use the documented recovery control."),
    ])

    chapter(story, "9", "Troubleshooting from layers", "Find the lowest failing layer before changing anything.", [
        table([
            ["Layer", "Question", "Evidence"],
            ["Power/host", "Is the machine up?", "LEDs, console, uptime"],
            ["Link", "Is Ethernet physically connected?", "link state and interface status"],
            ["Network", "Does it have an address and route?", "ip address, route, ping where allowed"],
            ["Transport", "Is the TCP port listening?", "ss/netstat and connection attempt"],
            ["Application", "Does the protocol return valid data?", "READ/PING response and logs"],
            ["Service", "Can the user objective be completed?", "readiness and fresh telemetry"],
        ], [30*mm, 61*mm, 86*mm]),
        p("Minimal diagnostic discipline", H2),
        p("Record the exact symptom and timestamp. Reproduce once safely. Compare healthy versus failing evidence. Change one variable. Verify the user-visible result. Document the command and result. Escalate when authorization, safety or scope is unclear."),
        exercise("A dashboard is blank. Name three different possible layers.", "Browser/UI: JavaScript failed. API: the status endpoint is unavailable. Device: no fresh telemetry exists. Start from the browser request, check API health, then move down to the device; do not assume the first visible symptom identifies the root cause."),
    ])

    chapter(story, "10", "Containers and reproducibility", "Containers make the lab repeatable; they do not remove the need to understand Linux and networking.", [
        p("Docker Compose declares four services, their images, environment, health checks, ports, volumes and startup relationships. Colima provides the Linux virtual-machine runtime on this Mac. The host binds user-facing ports to <font name='Courier'>127.0.0.1</font>, so the lab is not exposed to the local network by default."),
        table([
            ["Service", "Internal dependency", "Host port"],
            ["device", "none", "none"],
            ["control-api", "healthy device", "127.0.0.1:8000"],
            ["prometheus", "healthy control API", "127.0.0.1:9090"],
            ["grafana", "Prometheus", "127.0.0.1:3000"],
        ], [42*mm, 73*mm, 62*mm]),
        p("Build and verification", H2),
        code("docker compose config --quiet\ndocker compose build\ndocker compose run --rm --no-deps control-api pytest -q\ndocker compose run --rm --no-deps device --self-test"),
        exercise("Why bind dashboards to 127.0.0.1 instead of 0.0.0.0 for the local demo?", "127.0.0.1 limits access to the Mac itself. This fails closed while authentication is intentionally absent. Network access should be added only with an approved threat model and access control."),
    ])

    chapter(story, "11", "Toil and automation", "Automate work that is manual, repetitive, predictable and safe to encode.", [
        p("Toil is not simply 'work you dislike.' In SRE, it is operational work that is manual, repetitive, automatable, tactical and grows with the service. The setup, readiness and demo scripts remove repeated keystrokes while keeping the operator's decision visible."),
        table([
            ["Manual step", "Automation", "Human still decides"],
            ["Check every dependency", "wait-ready.sh", "whether the observed state is acceptable"],
            ["Run builds and tests", "verify.sh and CI", "whether a failure blocks release"],
            ["Inject and recover fault", "demo.sh", "whether this exercise is safe and authorized"],
            ["Start all services", "Docker Compose", "configuration and exposure policy"],
        ], [51*mm, 55*mm, 71*mm]),
        p("Good automation is idempotent where practical, returns a meaningful exit code, emits useful errors and fails closed. A green script is evidence only if it actually tests the required outcome."),
        exercise("Should a script automatically restart a failed service forever?", "Not by default. Limited restart policies can improve availability, but infinite restarts can hide a persistent defect and consume resources. Add bounded retries, observability and an escalation path."),
    ])

    chapter(story, "12", "Move from simulator to a real Linux host", "The physical step is a protocol replacement, not a rewrite of the whole system.", [
        p("First ask IP4IT for an approved Linux mini-PC, old laptop, Raspberry Pi or workstation on an isolated lab network. If none is available, the Raspberry Pi 5 4 GB kit is the recommended purchase. Do not connect an unmanaged personal device to a production or office network without approval."),
        p("Physical sequence", H2),
        table([
            ["Step", "Action", "Evidence"],
            ["1", "Install supported Linux and record version", "OS and kernel output"],
            ["2", "Create a restricted service account", "account and file ownership"],
            ["3", "Enable key-based SSH on the approved network", "successful login and disabled unnecessary access"],
            ["4", "Install hardware-agent/edge_agent.py as a systemd service", "enabled service and logs"],
            ["5", "Point the control API at the host", "fresh real-host samples"],
            ["6", "Disconnect link or stop service under supervision", "detected incident and measured recovery"],
            ["7", "Have another participant follow the runbook", "handover result and corrections"],
        ], [15*mm, 92*mm, 70*mm]),
        p("The agent reports real Linux thermal data only when the kernel exposes it. Unavailable values remain null. Never fabricate voltage or sensor readings."),
        exercise("What converts this from a software demo into hardware-aware operational evidence?", "A separately powered Linux host, real network link, supervised service deployment, a physical or process failure, measured recovery and an independent witness. Owning a Raspberry Pi alone is not evidence."),
    ])

    chapter(story, "13", "Use the external SSD correctly", "Turn the existing drive into recovery evidence without treating it as a server.", [
        p("An approved external drive can hold a versioned, non-sensitive project backup. Exclude secrets and personal data. The safest first exercise backs up only this public repository."),
        p("Backup drill - review the destination before running", H2),
        code("backup_root=${EDGE_SRE_BACKUP_ROOT:?Set EDGE_SRE_BACKUP_ROOT to an approved destination}\nstamp=$(date +%Y%m%d-%H%M%S)\ndest=\"$backup_root/$stamp\"\nmkdir -p \"$dest\"\nrsync -a --exclude '.git' --exclude '__pycache__' ./ \"$dest/\"\nfind \"$dest\" -maxdepth 2 -type f | sort"),
        p("Restore verification", H2),
        p("Do not restore over the live project. Restore into a new temporary directory, compare checksums or file lists, run the tests from the restored copy, then delete the temporary copy only after review."),
        code("restore_dir=$(mktemp -d)\nrsync -a \"$dest/\" \"$restore_dir/\"\ncd \"$restore_dir\"\ndocker compose config --quiet\necho \"Restored copy: $restore_dir\""),
        exercise("A backup command returned exit code 0. Is recovery proven?", "No. A backup is only proven after a restore to a separate location and validation of the required files or service. Record the restore result and time."),
    ])

    chapter(story, "14", "Security and safe lab boundaries", "Reliability includes preventing your own tools from creating a new incident.", [
        table([
            ["Control", "Current design", "Physical-lab requirement"],
            ["Network exposure", "host ports on 127.0.0.1", "approved isolated network and documented firewall"],
            ["Privileges", "containers run non-root where defined", "restricted service user; no shared admin account"],
            ["Secrets", "none required", "do not commit passwords, tokens or Wi-Fi credentials"],
            ["Data", "synthetic telemetry", "collect only approved host metrics"],
            ["Faults", "simulated command", "supervised and reversible; never on production"],
            ["Publishing", "public code uses synthetic data", "centre approves every centre name, image or internal detail"],
        ], [37*mm, 65*mm, 75*mm]),
        p("Never packet-capture other people's traffic. Wireshark exercises at IP4IT must use your own lab traffic or an explicitly provided capture. Never scan networks or hosts without written authorization." , WARN),
        exercise("Can you publish a screenshot showing the centre's internal IP addresses?", "Not without explicit approval. Use synthetic addresses or crop/redact internal identifiers. Public evidence should prove your method without exposing the centre."),
    ])

    chapter(story, "15", "Six-week IP4IT execution plan", "Each week ends with observable evidence and a supervisor decision.", [
        table([
            ["Week", "Work", "Definition of done"],
            ["1", "Baseline, architecture, Linux/network assessment", "Rebuild and explain the Mac lab without prompts"],
            ["2", "Deploy agent to approved physical Linux host", "systemd service survives reboot and emits real available metrics"],
            ["3", "Run three controlled failures", "symptom, diagnosis, action and recovery recorded"],
            ["4", "Security and configuration", "restricted account, approved exposure, no secrets in repo"],
            ["5", "SLO and recovery", "window defined; backup and restore drill passes"],
            ["6", "Independent handover and interview", "another participant runs the guide; reviewer scores evidence"],
        ], [15*mm, 77*mm, 85*mm]),
        p("Daily 60-minute pattern", H2),
        table([
            ["Minutes", "Activity"],
            ["0-10", "State the objective and expected evidence"],
            ["10-35", "Perform one lab change or drill"],
            ["35-45", "Run tests and inspect metrics/logs"],
            ["45-55", "Write the result and one remaining gap"],
            ["55-60", "Commit locally or prepare review; choose next action"],
        ], [30*mm, 147*mm]),
        p("Ask IP4IT to classify every skill as performed independently, performed with help, or not yet demonstrated. A factual record is more valuable than a vague certificate."),
    ])

    chapter(story, "16", "Your first IP4IT meeting", "Show a working system first, then ask for a narrow supervised physical extension.", [
        p("Opening script", H2),
        p('"I have prepared a small hardware-aware reliability lab. It polls a C++ device, validates telemetry in Python, exposes metrics, detects a controlled fault and recovers. The local version works. I would like to replace the simulator with one approved Linux host here, practise network and service failures, and produce a runbook another participant can follow."', BOX),
        p("Five-minute demonstration", H2),
        table([
            ["Time", "Show", "Say"],
            ["0:00", "Architecture", "One sentence per component"],
            ["0:45", "Healthy dashboard", "State current SLI and its small window"],
            ["1:30", "Inject fault", "Explain liveness versus readiness"],
            ["2:30", "Logs and Grafana", "Point to the causal evidence"],
            ["3:30", "Recover", "Verify a fresh sample, not only a green light"],
            ["4:15", "Repository/tests", "State limits and physical next step"],
        ], [20*mm, 54*mm, 103*mm]),
        p("Questions to obtain decisions", H2),
        *bullets([
            "Which approved Linux device and isolated network may I use?",
            "Who can review one hour per week and witness the final drill?",
            "Which existing tools - GLPI, OCS, Nagios or Wireshark - should the project integrate with, if any?",
            "What data and screenshots may be used in a public portfolio?",
            "What participation, funding and work-authorization framework applies?",
        ], SMALL),
        exercise("What is the meeting's definition of done?", "A named supervisor, one approved host, an allowed network boundary, a six-week schedule, a decision on public evidence, and a clear answer on participation/funding/authorization. Interest without these decisions is not a project start."),
    ])

    chapter(story, "17", "Connect to IP4IT's actual programme", "Use the centre's published tools only where they serve the project.", [
        p("The Geneva Business News IT page describes daily practice across support, development, systems and networking, a weekly IT session, technical presentations, labs, and work with GLPI, OCS, Nagios and Wireshark. That supports the project's direction, but it does not prove that a place, supervisor, device, funding or specific installation is available."),
        table([
            ["Published pillar", "Project contribution", "Do not assume"],
            ["Support", "runbook, incident ticket and handover", "access to real user tickets"],
            ["Development", "Python API, C++ device and tests", "production deployment"],
            ["Systems", "Linux service, logs, backup and restore", "administrator privileges"],
            ["Networking", "TCP protocol, link failure and diagnosis", "permission to inspect the office network"],
            ["Tools", "possible ticket, inventory, monitoring or packet-analysis integration", "that every named tool is currently installed"],
        ], [30*mm, 72*mm, 75*mm]),
        p("Best integration sequence", H2),
        p("First make the physical host work. Second create one GLPI ticket for a controlled incident if their GLPI is available. Third compare the lab's Prometheus alert with their approved Nagios process. Fourth inspect only your own lab TCP exchange in Wireshark. OCS integration is optional and should follow the centre's actual inventory architecture."),
        exercise("Why not install all four named tools immediately?", "Tools are not the objective. Reliability evidence is. Installing unused software adds complexity and security risk. Integrate the smallest centre-approved tool that improves a real workflow."),
    ])

    chapter(story, "18", "Turn the project into employment evidence", "Apply for roles using verified outcomes, not a promise that the project qualifies you for everything.", [
        p("Best-aligned role families", H2),
        table([
            ["Role family", "Evidence from this lab", "Remaining common gap"],
            ["Junior SRE / platform", "health checks, metrics, incident drill, automation", "production/on-call experience"],
            ["DevOps / cloud", "containers, CI, repeatable deployment", "cloud/IaC at organizational scale"],
            ["Linux / infrastructure", "systemd host, network diagnosis, restore", "enterprise fleet and identity tooling"],
            ["Control software", "C++, TCP, Python, hardware boundary", "real device/DAQ/FPGA domain"],
            ["Application support", "runbook, logs, incident reproduction", "specific business application knowledge"],
        ], [38*mm, 72*mm, 67*mm]),
        p("Truthful CV bullet after physical completion", H2),
        p("Built and operated a four-service hardware-aware reliability lab using C++, Python/FastAPI, Docker Compose, Prometheus and Grafana; deployed a telemetry agent to an approved Linux host, documented three controlled incidents and validated recovery through an independent runbook exercise.", BOX),
        p("Until the physical stage is complete, remove the phrase 'deployed ... to an approved Linux host' and keep the work under Projects, not Employment."),
        p("CERN and other employer references", H2),
        p("Hardware-aware software roles often combine Python, modern C++, device interaction, REST/web interfaces and CI/CD. This lab addresses those technical themes, but it cannot replace a vacancy's formal experience, nationality, degree or domain requirements. Verify every live vacancy independently before applying."),
        exercise("Where should this appear on your CV today?", "Under Projects as 'Edge SRE Hardware Lab - local simulation.' Link to the reviewed repository only after publication. Do not list IP4IT as employment unless a real employment relationship exists."),
    ])

    chapter(story, "19", "Assessment and next action", "Finish with proof that you can operate and explain the system without hiding its limits.", [
        table([
            ["Capability", "Pass condition"],
            ["Architecture", "Draw all five components and explain each boundary"],
            ["Operation", "Start, inspect and stop the stack from the guide"],
            ["Failure", "Detect, diagnose and recover a surprise fault"],
            ["Measurement", "Calculate an SLI with real numerator, denominator and window"],
            ["Linux", "Run agent as a restricted systemd service on approved hardware"],
            ["Networking", "Explain link, IP, TCP and application layers using evidence"],
            ["Recovery", "Restore a separate copy and validate it"],
            ["Communication", "Deliver the five-minute demo and truthful limits"],
            ["Handover", "Another person succeeds using your runbook"],
        ], [46*mm, 131*mm]),
        p("Today's exact action", H2),
        p("1. Open the dashboard. 2. Run <font name='Courier'>make demo</font>. 3. Read Chapters 1-5. 4. Explain the architecture aloud without reading. 5. Write one paragraph describing what failed and how recovery was verified."),
        p("Definition of done: you can reproduce the demo, state the difference between liveness and readiness, identify the numerator and denominator of availability, and name the one physical-host decision IP4IT must make." , BOX),
        p("No purchase is required today. Ask for a loaned approved host first. If none is available, recheck the Raspberry Pi 5 4 GB kit's total price and delivery immediately before purchasing. No order has been made."),
    ])

    chapter(story, "A", "Command reference", "Use this page during the demonstration; understand every command before an interview.", [
        p("Project operations", H2),
        code("git clone https://github.com/parrsi01/edge-sre-hardware-lab.git\ncd edge-sre-hardware-lab\nmake setup        # ensure the container runtime is running\nmake up           # build/start services\nmake status       # list container health\nmake logs         # follow service logs\nmake demo         # fault and recovery exercise\n./scripts/verify.sh\nmake down"),
        p("HTTP checks", H2),
        code("curl -i http://localhost:8000/healthz\ncurl -i http://localhost:8000/readyz\ncurl -s http://localhost:8000/api/status | jq\ncurl -s http://localhost:8000/metrics | head"),
        p("Views", H2),
        code("open http://localhost:8000\nopen http://localhost:8000/docs\nopen http://localhost:9090\nopen http://localhost:3000/d/edge-sre-lab"),
        p("Physical Linux checks", H2),
        code("hostnamectl\nip address\nip route\nss -lntp\nsystemctl status edge-agent\njournalctl -u edge-agent --since '10 minutes ago'"),
        p("Commands shown for the physical host are exercises for an authorized lab system. Never run network inspection or service changes on systems you do not own or have permission to administer." , WARN),
    ])

    chapter(story, "B", "Sources and evidence notes", "Primary sources support the concepts; all project-specific results were separately tested locally.", [
        p("Core learning sources", H2),
        *bullets([
            "Google, <link href='https://sre.google/sre-book/table-of-contents/'>Site Reliability Engineering - Table of Contents</link>: risk, SLOs, toil, monitoring, automation, troubleshooting, incidents and postmortems.",
            "Google, <link href='https://sre.google/workbook/table-of-contents/'>The Site Reliability Workbook</link>: practical SLO, monitoring, incident and configuration chapters.",
            "Prometheus, <link href='https://prometheus.io/docs/practices/instrumentation/'>Instrumentation best practices</link>: attempts, errors, latency, metric types and label-cardinality cautions.",
            "Raspberry Pi, <link href='https://www.raspberrypi.com/documentation/computers/getting-started.html'>Getting started</link> and <link href='https://www.raspberrypi.com/documentation/computers/remote-access.html'>remote access</link>: boot media, network and SSH setup.",
            "Geneva Business News, <link href='https://genevabusinessnews.ch/it/'>IT programme page</link>: support/dev/system/network practice, labs and named tools.",
            "CERN, <link href='https://careers.cern/jobs/devops-engineer-for-large-scale-compute/'>DevOps Engineer for Large Scale Compute</link>: current Geneva early-career stack, deadline and eligibility gates.",
            "CERN, <link href='https://careers.cern/jobs/ep-cms-tdq-2026-153-grap/'>Online Software Developer / CMS DAQ</link>: Python, C++, hardware interaction and CI/CD requirements.",
            "Proton, <link href='https://job-boards.eu.greenhouse.io/proton/jobs/4848439101?gh_src=6b341c62teu'>SRE Infrastructure Systems</link> and <link href='https://job-boards.greenhouse.io/proton/jobs/4612377101'>SRE Application Edge</link>: Kubernetes, Linux, networking, IaC and observability.",
            "adesso, <link href='https://www.adesso.ch/de_ch/jobs-karriere/unsere-stellenangebote/Senior-Site-Reliability-Engineer-all-genders-de-j2900.html'>Senior SRE</link>: Swiss DevOps/SRE stack and seniority boundary.",
            "PostFinance, <link href='https://jobs.postfinance.ch/offene-stellen/product-owner-continuous-integration-plattformen-w-m-d/4c9a3fca-6325-4494-86e5-19452b333564'>CI platform role</link>: current GitLab, observability, IaC and cloud-native evidence.",
            "OCSTAT, <link href='https://statistique.ge.ch/actualites/welcome.asp?Actudomaine=06_02&amp;aaaa1=2026&amp;aaaa2=2026&amp;actu=6016&amp;mm1=05/01&amp;mm2=12/31&amp;num=0'>Geneva employment Q2 2026 and detailed 2024 results</link>.",
            "ICT-Berufsbildung Schweiz, <link href='https://www.ict-berufsbildung.ch/resources/BSS-Schlussbericht-ICT-Bildungsbedarf-2033-2025-09_09.pdf'>ICT workforce requirements through 2033</link>: national cross-industry forecast, not a Geneva vacancy count.",
        ], SMALL),
        p("Procurement sources checked 19 September 2026", H2),
        *bullets([
            "<link href='https://www.pi-shop.ch/raspberry-pi-5-starter-kit-pi-5-4gb'>Pi-Shop Raspberry Pi 5 4 GB Starter Kit</link>.",
            "<link href='https://www.digitec.ch/en/s1/product/raspberry-pi-new-5-8gb-single-board-computer-kits-38955607'>Digitec Raspberry Pi 5 8 GB board</link> and live collection panel.",
            "<link href='https://www.digitec.ch/en/sites/246975'>Digitec Geneva store</link> and <link href='https://www.digitec.ch/sites'>Digitec locations</link>.",
        ], SMALL),
        p("Evidence boundaries", H2),
        p("The official IP4IT/GBN pages establish programme alignment only. Hardware, placement, supervision, funding and work authorization remain unknown until the centre confirms them. Store prices and stock are volatile. The user's skills and education are user-reported; the project build and demo results were observed locally. Publication proves access to code and documentation, not independent operation or employment."),
        p("Repository records", H2),
        code("README.md\nTRAINING_GUIDE.md\nSKILLS_MATRIX.md\nSECURITY.md\nhttps://github.com/parrsi01/edge-sre-hardware-lab"),
    ])

    # Remove the final page break so the document does not end with a blank page.
    if isinstance(story[-1], PageBreak):
        story.pop()
    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
