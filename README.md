*Portal Académico con Autenticación MFA (Password + Email OTP + SMS OTP)
Descripción general*

Este proyecto es un portal académico que implementa un flujo de autenticación con 3 factores (MFA):

1. Contraseña

2. ódigo OTP por correo

3. Código OTP por SMS

El objetivo es aumentar la seguridad del inicio de sesión usando OTP con expiración, hash del código, límite de intentos, y opción de reenviar código.

- Tecnologías principales

- Python 3.x

- Flask

- PostgreSQL (pgAdmin)

- SMTP (Gmail App Password) para envío de correo

- Twilio para envío de SMS

- HTML + CSS + JS (UI moderna + animación flip en login/register)

portal-academico-mfa/
├── src/
│   ├── app.py
│   ├── auth.py
│   ├── db.py
│   └── services/
│       ├── otp_service.py
│       ├── email_service.py
│       └── sms_service.py
│
├── static/
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── flip.js
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── verify_email.html
│   ├── verify_sms.html
│   └── dashboard.html
│
├── database/
│   └── (opcional, pero como nose guardaron scripts o backups se dejo vacio)
│
├── docs/
├── venv/
├── requirements.txt
├── .env              
└── README.md

Requisitos previos

- Python 3.x

- PostgreSQL instalado (y pgAdmin)

- Cuenta Gmail con App Password habilitada (para SMTP)

- Cuenta Twilio (Trial funciona, pero requiere:

 - número verificado

 - geo permissions habilitadas

 - formato E.164 para teléfonos)

1, clonar repositorio:
git clone https://github.com/cesarzinho/portal-academico-mfa.git
cd portal-academico-mfa

2, creamos y activamos el entorno virtual
python -m venv venv
venv\Scripts\activate

3, deependencias
pip install -r requirements.txt

4, creamos la database por ejemplo llamada portal_mfa
ejecutamos el script ubicado en database/portalDataBase

5, creamos el .env:
por ejemplo, asi:
# App
FLASK_SECRET_KEY=una_clave_larga
DATABASE_URL=postgresql://postgres:TU_CLAVE@localhost:5432/portal_mfa

# Email SMTP (Gmail)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tu_correo@gmail.com
SMTP_PASS=tu_app_password_sin_espacios

# Twilio SMS
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_FROM_NUMBER=+1867xxxxxxx

6, ejecutamos:
python -m flask --app src/app.py run


Flujo MFA (cómo funciona)

1. Usuario ingresa usuario + contraseña, o se registra con la informacion pertinente

2. Si es correcto → se crea un login_flow en estado PENDING_EMAIL

3. Se genera OTP email, se guarda como hash en otp_challenges y se envía por SMTP

4. Usuario verifica email → pasa a PENDING_SMS

6. Se genera OTP SMS y se envía por Twilio

7. Usuario verifica SMS → flujo queda AUTHENTICATED y entra al home/dashboard

8. Si hay demasiados intentos se bloquea el challenge y se solicita iniciar sesión de nuevo


Componentes principales

src/auth.py: rutas de login/registro/verificación y reenvío

src/services/otp_service.py: generación y validación OTP (hash, expiración, intentos)

src/services/email_service.py: envío OTP por correo (HTML)

src/services/sms_service.py: envío OTP por SMS (Twilio)

Seguridad implementada

OTP con expiración (TTL)

OTP guardado como hash, no texto plano

Límite de intentos (max_attempts)

Reenvío de códigos (email y SMS)

Validación y normalización de números telefónicos

Troubleshooting

Gmail: usa App Password, no tu contraseña normal

Twilio Trial:

verifica tu número “To”

habilita Geo Permissions del país

usa formato E.164


