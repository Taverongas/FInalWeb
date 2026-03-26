---
title: Proyecto Cabaña La Gabriela — Página Web
date: 2026-03-17
tags: [project, web, html, css, javascript, fastapi, colombia]
status: active
related: [[cabana-la-gabriela-tasks]], [[fastapi-sqlite-rest-api]], [[cabana-la-gabriela-deploy]]
---

# Proyecto: Cabaña La Gabriela — Página Web

**Estado**: 🟢 Activo
**Stack**: HTML5, CSS3, JavaScript (Vanilla), FastAPI (Python), SQLite
**Inicio**: 2026-03-17
**Meta**: Página web completa para alquiler vacacional de cabaña frente al mar

---

## 📁 Estructura del Proyecto

```
cabana-la-gabriela/
├── web/                          ← Frontend (HTML/CSS/JS)
│   ├── index.html                ← Página principal (Hero dron, secciones)
│   ├── habitaciones.html         ← Detalle de 7 habitaciones en 3 pisos
│   ├── galeria.html              ← Galería de fotos y video dron
│   ├── lugares.html              ← Playas y destinos cercanos
│   ├── como-llegar.html          ← Direcciones + Google Maps embed
│   ├── reservas.html             ← Formulario de reserva → WhatsApp
│   ├── reserva-exitosa.html      ← Página de confirmación
│   ├── admin.html                ← Panel administrador
│   ├── css/
│   │   └── styles.css            ← Estilos compartidos (design system)
│   ├── js/
│   │   └── main.js               ← JS principal (nav, animaciones, form)
│   └── img/                      ← Imágenes (agregar aquí)
│       ├── hero.jpg
│       ├── fachada.jpg
│       ├── habitacion.jpg
│       └── extra1-extra8.jpg
└── backend/
    ├── app.py                    ← FastAPI + SQLite
    ├── requirements.txt
    └── render.yaml               ← Config para deploy en Render
```

---

## 🚀 Correr Localmente

### Frontend (sin backend)
Abre `web/index.html` directamente en el navegador. Funciona sin servidor.

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

API disponible en: `http://localhost:8000`
Docs automáticas: `http://localhost:8000/docs`

### Con backend activo, actualizar en main.js:
```js
const API = 'http://localhost:8000';
```

---

## 📸 Agregar Fotos

1. Copia tus fotos a `web/img/`
2. En cada `<div class="gallery-item__media">` reemplaza el emoji por:
   ```html
   <img src="img/tu-foto.jpg" alt="Descripción" loading="lazy">
   ```
3. En `index.html` hero, reemplaza el fallback:
   ```html
   <img src="img/hero.jpg" alt="Vista del mar" class="hero__fallback">
   ```

---

## 🎬 Video del Dron

El archivo `drone.MP4` es demasiado grande para GitHub (>100MB). Opciones:

### YouTube (recomendado — gratis)
1. Sube el video a YouTube como "No listado"
2. En `galeria.html`, reemplaza el div `.video-placeholder` por:
```html
<iframe width="100%" style="aspect-ratio:16/9;"
  src="https://www.youtube.com/embed/TU_VIDEO_ID?rel=0"
  frameborder="0" allowfullscreen></iframe>
```
3. Para el hero en `index.html`, pon el video en `<source src="...">` dentro del `<video>`.

### Cloudinary (también gratis hasta cierto límite)
1. Sube en cloudinary.com
2. Usa la URL directa en el `<source src="TU_URL.mp4">` del `<video>`

---

## 🔐 Panel Administrador

URL: `/admin.html`
Contraseña por defecto: `gabriela2025`

**Para cambiar la contraseña:**
```python
import hashlib
print(hashlib.sha256("TU_NUEVA_CONTRASEÑA".encode()).hexdigest())
```
Copia el hash resultante en la variable de entorno `ADMIN_PASSWORD_HASH` en Render.

---

## 🌐 Deploy en Render

### Frontend (estático)
1. Crea un "Static Site" en render.com
2. Apunta al directorio `web/`
3. Publish directory: `.` (o `web/`)

### Backend (API)
1. Crea un "Web Service" en render.com
2. Apunta al directorio `backend/`
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Agrega disk persistente para `reservas.db`
6. Configura `ADMIN_PASSWORD_HASH` como variable de entorno

### Conectar frontend con backend
En `web/js/main.js`, cambia:
```js
const API = 'https://TU-BACKEND.onrender.com';
```

---

## 📱 Información de Contacto

- **WhatsApp**: +57 313 754 9732
- **Instagram**: @lagabriela06
- **TikTok**: @la_gabriela06
- **Facebook**: Cabaña La Gabriela
- **Ubicación GPS**: 9.35933, -76.00764
- **Dirección**: Playa Venado, ruta entre Moñitos y San Bernardo del Viento, Córdoba

---

## ✅ Tareas Pendientes

- [ ] Agregar fotos reales a `web/img/`
- [ ] Subir video dron a YouTube / Cloudinary y actualizar embed
- [ ] Crear logo y reemplazar emoji 🌴 en navbar
- [ ] Crear página de Facebook "Cabaña La Gabriela"
- [ ] Comprar dominio (ej: cabanalabgabriela.com)
- [ ] Deploy en Render (frontend + backend)
- [ ] Cambiar contraseña admin por defecto
- [ ] Configurar correos automáticos (opcional: usar SendGrid o Resend)
