from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT

doc = SimpleDocTemplate(
    "/app/QuantumEarn_Instructions.pdf",
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)

# Colors
purple = colors.HexColor('#6c63ff')
teal = colors.HexColor('#3ecfcf')
dark = colors.HexColor('#12122a')
light_gray = colors.HexColor('#f0f0f8')
white = colors.white

styles = getSampleStyleSheet()

title_style = ParagraphStyle('Title', fontSize=22, textColor=purple, alignment=TA_CENTER, spaceAfter=6, fontName='Helvetica-Bold')
subtitle_style = ParagraphStyle('Subtitle', fontSize=12, textColor=teal, alignment=TA_CENTER, spaceAfter=20, fontName='Helvetica')
heading_style = ParagraphStyle('Heading', fontSize=14, textColor=purple, spaceAfter=6, spaceBefore=16, fontName='Helvetica-Bold')
body_style = ParagraphStyle('Body', fontSize=10, textColor=colors.HexColor('#333333'), spaceAfter=6, leading=16, fontName='Helvetica')
step_style = ParagraphStyle('Step', fontSize=10, textColor=colors.HexColor('#222222'), spaceAfter=4, leading=15, leftIndent=15, fontName='Helvetica')
note_style = ParagraphStyle('Note', fontSize=9, textColor=colors.HexColor('#555577'), spaceAfter=4, leading=13, leftIndent=10, fontName='Helvetica-Oblique')

story = []

# Header
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph("⚛️ QUANTUM EARN", title_style))
story.append(Paragraph("AI-Powered Investment Platform — User Instructions", subtitle_style))
story.append(HRFlowable(width="100%", thickness=2, color=purple, spaceAfter=16))

# Intro
story.append(Paragraph("Welcome to Quantum Earn!", heading_style))
story.append(Paragraph(
    "Quantum Earn is an AI-powered investment platform that lets you grow your money with smart, automated strategies. "
    "Follow the steps below to get started and start earning today.",
    body_style
))

# Step 1: Register
story.append(HRFlowable(width="100%", thickness=1, color=light_gray, spaceAfter=8))
story.append(Paragraph("📝 Step 1 — Register Your Account", heading_style))
story.append(Paragraph("1. Go to: <b><font color='#6c63ff'>https://quantum-earn.base44.app</font></b>", step_style))
story.append(Paragraph("2. Click on <b>Sign Up</b> or <b>Register</b>.", step_style))
story.append(Paragraph("3. Enter your email address and create a password.", step_style))
story.append(Paragraph("4. Verify your email if required.", step_style))

# Step 2: KYC
story.append(HRFlowable(width="100%", thickness=1, color=light_gray, spaceAfter=8))
story.append(Paragraph("✅ Step 2 — Complete KYC Verification", heading_style))
story.append(Paragraph(
    "KYC (Know Your Customer) verification is required before you can deposit or invest. It protects your account and ensures platform security.",
    body_style
))
story.append(Paragraph("1. Go to: <b><font color='#6c63ff'>https://quantum-earn.base44.app/kyc-verification</font></b>", step_style))
story.append(Paragraph("2. Fill in your <b>Full Name</b> and <b>ID Number (CNIC)</b>.", step_style))
story.append(Paragraph("3. Upload a clear photo of your <b>CNIC Front</b>.", step_style))
story.append(Paragraph("4. Upload a clear photo of your <b>CNIC Back</b>.", step_style))
story.append(Paragraph("5. Upload a <b>Selfie</b> holding your CNIC.", step_style))
story.append(Paragraph("6. Select your <b>Country</b> and submit.", step_style))
story.append(Paragraph("⏱ Verification is usually approved within 24 hours. You will receive a confirmation email once approved.", note_style))

# Step 3: Deposit
story.append(HRFlowable(width="100%", thickness=1, color=light_gray, spaceAfter=8))
story.append(Paragraph("💳 Step 3 — Make a Deposit", heading_style))
story.append(Paragraph("1. Go to: <b><font color='#6c63ff'>https://quantum-earn.base44.app/deposit</font></b>", step_style))
story.append(Paragraph("2. Choose your <b>payment method</b> (JazzCash, EasyPaisa, Bank Transfer, etc.).", step_style))
story.append(Paragraph("3. Enter the amount you want to deposit (minimum as shown on the platform).", step_style))
story.append(Paragraph("4. Complete the payment and upload the <b>payment screenshot</b> as proof.", step_style))
story.append(Paragraph("5. Submit — your deposit will be reviewed and approved shortly.", step_style))
story.append(Paragraph("💡 Your deposit amount in PKR will be auto-converted to EUR at the current exchange rate.", note_style))

# Step 4: Invest
story.append(HRFlowable(width="100%", thickness=1, color=light_gray, spaceAfter=8))
story.append(Paragraph("📈 Step 4 — Start Investing", heading_style))
story.append(Paragraph("1. Go to: <b><font color='#6c63ff'>https://quantum-earn.base44.app/investment-plans</font></b>", step_style))
story.append(Paragraph("2. Browse the available AI investment plans.", step_style))
story.append(Paragraph("3. Choose a plan that suits your budget and risk preference.", step_style))
story.append(Paragraph("4. Enter the amount you wish to invest and confirm.", step_style))
story.append(Paragraph("5. Your investment will start working immediately!", step_style))

# Plans table
story.append(Spacer(1, 0.3*cm))
plan_data = [
    ['Plan', 'Risk Level', 'Duration', 'Est. Return'],
    ['⚡ Starter', 'Low', '30 Days', 'Steady'],
    ['🌟 Growth', 'Medium', '30 Days', 'Balanced'],
    ['🚀 Premium', 'High', '30 Days', 'Maximum'],
]
plan_table = Table(plan_data, colWidths=[4.5*cm, 3.5*cm, 3.5*cm, 3.5*cm])
plan_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), purple),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 10),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 9),
    ('BACKGROUND', (0,1), (-1,1), light_gray),
    ('BACKGROUND', (0,2), (-1,2), white),
    ('BACKGROUND', (0,3), (-1,3), light_gray),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [light_gray, white]),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#ddddee')),
    ('TOPPADDING', (0,0), (-1,-1), 7),
    ('BOTTOMPADDING', (0,0), (-1,-1), 7),
]))
story.append(plan_table)

# Step 5: Withdraw
story.append(HRFlowable(width="100%", thickness=1, color=light_gray, spaceAfter=8))
story.append(Paragraph("💰 Step 5 — Withdraw Your Earnings", heading_style))
story.append(Paragraph("1. Go to: <b><font color='#6c63ff'>https://quantum-earn.base44.app/withdraw</font></b>", step_style))
story.append(Paragraph("2. Enter the amount you want to withdraw.", step_style))
story.append(Paragraph("3. Enter your payment details (JazzCash/EasyPaisa number or bank account).", step_style))
story.append(Paragraph("4. Submit the withdrawal request.", step_style))
story.append(Paragraph("5. Withdrawals are processed by the admin within 24–48 hours.", step_style))

# Important Notes
story.append(HRFlowable(width="100%", thickness=1, color=light_gray, spaceAfter=8))
story.append(Paragraph("⚠️ Important Notes", heading_style))
notes = [
    "• Complete KYC before attempting to deposit or invest.",
    "• All amounts are displayed in EUR (Euro) on the platform.",
    "• PKR deposits are converted to EUR automatically.",
    "• Keep your login credentials safe — never share your password.",
    "• Contact support through the platform if you face any issues.",
    "• Investment returns are estimated and subject to market conditions.",
]
for note in notes:
    story.append(Paragraph(note, step_style))

# Footer
story.append(Spacer(1, 0.5*cm))
story.append(HRFlowable(width="100%", thickness=2, color=teal, spaceAfter=8))
story.append(Paragraph(
    "🌐 <b>Website:</b> https://quantum-earn.base44.app  |  📧 <b>Support:</b> zaoddevofficial@gmail.com",
    ParagraphStyle('Footer', fontSize=9, textColor=colors.HexColor('#555577'), alignment=TA_CENTER)
))
story.append(Paragraph(
    "© 2026 Quantum Earn — AI-Powered Investment Platform. All rights reserved.",
    ParagraphStyle('FooterSub', fontSize=8, textColor=colors.HexColor('#888899'), alignment=TA_CENTER, spaceBefore=4)
))

doc.build(story)
print("PDF generated successfully!")
