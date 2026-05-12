import { createClientFromRequest } from 'npm:@base44/sdk@0.8.25';

const OWNER_EMAIL = 'zaoddevofficial@gmail.com';
const APP_URL = 'https://quantum-earn.base44.app';

function buildMimeEmail(to: string, subject: string, htmlBody: string, fromName = 'Quantum Earn'): string {
  const fromEmail = OWNER_EMAIL;
  const boundary = 'boundary_qe_' + Date.now();
  const encodedSubject = `=?UTF-8?B?${btoa(unescape(encodeURIComponent(subject)))}?=`;

  const raw = [
    `From: ${fromName} <${fromEmail}>`,
    `To: ${to}`,
    `Subject: ${encodedSubject}`,
    `MIME-Version: 1.0`,
    `Content-Type: multipart/alternative; boundary="${boundary}"`,
    '',
    `--${boundary}`,
    'Content-Type: text/html; charset=UTF-8',
    'Content-Transfer-Encoding: base64',
    '',
    btoa(unescape(encodeURIComponent(htmlBody))),
    '',
    `--${boundary}--`,
  ].join('\r\n');

  return btoa(unescape(encodeURIComponent(raw)))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

async function sendEmail(accessToken: string, to: string, subject: string, html: string) {
  const encoded = buildMimeEmail(to, subject, html);
  const res = await fetch('https://gmail.googleapis.com/gmail/v1/users/me/messages/send', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ raw: encoded }),
  });
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Gmail API error: ${err}`);
  }
  return res.json();
}

function emailTemplate(title: string, body: string, ctaText: string, ctaLink: string): string {
  return `
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"/>
<style>
  body { font-family: Arial, sans-serif; background: #0a0a1a; color: #e0e0e0; margin: 0; padding: 0; }
  .container { max-width: 600px; margin: 40px auto; background: #12122a; border-radius: 12px; overflow: hidden; border: 1px solid #2a2a5a; }
  .header { background: linear-gradient(135deg, #6c63ff, #3ecfcf); padding: 30px; text-align: center; }
  .header h1 { margin: 0; color: #fff; font-size: 24px; }
  .header p { margin: 5px 0 0; color: rgba(255,255,255,0.8); font-size: 13px; }
  .body { padding: 30px; }
  .body p { line-height: 1.7; color: #c0c0d0; }
  .cta { text-align: center; margin: 30px 0; }
  .cta a { background: linear-gradient(135deg, #6c63ff, #3ecfcf); color: #fff; text-decoration: none; padding: 14px 32px; border-radius: 8px; font-weight: bold; font-size: 15px; }
  .footer { text-align: center; padding: 20px; font-size: 12px; color: #555577; border-top: 1px solid #2a2a5a; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>⚛️ Quantum Earn</h1>
    <p>AI-Powered Investment Platform</p>
  </div>
  <div class="body">
    <h2 style="color:#6c63ff;">${title}</h2>
    ${body}
    <div class="cta">
      <a href="${ctaLink}">${ctaText}</a>
    </div>
  </div>
  <div class="footer">
    &copy; 2026 Quantum Earn. All rights reserved.<br/>
    <a href="${APP_URL}" style="color:#6c63ff;">quantum-earn.base44.app</a>
  </div>
</div>
</body>
</html>`;
}

Deno.serve(async (req) => {
  try {
    const base44 = createClientFromRequest(req);
    const body = await req.json().catch(() => ({}));
    const { type, user_email, user_name, extra } = body;

    // Get Gmail access token
    const { accessToken } = await base44.asServiceRole.connectors.getConnection('gmail');

    let subject = '';
    let html = '';
    let ownerSubject = '';
    let ownerHtml = '';
    let sendToOwner = false;

    switch (type) {

      case 'kyc_pending': {
        subject = '⚠️ Complete Your KYC Verification – Quantum Earn';
        html = emailTemplate(
          'Your KYC Verification is Pending',
          `<p>Hello <strong>${user_name || user_email}</strong>,</p>
           <p>Welcome to <strong>Quantum Earn</strong>! We noticed you haven't completed your <strong>KYC (Know Your Customer)</strong> verification yet.</p>
           <p>KYC verification is required to:</p>
           <ul style="color:#c0c0d0;">
             <li>Make deposits and investments</li>
             <li>Withdraw your earnings</li>
             <li>Access all platform features</li>
           </ul>
           <p>It only takes a few minutes. Please complete your verification now to get started.</p>`,
          '✅ Complete KYC Now',
          `${APP_URL}/kyc-verification`
        );
        break;
      }

      case 'kyc_approved': {
        subject = '🎉 KYC Verified Successfully – Quantum Earn';
        html = emailTemplate(
          'KYC Verification Approved! 🎉',
          `<p>Hello <strong>${user_name || user_email}</strong>,</p>
           <p>Great news! Your <strong>KYC verification has been approved</strong>. Your account is now fully verified.</p>
           <p>You can now:</p>
           <ul style="color:#c0c0d0;">
             <li>✅ Make deposits</li>
             <li>✅ Start investing in AI-powered plans</li>
             <li>✅ Withdraw your earnings</li>
           </ul>
           <p>Start your investment journey today and let AI work for you!</p>`,
          '🚀 Start Investing Now',
          `${APP_URL}/investment-plans`
        );
        break;
      }

      case 'plan_expired': {
        subject = '⏰ Your Investment Plan Has Expired – Quantum Earn';
        html = emailTemplate(
          'Your Investment Plan Has Expired',
          `<p>Hello <strong>${user_name || user_email}</strong>,</p>
           <p>Your investment plan <strong>${extra?.plan_name || 'Active Plan'}</strong> has completed its <strong>1-month period</strong>.</p>
           <p>Your returns have been calculated and added to your wallet. You can now:</p>
           <ul style="color:#c0c0d0;">
             <li>💰 Withdraw your earnings</li>
             <li>🔄 Re-invest in a new plan</li>
             <li>📈 Upgrade to a higher-tier plan</li>
           </ul>
           <p>Don't let your money sit idle — start a new plan today!</p>`,
          '📈 View Investment Plans',
          `${APP_URL}/investment-plans`
        );
        break;
      }

      case 'no_deposit': {
        subject = '💳 Make Your First Deposit – Quantum Earn';
        html = emailTemplate(
          'Ready to Start? Make Your First Deposit!',
          `<p>Hello <strong>${user_name || user_email}</strong>,</p>
           <p>Your account is set up, but you haven't made a deposit yet. <strong>Your investment journey starts with just one step!</strong></p>
           <p>With Quantum Earn you get:</p>
           <ul style="color:#c0c0d0;">
             <li>🤖 AI-powered investment strategies</li>
             <li>📊 Transparent returns tracking</li>
             <li>🔒 Secure & verified platform</li>
           </ul>
           <p>Make your first deposit today and start earning!</p>`,
          '💳 Make a Deposit',
          `${APP_URL}/deposit`
        );
        break;
      }

      case 'no_investment': {
        subject = '📊 Start Investing Today – Quantum Earn';
        html = emailTemplate(
          'You Haven\'t Invested Yet – Don\'t Miss Out!',
          `<p>Hello <strong>${user_name || user_email}</strong>,</p>
           <p>You have funds in your wallet but haven't started investing yet. <strong>Your money could be working for you right now!</strong></p>
           <p>Choose from our AI-powered investment plans:</p>
           <ul style="color:#c0c0d0;">
             <li>⚡ Starter Plan – Low risk, steady returns</li>
             <li>🌟 Growth Plan – Balanced risk & reward</li>
             <li>🚀 Premium Plan – Maximum returns</li>
           </ul>
           <p>Start investing today and watch your portfolio grow!</p>`,
          '🚀 View Investment Plans',
          `${APP_URL}/investment-plans`
        );
        break;
      }

      case 'kyc_applied_owner': {
        ownerSubject = `🔔 New KYC Application – ${user_name || user_email}`;
        ownerHtml = emailTemplate(
          'New KYC Application Received',
          `<p>A user has submitted a <strong>KYC verification request</strong>.</p>
           <table style="width:100%; border-collapse:collapse; margin:15px 0;">
             <tr><td style="padding:8px; color:#888; width:140px;">Name:</td><td style="padding:8px; color:#e0e0e0;"><strong>${user_name || 'N/A'}</strong></td></tr>
             <tr style="background:#1a1a3a;"><td style="padding:8px; color:#888;">Email:</td><td style="padding:8px; color:#e0e0e0;">${user_email}</td></tr>
           </table>
           <p>Please review and approve/reject the application.</p>`,
          '🔍 Review KYC Application',
          `${APP_URL}/admin`
        );
        sendToOwner = true;
        break;
      }

      case 'deposit_made_owner': {
        ownerSubject = `💰 New Deposit – ${user_name || user_email} – €${extra?.amount || '?'}`;
        ownerHtml = emailTemplate(
          'New Deposit Received',
          `<p>A user has made a <strong>deposit request</strong>.</p>
           <table style="width:100%; border-collapse:collapse; margin:15px 0;">
             <tr><td style="padding:8px; color:#888; width:140px;">User:</td><td style="padding:8px; color:#e0e0e0;"><strong>${user_name || user_email}</strong></td></tr>
             <tr style="background:#1a1a3a;"><td style="padding:8px; color:#888;">Email:</td><td style="padding:8px; color:#e0e0e0;">${user_email}</td></tr>
             <tr><td style="padding:8px; color:#888;">Amount:</td><td style="padding:8px; color:#3ecfcf;"><strong>€${extra?.amount || 'N/A'}</strong></td></tr>
             <tr style="background:#1a1a3a;"><td style="padding:8px; color:#888;">Method:</td><td style="padding:8px; color:#e0e0e0;">${extra?.method || 'N/A'}</td></tr>
           </table>
           <p>Please review and process this deposit.</p>`,
          '💳 Review Deposit',
          `${APP_URL}/admin`
        );
        sendToOwner = true;
        break;
      }

      default:
        return Response.json({ error: 'Unknown email type' }, { status: 400 });
    }

    if (sendToOwner) {
      await sendEmail(accessToken, OWNER_EMAIL, ownerSubject, ownerHtml);
      return Response.json({ ok: true, sent_to: OWNER_EMAIL, type });
    } else {
      await sendEmail(accessToken, user_email, subject, html);
      return Response.json({ ok: true, sent_to: user_email, type });
    }

  } catch (error) {
    return Response.json({ error: error.message }, { status: 500 });
  }
});
