"""
Cabaña La Gabriela — Backend FastAPI
API de reservas con SQLite
"""

from fastapi import FastAPI, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
import sqlite3
import csv
import io
import os
import hashlib
import secrets

# =====================================================
# CONFIGURACIÓN
# =====================================================

DB_PATH = os.getenv("DB_PATH", "reservas.db")
ADMIN_PASSWORD_HASH = os.getenv(
    "ADMIN_PASSWORD_HASH",
    hashlib.sha256("gabriela2025".encode()).hexdigest()   # contraseña por defecto
)

app = FastAPI(
    title="Cabaña La Gabriela — API",
    description="API de gestión de reservas para Cabaña La Gabriela",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # En producción restringir a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# BASE DE DATOS
# =====================================================

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre          TEXT NOT NULL,
            telefono        TEXT NOT NULL,
            correo          TEXT,
            modalidad       TEXT NOT NULL DEFAULT 'cotizacion',
            num_habitaciones INTEGER,
            tipo_habitacion  TEXT DEFAULT 'indiferente',
            piso            TEXT DEFAULT 'indiferente',
            fecha_entrada   TEXT,
            fecha_salida    TEXT,
            huespedes       INTEGER,
            mensaje         TEXT,
            estado          TEXT NOT NULL DEFAULT 'pendiente',
            fecha_creacion  TEXT NOT NULL DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()
    conn.close()


init_db()

# =====================================================
# MODELOS
# =====================================================

class ReservaCreate(BaseModel):
    nombre:          str
    telefono:        str
    correo:          Optional[str] = None
    modalidad:       str = "cotizacion"
    num_habitaciones: Optional[int] = None
    tipo_habitacion: Optional[str] = "indiferente"
    piso:            Optional[str] = "indiferente"
    fecha_entrada:   Optional[str] = None
    fecha_salida:    Optional[str] = None
    huespedes:       Optional[int] = None
    mensaje:         Optional[str] = None
    estado:          str = "pendiente"


class EstadoUpdate(BaseModel):
    estado: str   # pendiente | confirmada | cancelada


class AdminLogin(BaseModel):
    password: str


# =====================================================
# HELPERS
# =====================================================

def row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)


VALID_ESTADOS = {"pendiente", "confirmada", "cancelada"}

# =====================================================
# ENDPOINTS — RESERVAS
# =====================================================

@app.post("/api/reservas", status_code=201)
def crear_reserva(reserva: ReservaCreate, db: sqlite3.Connection = Depends(get_db)):
    """Crea una nueva reserva (desde el formulario del frontend)."""
    cur = db.execute("""
        INSERT INTO reservas
            (nombre, telefono, correo, modalidad, num_habitaciones,
             tipo_habitacion, piso, fecha_entrada, fecha_salida,
             huespedes, mensaje, estado)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        reserva.nombre, reserva.telefono, reserva.correo,
        reserva.modalidad, reserva.num_habitaciones,
        reserva.tipo_habitacion, reserva.piso,
        reserva.fecha_entrada, reserva.fecha_salida,
        reserva.huespedes, reserva.mensaje, reserva.estado
    ))
    db.commit()
    new_id = cur.lastrowid
    row = db.execute("SELECT * FROM reservas WHERE id = ?", (new_id,)).fetchone()
    return row_to_dict(row)


@app.get("/api/reservas")
def listar_reservas(
    estado: Optional[str] = Query(None),
    q:      Optional[str] = Query(None, description="Buscar por nombre, teléfono, correo o mensaje"),
    limit:  int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: sqlite3.Connection = Depends(get_db)
):
    """Lista todas las reservas con filtros opcionales."""
    base_sql = "SELECT * FROM reservas WHERE 1=1"
    params: list = []

    if estado and estado in VALID_ESTADOS:
        base_sql += " AND estado = ?"
        params.append(estado)

    if q:
        base_sql += """ AND (
            nombre   LIKE ? OR
            telefono LIKE ? OR
            correo   LIKE ? OR
            mensaje  LIKE ?
        )"""
        like = f"%{q}%"
        params.extend([like, like, like, like])

    count_sql = base_sql.replace("SELECT *", "SELECT COUNT(*)")
    total = db.execute(count_sql, params).fetchone()[0]

    base_sql += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    rows = db.execute(base_sql, params).fetchall()
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": [row_to_dict(r) for r in rows]
    }


@app.get("/api/reservas/stats")
def estadisticas(db: sqlite3.Connection = Depends(get_db)):
    """Estadísticas rápidas del panel admin."""
    total      = db.execute("SELECT COUNT(*) FROM reservas").fetchone()[0]
    pendientes = db.execute("SELECT COUNT(*) FROM reservas WHERE estado='pendiente'").fetchone()[0]
    confirmadas= db.execute("SELECT COUNT(*) FROM reservas WHERE estado='confirmada'").fetchone()[0]
    canceladas = db.execute("SELECT COUNT(*) FROM reservas WHERE estado='cancelada'").fetchone()[0]
    return {
        "total": total,
        "pendientes": pendientes,
        "confirmadas": confirmadas,
        "canceladas": canceladas,
    }


@app.get("/api/reservas/{reserva_id}")
def obtener_reserva(reserva_id: int, db: sqlite3.Connection = Depends(get_db)):
    row = db.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return row_to_dict(row)


@app.patch("/api/reservas/{reserva_id}/estado")
def cambiar_estado(
    reserva_id: int,
    body: EstadoUpdate,
    db: sqlite3.Connection = Depends(get_db)
):
    """Cambia el estado de una reserva."""
    if body.estado not in VALID_ESTADOS:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Opciones: {VALID_ESTADOS}")
    result = db.execute(
        "UPDATE reservas SET estado = ? WHERE id = ?",
        (body.estado, reserva_id)
    )
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    row = db.execute("SELECT * FROM reservas WHERE id = ?", (reserva_id,)).fetchone()
    return row_to_dict(row)


@app.delete("/api/reservas/{reserva_id}", status_code=204)
def eliminar_reserva(reserva_id: int, db: sqlite3.Connection = Depends(get_db)):
    """Elimina una reserva."""
    result = db.execute("DELETE FROM reservas WHERE id = ?", (reserva_id,))
    db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return None


@app.get("/api/reservas/exportar/csv")
def exportar_csv(db: sqlite3.Connection = Depends(get_db)):
    """Exporta todas las reservas a CSV."""
    rows = db.execute("SELECT * FROM reservas ORDER BY id DESC").fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Nombre", "Teléfono", "Correo", "Modalidad",
        "Núm. Habitaciones", "Tipo Hab.", "Piso",
        "Entrada", "Salida", "Huéspedes", "Mensaje", "Estado", "Creado"
    ])
    for row in rows:
        writer.writerow([
            row["id"], row["nombre"], row["telefono"], row["correo"],
            row["modalidad"], row["num_habitaciones"], row["tipo_habitacion"],
            row["piso"], row["fecha_entrada"], row["fecha_salida"],
            row["huespedes"], row["mensaje"], row["estado"], row["fecha_creacion"]
        ])

    output.seek(0)
    filename = f"reservas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


# =====================================================
# ENDPOINT — ADMIN LOGIN (simple, stateless)
# =====================================================

@app.post("/api/admin/login")
def admin_login(body: AdminLogin):
    """Verifica la contraseña de administrador."""
    hashed = hashlib.sha256(body.password.encode()).hexdigest()
    if hashed == ADMIN_PASSWORD_HASH:
        token = secrets.token_hex(32)
        return {"ok": True, "token": token}
    raise HTTPException(status_code=401, detail="Contraseña incorrecta")


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/")
def root():
    return {
        "app": "Cabaña La Gabriela — API",
        "version": "1.0.0",
        "status": "ok"
    }


@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}
