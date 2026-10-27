from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db import init_db
from routers import reports, duplicates, admin

app = FastAPI(title="CivicPin")
init_db()

app.include_router(reports.router)
app.include_router(duplicates.router)
app.include_router(admin.router)

BASE = Path(__file__).parent
UPLOADS = BASE / "uploads"
UPLOADS.mkdir(exist_ok=True)

# Order matters: the "/" mount catches everything, so it must be LAST
app.mount("/uploads", StaticFiles(directory=UPLOADS), name="uploads")
app.mount("/", StaticFiles(directory=BASE.parent / "frontend", html=True), name="frontend")