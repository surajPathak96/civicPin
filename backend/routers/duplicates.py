from fastapi import APIRouter, HTTPException
from db import get_conn

router = APIRouter()

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