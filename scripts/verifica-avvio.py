#!/usr/bin/env python3
"""Controllo d'avvio (procedura 0) — SOLA LETTURA, non modifica e non pubblica niente.

Verifica in un colpo solo quello che serve al primo avvio: cartella di lavoro, database del piano,
credenziali (presenza e permessi: **mai i valori**), vault delle note, server MCP del sito, REST,
Search Console e Analytics via Maton.

Stampa per ogni voce: OK, DA FARE, ASSENTE o SALTATO — e un riepilogo. Quello che manca **si dichiara**,
non blocca il resto: immagini, Scrapling e `ddgs` sono opzionali.

Uso:  python3 verifica-avvio.py [--dominio il-tuo-sito.it] [--silenzioso]

I valori veri si leggono dall'ambiente (SEO_WORK_DIR, SITE_DOMAIN, SITE_MCP_URL, WP_CREDENTIALS,
GA4_PROPERTY_ID, OBSIDIAN_VAULT_PATH) e dal file di credenziali; se mancano, valgono i ripieghi di
`references/configurazione.md`. Nessun valore viene stampato.
"""
import argparse
import json
import os
import pathlib
import re
import subprocess

HOME = pathlib.Path.home()
ENV = HOME / ".hermes" / ".env"


def impostazione(nome: str, ripiego: str = "") -> str:
    """Legge una variabile: prima l'ambiente, poi il file locale di configurazione, poi il ripiego."""
    if os.environ.get(nome):
        return os.environ[nome]
    try:
        for riga in ENV.read_text().splitlines():
            if riga.startswith(nome + "="):
                return riga.split("=", 1)[1].strip().strip('"').strip("'")
    except OSError:
        pass
    return ripiego


LAVORO = pathlib.Path(impostazione("SEO_WORK_DIR", str(HOME / "seo-content")))
DOMINIO = impostazione("SITE_DOMAIN", "il-tuo-sito.it")
MCP = impostazione("SITE_MCP_URL", f"https://{DOMINIO}/wp-json/mcp/mcp-adapter-default-server")
CRED = pathlib.Path(impostazione("WP_CREDENTIALS", str(HOME / ".hermes" / "secrets" / "wp-credentials.env")))
VAULT = pathlib.Path(impostazione("OBSIDIAN_VAULT_PATH", str(HOME / "Documents" / "Obsidian Vault")))
GA4 = impostazione("GA4_PROPERTY_ID", "")
MATON = "https://api.maton.ai"

esiti: list[tuple[str, str, str]] = []   # (voce, esito, nota)


def segna(voce: str, esito: str, nota: str = "") -> None:
    esiti.append((voce, esito, nota))


def valori_locali() -> dict:
    """Nomi delle credenziali disponibili (mai i valori)."""
    fuori = {}
    for f in (CRED, ENV):
        try:
            for riga in f.read_text().splitlines():
                if "=" in riga and not riga.lstrip().startswith("#"):
                    k, v = riga.split("=", 1)
                    fuori[k.strip()] = v.strip().strip('"').strip("'")
        except OSError:
            pass
    return fuori


def per_suffisso(segreti: dict, suffisso: str) -> str:
    """Il valore della prima chiave che finisce così (i nomi cambiano da installazione a installazione)."""
    for k, v in segreti.items():
        if k.upper().endswith(suffisso):
            return v
    return ""


def basic(segreti: dict) -> str:
    """La credenziale Basic: quella dichiarata, oppure costruita da utente + application password."""
    dichiarata = per_suffisso(segreti, "BASIC_AUTH")
    if dichiarata:
        return dichiarata if dichiarata.lower().startswith("basic ") else "Basic " + dichiarata
    import base64
    u, pw = per_suffisso(segreti, "_USER"), per_suffisso(segreti, "APP_PASSWORD")
    return "Basic " + base64.b64encode(f"{u}:{pw}".encode()).decode() if u and pw else ""


def curl(stato_su: pathlib.Path, args: list[str]) -> tuple[int, str]:
    r = subprocess.run(["curl", "-s", "-o", str(stato_su), "-w", "%{http_code}",
                        "--max-time", "20"] + args, capture_output=True, text=True)
    codice = int(r.stdout.strip()) if r.stdout.strip().isdigit() else 0
    try:
        corpo = stato_su.read_text()[:4000]
    except OSError:
        corpo = ""
    return codice, corpo


def main() -> None:
    ap = argparse.ArgumentParser(description="Controllo d'avvio della skill (procedura 0)")
    ap.add_argument("--dominio", default=DOMINIO, help="dominio del sito (default: SITE_DOMAIN)")
    ap.add_argument("--silenzioso", action="store_true", help="solo il riepilogo finale")
    args = ap.parse_args()
    dominio = args.dominio
    temp = pathlib.Path("/tmp/verifica-avvio.out")

    # 1. cartella di lavoro
    mancanti = [c for c in ("content", "audits", "distribution", "shared") if not (LAVORO / c).is_dir()]
    segna("Cartella di lavoro", "OK" if not mancanti else "DA FARE",
          f"{LAVORO}" + (f" — mancano: {', '.join(mancanti)}" if mancanti else ""))

    # 2. database del piano
    db = LAVORO / "shared" / "lavoro.db"
    if not db.exists():
        segna("Database del piano", "DA FARE", f"manca {db} (schema in references/db-schema.md)")
    else:
        try:
            import sqlite3
            cx = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            colonne = [r[1] for r in cx.execute("PRAGMA table_info(content_calendar)")]
            righe = cx.execute("select count(*) from content_calendar").fetchone()[0]
            cx.close()
            attese = {"promessa", "copre_gia"}
            senza = attese - set(colonne)
            segna("Database del piano", "OK" if not senza else "DA FARE",
                  f"{len(colonne)} colonne, {righe} righe" + (f" — mancano le colonne: {', '.join(sorted(senza))}" if senza else ""))
        except Exception as e:  # noqa: BLE001
            segna("Database del piano", "DA FARE", f"non leggibile: {type(e).__name__}")

    # 3. credenziali (presenza e permessi, mai i valori)
    segreti = valori_locali()
    if not CRED.exists():
        segna("Credenziali WordPress", "ASSENTE", f"manca {CRED} — le consegna l'autore, fuori chat")
    else:
        modo = oct(CRED.stat().st_mode & 0o777)[-3:]
        nomi = sorted(k for k in segreti if re.match(r".*(USER|PASSWORD|APP_PASSWORD)$", k))
        segna("Credenziali WordPress", "OK" if modo == "600" else "DA FARE",
              f"permessi {modo}" + ("" if modo == "600" else " (devono essere 600)") +
              f" · voci presenti: {', '.join(nomi) if nomi else 'nessuna'}")

    # 4. vault delle note
    segna("Vault delle note", "OK" if VAULT.is_dir() else "SALTATO",
          f"{VAULT}" if VAULT.is_dir() else f"non configurato o assente ({VAULT}) — è consigliato, non obbligatorio")

    # 5. server MCP del sito (handshake initialize)
    intestazioni = ["-H", "Content-Type: application/json",
                    "-H", "Accept: application/json, text/event-stream"]
    credenziale = basic(segreti)
    if credenziale:
        intestazioni += ["-H", f"Auth: {credenziale}"]
    corpo = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                                   "clientInfo": {"name": "verifica-avvio", "version": "1.0"}}})
    # l'header giusto dipende dal server: si provano in ordine e si dice quale ha risposto
    codice, risposta, usato = 0, "", ""
    for nome_header in ("Authorization", "Auth"):
        prova = [*intestazioni]
        if credenziale:
            prova += ["-H", f"{nome_header}: {credenziale}"]
        codice, risposta = curl(temp, ["-X", "POST", MCP, *prova, "-d", corpo])
        if codice == 200:
            usato = nome_header
            break
    if codice == 200:
        segna("Server MCP (initialize)", "OK", f"{dominio} — risponde all'handshake con l'header {usato}")
    elif codice in (401, 403):
        segna("Server MCP (initialize)", "DA FARE",
              f"{codice}: header o credenziale. Provare Authorization e poi Auth")
    elif codice == 405:
        segna("Server MCP (initialize)", "DA FARE", "405: credenziali accettate, metodo sbagliato per l'handshake")
    elif codice == 400:
        segna("Server MCP (initialize)", "DA FARE", "400: manca il protocollo (protocolVersion) nella richiesta")
    else:
        segna("Server MCP (initialize)", "ASSENTE",
              f"{codice or 'nessuna risposta'}: {MCP} — se non c'è, si lavora via REST e si dichiara")

    # 6. il sito: pagina pubblica e REST
    codice, _ = curl(temp, [f"https://{dominio}/"])
    segna("Sito raggiungibile", "OK" if codice == 200 else "ASSENTE", f"{dominio}: {codice or 'nessuna risposta'}")

    codice, _ = curl(temp, ["-u", f"{per_suffisso(segreti, '_USER')}:{per_suffisso(segreti, 'APP_PASSWORD')}",
                            f"https://{dominio}/wp-json/wp/v2/users/me?context=edit"])
    mcp_ok = any(v == "Server MCP (initialize)" and e == "OK" for v, e, _ in esiti)
    if codice == 200:
        segna("REST con application password", "OK", "utente e credenziale validi")
    elif codice in (401, 403) and mcp_ok:
        segna("REST con application password", "SALTATO",
              f"{codice}: il sito blocca il REST diretto — si passa dall'MCP, che risponde")
    elif codice in (401, 403):
        segna("REST con application password", "DA FARE",
              f"{codice}: utente o application password non validi (o header dell'MCP da correggere)")
    else:
        segna("REST con application password", "ASSENTE", f"{codice or 'nessuna risposta'}")

    # 7. Maton: Search Console e Analytics
    if segreti.get("MATON_API_KEY"):
        codice, _ = curl(temp, ["-H", f"Authorization: Bearer {segreti['MATON_API_KEY']}",
                                f"{MATON}/connections"])
        segna("Maton (Search Console, Analytics)", "OK" if codice == 200 else "DA FARE",
              f"connessioni: {codice}")
    else:
        segna("Maton (Search Console, Analytics)", "SALTATO", "nessuna chiave Maton: si dichiara e si va avanti")
    segna("Proprietà Analytics", "OK" if GA4 else "SALTATO",
          f"GA4_PROPERTY_ID {'impostata' if GA4 else 'non impostata: il report Analytics non è disponibile'}")

    # 8. riepilogo
    if not args.silenzioso:
        larghezza = max(len(v) for v, _, _ in esiti)
        for voce, esito, nota in esiti:
            print(f"   {voce.ljust(larghezza)}  {esito.ljust(9)} {nota}")
        print()
    conteggio = {}
    for _, esito, _ in esiti:
        conteggio[esito] = conteggio.get(esito, 0) + 1
    print(f"Controllo d'avvio su {dominio}: " + " · ".join(f"{n} {e}" for e, n in sorted(conteggio.items())))
    da_fare = [v for v, e, _ in esiti if e in ("DA FARE", "ASSENTE")]
    if da_fare:
        print("Da sistemare: " + ", ".join(da_fare))
        print("Quello che manca si dichiara all'autore: non si inventa e non blocca il resto.")
    else:
        print("Tutto quello che serve c'è. Il contenuto lo pubblica solo l'autore (regola 1).")


if __name__ == "__main__":
    main()
