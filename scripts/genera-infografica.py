#!/usr/bin/env python3
"""Scorciatoia per le infografiche: chiama genera-immagine.py con --tipo infografica.

Uso: ~/seo-content/.venv/bin/python genera-infografica.py --prompt "..." --out ~/seo-content/content/infografica-x.png
"""
import pathlib
import subprocess
import sys

qui = pathlib.Path(__file__).resolve().parent
generico = qui / "genera-immagine.py"

args = sys.argv[1:]
if "--tipo" not in args:
    args = ["--tipo", "infografica"] + args

raise SystemExit(subprocess.run([sys.executable, str(generico)] + args).returncode)
