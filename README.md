# Konfigurator

Gantner Instruments – Kunden-Konfigurator (Dashboard → Projekttyp → 3D-Konfigurator).

- `app.html` – Quellcode (ohne eingebettete 3D-Modelle)
- `gantner-dashboard-konfigurator.html` – fertig gebaute Einzeldatei (im Browser öffnen)
- `tools/step_to_gmod.py` – STEP → web-taugliches Modell (`python3 tools/step_to_gmod.py in.step out.gmod.json`)
- `tools/build.py` – bettet alle `tools/models/*.gmod.json` ein (`python3 tools/build.py app.html out.html`)
- `tools/models/a101.gmod.json` – Q.bloxx-X A101 (Art.-Nr. 544223)
- `tools/models/a104.gmod.json` – Q.bloxx-X A104 TCK (Art.-Nr. 556731)
