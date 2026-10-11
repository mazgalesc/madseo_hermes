#!/usr/bin/env python3
"""Riepilogo di stato di il-tuo-sito.it — SOLA LETTURA.

Mettere insieme in un colpo solo: stato SEO dal sito (via MCP), query di Search Console
e pagine di Analytics (via Maton).

Uso: ~/seo-content/.venv/bin/python stato-sito.py [--giorni 28]
Tutto passa da curl: Cloudflare blocca i client Python (errore 1010).
"""
import os
import argparse
import base64
import json
import pathlib
import subprocess
import urllib.parse

HOME = pathlib.Path.home()
SEC = pathlib.Path(os.environ.get("WP_CREDENTIALS", str(HOME / ".hermes" / "secrets" / "wp-credentials.env")))
ENV = HOME / ".hermes" / ".env"
MCP = os.environ.get("SITE_MCP_URL", "https://il-tuo-sito.it/wp-json/mcp/mcp-adapter-default-server")
DOMINIO = os.environ.get("SITE_DOMAIN", "il-tuo-sito.it")
MATON = "https://api.maton.ai"
PROPRIETA_GA4 = os.environ.get("GA4_PROPERTY_ID", "<ID-GA4>")


def leggi_segreti() -> dict:
    valori = {}
    for riga in SEC.read_text().splitlines():
        if "=" in riga and not riga.lstrip().startswith("#"):
            k, v = riga.split("=", 1)
            valori[k.strip()] = v.strip()
    for riga in ENV.read_text().splitlines():
        if riga.startswith("MATON_API_KEY="):
            valori["MATON_API_KEY"] = riga.split("=", 1)[1].strip()
    return valori


def curl(args: list[str]) -> tuple[int, str, dict]:
    """Esegue curl e restituisce (stato, corpo, intestazioni)."""
    r = subprocess.run(["curl", "-s", "-D", "/tmp/stato-hdr.txt", "-w", "\\n%{http_code}"] + args,
                       capture_output=True, text=True)
    fuori = r.stdout.rsplit("\n", 1)
    corpo = fuori[0] if len(fuori) == 2 else r.stdout
    stato = int(fuori[1]) if len(fuori) == 2 and fuori[1].strip().isdigit() else 0
    intestazioni = {}
    for riga in pathlib.Path("/tmp/stato-hdr.txt").read_text().splitlines():
        if ":" in riga:
            k, v = riga.split(":", 1)
            intestazioni[k.strip().lower()] = v.strip()
    return stato, corpo, intestazioni


def sblocca(testo: str):
    """Le risposte MCP arrivano come SSE: estrae il JSON."""
    for riga in testo.splitlines():
        riga = riga.strip()
        if riga.startswith("data:"):
            riga = riga[5:].strip()
        if riga.startswith("{"):
            try:
                return json.loads(riga)
            except json.JSONDecodeError:
                continue
    try:
        return json.loads(testo)
    except Exception:
        return None


def abilita(segreti: dict, nome: str, parametri: dict | None = None):
    """Esegue un'abilita' di WordPress via MCP (sola lettura se l'abilita' e' di lettura)."""
    basic = base64.b64encode(f"{segreti['WP_USER']}:{segreti['WP_APP_PASSWORD']}".encode()).decode()
    comuni = ["-u", f"{segreti['WP_USER']}:{segreti['WP_APP_PASSWORD']}",
              "-H", "Content-Type: application/json",
              "-H", "Accept: application/json, text/event-stream"]
    _, corpo, hdr = curl(comuni + ["-X", "POST", MCP, "-d", json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "hermes", "version": "0.1"}}})])
    sid = hdr.get("mcp-session-id", "")
    if not sid:
        return {"errore": f"nessuna sessione MCP (risposta: {corpo[:120]})"}
    curl(comuni + ["-H", f"Mcp-Session-Id: {sid}", "-X", "POST", MCP,
                   "-d", json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"})])
    _, corpo, _ = curl(comuni + ["-H", f"Mcp-Session-Id: {sid}", "-X", "POST", MCP, "-d", json.dumps({
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": "mcp-adapter-execute-ability",
                   "arguments": {"ability_name": nome, "parameters": parametri or {}}}})])
    d = sblocca(corpo)
    if not d:
        return {"errore": corpo[:200]}
    testo = ((d.get("result") or {}).get("content") or [{}])[0].get("text", "")
    try:
        return json.loads(testo)
    except Exception:
        return {"testo": testo[:400]}


def maton(segreti: dict, percorso: str, corpo: dict):
    r = subprocess.run(["curl", "-s", MATON + percorso,
                        "-H", f"Authorization: Bearer {segreti['MATON_API_KEY']}",
                        "-H", "Content-Type: application/json",
                        "-d", json.dumps(corpo)], capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except Exception:
        return {"errore": r.stdout[:200]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--giorni", type=int, default=28)
    args = ap.parse_args()
    segreti = leggi_segreti()
    from datetime import date, timedelta
    fine = date.today()
    inizio_data = fine - timedelta(days=args.giorni)
    inizio = inizio_data.isoformat()          # la Search Console vuole date esplicite
    fine_iso = fine.isoformat()

    def stampa(dati, rientro=2):
        spazio = " " * rientro
        if isinstance(dati, dict):
            for k, v in dati.items():
                if isinstance(v, (dict, list)):
                    print(f"{spazio}{k}:")
                    stampa(v, rientro + 2)
                else:
                    print(f"{spazio}{k}: {v}")
        elif isinstance(dati, list):
            for v in dati[:12]:
                stampa(v, rientro + 2)
        else:
            print(f"{spazio}{dati}")

    print("=" * 70)
    print(f"STATO {DOMINIO} — dal {inizio} al {fine_iso}")
    print("=" * 70)

    print("\n### Sito (abilità seo via MCP)")
    riassunto = abilita(segreti, "seo/get-site-seo-summary")
    if isinstance(riassunto, dict) and "errore" not in riassunto:
        dati = riassunto.get("data", riassunto)
        stampa(dati)
    else:
        print(f"  non disponibile: {str(riassunto)[:160]}")

    print("\n### Search Console — query principali")
    sito = urllib.parse.quote("https://il-tuo-sito.it/", safe="")
    gsc = maton(segreti, f"/google-search-console/webmasters/v3/sites/{sito}/searchAnalytics/query",
                {"startDate": inizio, "endDate": fine_iso, "dimensions": ["query"], "rowLimit": 10})
    righe = gsc.get("rows") or []
    if righe:
        print(f"  {'clic':>5} {'impr':>7} {'CTR':>6} {'pos':>5}  query")
        for r in righe:
            print(f"  {int(r['clicks']):>5} {int(r['impressions']):>7} {r['ctr']*100:>5.1f}% {r['position']:>5.1f}  {r['keys'][0][:52]}")
    else:
        print(f"  nessun dato ({str(gsc)[:160]})")

    print("\n### Analytics — pagine principali")
    ga = maton(segreti, f"/google-analytics-data/v1beta/properties/{PROPRIETA_GA4}:runReport",
               {"dateRanges": [{"startDate": inizio, "endDate": "today"}],
                "dimensions": [{"name": "pagePath"}], "metrics": [{"name": "sessions"}],
                "orderBys": [{"metric": {"metricName": "sessions"}, "desc": True}], "limit": 10})
    righe = ga.get("rows") or []
    if righe:
        for r in righe:
            print(f"  {int(r['metricValues'][0]['value']):>5} sessioni  {r['dimensionValues'][0]['value'][:56]}")
    else:
        print(f"  nessun dato ({str(ga)[:160]})")

    print("\n(sola lettura: nessuna modifica e' stata fatta)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
