from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = r"C:\Users\Administrator\.openclaw\workspace\DaCreation_Introduction_v2.pdf"
LOGO = r"C:\Users\Administrator\.openclaw\workspace\brand_dacreation\logo-white.png"
FONT_HEAD = r"C:\Users\Administrator\.openclaw\workspace\brand_dacreation\PlayfairDisplay.ttf"
FONT_BODY = r"C:\Users\Administrator\.openclaw\workspace\brand_dacreation\Montserrat.ttf"

WORK1 = r"C:\Users\Administrator\.openclaw\workspace\brand_dacreation\work_mirchandani.png"
WORK2 = r"C:\Users\Administrator\.openclaw\workspace\brand_dacreation\work_beach.jpg"
WORK3 = r"C:\Users\Administrator\.openclaw\workspace\brand_dacreation\work_png_ls1.png"

# Register fonts
pdfmetrics.registerFont(TTFont('Playfair', FONT_HEAD))
pdfmetrics.registerFont(TTFont('Montserrat', FONT_BODY))

# Brand colors
MAROON = colors.HexColor('#601A29')
GOLD = colors.HexColor('#C2AD70')
OFFWHITE = colors.HexColor('#F9F8F6')
TEXT = colors.HexColor('#363330')
MUTED = colors.HexColor('#6B6661')

w, h = A4
c = canvas.Canvas(OUT, pagesize=A4)


def draw_topbar(page_title: str):
    c.setFillColor(MAROON)
    c.rect(0, h-18*mm, w, 18*mm, stroke=0, fill=1)
    logo = ImageReader(LOGO)
    lw, lh = 1808, 592
    logo_w = 42*mm
    logo_h = logo_w * (lh/lw)
    c.drawImage(logo, 18*mm, h-9*mm-logo_h/2, width=logo_w, height=logo_h, mask='auto')
    c.setFillColor(colors.white)
    c.setFont('Montserrat', 11)
    c.drawRightString(w-18*mm, h-11.5*mm, page_title)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.line(0, h-18*mm, w, h-18*mm)


# ---------------- Page 1: Cover ----------------
# Background (maroon) + subtle gold corner
c.setFillColor(MAROON)
c.rect(0, 0, w, h, stroke=0, fill=1)

c.setFillColor(GOLD)
c.rect(0, 0, 7*mm, h, stroke=0, fill=1)

logo = ImageReader(LOGO)
lw, lh = 1808, 592
logo_w = 110*mm
logo_h = logo_w * (lh/lw)
# Center logo better
c.drawImage(logo, (w-logo_w)/2, h-60*mm, width=logo_w, height=logo_h, mask='auto')

# Headline
c.setFillColor(colors.white)
c.setFont('Playfair', 28)
c.drawCentredString(w/2, h-82*mm, 'Company Introduction')

c.setStrokeColor(GOLD)
c.setLineWidth(2)
c.line(w*0.22, h-88*mm, w*0.78, h-88*mm)

# Subhead
c.setFont('Montserrat', 12)
c.setFillColor(OFFWHITE)
c.drawCentredString(w/2, h-102*mm, 'Weddings • Corporate Events • Celebrations • Decor')

# Elevator pitch
c.setFont('Montserrat', 11)
text = c.beginText(22*mm, h-125*mm)
text.setLeading(16)
text.setFillColor(OFFWHITE)
for line in [
    'Da Creation Events and Decor is a premium event management company based in Pune,',
    'delivering culturally rich weddings and high-impact corporate experiences across India.',
    '',
    'We bring together strategy, design, production, hospitality, and flawless on-ground execution—',
    'so your event feels effortless for you and unforgettable for your guests.'
]:
    text.textLine(line)
c.drawText(text)

# Stats strip
c.setFillColor(colors.Color(1,1,1,alpha=0.08))
c.roundRect(22*mm, 40*mm, w-44*mm, 30*mm, 8, stroke=0, fill=1)

c.setFillColor(GOLD)
c.setFont('Montserrat', 13)
c.drawCentredString(w*0.25, 58*mm, '100+')
c.drawCentredString(w*0.50, 58*mm, '20+')
c.drawCentredString(w*0.75, 58*mm, '2020')

c.setFillColor(OFFWHITE)
c.setFont('Montserrat', 9.5)
c.drawCentredString(w*0.25, 50*mm, 'Events Executed')
c.drawCentredString(w*0.50, 50*mm, 'Cities Covered')
c.drawCentredString(w*0.75, 50*mm, 'Founded')

# Footer
c.setFillColor(GOLD)
c.rect(0, 0, w, 16*mm, stroke=0, fill=1)
c.setFillColor(MAROON)
c.setFont('Montserrat', 9.5)
c.drawString(18*mm, 6*mm, 'dacreation.in  |  info@dacreation.in  |  +91 79724 96366')

c.showPage()

# ---------------- Page 2: About + Services ----------------
c.setFillColor(OFFWHITE)
c.rect(0, 0, w, h, stroke=0, fill=1)
draw_topbar('Overview')

c.setFillColor(TEXT)
c.setFont('Playfair', 22)
c.drawString(18*mm, h-38*mm, 'More Than Just Planners')

c.setFillColor(MUTED)
c.setFont('Montserrat', 10.5)
para = c.beginText(18*mm, h-50*mm)
para.setLeading(15)
for line in [
    'We blend modern design sensibilities with deep cultural understanding—',
    'bringing precision planning and premium execution to every event.',
    '',
    'From intimate celebrations to enterprise-scale corporate productions,',
    'our team manages everything end-to-end: concept, decor, vendors, timelines,',
    'technical production, hospitality, and on-ground coordination.'
]:
    para.textLine(line)
c.drawText(para)

# Services cards
c.setFont('Montserrat', 11)
card_w = (w-36*mm-10*mm)/2
card_h = 40*mm
x1, x2 = 18*mm, 18*mm + card_w + 10*mm
y = h-100*mm

cards = [
    ('Weddings & Celebrations', 'Tradition-led weddings with modern elegance, destination planning, and guest experience.'),
    ('Corporate Events', 'Conferences, product launches, brand activations, executive retreats, and gala nights.'),
    ('Design & Decor', 'Concept, staging, florals, lighting, set design, and styling aligned to your theme.'),
    ('Production & Logistics', 'Vendor management, timelines, technical production, hospitality, and run-of-show.'),
]

for i,(title,desc) in enumerate(cards):
    xx = x1 if i%2==0 else x2
    yy = y - (i//2)*(card_h+10*mm)
    # Card
    c.setFillColor(colors.white)
    c.roundRect(xx, yy, card_w, card_h, 10, stroke=0, fill=1)
    # Accent line
    c.setFillColor(GOLD)
    c.rect(xx, yy+card_h-3*mm, card_w, 3*mm, stroke=0, fill=1)
    c.setFillColor(TEXT)
    c.setFont('Montserrat', 11)
    c.drawString(xx+10*mm, yy+card_h-12*mm, title)
    c.setFillColor(MUTED)
    c.setFont('Montserrat', 9.5)
    t=c.beginText(xx+10*mm, yy+card_h-20*mm)
    t.setLeading(13)
    # wrap manually
    import textwrap
    for line in textwrap.wrap(desc, width=44):
        t.textLine(line)
    c.drawText(t)

# Why us
c.setFillColor(TEXT)
c.setFont('Playfair', 18)
c.drawString(18*mm, 78*mm, 'Why Clients Choose Us')

bullets = [
    'Clear timelines, transparent communication, and dedicated on-ground teams',
    'Modern aesthetic with cultural sensitivity for Indian rituals and brand guidelines',
    'Corporate-grade documentation, vendor management, and stakeholder alignment',
    'Execution-first approach focused on guest experience and business outcomes',
]

yb = 70*mm
c.setFont('Montserrat', 10.2)
for b in bullets:
    c.setFillColor(GOLD)
    c.circle(20*mm, yb+1.5*mm, 1.2*mm, stroke=0, fill=1)
    c.setFillColor(MUTED)
    c.drawString(24*mm, yb, b)
    yb -= 8*mm

c.setStrokeColor(colors.HexColor('#E7DDC8'))
c.setLineWidth(1)
c.line(18*mm, 20*mm, w-18*mm, 20*mm)
c.setFillColor(MUTED)
c.setFont('Montserrat', 9)
c.drawString(18*mm, 12*mm, 'Website: dacreation.in   |   Email: info@dacreation.in   |   Phone: +91 79724 96366 / +91 78878 28280')

c.showPage()

# ---------------- Page 3: Selected Works ----------------
c.setFillColor(OFFWHITE)
c.rect(0, 0, w, h, stroke=0, fill=1)
draw_topbar('Selected Works')

c.setFillColor(TEXT)
c.setFont('Playfair', 22)
c.drawString(18*mm, h-38*mm, 'Featured Moments')

c.setFillColor(MUTED)
c.setFont('Montserrat', 10.5)
c.drawString(18*mm, h-48*mm, 'A glimpse into events crafted with intention, precision, and emotion.')

# Work grid
items = [
    ('Mirchandani Family Wedding', 'Lonavala, Maharashtra', WORK1, 'Wedding'),
    ('Beach Destination Wedding', 'Goa', WORK2, 'Destination'),
    ('Litestyle By PNG', 'Pune', WORK3, 'Corporate'),
]

img_w = (w - 18*mm*2 - 10*mm*2)/3
img_h = 55*mm
start_y = h-70*mm

for i,(name,loc,img_path,tag) in enumerate(items):
    x = 18*mm + i*(img_w + 10*mm)
    y = start_y - img_h
    # image
    img = ImageReader(img_path)
    c.roundRect(x, y, img_w, img_h, 10, stroke=0, fill=0)
    c.drawImage(img, x, y, width=img_w, height=img_h, mask='auto', preserveAspectRatio=True, anchor='c')
    # tag pill
    c.setFillColor(colors.Color(0,0,0,alpha=0.45))
    c.roundRect(x+6*mm, y+img_h-10*mm, 26*mm, 8*mm, 4, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont('Montserrat', 8.5)
    c.drawString(x+8*mm, y+img_h-8.2*mm, tag.upper())
    # captions
    c.setFillColor(TEXT)
    c.setFont('Montserrat', 10.5)
    c.drawString(x, y-6*mm, name)
    c.setFillColor(MUTED)
    c.setFont('Montserrat', 9.5)
    c.drawString(x, y-11*mm, loc)

# CTA
c.setFillColor(MAROON)
c.roundRect(18*mm, 25*mm, w-36*mm, 20*mm, 10, stroke=0, fill=1)
c.setFillColor(colors.white)
c.setFont('Montserrat', 11)
c.drawCentredString(w/2, 34*mm, 'Book a Free Consultation  •  dacreation.in/inquire')

c.save()
print('wrote', OUT)
