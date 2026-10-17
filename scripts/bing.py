#!/usr/bin/env python3
"""Impression settimanali da Bing Webmaster Tools (API ufficiale, gratuita) — GetKeywordStats.

ATTENZIONE ALL'ETICHETTA: questi sono dati **Bing**, non volumi Google. Sul mercato italiano il
bacino Bing e' una frazione di Google, quindi i numeri valgono come segnale RELATIVO (confronto fra
keyword, trend nel tempo), mai come volume di ricerca. In un rapporto va scritto accanto al numero
"impression Bing (IT)".

Uso:
  python3 bing.py hosting wordpress "wordpress lento" --country it --language it-IT
  python3 bing.py --keywords-file ~/seo-content/shared/shortlist.txt --out ~/seo-content/audits/bing.csv

Chiave: BING_WEBMASTER_API_KEY in $HERMES_HOME/.env (Bing Webmaster Tools -> Webmaster API).

Comportamento misurato il 2026-10-13 (profilo `sito`):
- `language` vuole il tag completo (`it-IT`); con `it` l'API risponde 400 Bad Request.
- L'endpoint copre i termini **ampi**: `wordpress` 20.815 impression in 25 settimane, `hosting` 949,
  `come creare un sito web` 939, `affiliazione` 116. I long-tail (`wordpress lento`, `sicurezza
  wordpress`, `miglior hosting wordpress`) tornano `{"d":[]}`: sotto la soglia di reportistica Bing.
- Quindi serve a dare un **ordine di grandezza relativo e una tendenza sui termini di testa**, non
  volumi per le query di coda. Un `{"d":[]}` va riportato come «nessun dato», non come «zero domanda».
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://ssl.bing.com/webmaster/api.svc/json/GetKeywordStats"


def load_key() -> str:
    key = os.environ.get("BING_WEBMASTER_API_KEY")
    if key:
        return key
    home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
    for path in (os.path.join(home, ".env"), os.path.expanduser("~/.hermes/.env")):
        if not os.path.exists(path):
            continue
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if line.startswith("BING_WEBMASTER_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("BING_WEBMASTER_API_KEY non trovata: aggiungila a $HERMES_HOME/.env")


def stats(key: str, kw: str, country: str, language: str) -> list[dict]:
    url = f"{BASE}?q={urllib.parse.quote(kw)}&country={country}&language={language}&apikey={key}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
    except urllib.error.HTTPError as exc:
        body = exc.read()[:200].decode("utf-8", "replace")
        sys.exit(f"Bing HTTP {exc.code} su '{kw}': {body}")
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"Bing: {type(exc).__name__}: {exc}")
    return data.get("d") or []


def epoch_ms(raw: str) -> dt.date | None:
    """Bing manda '/Date(1776470400000)/'."""
    try:
        n = int("".join(c for c in str(raw) if c.isdigit())[:13])
        return dt.datetime.fromtimestamp(n / 1000, tz=dt.timezone.utc).date()
    except Exception:  # noqa: BLE001
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description="Impression settimanali Bing (GetKeywordStats)")
    ap.add_argument("keywords", nargs="*")
    ap.add_argument("--keywords-file")
    ap.add_argument("--country", default="it")
    ap.add_argument("--language", default="it-IT")
    ap.add_argument("--out")
    args = ap.parse_args()

    kws = list(args.keywords)
    if args.keywords_file:
        kws += [l.strip() for l in open(os.path.expanduser(args.keywords_file), encoding="utf-8")
                if l.strip() and not l.startswith("#")]
    if not kws:
        sys.exit("Nessuna keyword: passale come argomenti o con --keywords-file")

    key = load_key()
    rows = []
    for kw in kws:
        recs = stats(key, kw, args.country, args.language)
        if not recs:
            rows.append({"keyword": kw, "settimane": 0, "totale": None, "ultime4": None,
                         "media": None, "prima": None, "ultima": None, "trend": "nessun dato"})
            continue
        ordered = sorted((epoch_ms(r.get("Date")), int(r.get("Impressions") or 0),
                          int(r.get("BroadImpressions") or 0)) for r in recs)
        weeks = [w for w in ordered if w[0]]
        vals = [w[1] for w in weeks]
        last4 = sum(vals[-4:])
        prev4 = sum(vals[-8:-4]) if len(vals) >= 8 else None
        trend = "n/d"
        if prev4 is not None:
            trend = "su" if last4 > prev4 else ("giu" if last4 < prev4 else "piatto")
        rows.append({"keyword": kw, "settimane": len(weeks), "totale": sum(vals), "ultime4": last4,
                     "media": round(sum(vals) / len(vals), 1), "prima": weeks[0][0], "ultima": weeks[-1][0],
                     "trend": trend,
                     "ultime4_broad": sum(w[2] for w in weeks[-4:])})

    print(f"# Bing Webmaster — GetKeywordStats — mercato {args.country}/{args.language}")
    print("# ATTENZIONE: impression BING, non volumi Google. Numeri bassi = normale sul mercato IT.")
    print(f"# {'keyword':38s} {'sett':>5} {'totale':>7} {'ultime4':>8} {'media/sett':>10} {'trend':>7}")
    for r in rows:
        print(f"  {r['keyword'][:38]:38s} {r['settimane']:>5} {str(r['totale']):>7} {str(r['ultime4']):>8} "
              f"{str(r['media']):>10} {str(r['trend']):>7}")
    if any(r['settimane'] for r in rows):
        periodo = [(r['prima'], r['ultima']) for r in rows if r['prima']]
        if periodo:
            print(f"# finestra dati: {min(p[0] for p in periodo)} -> {max(p[1] for p in periodo)}")

    if args.out:
        path = os.path.abspath(os.path.expanduser(args.out))
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if path.endswith(".json"):
            json.dump(rows, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
        else:
            with open(path, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=["keyword", "settimane", "totale", "ultime4", "media", "trend",
                                                   "prima", "ultima", "ultime4_broad"])
                w.writeheader()
                for r in rows:
                    w.writerow({k: ("" if v is None else v) for k, v in r.items()})
        print(f"# scritto: {path}")


if __name__ == "__main__":
    main()
