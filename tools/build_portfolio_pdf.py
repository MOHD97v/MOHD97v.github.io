"""Build a recruiter-friendly, downloadable PDF companion to the interactive portfolio.

Run: pip install reportlab && python tools/build_portfolio_pdf.py
No network requests, credentials, or private client records are used.
"""
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'portfolio' / 'Mohammed_Almutairi_Portfolio.pdf'
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

# Fail loudly rather than publishing a stale document if the source facts change.
html = (ROOT / 'index.html').read_text(encoding='utf-8')
for fact in ('231,719 consolidated shipments', '1.39 million', 'PRODUCTION USE',
             'Creator &amp; Backend Engineer', 'CI/CD', 'django-pricing-engine-demo'):
    if fact not in html:
        raise SystemExit(f'Portfolio PDF source fact missing from index.html: {fact}')

NAVY = colors.HexColor('#172638')
INK = colors.HexColor('#25374B')
MUTED = colors.HexColor('#63778A')
MINT = colors.HexColor('#377C6B')
PALE = colors.HexColor('#EFF5F3')
BLUE_PALE = colors.HexColor('#EDF3F8')
LINE = colors.HexColor('#D9E3EA')
WHITE = colors.white
W, H = A4
M = 19 * mm
CONTENT = W - 2 * M

styles = {
    'eyebrow': ParagraphStyle('eyebrow', fontName='Helvetica-Bold', fontSize=8, leading=12, textColor=MINT, spaceAfter=9),
    'hero': ParagraphStyle('hero', fontName='Times-Roman', fontSize=35, leading=38, textColor=NAVY, spaceAfter=11),
    'section': ParagraphStyle('section', fontName='Times-Roman', fontSize=24, leading=28, textColor=NAVY, spaceBefore=7, spaceAfter=10),
    'sub': ParagraphStyle('sub', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=INK, spaceAfter=6),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=9.4, leading=15.3, textColor=INK, spaceAfter=8),
    'small': ParagraphStyle('small', fontName='Helvetica', fontSize=8.2, leading=12.8, textColor=INK, spaceAfter=6),
    'muted': ParagraphStyle('muted', fontName='Helvetica', fontSize=8.3, leading=12.7, textColor=MUTED, spaceAfter=6),
    'metric': ParagraphStyle('metric', fontName='Helvetica-Bold', fontSize=26, leading=29, textColor=NAVY, spaceAfter=5),
    'metric_label': ParagraphStyle('metric_label', fontName='Helvetica', fontSize=8.6, leading=13, textColor=INK),
    'link': ParagraphStyle('link', fontName='Helvetica', fontSize=8.6, leading=13, textColor=MINT),
    'tiny': ParagraphStyle('tiny', fontName='Helvetica', fontSize=7.3, leading=11, textColor=MUTED),
}

def P(text, style='body'):
    return Paragraph(text, styles[style])

def spacer(h=10):
    return Spacer(1, h)

def section(kicker, title):
    return [P(kicker.upper(), 'eyebrow'), P(title, 'section')]

def card(text, bg=PALE, pad=11):
    t = Table([[P(text, 'small')]], colWidths=[CONTENT], hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1),bg),
        ('BOX', (0,0),(-1,-1),.6,LINE),
        ('LEFTPADDING',(0,0),(-1,-1),pad),
        ('RIGHTPADDING',(0,0),(-1,-1),pad),
        ('TOPPADDING',(0,0),(-1,-1),pad),
        ('BOTTOMPADDING',(0,0),(-1,-1),pad-5),
    ]))
    return t

def grid(items, widths=None, bg=BLUE_PALE):
    widths = widths or [CONTENT / len(items)] * len(items)
    cells = []
    for title, body in items:
        cells.append([P(title, 'sub'), P(body, 'small')])
    t = Table([cells], colWidths=widths, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LINEBEFORE',(1,0),(-1,-1),.8,LINE),
        ('BOX',(0,0),(-1,-1),.6,LINE),
        ('LEFTPADDING',(0,0),(-1,-1),12),
        ('RIGHTPADDING',(0,0),(-1,-1),12),
        ('TOPPADDING',(0,0),(-1,-1),12),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),
    ]))
    return t


def decorate(canvas, doc):
    canvas.saveState()
    # Quiet header and footer that print cleanly.
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(.5)
    canvas.line(M, H - 15 * mm, W - M, H - 15 * mm)
    canvas.setFont('Helvetica-Bold', 8)
    canvas.setFillColor(NAVY)
    canvas.drawString(M, H - 12.5 * mm, 'MOHAMMED ALMUTAIRI')
    canvas.setFont('Helvetica', 7.4)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(W - M, H - 12.5 * mm, 'BACKEND SOFTWARE ENGINEER  /  PORTFOLIO')
    canvas.setStrokeColor(LINE)
    canvas.line(M, 17 * mm, W - M, 17 * mm)
    canvas.setFont('Helvetica', 7.4)
    canvas.drawString(M, 12.6 * mm, 'mohd97v.github.io  |  github.com/MOHD97v')
    canvas.drawRightString(W - M, 12.6 * mm, f'{doc.page}  /  PORTFOLIO')
    canvas.restoreState()

pdf = BaseDocTemplate(str(OUTPUT), pagesize=A4,
                      leftMargin=M, rightMargin=M, topMargin=22*mm, bottomMargin=23*mm,
                      title='Mohammed Almutairi | Software Engineering Portfolio',
                      author='Mohammed Almutairi',
                      subject='ShipMatrix, Smart Adaptable Mapping and Django commerce systems')
frame = Frame(M, 23*mm, CONTENT, H - 45*mm, id='normal', showBoundary=0,
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
pdf.addPageTemplates([PageTemplate(id='portfolio', frames=[frame], onPage=decorate)])

story = []
# PAGE 1 - EXECUTIVE INTRODUCTION
story.extend([
    spacer(18),
    P('SOFTWARE ENGINEERING  /  RIYADH, SAUDI ARABIA', 'eyebrow'),
    P('From concept.<br/>To production.', 'hero'),
    P('I turn operational problems into well-structured software. From enterprise logistics to adaptable e-commerce, I design, build and own systems people actually rely on.'),
    spacer(10),
    grid([
        ('230K+', 'Consolidated shipments processed through ShipMatrix'),
        ('30%', 'Logistics workload automated at Align Technology'),
        ('02', 'Startups adopting the configurable commerce backend'),
    ]),
    spacer(24),
    *section('01 / Flagship case study', 'ShipMatrix'),
    P('<b>Creator &amp; Backend Engineer | Oct 2023-present</b>', 'small'),
    P('ShipMatrix is a B2B logistics automation platform I designed, built and operated independently. It bridges inconsistent merchant exports and warehouse operations, preparing carrier-ready shipping data without requiring merchants to rebuild their ERP or OMS workflows.'),
    card('<font color="#377C6B"><b>PRODUCTION USE  /  ALIGN TECHNOLOGY</b></font><br/>ShipMatrix supports Align Technology\'s logistics operations.'),
    spacer(16),
    P('What the platform handles', 'sub'),
    grid([
        ('Data interpretation', 'Smart Adaptable Mapping learns how different source structures and values relate.'),
        ('Fulfillment workflows', 'Bulk processing, configurable handling, pick/pack workflows and order consolidation.'),
        ('Carrier-ready output', 'Transforms processed shipment data into carrier-specific export formats.'),
    ], bg=colors.white),
    spacer(12),
    P('<link href="https://shipmatrix.net" color="#377C6B">shipmatrix.net</link>', 'link'),
    PageBreak(),
])

# PAGE 2 - ENGINEERING DEPTH
story.extend([
    spacer(8),
    *section('01 / Engineering deep dive', 'Smart Adaptable Mapping (SAM)'),
    P('SAM uses a one-time, 18-question setup to interpret data structures, values and their relationships. When new files arrive, it checks those relationships against the actual upload and adapts the result accordingly.'),
    spacer(8),
    grid([
        ('Traditional template constraints', 'Each merchant must repeatedly reorganize their source export to match a rigid shipping template.'),
        ('SAM approach', 'One saved mapping interprets varied source files without requiring changes to the merchant\'s existing systems.'),
    ], widths=[CONTENT/2, CONTENT/2]),
    spacer(21),
    P('Two interpretation stages', 'sub'),
    grid([
        ('01 / One-time setup', 'Answer mapping questions. Interpret data structure, values and relationships, then save the configured model.'),
        ('02 / Every new upload', 'Reinterpret the incoming file; validate value relationships and adapt to actual columns or missing quantities.'),
    ], widths=[CONTENT/2, CONTENT/2], bg=colors.white),
    spacer(18),
    P('Three examples of structural differences', 'sub'),
    P('<b>Split address:</b> multiple address columns can be interpreted as a single delivery address.', 'small'),
    P('<b>Repeated items:</b> rows representing the same order/item can be consolidated under configured quantity rules.', 'small'),
    P('<b>Address reference:</b> a configured authoritative source can determine the correct delivery address.', 'small'),
    spacer(11),
    card('<b>Recorded operational scale</b><br/>231,719 consolidated shipments processed, representing approximately <b>1.39 million underlying orders</b>, based on an actual historical average of <b>6 orders per consolidated shipment</b>.', BLUE_PALE, 13),
    spacer(8),
    P('<b>Proven at increasing operational scale.</b> ShipMatrix handled a 4.8x year-over-year increase in June processing volume.', 'small'),
    P('23 months of recorded activity  |  1,100+ processing runs', 'small'),
    spacer(14),
    P('Business impact', 'sub'),
    P('This way, not a single change the merchant have to do in their systems to automate their shipments.'),
    PageBreak(),
])

# PAGE 3 - COMMERCE
story.extend([
    spacer(8),
    *section('02 / Reusable backend engineering', 'One architecture. Different businesses.'),
    P('I built a configurable commerce backend on Django, Django Oscar and PostgreSQL, designed for businesses with different products, pricing requirements and fulfillment models. Its reusable foundations can be configured rather than rewritten for each industry.'),
    spacer(7),
    grid([
        ('Reusable configuration', 'Option groups, values, levels and conditional pricing rules driven by database configuration.'),
        ('Server-authoritative pricing', 'The backend computes adjustments and validates totals instead of trusting browser-submitted prices.'),
        ('Operational architecture', 'Order workflows, localized Arabic/English behavior and integrations designed for real operational use.'),
    ], bg=colors.white),
    spacer(20),
    P('Django pricing-engine demo', 'sub'),
    P('A public, independently runnable extract of the pricing logic demonstrates jewelry, fashion and food configurations. It is <b>not</b> the private commerce platform, and contains no production data or credentials.'),
    P('The public repository includes <b>19 Django tests</b>, GitHub Actions checks and a downloadable tested demo artifact.', 'small'),
    P('<link href="https://github.com/MOHD97v/django-pricing-engine-demo" color="#377C6B">github.com/MOHD97v/django-pricing-engine-demo</link>', 'link'),
    spacer(14),
    P('YAGARZ', 'sub'),
    P('YAGARZ is a jewelry commerce application adopting the configurable backend foundation. Its presentation and customer experience are distinct from the publicly shared pricing-engine demo.'),
    spacer(14),
    card('<b>Engineering principle:</b> Build a reliable foundation once, then configure it for different businesses and operational constraints.'),
    PageBreak(),
])

# PAGE 4 - EXPERIENCE, DISCIPLINES, CONTACT
story.extend([
    spacer(8),
    *section('03 / Experience', 'Operational insight. Engineering ownership.'),
    P('<b>Creator &amp; Backend Engineer - ShipMatrix Solutions</b>   |   Oct 2023-present', 'sub'),
    P('Designed, developed and operated logistics automation infrastructure independently, processing more than 230,000 consolidated shipments.'),
    P('<b>Logistics Supervisor - Align Technology</b>   |   Mar 2024-Dec 2025', 'sub'),
    P('Automated approximately 30% of logistics workload across Saudi Arabia and the UAE using spreadsheet and workflow automations alongside enterprise operational responsibilities.'),
    P('<b>WMS / Systems Operations - Abudawood Logistics</b>   |   Feb 2021-May 2023', 'sub'),
    P('Warehouse-management systems and operational execution informed a pragmatic approach to automation and system reliability.'),
    spacer(12),
    *section('04 / Engineering mindset', 'Built for what happens after launch.'),
    P('Understand the real workflow first. Keep business logic authoritative. Build reusable capabilities. Own the full lifecycle from requirements through maintenance and support.', 'small'),
    spacer(10),
    P('Tools and disciplines', 'sub'),
    card('Python  /  JavaScript  /  Django  /  Django Oscar  /  PostgreSQL  /  MySQL  /  SQLite  /  GitHub Actions  /  CI/CD  /  Automated tests  /  Rule-driven pricing  /  Excel and CSV automation  /  ERP and WMS workflows  /  Cloudflare Pages and D1', BLUE_PALE),
    spacer(25),
    *section('05 / Get in touch', 'Have a difficult backend problem?'),
    P('Riyadh, Saudi Arabia  |  Backend software engineering and operational automation'),
    P('<link href="mailto:MFAlmutairimo@gmail.com" color="#377C6B">MFAlmutairimo@gmail.com</link>   |   +966 59 603 1170', 'link'),
    P('<link href="https://mohd97v.github.io/" color="#377C6B">mohd97v.github.io</link>   |   <link href="https://github.com/MOHD97v" color="#377C6B">github.com/MOHD97v</link>', 'link'),
])

pdf.build(story)
print(f'Portfolio PDF generated: {OUTPUT}, {OUTPUT.stat().st_size} bytes')