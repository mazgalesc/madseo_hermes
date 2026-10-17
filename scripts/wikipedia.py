#!/usr/bin/env python3
"""Domanda per ARGOMENTO da Wikipedia/Wikimedia Pageviews — keyless, nessun account.

Non e' un volume di ricerca: e' quante persone leggono quella voce di Wikipedia in un periodo.
Serve a due cose concrete:
  * dare un ordine di grandezza alla rilevanza di un tema (e confrontare temi fra loro);
  * vedere la tendenza (mese su mese) di un argomento, quando non c'e' un'altra fonte.

Uso:
  python3 wikipedia.py WordPress Hosting "Intelligenza artificiale"
  python3 wikipedia.py --days 90 --project it.wikipedia --out ~/seo-content/audits/wikipedia.csv

Endpoint: /metrics/pageviews/per-article/{project}/all-access/user/{titolo}/daily/{da}/{a}
Un 404 significa "nessun dato per quella voce/periodo" (spesso: la voce non esiste con quel titolo).
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

BASE = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article"
UA = {"User-Agent": "hermes-research/1.0 (contact: local agent)", "Accept-Encoding": "identity"}


def views(project: str, title: str, start: dt.date, end: dt.date):
    url = (f"{BASE}/{project}/all-access/user/{urllib.parse.quote(title.replace(' ', '_'), safe='')}"
           f"/daily/{start.strftime('%Y%m%d')}00/{end.strftime('%Y%m%d')}00")
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=45) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        return {"error": f"HTTP {exc.code}"}
    except Exception as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}"}


def main() -> None:
    ap = argparse.ArgumentParser(description="Pageviews Wikipedia per argomento (keyless)")
    ap.add_argument("titoli", nargs="*")
    ap.add_argument("--days", type=int, default=90)
    ap.add_argument("--project", default="it.wikipedia")
    ap.add_argument("--out")
    args = ap.parse_args()
    if not args.titoli:
        sys.exit("Nessun titolo: passali come argomenti (titoli esatti di voce, es. 'Hosting')")

    end = dt.date.today() - dt.timedelta(days=2)
    start = end - dt.timedelta(days=args.days)
    rows = []
    for t in args.titoli:
        d = views(args.project, t, start, end)
        if d is None:
            rows.append({"titolo": t, "media_giorno": None, "totale": None, "primo_mese": None,
                         "ultimo_mese": None, "trend": "nessun dato"})
            continue
        if isinstance(d, dict) and d.get("error"):
            rows.append({"titolo": t, "media_giorno": None, "totale": None, "primo_mese": None,
                         "ultimo_mese": None, "trend": d["error"]})
            continue
        items = d.get("items") or []
        if not items:
            rows.append({"titolo": t, "media_giorno": None, "totale": None, "primo_mese": None,
                         "ultimo_mese": None, "trend": "nessun dato"})
            continue
        per_month: dict[str, int] = {}
        tot = 0
        for it in items:
            v = int(it.get("views") or 0)
            tot += v
            per_month[it["timestamp"][:6]] = per_month.get(it["timestamp"][:6], 0) + v
        months = sorted(per_month)
        first, last = per_month[months[0]], per_month[months[-1]]
        prev = per_month[months[-2]] if len(months) >= 2 else None
        trend = "n/d" if prev in (None, 0) else ("su" if last > prev * 1.1 else ("giu" if last < prev * 0.9 else "piatto"))
        rows.append({"titolo": t, "media_giorno": round(tot / len(items), 1), "totale": tot,
                     "primo_mese": first, "ultimo_mese": last, "trend": trend})

    print(f"# Wikipedia Pageviews — {args.project} — {start} -> {end} (mai un volume di ricerca: letture di voce)")
    print(f"# {'voce':38s} {'media/gg':>9} {'totale':>8} {'ultimo mese':>11} {'trend':>7}")
    for r in rows:
        print(f"  {r['titolo'][:38]:38s} {str(r['media_giorno']):>9} {str(r['totale']):>8} "
              f"{str(r['ultimo_mese']):>11} {str(r['trend']):>7}")

    if args.out:
        path = os.path.abspath(os.path.expanduser(args.out))
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if path.endswith(".json"):
            json.dump(rows, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        else:
            with open(path, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=["titolo", "media_giorno", "totale", "primo_mese", "ultimo_mese", "trend"])
                w.writeheader()
                for r in rows:
                    w.writerow({k: ("" if v is None else v) for k, v in r.items()})
        print(f"# scritto: {path}")


if __name__ == "__main__":
    main()
