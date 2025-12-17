import random
import bcrypt
from datetime import datetime, timedelta, timezone
from db import get_conn

OTP_TTL_MIN = 5
MAX_ATTEMPTS = 5

def _now():
    return datetime.now(timezone.utc)

def generate_otp() -> str:
    return f"{random.randint(0, 999999):06d}"

def store_otp(flow_id: str, channel: str, otp_code: str) -> None:
    code_hash = bcrypt.hashpw(otp_code.encode(), bcrypt.gensalt()).decode()
    expires_at = _now() + timedelta(minutes=OTP_TTL_MIN)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO otp_challenges (flow_id, channel, code_hash, expires_at, attempts, max_attempts)
                VALUES (%s, %s, %s, %s, 0, %s)
            """, (flow_id, channel, code_hash, expires_at, MAX_ATTEMPTS))

def verify_otp(flow_id: str, channel: str, otp_code: str):
    """
    Returns: (ok: bool, reason: str)
    reason in: ok | missing | used | expired | locked | invalid
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, code_hash, expires_at, attempts, max_attempts, consumed_at
                FROM otp_challenges
                WHERE flow_id=%s AND channel=%s
                ORDER BY created_at DESC
                LIMIT 1
            """, (flow_id, channel))
            row = cur.fetchone()

            if not row:
                return False, "missing"

            otp_id, code_hash, expires_at, attempts, max_attempts, consumed_at = row

            if consumed_at is not None:
                return False, "used"
            if _now() > expires_at:
                return False, "expired"
            if attempts >= max_attempts:
                return False, "locked"

            ok = bcrypt.checkpw(otp_code.encode(), code_hash.encode())

            if ok:
                cur.execute("UPDATE otp_challenges SET consumed_at = NOW() WHERE id=%s", (otp_id,))
                return True, "ok"

            # solo suma intento si falló
            cur.execute("UPDATE otp_challenges SET attempts = attempts + 1 WHERE id=%s", (otp_id,))
            return False, "invalid"
