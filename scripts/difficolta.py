#!/usr/bin/env python3
"""Difficolta' SEO (Keyword Difficulty 0-100) via DataForSEO Labs, per la shortlist.

Una task copre fino a 1.000 keyword: $0,012 per task + $0,00012 per keyword (55 keyword ~ $0,019;
listino verificato il 17/10/2026 - la cifra si riverifica sulla pagina prima di citarla).
A differenza di `volumes.py` in coda standard, qui il costo lo dichiara l'API: lo script lo stampa e
legge anche il saldo prima e dopo, cosi' la spesa e' provata e non dedotta. `--stima` non chiama.

Il KD misura la forza dei link di chi sta in prima pagina, non la possibilita' di arrivarci: su query di
marchio o navigazionali legge valori falsi. Dove KD e SERP litigano decide la SERP. Vedi
`references/parole-chiave-strumenti.md` (Pitfalls) e `references/parole-chiave.md` §2.

Uso:
  python3 difficolta.py --keywords-file shortlist.txt --out audits/difficolta.csv
  python3 difficolta.py --keywords-file shortlist.txt --stima            # costo, nessuna chiamata

Credenziali: DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD in $HERMES_HOME/.env (fallback ~/.hermes/.env).
Non stampa mai un valore: solo presenza e lunghezza.
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request

API = "https://api.dataforseo.com"
ENDPOINT = "/v3/dataforseo_labs/google/bulk_keyword_difficulty/live"
PREZZO_TASK = 0.012
PREZZO_KEYWORD = 0.00012


def load_env() -> dict[str, str]:
    fuori: dict[str, str] = {}
    home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
    for percorso in (os.path.join(home, ".env"), os.path.expanduser("~/.hermes/.env")):
        if not os.path.exists(percorso):
            continue
        for riga in open(percorso, encoding="utf-8"):
            riga = riga.strip()
            if not riga or riga.startswith("#") or "=" not in riga:
                continue
            k, v = riga.split("=", 1)
            fuori[k.strip()] = v.strip().strip('"').strip("'")
    return fuori


def chiama(auth: str, corpo: list) -> dict:
    req = urllib.request.Request(
        API + ENDPOINT,
        data=json.dumps(corpo).encode(),
        headers={"Authorization": "Basic " + auth, "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def saldo(auth: str) -> float | None:
    """Il saldo si legge dall'endpoint a costo 0: e' l'unica prova della spesa."""
    req = urllib.request.Request(
        API + "/v3/appendix/user_data", headers={"Authorization": "Basic " + auth}
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode())
        return d["tasks"][0]["result"][0]["money"]["balance"]
    except Exception as e:
        print(f"# saldo non leggibile: {e}")
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description="Difficolta' SEO (KD) per una lista di keyword.")
    ap.add_argument("--keywords-file", required=True, help="un file con una keyword per riga (# = commento)")
    ap.add_argument("--out", default=None, help="file .csv di destinazione")
    ap.add_argument("--language", default="it")
    ap.add_argument("--location-code", default=2380, type=int, help="2380 = Italia")
    ap.add_argument("--stima", action="store_true", help="stampa il costo e non chiama l'API")
    args = ap.parse_args()

    kws = [l.strip() for l in open(os.path.expanduser(args.keywords_file), encoding="utf-8")
           if l.strip() and not l.startswith("#")]
    if not kws:
        sys.exit("Nessuna keyword nel file.")

    costo = PREZZO_TASK + PREZZO_KEYWORD * len(kws)
    print(f"# keyword: {len(kws)} - location {args.location_code} / {args.language}")
    print(f"# costo dichiarato dal listino: ${costo:.4f} (${PREZZO_TASK} per task + ${PREZZO_KEYWORD} a keyword)")
    if args.stima:
        return

    env = load_env()
    if not env.get("DATAFORSEO_LOGIN") or not env.get("DATAFORSEO_PASSWORD"):
        sys.exit("DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD assenti nel file di ambiente.")
    auth = base64.b64encode(f"{env['DATAFORSEO_LOGIN']}:{env['DATAFORSEO_PASSWORD']}".encode()).decode()

    prima = saldo(auth)
    try:
        d = chiama(auth, [{"location_code": args.location_code, "language_code": args.language,
                           "keywords": kws, "tag": "difficolta"}])
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}")

    t = d["tasks"][0]
    print(f"# stato: {t['status_code']} {t['status_message']} - costo dichiarato: ${t.get('cost')}")
    if t["status_code"] != 20000:
        sys.exit(f"task in errore: {t['status_message']}")

    righe = sorted(t["result"][0]["items"],
                   key=lambda x: (x.get("keyword_difficulty") is None, x.get("keyword_difficulty") or 0))
    print(f"# {'KD':>4}  keyword")
    for r in righe:
        kd = r.get("keyword_difficulty")
        print(f"  {'-' if kd is None else kd:>4}  {r['keyword']}")

    if args.out:
        dest = pathlib.Path(os.path.expanduser(args.out))
        with dest.open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=["keyword", "keyword_difficulty"])
            w.writeheader()
            for r in righe:
                w.writerow({"keyword": r["keyword"], "keyword_difficulty": r.get("keyword_difficulty")})
        print(f"# scritto: {dest}")

    dopo = saldo(auth)
    if prima is not None and dopo is not None:
        print(f"# saldo {prima} -> {dopo} - SPESA REALE: ${round(prima - dopo, 6)}")


if __name__ == "__main__":
    main()
