# TomGPT CarLab v14 — Blender / GTA V preparation

**Was dieses Paket tatsächlich kann:** Die v13-Fahrzeugmodelle als GLB prüfen, Bauteile in Blender nach Kategorien sortieren, Blender-Projektdatei erzeugen und Referenzpunkte setzen. Es erstellt **keine** fertige GTA-V-`.yft`/`.ytd` und ist **nicht** GTA-VI-kompatibel.

## Dateien
- `v13_tuned.glb` — das v13-Vortex-GT-Modell
- `v13_crash_front.glb` — Unfallvariante
- `v13_runtime.json` — v13-Funktionsdaten
- `validate_glb_v14.py` — Offline-Modellprüfung
- `blender_prepare_v14.py` — Blender-Batch-Skript zur Modellvorbereitung
- `gta5_export_checklist.md` — fehlende Schritte zum spielbaren GTA-V-Mod

## Am PC mit Blender
1. Blender installieren, zusätzlich Sollumz für den GTA-V-Export.
2. ZIP entpacken.
3. In einem Terminal im entpackten Ordner ausführen:
   `blender -b --python blender_prepare_v14.py -- --input v13_tuned.glb --out prepared_vehicle.blend`
4. Die `prepared_vehicle.blend` in Blender öffnen.
5. Mit Sollumz GTA-V-Struktur (Fragment/Drawable), Fahrzeug-Bones, korrekte Pivotpunkte, Materialien, Kollisionen, LODs und Licht-Setup **manuell** erstellen und testen.
6. Die nativen Dateien erst dann in einem lokalen GTA-V-Modding-Projekt testen.

## Auf dem Handy
Die GLB-Dateien lassen sich mit einem geeigneten 3D-Viewer betrachten. Die eigentliche GTA-V-Exportpipeline benötigt einen PC mit Blender, Sollumz und ein lokales GTA V.

## Grenzen
- Die Gruppierung erfolgt heuristisch anhand der Bauteilnamen; falsch benannte Teile brauchen manuelle Korrektur.
- Das Skript wird in dieser Umgebung auf Syntax geprüft, aber **nicht innerhalb von Blender ausgeführt**, weil Blender hier nicht installiert ist.
- Kein automatischer GTA-V-Export, keine GTA-VI-Unterstützung, keine fotorealistische Rockstar-Qualität garantiert.
