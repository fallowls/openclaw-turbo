from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

OUT = r"C:\Users\Administrator\.openclaw\workspace\DaCreation_Introduction.pdf"
LOGO = r"C:\Users\Administrator\.openclaw\workspace\brand_dacreation\logo-white.png"

# Brand colors (from site scan)
MAROON = colors.HexColor('#601A29')
GOLD = colors.HexColor('#C2AD70')
OFFWHITE = colors.HexColor('#F9F8F6')
TEXT = colors.HexColor('#363330')

w, h = A4
c = canvas.Canvas(OUT, pagesize=A4)

# ---------- Page 1 (Cover) ----------
# Full-bleed maroon background
c.setFillColor(MAROON)
c.rect(0, 0, w, h, stroke=0, fill=1)

# Logo
logo = ImageReader(LOGO)
# fit logo to width ~90mm maintaining aspect
logo_w = 90*mm
# original aspect
lw, lh = 1808, 592
logo_h = logo_w * (lh / lw)

c.drawImage(logo, 20*mm, h - 35*mm - logo_h, width=logo_w, height=logo_h, mask='auto')

# Gold accent line
c.setStrokeColor(GOLD)
c.setLineWidth(2)
c.line(20*mm, h - 45*mm, w - 20*mm, h - 45*mm)

# Title
c.setFillColor(colors.white)
c.setFont('Helvetica-Bold', 26)
c.drawString(20*mm, h - 70*mm, 'Company Introduction')

# Subtitle
c.setFont('Helvetica', 14)
c.setFillColor(OFFWHITE)
c.drawString(20*mm, h - 82*mm, 'Events • Decor • Wedding & Corporate Experiences')

# Value statement
c.setFillColor(OFFWHITE)
c.setFont('Helvetica', 12)
text = c.beginText(20*mm, h - 105*mm)
text.setLeading(18)
for line in [
    'Da Creation Events and Decor crafts culturally rich, aesthetically modern,',
    'and flawlessly executed events across India—built on precision, creativity, and impact.',
    '',
    'From grand weddings to high-stakes corporate conferences, we manage end-to-end planning,',
    'design, production, vendors, logistics, hospitality, and on-ground execution.'
]:
    text.textLine(line)
c.drawText(text)

# Bottom bar
c.setFillColor(GOLD)
c.rect(0, 0, w, 18*mm, stroke=0, fill=1)
c.setFillColor(MAROON)
c.setFont('Helvetica-Bold', 11)
c.drawString(20*mm, 6*mm, 'dacreation.in  |  info@dacreation.in  |  +91 79724 96366')

c.showPage()

# ---------- Page 2 (Services / Why Us) ----------
# Background
c.setFillColor(OFFWHITE)
c.rect(0, 0, w, h, stroke=0, fill=1)

# Header strip
c.setFillColor(MAROON)
c.rect(0, h-25*mm, w, 25*mm, stroke=0, fill=1)
# small logo
logo_w2 = 55*mm
logo_h2 = logo_w2 * (lh / lw)
c.drawImage(logo, 20*mm, h-18*mm-logo_h2/2, width=logo_w2, height=logo_h2, mask='auto')

c.setFillColor(colors.white)
c.setFont('Helvetica-Bold', 18)
c.drawRightString(w-20*mm, h-16*mm, 'What We Do')

# Section: Services
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 14)
c.drawString(20*mm, h-45*mm, 'Core Services')

c.setFont('Helvetica', 11)
services = [
    ('Weddings & Celebrations', 'Traditional ceremonies, modern aesthetics, destination planning, and guest experience.'),
    ('Corporate Events', 'Conferences, product launches, brand activations, executive retreats, and gala nights.'),
    ('Design & Decor', 'Concept, staging, florals, lighting, set design, and on-site styling aligned to your theme.'),
    ('Production & Logistics', 'Vendor management, timelines, technical production, hospitality, and flawless run-of-show.'),
]

y = h-55*mm
for title, desc in services:
    c.setFillColor(MAROON)
    c.circle(22*mm, y+2.5*mm, 1.3*mm, stroke=0, fill=1)
    c.setFillColor(TEXT)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(26*mm, y, title)
    c.setFont('Helvetica', 10.5)
    c.setFillColor(colors.HexColor('#6B6661'))
    c.drawString(26*mm, y-5.5*mm, desc)
    y -= 18*mm

# Section: Why choose us
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 14)
c.drawString(20*mm, y-4*mm, 'Why Clients Choose Da Creation')

bullets = [
    'End-to-end execution with clear timelines and transparent communication',
    'Modern aesthetic with cultural sensitivity for Indian rituals and brand guidelines',
    'Corporate-grade professionalism: documentation, NDAs, and stakeholder alignment',
    'Precision planning focused on guest experience and business outcomes',
]

y2 = y - 14*mm
c.setFont('Helvetica', 11)
c.setFillColor(TEXT)
for b in bullets:
    c.setFillColor(GOLD)
    c.rect(20*mm, y2+2.5*mm, 3*mm, 3*mm, stroke=0, fill=1)
    c.setFillColor(TEXT)
    c.drawString(25*mm, y2, b)
    y2 -= 9*mm

# Footer
c.setStrokeColor(GOLD)
c.setLineWidth(1)
c.line(20*mm, 20*mm, w-20*mm, 20*mm)

c.setFillColor(colors.HexColor('#6B6661'))
c.setFont('Helvetica', 9.5)
c.drawString(20*mm, 12*mm, 'Website: dacreation.in   |   Email: info@dacreation.in   |   Phone: +91 79724 96366 / +91 78878 28280')

c.save()
print('wrote', OUT)
