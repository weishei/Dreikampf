# Dreikampf – Anleitung für Claude

Partyquiz für mehrere Handys von Basti (Sebastian). Live: https://weishei.github.io/Dreikampf/
Läuft über GitHub Pages, Spielstände und Profile liegen in Firebase (Projekt „dreikampf“).

## Mit Basti arbeiten
- Er ist kein Programmierer: kurz antworten, in Stichpunkten, einfaches Deutsch, keine Fachbegriffe.
- Präzise und ehrlich sein, auch wenn es unangenehm ist. Keine erfundenen Zahlen oder Zitate, unsichere Stellen markieren.
- Vor jeder Nachricht an Lovable erst nachfragen (gilt für seine anderen Projekte).
- Geheimes (Gründer-Link-Schlüssel, Profil-Codes) nie ins Projekt schreiben und nie in Gruppen posten. Das Projekt ist öffentlich.
- Es arbeitet immer nur eine Claude-Sitzung am Spiel. Vor jeder Arbeit `git pull`.

## Aufbau
- Das ganze Spiel steckt in **einer** Datei: `index.html` (ca. 1,2 MB, HTML, CSS und JS in einem).
  Die frühere Bearbeitungsdatei und das Build-Skript gibt es nicht mehr. Es wird direkt in `index.html` gearbeitet.
- Daneben: `version.json`, `sw.js` (Offline-Cache, lässt .mp4 aus), `manifest.json`, Icons, zwei Videos
  (`profil-mitnehmen.mp4` für die Erklärung „Profil mitnehmen“, `weihnachtsspot.mp4`), `migr.json`.
- Die Datei ist sehr lang. Nicht komplett lesen, sondern mit Suche oder kleinen Python-Skripten gezielt ändern.
  Jede Ersetzung vorher prüfen: Der Suchtext muss genau einmal vorkommen.

## Neue Version veröffentlichen
1. Änderungen in `index.html`.
2. `BUILD_ID="…"` in `index.html` **und** `{"v": "…"}` in `version.json` auf denselben neuen Wert setzen
   (aktuelle Unix-Zeit). Nur dann bekommen die Spieler „✨ Neue Version da“.
3. Commit mit kurzer deutscher Nachricht, `git push origin main`. GitHub Pages ist nach etwa einer Minute aktuell.
   Fehler beim Push nie verschweigen.

## Fragen-Daten
- **Auswahlfragen** `MC`: `{"q":Frage,"a":[richtig,falsch,falsch,falsch],"f":Erklärung,"d":1|2|3}`
  (d = leicht/mittel/schwer, ältere Fragen haben kein d). Die Antworten werden im Spiel gemischt.
- **Kategorie** je Frage im Parallel-Array `THEME_MC`, gleiche Reihenfolge wie `MC`.
- **Finale** `FIN`: `{"c":Kategorie-Name,"q","a":[...],"f"}`, Kategorie in `THEME_FIN`.
  Jedes Thema braucht Finalfragen, sonst stürzt die Spielauswahl ab.
- **Schätzfragen** `EST`: `{"q","a":Zahl,"u":Einheit,"f"}`, Jahre mit `"y":true`.
- **Themen** `THEMES`: `schlüssel:["Name",[Kategorien]]`. `mix` (Gemischt) nimmt alles außer `xmas`.
  `sport` enthält `sportlerinnen`. Symbole in `THEME_ICON`.
- Eigene Stapel: `IQ` (Logik), `BABY`/`BABY_MYTH`/`BABY_EST` (Baby & Eltern), `KI_MC` (KI-Prüfungstraining).
  Weihnachten (`xmas`) nur vom 1.12. bis 6.1. (`xmasOn`).
- **Neue Fragenblöcke** stehen als eigener Block **direkt vor** der Zeile
  `(function(){const m=[{"q":"In welchem Land entstand das Lied`. Muster (so sind Berge, Biologie,
  Zeitgeschichte und Wirtschaft & Politik eingebaut):
  ```js
  const NEU_MC=[...];MC.push.apply(MC,NEU_MC);THEME_MC.push.apply(THEME_MC,NEU_MC.map(()=>"neu"));
  const NEU_FIN=[...];FIN.push.apply(FIN,NEU_FIN);THEME_FIN.push.apply(THEME_FIN,NEU_FIN.map(()=>"neu"));
  const NEU_EST=[...];EST.push.apply(EST,NEU_EST);
  ```
  Dann in `THEMES` `neu:["Name",["neu"]]` ergänzen und in `THEME_ICON` ein Symbol.
  Ein Thema mit eigener Schätzrunde (wie `berge`, `bio`) bekommt zusätzlich einen Zweig in `modeSteps0`
  (`m==="est"&&used.theme==="…"`).

## Ablauf für neue Fragen (Bastis Wunsch, immer so)
1. Mit öffentlichen Quellen recherchieren und jede Antwort an der Quelle prüfen.
2. Freigabe-Liste zeigen: Frage, richtige und falsche Antworten, Erklärung, Quelle,
   Schwierigkeit etwa je ein Drittel, ein paar Schätzfragen, unsichere Stellen oben markiert.
3. Erst nach Bastis **„Freigabe“** einbauen.
- Vorher auf Dopplungen mit bestehenden Fragen prüfen.
- Falsche Antworten müssen eindeutig falsch sein. Bei Logik-Fragen muss die Regel für die ganze Reihe gelten.
- Zeitgebundene Fakten mit Jahr in die Frage schreiben. Politik nur neutral, ohne Wertung.

## Testen
- Keine Testumgebung im Projekt. Bewährt hat sich: eine **Kopie** von `index.html` mit einem eingeschleusten Hook
  vor `function buildSteps(` (z. B. `window.__bs=(...x)=>buildSteps(...x);window.__x=()=>({MC,THEME_MC,FIN,THEME_FIN,EST,THEMES});`),
  in Playwright öffnen (alle Netzwerkzugriffe blocken) und je Thema ein paar hundert Spiele mit
  `__bs({theme:"…",len:"normal"},[{},{},{}])` bauen lassen. Erwartet: keine Fehler, `MC.length === THEME_MC.length`,
  `FIN.length === THEME_FIN.length`, das Finale kommt aus dem richtigen Thema.
- Firebase ist aus Sandboxen meist nicht erreichbar, Mehrspieler-Abläufe also nur von Hand auf dem Handy testen.

## Stand (November 2026)
- Etwa 1.860 Auswahlfragen, 309 Finalfragen, 470 Schätzfragen. Themen: Bayern & München, Sport, Sportlerinnen,
  Geschichte & Welt, Natur & Wissen, Kultur & Unterhaltung, Essen & Alltag, Logik & IQ, Weihnachten,
  Baby & Eltern, Berge, Biologie, Zeitgeschichte, Wirtschaft & Politik.
- Spielräume (mehrere Gruppenspiele gleichzeitig), Profile mit PIN, Code, Mail und Laden, Gründer-Statistik.

## Offene Punkte
- **Sicherheit** der Datenbank-Regeln und der Profil-Anmeldung überarbeiten. Details bei Basti erfragen,
  nicht ins öffentliche Projekt schreiben.
- **„Dohlen-Schützenfest“** (Moorhuhn-artiges Minispiel): Einbau erst, wenn Basti „Dohlen einbauen“ sagt.
  Details im Abschnitt unten.
- **Anfang 2027** die zeitgebundenen Fragen prüfen (Mindestlohn, Deutschlandticket, Haushalt, Euro-Länder,
  Bundespräsident usw. in „Wirtschaft & Politik“).
- Ton-Problem auf manchen Handys: Ursache noch offen, Details von Basti abwarten.

## Dohlen-Schützenfest (geplantes Geschick-Minispiel)
Spielbarer Prototyp mit Konzept: `docs/dohlen-prototyp.html` (eigenständige Testseite, nicht Teil des Spiels).
Spielablauf und Logik von dort übernehmen (Funktionen `dh…`), nicht neu erfinden.

**Regeln laut Prototyp**
- 25 s, Alpendohlen und Brezn fliegen quer über ein Bergpanorama. Antippen = Schuss.
- Drei Tiefen, erkennbar an der Größe: vorn 5, Mitte 10, hinten 25 Punkte. Zweimal pro Runde goldene Brezn: 50.
- 6 Schuss, dann Nachladen (0,6 s, Knopf oder Antippen der Patronen).
- Alle Spieler bekommen dieselbe Zielfolge über dieselbe Startzahl wie die anderen Minispiele (`dhSchedule(seed)`).
- Trefferbereich 35 % größer als die Figur, mindestens fingerbreit, das vorderste Ziel zählt.
- Kein Blut, keine Waffe im Bild. Getroffene Dohlen verlieren Federn und fliegen weg.
- Wertung im Dreikampf wie bei den anderen Geschick-Spielen über die Platzierung.

**Testergebnis (Basti, 08.11.2026)**
- Ohne Erklärung verstanden: ja.
- 205 Punkte, 16 Treffer bei 18 Schuss (vorn 5, Mitte 8, hinten 2, Gold 1). Er schießt also genau, aber wenig.
- Die simulierten Werte (Gelegenheit 115, normal 280, Profi 470) sind damit vermutlich zu hoch.
  Solo-Gegner nach echten Ergebnissen einstellen, nicht nach der Simulation. Basti nach weiteren Testrunden fragen.
- Auf der Testseite überlappt am Handy der Nachladen-Knopf den Text (nur Layout der Testseite).

**Vor dem Einbau mit Basti klären**
- **Optik:** Basti will, dass es „noch schöner“ wird. Erst fragen, was genau (z. B. Figuren, Hintergrund,
  Treffer-Effekte, Animationen, Ton). Vorschläge zeigen, bevor gebaut wird.
- Dauer (25 s ist deutlich länger als Treffsicher ~7 s und Brezn-Jagd 10 s), Häufigkeit, Name.
- Ablauf, wenn die Zeit der Runde endet, während jemand noch spielt (wie bei den anderen Zeitspielen werten).
- Auf echten Handys testen, vor allem iPhone.
