#!/usr/bin/env python3
"""
step_to_gmod.py  -  wandelt eine STEP-Datei (CAD) in ein schlankes Web-Modell (.gmod.json) fuer den Gantner-Konfigurator.

Benutzung:
  python3 step_to_gmod.py <datei.step> <ausgabe.gmod.json> [--budget 60000] [--map z,x,y] [--drop r,g,b;r,g,b] [--flip] [--agg 7]

  --budget  Ziel-Anzahl Dreiecke im Web-Modell (Standard 60000)
  --flip    dreht das Modell um 180 Grad um die Hochachse (Front <-> Rueckseite)
  --map     Zuordnung der CAD-Achsen auf Konfigurator-Achsen (Breite, Hoehe, Tiefe). Standard 'z,x,y'
            = CAD-Z ist Modulbreite, CAD-X ist Modulhoehe, CAD-Y ist Tiefe (Front bei +Y). Passt fuer die Q.bloxx-X-Modelle.
  --drop    Farbgruppen entfernen (z. B. verdeckte Innenteile), Format 'r,g,b;r,g,b'

Voraussetzungen:  pip install cadquery-ocp numpy trimesh fast-simplification
Ausgabe: JSON mit Masse in mm. Ursprung: Mitte der Breite, Unterkante, Rueckseite (DIN-Schienen-Seite).
"""
import sys, json, time, base64, argparse
import numpy as np
from collections import defaultdict
from OCP.STEPCAFControl import STEPCAFControl_Reader
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFApp import XCAFApp_Application
from OCP.XCAFDoc import XCAFDoc_DocumentTool
from OCP.XCAFPrs import XCAFPrs_DocumentExplorer
from OCP.IFSelect import IFSelect_RetDone
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE, TopAbs_REVERSED
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
import trimesh, fast_simplification

ap = argparse.ArgumentParser()
ap.add_argument('step'); ap.add_argument('out')
ap.add_argument('--budget', type=int, default=60000)
ap.add_argument('--map', default='z,x,y')
ap.add_argument('--drop', default='')
ap.add_argument('--agg', type=int, default=7)   # Aggressivitaet der Vereinfachung (niedriger = genauer)
ap.add_argument('--flip', action='store_true')   # Modell um 180 Grad um die Hochachse drehen
ap.add_argument('--lin', type=float, default=0.08)   # mm Abweichung beim Triangulieren
ap.add_argument('--ang', type=float, default=0.5)
a = ap.parse_args()

# 1) STEP lesen (mit Farben und Baugruppen-Struktur)
app = XCAFApp_Application.GetApplication_s()
doc = TDocStd_Document(TCollection_ExtendedString("MDTV-XCAF")); app.InitDocument(doc)
rd = STEPCAFControl_Reader(); rd.SetColorMode(True); rd.SetNameMode(True)
t = time.time(); assert rd.ReadFile(a.step) == IFSelect_RetDone, 'STEP konnte nicht gelesen werden'
rd.Transfer(doc); print(f'gelesen in {time.time()-t:.0f}s', flush=True)

# 2) Alle Bauteile triangulieren, nach Farbe gruppieren
expl = XCAFPrs_DocumentExplorer(doc, 0)
buckets = defaultdict(lambda: ([], [])); offs = defaultdict(int)
while expl.More():
    node = expl.Current()
    if not node.IsAssembly:
        shape = XCAFDoc_DocumentTool.ShapeTool_s(doc.Main()).GetShape_s(node.RefLabel)
        BRepMesh_IncrementalMesh(shape, a.lin, False, a.ang, True)
        col = (0.7, 0.72, 0.75)
        if node.Style.IsSetColorSurf():
            c = node.Style.GetColorSurfRGBA().GetRGB(); col = (c.Red(), c.Green(), c.Blue())
        key = tuple(int(round(v*255)) for v in col)
        loc = node.Location
        fx = TopExp_Explorer(shape, TopAbs_FACE)
        while fx.More():
            face = TopoDS.Face(fx.Current()); fx.Next()
            fl = TopLoc_Location(); tri = BRep_Tool.Triangulation_s(face, fl)
            if tri is None: continue
            trsf = loc.Transformation().Multiplied(fl.Transformation())
            V, F = buckets[key]; base = offs[key]; n = tri.NbNodes()
            for i in range(1, n+1):
                p = tri.Node(i).Transformed(trsf); V.append((p.X(), p.Y(), p.Z()))
            rev = face.Orientation() == TopAbs_REVERSED
            for i in range(1, tri.NbTriangles()+1):
                x, y, z = tri.Triangle(i).Get()
                F.append((base+x-1, base+z-1, base+y-1) if rev else (base+x-1, base+y-1, base+z-1))
            offs[key] += n
    expl.Next()

drop = {tuple(int(v) for v in s.split(',')) for s in a.drop.split(';') if s.strip()}
groups = [(k, np.array(V, np.float64), np.array(F, np.uint32)) for k, (V, F) in buckets.items() if k not in drop]
total = sum(len(f) for _, _, f in groups)
print(f'{len(groups)} Farbgruppen, {total} Dreiecke roh', flush=True)

# 3) Achsen zuordnen, Ursprung normieren
ax = {'x': 0, 'y': 1, 'z': 2}
perm = [ax[c] for c in a.map.split(',')]          # Konfigurator-(Breite,Hoehe,Tiefe) <- CAD-Achsen
allv = np.concatenate([g[1] for g in groups])[:, perm]
mn, mx = allv.min(0), allv.max(0)
origin = np.array([(mn[0]+mx[0])/2, mn[1], mn[2]])
size = (mx - mn)

# 4) Vereinfachen und serialisieren
parts = []; out_tris = 0
for key, V, F in groups:
    V = V[:, perm] - origin
    if a.flip: V = np.stack([-V[:, 0], V[:, 1], size[2] - V[:, 2]], 1)
    m = trimesh.Trimesh(V, F, process=True); m.merge_vertices(); m.remove_unreferenced_vertices()
    n = len(m.faces)
    target = n if n < 3000 else max(3000, int(n * a.budget / total))
    if target < n:
        p, f = fast_simplification.simplify(np.asarray(m.vertices, np.float32), np.asarray(m.faces, np.int32), target_count=target, agg=a.agg)
        m = trimesh.Trimesh(p, f, process=False)
    pos = np.asarray(m.vertices, np.float32); idx = np.asarray(m.faces, np.uint32).ravel()
    big = len(pos) > 65535
    idx = idx.astype(np.uint32 if big else np.uint16)
    parts.append({'color': list(key), 'nv': len(pos), 'pos': base64.b64encode(pos.tobytes()).decode(),
                  'idx': base64.b64encode(idx.tobytes()).decode(), 'i32': bool(big)})
    out_tris += len(m.faces)

json.dump({'format': 'gmod1', 'sizeMM': [round(float(s), 2) for s in size], 'parts': parts, 'tris': out_tris}, open(a.out, 'w'), separators=(',', ':'))
import os
print(f'fertig: {out_tris} Dreiecke, Masse B x H x T = {size[0]:.1f} x {size[1]:.1f} x {size[2]:.1f} mm, Datei {os.path.getsize(a.out)//1024} KB')
