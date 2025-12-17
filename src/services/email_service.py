import os
import smtplib
from email.message import EmailMessage

BRAND_NAME = "Portal Académico"
SUPPORT_EMAIL = "soporte@portal-academico.local"  # opcional

def send_email_otp(to_email: str, otp_code: str) -> None:
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    pwd  = os.getenv("SMTP_PASS")

    if not user or not pwd:
        raise RuntimeError("Faltan SMTP_USER / SMTP_PASS en .env")

    msg = EmailMessage()
    msg["Subject"] = f" Tu código de verificación – {BRAND_NAME}"
    msg["From"] = f"{BRAND_NAME} <{user}>"
    msg["To"] = to_email

    # Texto plano (fallback)
    msg.set_content(
        f"{BRAND_NAME}\n\n"
        f"Tu código de verificación es: {otp_code}\n"
        f"Expira en 5 minutos.\n\n"
        f"Si no solicitaste este código, ignora este correo."
    )

    # HTML (table-based + inline styles)
    preheader = f"Tu código es {otp_code} (expira en 5 minutos)."
    html = f"""\
<!doctype html>
<html>
  <body style="margin:0;padding:0;background:#f4f6f8;">
    <div style="display:none;max-height:0;overflow:hidden;opacity:0;color:transparent;">
      {preheader}
    </div>

    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f4f6f8;padding:24px 0;">
      <tr>
        <td align="center">
          <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="width:600px;max-width:92%;background:#ffffff;border-radius:14px;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,.08);">

            <!-- Header -->
            <tr>
              <td style="padding:22px 26px;background:linear-gradient(135deg,#1f6feb,#6f42c1);">
                <table role="presentation" width="100%">
                  <tr>
                    <td style="font-family:Arial,sans-serif;color:#fff;">
                      <div style="font-size:16px;opacity:.95;">{BRAND_NAME}</div>
                      <div style="font-size:22px;font-weight:700;margin-top:4px;">Verificación de inicio de sesión</div>
                    </td>
                    <td align="right" style="font-family:Arial,sans-serif;color:#fff;">
                      <div style="width:40px;height:40px;border-radius:12px;background:rgba(255,255,255,.18);display:inline-block;text-align:center;line-height:40px;font-weight:700;">
                        PA
                      </div>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>

            <!-- Body -->
            <tr>
              <td style="padding:26px;font-family:Arial,sans-serif;color:#111827;">
                <p style="margin:0 0 12px;font-size:14px;color:#374151;">
                  Usa este código para continuar con tu autenticación:
                </p>

                <div style="text-align:center;margin:18px 0 18px;">
                  <div style="display:inline-block;padding:14px 18px;border:1px solid #e5e7eb;border-radius:12px;background:#f9fafb;">
                    <span style="font-size:30px;letter-spacing:8px;font-weight:800;color:#111827;">
                      {otp_code}
                    </span>
                  </div>
                </div>

                <p style="margin:0;font-size:13px;color:#6b7280;">
                  Este código expira en <b>5 minutos</b>. Si no fuiste tú, ignora este correo.
                </p>

                <div style="margin-top:18px;padding:14px;border-radius:12px;background:#f3f4f6;color:#374151;font-size:12px;">
                  <b>Tip:</b> No compartas este código con nadie.
                </div>
              </td>
            </tr>

            <!-- Footer -->
            <tr>
              <td style="padding:18px 26px;font-family:Arial,sans-serif;color:#6b7280;font-size:12px;background:#fafafa;border-top:1px solid #eee;">
                Si necesitas ayuda, responde a este correo o contacta: {SUPPORT_EMAIL}
              </td>
            </tr>

          </table>

          <div style="font-family:Arial,sans-serif;color:#9ca3af;font-size:11px;margin-top:12px;">
            © {BRAND_NAME}
          </div>
        </td>
      </tr>
    </table>
  </body>
</html>
"""
    msg.add_alternative(html, subtype="html")

    with smtplib.SMTP(host, port) as server:
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.send_message(msg)
