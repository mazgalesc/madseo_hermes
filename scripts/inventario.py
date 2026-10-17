#!/usr/bin/env python3
"""Rigenera INVENTARIO.md leggendo il sito — SOLA LETTURA.

Perché esiste. L'inventario è **il file su cui gira il controllo anti-duplicato**: prima di
proporre un titolo si confrontano le promesse con quello che il sito ha già. Finché nessuno
lo rigenerava, il file invecchiava in silenzio — e un inventario vecchio è **peggio di nessun
inventario**, perché dice «libera» a una promessa già coperta (è successo: dichiarava 45
pubblicati e 15 bozze mentre il sito ne aveva 47 e 13, e in coda c'era una voce già coperta da
un articolo pubblicato). Quindi: si lancia **prima** di ogni confronto, non si cita a memoria.

Cosa legge e da dove:
  * gli elenchi e i **conteggi** dal REST di WordPress (`status=publish|draft|future|trash`,
    più le pagine) — il totale vero è nell'intestazione `X-WP-Total`, perché l'abilità
    `content/list-posts` risponde `total: null`;
  * la **promessa** (titolo SEO + description) dall'abilità `seo/get-post-seo`;
  * la **parola chiave** dal postmeta, con la chiave che si ricava dal namespace delle abilità
    (`_<prefisso>_seo_focus_keyword`) — `get-post-seo` **non** la restituisce.

Uso:
    python3 inventario.py                    # riscrive <cartella di lavoro>/shared/INVENTARIO.md
    python3 inventario.py --out /tmp/prova.md --limite 5     # prova rapida

Tutto passa da `curl`: Cloudflare blocca i client Python con l'errore 1010. Solo libreria
standard, nessun venv. Non stampa mai le credenziali.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import subprocess
import sys

HOME = pathlib.Path.home()
ENV = HOME / ".hermes" / ".env"


def impostazione(nome: str, ripiego: str = "") -> str:
    """Prima l'ambiente, poi `~/.hermes/.env`, poi il ripiego (come `stato-sito.py`)."""
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
SEC = pathlib.Path(impostazione("WP_CREDENTIALS", str(HOME / ".hermes" / "secrets" / "wp-credentials.env")))
DOMINIO = impostazione("SITE_DOMAIN", "il-tuo-sito.it")
SITO = f"https://{DOMINIO}"
MCP = impostazione("SITE_MCP_URL", f"{SITO}/wp-json/mcp/mcp-adapter-default-server")


def leggi_segreti() -> dict:
    valori = {}
    try:
        for riga in SEC.read_text().splitlines():
            if "=" in riga and not riga.lstrip().startswith("#"):
                k, v = riga.split("=", 1)
                valori[k.strip()] = v.strip()
    except OSError:
        pass
    return valori


def per_suffisso(segreti: dict, suffisso: str) -> str:
    """Il valore della prima chiave che **finisce** così: i nomi cambiano da installazione a
    installazione (`WP_USER`, `<SITO>_WP_USER`…), e cercarli per nome intero fa fallire lo
    script dove basterebbe riconoscerli."""
    for k, v in segreti.items():
        if k.upper().endswith(suffisso):
            return v
    return ""


def curl(args: list[str]) -> tuple[int, str, dict]:
    r = subprocess.run(["curl", "-s", "-D", "/tmp/inventario-hdr.txt", "-w", "\n%{http_code}"] + args,
                       capture_output=True, text=True)
    fuori = r.stdout.rsplit("\n", 1)
    corpo = fuori[0] if len(fuori) == 2 else r.stdout
    stato = int(fuori[1]) if len(fuori) == 2 and fuori[1].strip().isdigit() else 0
    intestazioni = {}
    for riga in pathlib.Path("/tmp/inventario-hdr.txt").read_text().splitlines():
        if ":" in riga:
            k, v = riga.split(":", 1)
            intestazioni[k.strip().lower()] = v.strip()
    return stato, corpo, intestazioni


_SESSIONE: dict = {}
_ELENCO: dict = {}


def _apri_sessione(segreti: dict) -> list:
    """La sessione MCP si apre una volta e si riusa. **`MCP-Protocol-Version` è obbligatorio**
    su ogni chiamata dopo l'`initialize`: senza, il server risponde 400 e sembra un problema di
    credenziali (trappola documentata in `references/trappole.md`)."""
    if _SESSIONE.get("comuni"):
        return _SESSIONE["comuni"]
    utente, password = per_suffisso(segreti, "_USER"), per_suffisso(segreti, "APP_PASSWORD")
    comuni = ["-u", f"{utente}:{password}",
              "-H", "Content-Type: application/json",
              "-H", "Accept: application/json, text/event-stream"]
    _, _, hdr = curl(comuni + ["-X", "POST", MCP, "-d", json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                   "clientInfo": {"name": "inventario", "version": "1.0"}}})])
    sid = hdr.get("mcp-session-id", "")
    if sid:
        comuni += ["-H", f"Mcp-Session-Id: {sid}", "-H", "MCP-Protocol-Version: 2025-06-18"]
        curl(comuni + ["-X", "POST", MCP, "-d", json.dumps({"jsonrpc": "2.0",
                                                             "method": "notifications/initialized"})])
    _SESSIONE["comuni"] = comuni
    return comuni


def _testo(d: dict) -> str:
    return ((d.get("result") or {}).get("content") or [{}])[0].get("text", "")


def _chiama(segreti: dict, strumento: str, argomenti: dict, id_: int = 2) -> dict:
    comuni = _apri_sessione(segreti)
    _, corpo, _ = curl(comuni + ["-X", "POST", MCP, "-d", json.dumps({
        "jsonrpc": "2.0", "id": id_, "method": "tools/call",
        "params": {"name": strumento, "arguments": argomenti}})])
    for riga in corpo.splitlines():
        riga = riga[5:].strip() if riga.startswith("data:") else riga.strip()
        if riga.startswith("{"):
            try:
                return json.loads(riga)
            except json.JSONDecodeError:
                continue
    return {}


def _elenco(segreti: dict) -> dict:
    if not _ELENCO:
        try:
            voci = (json.loads(_testo(_chiama(segreti, "mcp-adapter-discover-abilities", {}))) or {}).get("abilities") or []
        except Exception:  # noqa: BLE001
            voci = []
        _ELENCO.update({v["name"]: v for v in voci if isinstance(v, dict) and v.get("name")})
    return _ELENCO


def _risolvi(segreti: dict, nome: str) -> str:
    """`seo/get-post-seo` -> `madweb-seo/get-post-seo`: il namespace è **generico** nel testo
    della skill e cambia da installazione a installazione. Quando il nome corto esiste in più
    namespace non si indovina (vedi `stato-sito.py`), si restituisce com'era."""
    elenco = _elenco(segreti)
    if nome in elenco or not elenco:
        return nome
    corto = nome.split("/", 1)[-1]
    candidati = sorted(n for n in elenco if n.endswith("/" + corto))
    if len(candidati) == 1:
        return candidati[0]
    generico = nome.split("/", 1)[0].lower()
    con_generico = [n for n in candidati if generico in n.split("/")[0].lower()]
    if len(con_generico) == 1:
        return con_generico[0]
    return nome


def abilita(segreti: dict, nome: str, parametri: dict | None = None):
    d = _chiama(segreti, "mcp-adapter-execute-ability",
                {"ability_name": _risolvi(segreti, nome), "parameters": parametri or {}})
    if not d:
        return {}
    if (d.get("result") or {}).get("isError"):
        return {}
    try:
        return json.loads(_testo(d))
    except Exception:  # noqa: BLE001
        return {}


def chiave_keyword(segreti: dict) -> str:
    """`_<prefisso>_seo_focus_keyword`, col prefisso letto dal namespace delle abilità.

    Nel testo della skill il campo è scritto col nome generico (`_sito_seo_focus_keyword`): qui il
    prefisso si **scopre** (`madweb-seo/get-post-seo` -> `madweb`), perché interrogare il nome
    generico risponde `{"meta": []}` e fa concludere «manca» su un campo che c'è.
    """
    risolto = _risolvi(segreti, "seo/get-post-seo")
    prefisso = risolto.split("/", 1)[0].replace("-seo", "")
    return f"_{prefisso}_seo_focus_keyword"


def categorie(segreti: dict) -> dict:
    """Id -> nome delle categorie: nel file si legge il **nome**, non `2` o `5`."""
    utente, password = per_suffisso(segreti, "_USER"), per_suffisso(segreti, "APP_PASSWORD")
    stato, corpo, _ = curl(["-u", f"{utente}:{password}",
                            f"{SITO}/wp-json/wp/v2/categories?per_page=100&_fields=id,name"])
    try:
        return {c["id"]: c["name"] for c in json.loads(corpo)}
    except Exception:  # noqa: BLE001
        return {}


def elenco_rest(segreti: dict, tipo: str, stato: str, limite: int = 0) -> tuple[int, list]:
    """Gli elementi di un tipo (`posts`/`pages`) in un certo stato, e il totale vero.

    Il totale si legge da `X-WP-Total` e **non** dagli elementi restituiti: `per_page` taglia.
    """
    utente, password = per_suffisso(segreti, "_USER"), per_suffisso(segreti, "APP_PASSWORD")
    elementi, pagina, totale = [], 1, 0
    while True:
        url = (f"{SITO}/wp-json/wp/v2/{tipo}?per_page=100&page={pagina}&status={stato}"
               f"&context=edit&_fields=id,status,slug,title,link,categories")
        stato_http, corpo, hdr = curl(["-u", f"{utente}:{password}", url])
        if pagina == 1:
            totale = int(hdr.get("x-wp-total", 0) or 0)
        if stato_http != 200:
            break
        try:
            blocco = json.loads(corpo)
        except json.JSONDecodeError:
            break
        if not blocco:
            break
        elementi += blocco
        if limite and len(elementi) >= limite:
            break
        if pagina >= int(hdr.get("x-wp-totalpages", 1) or 1):
            break
        pagina += 1
    return totale, elementi


def riga_markdown(segreti: dict, e: dict, chiave_kw: str, con_keyword: bool, cat: dict | None = None) -> str:
    pid = e.get("id")
    titolo = (e.get("title") or {}).get("rendered", "") if isinstance(e.get("title"), dict) else str(e.get("title", ""))
    titolo = re.sub(r"\s+", " ", titolo).replace("|", "\\|").strip()
    seo = abilita(segreti, "seo/get-post-seo", {"post_id": pid}) or {}
    dati = seo.get("data", seo) or {}
    seo_title = re.sub(r"\s+", " ", str(dati.get("seo_title") or "")).replace("|", "\\|").strip()
    promessa = re.sub(r"\s+", " ", str(dati.get("seo_description") or "")).replace("|", "\\|").strip()
    kw = ""
    if con_keyword:
        m = abilita(segreti, "meta/get-post-meta", {"post_id": pid, "keys": [chiave_kw]}) or {}
        voci = ((m.get("data") or {}).get("meta") or {}).get(chiave_kw) or []
        kw = (voci[0] if voci else "")
    cats = e.get("categories") or []
    nome_cat = (cat or {}).get(cats[0], str(cats[0])) if cats else ""
    return (f"| {pid} | {e.get('status','')} | {nome_cat} | {titolo} | "
            f"{seo_title} | {promessa} | `{e.get('slug','')}` | {kw} |")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(LAVORO / "shared" / "INVENTARIO.md"))
    ap.add_argument("--limite", type=int, default=0, help="per una prova rapida")
    ap.add_argument("--senza-keyword", action="store_true", help="salta la lettura del postmeta (metà delle chiamate)")
    args = ap.parse_args()

    segreti = leggi_segreti()
    if not SEC.exists():
        print(f"Credenziali non trovate: manca {SEC}. Senza, non si legge niente: si consegnano fuori chat.")
        return 1

    chiave_kw = chiave_keyword(segreti)
    cat = categorie(segreti)
    print(f"Sito: {SITO}\nCampo della parola chiave: {chiave_kw}\nCategorie: {cat}")

    elenchi = {}
    for tipo, stato, etichetta in (("posts", "publish", "pubblicati"), ("posts", "draft", "bozze"),
                                   ("posts", "future", "programmati"), ("posts", "trash", "cestinati"),
                                   ("pages", "publish", "pagine")):
        chiave = f"{tipo}:{stato}"
        totale, elementi = elenco_rest(segreti, tipo, stato, args.limite)
        elenchi[chiave] = (totale, elementi)
        print(f"  {etichetta:12} {totale:4}  ({len(elementi)} letti)")

    oggi = dt.date.today().strftime("%d/%m/%Y")
    righe = [
        "# Inventario dei contenuti",
        "",
        f"**Rigenerato il {oggi} leggendo il sito** (REST `X-WP-Total` + `seo/get-post-seo`). "
        f"**{elenchi['posts:publish'][0]} pubblicati**, **{elenchi['posts:draft'][0]} bozze**, "
        f"{elenchi['posts:future'][0]} programmati, {elenchi['posts:trash'][0]} nel cestino, "
        f"{elenchi['pages:publish'][0]} pagine.",
        "",
        "**Questo file invecchia da solo: si rigenera con `scripts/inventario.py` prima di ogni "
        "confronto**, non si cita a memoria. Un inventario vecchio dice «libera» a una promessa "
        "già coperta (`references/pianificazione-e-duplicati.md` §2).",
        "",
        "| id | stato | categoria | titolo nativo | titolo SEO | promessa (description SEO) | slug | parola chiave |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for etichetta, chiave in (("Pubblicati", "posts:publish"), ("Bozze", "posts:draft"),
                              ("Programmati", "posts:future"), ("Cestinati", "posts:trash"),
                              ("Pagine", "pages:publish")):
        totale, elementi = elenchi[chiave]
        if not elementi and chiave in ("posts:future", "posts:trash"):
            continue
        righe += ["", f"## {etichetta} ({totale})", ""]
        for e in elementi:
            righe.append(riga_markdown(segreti, e, chiave_kw, not args.senza_keyword, cat))

    fuori = pathlib.Path(args.out)
    fuori.parent.mkdir(parents=True, exist_ok=True)
    fuori.write_text("\n".join(righe) + "\n")
    print(f"\nscritto {fuori} ({len(righe)} righe)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
