// TODO Day 1: replace with your chosen locality once you've picked it
const START = [20.5937, 78.9629];
const START_ZOOM = 5;

const COLORS = { low: "green", medium: "orange", high: "red" };

const map = L.map("map").setView(START, START_ZOOM);
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

let picked = null;
let pickMarker = null;
let reportLayer = L.layerGroup().addTo(map);

map.on("click", (e) => {
  picked = e.latlng;
  if (pickMarker) pickMarker.remove();
  pickMarker = L.marker(picked).addTo(map);
  document.getElementById("location-hint").textContent =
    `Location set: ${picked.lat.toFixed(5)}, ${picked.lng.toFixed(5)}`;
});

function popupFor(r) {
  // Build with textContent, not innerHTML: user text must never be parsed as HTML (XSS)
  const div = document.createElement("div");
  const title = document.createElement("strong");
  title.textContent = `${r.category} (${r.severity})`;
  const body = document.createElement("p");
  body.textContent = r.description || "(no description)";
  const meta = document.createElement("small");
  meta.textContent = `Open ${r.days_open} day(s) · reported ${r.report_count}×`;
  div.append(title, body, meta);
  return div;
}

async function loadReports() {
  const res = await fetch("/reports");
  if (!res.ok) { console.error("Failed to load reports"); return; }
  const reports = await res.json();
  reportLayer.clearLayers();
  for (const r of reports) {
    L.circleMarker([r.lat, r.lng], {
      radius: 9, color: COLORS[r.severity], fillOpacity: 0.7,
    }).bindPopup(popupFor(r)).addTo(reportLayer);
  }
}

document.getElementById("report-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!picked) { alert("Click the map to set a location first."); return; }
  const fd = new FormData(e.target);
  fd.append("lat", picked.lat);
  fd.append("lng", picked.lng);
  const res = await fetch("/reports", { method: "POST", body: fd });
  if (!res.ok) { alert("Failed: " + (await res.text())); return; }
  e.target.reset();
  if (pickMarker) { pickMarker.remove(); pickMarker = null; }
  picked = null;
  document.getElementById("location-hint").textContent = "Click the map to set the location";
  loadReports();
});

loadReports();