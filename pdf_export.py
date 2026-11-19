import io
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def _escape_xml(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _format_inline(line: str) -> str:
    escaped = _escape_xml(line)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', escaped)
    return escaped


def markdown_to_pdf_bytes(md_text: str, title: str = "Supply Chain Recovery Playbook") -> bytes:
    """Convert Markdown playbook text into a downloadable PDF byte buffer."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=48,
        bottomMargin=45,
        title=title,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "PlaybookTitle",
        parent=styles["Heading1"],
        fontSize=17,
        leading=22,
        textColor=HexColor("#0f172a"),
        spaceAfter=12,
    )
    h2_style = ParagraphStyle(
        "PlaybookH2",
        parent=styles["Heading2"],
        fontSize=13,
        leading=17,
        textColor=HexColor("#0f766e"),
        spaceBefore=12,
        spaceAfter=6,
    )
    h3_style = ParagraphStyle(
        "PlaybookH3",
        parent=styles["Heading3"],
        fontSize=11,
        leading=15,
        textColor=HexColor("#1e293b"),
        spaceBefore=8,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "PlaybookBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=14.5,
        textColor=HexColor("#1e293b"),
        spaceAfter=5,
    )
    bullet_style = ParagraphStyle(
        "PlaybookBullet",
        parent=body_style,
        leftIndent=16,
        firstLineIndent=-10,
        spaceAfter=4,
    )

    story = [Paragraph(_escape_xml(title), title_style)]

    for raw_line in md_text.splitlines():
        line = raw_line.strip()
        if not line:
            story.append(Spacer(1, 5))
            continue
        if line in ("---", "***", "___"):
            story.append(Spacer(1, 8))
            continue
        if line.startswith("### "):
            story.append(Paragraph(_format_inline(line[4:].strip()), h3_style))
        elif line.startswith("## "):
            story.append(Paragraph(_format_inline(line[3:].strip()), h2_style))
        elif line.startswith("# "):
            story.append(Paragraph(_format_inline(line[2:].strip()), title_style))
        elif line.startswith(("- ", "* ")):
            story.append(Paragraph("• " + _format_inline(line[2:].strip()), bullet_style))
        elif re.match(r"^\d+\.\s+", line):
            story.append(Paragraph(_format_inline(line), bullet_style))
        else:
            story.append(Paragraph(_format_inline(line), body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()