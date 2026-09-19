#!/usr/bin/env python3
"""Build the verified one-page operator guide for Edge SRE Hardware Lab."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT.parents[1] / "output" / "pdf" / "EDGE_SRE_LAB_ONE_PAGE_GUIDE.pdf"

INK = colors.HexColor("#12211E")
GREEN = colors.HexColor("#0B7A53")
MINT = colors.HexColor("#DDF5EA")
PALE = colors.HexColor("#F4F8F6")
LINE = colors.HexColor("#B9CBC4")
MUTED = colors.HexColor("#50605B")


def page(canvas, doc):
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.rect(0, height - 24 * mm, width, 24 * mm, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 19)
    canvas.drawString(14 * mm, height - 14 * mm, "EDGE SRE HARDWARE LAB")
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(colors.HexColor("#A9EFD1"))
    canvas.drawRightString(width - 14 * mm, height - 14 * mm, "ONE-PAGE OPERATOR GUIDE")
    canvas.setStrokeColor(LINE)
    canvas.line(14 * mm, 11 * mm, width - 14 * mm, 11 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(14 * mm, 7 * mm, "Local training system - C++ device, Python control plane, metrics and recovery")
    canvas.drawRightString(width - 14 * mm, 7 * mm, "Verified 19 Sep 2026")
    canvas.restoreState()


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    body = ParagraphStyle(
        "Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.4,
        leading=10.4, textColor=INK, spaceAfter=2.5 * mm,
    )
    small = ParagraphStyle(
        "Small", parent=body, fontSize=7.5, leading=9, spaceAfter=1.5 * mm,
    )
    heading = ParagraphStyle(
        "Heading", parent=body, fontName="Helvetica-Bold", fontSize=10.7,
        leading=12.5, textColor=GREEN, spaceBefore=1.5 * mm, spaceAfter=1.5 * mm,
    )
    code = ParagraphStyle(
        "Code", parent=body, fontName="Courier", fontSize=7.1, leading=9.2,
        leftIndent=3 * mm, rightIndent=3 * mm, spaceBefore=1 * mm, spaceAfter=1 * mm,
    )
    note = ParagraphStyle(
        "Note", parent=small, borderColor=GREEN, borderWidth=0.8,
        borderPadding=6, backColor=MINT, textColor=INK,
    )

    doc = BaseDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=14 * mm, leftMargin=14 * mm,
        topMargin=29 * mm, bottomMargin=15 * mm,
        title="Edge SRE Hardware Lab - One-Page Operator Guide",
        author="Simon Parris",
        subject="Local SRE and hardware-aware DevOps project operator guide",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates(PageTemplate(id="one", frames=frame, onPage=page))

    story = [
        Paragraph(
            "<b>Purpose.</b> Demonstrate that you can operate a networked Linux service: collect device telemetry, expose an API, observe reliability, inject a safe fault and restore service. The current device is a C++ simulator; the supplied Linux agent is the supervised physical-host upgrade.",
            body,
        ),
    ]

    architecture = Table(
        [[Paragraph("C++ DEVICE", small), Paragraph("TCP / JSON", small), Paragraph("PYTHON API", small), Paragraph("PROMETHEUS", small), Paragraph("GRAFANA + WEB", small)]],
        colWidths=[33 * mm, 29 * mm, 34 * mm, 34 * mm, 42 * mm],
    )
    architecture.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PALE),
        ("TEXTCOLOR", (0, 0), (-1, -1), GREEN),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.7, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.extend([architecture, Spacer(1, 2 * mm)])

    left = [
        Paragraph("1. Start it", heading),
        Paragraph(
            "git clone https://github.com/parrsi01/<br/>edge-sre-hardware-lab.git<br/>cd edge-sre-hardware-lab<br/>make setup<br/>make up<br/>open http://localhost:8000",
            code,
        ),
        Paragraph("2. Run the five-minute demonstration", heading),
        Paragraph(
            "1. Show the healthy dashboard.<br/>2. Select <b>Inject fault</b> and wait about 3 seconds.<br/>3. Explain: liveness remains available while readiness fails.<br/>4. Show failed polls in Grafana.<br/>5. Select <b>Recover device</b>; show readiness returning.<br/>6. In Terminal, run <font name='Courier'>make demo</font> for the scripted proof.",
            small,
        ),
        Paragraph("3. Operate and stop", heading),
        Paragraph(
            "<font name='Courier'>make status</font> - container health<br/><font name='Courier'>make logs</font> - live service logs<br/><font name='Courier'>./scripts/verify.sh</font> - build and tests<br/><font name='Courier'>make down</font> - stop the stack",
            small,
        ),
    ]

    locations_data = [
        [Paragraph("LOCATION", small), Paragraph("WHAT IS THERE", small)],
        [Paragraph("device-simulator/", small), Paragraph("C++ sockets, telemetry and fault state", small)],
        [Paragraph("control-api/", small), Paragraph("Polling, validation, REST, metrics and UI", small)],
        [Paragraph("observability/", small), Paragraph("Prometheus and Grafana configuration", small)],
        [Paragraph("hardware-agent/", small), Paragraph("Optional real Linux host replacement", small)],
        [Paragraph("scripts/", small), Paragraph("Setup, demo, readiness and verification", small)],
        [Paragraph("docs/", small), Paragraph("Public-ready static case study", small)],
    ]
    locations = Table(locations_data, colWidths=[38 * mm, 48 * mm], repeatRows=1)
    locations.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), INK),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.45, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    right = [
        Paragraph("Open these views", heading),
        Paragraph(
            "Dashboard - http://localhost:8000<br/>Grafana - http://localhost:3000/d/edge-sre-lab<br/>Prometheus - http://localhost:9090<br/>API docs - http://localhost:8000/docs",
            small,
        ),
        Paragraph("Where everything is", heading),
        locations,
        Spacer(1, 1.5 * mm),
        Paragraph("What to say at the centre", heading),
        Paragraph(
            '"I built a hardware-aware reliability system. A C++ service represents a networked device. A Python control plane validates telemetry and exposes metrics. I can create a controlled incident, observe it and restore service. I want to replace the simulator with an approved Linux device here and document the handover."',
            note,
        ),
    ]

    columns = Table(
        [[left, right]],
        colWidths=[86 * mm, 89 * mm],
        hAlign="LEFT",
    )
    columns.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 5 * mm),
        ("LEFTPADDING", (1, 0), (1, 0), 3 * mm),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("LINEBEFORE", (1, 0), (1, 0), 0.7, LINE),
    ]))
    story.append(columns)
    story.extend([
        Spacer(1, 3 * mm),
        Paragraph(
            "<b>Evidence boundary:</b> This proves a local simulated system, tested fault handling and reproducible operation. It does not prove production, FPGA, physical data-centre or CERN experience. The public repository documents the work; the next proof is an independently supervised deployment to an approved physical Linux host.",
            note,
        ),
    ])

    doc.build(story)
    print(OUTPUT)


if __name__ == "__main__":
    build()
