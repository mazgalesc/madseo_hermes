#!/usr/bin/env python3
"""Riepilogo dello stato del sito — SOLA LETTURA.

Mettere insieme in un colpo solo: stato SEO dal sito (via MCP), query di Search Console
e pagine di Analytics (via Maton).

Uso: python3 stato-sito.py [--giorni 28]      (solo libreria standard: nessun venv serve)

Tutto passa da curl: Cloudflare blocca i client Python (errore 1010).
"""
from __future__ import annotations

import os
import argparse
import json
import pathlib
import subprocess
import urllib.parse

HOME = pathlib.Path.home()
ENV = HOME / ".hermes" / ".env"


def impostazione(nome: str, ripiego: str = "") -> str:
    """Legge una variabile: prima l'ambiente, poi `~/.hermes/.env`, poi il ripiego.

    Stesso ordine di `verifica-avvio.py`, e per la stessa ragione: quando un agente lancia lo
    script **l'ambiente non è quasi mai esportato**, quindi senza questo passo il file di
    configurazione non viene mai letto e lo script cerca percorsi che non esistono.
    """
    if os.environ.get(nome):
        return os.environ[nome]
    try:
        for riga in ENV.read_text().splitlines():
            if riga.startswith(nome + "="):
                valore = riga.split("=", 1)[1].strip()
                return valore.strip('"').strip("'")
    except OSError:
        pass
    return ripiego


SEC = pathlib.Path(impostazione("WP_CREDENTIALS", str(HOME / ".hermes" / "secrets" / "wp-credentials.env")))
DOMINIO = impostazione("SITE_DOMAIN", "il-tuo-sito.it")
MCP = impostazione("SITE_MCP_URL", f"https://{DOMINIO}/wp-json/mcp/mcp-adapter-default-server")
MATON = "https://api.maton.ai"
PROPRIETA_GA4 = impostazione("GA4_PROPERTY_ID", "")


def leggi_segreti() -> dict:
    """Le credenziali e la chiave Maton, senza mai stamparle.

    Un file assente **non fa cadere lo script**: torna quello che c'è e sarà il controllo a
    dichiarare cosa manca, con una riga leggibile invece di un traceback.
    """
    valori = {}
    try:
        for riga in SEC.read_text().splitlines():
            if "=" in riga and not riga.lstrip().startswith("#"):
                k, v = riga.split("=", 1)
                valori[k.strip()] = v.strip()
    except OSError:
        pass
    try:
        for riga in ENV.read_text().splitlines():
            if riga.startswith("MATON_API_KEY="):
                valori["MATON_API_KEY"] = riga.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return valori


def per_suffisso(segreti: dict, suffisso: str) -> str:
    """Il valore della prima chiave che finisce così.

    I nomi delle voci cambiano da installazione a installazione (`WP_USER`, `MADWEB_WP_USER`,
    il nome del sito…): si riconosce la chiave **dal suffisso**, non dal nome intero. Cercarle
    per nome intero fa fallire lo script su ogni installazione che le ha nominate diversamente.
    """
    for k, v in segreti.items():
        if k.upper().endswith(suffisso):
            return v
    return ""


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


_SESSIONE: dict = {}
_ELENCO: dict = {}


def _sessione(segreti: dict) -> tuple[list, str]:
    """Intestazioni comuni e session id. La sessione si apre una volta sola e si riusa.

    **L'header `MCP-Protocol-Version` è obbligatorio** su ogni chiamata dopo l'`initialize`:
    senza, il server risponde `400 Invalid Request: MCP-Protocol-Version header is required for a
    2025-06-18 session` e sembra un problema di credenziali. È la trappola documentata in
    `references/wordpress-content-audit-mcp.md` — e vale per gli script come per gli agenti.
    """
    if _SESSIONE.get("sid"):
        return _SESSIONE["comuni"], _SESSIONE["sid"]
    utente, password = per_suffisso(segreti, "_USER"), per_suffisso(segreti, "APP_PASSWORD")
    comuni = ["-u", f"{utente}:{password}",
              "-H", "Content-Type: application/json",
              "-H", "Accept: application/json, text/event-stream"]
    _, _, hdr = curl(comuni + ["-X", "POST", MCP, "-d", json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "hermes", "version": "0.1"}}})])
    sid = hdr.get("mcp-session-id", "")
    if not sid:
        return comuni, ""
    comuni = comuni + ["-H", f"Mcp-Session-Id: {sid}",
                       "-H", "MCP-Protocol-Version: 2025-06-18"]
    curl(comuni + ["-X", "POST", MCP,
                   "-d", json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"})])
    _SESSIONE.update({"comuni": comuni, "sid": sid})
    return comuni, sid


def _chiama(segreti: dict, strumento: str, argomenti: dict, id_: int = 2) -> dict:
    comuni, sid = _sessione(segreti)
    if not sid:
        return {}
    _, corpo, _ = curl(comuni + ["-X", "POST", MCP, "-d", json.dumps({
        "jsonrpc": "2.0", "id": id_, "method": "tools/call",
        "params": {"name": strumento, "arguments": argomenti}})])
    return sblocca(corpo) or {}


def _testo(d: dict) -> str:
    return ((d.get("result") or {}).get("content") or [{}])[0].get("text", "")


def _risolvi(segreti: dict, nome: str) -> str:
    """`seo/get-site-seo-summary` -> `madweb-seo/get-site-seo-summary`.

    Il namespace delle abilità è **generico** nel testo della skill (`seo/*`, vedi
    `configurazione.md`) e cambia da installazione a installazione: si scopre dall'elenco invece
    di darlo per scontato. Un nome già valido passa intatto.
    """
    if not _ELENCO:
        try:
            voci = (json.loads(_testo(_chiama(segreti, "mcp-adapter-discover-abilities", {}))) or {}).get("abilities") or []
        except Exception:  # noqa: BLE001
            voci = []
        _ELENCO.update({v["name"]: v for v in voci if isinstance(v, dict) and v.get("name")})
    if nome in _ELENCO or not _ELENCO:
        return nome
    corto = nome.split("/", 1)[-1]
    candidati = sorted(n for n in _ELENCO if n.endswith("/" + corto))
    return candidati[0] if candidati else nome


def abilita(segreti: dict, nome: str, parametri: dict | None = None) -> dict:
    """Esegue un'abilità di WordPress via MCP (sola lettura se l'abilità è di lettura)."""
    risolto = _risolvi(segreti, nome)
    d = _chiama(segreti, "mcp-adapter-execute-ability",
                {"ability_name": risolto, "parameters": parametri or {}})
    if not d:
        return {"errore": f"nessuna risposta dal server MCP ({MCP})"}
    if (d.get("result") or {}).get("isError"):
        return {"errore": _testo(d) or f"l'abilità {risolto} non ha risposto"}
    testo = _testo(d)
    try:
        return json.loads(testo)
    except Exception:  # noqa: BLE001
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
    if not SEC.exists():
        print(f"Credenziali non trovate: manca {SEC}")
        print("  Si consegnano fuori chat, in un file con permessi 600 (primo-avvio.md, passo 3).")
        print("  Senza, si leggono solo le parti che non passano da WordPress.\n")
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
    sito = urllib.parse.quote(f"https://{DOMINIO}/", safe="")
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
