# Free and cheap keyword data sources

Re-verify prices and limits on the linked page before quoting them — the market repriced through
2026. "Verified live" means the endpoint was called successfully from this machine, not that a
vendor page says so.

## Real data for a site the user owns

| Source | Free? | Gives | Limit / cost | URL |
|---|---|---|---|---|
| Google Search Console API (Search Analytics) | Yes | real queries, impressions, clicks, CTR, positions for owned sites | free; per-user/project QPS+QPD quotas | developers.google.com/webmaster-tools/limits |
| Google Search Console / Analytics MCP servers | Yes | the same own-site data inside the agent | own sites only; cannot show competitors | registry.modelcontextprotocol.io |
| Bing Webmaster Tools → Keyword Research | Yes with account | keyword ideas, **search volume**, trend, country breakdown | account only | bing.com/webmasters/help/keyword-research-628070b6 |
| Bing Webmaster Tools API | Yes with account | programmatic access to the same data | API key per user, covers all verified sites | learn.microsoft.com/en-us/bingwebmaster/getting-access |

## Volume sources (account-gated, free)

| Source | Free? | Gives | Limit | Notes |
|---|---|---|---|---|
| Google Keyword Planner (inside Google Ads) | Yes | volume, ideas, CPC, forecasts | **ranges (1K–10K) unless a campaign is actively spending** | range behaviour reported consistently by 2026 reviews; verify against the actual account |
| Google Ads API — Keyword Planning | Yes with Ads account | keyword ideas + historical metrics programmatically | developer token; stricter rate limits than other services | developers.google.com/google-ads/api/docs/keyword-planning/overview |
| Semrush free tool | Yes | volume, KD, CPC | ~10 analytics reports/day, 10 tracked keywords | zapier.com/blog/best-keyword-research-tool |
| KWFinder (Mangools) | Yes | volume, difficulty | ~5 searches/day | same source as above |
| AnswerThePublic | Yes | question/PPA-style clustering | 3 searches/day (vendor confirms "3 free daily searches") | answerthepublic.com |
| Ubersuggest | Yes | volume + intent + suggestions | ~3 queries/day | neilpatel.com/keyword-research-tool |
| WordStream free tool | Yes | ideas | first 25 keywords, then email gate | wordstream.com/keywords |
| Ahrefs free tools (Keyword Generator, KD checker, Bing keyword tool) | Yes | ideas + volume estimates + KD | tool-by-tool caps; no free tier on Keywords Explorer | ahrefs.com/free-seo-tools |
| Keywords Everywhere / Keyword Tool MCPs | No (credits) | volume from Google Keyword Planner inside the agent | credits expire yearly; cheapest tier ~$5-10 | keywordseverywhere.com, keywordtool.io/mcp |
| **Microsoft Advertising Keyword Planner + Ad Insight API** | Yes — *"Free to use this powerful keyword research tool once you have a Microsoft Advertising account"* | keyword ideas each carrying **monthly searches, competition, average CPC, ad impression share** (`GetKeywordIdeas`); traffic estimates (`GetKeywordTrafficEstimates`) | free account + **free developer token** (Developer Portal) + OAuth; open sandbox environment | learn.microsoft.com/en-us/advertising/guides/keyword-ideas-traffic-estimates · about.ads.microsoft.com/en/tools/planning/keyword-planner |
| Ahrefs Free (ex Webmaster Tools) | Yes, for **verified own sites** | Site Explorer (pages + keywords driving organic traffic, backlinks), Site Audit, Web Analytics | site verified via Search Console | ahrefs.com/free |
| Open PageRank | Yes, free key | domain authority score + monthly history, up to 100 domains per call | **30.000 domains/month**, 60 req/min | domcop.com/openpagerank/documentation |
| Google Custom Search JSON API | Yes | SERP-style results for a configured CSE engine | **100 queries/day**, then $5/1.000 up to 10k/day | developers.google.com/custom-search/v1/overview |
| Currents (news search) | Yes | news, 168 countries, 20+ languages | **250 requests/day**, no card | currentsapi.services |
| Google Trends API | **alpha, application-gated** | official Trends data | apply and wait; assume no access when planning | developers.google.com/search/apis/trends |
| Moz API | nominally | DA/PA, links | **50 rows/month**, 1 request/10s — unusable for research | moz.com/products/api/pricing |

**Not free — do not propose them to answer one question:** Semrush API (needs a Business plan, ~$549/mo),
Ahrefs API (paid plans; the free Ahrefs tools are UI-only), Majestic, SE Ranking API. Google Ads
Keyword Planner is free but ranged *and* its account carries a paid verification step this user has
declined so far — Microsoft Advertising is the free substitute for ideas plus volumes, DataForSEO for
Exact numbers.

## Keyless discovery (no account, no volume)

| Source | What it gives | How |
|---|---|---|
| Google Suggest | real user phrasings, per market (`hl`/`gl`) | `curl -s "https://suggestqueries.google.com/complete/search?client=firefox&hl=it&gl=it&q=<seed>"` — **verified live** |
| Bing autosuggest | same, Bing index | `curl -s "https://api.bing.com/osjson.aspx?query=<seed>"` — **verified live** |
| Google Trends (library) | relative interest, seasonality, related queries | `trendspyg` 1.9.0 on PyPI (maintained); `pytrends` is unreliable |
| Community/forum mining | real phrasing and pain points | search the niche on Reddit/forums and register the URLs as sources |

## Pay-per-call providers (for the shortlist only)

| Provider | Shape | Order of magnitude | Notes |
|---|---|---|---|
| DataForSEO | per-request (SERP, keyword volume, difficulty, backlinks) | **$0,06 per standard task / $0,09 per live task, and one task carries up to 1.000 keywords** — batch the whole shortlist into a single call; SERP ~$0.0006–0.0012 per SERP by queue | verified live: 980 keywords = **$0,06**, balance $1,00 → $0,94. The task payload's `cost` reads `0` in the standard queue — read the charge from `GET /v3/appendix/user_data` before/after. `40104` = account verification (email/phone) still pending, **not** bad credentials. $1 trial credit + unlimited Sandbox |
| Serper | per-request Google SERP | ~$1 per 1,000 at entry, falling with volume | free credits are one-time, **not** a monthly reset |
| Scrapfly / Scrape.do / Searlo | SERP + scrape credits | free starter credits (1,000–3,000) | credit-based, some without expiry |
| Parallel | per-request search/extract/monitor | search & extract at the low end ($1–5 per 1,000) | keyless anonymous tier exists — see hermes-agent → references/web-search-providers.md |

## Open source that builds on those APIs

| Project | What it is | Needs |
|---|---|---|
| every-app/open-seo | self-hosted Semrush/Ahrefs alternative (keyword research, rank tracking) | own DataForSEO key; Docker or Cloudflare deploy |
| Ryze-AI-Adgent/open-seo-mcp-skills | free SEO MCP + MIT skills (keyword research, rank tracking, gaps) | account + GSC/GA4 connection; volumes via Google Ads, competitor data via DataForSEO |
| AgriciDaniel/keywordpro | local keyword console, 94 markets / 46 languages | own DataForSEO key; caches reports so re-opening costs nothing |
| crawlseo | open-source SEO monitoring (GSC + crawler + Core Web Vitals) | GSC access |
| Agent-skill collections (claude-seo, marketingskills, seo-geo-claude-skills) | audit/on-page/GEO skills for coding agents | read the SKILL.md before installing — they run local scripts |

## DataForSEO: sandbox, per-endpoint prices, and the cheaper Labs route

Read from DataForSEO's own docs and pricing pages on 2026-10-14; the sandbox behaviour was exercised
from this machine the same day.

### Sandbox — free, and the way to test before spending

Every endpoint has a free twin: swap the host `api.dataforseo.com` → `sandbox.dataforseo.com` and keep
path, auth and body identical. Responses are structurally real but the **values are fake**, and the
account is not charged (`cost: 0`). No separate signup: the same API login/password work. That makes it
the correct place to debug a payload, a parser or a script change — only the final run goes to
production. `scripts/volumes.py --sandbox` performs the switch.

### What a task costs (production)

| Route | Billing | Price |
|---|---|---|
| `keywords_data/google_ads/search_volume` — Standard queue | per task, **up to 1.000 keywords** in the array | **$0,06** flat |
| `keywords_data/google_ads/search_volume` — Live | per task, up to 1.000 keywords | **$0,09** flat |
| `keywords_data/google_ads/keywords_for_keywords` | per task | $0,06 / $0,09 |
| DataForSEO Labs — most endpoints | task + per item | **$0,012 task + $0,00012/item** |
| DataForSEO Labs — `search_intent` | task + per keyword | $0,0012 task + $0,00012/keyword |

Consequence: the flat Google Ads task is the cheapest way to price a **long** list (1 keyword costs
what 1.000 cost), while the Labs per-item route wins on a **short** one — break-even is around 400
items ($0,012 + 400 × $0,00012 ≈ $0,06). Never submit a 30-keyword Google Ads task: that is $0,06 for
3% of the capacity.

### Labs endpoints that answer questions the Google Ads route cannot

Verified callable against the sandbox on 2026-10-14:

| Endpoint | Gives |
|---|---|
| `dataforseo_labs/google/keyword_ideas/live` | keyword ideas from a seed, with volume |
| `dataforseo_labs/google/related_keywords/live` | related keywords, depth |
| `dataforseo_labs/google/bulk_keyword_difficulty/live` | **keyword difficulty (0-100)** for a supplied list |
| `dataforseo_labs/google/search_intent/live` | informational / commercial / navigational with probability |

So "no KD and no competitor keyword lists" holds only while shopping at the free and Google-Ads
counters: Labs sells KD, ranked keywords, domain rank overview and competitor domains pay-per-item.

### Account floor

Minimum deposit is **$50** and the signup credit is **$1**, so the trial balance is a hard ceiling — it
cannot be topped up in small amounts. Treat every paid call as irreversible and report the balance
delta, not the payload's `cost` field.

## Provenance of this table

Verified live from this machine: the two autocomplete endpoints, the Bing WMT `GetKeywordStats`
endpoint (weekly rows, HTTP 200), and one full DataForSEO volume task (980 keywords, $0,06 charged).
Quoted from vendor pages: Bing WMT Keyword Research, the Microsoft Advertising Keyword Planner /
Ad Insight API, Ahrefs Free, Open PageRank, Google Custom Search, Currents, the Google Trends alpha,
Moz's free cap, and the search-API free tiers (see grounded-citations →
`references/tooling-landscape-research.md`). Secondary sources (named inline): tier limits for
Semrush, KWFinder, AnswerThePublic, Ubersuggest, WordStream, Serper's one-time credits, and the
Keyword Planner range behaviour. Verified 2026-10-14 against DataForSEO's own pricing pages: the $0,06 standard / $0,09 live
price for a Keywords Data task (up to 1.000 keywords) and the Labs task+item model — see the
DataForSEO section above. Unverified: any free tier not re-fetched at the moment of use.
