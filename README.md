# Konfigurator

Gantner Instruments – Kunden-Konfigurator (Dashboard → Projekttyp → 3D-Konfigurator).

- `app.html` – Quellcode (ohne eingebettete 3D-Modelle)
- `gantner-dashboard-konfigurator.html` – fertig gebaute Einzeldatei (im Browser öffnen)
- `tools/step_to_gmod.py` – STEP → web-taugliches Modell (`python3 tools/step_to_gmod.py in.step out.gmod.json`)
- `tools/build.py` – bettet alle `tools/models/*.gmod.json` ein (`python3 tools/build.py app.html out.html`)
- `tools/models/a101.gmod.json` – Q.bloxx-X A101 (Art.-Nr. 544223)
- `tools/models/a104.gmod.json` – Q.bloxx-X A104 TCK (Art.-Nr. 556731)
- `tools/models/a111.gmod.json` – Q.bloxx-X A111 BNC (Art.-Nr. 556832)
- `tools/models/qs.gmod.json` – Q.station X (Art.-Nr. 561828), steht immer am Anfang, nur einmal
- `tools/models/a128.gmod.json` – Q.bloxx-X A128 (Art.-Nr. 565327)
- `tools/models/a105.gmod.json` – Q.bloxx-X A105 DB15 (Art.-Nr. 563628)
- `tools/models/cab_1034|1050|1059.gmod.json` – Schaltschrank-Varianten für die Hardware-Auswahl (Typ 1034.000 / 1050.000 / 1059.000)
- weitere Schrank-Varianten: `cab_1033500`, `cab_1380`, `cab_1350`, `cab_1376`, `cab_1091` (Hardware-Auswahl, 8 Varianten gesamt)

## Status quo (Basisstand)

Funktionsumfang des Schaltschrank-Konfigurators:

- Neues-Projekt-Assistent mit 8 Schrankvarianten (Hardware-Auswahl, 3D-Vorschau, Infos)
- Bins / Einschübe: ganze und halbe Bins, aus den Innenmaßen berechneter Platz, Planer (oben → unten, halbe Bins links/rechts, nach unten schiebbar)
- Modul-Platzierung in Bins, Drag&Drop (3D und Stückliste), Station immer zuerst
- Modul-Popup: UART (1–4) und Adresse (automatisch/manuell), Speichern mit Warnung bei ungespeicherten Änderungen
- Hinweissymbol „Fehlende UART-Definition“ je Modul ohne UART
- Ansichtsfilter (UART, Modultyp; Funktion folgt)
- Kabelkanal-Platzierung (25 × 40 mm, waagrecht/senkrecht): Zeichnen mit der Maus, Beschriftung KK1…, Länge änderbar, Drag&Drop, bündiges Einrasten/Anschließen und Kreuzungsauflösung

Offene Platzhalter: Preise, Beschreibungen/Modulinfos, Leistungswerte, Schrank-Innenmaße-Annahmen (Randabstände, Reihenabstand), Kabelkanal-Orientierung (25 breit / 40 tief).
