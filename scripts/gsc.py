#!/usr/bin/env python3
"""Search Console (via Maton) — query reali, impression, clic, CTR, posizione.

Passo 1 dell'ordine di lavoro: la realta' del sito prima di qualsiasi tool esterno.

Uso:
  python3 gsc.py --days 28 --dims query
  python3 gsc.py --days 90 --dims page --limit 100 --out ~/seo-content/audits/gsc-pages.csv
  python3 gsc.py --days 28 --dims page-query --top 30

Legge MATON_API_KEY da $HERMES_HOME/.env (o dall'ambiente) e non la stampa mai.
Sito di default: $SITE_DOMAIN (es. https://il-tuo-sito.it/).

Nota: Google omette le query a volume troppo basso, quindi l'assenza di una query qui
non prova che la domanda non esista (vedi references/free-keyword-data-sources.md).
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

MATON = "https://api.maton.ai"


def load_key() -> str:
    key = os.environ.get("MATON_API_KEY")
    if key:
        return key
    home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
    for path in (os.path.join(home, ".env"), os.path.expanduser("~/.hermes/.env")):
        if not os.path.exists(path):
            continue
        for line in open(path):
            line = line.strip()
            if line.startswith("MATON_API_KEY="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("MATON_API_KEY non trovata: aggiungila a $HERMES_HOME/.env")


def default_site() -> str:
    dom = os.environ.get("SITE_DOMAIN", "").strip()
    if not dom:
        home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
        env_path = os.path.join(home, ".env")
        if os.path.exists(env_path):
            for line in open(env_path):
                if line.strip().startswith("SITE_DOMAIN="):
                    dom = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    if not dom:
        sys.exit("Sito non indicato: usa --site oppure imposta SITE_DOMAIN in .env")
    return dom if dom.startswith("http") else f"https://{dom}/"


DIMS = {"query": ["query"], "page": ["page"], "page-query": ["page", "query"], "date": ["date"]}


def fetch(key: str, site: str, dims: list[str], start: str, end: str, limit: int) -> list[dict]:
    url = f"{MATON}/google-search-console/webmasters/v3/sites/{urllib.parse.quote(site, safe='')}/searchAnalytics/query"
    body = {"startDate": start, "endDate": end, "dimensions": dims, "rowLimit": limit}
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode()).get("rows", [])
    except urllib.error.HTTPError as exc:
        body_txt = exc.read()[:400].decode("utf-8", "replace")
        sys.exit(f"Search Console HTTP {exc.code}: {body_txt}")
    except Exception as exc:  # noqa: BLE001
        sys.exit(f"Search Console: {type(exc).__name__}: {exc}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Search Console via Maton")
    ap.add_argument("--site", default=None, help="proprieta' GSC (default: SITE_DOMAIN)")
    ap.add_argument("--days", type=int, default=28)
    ap.add_argument("--dims", default="query", choices=sorted(DIMS))
    ap.add_argument("--limit", type=int, default=100, help="righe richieste a Google")
    ap.add_argument("--top", type=int, default=25, help="righe stampate")
    ap.add_argument("--out", default=None, help="file .csv o .json di destinazione")
    args = ap.parse_args()

    site = args.site or default_site()
    key = load_key()
    end = dt.date.today()
    start = end - dt.timedelta(days=args.days)
    rows = fetch(key, site, DIMS[args.dims], start.isoformat(), end.isoformat(), args.limit)
    rows.sort(key=lambda r: (-r.get("impressions", 0), r.get("position", 0)))

    print(f"# Search Console — {site} — {start} -> {end} — dims={args.dims} — righe={len(rows)}")
    print(f"# {'chiave':60s} {'imp':>6} {'clic':>5} {'ctr':>6} {'pos':>6}")
    for r in rows[: args.top]:
        k = " | ".join(r.get("keys", []))[:60]
        print(f"  {k:60s} {int(r.get('impressions', 0)):>6} {int(r.get('clicks', 0)):>5} "
              f"{r.get('ctr', 0) * 100:>5.1f}% {r.get('position', 0):>6.1f}")
    tot_imp = sum(r.get("impressions", 0) for r in rows)
    tot_clk = sum(r.get("clicks", 0) for r in rows)
    print(f"# TOTALI: impression={int(tot_imp)} clic={int(tot_clk)} "
          f"ctr={(tot_clk / tot_imp * 100) if tot_imp else 0:.2f}%")

    if args.out:
        path = os.path.abspath(os.path.expanduser(args.out))
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if path.endswith(".json"):
            json.dump({"site": site, "start": start.isoformat(), "end": end.isoformat(),
                       "dimensions": DIMS[args.dims], "rows": rows}, open(path, "w"), ensure_ascii=False, indent=1)
        else:
            with open(path, "w", newline="") as fh:
                w = csv.writer(fh)
                w.writerow(["chiave", "impression", "clic", "ctr", "posizione"])
                for r in rows:
                    w.writerow([" | ".join(r.get("keys", [])), int(r.get("impressions", 0)),
                                int(r.get("clicks", 0)), round(r.get("ctr", 0), 4), round(r.get("position", 0), 1)])
        print(f"# scritto: {path}")


if __name__ == "__main__":
    main()
