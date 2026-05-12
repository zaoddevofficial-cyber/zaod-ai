import base64
import json
import urllib.request
import urllib.error
import os

ACCESS_TOKEN = os.environ['GMAIL_ACCESS_TOKEN']
APP_URL = 'https://quantum-earn.base44.app'
PDF_URL = 'https://base44.app/api/apps/6a028c62767727bb348239f0/files/mp/public/6a028c62767727bb348239f0/4ba8c1142_QuantumEarn_Instructions.pdf'

def build_email_with_attachment(to, subject, html_body, pdf_url, pdf_filename):
    boundary = f"bound_{abs(hash(to)) & 0xffffffff}"
    
    with urllib.request.urlopen(pdf_url) as r:
        pdf_data = r.read()
    pdf_b64 = base64.b64encode(pdf_data).decode()

    parts = []
    parts.append(f"--{boundary}")
    parts.append("Content-Type: text/html; charset=UTF-8")
    parts.append("Content-Transfer-Encoding: base64")
    parts.append("")
    parts.append(base64.b64encode(html_body.encode('utf-8')).decode())
    parts.append(f"--{boundary}")
    parts.append(f'Content-Type: application/pdf; name="{pdf_filename}"')
    parts.append("Content-Transfer-Encoding: base64")
    parts.append(f'Content-Disposition: attachment; filename="{pdf_filename}"')
    parts.append("")
    parts.append(pdf_b64)
    parts.append(f"--{boundary}--")

    encoded_subject = "=?UTF-8?B?" + base64.b64encode(subject.encode('utf-8')).decode() + "?="
    
    raw = "\r\n".join([
        f"From: Quantum Earn <zaoddevofficial@gmail.com>",
        f"To: {to}",
        f"Subject: {encoded_subject}",
        f"MIME-Version: 1.0",
        f'Content-Type: multipart/mixed; boundary="{boundary}"',
        "",
    ] + parts)

    return base64.urlsafe_b64encode(raw.encode('utf-8')).decode().rstrip('=')

def send_email(to, subject, html):
    raw = build_email_with_attachment(to, subject, html, PDF_URL, "QuantumEarn_Instructions.pdf")
    payload = json.dumps({"raw": raw}).encode()
    req = urllib.request.Request(
        "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
        data=payload,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            print(f"✅ Sent to {to} | ID: {result.get('id')}")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ Failed {to}: {e.read().decode()}")
        return False

def email_template(title, body_html, cta_text, cta_link):
    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"/>
<style>
body{{font-family:Arial,sans-serif;background:#0a0a1a;color:#e0e0e0;margin:0;padding:0}}
.c{{max-width:600px;margin:40px auto;background:#12122a;border-radius:12px;overflow:hidden;border:1px solid #2a2a5a}}
.h{{background:linear-gradient(135deg,#6c63ff,#3ecfcf);padding:30px;text-align:center}}
.h h1{{margin:0;color:#fff;font-size:24px}}
.h p{{margin:5px 0 0;color:rgba(255,255,255,0.8);font-size:13px}}
.b{{padding:30px}}
.b p{{line-height:1.7;color:#c0c0d0}}
.step{{background:#1a1a3a;border-left:3px solid #6c63ff;padding:10px 15px;margin:8px 0;border-radius:4px;color:#e0e0e0;font-size:13px}}
.cta{{text-align:center;margin:30px 0}}
.cta a{{background:linear-gradient(135deg,#6c63ff,#3ecfcf);color:#fff;text-decoration:none;padding:14px 32px;border-radius:8px;font-weight:bold;font-size:15px}}
.f{{text-align:center;padding:20px;font-size:12px;color:#555577;border-top:1px solid #2a2a5a}}
</style></head>
<body><div class="c">
<div class="h"><h1>⚛️ Quantum Earn</h1><p>AI-Powered Investment Platform</p></div>
<div class="b"><h2 style="color:#6c63ff;">{title}</h2>{body_html}
<div class="cta"><a href="{cta_link}">{cta_text}</a></div></div>
<div class="f">&copy; 2026 Quantum Earn. All rights reserved.<br/>
<a href="{APP_URL}" style="color:#6c63ff;">quantum-earn.base44.app</a></div>
</div></body></html>"""

# Full onboarding email for new users
def get_onboarding_email(email):
    body = f"""
    <p>Hello! 👋 Welcome to <strong>Quantum Earn</strong> — the AI-powered investment platform.</p>
    <p>You're just <strong>3 simple steps</strong> away from growing your money with our smart AI strategies:</p>
    
    <div class="step">✅ <strong>Step 1 — Complete KYC Verification</strong><br/>
    Verify your identity to unlock all features.<br/>
    👉 <a href="{APP_URL}/kyc-verification" style="color:#3ecfcf;">quantum-earn.base44.app/kyc-verification</a></div>
    
    <div class="step">💳 <strong>Step 2 — Make Your First Deposit</strong><br/>
    Add funds to your wallet (JazzCash, EasyPaisa, Bank Transfer).<br/>
    👉 <a href="{APP_URL}/deposit" style="color:#3ecfcf;">quantum-earn.base44.app/deposit</a></div>
    
    <div class="step">📈 <strong>Step 3 — Start Investing</strong><br/>
    Choose an AI investment plan and watch your money grow!<br/>
    👉 <a href="{APP_URL}/investment-plans" style="color:#3ecfcf;">quantum-earn.base44.app/investment-plans</a></div>
    
    <p style="margin-top:20px;">We've attached a <strong>complete PDF guide</strong> with detailed instructions for each step. 📎</p>
    <p>Start today and let AI work for you! 🚀</p>
    """
    return email_template(
        "Welcome! Complete Your Setup & Start Earning 🎉",
        body,
        "🚀 Get Started Now",
        APP_URL
    )

users = [
    "dumar0472@gmail.com",
    "musmanmusman719@gmail.com",
    "musmansattar933@gmail.com",
]

print("Sending onboarding emails...\n")
for user_email in users:
    html = get_onboarding_email(user_email)
    send_email(
        user_email,
        "🎉 Welcome to Quantum Earn – Complete KYC, Deposit & Start Investing!",
        html
    )

print("\n✅ All done!")
