from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf(filepath, data):
    doc = SimpleDocTemplate(filepath)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>AI Prompt Optimization Report</b>", styles["Heading1"]))
    story.append(Paragraph(f"<b>Original Prompt:</b> {data['original_prompt']}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Optimized Prompt:</b> {data['optimized_prompt']}", styles["BodyText"]))
    story.append(Paragraph(f"<b>Quality Score:</b> {data['quality_score']}/100", styles["BodyText"]))
    story.append(Paragraph(f"<b>Category:</b> {data['category']}", styles["BodyText"]))

    story.append(Paragraph("<b>Suggestions:</b>", styles["Heading2"]))

    for suggestion in data["suggestions"]:
        story.append(Paragraph(f"• {suggestion}", styles["BodyText"]))

    doc.build(story)