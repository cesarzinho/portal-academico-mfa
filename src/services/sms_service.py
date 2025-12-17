import os
from twilio.rest import Client

def normalize_phone(phone: str) -> str:
    p = phone.strip().replace(" ", "").replace("-", "")
    if p.startswith("+"):
        return p
    if p.isdigit():
        return "+" + p
    return p

def send_sms_otp(to_phone: str, otp_code: str) -> None:
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")

    if not all([account_sid, auth_token, from_number]):
        raise RuntimeError("Faltan variables TWILIO_* en .env")

    to_phone = normalize_phone(to_phone)
    from_number = normalize_phone(from_number)

    client = Client(account_sid, auth_token)
    client.messages.create(
        body=f"CiberSeguridad: tu código es {otp_code}. Expira en 5 minutos.",
        from_=from_number,
        to=to_phone
    )
