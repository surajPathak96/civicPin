from fastapi import APIRouter, Form, HTTPException
from db import get_conn

router = APIRouter()

CATEGORIES = {"waterlogging", "drain", "pothole", "garbage", "other"}
SEVERITIES = {"low", "medium", "high"}

@router.post("/reports", status_code=201)
def create_report(
    lat: float = Form(...),
    lng: float = Form(...),
    category: str = Form(...),
    severity: str = Form(...),
    description: str = Form(""),
):
    if category not in CATEGORIES:
        raise HTTPException(422, f"category must be one of {sorted(CATEGORIES)}")
    if severity not in SEVERITIES:
        raise HTTPException(422, f"severity must be one of {sorted(SEVERITIES)}")
    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        raise HTTPException(422, "invalid coordinates")

    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO reports (lat, lng, category, severity, description) "
            "VALUES (?, ?, ?, ?, ?)",
            (lat, lng, category, severity, description.strip()[:500]),
        )
        row = conn.execute(
            "SELECT * FROM reports WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
    return dict(row)

@router.get("/reports")
def list_reports():
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT *,
                   CAST(julianday(COALESCE(resolved_at, 'now'))
                        - julianday(created_at) AS INTEGER) AS days_open
            FROM reports
            ORDER BY created_at ASC
        """).fetchall()
    return [dict(r) for r in rows]


