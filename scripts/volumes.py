#!/usr/bin/env python3
"""Volumi di ricerca reali via DataForSEO (Keywords Data -> Google Ads).

Costa denaro: ogni task in coda standard costa $0,06 e copre fino a 1.000 keyword
(live: $0,09). Lo script stampa il costo dichiarato dall'API a fine chiamata.

Uso:
  python3 volumes.py hosting wordpress "quanto costa un sito web"      # live, poche keyword
  python3 volumes.py --keywords-file ~/seo-content/shared/shortlist.txt --queue standard --out ~/seo-content/audits/volumi.csv
  python3 volumes.py --keywords-file shortlist.txt --location 2380 --language it

Credenziali: DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD in $HERMES_HOME/.env (Basic auth).
Un account non verificato risponde 40104: va verificato su https://app.dataforseo.com/ .
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://api.dataforseo.com"
SANDBOX = "https://sandbox.dataforseo.com"
ENDPOINT = "/v3/keywords_data/google_ads/search_volume"
LOCATIONS = {"it": 2380, "us": 2840, "gb": 2826, "de": 2276, "fr": 2250, "es": 2724}


def load_env() -> dict[str, str]:
    out: dict[str, str] = {}
    home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
    for path in (os.path.join(home, ".env"), os.path.expanduser("~/.hermes/.env")):
        if not os.path.exists(path):
            continue
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def auth_header(env: dict[str, str]) -> str:
    login, pwd = env.get("DATAFORSEO_LOGIN"), env.get("DATAFORSEO_PASSWORD")
    if not login or not pwd:
        sys.exit("DATAFORSEO_LOGIN / DATAFORSEO_PASSWORD mancanti in $HERMES_HOME/.env")
    return "Basic " + base64.b64encode(f"{login}:{pwd}".encode()).decode()


def call(auth: str, path: str, body=None, base: str = API, timeout: int = 90):
    req = urllib.request.Request(
        base + path,
        data=(json.dumps(body).encode() if body is not None else None),
        headers={"Authorization": auth, "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        try:
            return exc.code, json.loads(exc.read().decode())
        except Exception:
            return exc.code, {"status_message": "HTTP error"}
    except Exception as exc:  # noqa: BLE001
        return None, {"status_message": f"{type(exc).__name__}: {exc}"}


def guard(status: int | None, payload: dict) -> None:
    if isinstance(payload, dict) and payload.get("status_code") == 40104:
        sys.exit("DataForSEO: account non verificato (40104). Verificalo su https://app.dataforseo.com/ "
                 "prima di usare l'API.")
    if status != 200 or not isinstance(payload, dict) or payload.get("status_code") != 20000:
        sys.exit(f"DataForSEO errore: HTTP {status} — {json.dumps(payload)[:400]}")


def main() -> None:
    ap = argparse.ArgumentParser(description="Volumi DataForSEO (Keywords Data / Google Ads)")
    ap.add_argument("keywords", nargs="*")
    ap.add_argument("--keywords-file")
    ap.add_argument("--queue", default="live", choices=["live", "standard"])
    ap.add_argument("--location", default="it", help="codice paese (it, us…) o numero location_code")
    ap.add_argument("--language", default="it")
    ap.add_argument("--out")
    ap.add_argument("--sandbox", action="store_true",
                    help="host sandbox.dataforseo.com: risposte FINte e costo $0, per collaudare la pipeline")
    args = ap.parse_args()

    kws = list(args.keywords)
    if args.keywords_file:
        kws += [l.strip() for l in open(os.path.expanduser(args.keywords_file), encoding="utf-8")
                if l.strip() and not l.startswith("#")]
    if not kws:
        sys.exit("Nessuna keyword: passale come argomenti o con --keywords-file")
    if len(kws) > 1000:
        sys.exit("Un task copre al massimo 1.000 keyword: dividi la lista")

    loc = LOCATIONS.get(args.location, None) if not args.location.isdigit() else int(args.location)
    base = SANDBOX if args.sandbox else API
    if args.sandbox:
        print("# SANDBOX: risposte finte, nessun addebito sull'account.")
    auth = auth_header(load_env())
    task = {"keywords": kws, "language_code": args.language, "location_code": loc or 2380,
            "search_partners": False}

    if args.queue == "live":
        status, payload = call(auth, ENDPOINT + "/live", [task], base=base)
        guard(status, payload)
        result = (payload["tasks"][0].get("result") or [])
        cost = payload["tasks"][0].get("cost")
    else:
        status, payload = call(auth, ENDPOINT + "/task_post", [task], base=base)
        guard(status, payload)
        task_id = payload["tasks"][0]["id"]
        result, cost = [], None
        for _ in range(30):
            time.sleep(6)
            status, payload = call(auth, f"{ENDPOINT}/task_get/{task_id}", base=base)
            if status == 200 and isinstance(payload, dict) and payload.get("status_code") == 20000:
                t = payload["tasks"][0]
                if t.get("status_code") == 20000:
                    result = t.get("result") or []
                    cost = t.get("cost")
                    break
        else:
            sys.exit("DataForSEO: task non completato entro l'attesa")

    rows = []
    for r in result:
        rows.append({
            "keyword": r.get("keyword"),
            "volume": (r.get("search_volume") if r.get("search_volume") is not None else "n/d"),
            "cpc": r.get("cpc"),
            "competition": r.get("competition"),
            "competition_index": r.get("competition_index"),
            "tipo": r.get("search_volume_type") or "esatto",
        })
    rows.sort(key=lambda x: (x["volume"] if isinstance(x["volume"], int) else -1), reverse=True)

    print(f"# DataForSEO — {len(kws)} keyword — location {loc or 2380} / {args.language} — coda {args.queue}")
    print(f"# {'keyword':45s} {'volume':>8} {'tipo':>8} {'cpc':>6} {'compet.':>8}")
    for r in rows:
        print(f"  {str(r['keyword'])[:45]:45s} {str(r['volume']):>8} {str(r['tipo'])[:8]:>8} "
              f"{str(r['cpc'])[:6]:>6} {str(r['competition'])[:8]:>8}")
    if not rows:
        print("  (nessun risultato)")
    print(f"# costo dichiarato dall'API: ${cost if cost is not None else '?'} "
          f"({'live' if args.queue == 'live' else 'standard queue'})")

    if args.out:
        path = os.path.abspath(os.path.expanduser(args.out))
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        if path.endswith(".json"):
            json.dump(rows, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        else:
            with open(path, "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=["keyword", "volume", "tipo", "cpc", "competition", "competition_index"])
                w.writeheader()
                w.writerows(rows)
        print(f"# scritto: {path}")


if __name__ == "__main__":
    main()
