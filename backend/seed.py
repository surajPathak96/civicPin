import sys
from db import get_conn, init_db

CENTER =  (20.5937, 78.9629)  # TODO: same as START in map.js

# (lat offset, lng offset, category, severity, description, days_ago, days_to_resolve or None)
# 0.001 degrees is roughly 100 m. TODO Day 4: replace offsets with real spots in your locality.
SEED = [
    ( 0.0010,  0.0005, "waterlogging", "high",   "Water stays after every rain", 12, None),
    ( 0.0012,  0.0006, "drain",        "medium", "Drain blocked with plastic",    9, None),
    (-0.0008,  0.0010, "pothole",      "high",   "Deep pothole near the gate",    7, None),
    (-0.0015, -0.0004, "garbage",      "low",    "Garbage pile at the corner",    3, 2),
    ( 0.0004, -0.0011, "pothole",      "medium", "Cracked road edge",            15, 6),
    # TODO: add 15+ more so the map looks alive
]

def main():
    init_db()
    force = "--force" in sys.argv
    with get_conn() as conn:
        n = conn.execute("SELECT COUNT(*) FROM reports").fetchone()[0]
        if n and not force:
            sys.exit(f"DB already has {n} reports. Use --force to wipe and reseed.")
        if force:
            conn.execute("DELETE FROM reports")
        for dlat, dlng, cat, sev, desc, days_ago, to_resolve in SEED:
            created = f"-{days_ago} days"
            # datetime('now', NULL) returns NULL, so open reports get resolved_at = NULL
            resolved = None if to_resolve is None else f"-{days_ago - to_resolve} days"
            conn.execute(
                "INSERT INTO reports (lat, lng, category, severity, description, status, "
                "created_at, resolved_at) VALUES (?, ?, ?, ?, ?, ?, datetime('now', ?), datetime('now', ?))",
                (CENTER[0] + dlat, CENTER[1] + dlng, cat, sev, desc,
                 "open" if to_resolve is None else "resolved", created, resolved),
            )
    print("Seeded.")

if __name__ == "__main__":
    main()