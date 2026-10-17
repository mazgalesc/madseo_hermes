#!/usr/bin/env python3
"""Verifica che ogni URL citata in un report ESISTA davvero.

Perche' esiste questo script: Search Console continua a riportare URL che Google ha ancora in
indice anche quando in WordPress non esistono piu' (slug rinominato senza redirect). Prendere una
riga di GSC per "una pagina" senza controllare produce affermazioni false (es. "due pagine in
concorrenza" quando la seconda e' un 404).

Uso:
  python3 check_urls.py https://il-tuo-sito.it/vecchio-slug/ https://il-tuo-sito.it/nuovo-slug/
  python3 check_urls.py --from-csv ~/seo-content/shared/keywords/gsc-page-query-90d-2026-10-13.csv

Esito per ogni URL: stato HTTP + esistenza in WordPress (post/pagina, qualsiasi stato).
La home e la pagina dei post NON esistono come post/pagina: per quelle vale solo lo stato HTTP.
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

HOME = pathlib.Path.home()
ENV = HOME / ".hermes" / ".env"


def impostazione(nome: str, ripiego: str = "") -> str:
    """Prima l'ambiente, poi `~/.hermes/.env`, poi il ripiego (come `inventario.py`)."""
    if os.environ.get(nome):
        return os.environ[nome]
    try:
        for riga in ENV.read_text().splitlines():
            if riga.startswith(nome + "="):
                return riga.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return ripiego


DOMINIO = impostazione("SITE_DOMAIN", "il-tuo-sito.it")
SITE = f"https://{DOMINIO}"
SEC = pathlib.Path(impostazione("WP_CREDENTIALS", str(HOME / ".hermes" / "secrets" / "wp-credentials.env")))
UA_STR = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
          "(KHTML, like Gecko) Chrome/145.0 Safari/537.36")


def per_suffisso(segreti: dict, suffisso: str) -> str:
    """Il valore della prima chiave che **finisce** così: i nomi cambiano da installazione a
    installazione (`WP_USER`, `<SITO>_WP_USER`…), e cercarli per nome intero fa fallire lo
    script dove basterebbe riconoscerli."""
    for k, v in segreti.items():
        if k.upper().endswith(suffisso):
            return v
    return ""


def wp_auth() -> str | None:
    creds: dict[str, str] = {}
    try:
        for line in SEC.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                creds[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        return None
    user, pwd = per_suffisso(creds, "_USER"), per_suffisso(creds, "APP_PASSWORD")
    if not user or not pwd:
        return None
    return "Basic " + base64.b64encode(f"{user}:{pwd}".encode()).decode()


def http_status(url: str) -> int | str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA_STR})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except Exception as exc:  # noqa: BLE001
        return f"ERR {type(exc).__name__}"


def wp_exists(url: str, auth: str | None) -> str:
    if not auth:
        return "(credenziali WP assenti)"
    slug = url.rstrip("/").split("/")[-1]
    if not slug:
        return "home (non e' un post/pagina)"
    hdrs = {"User-Agent": UA_STR, "Authorization": auth, "Accept": "application/json"}
    for kind in ("posts", "pages"):
        for status in ("publish", "draft,pending,future,private"):
            try:
                q = (f"{SITE}/wp-json/wp/v2/{kind}?slug={slug}&status={status}"
                     "&context=edit&_fields=id,status,slug")
                data = json.loads(urllib.request.urlopen(urllib.request.Request(q, headers=hdrs), timeout=30).read().decode())
                if data:
                    return f"{kind}:{data[0]['status']} (id {data[0]['id']})"
            except Exception:  # noqa: BLE001
                pass
    return "NON ESISTE in WordPress"


def urls_from_csv(path: str) -> list[str]:
    out: list[str] = []
    for row in csv.DictReader(open(os.path.expanduser(path), encoding="utf-8")):
        for key in ("pagina", "chiave", "url"):
            v = (row.get(key) or "").strip()
            if v.startswith("http") and v not in out:
                out.append(v)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Verifica esistenza delle URL citate in un report")
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--from-csv", action="append", default=[], help="CSV con colonna pagina/chiave/url")
    args = ap.parse_args()

    urls = list(args.urls)
    for p in args.from_csv:
        urls += [u for u in urls_from_csv(p) if u not in urls]
    if not urls:
        sys.exit("Nessuna URL: passale come argomenti o con --from-csv")

    auth = wp_auth()
    print(f"{'URL':62s} {'HTTP':>6}  WordPress")
    print("-" * 104)
    problematiche = 0
    for u in urls:
        st = http_status(u)
        ex = wp_exists(u, auth)
        bad = (st != 200) or ("NON ESISTE" in ex)
        if bad:
            problematiche += 1
        print(f"{u.replace(SITE,''):62s} {str(st):>6}  {ex}{'   <-- VERIFICARE' if bad else ''}")
    print(f"\n# URL verificate: {len(urls)} | con problemi: {problematiche}")
    if problematiche:
        print("# Regola: una URL che compare in Search Console NON e' una pagina viva finche' non passa questo controllo.")
        print("# Un 404 con impression pregresse = slug rinominato senza redirect: si corregge con un 301.")


if __name__ == "__main__":
    main()
