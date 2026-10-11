#!/usr/bin/env python3
"""Genera il calendario leggibile in ~/seo-content/shared/CALENDARIO.md

Dal 29/09/2026 la coda operativa è il piano dell'agenda: gli 80 titoli di
PIANO-ARTICOLI-2026-09-23.md, in ordine di rotazione (1 articolo per categoria
per ciclo: WordPress, Affiliazione, Guide AI, Strumenti AI), senza date finché
l'ordine lo decide la disponibilità del materiale.

Struttura del database (dal 29/09/2026):
- `title` = il titolo **del piano** (da dove viene la voce)
- `article_title` / `article_slug` = il titolo e lo slug **dell'articolo scritto**, letti da WordPress
- `status`: Scheduled (in coda) → Draft (scritto, in bozza su WordPress) → Published
"""
import pathlib
import os
import sqlite3

home = pathlib.Path.home()
lavoro = pathlib.Path(os.environ.get("SEO_WORK_DIR", str(home / "seo-content")))
db = lavoro / "shared" / "lavoro.db"
conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row
CAT = {3: "WordPress", 5: "Affiliazione", 2: "Guide AI", 4: "Strumenti AI", 1: "Sito"}

righe = [f"# Calendario editoriale — {os.environ.get('SITE_DOMAIN', 'il-tuo-sito.it')}", "",
         "Coda operativa: **le voci del piano in `audits/`** (il documento più recente), in ordine di",
         "rotazione — **1 articolo per categoria per ciclo** (WordPress, Affiliazione, Guide AI, Strumenti AI).",
         "**Date assegnate**: due a settimana, martedì e venerdì; slittano se il materiale non è pronto.",
         "Le voci con **Draft** sono già scritte e aspettano la revisione; quelle **Scheduled** sono da scrivere.",
         "Lo stadio di funnel è **derivato dalla colonna «intenzione»** del piano (informativo TOFU,",
         "problem solving/commerciale MOFU, transazionale BOFU): non è una scelta editoriale a parte.",
         "", f"Stato del database (`{lavoro}/shared/lavoro.db`):"]
for stato, n in conn.execute("SELECT status, COUNT(*) c FROM content_calendar GROUP BY 1 ORDER BY c DESC"):
    righe.append(f"- **{stato}**: {n}")

# --- bozze scritte e in attesa di pubblicazione ---
righe += ["", "## Bozze in attesa di pubblicazione", "",
          "Scritte e caricate su WordPress come **bozza** (mai pubblicate). Il titolo è quello",
          "dell'articolo; fra parentesi il titolo della voce di piano, quando è diverso.", "",
          "| Data | Post | Categoria | Titolo dell'articolo | Voce di piano |", "|---|---|---|---|---|"]
for r in conn.execute("""SELECT wp_post_id, wp_category_id, article_title, article_slug, title, scheduled_date
                          FROM content_calendar
                         WHERE status = 'Draft' AND wp_post_id IS NOT NULL
                         ORDER BY scheduled_date, wp_post_id"""):
    titolo = r["article_title"] or r["title"]
    voce = "" if (r["article_title"] is None or r["article_title"].strip() == r["title"].strip()) else f"*{r['title']}*"
    righe.append(f"| {r['scheduled_date'] or '—'} | {r['wp_post_id']} | {CAT.get(r['wp_category_id'], '?')} | {titolo} | {voce} |")

# --- coda in rotazione ---
righe += ["", "## Coda in rotazione", "",
          "| Data | Stadio | Categoria | Titolo del piano |", "|---|---|---|---|"]
for i, r in enumerate(conn.execute("""SELECT funnel_stage, wp_category_id, title, scheduled_date
                                      FROM content_calendar
                                      WHERE status='Scheduled' ORDER BY scheduled_date, id"""), start=1):
    righe.append(f"| {r['scheduled_date'] or '—'} | {r['funnel_stage']} | {CAT.get(r['wp_category_id'], '?')} | {r['title']} |")

# --- altre bozze (famiglia vecchia, senza voce di piano) ---
altre = [r for r in conn.execute("""SELECT wp_post_id, wp_category_id, article_title, title
                                    FROM content_calendar
                                   WHERE status='Draft' AND wp_post_id IS NULL""")]
if altre:
    righe += ["", "## Altre bozze (famiglia precedente, non dalla coda nuova)", "",
              "| Categoria | Titolo |", "|---|---|"]
    for r in altre:
        righe.append(f"| {CAT.get(r['wp_category_id'], '?')} | {r['title']} |")


n_pub = conn.execute("SELECT COUNT(*) FROM content_calendar WHERE status='Published'").fetchone()[0]
righe += ["", f"## Articoli pubblicati ({n_pub})", "",
          "Qui ci sono solo le voci della **coda** (da scrivere) e le **bozze** già scritte: i contenuti",
          "già pubblicati stanno in `INVENTARIO.md`, rigenerato dal sito.", "",
          "## Controllo duplicati", "",
          "**Regola attiva**: prima di proporre o scrivere un titolo si confronta la **promessa** — non il",
          "titolo — con i pubblicati, le bozze e la coda. L'inventario è in `INVENTARIO.md`; il metodo in",
          "`references/pianificazione-e-duplicati.md`.", ""]

(lavoro / "shared" / "CALENDARIO.md").write_text("\n".join(righe))
print(f"  scritto CALENDARIO.md ({len(righe)} righe)")
conn.close()
