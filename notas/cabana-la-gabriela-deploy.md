---
title: Deploy — Cabaña La Gabriela
date: 2026-03-17
tags: [deploy, render, fastapi, static-site, cabana-la-gabriela]
status: active
related: [[Projects/cabana-la-gabriela/README]], [[fastapi-sqlite-rest-api]]
---

# Deploy: Cabaña La Gabriela

Guía de despliegue completo en Render.com (gratis).

## Arquitectura de deploy

```
render.com
├── Static Site  →  web/          (frontend)
└── Web Service  →  backend/      (API FastAPI)
    └── Persistent Disk  →  reservas.db
```

## Pasos — Frontend

1. Conectar repositorio GitHub a Render
2. Crear **Static Site**
3. Root directory: `web/`
4. Publish directory: `.`

## Pasos — Backend

1. Crear **Web Service**
2. Root directory: `backend/`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Agregar **Persistent Disk** en `/data`
6. Variable de entorno: `DB_PATH=/data/reservas.db`

## Cambiar contraseña admin

```python
import hashlib
print(hashlib.sha256("NUEVA_CLAVE".encode()).hexdigest())
```
Variable de entorno en Render: `ADMIN_PASSWORD_HASH=<el hash>`

## Conectar frontend con API

En `web/js/main.js` y `web/admin.html`:
```js
const API = 'https://TU-BACKEND.onrender.com';
```

## Dominio personalizado

Comprar dominio → DNS → apuntar a la URL del Static Site en Render.

> [!warning] Backend en Render gratis
> El servicio gratuito de Render se "duerme" después de 15 min de inactividad. Para producción real, usar plan de pago o Railway.

## Referencias
- [[Projects/cabana-la-gabriela/README]]
- [[fastapi-sqlite-rest-api]]
