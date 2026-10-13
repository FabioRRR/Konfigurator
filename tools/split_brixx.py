#!/usr/bin/env python3
"""Teilt das konvertierte Q.brixx-X-System (Station + 2 Griffe) in drei Web-Modelle:
   bx_handle_l, bx_handle_r (Griffe) und bx_ph (Platzhalter-Modul in der Mitte).
   Benutzung: python3 -I split_brixx.py <raw.gmod.json> <ausgabeordner> [--ph-tris 25000]"""
import sys, json, base64, numpy as np, trimesh, fast_simplification, os
src, outdir = sys.argv[1], sys.argv[2]
ph_tris = int(sys.argv[sys.argv.index('--ph-tris')+1]) if '--ph-tris' in sys.argv else 25000
d = json.load(open(src))
sets = {'bx_handle_l': [], 'bx_handle_r': [], 'bx_ph': []}
for p in d['parts']:
    V = np.frombuffer(base64.b64decode(p['pos']), np.float32).reshape(-1, 3).astype(np.float64)
    F = np.frombuffer(base64.b64decode(p['idx']), np.uint32 if p['i32'] else np.uint16).reshape(-1, 3)
    m = trimesh.Trimesh(V, F, process=False)
    for c in m.split(only_watertight=False):
        cx = (c.bounds[0][0] + c.bounds[1][0]) / 2
        key = 'bx_handle_l' if cx < -20 else 'bx_handle_r' if cx > 20 else 'bx_ph'
        sets[key].append((tuple(p['color']), c))
for name, items in sets.items():
    by = {}
    for col, c in items: by.setdefault(col, []).append(c)
    parts = []; allv = []; tris = 0
    for col, cs in by.items():
        m = trimesh.util.concatenate(cs)
        if name == 'bx_ph' and len(m.faces) > ph_tris // max(1, len(by)):
            v, f = fast_simplification.simplify(m.vertices, m.faces, target_count=ph_tris // max(1, len(by)), agg=7)
            m = trimesh.Trimesh(v, f, process=False)
        V = m.vertices.astype(np.float32); F = m.faces.astype(np.uint32)
        parts.append({'color': list(col), 'nv': len(V), 'pos': base64.b64encode(V.tobytes()).decode(),
                      'idx': base64.b64encode(F.astype(np.uint32 if len(V) > 65535 else np.uint16).tobytes()).decode(), 'i32': bool(len(V) > 65535)})
        allv.append(V); tris += len(F)
    A = np.concatenate(allv); mn, mx = A.min(0), A.max(0)
    json.dump({'format': 'gmod1', 'sizeMM': [round(float(x), 2) for x in (mx - mn)], 'parts': parts, 'tris': tris,
               'bounds': [[round(float(x), 2) for x in mn], [round(float(x), 2) for x in mx]]},
              open(os.path.join(outdir, name + '.gmod.json'), 'w'), separators=(',', ':'))
    print(name, tris, 'Dreiecke', mn.round(1), mx.round(1))
