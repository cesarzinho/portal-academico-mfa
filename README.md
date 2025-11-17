\# Portal Académico con Autenticación MFA



\## Descripción general



Este proyecto es un \*\*portal académico\*\* que implementa un sistema de autenticación con

\*\*Multi-Factor Authentication (MFA)\*\* utilizando códigos OTP (One-Time Password).

El objetivo es proporcionar un flujo de inicio de sesión más seguro para usuarios

del sistema académico.



El backend está desarrollado con \*\*Flask (Python)\*\* y utiliza \*\*SQLite\*\* como base de datos

ligera para desarrollo.



---



\## Tecnologías principales



\- Python 3.x

\- Flask

\- SQLite

\- HTML5, CSS3, JavaScript

\- (Opcional) Librerías para envío de correos / generación de OTP



---



\## Estructura del proyecto



```text

portal-academico-mfa/

├── src/

│   ├── models/        # Modelos de datos (Usuario, Sesión, etc.)

│   ├── controllers/   # Controladores / lógica de rutas

│   ├── services/      # Servicios (OTP, email, seguridad)

│   └── utils/         # Utilidades y validadores

│

├── static/

│   ├── css/           # Estilos CSS

│   ├── js/            # Lógica JS del frontend

│   └── img/           # Imágenes estáticas

│

├── templates/         # Vistas HTML (login, verify\_otp, dashboard, etc.)

│

├── database/          # Archivos relacionados a la BD (schema.sql, portal.db)

│

├── docs/

│   └── diagramas/     # Diagramas de arquitectura, flujo MFA, modelo de BD

│

└── tests/             # Pruebas unitarias



Requisitos previos:



Python 3.x instalado

pip (gestor de paquetes de Python)

(Opcional pero recomendado) Entorno virtual: venv



Configuración del entorno:



Clonar el repositorio

git clone https://github.com/cesarzinho/portal-academico-mfa.git

cd portal-academico-mfa

Crear y activar un entorno virtual (opcional)

python -m venv venv

En Windows:



venv\\Scripts\\activate



Instalar dependencias:



Cuando exista el archivo requirements.txt:

pip install -r requirements.txt



Variables de entorno:



Las variables de entorno se gestionan a través de un archivo .env en la raíz

del proyecto (no debe versionarse en Git).



Flujo de autenticación y MFA (visión general)



1. El usuario ingresa sus credenciales (usuario y contraseña).



2\. El sistema valida las credenciales.



3\. Si son correctas, se genera un código OTP (por ejemplo, enviado por email).



4\. El usuario introduce el código OTP en la pantalla de verificación.



5\. Si el OTP es válido y no ha expirado, se concede acceso al sistema.



Los componentes principales involucrados serán:



-controllers/auth\_controller.py

Maneja las rutas de login, logout y verificación de OTP.



-services/otp\_service.py

Generación, almacenamiento temporal y validación de códigos OTP.



-services/email\_service.py

Envío de correos con el código OTP al usuario.



-models/usuario.py y models/sesion.py

Representan los usuarios y las sesiones activas en la base de datos



Base de datos



La carpeta database/ contendrá:



schema.sql: script de creación de tablas (usuarios, sesiones, tokens OTP, etc.).



portal.db: archivo de base de datos SQLite (no versionado en Git, recomendado

agregarlo a .gitignore).

