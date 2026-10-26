# CivicPin API Contract

## The Report object

```json
{
  "id": 1,
  "lat": 26.9124,
  "lng": 75.7873,
  "category": "pothole",
  "severity": "High",
  "description": "Deep pothole near the bus stop",
  "photo_path": null,
  "status": "Open",
  "created_at": "2026-10-25T10:30:00Z"
}
```

Allowed values:
- category: waterlogging, drain, pothole, garbage
- severity: Low, Med, High
- status: Open, Resolved



## POST /reports
Create a new report.

Request body (JSON):
```json
{
  "lat": 26.9124,
  "lng": 75.7873,
  "category": "pothole",
  "severity": "High",
  "description": "Deep pothole near the bus stop"
}
```

Success: `201 Created`. Returns the full Report object, including the new `id`, `status: "Open"` and `created_at`.

Failure: `400 Bad Request`. Returns:
```json
{ "error": "category must be one of: waterlogging, drain, pothole, garbage" }
```

## GET /reports
List reports. All filters are optional.

Example: `GET /reports?category=pothole&severity=High&status=Open`

Query parameters:
- category: waterlogging | drain | pothole | garbage
- severity: Low | Med | High
- status: Open | Resolved

Success: `200 OK`. Returns a JSON array of Report objects (newest first).
If nothing matches, returns an empty array `[]`, not an error.
EOF