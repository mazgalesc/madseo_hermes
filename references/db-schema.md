# SQLite Content Calendar Schema

This document outlines the expected schema for the SQLite database used by l'autore SEO Manager to track the content lifecycle (`./shared/lavoro.db`).

## Table: `content_calendar`

The `content_calendar` table stores all planned, drafted, and published content across the entire pipeline.

### Schema Definition

**Questo è lo schema completo: si legge da qui e si copia da qui.** Una installazione nuova crea la
tabella con questo blocco **una volta sola**, comprese le cinque colonne in fondo (`keyword_primaria`,
`intento`, `refresh_at`, `promessa`, `copre_gia`): sono le nostre, aggiunte il 01/10/2026 e l'11/10/2026
alla tabella dell'autore, e senza di esse il controllo dei duplicati non ha niente da confrontare. Su un
database che esiste già si aggiungono con `ALTER TABLE content_calendar ADD COLUMN …`, una per una.

```sql
CREATE TABLE content_calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    wp_category_id INTEGER,
    funnel_stage TEXT NOT NULL CHECK (funnel_stage IN ('TOFU', 'MOFU', 'BOFU')),
    status TEXT NOT NULL CHECK (status IN ('Idea', 'Draft', 'Review', 'Scheduled', 'Published', 'Repurposed')),
    scheduled_date DATE,
    wp_post_id INTEGER,
    published_url TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    article_title TEXT,
    article_slug TEXT,
    keyword_primaria TEXT,
    intento TEXT,
    refresh_at DATE,
    promessa TEXT,
    copre_gia TEXT
);
```

Note sul campo `article_slug` (aggiunto il 01/10/2026): contiene lo slug dell'articolo dopo la
creazione della bozza. Nella lettura delle ultime righe del database risultava **vuoto su tutte le righe
controllate**: prima di usarlo per confronti, verificarlo; l'identificativo che conta è `wp_post_id`.

## Colonne aggiunte il 01/10/2026 (nostre, non dell'autore)

| Colonna | Tipo | A cosa serve | Come si riempie |
|---|---|---|---|
| `keyword_primaria` | TEXT | la query principale della pagina — la stessa cosa che va in `_sito_seo_focus_keyword` | dalla colonna `query` del piano del 23/09, oppure quando si scrive o si verifica l'articolo |
| `intento` | TEXT | l'intento della voce (`informativo`, `problem solving`, `commerciale`, `transazionale`) | dalla colonna `intenzione` del piano — è la stessa da cui è derivato `funnel_stage` |
| `refresh_at` | DATE | quando la pagina va riguardata (§3-bis del `SKILL.md`) | per le pagine pubblicate = **data di pubblicazione + 3 mesi** |
| `promessa` | TEXT | la promessa che la pagina fa al lettore, in una riga (`pianificazione-e-duplicati.md` §3) | si ricava dal **titolo SEO + description + H2 vivi**; **non si inventa** |
| `copre_gia` | TEXT | l'id del contenuto con cui la voce è vicina | dalla mappa del cluster (`pianificazione-e-duplicati.md` §5) |

**Stato del riempimento al 01/10/2026:** `refresh_at` **37/67** (tutte le pubblicate, con la data vera
letta da WordPress), `keyword_primaria` e `intento` **28/67** — sono le righe che vengono dal piano del
23/09/2026, le uniche che hanno il dato scritto. Le altre restano vuote e si riempiono **man mano che si
lavora l'articolo**: non si inventano.

**`promessa` e `copre_gia` sono richieste dall'11/10/2026** (dall'audit dei contenuti: la cannibalizzazione
si evita confrontando le promesse, non i titoli). Al primo allestimento del database si creano insieme
alle altre; se la tabella esiste già si aggiungono con `ALTER TABLE content_calendar ADD COLUMN …`.

**Dove vive la keyword obiettivo.** Sta in `postmeta` (`_sito_seo_focus_keyword`) e **non è fra i campi
che l'API REST pubblica** (che espone solo `_sito_seo_faq`, `_sito_seo_howto` e `footnotes`): si legge
via MCP (`meta/get-post-meta`, `seo/get-post-seo`) o dall'editor di WordPress.

**I 401 annotati prima non sono una prova di blocco.** Un `401` misurato su questo sito può essere
l'artefatto della lettura sbagliata delle credenziali (i valori di `.env` e di `wp-credentials.env` non hanno
virgolette e **contengono spazi**: la trappola è in «Il 401 che non vuol dire “credenziali sbagliate”»,
`ricerca-webcmd.md`). **Riverificato con un parser vero:** con l'application password la collezione risponde
**200** — `posts?status=draft&per_page=1&context=edit`, `media?per_page=1&context=edit`, `users/me` — e
l'endpoint MCP col valore reale di `WP_BASIC_AUTH` risponde **405** (credenziali accettate, metodo
sbagliato per l'handshake), non `401`. Quindi **prima di dichiarare bloccata una rotta si ripete la prova
con le credenziali rilette da un parser**, chiedendosi se quel `401` viene dal sito o dal valore troncato.

### Note di esercizio (verificate il 12/10/2026)

- **Il database può risultare «locked»** se una chiamata interrotta lascia aperta una connessione: l'errore
  è `database is locked` e non c'entra il sito né il file. Si chiudono le connessioni rimaste aperte (o si
  riparte con un processo nuovo) e si riprova. **Non si cancellano file per sbloccarlo**: uno script che
  cancella file chiede un consenso che può non arrivare, e il lock non si risolve così.
- **I valori in uso**: `status` = `Scheduled` (voce da scrivere), `Draft` (scritta, caricata come bozza su
  WordPress), `Published`. `funnel_stage` = `TOFU` | `MOFU` | `BOFU` — il database **rifiuta** altro: un
  valore fuori lista fa fallire l'intero inserimento con `CHECK constraint failed`. Il funnel si **deriva
  dall'`intento`**, non si sceglie a parte.
- **Ogni voce del piano porta la sua data**: due articoli a settimana, **martedì e venerdì**, con la
  rotazione per categoria (WordPress → Affiliazione → Guide AI → Strumenti AI). Le date sono **slot**: se il
  materiale non è pronto slittano, e si aggiornano nel database (il calendario leggibile le stampa).
- **I contenuti gi\u00e0 pubblicati non stanno qui**: stanno in `INVENTARIO.md`. La tabella tiene la **coda**
  (voci da scrivere/rifare) e le **bozze** gi\u00e0 scritte.

### Required Agent Operations

#### 1. Inserting New Ideas (Via `plan_strategy`)
When planning content, the agent should insert records with status `Idea` and the correct category ID.
```sql
INSERT INTO content_calendar (title, wp_category_id, funnel_stage, status, scheduled_date)
VALUES ('Title', 10, 'TOFU', 'Idea', '2026-05-01');
```

#### 2. Updating Status (Via WordPress Integration)
When a post is created as a draft on WordPress, store the `wp_post_id`.
```sql
UPDATE content_calendar 
SET status = 'Draft', wp_post_id = [WP_ID], updated_at = CURRENT_TIMESTAMP 
WHERE id = [ID];
```

#### 3. Reviewing the Calendar
The agent can query this database at any time to review what needs to be drafted next or what gaps exist in the funnel.
