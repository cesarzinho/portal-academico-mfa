import os
from flask import Flask, render_template, session, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

from auth import auth_bp

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev")

app.register_blueprint(auth_bp)

@app.get("/")
def home():
    return redirect(url_for("auth.login_form"))

@app.get("/dashboard")
def dashboard():
    if not session.get("authed"):
        return redirect(url_for("auth.login_form"))
    return render_template("dashboard.html")
