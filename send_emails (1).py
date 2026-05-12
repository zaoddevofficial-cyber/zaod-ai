import base64
import json
import urllib.request
import urllib.error
import os

ACCESS_TOKEN = os.environ['GMAIL_ACCESS_TOKEN']
APP_URL = 'https://quantum-earn.base44.app'
PDF_URL = 'https://base44.app/api/apps/6a028c62767727bb348239f0/files/mp/public/6a028c62767727bb348239f0/4ba8c1142_QuantumEarn_Instructions.pdf'

def build_email_with_attachment(to, subject, html_body, pdf_url, pdf_filename):
    boundary = f"bound_{hash(to) & 0xffffffff}"
    
    # Download PDF
    with urllib.request.urlopen(pdf_url) as r:
        pdf_data = r.read()
    pdf_b64 = base64.b64encode(pdf_data).decode()

    # Build multipart MIME
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

def send_email(to, subject, html, pdf_url, pdf_filename):
    raw = build_email_with_attachment(to, subject, html, pdf_url, pdf_filename)
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

# =====================
# EMAILS TO SEND
# =====================

# 1. zaoddevofficial@gmail.com — has deposit but NO investment
invest_html = email_template(
    "Start Investing Today! 🚀",
    """<p>Hello <strong>Zoad Official</strong>,</p>
    <p>Great news — your deposit has been approved and your wallet is ready! But we noticed you <strong>haven't started investing yet</strong>.</p>
    <p><strong>Your money could be growing right now!</strong> Choose from our AI-powered investment plans and start earning today:</p>
    <ul style="color:#c0c0d0;">
      <li>⚡ <b>Starter Plan</b> — Low risk, steady returns</li>
      <li>🌟 <b>Growth Plan</b> — Balanced risk & reward</li>
      <li>🚀 <b>Premium Plan</b> — Maximum returns</li>
    </ul>
    <p>We've attached a full <strong>step-by-step instructions guide</strong> (PDF) to help you get started easily. 📎</p>""",
    "🚀 Invest Now",
    f"{APP_URL}/investment-plans"
)

send_email(
    "zaoddevofficial@gmail.com",
    "🚀 Start Investing – Your Wallet is Ready! – Quantum Earn",
    invest_html,
    PDF_URL,
    "QuantumEarn_Instructions.pdf"
)

print("\nAll emails sent!")
