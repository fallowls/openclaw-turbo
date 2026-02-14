from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

name = "Pallavi Srivastava"
contact = "✉ pallavisrivastava0507@gmail.com   |   ☎ 6395934465"

summary = (
"Results-driven sales professional with a robust foundation in strategic account management and business development across diverse markets. "
"Adept at building high-impact client relationships, optimizing revenue channels, and delivering tailored solutions. "
"Skilled in market expansion, CRM-based pipeline development, and cross-functional collaboration to drive B2B growth."
)

experience = [
    ("Business Development Executive", "Ziff Davis – Performance Marketing", "Aug 2025 – Jan 2026", [
        "Generated qualified appointments via email, phone, and LinkedIn outreach.",
        "Refined target accounts to improve appointment‑to‑meeting conversion rates.",
        "Maintained CRM records for accurate pipeline tracking.",
        "Collaborated on outreach messaging to improve response rates."
    ]),
    ("Sales Development Representative", "Unbound B2B", "Mar 2025 – Jul 2025", [
        "Outbound prospecting across global markets; generated qualified leads.",
        "Qualified prospects against ICP via discovery conversations.",
        "Coordinated demos/meetings with Global Account Directors.",
        "Optimized CRM workflows (HubSpot Dream Plan).",
        "Delivered pipeline reports to leadership."
    ]),
    ("Assistant Sales Manager", "Atica", "Feb 2024 – Present", [
        "Supported multi‑branded hotels across the USA; exceeded targets.",
        "Built/maintained sales pipeline using CRM systems.",
        "Led bi‑weekly strategy calls with hotels.",
        "Drove cross‑selling and auditing projects for ROI.",
        "Activated new accounts and expanded market share."
    ]),
    ("Senior Business Development Associate", "Scaler", "May 2022 – Jan 2024", [
        "B2C market analysis driving 20% YoY revenue surge.",
        "Implemented sales strategies; improved conversion by 15%.",
        "Closed high‑profile deals; secured long‑term partnerships."
    ]),
    ("Senior Business Development Associate", "Planet Spark", "Jan 2021 – Apr 2022", [
        "Delivered 25% CSAT growth; surpassed quarterly targets by 15%."
    ]),
    ("Sales Associate", "The Times of India", "Jul 2020 – Dec 2020", [
        "Conducted market research and improved client retention."
    ])
]

education = "MBA | Graphic Era Deemed to be University"
skills = (
"Business Relationship Management, CRM, Consultative Selling, Strategic Thinking, Solution Selling, Analytical Skills, "
"Negotiation, Deal Closure, Cross‑team Collaboration, Business Acumen"
)

file_path = r"C:\Users\Administrator\.openclaw\workspace\Pallavi_Srivastava_OnePage_Final.pdf"

styles = getSampleStyleSheet()
style_name = ParagraphStyle('name', parent=styles['Normal'], fontSize=14, alignment=TA_CENTER, spaceAfter=2)
style_contact = ParagraphStyle('contact', parent=styles['Normal'], fontSize=9.5, alignment=TA_CENTER, spaceAfter=6)
style_heading = ParagraphStyle('heading', parent=styles['Normal'], fontSize=10.5, spaceBefore=4, spaceAfter=2)
style_body = ParagraphStyle('body', parent=styles['Normal'], fontSize=9, leading=11)
style_role = ParagraphStyle('role', parent=styles['Normal'], fontSize=9, leading=11, spaceBefore=1, spaceAfter=0)

story = []
story.append(Paragraph(name, style_name))
story.append(Paragraph(contact, style_contact))

story.append(Paragraph("Professional Summary", style_heading))
story.append(Paragraph(summary, style_body))

story.append(Paragraph("Professional Experience", style_heading))
for title, company, dates, bullets in experience:
    story.append(Paragraph(f"<b>{title}</b>", style_role))
    story.append(Paragraph(f"{company} | {dates}", style_body))
    for b in bullets:
        story.append(Paragraph(f"• {b}", style_body))
    story.append(Spacer(1, 1))

story.append(Paragraph("Education", style_heading))
story.append(Paragraph(education, style_body))

story.append(Paragraph("Skills", style_heading))
story.append(Paragraph(skills, style_body))

doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=28, leftMargin=28, topMargin=24, bottomMargin=24)
doc.build(story)
print(file_path)
