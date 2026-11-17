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
  Baby & Eltern, Berge, Biologie, Zeitgeschichte, Wirtschaft & Politik, Künstliche Intelligenz (Schlüssel `kint`,
  weil `ki` schon der Google-Prüfungsmodus ist).
- Spielräume (mehrere Gruppenspiele gleichzeitig), Profile mit PIN, Code, Mail und Laden, Gründer-Statistik.

## Messung und Verbesserungen (seit 15.11.2026)
**Vorgehen:** erst Daten (Export „📊 Statistik → 📥 Daten exportieren“), dann kurze Entscheidungsliste, gebaut wird nur nach Bastis
„Freigabe“. Exportdateien enthalten Namen: nie ins Projekt legen oder committen (`.gitignore`), nur außerhalb ablegen.
Erfolgszahlen rechnet `python3 -I tools/auswertung.py <export.json>` (Spiele, Räume pro Spiel, nie gestartete Räume je Woche).

**Vorher-Werte (Export 14.11.2026):** Gruppenspiele je Woche KW40–46: 15, 44, 15, 1, 6, 0, 4. Verschiedene Spieler KW41: 14,
danach 2–6. Räume pro fertigem Spiel seit 15.10.: 1,14 (KW46: 2,0). Nie gestartete Räume: 13 von 25. Leitung verlässt
Raum allein: 11-mal. Meldungen mit Grund: 0 von 5. Quiz 62 % richtig, Finale 49 %. 9 überzählige Profile, alle vor dem 12.10.
entstanden. Start bis Startseite bedienbar (eigene Messung, langsames Netz, 4× langsamer Prozessor): 5,3 s.

**Freigegeben und gebaut (15.11.2026):**
1. Spielende: Leitung „🔁 Nochmal spielen“ (Revanche) und „⚙️ Thema oder Länge ändern“. Diese Lobby nimmt alle aus dem
   letzten Spiel automatisch mit (`G.carry`, Auto-Beitritt in `onChange`). Mitspieler sehen „✋ Ich will nochmal“
   (`P.again`), die Leitung sieht „✋ x von y wollen nochmal“. „Raum schließen“ nur noch im Menü mit Rückfrage.
2. Ereignis `app_geoeffnet` mit `via` (start/link/homescreen) und `dev` (ios/android/computer). Neu gezählt außerdem:
   `revanche`, `neue_runde`, `nochmal_signal`, `raum_gewechselt`, `beitritt` mit `via:"weiter"`.
3. Vor „Neuen Raum eröffnen“: Hinweis auf einen frisch eröffneten Raum anderer (`freshRoom`). Zwei gleichzeitig eröffnet:
   der später eröffnete Raum bekommt „Dorthin wechseln“ (`twinRoom`, `roomswitch`).
5. „Frage melden“ fragt den Grund (falsch, unklar, zu schwer, Tippfehler), Feld `g` in `reports`.
8. Firebase-Dateien mit `defer`, `fbInit` wartet auf `fbReady()`. Messung: Startseite bedienbar 5,3 → 5,1 s (kleiner Effekt;
   die eigentliche Bremse ist die Größe von `index.html`).
Nach 1–2 Wochen: neuen Export mit `tools/auswertung.py` gegen die Vorher-Werte vergleichen und hier eintragen.

**Offener Befund:** Im Firebase-Nachbau (Emulator) lädt beim gleichzeitigen Eröffnen zweier Räume bei etwa 1–3 von 16
Versuchen der eigene neue Raum auf dem Handy des Eröffners nicht (Raum existiert in der Datenbank, Handy zeigt Startseite).
Kommt auch in der Version vor dem 15.11. vor. Ob es im echten Firebase passiert, ist unbekannt.

**Testen mit mehreren Spielern:** Firebase-Emulator (`firebase-tools`, Firestore + Auth) außerhalb des Projekts starten,
eine Kopie von `index.html` lädt Firebase aus `node_modules/firebase` statt gstatic und ruft `auth.useEmulator(...)` sowie
`fs.settings({host:"127.0.0.1:8085",ssl:false})` auf. Dann mehrere Playwright-Fenster als getrennte Spieler.
Vor jedem Lauf die Test-Datenbank leeren (sonst fragt die PIN-Abfrage nach bekannten Namen).

## Offene Punkte
- **Sicherheit:** Stufe A (strengere Datenbank-Regeln, 17.11.2026) im Nachbau getestet, Basti trägt sie in Firebase ein.
  Neue Bereiche in der Datenbank brauchen ab dann eine eigene Regel, sonst wird das Schreiben abgelehnt.
  Stufe B (Profile wirklich schützen, braucht Firebase-Tarif Blaze) später. Details nicht ins öffentliche Projekt schreiben.
- **Phönixflug** (Geschick-Minispiel, früher „Dohlen-Schützenfest“): **eingebaut (12.11.2026)**. Offen:
  Test auf echten Handys (vor allem iPhone), Computer-Gegner nach echten Ergebnissen nachstellen.
  Details im Abschnitt unten.
- **Kreativität**: ins Spiel eingebaut (17.11.2026, Basti: „Bau ein“), im Nachbau getestet. Offen: Test mit Freunden auf echten Handys. Details im Abschnitt unten.
- **Anfang 2027** die zeitgebundenen Fragen prüfen (Mindestlohn, Deutschlandticket, Haushalt, Euro-Länder,
  Bundespräsident usw. in „Wirtschaft & Politik“).
- Ton-Problem auf manchen Handys: Ursache noch offen, Details von Basti abwarten.

## Phönixflug (Geschick-Minispiel, früher „Dohlen-Schützenfest“)
**Im Spiel (seit 12.11.2026):** Schlüssel `phx` in `SKILLS`/`SKG`, kommt so oft dran wie die anderen 11 Geschick-Spiele.
Code-Block `const PHX=(function(){…})();` direkt vor `/* ========== Ende GESCHICK ========== */`, darin die
`dh…`-Funktionen wörtlich aus dem Prototyp. Anbindung: `skStage` (Spielfeld), `skTap` (Start, `data-sk="rl"` = Nachladen),
`skTick` (`PHX.tick`, nach 25 s `skFinish(Punkte)`), `skAfter` (`PHX.bind` nach jedem Neuzeichnen), `skDeadline`,
`skFmt`. Zustand liegt in `SK`. Wertung: mehr Punkte = besser (Standardzweig in `skMetric`), 0 Punkte = nicht platziert.
Ton über `ac`/`soundOn` des Hauptspiels, Effekte nach `fxAllowed()`. Startzahl = `st.seed` der Geschick-Runde.
Computer-Gegner `BOT_SK.phx=[100,190,300]` sind geschätzt (nur ein echtes Ergebnis: 205), nach Tests anpassen.

**Umbenennung (Basti, 08.11.2026):** Statt Alpendohlen fliegt ein Phönix, abgeleitet vom App-Symbol `icon.svg`
(Flammenfarben Rot/Orange/Gelb, Fächer aus Flammenfedern, Krone aus drei Flammen). Brezn und Gold-Brezn bleiben.
Treffer-Effekt neu: Glut und Funken, der Phönix zerfällt kurz zu Asche und steigt als Flämmchen davon.
Regeln, Zielfolge, Trefferbereiche und Punkte bleiben **unverändert** (Funktionen `dh…` nicht anfassen).
Im Code heißt die Zielart weiter `"dohle"`, damit die Zielfolge gleich bleibt.

- Spielbarer Prototyp mit Konzept (noch mit Dohlen): `docs/dohlen-prototyp.html`.
- Stilseite mit drei Varianten: `docs/phoenix-stil.html`. **Gewählt (10.11.2026): Variante B** (Sticker-Stil
  mit hellem Rand, Sternennacht), weil am leichtesten erkennbar.
- Spielbare Testseite mit neuer Optik: `docs/phoenixflug-test.html` (enthält auch „Alte Dohlen“ zum Vergleich,
  5-Sekunden-Standbild, Checkliste). Zeichnung als vorbereitete Bilder (Sprites), Hintergrund als ein Bild
  plus Wolken, damit es auf schwachen Handys flüssig bleibt. `#fps` an die Adresse hängen zeigt die Bildrate.
- Geprüft: `dh…`-Funktionen Zeichen für Zeichen gleich wie im Prototyp, Zielfolge und Treffer für 300 Folgen gleich,
  kein sichtbares Pixel von Phönix, Brezn oder Gold-Strahlen liegt außerhalb des Trefferbereichs.
- Treffer-Stopp friert nur den getroffenen Phönix kurz ein, nicht das ganze Bild (sonst würde die Runde länger).
- Ton: Web Audio, startet erst nach Tippen, `navigator.audioSession.type="playback"` wie im Hauptspiel
  (ab iOS 17 Ton trotz Stumm-Schalter, Musik anderer Apps pausiert). Nicht auf echtem iPhone geprüft.
- Phönix muss in den alten Dohlen-Umriss passen (etwa 30 Einheiten Radius), sonst wirkt der Trefferbereich unfair.
- Spielablauf und Logik aus dem Prototyp übernehmen (Funktionen `dh…`), nicht neu erfinden.

**Regeln laut Prototyp**
- 25 s, Phönixe (früher Alpendohlen) und Brezn fliegen quer über den Himmel. Antippen = Schuss.
- Drei Tiefen, erkennbar an der Größe: vorn 5, Mitte 10, hinten 25 Punkte. Zweimal pro Runde goldene Brezn: 50.
- 6 Schuss, dann Nachladen (0,6 s, Knopf oder Antippen der Patronen).
- Alle Spieler bekommen dieselbe Zielfolge über dieselbe Startzahl wie die anderen Minispiele (`dhSchedule(seed)`).
- Trefferbereich 35 % größer als die Figur, mindestens fingerbreit, das vorderste Ziel zählt.
- Kein Blut, keine Waffe im Bild. Getroffene Phönixe zerfallen zu Glut und steigen als Flämmchen auf.
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

## Kreativ-Runden (eingebaut 17.11.2026)
**Idee:** neue Säule „Kreativität“ mit zwei Gruppen-Spielen. Entschieden (Basti): als **Überraschungsrunden** wie Bluff und
Mehrheit, **nur ab 3 echten Spielern, nur bei Normal und Lang, nie im Solo, nie mit Computer-Gegnern** (in `SOLO_NO`
und `MIN3`). Bluff-Runde bleibt unverändert. Design: **gemischt** – Entwurf A (Notizzettel, Antworten A–D) für
Kritzel-Raten, Entwurf B (bunte Zettel, 😂-Stempel) für Lacher der Runde. Entwürfe: `docs/kreativ-entwurf.html`.

**Kritzel-Raten ✏️:** 3 Zeichnungen pro Runde (reihum, niemand doppelt). Der Zeichner sieht geheim einen Begriff,
3 s Countdown, 45 s zeichnen (6 Farben, 2 Stiftdicken, Zurück, Löschen, keine Buchstaben/Zahlen). Die anderen sehen die
Zeichnung live und tippen eine von 4 Antworten (3 falsche aus derselben Gruppe), nur ein Tipp. Punkte: richtig 100 plus
Tempo-Bonus bis 100 (`100*(1-t/45s)`), Zeichner 50 pro richtigem Tipp, höchstens 300, falsch 0.
Begriffe (freigegeben): 150 in 6 Gruppen zu je 25 – Tiere, Essen, Bayern, Sport, **Tätigkeiten** (statt Berufen, damit
nichts gegendert werden muss), Gegenstände.

**Lacher der Runde 😂:** 2 Aufgaben pro Runde. Alle schreiben in 60 s eine Antwort (max. 60 Zeichen), dann anonyme
Abstimmung (40 s), eigene nicht wählbar, leere Antworten werden nicht gezeigt, die Leitung kann eine Antwort ausblenden
(zählt dann 0). Punkte: 100 pro Stimme plus 100 für die meisten Stimmen (bei Gleichstand alle Besten, nur wenn > 0).
Lückensätze (freigegeben): 80 Stück. Spielertexte immer mit `h()` als Text, nie als HTML.

**Testseite `docs/kreativ-prototyp.html`:** beide Spiele komplett, gleiche Bausteine und CSS wie `index.html`.
Mehrere Fenster im selben Browser spielen zusammen (gemeinsamer Speicher im Browser statt Firebase, Raum über
`?room=NAME`, Name über `&name=`). Datenaufbau wie im Spiel: Spielstand mit `steps`, `idx`, `reveal`, Antworten-Schnappschuss
`A`, Spieler-Einträge mit `ans`. Testhilfen: weiteres Fenster, schlechtes Netz (1,5 s Verzögerung), Fenster verlassen.
Zeichnung: Striche vereinfacht (Ramer-Douglas-Peucker, 1000er-Raster) und alle 300 ms als eigenes kleines Paket gesendet
(im Spiel: eigene Firestore-Dokumente pro Paket, damit Zuschauer nur Neues bekommen).

**Geprüft (17.11.2026, 4–5 Fenster, 30 Prüfungen bestanden):** Punkte beider Spiele inkl. Tempo-Bonus und Gleichstand,
Zeichner verlässt das Spiel (Runde übersprungen, niemand bekommt oder verliert Punkte), Zeit läuft ab, später Gast schaut zu,
zwei Räume gleichzeitig getrennt, schlechtes Netz, eingeschleuster HTML-Code wird nur als Text gezeigt, Leitungsübergabe.
Datenmenge pro Zeichnung: normal ~2,3 KB in ~45 Paketen, ungünstigster Fall (41 s Dauerkritzeln) ~12 KB in ~160 Paketen
(nur Nutzdaten, Firebase-Zuschlag pro Paket kommt dazu). Kleines iPhone (375×667): kein seitliches Scrollen,
Werkzeuge und Antworten ohne Scrollen sichtbar.
Beim Test gefunden und behoben: Wiederbeitreten muss den Spieler-Eintrag neu anlegen (sonst wandern alte Antworten mit),
Zeichner gilt erst nach Verlassen oder 20 s ohne Lebenszeichen als weg (kurzer App-Wechsel erlaubt).

**Im Spiel (seit 17.11.2026):** Block `const KR=(function(){…})();` direkt vor `/* ========== Ende GESCHICK ========== */`,
darin Begriffe und Lückensätze. Modus-Schlüssel `kz` (Kritzel-Raten) und `lach` (Lacher), Schritt-Arten `kz`, `lw` (schreiben),
`lv` (abstimmen). Angebunden über `POOL_MODES`, `MODES`, `MIN3`, `SOLO_NO`, `fits` (Sperre bei „Kurz“), `buildSteps`
(`KR.steps`), `STEP_T` (sonst wird der Spielstand als kaputt verworfen!), `QTYPES`, `NOBONUS`, `extraPoints` (`KR.points`),
`expired`, `myWindow` (`KR.total`), `hostTick` (`KR.timing`, `KR.hostCheck`, „skip“ setzt `G.skip[idx]`), `vMain` (`KR.view`),
`mainKey` (`KR.viewKey`), `afterMain` (`KR.after`), `act` (kzguess, kzcol, kzwid, kzundo, kzclr, lwsend, lvvote, lvhide).
Ausblenden durch die Leitung: `G.hid[idx][uid]`. Zeichnung: eigene Dokumente `kzs/{G.v}_{idx}_{seq}` mit Feld `g`=G.v (Abfrage `where("g","==",G.v)`, `o` = JSON-Text,
nur anlegen, nicht ändern); sperren die Datenbank-Regeln das, schickt das Handy die Pakete im eigenen Spieler-Eintrag (`kz.{v_idx}.cNNNN`, etwa jede Sekunde).
Zeichner-Lebenszeichen: `seen` alle 5 s während der eigenen Zeichnung. Häufigkeit: in etwa jedem 9. Normal-/Lang-Spiel mit
≥ 3 Leuten je eine der beiden Runden (Messung mit `buildSteps`, 300 Spiele).
**Geprüft im Firebase-Nachbau (17.11.2026, 4 Spieler + Gast, 45 Prüfungen, zweimal: offene Regeln und gesperrter
Zeichnungs-Speicher):** Auswahl (nie Kurz, nie Solo, nie unter 3), live zeichnen inkl. Zurück, später Gast schaut zu,
Punkte inkl. Tempo, alle Handys rechnen gleich, Zeit läuft ab, Zeichner verlässt das Spiel, Schreibfeld bleibt beim Neuzeichnen
offen, leere Antwort, HTML-Code nur als Text, Gleichstand, Ausblenden, Spiel läuft bis zum Ende, keine Fehler.
**Offen:** Test mit Freunden auf echten Handys (vor allem iPhone: Zeichnen mit dem Finger, Tastatur beim Lacher).
Ob die echten Datenbank-Regeln den Zeichnungs-Speicher erlauben, ist unbekannt (Ersatzweg funktioniert, ist aber langsamer).

