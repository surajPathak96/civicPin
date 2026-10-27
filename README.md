# CivicPin

Residents report civic issues (waterlogging, drains, potholes, garbage) on a map.
Unlike a plain report form, CivicPin shows how long each issue has been open and
merges duplicate reports of the same problem, so real hotspots stand out.
Scoped to <locality> as a learning project.

## Team
- <name> (P1: reports core)
- <name> (P2: duplicates + list)
- <name> (P3: admin + stats)

## Run locally
```bash
git clone <repo-url> && cd civicpin
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cd backend
uvicorn main:app --reload
```
Open http://127.0.0.1:8000 (app) or http://127.0.0.1:8000/docs (API explorer).

## Fixed values
- category: `waterlogging` | `drain` | `pothole` | `garbage` | `other`
- severity: `low` | `medium` | `high`
- status: `open` | `resolved`
- Timestamps are UTC strings: `YYYY-MM-DD HH:MM:SS`
- Errors: `{"detail": "<message>"}` with HTTP 4xx

## Report object
| Field | Type | Notes |
|---|---|---|
| id | int | |
| lat, lng | float | |
| category, severity, status | string | see fixed values |
| description | string | max 500 chars |
| photo_path | string or null | |
| report_count | int | starts at 1, +1 per confirmation |
| created_at | string | |
| resolved_at | string or null | |
| days_open | int | **only in GET responses**, computed |

## Endpoints

### Done (Day 1)

**POST /reports**: multipart form: `lat`, `lng`, `category`, `severity`, `description` (optional)
→ `201` report object (without `days_open`)
```json
<paste your real response here>
```
→ `422` invalid category, severity, or coordinates
```json
<paste your real error here>
```

**GET /reports**
→ `200` array of report objects (with `days_open`), oldest first
```json
<paste your real response here>
```

### Planned (owner changes the row to "Done" when merged)

| Endpoint | Owner | Request | Response |
|---|---|---|---|
| POST /reports (add photo) | P1 | extra optional form field `photo` (JPEG/PNG, max 5 MB) | report object; 422 if wrong type or too large |
| GET /reports?category=&severity=&status= | P2 | optional query filters | array of report objects |
| GET /reports/nearby?lat=&lng=&category= | P2 | query params | open reports of that category within 50 m, each with extra `distance_m` |
| POST /reports/{id}/confirm | P2 | none | updated report object (`report_count` + 1); 404 if missing |
| PATCH /reports/{id} | P3 | JSON `{"status": "resolved"}`, header `X-Admin-Key` | updated report; sets `resolved_at`; 401 bad key, 404 missing |
| DELETE /reports/{id} | P3 | header `X-Admin-Key` | 204; 401 bad key, 404 missing |
| GET /stats | P3 | none | `{"total":int,"open":int,"resolved":int,"by_category":{...},"avg_days_to_resolve":number or null}` |

## Rules
1. Changing an endpoint's request or response means editing this README **in the same commit**.
2. Only edit your own files (see the slice table); ask the owner for changes elsewhere.
3. `main` must always run.

## Decisions (Day 1)
- Locality: <name> (center: <lat>, <lng>)
- Slices: P1 <name> (reports core), P2 <name> (duplicates + list), P3 <name> (admin + stats)
- Photo storage: local `backend/uploads/` for now; revisit on Day 4
- Daily check-in: <time>; chat: <where>
- Rubric / rules from organizers: <answers, or "still waiting">

## Open decisions
- Hosting provider and photo persistence (Day 4)