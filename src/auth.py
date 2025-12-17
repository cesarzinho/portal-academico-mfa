from flask import Blueprint, render_template, request, redirect, session, url_for
import bcrypt
from datetime import datetime, timedelta, timezone
from db import get_conn
from services.otp_services import generate_otp, store_otp, verify_otp
from services.email_service import send_email_otp
from services.sms_service import send_sms_otp
from flask import Blueprint, render_template, request, redirect, session, url_for, flash


auth_bp = Blueprint("auth", __name__)

def _now():
    return datetime.now(timezone.utc)

@auth_bp.get("/register")
def register_form():
    return render_template("register.html")

@auth_bp.post("/register")
def register_post():
    username = request.form["username"]
    email = request.form["email"]
    phone = request.form["phone"]
    password = request.form["password"]

    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (username, email, phone, password_hash)
                VALUES (%s, %s, %s, %s)
            """, (username, email, phone, pw_hash))

    return redirect(url_for("auth.login_form"))

@auth_bp.get("/login")
def login_form():
    return render_template("login.html")

@auth_bp.post("/login")
def login_post():
    username = request.form["username"]
    password = request.form["password"]

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, email, phone, password_hash FROM users WHERE username=%s", (username,))
            row = cur.fetchone()

    if not row:
        return "Usuario no existe", 401

    user_id, email, phone, pw_hash = row
    if not bcrypt.checkpw(password.encode(), pw_hash.encode()):
        return "Password incorrecta", 401

    expires = _now() + timedelta(minutes=15)
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO login_flows (user_id, stage, expires_at)
                VALUES (%s, 'PENDING_EMAIL', %s)
                RETURNING id
            """, (user_id, expires))
            flow_id = cur.fetchone()[0]

    session["flow_id"] = str(flow_id)

    code = generate_otp()
    store_otp(flow_id, "email", code)
    send_email_otp(email, code)

    return redirect(url_for("auth.verify_email_form"))

@auth_bp.get("/verify-email")
def verify_email_form():
    return render_template("verify_email.html")

@auth_bp.post("/verify-email")
def verify_email_post():
    flow_id = session.get("flow_id")
    code = request.form["code"].strip()

    if not flow_id:
        return redirect(url_for("auth.login_form"))

    ok, reason = verify_otp(flow_id, "email", code)

    if not ok:
        if reason == "locked":
            flash("Demasiados intentos. Inicia sesión de nuevo.", "error")
            session.clear()
            return redirect(url_for("auth.login_form"))
        if reason == "expired":
            flash("El código expiró. Presiona Reenviar.", "error")
            return redirect(url_for("auth.verify_email_form"))

        flash("Código incorrecto.", "error")
        return redirect(url_for("auth.verify_email_form"))

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE login_flows SET stage='PENDING_SMS', updated_at=NOW()
                WHERE id=%s
                RETURNING user_id
            """, (flow_id,))
            user_id = cur.fetchone()[0]

            cur.execute("SELECT phone FROM users WHERE id=%s", (user_id,))
            phone = cur.fetchone()[0]

    sms_code = generate_otp()
    store_otp(flow_id, "sms", sms_code)
    send_sms_otp(phone, sms_code)

    return redirect(url_for("auth.verify_sms_form"))


@auth_bp.get("/verify-sms")
def verify_sms_form():
    return render_template("verify_sms.html")

@auth_bp.post("/verify-sms")
def verify_sms_post():
    flow_id = session.get("flow_id")
    code = request.form.get("code", "").strip()

    if not flow_id:
        return redirect(url_for("auth.login_form"))

    ok, reason = verify_otp(flow_id, "sms", code)

    if not ok:
        if reason == "locked":
            flash("Demasiados intentos. Inicia sesión de nuevo.", "error")
            session.clear()
            return redirect(url_for("auth.login_form"))
        if reason == "expired":
            flash("El código expiró. Presiona Reenviar.", "error")
            return redirect(url_for("auth.verify_sms_form"))

        flash("Código incorrecto.", "error")
        return redirect(url_for("auth.verify_sms_form"))

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE login_flows SET stage='AUTHENTICATED', updated_at=NOW()
                WHERE id=%s
            """, (flow_id,))

    session["authed"] = True
    flash("Verificación completada correctamente ", "success")
    return redirect(url_for("dashboard"))


@auth_bp.post("/resend-email")
def resend_email():
    flow_id = session.get("flow_id")
    if not flow_id:
        return redirect(url_for("auth.login_form"))

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id, stage FROM login_flows WHERE id=%s", (flow_id,))
            row = cur.fetchone()
            if not row:
                return redirect(url_for("auth.login_form"))
            user_id, stage = row
            if stage != "PENDING_EMAIL":
                return redirect(url_for("auth.login_form"))

            cur.execute("SELECT email FROM users WHERE id=%s", (user_id,))
            email = cur.fetchone()[0]

    code = generate_otp()
    store_otp(flow_id, "email", code)
    send_email_otp(email, code)

    flash("Te enviamos un nuevo código al correo.", "success")
    return redirect(url_for("auth.verify_email_form"))


@auth_bp.post("/resend-sms")
def resend_sms():
    flow_id = session.get("flow_id")
    if not flow_id:
        return redirect(url_for("auth.login_form"))

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT user_id, stage FROM login_flows WHERE id=%s", (flow_id,))
            row = cur.fetchone()
            if not row:
                return redirect(url_for("auth.login_form"))
            user_id, stage = row
            if stage != "PENDING_SMS":
                return redirect(url_for("auth.login_form"))

            cur.execute("SELECT phone FROM users WHERE id=%s", (user_id,))
            phone = cur.fetchone()[0]

    code = generate_otp()
    store_otp(flow_id, "sms", code)
    send_sms_otp(phone, code)

    flash("Te enviamos un nuevo código por SMS.", "success")
    return redirect(url_for("auth.verify_sms_form"))


@auth_bp.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login_form"))
