#!/usr/bin/env python3
"""Bettet alle tools/models/*.gmod.json in app.html ein und schreibt die fertige Einzeldatei.
Benutzung: python3 tools/build.py app.html <ausgabe.html>"""
import sys, json, glob, os
src, dst = sys.argv[1], sys.argv[2]
models = {}
for f in sorted(glob.glob(os.path.join(os.path.dirname(__file__), 'models', '*.gmod.json'))):
    models[os.path.basename(f).replace('.gmod.json', '')] = json.load(open(f))
html = open(src, encoding='utf-8').read()
assert '/*__STEP_MODELS__*/' in html, 'Platzhalter fehlt'
html = html.replace('/*__STEP_MODELS__*/', 'window.STEP_MODELS=' + json.dumps(models, separators=(',', ':')) + ';')
open(dst, 'w', encoding='utf-8').write(html)
print(f'{len(models)} Modell(e) eingebettet -> {dst} ({os.path.getsize(dst)//1024} KB)')
