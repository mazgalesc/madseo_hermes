#!/usr/bin/env python3
"""Verifica GRATUITA delle credenziali SEO: nessun task a pagamento.

Ogni fonte usata dagli script di questa skill ha un endpoint che non costa nulla. Usare questo
script quando le chiavi vengono aggiunte, spostate fra profili o ruotate: un task `search_volume`
live costa soldi, `appendix/user_data` no. Lo script non stampa MAI il valore di una chiave —
solo presenza, lunghezza implicita ed esito della chiamata.

Uso:
  python3 check_credentials.py
  python3 check_credentials.py --term hosting --country it --language it-IT

Esito: 0 se ogni chiave PRESENTE risponde; 1 se almeno una chiave presente fallisce.
Una chiave assente non e' un errore: viene segnalata come lacuna.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

DATAFORSEO = "https://api.dataforseo.com"
MATON = "https://api.maton.ai"
BING = "https://ssl.bing.com/webmaster/api.svc/json/GetKeywordStats"


def load_env() -> dict[str, str]:
    """Prima $HERMES_HOME/.env, poi ~/.hermes/.env; l'ambiente vero vince su entrambi."""
    out: dict[str, str] = {}
    home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
    for path in (os.path.join(home, ".env"), os.path.expanduser("~/.hermes/.env")):
        if not os.path.exists(path):
            continue
        try:
            fh = open(path, encoding="utf-8")
        except OSError:
            continue
        with fh:
            for line in fh:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                out.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    out.update(os.environ)
    return out


def get(url: str, headers: dict[str, str], timeout: int = 45):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, json.loads(resp.read().decode("utf-8", "replace"))


def _err(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        try:
            body = exc.read()[:200].decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            body = "(corpo non leggibile)"
        return f"HTTP {exc.code} — {body}"
    return f"{type(exc).__name__}: {exc}"


def probe_dataforseo(login: str, password: str) -> tuple[bool, str]:
    auth = "Basic " + base64.b64encode(f"{login}:{password}".encode()).decode()
    try:
        _, payload = get(DATAFORSEO + "/v3/appendix/user_data", {"Authorization": auth})
    except Exception as exc:  # noqa: BLE001
        return False, _err(exc)

    task = (payload.get("tasks") or [{}])[0]
    if payload.get("status_code") != 20000 or task.get("status_code") != 20000:
        return False, (f"status_code {payload.get('status_code')} / {task.get('status_code')} — "
                       f"{payload.get('status_message') or task.get('status_message')}")
    res = (task.get("result") or [{}])[0]
    money = res.get("money") or {}
    return True, (f"login={res.get('login')} tz={res.get('timezone')} "
                  f"saldo ${money.get('balance')} — endpoint a costo 0")


def probe_bing(key: str, term: str, country: str, language: str) -> tuple[bool, str]:
    url = (f"{BING}?q={urllib.parse.quote(term)}&country={urllib.parse.quote(country)}"
           f"&language={urllib.parse.quote(language)}&apikey={urllib.parse.quote(key)}")
    try:
        _, payload = get(url, {"User-Agent": "Mozilla/5.0"})
    except Exception as exc:  # noqa: BLE001
        return False, _err(exc)

    rows = payload.get("d") or []
    if not rows:
        return True, (f"200 ma nessun dato per '{term}' — termine sotto la soglia di reportistica "
                      f"Bing, non un errore di chiave")
    dates = []
    for r in rows:
        digits = "".join(c for c in str(r.get("Date", "")) if c.isdigit())[:13]
        if digits:
            dates.append(dt.datetime.fromtimestamp(int(digits) / 1000, tz=dt.timezone.utc).date())
    window = f"{min(dates)} -> {max(dates)}" if dates else "n/d"
    return True, f"{len(rows)} settimane per '{term}' — finestra {window}"


def probe_maton(key: str) -> tuple[bool, str]:
    try:
        _, payload = get(MATON + "/connections", {"Authorization": "Bearer " + key})
    except Exception as exc:  # noqa: BLE001
        return False, _err(exc)

    conns = payload.get("connections") or []
    active = sorted({str(c.get("app")) for c in conns
                     if str(c.get("status", "")).upper() == "ACTIVE"})
    if not active:
        return False, f"{len(conns)} connessioni, nessuna ACTIVE"
    return True, f"{len(active)} ACTIVE: {', '.join(active)}"


def main() -> None:
    ap = argparse.ArgumentParser(description="Verifica gratuita delle credenziali SEO")
    ap.add_argument("--term", default="hosting", help="termine di test per Bing (un head term)")
    ap.add_argument("--country", default="it")
    ap.add_argument("--language", default="it-IT",
                    help="tag completo: 'it' da solo fa rispondere HTTP 400 a Bing")
    args = ap.parse_args()

    env = load_env()
    checks = [
        ("DataForSEO", ("DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD")),
        ("Bing Webmaster", ("BING_WEBMASTER_API_KEY",)),
        ("Maton (GSC/GA4)", ("MATON_API_KEY",)),
    ]

    home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
    print("# Verifica credenziali SEO — solo endpoint gratuiti, nessun task a pagamento")
    print(f"# .env: {os.path.join(home, '.env')}")
    print()

    missing: list[str] = []
    failed: list[str] = []
    for name, keys in checks:
        absent = [k for k in keys if not env.get(k)]
        if absent:
            missing.append(name)
            print(f"  {name:18s} {'ASSENTE':9s} {', '.join(absent)} non configurata")
            continue
        if name == "DataForSEO":
            ok, detail = probe_dataforseo(env["DATAFORSEO_LOGIN"], env["DATAFORSEO_PASSWORD"])
        elif name == "Bing Webmaster":
            ok, detail = probe_bing(env["BING_WEBMASTER_API_KEY"], args.term, args.country, args.language)
        else:
            ok, detail = probe_maton(env["MATON_API_KEY"])
        print(f"  {name:18s} {'OK' if ok else 'FALLITA':9s} {detail}")
        if not ok:
            failed.append(name)

    print()
    if failed:
        print(f"# ESITO: {len(failed)} fonte/i fallita/e — {', '.join(failed)}")
    else:
        print("# ESITO: ogni chiave configurata risponde.")
    if missing:
        print(f"# Non configurate (non un errore): {', '.join(missing)}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
