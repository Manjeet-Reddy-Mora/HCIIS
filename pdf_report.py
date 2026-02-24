from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap


def _draw_text(c, text, x, y, width=90):
    for line in wrap(text, width):
        c.drawString(x, y, line)
        y -= 14
    return y


def generate_pdf_report(text, cog, manip, emo, dec, qual):
    file_name = "HCIIS_Report.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Human-Centered Information Intelligence System Report")

    y -= 30
    c.setFont("Helvetica", 11)
    y = _draw_text(
        c,
        "This report presents a multi-dimensional analysis of how text "
        "impacts human cognition, emotion, decision-making, and information quality.",
        50, y
    )

    sections = [
        ("Cognitive Load Analysis",
         f"Score: {cog['load']} | Attention Risk: {cog['attention_drop']}\n"
         f"{cog['explanation']}"),

        ("Manipulation & Persuasion",
         f"Score: {manip['score']}\n{manip['details']}"),

        ("Emotion & Tone",
         f"Dominant Emotion: {emo['dominant']} | Volatility: {emo['volatility']}\n"
         f"{emo['summary']}"),

        ("Decision Risk",
         f"Decision Density: {dec['density']} | Ambiguity: {dec['ambiguity']}\n"
         f"{dec['notes']}"),

        ("Information Quality",
         f"Quality Score: {qual['quality']}\n{qual['analysis']}")
    ]

    for title, content in sections:
        y -= 25
        if y < 120:
            c.showPage()
            y = height - 50

        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, y, title)
        y -= 18

        c.setFont("Helvetica", 11)
        y = _draw_text(c, content, 50, y)

    c.save()
    return file_name
