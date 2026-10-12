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
- `tools/models/cab_1034|1050|1059.gmod.json` – Schaltschrank-Varianten für die Hardware-Auswahl (Typ 1034.000 / 1050.000 / 1059.000)
- weitere Schrank-Varianten: `cab_1033500`, `cab_1380`, `cab_1350`, `cab_1376`, `cab_1091` (Hardware-Auswahl, 8 Varianten gesamt)
