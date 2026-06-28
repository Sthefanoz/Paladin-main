# Paladin — Gestión de activos y riesgos cibernéticos

Aplicativo web (Django) que automatiza una metodología de gestión de riesgos:
valoración de activos, identificación de riesgos, tratamiento (ISO/IEC 27002:2022),
cálculo de riesgo residual, comunicación (reportes) y monitoreo (panel).

## Requisitos previos

- **Python 3.12 o superior** (descargar de https://www.python.org/downloads/).
  Durante la instalación, marcar la casilla **"Add Python to PATH"**.

## Cómo ejecutarlo (paso a paso)

Abrir una terminal en la carpeta del proyecto y ejecutar:

```bash
# 1. Instalar Django
pip install -r requirements.txt

# 2. Entrar a la carpeta del proyecto Django
cd Paladin

# 3. (Opcional) Aplicar migraciones. La base de datos ya viene cargada,
#    pero esto no hace daño si se ejecuta.
python manage.py migrate

# 4. Iniciar el servidor
python manage.py runserver
```

Luego abrir en el navegador: **http://127.0.0.1:8000/**

La aplicación requiere **iniciar sesión**. La primera vez, ir a
**http://127.0.0.1:8000/cuentas/registro/** para crear una cuenta.

> En Windows, si `python` no funciona, usar `py` en su lugar
> (por ejemplo: `py manage.py runserver`).

## Estructura

- `Paladin/activos/` — registro y valoración de activos (CIA).
- `Paladin/riesgos/` — riesgos, amenazas, vulnerabilidades, controles ISO,
  panel de monitoreo y reporte.
- `Paladin/db.sqlite3` — base de datos SQLite (incluye datos de ejemplo precargados).

## Panel de administración (opcional)

Para usar el admin de Django, crear un usuario:

```bash
python manage.py createsuperuser
```

y entrar a http://127.0.0.1:8000/admin/
