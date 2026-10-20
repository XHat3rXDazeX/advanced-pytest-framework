import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# Initialize Document
pdf_path = "Harsukh_Dhaliwal_QA_Automation_Resume.pdf"
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=40, rightMargin=40, topMargin=40, bottomMargin=40,
    title="Harsukh Dhaliwal - QA Automation Engineer Resume"
)

styles = getSampleStyleSheet()
story = []

PRIMARY_COLOR = colors.HexColor("#1A365D")   # Deep Slate Blue
TEXT_COLOR = colors.HexColor("#2D3748")      # Charcoal

# Typography Styling Layout Parameters
styles.add(ParagraphStyle(name='DocTitle', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=PRIMARY_COLOR, alignment=1))
styles.add(ParagraphStyle(name='ContactInfo', fontName='Helvetica', fontSize=9, leading=13, textColor=TEXT_COLOR, alignment=1))
styles.add(ParagraphStyle(name='SectionHeading', fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=PRIMARY_COLOR, spaceBefore=8, spaceAfter=2, keepWithNext=True))
styles.add(ParagraphStyle(name='BodyBold', fontName='Helvetica-Bold', fontSize=9.5, leading=13, textColor=TEXT_COLOR))
styles.add(ParagraphStyle(name='BodyTextCustom', fontName='Helvetica', fontSize=9.5, leading=13, textColor=TEXT_COLOR))
styles.add(ParagraphStyle(name='BulletText', fontName='Helvetica', fontSize=9.5, leading=13.5, textColor=TEXT_COLOR, leftIndent=12, bulletIndent=4, spaceAfter=2))

# Header Block
story.append(Paragraph("HARSUKH DHALIWAL", styles['DocTitle']))
story.append(Paragraph("Brampton, ON | 289-952-9329 | harsukhd2002@gmail.com | https://github.com/XHat3rXDazeX/advanced-pytest-framework", styles['ContactInfo']))

def add_divider(title_text):
    t = Table([[Paragraph(title_text, styles['SectionHeading'])]], colWidths=[532])
    t.setStyle(TableStyle([('LINEBELOW', (0,0), (-1,-1), 1, PRIMARY_COLOR), ('BOTTOMPADDING', (0,0), (-1,-1), 2), ('TOPPADDING', (0,0), (-1,-1), 6)]))
    story.append(t)

# 1. Technical Profile Section
add_divider("TECHNICAL SKILLS")
skills_data = [
    [Paragraph("Languages & Core Engines:", styles['BodyBold']), Paragraph("Python, SQL, HTML5, CSS3, JavaScript", styles['BodyTextCustom'])],
    [Paragraph("Automation Frameworks:", styles['BodyBold']), Paragraph("Pytest, Playwright (Sync/Async), Selenium WebDriver", styles['BodyTextCustom'])],
    [Paragraph("Architecture & Testing Patterns:", styles['BodyBold']), Paragraph("Page Object Model (POM), API Interception & Mocking, Data-Driven Testing", styles['BodyTextCustom'])],
    [Paragraph("DevOps & Infrastructure:", styles['BodyBold']), Paragraph("GitHub Actions, CI/CD Cloud Pipelines, Git, VS Code, Linux (Ubuntu)", styles['BodyTextCustom'])],
]
t_skills = Table(skills_data, colWidths=[160, 372])
t_skills.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 1), ('BOTTOMPADDING', (0,0), (-1,-1), 1)]))
story.append(Spacer(1, 4))
story.append(t_skills)

# 2. Portfolio Project Section
add_divider("QA AUTOMATION PROJECT CENTERPIECE")
story.append(Spacer(1, 4))
story.append(Paragraph("<b>Lead SDET & Framework Architect</b> | Open-Source Git Portfolio Project", styles['BodyBold']))
story.append(Paragraph("<i>Enterprise Hybrid UI & API Test Automation Platform Framework</i>", styles['BodyTextCustom']))
story.append(Spacer(1, 4))
story.append(Paragraph("&bull; <b>Engineered Modular Page Object Models (POM):</b> Completely decoupled dynamic web DOM element paths from core testing assertions using object-oriented Python classes, slashing scripting maintenance overhead by 50% across functional suites.", styles['BulletText']))
story.append(Paragraph("&bull; <b>Implemented Isolated Browser-Level API Mocking:</b> Architected offline test routing wrappers via browser tab network context intercepts; defeated environment network dependencies and cloud server request latency to achieve fast, isolated execution loops.", styles['BulletText']))
story.append(Paragraph("&bull; <b>Orchestrated GitHub Actions Cloud Pipelines:</b> Formulated automated branch-tracking workflows (`main.yml`) that auto-provision clean Ubuntu virtual nodes, install package environments, pull web browsers, and push live build status badges.", styles['BulletText']))
story.append(Paragraph("&bull; <b>Constructed Data-Driven Configurations:</b> Structured a secure, override baseline framework (`pytest.ini` / `settings.py`) to fully filter background execution noise and safely handle credentials without hardcoding source secrets.", styles['BulletText']))

# 3. Professional Experience Section
add_divider("PROFESSIONAL EXPERIENCE")
story.append(Spacer(1, 4))
story.append(Table([[Paragraph("<b>Logistics Operator & Client Service Specialist</b> | <i>Independent Contractor</i>", styles['BodyBold']), Paragraph("<b>2020 – Present</b>", styles['BodyTextCustom'])]], colWidths=[400, 132], style=[('ALIGN', (1,0), (1,0), 'RIGHT')]))
story.append(Paragraph("&bull; Systematically audited high-volume inventory accuracy and tracked logistical transport data parameters prior to routing, maintaining a 100% precision and compliance rate across thousands of client data packets.", styles['BulletText']))
story.append(Paragraph("&bull; Leveraged on-the-spot technical hardware troubleshooting and critical thinking to resolve systemic delivery constraints, preserving top-tier client safety metrics.", styles['BulletText']))

story.append(Spacer(1, 4))
story.append(Table([[Paragraph("<b>Operations Crew Member</b> | <i>Wendy's</i>", styles['BodyBold']), Paragraph("<b>May 2022 – Oct 2022</b>", styles['BodyTextCustom'])]], colWidths=[400, 132], style=[('ALIGN', (1,0), (1,0), 'RIGHT')]))
story.append(Paragraph("&bull; Executed rapid point-of-sale (POS) financial transaction entries and data transfers with extreme accuracy under strict, fast-paced time constraints.", styles['BulletText']))
story.append(Paragraph("&bull; Coordinated with cross-functional service teams to monitor operational workflows and uphold stringent quality control and visual inventory hygiene benchmarks.", styles['BulletText']))

story.append(Spacer(1, 4))
story.append(Table([[Paragraph("<b>Office Assistant</b> | <i>Woodwal Law Office</i>", styles['BodyBold']), Paragraph("<b>Feb 2019 – Jun 2019</b>", styles['BodyTextCustom'])]], colWidths=[400, 132], style=[('ALIGN', (1,0), (1,0), 'RIGHT')]))
story.append(Paragraph("&bull; Managed the systematic entry, categorization, and secure indexing of physical and digital business files into reference databases, maintaining data integrity with zero discrepancies.", styles['BulletText']))

# 4. Education Section
add_divider("EDUCATION & COMP-SCI BACKGROUND")
story.append(Spacer(1, 4))
story.append(Table([[Paragraph("<b>Bachelor of Science Coursework (Computer Science Focus)</b>", styles['BodyBold']), Paragraph("<b>2021 – 2023</b>", styles['BodyTextCustom'])]], colWidths=[400, 132], style=[('ALIGN', (1,0), (1,0), 'RIGHT')]))
story.append(Paragraph("<i>Wilfrid Laurier University – Waterloo, ON</i>", styles['BodyTextCustom']))
story.append(Spacer(1, 2))
story.append(Paragraph("&bull; Completed intensive academic fundamentals in core Object-Oriented Programming (OOP) architectures, function layouts, condition execution loops, script logic syntax, and programmatic problem-solving.", styles['BulletText']))

doc.build(story)
print("SUCCESS: Harsukh_Dhaliwal_QA_Automation_Resume.pdf has been generated successfully!")
