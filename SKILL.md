---
name: seo-content
description: Use when producing verifiable SEO content for a WordPress site (research, keywords, writing, audits, publishing).
version: 2.1.0
metadata:
  hermes:
    tags: [SEO, GEO, WordPress, content, immagini, italiano]
    related_skills: [scrapling, mnemosyne-memory-override]
prerequisites:
  commands: [curl, npm, webcmd]
---

# SEO CONTENT — versione Hermes

Porting di una versione precedente della skill (OpenClaw) (i 12 "tool" erano istruzioni per l'agente,
non codice). Qui diventano 13 procedure (dalla 0 alla 12), ricablate sugli strumenti di Hermes. I documenti di
conoscenza dell'autore sono in `references/`.

## ⛔ Il contenuto lo pubblica solo l'autore

**Mai cambiare lo stato di un contenuto.** Se una scrittura riporta `status: publish`, o se un articolo
risulta pubblicato mentre io lo credevo bozza, **non lo rimetto in bozza**: lo stato è una decisione di
dell'autore (il 19/09/2026 l'ho riportato in bozza una volta e lui stava solo guardando come veniva
l'articolo pubblicato). Se qualcosa non torna, **chiedere** e non toccare niente.

Nelle scritture di contenuto (`content/update-post`) il campo `status` va sempre passato in modo
esplicito quando si vuole restare in bozza, e subito dopo si rilegge con `content/get-post` per
confermarlo: un aggiornamento senza `status` può cambiarlo.

## ⛔ La regola che viene prima di tutto: SOLO BOZZE

- **Mai pubblicare.** Il massimo consentito è creare una **bozza** su WordPress.
- **Ogni scrittura in produzione** (metadati SEO, schema, redirect, link interni, impostazioni)
  richiede un **ok esplicito dell'autore per quella singola azione**. Senza ok: si prepara la modifica e
  la si mostra, non si applica.
- Tutto il resto è **sola lettura** e si può fare liberamente.
- Prima di qualunque scrittura: dire esattamente cosa cambia, su quale contenuto, e con quale payload.

## ⛔ Attivare o spegnere un plugin è una scrittura in produzione

Vale la regola generale (ok esplicito dell'autore **per quella singola azione**), più tre cautele che su un
sito vivo non si saltano:

- **Uno alla volta**, mai in blocco: se il sito si rompe, si sa quale plugin l'ha rotto.
- **Controllo di salute dopo ogni attivazione**: la home **più un articolo pubblicato vero**, con un
  parametro di cache-busting nell'URL. Una home che risponde 200 non basta: un plugin può rompere solo il
  singolo contenuto, o solo la resa.
- **Se il sito non risponde, si ripristina subito** lo stato precedente (`status` invertito) e si riferisce
  l'esito. Il ripristino è una scrittura come le altre, ma è l'unica che si esegue **senza aspettare**: è la
  rete di sicurezza di un guasto che si sta causando. Poi si indaga, non si insiste.

**Il numero di abilità MCP segue lo stato dei plugin**, quindi dopo un'attivazione si rimisura (non si
assume). Un plugin spento non toglie solo le sue abilità: può togliere un intero gruppo da quelle esposte.

## Configurazione: nomi generici, valori reali fuori dalla repo

Il testo usa **nomi generici** (`il-tuo-sito.it`, `sito`, `seo/*`, `tema`, `~/seo-content/`): valgono per
qualunque installazione. **I valori concreti non stanno qui**: si leggono dal file di configurazione locale
(`CONFIGURAZIONE.md` nella cartella di lavoro). La mappa dei nomi e le variabili d'ambiente che leggono gli
script sono in **`references/configurazione.md`**. Se il file locale non c'è, i nomi generici valgono come
esempio e vanno adattati prima di usare la skill.

## Gli script (tutti in `scripts/`, sola lettura tranne le bozze)

| Script | Cosa fa | Quando |
|---|---|---|
| `verifica-avvio.py` | il controllo d'avvio: cartella, database, credenziali (presenza e permessi, mai i valori), vault, MCP con entrambi gli header, sito, REST, Maton, Analytics | **procedura 0**, e ogni volta che qualcosa smette di funzionare |
| `controlla-articolo.py` | i controlli incrociati su un articolo o una bozza: numeri annunciati, aritmetica, artefatti, alt, link, ripetizioni | prima di consegnare una lettura |
| `stato-sito.py` | stato del sito in un colpo: SEO via MCP, query di Search Console, pagine di Analytics | quando serve il quadro d'insieme |
| `calendario.py` | genera `CALENDARIO.md` dal piano editoriale | dopo ogni modifica al database del piano |
| `genera-immagine.py`, `genera-infografica.py` | copertine e infografiche con la chiave immagini (**opzionale**) | solo se la chiave c'è; altrimenti si dichiara e si fa a mano |

## Dove stanno le cose

| Cosa | Dove |
|---|---|
| Cartella di lavoro | `~/seo-content/` — `content/` (bozze e immagini), `audits/` (analisi), `distribution/` (pillar→social), `shared/` (stato, calendario) |
| **Vault Obsidian** | percorso scelto dall'autore (esempio: `~/Documents/hermes`), dichiarato in `OBSIDIAN_VAULT_PATH` — **dove vivono le note dei contenuti, delle promesse e della ricerca**: `references/vault-obsidian.md` |
| Credenziali WordPress | `~/.hermes/secrets/wp-credentials.env` (600): `WP_USER`, `WP_APP_PASSWORD` |
| Chiavi in `.env` | `MATON_API_KEY` (Search Console, Analytics), `GOOGLE_API_KEY` (immagini), `BRAVE_SEARCH_API_KEY` / `EXA_API_KEY` / `TAVILY_API_KEY` (motori di `web_search`), `WP_BASIC_AUTH` (autenticazione dell'MCP) |
| Ambiente Python dedicato | `~/seo-content/.venv` — contiene `scrapling` 0.4.15 (con `playwright` 1.63.0), `google-genai` 2.24.0, `pillow`. **Mai installare pacchetti nel venv di Hermes**, con una sola eccezione: `ddgs` (lo mette lì la skill `duckduckgo-search`) |
| Server MCP | `sito` già configurato in Hermes → 3 strumenti: `mcp-adapter-discover-abilities`, `mcp-adapter-get-ability-info`, `mcp-adapter-execute-ability` |
| Sito | `https://il-tuo-sito.it` (WordPress multisite, plugin SEO = **plugin-seo**, non Rank Math / Yoast) |

## Mappa dei file — dove sta cosa

**L'elenco completo dei file di `references/`, con il peso e lo stato di ognuno, è in
`references/indice-file.md`** (35 file). Qui resta la regola: se cerchi una regola e non è in questo file,
è in uno di quelli; il metodo sta qui, i cataloghi stanno nei reference.

## Difetti noti del sito (verificati, da non riscoprire)

**1. `missing_alt` — corretto in `plugin-seo` 3.0.31 (19/09/2026); l'11/10/2026 la versione attiva è la 3.0.34** — si legge con `curl -u … 'https://il-tuo-sito.it/wp-json/wp/v2/plugins?context=edit'`, che dà nome e `version` (il tema a blocchi è nella stessa risposta) — **ma non fidarsi del suo `status`**: quella lista riporta lo stato **per-sito**, quindi su un multisite un plugin attivo a livello di **rete** lì compare `inactive`. Lo stato vero è sul singolo plugin, `…/wp/v2/plugins/<cartella>/<slug>` → `network-active`, ed è quello che si legge. **Mai dichiarare «disattivato per sbaglio» guardando solo la lista** (verificato il 13/10/2026: tre plugin riferiti come spenti erano attivi a livello di rete, e su quella lettura sbagliata è stato programmato un intervento inutile).
Il controllo era
`preg_match('/<img[^>]+(?!alt=)[^>]*>/i', …)`: il lookahead negativo viene valutato dopo che `[^>]+`
ha già consumato il tag, quindi combaciava con **qualsiasi** `<img>` — 31 contenuti segnalati a
fronte di 5 immagini davvero senza alt. Ora tutto passa da
`sito_seo_count_images_without_alt()` in `includes/common/helpers.php`, che esamina **ogni** tag
`<img>` (attributo assente o vuoto = mancante, `data-alt` non conta, ignora `>` dentro un attributo
quotato). Stessa funzione usata dal pannello e dall'elenco articoli, che prima contavano al
contrario (solo `alt=""`). Test: `php scripts/test-alt-check.php` (35 controlli).
Correzione giusta: `'/<img(?![^>]*\balt=)[^>]*>/i'`.

**Il conteggio si rifà, non si eredita.** Al **11/10/2026**, sui **45 articoli pubblicati** contati con
`scripts/controlla-articolo.py`: **134 immagini, 0 senza alt** (il caso del `585` è chiuso), più **2
immagini nelle 8 pagine**. Due avvertenze: lo script legge `alt` con **apici singoli e doppi** (un
controllo scritto a mano che accetta solo i doppi trova falsi «senza alt»), e il numero delle **pagine
renderizzate** (logo, avatar, template) è più alto e non confrontabile con quello del contenuto — il
19/09/2026 erano 168.

**2. Il link automatico del glossario riscrive anche dentro i tag.** In
`tema-blocks/inc/glossary/class-tema-compagnon-glossary-autolink.php` (righe 161-167) i
segmenti protetti sono link, script, style, pre/code e titoli: **manca la protezione dei tag
stessi**, quindi un termine del glossario che compare in un attributo (`src`, `alt`) viene
sostituito con `<a class="mw-glossary-term">` **dentro l'attributo**. Effetto: immagine rotta o alt
distrutto nella pagina pubblica. Il contenuto nel database resta integro: è un danno di resa.
Verificato il 19/09/2026 su 2 pagine (215: `src` rotto, immagine non visibile; 224: `alt` rotto).
**Corretto e verificato l'11/10/2026**: sui due contenuti i link del glossario non compaiono più dentro
`src`/`alt` (0 casi) e i termini evidenziati funzionano ancora (14 e 27). Il rischio resta se il plugin
viene aggiornato senza riportare la protezione dei tag.
Rischio alto: **66 file della libreria hanno un termine del glossario nel nome** (epc, backup,
hosting, cache, plugin, affiliazione, Gutenberg...). Correzione: aggiungere `'<[^>]+>'` all'array
`$protected` (in coda, dopo il pattern dei link). Quando è corretto, non serve toccare i contenuti.

**3. I difetti di SITO trovati nell'audit dell'11/10/2026 (45 articoli + 15 bozze) — si correggono UNA
volta, non su 45 pagine.** L'elenco completo con i casi e i numeri è in `~/seo-content/archivio/rapporto-difetti-audit.md`
e in `~/seo-content/archivio/correzioni_articoli/00-INDICE.md` (§1-98). Quelli che sono di sito, non di articolo:

- **`HowTo` nello schema di molti articoli del lotto di fine settembre** (verificato l'11/10/2026: presente
  in `1952`, `1967`, `204`; **assente** in `1854` e `1883`): funzionalità ritirata da Google nel 2023 (e il
  sito lo spiega da sé nel `1529`). Da togliere **dove c'è, uno per uno** — non «su tutti»: il tipo
  principale va uniformato su **`BlogPosting`** (all'11/10/2026 usano ancora `Article` il `1854` e il `1883`;
  il `1952` è già a posto).
- **`FAQPage` su tutti**: i rich result FAQ sono ritirati dal **7 maggio 2026** — il markup resta valido,
  ma non promette più niente in SERP.
- **La dichiarazione di affiliazione non esiste su nessuna pagina**, mentre quattro articoli la insegnano
  (`1593`, `1603`, `1900`, `1962`) e Amazon ne impone una formula propria. È il difetto più costoso.
- **`nofollow` sulle fonti autorevoli**: incoerente fra articoli (`226`/`227` ce l'hanno, `1412` no). Le
  fonti si linkano normali; `nofollow`/`sponsored` solo per i link commerciali.
- **Duplicazione riquadro + primo paragrafo**: **352 riquadri** sul sito, **29 con ripetizione**
  (`204` 9, `206` 7, `202` 5, `203` 4). Dal `209` in poi zero: `213` dimostra che si può fare bene.
- **Etichette di tema non tradotte**: «Updated on» sotto la data italiana, «Table of contents».
- **Campi dello schema a video**: `PT2H`/`PT10M` nei blocchi HowTo (`222`, `1412`, `1441`) — si corregge
  nel template.
- **Cannibalizzazione**: `204`/`212` sullo stesso tema (il `212` linka il `204` 7 volte ed è mai
  scansionato); cinque articoli di affiliazione che si linkano in cerchio; **quattro pagine orfane**
  (`224`, `1441`, `1412`, `1452`).
- **Identità del sito**: autore anonimo (uno pseudonimo, senza credenziali dichiarate), Gravatar predefinito, social del
  footer a `href="#"`, commenti = solo auto-pingback. E il `217` — l'articolo più accurato del sito,
  dieci affermazioni verificabili tutte esatte — **è stato scartato da Google**: il problema è di dominio,
  non di singolo articolo.

*Indirizzi*
- **piatti** come il resto del sito: `https://il-tuo-sito.it/slug-dell-articolo/` — niente prefissi
  gerarchici tipo `/seo/…`.

## Cosa usare per cosa

| Serve per | Strumento |
|---|---|
| SEO on-site: titolo, meta, schema, redirect, 404, link interni, analisi | **abilità `seo` via MCP** (26 abilità) |
| Search Console e Analytics | **Maton** (gateway HTTP, `Authorization: Bearer $MATON_API_KEY`) |
| Ricerca: le query che la gente digita | **suggerimenti Google**: `suggestqueries.google.com/complete/search?client=chrome&hl=it&gl=it&q=…` — **decodifica tollerante**: la risposta non è sempre UTF-8 valido (un byte come `0xe9` fa fallire la decodifica rigida), quindi si prova UTF-8 e si ripiega su `latin-1`/`errors="replace"`; sennò gli accenti diventano `perchÃ¨` o la chiamata si interrompe |
| Ricerca: SERP e pagine | `web_search` / `web_extract` + skill **`duckduckgo-search`** (`ddgs text -q "…" -m 10 -r it-it`); se una pagina blocca, skill `blocked-page-recovery` |
| Ricerca: Reddit | skill **`reddit-reading`** (`scripts/reddit.py search|sub|thread|user|doctor`) — feed pubblici, 1 richiesta al minuto, nessuna credenziale |
| Ricerca: siti che richiedono l'accesso (Reddit completo, LinkedIn, X, Quora, SERP Google) | **`webcmd`** col profilo `sito` — configurazione e accessi in `references/ambiente-setup-maton.md`. Sola lettura, poche pagine per volta |
| Ricerca: tecnica WordPress | **Stack Exchange** sezione `wordpress`, **API di WordPress.org** (`curl --globoff`), feed del **forum italiano** (`it.wordpress.org/support/feed/`), **GitHub**, **Hacker News** |
| Ricerca: scraping quando serve davvero | **Scrapling** in `~/seo-content/.venv` + skill `scrapling` (stealth, ~22 s per pagina) |
| Copertine e infografiche | **opzionali**: `gemini-3-pro-image` (Nano Banana) via `~/seo-content/.venv`. **Senza la chiave API si genera a mano** con l'abbonamento Gemini e il prompt che prepara lo script — `references/immagini-e-stili.md` |
| Bozza su WordPress | REST API con application password, **via curl** |
| Ripubblicare in pillole su social/newsletter | drafting, in `~/seo-content/distribution/` |

## Setup: cosa serve, da dove si installa, come si verifica

**Spostato in `references/ambiente-setup-maton.md`**: il comando di controllo dell'ambiente, la tabella
dei componenti (MCP, REST, Maton, Scrapling, webcmd, immagini, Mnemosyne), la configurazione di **webcmd**
(daemon, profilo `sito`, chi fa gli accessi, siti disponibili oggi) e le **chiamate a Search Console e
Analytics via Maton**. **Leggerlo prima di dire «l'ambiente non funziona» o di configurare qualcosa.**

**Verificato l'11/10/2026**: Maton risponde via curl senza nessuna skill installata —
`GET https://api.maton.ai/connections` → **200**, e `searchAnalytics` su `https://il-tuo-sito.it/` → **200**
con le query vere. Quindi **non serve installare niente**: si chiama via `curl` come negli esempi.

Dove stanno le cose (cartella di lavoro, credenziali, venv, server MCP) è la tabella «Dove stanno le
cose» qui sopra.

## Abilità MCP (plugin SEO, Gutenberg) e stile del tema

**Spostato in `references/abilita-mcp.md`**: l'elenco delle abilità `seo/*` e `gutenberg/*`, come
si legge e come si scrive un contenuto a blocchi, la **trappola dei nomi dei parametri**
(`content/*` vogliono `id`, `gutenberg/*` e `content/get-post` vogliono `post_id`: sbagliare non produce
errore e non succede niente), i valori di **stile del tema** (colori, misure, larghezze, preset) e le
ricette dei pattern. **Leggerlo prima di comporre o modificare un contenuto a blocchi.**

## Come si verificano davvero le modifiche SEO (imparato sul campo)

**Lo schema va confrontato col contenuto visibile — ma sulla SOSTANZA, non sulle stringhe.** FAQ e HowTo
sono validi solo se descrivono roba che si vede in pagina. Cercare le stringhe dei passi come testi
letterali **dà falsi allarmi**, perché la pagina dice la stessa cosa con altre parole: verificato il
24/09/2026, i nomi dei passi HowTo di 211 e 212 compaiono **solo dentro il JSON-LD** (posizione nel
sorgente dentro gli intervalli `<script type="application/ld+json">`), e però in entrambe le pagine
esiste la **procedura equivalente, visibile e numerata** (211: l'elenco di `Come provare un tema senza
rischi`; 212: l'elenco di `Le 5 cose da controllare prima di comprare un hosting`). Quindi i due HowTo
sono legittimi.

Procedura giusta, in due passi: (1) ricerca posizionale dei testi nel sorgente, dentro/fuori gli script
JSON-LD; (2) **lettura del contenuto salvato** per trovare la procedura equivalente nel corpo. Si dichiara
il problema **solo se la procedura in pagina non c'è affatto**. Le FAQ invece si controllano in
`<dt class="seo-faq__question">` — attenzione, gli accenti sono in entità HTML: cercare «è» senza
entità le fa sembrare assenti.

**Casi reali dalla stessa verifica:** 208 ha due `HowToTool` chiamati letteralmente `"Array"` (campo meta
`tools` rotto, quello è un difetto vero); 211 ha il titolo dello HowTo più ampio della sezione visibile e
un quarto passo che nel testo non esiste; 212 ha i 5 passi che corrispondono uno a uno all'elenco visibile.
Le abilità di lettura del plugin **non sempre dicono la verità**: la verifica vera è l'HTML pubblico.

- **`missing_meta` vuole titolo *e* description**: il controllo (`seo-abilities.php`) segnala il
  problema se manca anche **solo** `_sito_seo_title`. Scrivere solo la description non fa
  scendere il conteggio.
- **`get-post-seo` non legge la description personalizzata**: restituisce un estratto del contenuto
  con ellissi anche quando `_sito_seo_description` è valorizzata. **Non fidarsi di quel campo:**
  verificare con
  `curl -s https://il-tuo-sito.it/<slug>/ | grep -o '<meta name="description"[^>]*>'`
  (o con `meta/get-post-meta` su `_sito_seo_description`, che è la fonte vera).
- **Il tag robots usa virgolette singole** nell'HTML di questo sito:
  `<meta name='robots' content='max-image-preview:large, noindex' />`. Cercarlo con virgolette
  doppie fa credere che non ci sia (successo davvero).
- **`noindex` sull'HTML**: si scrive `meta/update-post-meta` con
  `{"_sito_seo_robots": {"noindex": true, "nofollow": false}}`; il plugin lo applica tramite
  il filtro di WordPress `wp_robots`. Il contatore `noindex_posts` del riepilogo resta però a **0**
  per un difetto del plugin (cerca un formato JSON mentre l'editor salva un array PHP): **non usarlo
  per verificare**, guardare l'HTML.
- **Keyword obiettivo**: campo meta `_sito_seo_focus_keyword` (verificato nel sorgente del plugin),
  si scrive con `meta/update-post-meta`. `update-post-seo` **non** ha quel campo.
- **I link rotti si riscansionano da soli** alla prima lettura di `get-broken-links` dopo la
  modifica, quindi il conteggio si aggiorna senza comandi di riscansione.
- **La home (`https://il-tuo-sito.it/`) viene segnalata come link rotto** ma risponde 200: è un falso
  positivo del controllo (non riesce a mapparla a un articolo). Non toccarla.
- **Modificare i link dentro un articolo**: leggere il contenuto con `get-post-blocks`, salvare una
  copia in `~/seo-content/audits/backup-articoli/`, fare la sostituzione esatta sull'HTML degli anchor,
  riscrivere con `gutenberg/update-post-blocks` passando `content`, poi **rileggere e validare**.
  WordPress conserva le revisioni (`content/list-revisions`, `restore-revision`) come rete di
  sicurezza.

## Schema: quale scegliere, articolo per articolo

**Decidere lo schema fa parte della scrittura dell'articolo, non è un passaggio a parte.** Si imposta
con `seo/update-schema-data` (campi: `schema_type`, `faq`, `howto`, `video`, `product`,
`job`, `event`, `course`, `recipe`, `speakable`, `breadcrumb_label`).

Valori ammessi per `schema_type`: `''` (usa il default del sito), `Article`, `BlogPosting`,
`NewsArticle`, `TechArticle`, `ScholarlyArticle`, `Report`, `WebPage`, `Product`, `JobPosting`,
`Event`, `Course`, `Recipe`, `LocalBusiness`.

**`FAQ` e `HowTo` non sono tipi**: sono blocchi che si aggiungono al tipo. Si mettono **solo se il
contenuto si vede davvero nella pagina** (regola di Google): la FAQ per una sezione di domande e
risposte, lo HowTo per una procedura numerata passo passo.

| Tipo di articolo | `schema_type` | Blocchi aggiuntivi |
|---|---|---|
| Guida o approfondimento (default del sito) | `Article` | — |
| Guida molto tecnica, per chi già conosce l'argomento | `TechArticle` | — |
| Articolo con sezione domande e risposte | `Article` | **FAQ** (una voce per domanda) |
| Procedura passo passo ("come installare…", "come migrare…") | `Article` | **HowTo** (con i passi reali) |
| Confronto o recensione di uno strumento/prodotto | `Article` | `product` se riguarda un prodotto specifico |
| Contenuto con video incorporato | `Article` | **video** |
| Pagina di servizio (contatti, documentazione) | `WebPage` | — |

**Aggiornamento 2026 — FAQ e HowTo non danno più risultati arricchiti (verificato il 19/09/2026):**
Google ha ritirato i risultati delle **FAQ il 7 maggio 2026** (dopo averli già limitati nel 2023 ai siti
governativi e sanitari) e delle **HowTo** già nel 2023. Dal giugno 2026 il Rich Results Test non
supporta più le FAQ e il rapporto dedicato è stato tolto da Search Console. **Il markup resta valido**
(non genera errori, non è una violazione, Google continua a leggerlo per capire la pagina) ma **non
promettere risultati visibili**: nell'articolo si dichiara FAQ/HowTo per far capire la pagina alle
macchine e alle risposte AI, non per il menu a tendina. Fonte:
`https://developers.google.com/search/updates` (voce del 7 maggio 2026).
Chi vuole un risultato visibile investe su Article, Product e recensioni, Event, LocalBusiness,
Breadcrumb, Video: quelli ci sono ancora.

**Regole pratiche**
- il tipo di default del sito è `Article`: non serve impostarlo se l'articolo è una guida normale
- **se l'articolo contiene una FAQ, lo schema FAQ va messo** (verificarlo sul contenuto o con
  `seo/get-schema-data`, non sulla pagina resa di una bozza)
- lo schema deve **descrivere quello che si vede**: niente FAQ o HowTo su contenuti che non li hanno
- i breadcrumb sono disattivati sul sito e Local Business non è configurato: non impostarli per ora
- dopo la scrittura, **rileggere** con `seo/get-schema-data` per confermare

## Il giro completo di un articolo, passo per passo (verificato)

Sequenza provata scrivendo l'articolo *Come misurare l'autorità di un sito* (bozza 1479):

1. **immagini prima del testo**: copertina (16:9, 4K) e infografica (3:2, 2K) con
   `~/seo-content/.venv/bin/python scripts/genera-immagine.py`, poi ridotte a 1408×768 e 1264×848.
   **Se la chiave API non c'è, le immagini si generano a mano** (abbonamento Gemini + prompt dello script) e
   si dichiara «immagini: da generare»: non bloccano la scrittura (`references/immagini-e-stili.md`).
   **Guardare l'infografica con gli occhi** (`vision_analyze`) prima di usarla: il modello può
   sbagliare le parole o perdere gli accenti (è successo con "AUTORITÀ" → rigenerata).
2. **caricare le immagini**: `media/upload` vuole un **URL**, non un file locale. Per un file locale
   si usa **`media/upload-base64`** (`filename`, `mime_type`, `base64`, `alt_text`). Con file da ~1 MB
   il payload base64 supera i limiti della riga di comando: scriverlo in un file e passare
   `curl -d @/tmp/payload.json`.
3. **prova a vuoto obbligatoria**: `content/create-post` accetta `dry_run: true` — valida la richiesta
   senza creare niente. Falla sempre prima di scrivere.
4. **creare la bozza**: `content/create-post` con `title`, `slug` (piatto), `content`, `excerpt`,
   `status: "draft"`, `category_ids`, `featured_image_id` e `meta_input` con
   `{"_sito_seo_focus_keyword": "..."}` (la keyword si può impostare già qui).
5. **campi SEO**: `seo/update-post-seo` con `title` e `description`.
6. **schema**: `seo/update-schema-data` con `schema_type` ed eventuali `faq`/`howto`.
   Il plugin genera il JSON-LD (compreso `FAQPage`) dalla meta: verificato in
   `includes/modules/schema/class-schema.php`.
7. **verifica finale**: `gutenberg/get-post-blocks` per rileggere, `gutenberg/validate-content`
   (deve dire `is_valid_gutenberg: true` e zero problemi), `gutenberg/evaluate-copy` e
   `evaluate-design` per la qualità, `meta/get-post-meta` per la keyword, `get-schema-data` per lo
   schema, e `curl` per confermare che la bozza risponda **404 senza login**, e `python3 scripts/controlla-articolo.py` per i controlli incrociati
   (`controlli-verifica.md`).
8. **nota nel vault**: aggiornare la nota del contenuto (`references/vault-obsidian.md`) con promessa,
   collegamenti, fonti con le date e verifiche spuntate. **Senza la nota aggiornata l'articolo non è
   pronto**: è la nota che dice da dove vengono i numeri.

**Soglie di qualità da rispettare** (imparate sul campo): almeno **1.500 parole**, meglio **1.800-2.000**
per coprire tutto l'argomento — la prima stesura ne aveva 1.266 ed è stata estesa — e **frasi brevi**:
`evaluate-copy` boccia i periodi lunghi (52/100 al primo giro, 92/100 dopo aver spezzato le frasi).

**Il conteggio si verifica PRIMA di creare la bozza, non dopo.** Un articolo non si scrive «e poi si misura»:
si pianificano le sezioni con un budget di parole ciascuna (riferimento pratico: **11-12 sezioni × 160-170
parole = 1.800-2.000**, contando le domande frequenti) e **si misura il contenuto prima di chiamare
`content/create-post`**. Se il conto è sotto il minimo, si allunga **adesso** — non con una seconda passata
sul post già creato. Verificato quattro volte il 30/09/2026: quattro articoli creati a 1.253-1.423 parole e
poi tutti allungati a mano, con il doppio del lavoro e un rapporto da correggere. Le cause tipiche di un
articolo corto: capitoli descritti invece che misurati (mancano i numeri, e i numeri sono parole),
nessun capitolo sulle **domande di chi legge** (le FAQ), e nessun capitolo su **cosa non fare** — che è
quello che i lettori cercano davvero.

**Non inseguire il punteggio perfetto**: `evaluate-copy` legge **elenchi e celle di tabella come se
fossero frasi lunghe** (non hanno punteggiatura), quindi il 100 è irraggiungibile su un articolo ben
strutturato. Un **80 o più con i contenuti giusti va bene**: controllare che i problemi segnalati non
siano veri periodi interminabili nel testo dei paragrafi.

**Avvisi che sono falsi positivi**: su una **bozza**, l'avviso `faq_schema_missing_risk` che compare in
`gutenberg/evaluate-design` (gravità warning, sorgente `rendered-html`) **non è un errore**: quel
controllo sta nel plugin di terze parti del block editor (`MCP Abilities - Block Editor`, non nel repo)
e legge la **pagina resa**, dove su una bozza lo schema FAQ non c'è perché la pagina non è pubblica.
Non è in plugin-seo e non è nel repo: la stringa non si trova cercandola nei plugin del repository.
Verificare lo schema sul contenuto o con `seo/get-schema-data`, non sulla pagina resa.

## Il giro di verifica di un articolo **già pubblicato** (audit dei contenuti)

Lavoro diverso dalla scrittura: si legge, si verifica, si propone — non si tocca niente. Le regole dell'autore:
**si legge tutto parola per parola** (i contatori sottostimano); al secondo lettore va **la pagina intera**,
**mai un estratto né un digest prodotto da uno script**; **ogni accusa si verifica**, la sua e la mia,
comprese le quantità (lui le gonfia); **nessuna scrittura** senza ok per la singola azione; i rapporti si
consegnano **dove li vede lui** (una cartella della cartella di lavoro, un file `.md` per articolo + `00-INDICE.md`), non
dentro il repo del progetto. **Il riassunto in chat si scrive in Markdown ricco — titoli, elenchi,
grassetti e tabelle**: Mada comunica quasi sempre da Telegram e vuole le cose «organizzate bene», e in
Telegram le tabelle si leggono. La preferenza vale per ogni risposta, non solo per i rapporti; le
tabelle del rapporto restano comunque anche nel file `.md`, che è quello che si archivia. La sintesi
serve a decidere cosa aprire, non a sostituire il rapporto.
Procedura completa, comandi, trappole della misurazione e forma del rapporto:
**`references/audit-contenuti-pubblicati.md`** — e i controlli incrociati da usare anche qui (conteggi
annunciati, aritmetica, promesse, artefatti): **`references/controlli-verifica.md`**.

## Il giro di verifica di una **bozza** (non pubblicata)

Variante dell'audit, con regole sue. Una bozza risponde **404**: non c'è stato su Google, sitemap né
pagina resa da valutare — al posto di quello si verifica la **prontezza alla pubblicazione**, e contano
soprattutto i **campi** (titolo SEO, description, slug, **estratto**, immagine, blocco FAQ, link).
Le stringhe inglesi del tema e i **marcatori dei blocchi** (`[RIQUADRO]`, `[CITAZIONE]`, `[IMMAGINE]`,
`[FAQ — schema: attivo]`) **non sono difetti della bozza**: sono del tema e dell'editor, e in pagina
vengono resi. Valgono le stesse regole dell'autore: lettura integrale a mano, testo intero al secondo lettore,
**ogni accusa verificata** (anche le sue), **nessuna scrittura** — solo rapporti, in una cartella separata
da quella degli articoli pubblicati. Procedura, comandi per verificare citazioni e dati, i difetti che
ricorrono in tutte le bozze e la forma del rapporto: **`references/audit-bozze.md`** — più i controlli
incrociati di **`references/controlli-verifica.md`**, che valgono anche su una bozza.

**Applicare le correzioni è un lavoro a parte, con la sua procedura**: si legge il **«piano di
correzione»** del rapporto (non tutto il rapporto), si prendono le modifiche una per una sull'HTML dei
blocchi, si riscrive con lo **stesso `status`** e si rilegge dal sito controllando **ogni singola
modifica**. **Gli agganci si prendono dal testo grezzo, non dal testo pulito, e una sostituzione non
trovata blocca la scrittura**: è l'errore che lascia in pagina il difetto che il rapporto dà per
corretto. Dettaglio, payload, trappole e controllo finale del giro: **`references/audit-bozze.md`**,
sezione «Applicare le correzioni». **Le immagini della bozza restano quelle che ci sono**: non si rigenerano se non lo chiede
l'autore.

## Le 13 procedure

**La procedura 0 si fa una volta sola, al primo avvio: senza, tutte le altre chiedono cose che non esistono.**
Le prime due delle altre vivono nei reference: qui resta il puntatore.

### 0. Primo avvio: la configurazione (`setup`)

Serve a far combaciare i **nomi generici** del testo con la **installazione vera** (`references/configurazione.md`).
Si fa una volta, e si rifà solo quando cambia qualcosa (dominio, percorsi, server).

1. **La cartella di lavoro.** Si sceglie (proposta: `~/seo-content/`) e si crea con `content/`, `audits/`,
   `distribution/`, `shared/`, `archivio/`.
2. **Il database del piano**: `shared/lavoro.db` con la tabella `content_calendar` (schema in
   `references/db-schema.md`).
3. **Le credenziali — le fa l'autore, mai in chat**: application password di WordPress in un file con
   permessi 600 (`~/.hermes/secrets/wp-credentials.env`) e la credenziale per l'MCP del sito in
   `~/.hermes/.env`.
4. **Il server MCP in Hermes**:
   `hermes config set mcp_servers '{sito: {url: "https://<dominio>/wp-json/mcp/mcp-adapter-default-server", headers: {Authorization: "${WP_BASIC_AUTH}"}}}'`
   — l'header dipende dal server: **si prova `Authorization` e poi `Auth`** e si tiene quello che risponde.
   Caso vero: **con `Auth` il sito risponde 401, con `Authorization` 200** — l'header giusto è quello che risponde, non quello che sembra giusto. Un **405** significa credenziali accettate e metodo sbagliato per l'handshake.
   Se lo si prova **a mano con curl** (cosa che gli script non fanno): dopo l'`initialize` servono la notifica
   `notifications/initialized` e, su ogni richiesta successiva, l'header **`MCP-Protocol-Version: 2025-06-18`**,
   altrimenti `tools/list` risponde «Invalid Request: MCP-Protocol-Version header is required». **Il modo
   giusto resta lo strumento di Hermes** (`mcp-adapter-*`), non curl.
5. **Il vault delle note**: percorso in `OBSIDIAN_VAULT_PATH` (`~/.hermes/.env`); cartelle e convenzioni
   in `references/vault-obsidian.md`.
6. **Le variabili degli script** in `~/.hermes/.env`: `SEO_WORK_DIR`, `SITE_DOMAIN`, `SITE_MCP_URL`,
   `WP_CREDENTIALS`, `GA4_PROPERTY_ID` (tabella in `references/configurazione.md`).
7. **Il file `CONFIGURAZIONE.md`** nella cartella di lavoro: la mappa fra i nomi generici del testo e i
   valori veri di questa installazione.
8. **La prova**: il controllo dell'ambiente in `references/ambiente-setup-maton.md` deve dire OK su MCP,
   REST, Search Console e Analytics. Quello che manca si **dichiara** — immagini, Scrapling e `ddgs` sono
   **opzionali** e hanno il loro ripiego.

**Dettaglio passo per passo, con i comandi e il controllo finale**: `references/primo-avvio.md`.

**Regola**: si chiede all'autore tutto quello che non si sa e **non si inventa nessun valore**. Un nome
generico che resta nel testo senza la sua corrispondenza reale è un errore di configurazione, non una
licenza a improvvisare.

### 1. Onboarding (`onboard`)

Primo accesso a un progetto, stato del sito, categorie e funnel, **regole editoriali**, i blocchi
dell'editor, il blocco FAQ, il glossario → **`references/scrittura-articolo.md`**.

### 2. Ricerca omnichannel (`research_strategy`)

**A chi credere** — la gerarchia delle fonti, i divieti (attribuzioni anonime, dataset e «team»
inventati), le prove di prima mano e cosa si scrive quando la fonte non c'è →
**`references/fonti.md`**.
I canali, cosa si cerca in ciascuno, cosa si scrive nel rapporto → **`references/ricerca-omnichannel.md`**
(la meccanica di webcmd → **`references/ricerca-webcmd.md`**).


### 3. Strategia e calendario 12 mesi (`plan_strategy`)
1. **Inventario in quattro elenchi** — pubblicati, **bozze**, programmati e cestinato, più le pagine —
   salvato in un file rigenerabile; e per ogni voce **la promessa** letta dai campi vivi
   (titolo SEO + description + H2), non dal titolo del database. Comandi, confronto e trappole:
   **`references/pianificazione-e-duplicati.md`**.
2. Calendario delle prossime settimane, rispettando i giorni di pubblicazione.
3. Mix TOFU/MOFU/BOFU bilanciato, ognuno mappato sulla categoria WordPress corrispondente.
4. Inserimento in blocco nella tabella `content_calendar` del database SQLite
   (`~/seo-content/shared/lavoro.db`, schema in `references/db-schema.md`): per ogni voce entrano
   **`keyword_primaria`**, **`intento`**, la categoria, il `funnel_stage` e `refresh_at`.
5. **Controllo duplicati prima di scrivere**: si confrontano le **promesse**, non i titoli — e si
   confrontano sui contenuti **vivi** (titolo SEO e description con `seo/get-post-seo`), mai
   sulla riga di `content_calendar`, che può portare il titolo vecchio. Tre esiti: promessa già
   coperta → la voce **non entra**; coperta in parte → entra solo dichiarando nel piano **quale parte
   copre ognuno**; libera → entra. Il caso che ha insegnato la regola (29/09/2026: il controllo
   automatico dava «nessun conflitto» mentre l'articolo 223 aveva in pagina la stessa promessa) e la
   mappa del cluster sono in **`references/pianificazione-e-duplicati.md`**.

**Cosa contiene il database, e cosa no.** `content_calendar` contiene **le voci della coda** (`Scheduled`)
e **le bozze già scritte** (`Draft`), con `keyword_primaria`, `intento`, `funnel_stage`, `promessa` e
`scheduled_date`. **I pubblicati non stanno qui**: stanno in `~/seo-content/shared/INVENTARIO.md`,
rigenerabile dal sito (REST + `seo/get-post-seo`), ed è quello che si consulta per il controllo
anti-duplicato. Comando per lo stato: `sqlite3 ~/seo-content/shared/lavoro.db "select status, count(*)
from content_calendar group by status;"`; versione leggibile: `~/seo-content/shared/CALENDARIO.md`
(si rigenera con `scripts/calendario.py`, non si modifica a mano).

**I numeri scritti qui invecchiano: quello che non invecchia è il comando.** Rileggerli, non ricordarli.
Le categorie in rotazione sono quattro (WordPress → Affiliazione → Guide AI → Strumenti AI), e il
`funnel_stage` è **derivato** dall'`intento` (informativo→TOFU, problem solving/commerciale→MOFU,
transazionale→BOFU), mai scelto a parte.

**Le date sono slot, non impegni.** Il ritmo concordato è **due articoli a settimana, martedì e venerdì**:
si assegnano in ordine di rotazione, partendo dai lavori già pronti (prima i **refresh** dei contenuti che
Search Console mostra già vicini, poi le bozze, poi le voci da scrivere) e slittano se il materiale non è
pronto. Il piano del giro vive in `audits/` con la data nel nome (es. `PIANO-ARTICOLI-<AAAA-MM-GG>.md`):
**si cita il più recente, non un nome fisso** — i piani vecchi non sono più su questa macchina.

Riferimenti: `references/roadmap-strategy.md`, `references/funnel-strategy.md`,
`references/parole-chiave.md` (come si sceglie la keyword di ogni riga).

### 3-bis. La manutenzione del piano — un articolo pubblicato non è finito

**Il piano non è solo la coda di quello che si scrive: ha anche una coda di quello che si rivede.** Un
articolo pubblicato può smettere di avere senso — Google lo dice nella pagina dei contenuti utili e le
linee guida dei valutatori chiamano «senza valore aggiunto» le pagine che non aggiungono niente rispetto
a quelle simili sul web. Quindi ogni tanto si guarda indietro, con criteri decisi **prima**.

**Cadenza:** a ogni giro di pianificazione, e comunque **ogni 3 mesi**, si leggono i dati di §11
(`analytics_suite`: `low_ctr`, `decay`, `cannibalization`) e per ogni pagina segnalata si sceglie **uno
dei tre esiti**, in ordine di costo crescente:

| Esito | Quando | Come |
|---|---|---|
| **Aggiornare** | la pagina perde posizioni o è invecchiata, ma la promessa regge | refresh: dati, date e versioni nuovi; poi si rilegge e si valida come un articolo nuovo |
| **Consolidare** | due pagine nostre si contendono la stessa query (cannibalizzazione) | si fondono nella più forte, con redirect dalla perdente |
| **Togliere** | non ha traffico, non ha link, non serve a nessuno | disindizzazione o rimozione, con redirect alla pagina più simile |

**Criteri per «togliere»** (da fissare prima, non quando il caso si presenta): zero traffico organico,
zero link in entrata, nessuna conversione. **Un dettaglio che rende inutile il criterio «zero visite»
da solo:** una pagina con zero visite **non compare in Google Analytics**, quindi il conteggio va fatto
con un crawler o guardando le pagine a traffico bassissimo — non fidandosi del report.

**La manutenzione propone, non esegue**: nessuna cancellazione, disindizzazione o fusione senza un
**ordine esplicito dell'autore e un elenco nominato di contenuti** (regola in `references/regole-di-controllo.md`).
Prima di toccare una pagina si salva il contenuto in `~/seo-content/audits/backup-articoli/` (procedura in §8).

**La coda di manutenzione adesso ha una colonna:** dal 01/10/2026 `content_calendar` ha `refresh_at`
(per le pubblicate = data di pubblicazione + 3 mesi), più `keyword_primaria` e `intento`. Colonne e
stato del riempimento: `references/db-schema.md`. **Le righe senza `refresh_at` sono quelle mai
pubblicate**: non vanno inventate.

### 4. Bozza articolo (`draft_article`)
1. Pillar post da 1.500-3.000 parole, nella lingua configurata, nel formato di output scelto
   (HTML semantico: `h2`, `p`, `figure`, `table`).
2. Passata di **umanizzazione** con il framework Human-GEO: varietà linguistica, ancoraggio
   contestuale, niente frasi fatte.
3. Salva in `~/seo-content/content/<slug>.html`.

#### La passata di umanizzazione, con controlli misurati (imparato il 21/09/2026)

Non basta "scrivere bene": la passata si fa con `humanizer` + `references/humanizer_config.json` e si
**misura**. I controlli, in quest'ordine:

- **parole bandite** (`humanizer_config.json`): tier 1 (`delve`, `tapestry`, `pivotal`, `comprehensive`,
  `landscape`, `testament`, `in conclusione`, `moreover`, `furthermore`) e tier 2 (`elevate`, `unlock`,
  `seamless`, `empower`, `harness`, `dive into`, `embark`, `transformative`, `innovative`, `cutting-edge`).
  Vanno cercati **anche gli equivalenti italiani** (`panorama`, `pietra miliare`, `inoltre`, `potenzia`,
  `rivoluzionario`, `all'avanguardia`, `è importante notare`).
- **frasi oltre 30 parole**: si spezzano. Soglia di partenza tipica: 7-9 frasi. Dopo la passata ne
  restano 0-1 (una può essere l'artefatto della tabella, che il conteggio legge come una frase unica).
- **elenchi con intestazione in grassetto** (`<li><strong>Termine</strong>: …`): è il pattern 16
  dell'umanizzatore. Se il contenuto regge la prosa, si converte in paragrafo.
- **citazioni di community**: la regola di casa chiede **almeno una citazione specifica ogni 500 parole**
  (quindi 4 su un pezzo da 2.000). Reddit, Quora, forum: nomi di community e numeri reali verificati
  in ricerca. Sono anche ciò che alza la copertura entità del plugin.
- **mai inventare aneddoti personali**: se serve una voce in prima persona, si chiede all'autore (la sua
  esperienza è l'unica cosa che non posso scrivere io). Un'"esperienza" inventata viola E-E-A-T.

#### Definizione di "pronto" — controllo prima di dirlo all'autore

Un articolo è pronto solo con **tutti** questi riscontri, non con la maggior parte:

**Ai controlli di forma di questa tabella se ne aggiungono altri, incrociati, che sono obbligatori**
(conteggi annunciati vs elenchi, aritmetica rifatta, riquadro vs corpo, sintesi vs prova, promesse
aperte, blocchi e artefatti, alt di tutte le immagini, la tripletta dell'affiliazione): sono in
**`references/controlli-verifica.md`**. I primi quattro sono bloccanti.

| Controllo | Come | Atteso |
|---|---|---|
| Link interni | `curl -o /dev/null -w '%{http_code}'` su ognuno | tutti **200** |
| Link esterni | idem | tutti **200** |
| Slug e meta | `seo/get-post-seo` + `meta/get-post-meta` | titolo ≤60, description 120-160 |
| Keyword | `_sito_seo_focus_keyword` | impostata |
| Schema | `seo/get-schema-data` | tipo giusto + FAQ se le domande ci sono |
| Meta FAQ | `_sito_seo_faq` | tante voci quante sono nell'articolo |
| Blocchi | `gutenberg/validate-content` | `is_valid_gutenberg: true`, 0 problemi, `roundtrip_equal: true` |
| Immagini | `curl` su ogni URL + `alt` presenti | tutti **200**, 0 `{{…}}` nel contenuto |
| Punteggio | `seo/analyze-post-content` | SEO al massimo; GEO/AEO alti |
| Privacy | `curl` sull'URL pubblico senza login | **404** (è una bozza) |
| **Nota nel vault** | `references/vault-obsidian.md` | aggiornata: promessa, collegamenti, fonti con le date, verifiche spuntate |
**Come si consegna il lavoro all'autore: sempre il link, mai l'allegato.** Verifica sul sito, dal browser:
per ogni articolo sistemato si dà **l'URL pubblico** della pagina (e, quando servono, i link di
riferimento delle fonti). Non mandare file in chat — né PDF, né immagini, né rapporti: gli artefatti
(copertine, infografiche, PDF come il 216) si caricano sul sito o si salvano nella cartella dei
rapporti, e in chat va il link per vederli dal vivo. Detto dall'autore il 25/09/2026:
«non mi serve pdf mi dai sempre il link così vedo sul sito».

Riferimenti: `references/writer_quality.md`, `references/content-structure-templates.md`,
`references/title-formulas.md`, `references/humanizer_config.json`.
`references/vault-obsidian.md` (la nota del contenuto si crea con la voce di calendario e si
aggiorna fino alla pubblicazione).

### 5. Audit EEAT (`audit_eeat`)
1. Controllo delle affermazioni non supportate e delle invenzioni ("mi ricordo quando…", dati
   senza fonte).
2. **Information gain**: almeno 3 concetti che non stanno nei primi 10 risultati.
3. Valuta la biografia dell'autore per i marcatori di competenza.
4. Punteggio unico 0-100 (fiducia del contenuto + fiducia dell'autore) in `~/seo-content/audits/`.
Riferimenti: `references/author-eeat-benchmarks.md`, `references/writer_quality.md`.

### 6. Schema JSON-LD (`generate_schema`)
1. Genera lo schema adatto al tipo di contenuto (Article, FAQ, HowTo, Video, Product, Event…).
2. Aggancia gli identificativi del Knowledge Graph (Wikidata) dove ha senso.
3. **Scrittura**: passare dall'abilità `seo/update-schema-data` — **solo con l'ok dell'autore**.
Riferimenti: `references/schema-architect-logic.md`.

### 7. Intelligenza di sito e mappa delle entità (`site_wide_intelligence`)
1. Scarica la sitemap.
2. Incrocia gli URL con i dati di Search Console (via Maton) per trovare cosa rende e cosa no.
3. Costruisci `~/seo-content/shared/ENTITY_MAP.json` (entità del sito e relazioni).
4. Rapporti di ottimizzazione per singolo contenuto in `~/seo-content/audits/`.
Per il riepilogo rapido esiste già l'abilità `seo/get-site-seo-summary`.

### 8. Link interni (`inject_internal_links`)

**Una volta per gruppo di articoli: la scansione dei link in entrata su tutto il sito.** Si leggono i contenuti
di **tutti** i post pubblicati (REST, `_fields=id,title,content`) e per ogni pagina bersaglio si conta in quanti
articoli compare il suo slug. È il controllo che trova le **pagine orfane**, e nessun altro lo vede: verificato
il 24/09/2026 sono **quattro**: **224** (errori di sicurezza, 0 in / 24 out), **1441** (dominio e DNS, 0 in / 21
out), **1412** (menu, 0 in / 13 out) e **1452** (keyword research, 0 in / 18 out). **Non è più un'anomalia ma un
difetto strutturale del sito**: in tutti e quattro i casi sono **pagine perno molto collegate in uscita che
nessuno cita** — nessuno cita le pagine che considera «generali», e sono proprio quelle che distribuiscono più
link al resto. Il caso più stridente è il 1452: **linka tutto il silo di affiliazione (214, 215, 219, 221) e
nessuno di quei quattro linka lei**. Il rimedio totale è **dodici link** (tre per orfana), ed è l'intervento
più utile all'architettura del sito.

**Il conteggio degli zero in entrata va rifatto con un pattern largo.** Cercare solo lo slug esatto può dare
falsi zeri (link con `?p=<id>`, con URL assoluto, o con il titolo invece dello slug): la scansione buona usa
un pattern tipo `slug|titolo esteso|\?p=<id>`. Verificato sui due casi: entrambi gli zeri **hanno retto** al
controllo largo.

Da tenere presente per i gruppi di articoli **con lo stesso schema di titolo** («Errori comuni con
WordPress…», 222/223/224): sistematicamente **non si linkano fra loro**, e sono i collegamenti più contestuali
che esistano.

**I collegamenti si controllano in due direzioni, e poi si guarda se la pagina è un hub che non distribuisce.**
Non basta sapere dove punta l'articolo: si legge anche se i **vicini semantici** puntano a lui (lettura REST
dei vicini + ricerca dello slug nel loro contenuto), e si confrontano i due elenchi. Il caso tipico che
salta fuori è la **porta d'ingresso di un silo** (stadio TOFU, la prima pagina della categoria): riceve link
da mezza categoria e non ne manda quasi nessuno. Verificato il 24/09/2026 sul 214: riceveva da 219, 221,
1603 e 1452 e mandava **un solo** link di silo. È l'intervento più redditizio in rapporto allo sforzo,
perché i quattro link mancanti sono esattamente il passo successivo che il lettore cerca.
1. Trova 3 articoli esistenti e autorevoli semanticamente vicini (usa `ENTITY_MAP.json` e
   `seo/get-post-link-details`).
2. Prepara le frasi di aggancio contestuali.
3. **Mostra la differenza** all'autore e attendi conferma.
4. Con conferma, applica (in WordPress passando da una bozza o dall'abilità dei link), altrimenti
   fermati alla proposta. In locale: `dry_run` significa "solo proposta, non toccare i file".

### 9. Ripubblicazione (`repurpose_content`)
Da un pillar post ricava: thread per X (3 spunti), post LinkedIn (narrativo), teaser newsletter
(150 parole). Salva in `~/seo-content/distribution/`. Riferimento: `references/funnel-strategy.md`.

### 10. Quota di voce nell'AI search (`analyze_share_of_voice`)
Interroga i motori di ricerca AI (Gemini, Perplexity) **con il browser interno** (`browser_exec`,
anonimo: nessun login serve), estrai i domini citati come fonte, calcola la quota di voce per
`il-tuo-sito.it` e i "fatti di relazione" che i concorrenti portano e voi no.

### 11. Suite analitica (`analytics_suite`)
Tutto via Maton:
- **`low_ctr`**: query con molte impression e pochi clic → proponi titolo e schema nuovi.
- **`decay`**: URL che perdono più del 20% anno su anno → segnali per il "refresh".
- **`cannibalization`**: più URL che si contendono la stessa query → 301 o canonical sul perdente.
Output in `~/seo-content/audits/`.

### 12. Bozza su WordPress (`create_wp_draft`)
1. Immagine in evidenza: genera (vedi sotto), ridimensiona a **1408×768**.
2. Carica l'immagine: `POST /wp-json/wp/v2/media` con l'application password.
3. Crea il post: `POST /wp-json/wp/v2/posts` con `status: "draft"` — **mai `publish`**.
4. Metadati SEO: abilità `seo/update-post-seo` (solo con ok dell'autore).
5. Verifica: rileggi il post e riporta ID e URL di anteprima.

## Immagini: due famiglie, due stili

**Spostato in `references/immagini-e-stili.md`** (estratto da SKILL.md per dimensione, contenuto invariato):
regola WebP non PNG, alt text, pesi misurati, e lo stile di copertine e infografiche (con i rimandi a
`references/stile-copertine.md` e `references/stile-infografiche.md`). **Leggerlo prima di generare, ridimensionare
o caricare un'immagine.**

## Trappole (tutte verificate)

**Un solo file: `references/trappole.md`** — nove sezioni: codici HTTP che non sono link rotti (202/403
anti-bot, `chat.openai.com`, `wordfence`) · fonti e autorevolezza · pagine a zero impression · schema
(`@type`, promesse di risultati arricchiti) · meta in caratteri · **contenuto: il difetto `u003` e i
blocchi rotti** · blocchi, media, ambiente · domanda e query (il segnale «Mancanti:», il sintomo) · bozze.

**Le tre che sono costate di più, in breve:** il **`u003`** si vede a occhio nudo in pagina e va cercato
su tutto il sito (24/09/2026: 1441, 1479, 222); le **immagini** si controllano una per una, non a occhio
(3 rotte su 148) e le **varianti ridimensionate** vanno usate, non solo generate; un **403 o un 202 non è
un link rotto** se il sito è dietro una sfida anti-bot.

## Riferimenti

**L'elenco completo dei `references/` è la «Mappa dei file» qui sopra, con il peso di ognuno: questo
file non lo ripete.** Due elenchi delle stesse cose divergono, e il meno aggiornato è quello che
qualcuno leggerà.

**Nessun reference orfano**: ogni file in `references/` sta nella mappa. Se ne aggiungi uno e non lo
metti lì, diventa invisibile come lo è stato `schema-google-support.md` fino al 24/09/2026.

**Script in `scripts/`:** `controlla-articolo.py` (**i controlli incrociati prima di pubblicare**: numeri
annunciati contro le voci vicine, aritmetica, artefatti rimasti nel testo, alt di tutte le immagini, link
interni con etichetta, ripetizioni a mezza frase, intestazioni vuote; `--parole` per il conteggio **prima**
di creare la bozza, `--json` per usarlo da altri script — limiti e procedura in
`references/controlli-verifica.md` §8), `genera-immagine.py` (copertina), `genera-infografica.py`,
`stato-sito.py` (riepilogo SEO e analytics in sola lettura), `calendario.py`, `verifica-avvio.py` (il controllo
d'avvio: cartella di lavoro, database, credenziali senza mostrarne i valori, MCP provando entrambi gli header,
REST, Maton).

**Versioni precedenti del `SKILL.md`: non dentro l'albero della skill.** Una copia di `SKILL.md`
dentro la skill crea una skill omonima e **rompe il caricamento per nome** (è successo davvero, fino
al 01/10/2026: `skill_view` rispondeva *Ambiguous skill name*). L'istantanea sta fuori, in `~/seo-content/archivio/seo-content-istantanea/`.

**Due copie, e non sono la stessa cosa.** `~/.hermes/skills/productivity/seo-content/` è la copia che
Hermes carica **ed è quella che il curator di Hermes aggiorna da solo** (la lezione, la prova e il registro
stanno in `~/.hermes/skills/.curator_ledger.jsonl`); `~/seo-content/archivio/seo-content-istantanea/` è un'istantanea che
**non si aggiorna da sola** e invecchia in silenzio. Prima di modificare una regola: **confrontare le due
copie** (`diff -rq <istantanea> <installata>`) e modificare **l'installata**; poi rigenerare l'istantanea, che
serve come storico. **Mai copiare l'istantanea sopra l'installata senza riallinearla**, altrimenti si
cancellano le patch che il curator ha già applicato.

**Prima di rendere pubblica la repo** (scansione dei segreti, cosa rendere generico, licenza, igiene del
commit, regole per le PR): **`references/pubblicazione-e-contributi.md`**.
