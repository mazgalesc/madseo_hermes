#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
controlla-articolo.py — i controlli incrociati di references/controlli-verifica.md, in forma di lista.

COSA FA: legge un contenuto (JSON del plugin/MCP, HTML salvato o pagina resa, testo semplice) e stampa
i PUNTI DA VERIFICARE A MANO: i numeri annunciati contro il numero di voci degli elenchi vicini, le
uguaglianze aritmetiche, gli artefatti di produzione rimasti nel testo, i testi alternativi delle
immagini, i link interni con l'etichetta, le ripetizioni a mezza frase, le intestazioni vuote.

COSA NON FA: non dà verdetti. Nessun controllo automatico misura se un articolo è giusto: questo
strumento dice DOVE guardare. Il giudizio resta la lettura.

USO
    python3 controlla-articolo.py <file>
        <file> = .json (risposta di content/get-post: usa il campo `content`)
                 .html (contenuto Gutenberg salvato, o pagina pubblica)
                 .md/.txt (testo: restano solo i controlli che non richiedono la struttura)

    python3 controlla-articolo.py --testo            # legge il contenuto da stdin

OPZIONI
    --json     stampa i risultati in JSON (per script successivi)
    --parole   stampa solo il conteggio parole

Nessuna dipendenza: solo libreria standard. Nessuna rete: non apre link, non interrogal sito.
"""

import json
import os
import re
import sys
import unicodedata
from collections import Counter

# ---------------------------------------------------------------- utilità

MESI = ("gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre dicembre").split()

def senza_markup(html: str) -> str:
    """Da HTML a testo leggibile: blocchi di codice esclusi, entità risolte, una riga per blocco."""
    t = re.sub(r"<(script|style|pre|code)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
    t = re.sub(r"</(p|li|tr|h[1-6]|blockquote|div|figure)>", "\n", t, flags=re.I)
    t = re.sub(r"<h([1-6])[^>]*>(.*?)</h\1>", lambda m: "\n" + "#" * int(m.group(1)) + " " + m.group(2) + "\n", t, flags=re.S | re.I)
    t = re.sub(r"<td[^>]*>|<th[^>]*>", " | ", t, flags=re.I)
    t = re.sub(r"<[^>]+>", "", t)
    for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&quot;", '"'), ("&#8217;", "'"),
                 ("&nbsp;", " "), ("&#8211;", "–"), ("&#8230;", "…")):
        t = t.replace(a, b)
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n{3,}", "\n\n", t).strip()

def maschera(html: str) -> str:
    """Testo leggibile a LUNGHEZZA IDENTICA all'HTML: ogni tag diventa tanti spazi quanti ne occupava.
    Serve perché le posizioni trovate nel testo si possano confrontare con le posizioni nell'HTML
    (elenchi, tabelle, intestazioni): con un testo accorciato i due spazi di coordinate non coincidono."""
    def spazi(m):
        return " " * len(m.group(0))
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", spazi, html, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", spazi, t)
    return t


def parole(testo: str) -> list:
    return re.findall(r"[\w\u00c0-\u00ff'’]+", testo, re.UNICODE)

def riga_intorno(testo: str, pos: int, ampiezza: int = 120) -> str:
    a = max(0, pos - ampiezza // 2)
    return " ".join(testo[a:pos + ampiezza].split())

NUMERI_PAROLA = {"un": 1, "uno": 1, "una": 1, "due": 2, "tre": 3, "quattro": 4, "cinque": 5, "sei": 6,
                 "sette": 7, "otto": 8, "nove": 9, "dieci": 10, "undici": 11, "dodici": 12,
                 "quindici": 15, "venti": 20}

# ------------------------------------------------------------------ controlli

def numeri_annunciati(testo: str, blocchi: list, sezioni: int = 0) -> list:
    """Numeri annunciati ('i 10 errori', 'tre cose', 'la tabella elenca 6') contro le voci vicine.
    Per ogni annuncio si stampano DUE numeri da confrontare a mano: le voci dell'elenco o della tabella
    più vicina, e il numero di sezioni H2 del documento (è il caso 'tre punti' con sette sezioni)."""
    esiti = []
    n = "|".join(NUMERI_PAROLA)
    nome = r"(?:punti|errori|cose|controlli|passi|modi|motivi|regole|criteri|strumenti|domande|esempi|voci|consigli|sezioni|capitoli|trappole|segnali|fasi|livelli|tipi|problemi)"
    schemi = [rf"\b(?P<num>\d+|{n})\s+{nome}\b", rf"\b(?:i|le|gli)\s+(?P<num>\d+)\b",
              rf"tabella[^.\n]{{0,30}}elenca\s+(?P<num>\d+)", rf"qui sotto[^.\n]{{0,20}}(?P<num>\d+)"]
    for schema in schemi:
        for m in re.finditer(schema, testo, re.I):
            grezzo = m.group("num").lower()
            valore = int(grezzo) if grezzo.isdigit() else NUMERI_PAROLA.get(grezzo)
            if not valore or valore > 40:
                continue
            # l'elenco o la tabella più vicina DOPO l'annuncio
            dopo = [b for b in blocchi if b["inizio"] > m.end()]
            vicino = dopo[0] if dopo and dopo[0]["inizio"] - m.end() <= 2500 else None
            esiti.append({"annuncio": f"{valore}", "testo": riga_intorno(testo, m.start()),
                          "voci_vicine": vicino["voci"] if vicino else 0,
                          "tipo": vicino["tipo"] if vicino else "nessun elenco o tabella vicino",
                          "sezioni": sezioni,
                          "coincide": (valore == vicino["voci"]) if vicino else None})
    # dedup per annuncio+conteggio
    visti, unici = set(), []
    for e in esiti:
        k = (e["annuncio"], e["voci_vicine"], e["testo"][:40])
        if k not in visti:
            visti.add(k); unici.append(e)
    return unici

def aritmetica(testo: str) -> list:
    """Righe con più numeri e un segno di calcolo o un uguale: da rifare a mano."""
    fuori = []
    for r in testo.split("\n"):
        if len(re.findall(r"\d", r)) < 3:
            continue
        if re.search(r"[=×x*]|\bper cento\b", r) and re.search(r"\d", r):
            if re.search(r"(=|×|\d\s*[x*]\s*\d|\d\s*%\s*[x*]|\d\s*[x*]\s*\d\s*%)", r):
                fuori.append(" ".join(r.split())[:300])
    return fuori

ARTEFATTI = [
    (r"PT\d+[HMS]\b", "durata ISO dello schema stampata a video"),
    (r"\bu/[A-Za-z0-9_-]{2,}", "nota di fonte Reddit (utente) rimasta nel testo"),
    (r"\br/[A-Za-z0-9_-]{2,}", "nota di fonte Reddit (subreddit) rimasta nel testo"),
    (r"\bla\s\d{2,}\sstessa\b", "ID del post rimasto nel testo"),
    (r"&lt;|<p>|</p>|<br\s*/?>|<span>", "HTML escapato o stampato a video"),
    (r"`", "backtick di markdown non convertito"),
    (r"\*\*", "markdown non convertito (grassetto)"),
    (r"Risposta diretta:|Risposta rapida:", "etichetta di layout rimasta visibile"),
    (r"Updated on|Table of contents|which is better", "inglese rimasto in produzione"),
    (r"\?\?", "bandierina o carattere perso"),
    (r"\bSERP\b|\bquery\b|in prima pagina|posizione\s\d", "linguaggio da analisi di ricerca"),
    (r"post_id|pagePath|focus_keyword", "nome tecnico di campo rimasto nel testo"),
    (r"\[RIQUADRO\]|\[CITAZIONE\]|\[IMMAGINE\]|\[CODICE\]", "marcatore di blocco non risolto"),
    (r"\btuosit[oa]\.it\b", "dominio di esempio non sostituito"),
]

def artefatti(testo: str) -> list:
    fuori = []
    for schema, che in ARTEFATTI:
        for m in re.finditer(schema, testo):
            fuori.append({"cosa": che, "trovato": m.group(0)[:40], "contesto": riga_intorno(testo, m.start())})
    return fuori

def entita_escapate(grezzo: str) -> list:
    """`&lt;p&gt;` nel contenuto salvato significa che il lettore vede `<p>` in pagina (caso 1529).
    Script e style si escludono: lì le entità sono normali e non arrivano mai all'occhio."""
    senza_script = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", grezzo, flags=re.S | re.I)
    fuori, visti = [], set()
    for m in re.finditer(r"&lt;\s*/?\s*([a-zA-Z][a-zA-Z0-9]*)\s*&gt;", senza_script):
        tag = m.group(1).lower()
        if tag in visti:
            continue
        visti.add(tag)
        fuori.append({"trovato": m.group(0)[:30], "contesto": ""})
    return fuori[:12]


def immagini(html: str) -> dict:
    """Tutte le <img>: quante, e per ognuna src, alt (o mancante, o vuoto)."""
    fuori, alt_visti = [], Counter()
    for m in re.finditer(r"<img\b[^>]*>", html, re.I):
        tag = m.group(0)
        src = re.search(r'src=["\']([^"\']*)', tag, re.I)
        alt = re.search(r'\balt=["\']([^"\']*)', tag, re.I)
        nome = os.path.basename(src.group(1).split("?")[0]) if src else "(senza src)"
        if not alt:
            stato = "ALTERNATIVO ASSENTE"
        elif not alt.group(1).strip():
            stato = "ALTERNATIVO VUOTO"
        else:
            stato = alt.group(1)
            alt_visti[stato] += 1
        fuori.append({"file": nome, "alt": stato})
    duplicati = [a for a, c in alt_visti.items() if c > 1]
    return {"totale": len(fuori), "immagini": fuori, "alternativi_duplicati": duplicati}

def link_interni(html: str) -> list:
    """Ancore che puntano dentro il sito: l'etichetta si confronta a mano con la destinazione."""
    fuori = []
    for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html, re.I | re.S):
        href, etichetta = m.group(1), senza_markup(m.group(2))[:70]
        DOMINIO = os.environ.get("SITE_DOMAIN", "")
        if href.startswith(("http://", "https://")) and (DOMINIO not in href if DOMINIO else True):
            continue
        rel = re.search(r'rel=["\']([^"\']*)', m.group(0), re.I)
        fuori.append({"etichetta": etichetta, "destinazione": href,
                      "rel": (rel.group(1) if rel else "")})
    return fuori

def ripetizioni(testo: str, finestra: int = 9, minimo: int = 2) -> list:
    """Ripetizioni a MEZZA FRASE: confronta finestre di parole, non frasi intere (il contatore
    a frase intera non le vede)."""
    p = [w.lower() for w in parole(testo)]
    if len(p) < finestra * 2:
        return []
    visti = Counter()
    for i in range(len(p) - finestra):
        visti[" ".join(p[i:i + finestra])] += 1
    cand = [(frase, c) for frase, c in visti.most_common(600)
            if c >= minimo and not re.match(r"^(\d+ )+$", frase) and len(set(frase.split())) > 4]
    # finestre sovrapposte = stessa ripetizione: si tiene la più lunga (le parole in più sono il contesto)
    fuori = []
    for frase, c in cand:
        chiave = set(frase.split())
        if any(chiave & set(g["testo"].split()) and
               (len(chiave & set(g["testo"].split())) / max(len(chiave), len(set(g["testo"].split())))) > 0.6
               for g in fuori):
            continue
        fuori.append({"ripetuta": c, "testo": frase})
        if len(fuori) >= 10:
            break
    return fuori

def intestazioni_vuote(html: str) -> list:
    """H2/H3 che non hanno nulla sotto prima dell'intestazione successiva (blocco finito altrove)."""
    fuori = []
    h = list(re.finditer(r"<h([2-3])[^>]*>(.*?)</h\1>(.*?)(?=<h[1-6][^>]*>|$)", html, re.I | re.S))
    for i, m in enumerate(h):
        corpo = senza_markup(m.group(3))
        if len(parole(corpo)) < 12:
            fuori.append({"titolo": senza_markup(m.group(2))[:80], "parole_sotto": len(parole(corpo))})
    return fuori

def blocchi_struttura(html: str) -> list:
    """Elenchi e tabelle con il loro numero di voci, e dove cominciano."""
    fuori = []
    for m in re.finditer(r"<(ul|ol)\b[^>]*>(.*?)</\1>", html, re.I | re.S):
        fuori.append({"tipo": m.group(1).lower(), "voci": len(re.findall(r"<li\b", m.group(2), re.I)),
                      "inizio": m.start()})
    for m in re.finditer(r"<table\b[^>]*>(.*?)</table>", html, re.I | re.S):
        righe = len(re.findall(r"<tr\b", m.group(1), re.I))
        fuori.append({"tipo": "tabella", "voci": max(righe - 1, 0), "inizio": m.start()})
    return sorted(fuori, key=lambda b: b["inizio"])

# -------------------------------------------------------------------- main

def analizza(grezzo: str, nome: str, struttura: bool) -> dict:
    testo = senza_markup(grezzo) if struttura else grezzo
    testo_pos = maschera(grezzo) if struttura else grezzo   # posizioni allineate all'HTML
    out = {
        "file": nome,
        "parole": len(parole(testo)),
        "numeri_annunciati": (numeri_annunciati(testo_pos, blocchi_struttura(grezzo), len(re.findall(r"<h2\b", grezzo, re.I)))
                               if struttura else []),
        "aritmetica": aritmetica(testo_pos),
        "artefatti": artefatti(testo),
        "immagini": immagini(grezzo) if struttura else {"totale": 0, "immagini": [], "alternativi_duplicati": []},
        "link_interni": link_interni(grezzo) if struttura else [],
        "ripetizioni": ripetizioni(testo),
        "intestazioni_vuote": intestazioni_vuote(grezzo) if struttura else [],
        "entita_escapate": entita_escapate(grezzo) if struttura else [],
    }
    return out

def stampa(r: dict):
    print(f"\n=== {r['file']} — {r['parole']} parole ===")
    if not r["numeri_annunciati"] and not r["aritmetica"] and not r["artefatti"] and not r["immagini"]["totale"]:
        print("   (niente struttura HTML: restano i controlli su testo, artefatti e ripetizioni)")

    print(f"\n-- 1. Numeri annunciati contro le voci vicine ({len(r['numeri_annunciati'])}) --")
    for e in r["numeri_annunciati"]:
        segno = "✅ coincide" if e["coincide"] else ("⚠️ DA VERIFICARE" if e["coincide"] is False else "·  da leggere")
        print(f"   {segno} — annuncia {e['annuncio']}; {e['tipo']}: {e['voci_vicine']} voci; sezioni H2 nel documento: {e['sezioni']}")
        print(f"        …{e['testo'][:150]}…")

    print(f"\n-- 2. Aritmetica da rifare a mano ({len(r['aritmetica'])}) --")
    for riga in r["aritmetica"][:12]:
        print(f"   ⚠️ {riga}")

    print(f"\n-- 3. Artefatti di produzione nel testo ({len(r['artefatti'])}) --")
    for a in r["artefatti"][:25]:
        print(f"   ⚠️ {a['cosa']}: «{a['trovato']}»")
        print(f"        …{a['contesto'][:150]}…")

    img = r["immagini"]
    print(f"\n-- 4. Immagini ({img['totale']}) --")
    for i in img["immagini"]:
        stato = i["alt"]
        segno = "❌" if "ASSENTE" in stato or "VUOTO" in stato else "   "
        print(f"   {segno} {i['file'][:52]:52} alt: {stato[:70]}")
    for d in img["alternativi_duplicati"]:
        print(f"   ⚠️ alternativo ripetuto su più immagini: «{d[:80]}»")

    if r["link_interni"]:
        print(f"\n-- 5. Link interni: etichetta e destinazione ({len(r['link_interni'])}) — leggere a mano --")
        for l in r["link_interni"]:
            print(f"      «{l['etichetta']}» → {l['destinazione']}{'  [' + l['rel'] + ']' if l['rel'] else ''}")

    print(f"\n-- 6. Ripetizioni a mezza frase ({len(r['ripetizioni'])}) --")
    for x in r["ripetizioni"]:
        print(f"   ⚠️ ×{x['ripetuta']}  {x['testo'][:130]}")

    if r["entita_escapate"]:
        print(f"\n-- 7-bis. HTML escapato nel contenuto ({len(r['entita_escapate'])}) — il lettore lo vede in pagina --")
        for x in r["entita_escapate"][:6]:
            print(f"   ⚠️ {x['trovato']}")

    if r["intestazioni_vuote"]:
        print(f"\n-- 7. Intestazioni senza corpo sotto ({len(r['intestazioni_vuote'])}) --")
        for h in r["intestazioni_vuote"]:
            print(f"   ⚠️ «{h['titolo']}» — {h['parole_sotto']} parole sotto")

    print("\nPromemoria: questi sono INDIZI, non verdetti. Il conteggio delle parole non dice se l'articolo")
    print("è buono, e nessuno di questi controlli sostituisce la lettura.")

def main():
    argomenti = [a for a in sys.argv[1:] if not a.startswith("--")]
    opzioni = {a for a in sys.argv[1:] if a.startswith("--")}
    if not argomenti and "--testo" not in opzioni:
        print(__doc__)
        return 1
    grezzo, nome, struttura = "", "(stdin)", False
    if argomenti:
        percorso = argomenti[0]
        if not os.path.exists(percorso):
            print(f"file non trovato: {percorso}")
            return 1
        grezzo = open(percorso, encoding="utf-8", errors="replace").read()
        nome = os.path.basename(percorso)
        if percorso.endswith(".json"):
            try:
                dati = json.loads(grezzo)
                grezzo = dati.get("content") or dati.get("data", {}).get("content") or ""
                nome += " (campo content)"
            except Exception:
                pass
        struttura = bool(re.search(r"<(p|h[1-6]|ul|ol|table|figure)\b", grezzo, re.I))
    else:
        grezzo = sys.stdin.read()
        struttura = bool(re.search(r"<(p|h[1-6]|ul|ol|table|figure)\b", grezzo, re.I))
    r = analizza(grezzo, nome, struttura)
    if "--parole" in opzioni:
        print(f"{r['parole']} parole — {r['file']}")
        return 0
    if "--json" in opzioni:
        print(json.dumps(r, ensure_ascii=False, indent=1)); return 0
    stampa(r)
    return 0

if __name__ == "__main__":
    sys.exit(main())
