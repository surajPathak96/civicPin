from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db import init_db
from routers import reports

app = FastAPI(title="CivicPin")
init_db()
app.include_router(reports.router)

# Must be LAST
# : serves the frontend from the same origin, so no CORS setup needed
FRONTEND = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND, html=True), name="frontend")