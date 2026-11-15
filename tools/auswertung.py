"""Erfolgszahlen aus einem Export („Statistik → Daten exportieren“) berechnen.
Aufruf:  python3 -I tools/auswertung.py /pfad/zu/dreikampf-daten-JJJJ-MM-TT.json
Die Exportdatei enthält Namen: NIE ins Projekt legen oder committen (siehe .gitignore)."""
import json, sys, collections, datetime as dt
from zoneinfo import ZoneInfo
TZ = ZoneInfo("Europe/Berlin"); T = lambda ms: dt.datetime.fromtimestamp(ms / 1000, TZ)
d = json.load(open(sys.argv[1]))["daten"]
grp = [r for r in d["results"] if len(r["players"]) > 1]
RO, EV = d["rooms"], d["events"]
kw = lambda ms: "%d-KW%02d" % T(ms).isocalendar()[:2]
g = collections.Counter(kw(r["at"]) for r in grp)
ro = collections.Counter(kw(r["createdAt"]) for r in RO if r.get("createdAt"))
nie = collections.Counter(kw(r["createdAt"]) for r in RO if r.get("createdAt") and not r.get("startedAt"))
ev = collections.defaultdict(collections.Counter)
for e in EV: ev[kw(e["at"])][e["t"]] += 1
print("Woche      Spiele  Räume  Räume/Spiel  nie gestartet  App geöffnet  Revanche  neue Runde")
for w in sorted(set(g) | set(ro)):
    rs = ro.get(w, 0); gs = g.get(w, 0)
    print(f"{w}  {gs:6}  {rs:5}  {(rs/gs if gs else float('nan')):11.2f}  {nie.get(w,0):13}  {ev[w]['app_geoeffnet']:12}  {ev[w]['revanche']:8}  {ev[w]['neue_runde']:10}")
rep = d.get("reports", [])
print("Meldungen mit Grund:", sum(1 for x in rep if x.get("g")), "von", len(rep))
via = collections.Counter((e.get("via"), e.get("dev")) for e in EV if e["t"] == "app_geoeffnet")
print("App geöffnet über (Herkunft, Gerät):", dict(via))
