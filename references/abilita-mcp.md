# Le abilità MCP: il plugin SEO, Gutenberg e lo stile del tema

> Estratto da `SKILL.md` l'11/10/2026 (stessa ragione: il file era oltre il proprio tetto).
> **Contenuto invariato.** È il catalogo delle abilità che si chiamano **attraverso** gli strumenti MCP
> (`mcp-adapter-execute-ability`), più le trappole dei nomi dei parametri e i valori di stile del tema.
>
> **Da leggere quando**: si scrive o si modifica un contenuto a blocchi, si legge un contenuto, si
> scelgono i campi, o si compone un blocco e serve il contesto di stile.

## Abilità del plugin SEO (via MCP)

WordPress espone **87 abilità**, di cui **26 del gruppo `seo`**. L'MCP ne mostra 3
(scopri / leggi / esegui): le abilità si chiamano **attraverso** quelle.

Le più usate:

| Abilità | A cosa serve |
|---|---|
| `seo/get-post-seo`, `update-post-seo` | leggere/scrivere titolo SEO, meta description, OpenGraph di un contenuto |
| `seo/get-schema-data`, `update-schema-data` | schema JSON-LD (FAQ, HowTo, Video, Product, Event, Course, Recipe…) |
| `seo/analyze-post-content`, `analyze-with-keyword` | analisi SEO di un articolo (titolo, lunghezza, intestazioni, keyword) |
| `seo/get-site-seo-summary` | riepilogo dashboard: articoli senza meta, senza keyword, link rotti |
| `seo/analyze-site`, `get-technical-seo` | audit di sito: robots, sitemap, canonical, catene di redirect |
| `seo/detect-search-intent` | intento di ricerca (informativo, navigazionale, transazionale, commerciale) |
| `seo/list-redirects`, `create-redirect`, `delete-redirect` | redirect |
| `seo/list-keyword-links`, `create-keyword-link`, `delete-keyword-link` | link interni automatici per parola chiave |
| `seo/list-404-errors` | errori 404 registrati |
| `seo/get-link-intel-status`, `get-post-link-details`, `get-broken-links` | link intelligence e link interni rotti |
| `seo/get-settings`, `update-settings`, `get-enabled-modules` | impostazioni e moduli del plugin |
| `seo/get-local-business`, `update-local-business` | schema Local Business |
| `seo/get-sitemap-status` | stato della sitemap |

Per un elenco completo e aggiornato: `https://il-tuo-sito.it/wp-json/wp-abilities/v1/abilities?per_page=100`
(il default è **50 per pagina**: senza `per_page` se ne vedono solo la metà).
**Attenzione**: il REST elenca meno abilità dell'MCP (87 contro 273 all'11/10/2026) — il REST mostra solo
quelle esposte pubblicamente. Per l'elenco vero da usare nel lavoro: `mcp-adapter-discover-abilities`.
**Il numero si legge al momento e non si fissa nel testo — e non dipende solo dal tempo, dipende dai plugin
attivi**: il gruppo `ai-editor` (8 abilità) lo porta il plugin dell'editor AI, quindi con esso spento il
totale è **273** e con esso attivo torna **288** — stesso sito, stesso giorno, verificato il 13/10/2026.
Quindi quando un gruppo che c'era non compare più, **prima di scrivere «non esiste più» si controlla lo
stato dei plugin**: lo stato vero è sul singolo plugin (`…/wp/v2/plugins/<cartella>/<slug>` →
`network-active`), non sulla lista, che dà il valore per-sito (vedi «Difetti noti del sito» in `SKILL.md`).

## Abilità Gutenberg (block editor) — 68, dai plugin MCP

Il sito ha attivi tre plugin che espongono il block editor via MCP: **MCP Abilities - Block Editor**
(67/68 abilità `gutenberg/*`), **MCP Adapter** e **MCP Expose Abilities** (contenuti, media, menu,
utenti, opzioni). Totale superficie MCP **all'11/10/2026: 273 abilità** — gutenberg 68, content 27,
multisite-ultimate 51, **26 del plugin SEO**, plugins 11, menus 8, users 7, comments 7, media 5, system 4,
core 3, mcp-adapter 3, meta 3, widgets 3, options 3, taxonomy 1, e **43 dei plugin del sito** (link, lead,
mail, tema, backup, analytics, azioni: i nomi reali stanno nella configurazione locale). **Si rimisura
prima di fidarsene**: la lista cambia con i plugin attivi.

**Come si legge un contenuto Gutenberg** (verificato sull'articolo 585, 107 blocchi):
`gutenberg/get-post-blocks` con `{post_id}` → restituisce `{success, post, content, summary, blocks}`;
ogni blocco ha la forma `{block_name, attrs, inner_blocks, inner_html, inner_content}`
(es. `core/paragraph`, `core/heading`, `core/image`, `core/list`).

**Come si controlla prima di salvare**: `gutenberg/validate-content` (struttura + problemi di sintassi +
riepilogo con conteggio blocchi e parole), `gutenberg/audit-content`, `gutenberg/evaluate-design`,
`gutenberg/evaluate-copy`, `gutenberg/evaluate-render-context`, `gutenberg/suggest-design-fixes`,
`gutenberg/suggest-copy-fixes`.

**Come si scrive**:
- nuovo contenuto: `content/create-post` (obbligatorio `title`; `content` accetta blocchi Gutenberg,
  `status` anche `draft`, più `category_ids`, `tag_ids`, `featured_image_id`)
- composizione: `gutenberg/generate-section` (ricette: hero, feature list, FAQ, testimonial, stats row,
  pricing table, team grid, timeline, gallery, contact-map, final CTA), `gutenberg/serialize-blocks`,
  `gutenberg/block-guidance`, `gutenberg/get-section-recipes`, `gutenberg/list-patterns`,
  `gutenberg/insert-pattern-into-post`, `gutenberg/create-page-from-blocks`
- modifiche chirurgiche a un contenuto esistente: `gutenberg/mutate-block-tree` (operazione +
  percorso annidato tipo `[0,1,2]` + `attrs`/`block`), `gutenberg/replace-block-text`,
  `gutenberg/insert-inner-block`, `gutenberg/move-block`, `gutenberg/duplicate-block`,
  `gutenberg/normalize-heading-levels`
- riscrittura completa del documento: `gutenberg/update-post-blocks` (`post_id`, `blocks` o `content`,
  `title`, `status`, `allow_design_markup_loss`)
- immagini: `media/upload` / `media/upload-base64`, poi `featured_image_id` in `content/create-post`
- campi dei plugin: `meta/update-post-meta`; SEO: `seo/update-post-seo`

**Contesto di stile prima di comporre** (per restare nel tema): `gutenberg/get-style-guide`,
`gutenberg/get-theme-context`, `gutenberg/get-style-book`, `gutenberg/list-available-blocks`,
`gutenberg/get-block-details`, e dal plugin del tema `tema/get-design-system` e
`tema/get-patterns`.

**Regola**: si compone a blocchi, si valida, e si crea **solo una bozza**. Mai `status: publish`.

### Il giro di scrittura, verificato end-to-end (19/09/2026)

Sequenza provata creando la bozza 1472:
1. `gutenberg/get-theme-context` + `gutenberg/get-style-guide` → leggere palette, tipografia, larghezze
2. `content/create-post` con `title`, `content` (markup a blocchi) e `status: "draft"` → risponde con `data.posts[0].id`
3. `gutenberg/insert-pattern-into-post` con `post_id`, `pattern_name`, `position: "append"` → innesta un pattern del tema
4. `gutenberg/get-post-blocks` → rileggere quello che si è scritto
5. `gutenberg/validate-content` → `is_valid_gutenberg: true`, zero problemi di sintassi
6. `gutenberg/audit-content`, `evaluate-design`, `evaluate-copy` → controlli qualità (la bozza di prova ha dato copia 100/100 e design 70/100)
7. controllo di sicurezza: `https://il-tuo-sito.it/?p=<id>` **senza login** risponde 404 → la bozza non è pubblica

Per **leggere le bozze esistenti**: `content/list-posts` con `{"status": "draft"}` (risposta in `data.posts[]`, campi `id`, `title`, `status`, `link`).

**Attenzione ai nomi dei parametri (trappola silenziosa)**: le abilità `content/*` che modificano
un contenuto esistente usano **`id`** — `content/update-post`, `content/patch-post`,
`content/delete-post` (+ `force`: `false` = cestino, `true` = definitivo) — mentre le abilità
`gutenberg/*` e `content/get-post` usano **`post_id`**. **Sbagliare nome non produce errore**: la
risposta torna vuota, `success` è `null` e non succede niente. Dopo ogni scrittura **rileggere** e
confermare il risultato (per una cancellazione: `{"status": "trash"}`).

### Valori di stile del tema (tema a blocchi)

| Cosa | Valore |
|---|---|
| Colori | Base `#ffffff`, Base 2 `#f5f5f7`, Base 3 `#e5e6fa`, Contrast `#101012`, Contrast 2 `#000000`, **Accent `#3740b9`** |
| Misure di testo | da `x-small` (0.875rem) a `5-x-large` (2.5-5rem), fluide; `normal` = 1.125rem |
| Carattere | sans di sistema (`ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto…`) |
| Larghezze | contenuto **44rem**, ampio **87rem** |
| Blocchi | **159** disponibili (core/accordion, cover, details, group, columns, image, list…) |
| Pattern | **310**: 249 `tema-blocks/*` + 61 `tema/*`, titoli in italiano (es. `tema-blocks/faq-2-columns` = "FAQ a 2 colonne") |

Nel markup si usano i preset per nome: `{"backgroundColor":"base-2"}` + classe `has-base-2-background-color`,
`{"fontSize":"large"}` + classe `has-large-font-size`, `{"style":{"color":{"text":"var:preset|color|accent)"}}}`.
I blocchi del tema hanno attributi propri (`core/cover`: `mwOverlay`, `mwRatio`, varianti `mw-rounded-corners`,
`mw-shadow`, `mw-hard-border`; `core/accordion`/`core/details`: `mwIcon`, `showIcon`, `iconType`, `iconPosition`).

**Avviso visto sul campo**: innestando il pattern FAQ lo schema FAQ va aggiunto con
`seo/update-schema-data` (con l'ok dell'autore). Su **bozza** l'avviso che lo segnala mancante è un
falso positivo: lo schema non compare nell'HTML perché la pagina non è pubblica (dettagli in "Difetti
noti").

