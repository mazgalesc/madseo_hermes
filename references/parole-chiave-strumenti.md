# Le parole chiave: gli strumenti e i dati

> Parte operativa del lavoro sulle parole chiave: quali programmi girano, come si verificano le
> credenziali **prima** di spendere, cosa finisce nei file e dove. Il *perché* e l'ordine delle
> scelte stanno in `parole-chiave.md`: questo file è il banco degli attrezzi.
>
> Viene dalla skill `seo-keyword-research`, incorporata qui il 17/10/2026: i suoi script stanno in
> `scripts/`, la tabella delle fonti in `references/free-keyword-data-sources.md`.
>
> I valori concreti di una installazione (dominio, percorsi, nomi dei server) stanno in
> `CONFIGURAZIONE.md`, accanto alla cartella di lavoro: qui si usano i nomi generici.

## Rules about the data (apply to every deliverable)

- **No free source gives exact Google volumes.** Autocomplete and Trends give *relative* demand;
  Keyword Planner without an actively spending campaign shows **ranges** (1K–10K); clickstream
  estimates (Ahrefs, Semrush) are modelled. Label every figure with its source and granularity, and
  never print a range or a model as an exact volume — content decisions get made on these numbers.
- **Record source + date with every volume.** Volumes drift; a figure reused later without its
  provenance is a liability. (Citation discipline: `grounded-citations`.)
- **Volume is a filter, not the target.** Around 95% of all keywords get 10 or fewer searches a
  month; shortlisting by volume discards the long tail that actually converts. Rank candidates by
  intent and fit first, then check volume.
- **Never scrape Google SERPs directly.** ToS, blocking, and the litigation pattern against SERP-API
  vendors. Use official APIs, a licensed provider, or the site's own Search Console.
- **A Search Console row is not proof that a page exists.** GSC keeps reporting URLs Google still has
  in its index after the slug was renamed — a 404 can show clicks, impressions and a position. Before
  calling any GSC URL "a page" (worse: "a page competing with another"), run `scripts/check_urls.py`:
  status HTTP **and** existence in WordPress (post/page, any status). A dead URL with impressions =
  a rename without a 301, not cannibalisation. This mistake once produced a false "two pages on the
  same query" claim in a delivered report.
- **Do not mix models in one column** — Google Ads-derived, clickstream-derived and autocomplete
  data are different measurements. One table = one source, stated in the header.

## Order of work

① **Own-site reality first.** Google Search Console API (Search Analytics) is free and the only
free source of *real* queries, impressions, CTR and positions — for the user's own site. It answers
"what do I already rank for" and surfaces near-misses (positions 5-20, worth rewriting). Do this
before opening any external tool.

② **Expand the query set keylessly**, in the site's languages. Both endpoints below are free, need
no account, and return JSON:

```bash
curl -s "https://suggestqueries.google.com/complete/search?client=firefox&hl=it&gl=it&q=<seed>"
curl -s "https://api.bing.com/osjson.aspx?query=<seed>"
```

Vary `hl`/`gl` per market, seed with head terms and then with the site's existing titles. People
Also Ask and related searches require a licensed SERP API — budget for them or skip.

③ **Get free volume reference for the shortlist:** Bing Webmaster Tools → Keyword Research (free
with a WMT account; volume plus country breakdown) and Google Keyword Planner inside a free Google
Ads account (ranges as above). Both are account-gated but cost nothing.

④ **Cluster and shortlist locally — no API.** Group by intent (informational / commercial /
navigational), dedupe near-identical phrasing, cut to the handful that matter. This step is free and
is where the value is; skipping it is how a 3,000-row keyword dump gets delivered.

⑤ **Buy exact numbers only for the shortlist — and spend on purpose.** Assemble the *whole*
shortlist with the free steps above **before** the first paid call, then batch: one DataForSEO task
carries up to **1.000 keywords** for **$0,06** (standard queue) or **$0,09** (live), so 900 keywords
cost exactly what one costs. Never spend a paid call to explore — explore free, pay once. Check the
balance with `GET /v3/appendix/user_data` before and after, report the real charge, and **propose the
next spend before making it** — chi paga approva ogni chiamata: la spesa si propone prima di farla.
An Ahrefs or Semrush MCP is worth it only if the user already pays for that suite. See
`references/free-keyword-data-sources.md` for the source table and the DataForSEO operating rules.

⑥ **Write the result where the user's SEO work lives**, not only into chat. Layout the user expects
(other agents read this folder too, so the index is part of the deliverable, not decoration):

- `SEO_WORK_DIR/shared/keywords/` — one CSV per paid batch, **dated in the filename**, one line per
  keyword with volume/CPC/competition and the source+date in a column;
- `SEO_WORK_DIR/shared/keywords/README.md` — index: what each file holds, its source and date, what
  it cost, the exact regeneration commands, and the data limits (nulls, close variants, foreign
  variants) restated once;
- `SEO_WORK_DIR/audits/` — the dated readable report; per-content audits as **one CSV row per
  content**, not prose.

## Auditing existing content against the keywords it targets

The other direction of the same work: the user asks whether the keywords already targeted by
published posts **and drafts** are right, and how the site is positioned for them. Order of work:

① **Inventory the content first, drafts included.** WordPress REST with the application password:

```
GET /wp-json/wp/v2/posts?status=publish,draft&per_page=100&context=edit&_fields=id,slug,status,title,link,date,modified,meta
GET /wp-json/wp/v2/pages?per_page=100&status=publish,draft&context=edit
```

`context=edit` **plus** auth is what exposes drafts; an unauthenticated call returns published only
and looks like there are no drafts. The `meta` object in the payload lists only *registered* meta
keys — the SEO focus keyword is normally absent, so do not conclude the field is empty. The MCP route
gives the site-level counters in one call and they belong in the report: no-focus-keyword count,
no-meta count, broken links, noindex count, sitemap URL, total published.

② **Positioning before keywords.** Search Analytics with `--dims page-query` is the only view where
"which page competes for which query, and where it sits" appears. Group the rows **by query**: two
URLs sharing one query is cannibalisation, the cheapest and highest-impact fix on the list. And if
most published pages have *no* query row at all, the site has a visibility problem, not a keyword
problem — say that at the top of the report, before proposing any keyword edit. A handful of
impressions spread over dozens of published pages means indexing/authority/age, and keyword edits
will not move it.

③ **Derive the keyword actually targeted — it is not readable.** The site's MCP abilities return SEO
title/description/canonical/robots (get-post-seo), a quality score (analyze-post-content) and the
body (content/get-post); none of them exposes the focus keyword. Derive candidates instead: slug with
hyphens → spaces, the SEO title up to the first `:`/`?`/`|`, and every query Search Console already
attributes to that page. Then confirm a candidate with `seo/analyze-with-keyword`
(`post_id` + `keyword`), which scores the content against a keyword you supply. Probe recipe, ability
parameter quirks and the read-only handshake: `references/abilita-mcp.md`.

④ **Price all candidates in a single paid call** (see ⑤ above), then join them with the positioning:
**one row per content** with keyword, volume, the content's own Search Console impressions/position,
and a verdict in three buckets — *ok* (volume ≥ 100), *low volume* (< 100: keep only if the intent is
precise), *rephrase* (no measured volume for that phrasing).

⑤ **"Rephrase" is not "rewrite".** A slug is a descriptive phrase nobody types, so most existing
content lands in that bucket. The fix is to put the searched wording into the SEO title, the H1 and
one H2 — the article stays. Where the phrase has no volume, give the searched alternative that shares
the article's topic (see the pitfall on token overlap).

## Judging intent against the live SERP (before proposing any rewrite)

The audit above says *what* a page targets; this step says whether that target is winnable, and it is
the step that decides between "rephrase", "re-shape" and "leave it alone".

- **Read the article body before calling the shape wrong.** Title, SEO title and H1 can misrepresent
the piece: a draft whose title promised an explainer was already a per-tool comparison underneath, so
the correct fix was changing the **promise** (SEO title, H1, opening paragraph), not the article. A
verdict of "the shape does not match the SERP" is only valid after the body has been read.
- **The first screen decides.** If page 1 is product/tool pages plus an AI answer block, an
informative page cannot win the head term, whatever its quality — either give the piece the shape the
SERP rewards, or move the target to a phrasing whose page 1 matches the piece. Never both at once.
- **A knowledge panel on the bare term is a stop sign.** When the head term resolves to a person,
place or encyclopaedia entry, the volume belongs to that other intent: retarget the qualified phrase
(`<term> wordpress`, `<term> plugin`) instead of chasing the bare word.
- **Decide People-Also-Ask coverage from the page text, not from the topic.** Count the answer markers
in the body (currency amounts, `cos'è`, `economico`, a named year) for each question; topic adjacency
is not coverage. When one answer is missing, add it **inside the existing page** — and if two pages
already answer the same question, first decide which one owns it, because that is self-competition.
- **Record ads and the AI answer per query** in the report: they explain why a slot is unavailable
even when the ranking looks reachable.

Programs, blocks and pitfalls for reading those SERPs: `references/ricerca-webcmd.md`.

## Scripts that make this procedural

`scripts/gsc.py` — Search Console via the Maton gateway, verified working 2026-10-13.

```bash
python3 scripts/gsc.py --days 28 --dims query                 # query reali: impression, clic, CTR, posizione
python3 scripts/gsc.py --days 90 --dims page --out ~/seo-content/audits/gsc-pages-$(date +%F).csv
python3 scripts/gsc.py --days 28 --dims page-query --top 40
```

Reads `MATON_API_KEY` from `$HERMES_HOME/.env` and never prints it; site defaults to `$SITE_DOMAIN`.
`--out` writes CSV or JSON. Prefer this over hand-written curl: it sorts by impressions, totals CTR, and
handles the URL-encoding of the property path.

`scripts/suggest.py` — keyless Google + Bing autocomplete expansion, no account.

```bash
python3 scripts/suggest.py "sicurezza wordpress" "hosting wordpress" --hl it --gl it
python3 scripts/suggest.py --seeds-file ~/seo-content/shared/semi.txt --out ~/seo-content/audits/suggest.json
```

Reports per-seed counts (a `google=0` seed gets flagged for the two-seed counter-check) and prints the
deduplicated union. Remember: suggestions give the *shape* of demand, never the volume.

`scripts/bing.py` — weekly impressions from Bing Webmaster Tools (free, official `GetKeywordStats`).

```bash
python3 scripts/bing.py hosting wordpress "wordpress lento" --country it --language it-IT
python3 scripts/bing.py --keywords-file ~/seo-content/shared/shortlist.txt --out ~/seo-content/audits/bing.csv
```

**Label every figure as "impression Bing (IT)", never as a search volume** — Bing's Italian share is a
fraction of Google's, so the numbers are usable relatively (keyword vs keyword, week vs week) and not
absolutely. `{"d":[]}` means *no data for that term*, which is a finding, not a failure. Key:
`BING_WEBMASTER_API_KEY` in `$HERMES_HOME/.env` (verified live 2026-10-13: HTTP 200 with weekly rows).

Measured behaviour (2026-10-13): the endpoint answers for **head terms** (`wordpress` 20.815 impressions
over 25 weeks, `hosting` 949, `come creare un sito web` 939) and returns empty for long tails below Bing's
reporting threshold (`wordpress lento`, `sicurezza wordpress`, `miglior hosting wordpress`). `language`
must be the full tag (`it-IT`); `it` alone returns HTTP 400. So: use Bing for relative ranking and trend on
broad terms, and take long-tail numbers from DataForSEO.

`scripts/wikipedia.py` — keyless demand proxy per **topic** (no account, Wikimedia Pageviews API).

```bash
python3 scripts/wikipedia.py WordPress Hosting "Intelligenza artificiale" --days 90
```

Gives daily-mean views, monthly totals and month-over-month trend for the matching `it.wikipedia`
article. It measures how many people *read a topic's encyclopaedia entry*, not how many search for a
keyword — use it to rank topics by real interest and to read a trend when no other free source exists.
A 404 means no data for that title (often the article name differs).

`scripts/volumes.py` — the one paid step: real volumes, CPC and competition for the shortlist.

```bash
python3 scripts/volumes.py --keywords-file ~/seo-content/shared/keyword-shortlist.txt --queue standard \
  --language it --location it --out ~/seo-content/audits/volumi-$(date +%F).csv
```

Credits `DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD` from `$HERMES_HOME/.env`; `--location` can be a
country code (`it`, `us`) or a numeric location_code. Default is the live queue — `--queue standard`
is the cheap one and polls until the task lands; a task accepts up to 1.000 keywords, so feed it the
full shortlist rather than a sample. **Sanitise the list before the task**: the API rejects any keyword
that is too long (roughly more than eight words) or carries `:` `,` `?`, and a rejected task costs
nothing — so strip punctuation and split over-long phrases instead of shipping them. Prints one line
per keyword plus a cost line, and writes CSV/JSON with `--out`. Where the cost line reads 0 the charge
shows only as a balance drop (see Pitfalls). `--sandbox` points the same call at
`sandbox.dataforseo.com`: identical payload, fake values, **$0** — test a change there before the real
run.

## Credentials — verify free before the first billed run

Every source behind these scripts has a **free** probe. Run `scripts/check_credentials.py` whenever keys
are added, moved between profiles, or rotated, and only then start the real work:

```bash
python3 scripts/check_credentials.py
python3 scripts/check_credentials.py --term hosting --country it --language it-IT
```

- **DataForSEO** → `GET https://api.dataforseo.com/v3/appendix/user_data` (Basic auth, cost 0). Returns
  the login, the timezone and `money.balance`; it proves the login/password pair on its own. **Never spend
  a `search_volume` task to find out whether a key works** — the paid call is for data, not for auth.
- **Bing Webmaster** → `GetKeywordStats` on a head term; free, and returns real weekly rows when the key
  is live.
- **Maton** → `GET https://api.maton.ai/connections`; free, and lists the ACTIVE connections behind it
  (GSC plus the GA4 admin/data pair).

All three read `$HERMES_HOME/.env` with `~/.hermes/.env` as fallback and print only presence and length,
never a value. A 200 from the free probe means the key is ready. A 401 from the free probe is the
credential — while an error *body* `40104` is a different thing entirely (see Pitfalls). A key that is
simply absent is not a failure: report the gap and name the source it locks out.

## I valori di questa installazione

Non stanno qui: dominio, percorsi, nomi dei server MCP e identificativi delle proprietà stanno in
**`CONFIGURAZIONE.md`** (accanto alla cartella di lavoro) e nel file di ambiente. Le regole che
valgono sempre:

- **Le chiavi si verificano per presenza, mai per valore** (`scripts/check_credentials.py`); il valore
  non si stampa e non entra in un rapporto (ricetta: skill `hermes-agent`, reference `security-privacy`).
- **Una fonte che manca non è un fallimento**: si dichiara il buco e si nomina cosa resta chiuso. Mai
  stimare un numero al posto di uno che non c'è.
- **Google Ads non si dà per scontata**: la connessione a Keyword Planner è un passo di verifica a
  pagamento, quindi il livello gratuito non la include finché non è provata.
- Su Search Console si usa `scripts/gsc.py`: non si ricava la chiamata a mano da un esempio curl.
- Volume e difficoltà a pagamento: tabella e regole in `references/free-keyword-data-sources.md`
  (DataForSEO Labs: `bulk_keyword_difficulty`, `ranked_keywords`, `domain_rank_overview`).
- Lettura da dietro l'accesso (SERP Google vera, Quora, Reddit, X, LinkedIn):
  `references/ricerca-webcmd.md`.
- Ricerca web approfondita con citazioni: skill `research/parallel-cli` (`PARALLEL_API_KEY` nel file
  di ambiente).
- **Il server MCP del sito si usa in sola lettura** quando il lavoro è di ricerca: `execute-ability`
  può scrivere, quindi ogni scrittura è fuori perimetro (i dettagli in `references/abilita-mcp.md`).
  Gli strumenti MCP compaiono a partire dalla sessione successiva all'avvio del profilo.

## Where the tooling lives

- Which web search/extract provider is configured, and which vendors have a **keyless free tier**:
  the hermes-agent skill's `web-search-providers` reference (includes the curl probe that proves a
  keyless provider is live before recommending it).
- Finding SEO/keyword tools, agent skills and MCP servers, and judging their maturity: the
  grounded-citations skill's `tooling-landscape-research` reference.
- Source-by-source free-vs-paid table with limits: `references/free-keyword-data-sources.md`.

## Pitfalls

- **Autocomplete output presented as demand.** Suggestions show how people phrase things, never how
  often. Discovery yes, volumes no.
- **Trusting a free tool's number for a low-volume keyword.** Below roughly 100 searches/month the
  estimates are noise across all providers; say so instead of ranking them.
- **Recommending a $100+/month suite to answer one question.** Free tier plus pay-per-call covers
  one-off research; check what the user already pays for before proposing anything.
- **Installing a third-party SEO skill or MCP without reading its SKILL.md first.** They run local
  scripts, and several require an account or a paid plan (hosted SEO MCPs, suite-tied MCPs). Read the
  file, check the data source it claims, then decide.
- **`pytrends` is unmaintained** — use `trendspyg` for Google Trends data; cookie/auth-gated CLI
  alternatives exist when it rate-limits.
- **Delivering a list nobody can read.** Every table ships with the intent grouping and, per figure,
  its source and window — that part is data and is always expected. A recommended action is a
  separate thing: la regola di casa è **ricerca, non verdetti**: dati e fonti, mai giudizi sui contenuti. Una raccomandazione entra solo se la richiesta la nomina, in una sezione etichettata, e non travestita da osservazione.
- **Reading the DataForSEO charge from the task payload.** In the standard queue the task's `cost`
  field is `0`; the money appears only as a balance drop. Read `GET /v3/appendix/user_data` before
  and after and report the difference — otherwise the report claims a free call.
- **Treating `40104` as bad credentials.** It means *account verification (email and/or phone) still
  pending in the DataForSEO panel*. `user_data` answering 200 proves the login and password are fine,
  so do not rotate the key or re-derive the request; production and sandbox answer the same gate.
- **Summing close variants.** Near-identical phrasings return the *same* volume (`hosting by/in/a
  wordpress` → all 1300): one aggregated query, not four markets. Count the group once and say so in
  the report, or the market size inflates.
- **Reading a `null` volume as zero demand.** A large share of long-tail rows carries no figure at
  all. Report the null rate per cluster and print `–`, not `0`; absence of data is not absence of
  demand, and those keywords stay in the intent-based shortlist.
- **Trusting autocomplete as monolingual.** An `hl=it` pool still returns English and Spanish
  phrasings (`seo wordpress meaning`, `elementor comentarios`) — strip foreign-language variants
  *before* paying for volumes.
- **Claiming content coverage from a token match alone.** Slug/title overlap marks a keyword
  "covered" as soon as one generic stem (`wordpress`, `sito`) matches half the site; require at least
  two matching stems or a curated per-keyword override, and label the check as lexical — the page
  still has to be read before deciding an intervention. **The same two-stem floor applies when
  *proposing* an alternative keyword by topical overlap**: one shared generic token produces pairings
  a human has to catch (a prompt-writing article "suggested" `wordpress come funziona`).

## Verification before delivering

- **Every URL named in the deliverable passed `scripts/check_urls.py`** — HTTP status *and* existence
  in WordPress (post/page, any status). A Search Console row is not a page: a 404 keeps impressions
  and a position. When one existence claim turns out false, re-check **every** URL in every dataset
  behind the report before re-delivering; the false one is never alone.
- **Every figure states its window and the day it was read.** Re-checking re-uses the declared window:
  the same 90-day query answered a day later returns different counts, and the mismatch reads as a
  contradiction that is not there.
- **Counts of occurrences inside a page come from one literal pattern each.** An alternation or a
  proximity window measures something else and inflates the figure (a phrase occurring 0 times was
  reported as 8 because the pattern was `hosting` plus a price within 40 characters).
- **The perimeter is declared**: which content types and which statuses were analysed, and what was
  left out (pages vs posts, drafts, another site).
- Every volume in the table carries a source and a date; nothing labelled exact that came from a free
  or modelled source.
- Totals are computed by script, not by eye, and the row count matches what was asked for.
- **`SEO_WORK_DIR` is confirmed to hold the live work directory before anything is written.** The path
  in `.env` goes stale when the folder is moved, and a run then writes dated CSVs into an empty
  directory without raising anything — the output looks correct and is invisible to whoever reads the
  real folder. Check the directory exists and holds the site's data before the first write.
- Data files land under `SEO_WORK_DIR` with the index in `shared/keywords/README.md`, so the next
  reader can regenerate every figure without asking.
