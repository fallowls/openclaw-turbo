from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

name = "Pallavi Srivastava"
contact = "pallavisrivastava0507@gmail.com   6395934465"

summary = (
"Results-driven sales professional with a robust foundation in strategic account management and business development across "
"diverse markets. Adept at building and nurturing high-impact client relationships, optimizing revenue channels, and delivering "
"tailored solutions to meet complex client needs. Poised to leverage expertise in market expansion, CRM-based pipeline "
"development, and cross-functional collaboration to drive sustainable growth in a dynamic B2B sales environment. Passionate "
"about bringing innovative sales strategies to new challenges and contributing to a high-performing sales team."
)

experiences = [
    ("Business Development Executive", "Ziff Davis – Performance Marketing", "Aug 2025 – Jan 2026", [
        "Generated qualified appointments through outbound prospecting across email, phone, and LinkedIn outreach.",
        "Worked closely with sales leadership to refine target accounts and improve appointment-to-meeting conversion rates.",
        "Maintained and updated CRM records to ensure clean pipeline tracking and accurate reporting.",
        "Collaborated with internal teams to tailor outreach messaging and improve response rates."
    ]),
    ("Sales Development Representative", "Unbound B2B", "Mar 2025 – Jul 2025", [
        "Spearheaded outbound prospecting across global markets via cold calls, email campaigns, and LinkedIn outreach, generating a steady flow of qualified leads.",
        "Conducted discovery conversations to assess client needs, qualifying prospects against ideal customer profiles to drive high-quality sales opportunities.",
        "Coordinated strategic demos and meetings between leads and Global Account Directors, accelerating deal progression and improving conversion rates.",
        "Designed and optimized CRM workflows, co-developing the HubSpot Dream Plan to streamline lead tracking and boost team productivity.",
        "Partnered with marketing to enhance lead generation strategy and delivered detailed pipeline reports to senior leadership for data-driven decisions."
    ]),
    ("Assistant Sales Manager", "Atica", "Feb 2024 – Present", [
        "Provided sales support for multi-branded hotels across the USA, developing and executing strategies to consistently exceed revenue targets.",
        "Built and maintained a high-performing sales pipeline using CRM systems, improving efficiency and accelerating the sales cycle.",
        "Conducted bi-weekly strategy calls with hotels to align goals, enhance performance, and optimize engagement.",
        "Led cross-selling initiatives and auditing projects to identify new revenue opportunities and drive measurable ROI.",
        "Activated new accounts and expanded market share by leveraging strong client relationships and strategic market insights."
    ]),
    ("Senior Business Development Associate", "Scaler", "May 2022 – Jan 2024 (1 year 7 months)", [
        "Pioneered a comprehensive analysis of the B2C market, identifying key trends and untapped opportunities that contributed to a 20% YoY revenue surge.",
        "Spearheaded cross-functional teams to implement innovative B2C sales strategies, driving portfolio expansion and acquiring pivotal consumer accounts.",
        "Applied consultative selling techniques and data-driven approaches to achieve a 15% improvement in conversion rates and surpass sales targets.",
        "Negotiated and closed deals with high-profile clients, securing long-term partnerships and aligning product offerings with market demands."
    ]),
    ("Senior Business Development Associate", "Planet Spark", "Jan 2021 – Apr 2022 (1 year 4 months)", [
        "Delivered 25% customer satisfaction growth by presenting tailored ed-tech solutions in the US & Canadian markets.",
        "Surpassed quarterly revenue targets and enhanced market share by 15% through adaptive sales strategies."
    ]),
    ("Sales Associate", "The Times of India", "Jul 2020 – Dec 2020 (6 months)", [
        "Conducted market research, streamlined processes, and fostered client relationships to improve retention."
    ])
]

education = "MBA | Graphic Era Deemed to be University"
skills = (
"Business Relationship Management • Customer Relationship Management (CRM) • Consultative Selling • Strategic Thinking • "
"Solution Selling • Analytical Skills • Negotiation • Deal Closure • Cross-team Collaboration • Business Acumen"
)

file_path = r"C:\Users\Administrator\.openclaw\workspace\Pallavi_Srivastava_Updated_SameFormat.pdf"

styles = getSampleStyleSheet()
style_name = ParagraphStyle('name', parent=styles['Normal'], fontSize=14, spaceAfter=4)
style_contact = ParagraphStyle('contact', parent=styles['Normal'], fontSize=10, textColor=colors.black, spaceAfter=8)
style_heading = ParagraphStyle('heading', parent=styles['Normal'], fontSize=11, spaceBefore=6, spaceAfter=4, textColor=colors.black)
style_body = ParagraphStyle('body', parent=styles['Normal'], fontSize=10, leading=13)

story = []
story.append(Paragraph(name, style_name))
story.append(Paragraph(contact, style_contact))

story.append(Paragraph("Summary", style_heading))
story.append(Paragraph(summary, style_body))

story.append(Paragraph("Experience", style_heading))
for title, company, dates, bullets in experiences:
    story.append(Paragraph(f"{title}", style_body))
    story.append(Paragraph(f"{company}: {dates}", style_body))
    for i, b in enumerate(bullets, 1):
        story.append(Paragraph(f"{i}. {b}", style_body))
    story.append(Spacer(1, 4))

story.append(Paragraph("Education", style_heading))
story.append(Paragraph(education, style_body))

story.append(Paragraph("Skills", style_heading))
story.append(Paragraph(skills, style_body))

doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
doc.build(story)
print(file_path)
