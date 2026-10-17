# Ambiente, setup e Maton

> Estratto da `SKILL.md` l'11/10/2026 (il file era a 64.251 caratteri contro il tetto di 60.000 che si è
> dato). **Contenuto invariato**: è la fotografia dell'ambiente di lavoro, di come si verifica, e di come
> si interrogano Search Console e Analytics.
>
> **Da leggere quando**: si prepara l'ambiente, qualcosa dell'ambiente non torna, si configura webcmd, o
> si chiamano Search Console / Analytics. **Il comando di controllo dell'ambiente è in cima.**

## Setup: cosa serve, da dove si installa, come si verifica

**Controllo rapido dell'ambiente** (sola lettura; da eseguire quando qualcosa non torna):

```bash
ls ~/seo-content/.venv/bin/python >/dev/null && echo "venv: OK"
for s in reddit-reading blocked-page-recovery humanizer grounded-citations; do
  find ~/.hermes/skills -maxdepth 3 -type d -name "$s" | grep -q . && echo "skill $s: OK" || echo "skill $s: MANCA"; done
# OPZIONALI (l'assenza non blocca: c'è il ripiego)
[ -d ~/seo-content/.venv ] && echo "scrapling: venv presente" || echo "scrapling: ASSENTE (ripiego: browser interno)"
command -v ddgs >/dev/null && echo "ddgs: presente" || echo "ddgs: ASSENTE (ripiego: web_search)"
grep -q "^GOOGLE_API_KEY=" ~/.hermes/.env && echo "chiave immagini: presente" || echo "chiave immagini: ASSENTE (immagini a mano: immagini-e-stili.md)"
webcmd doctor | tail -3
cp ~/.webcmd/cloak/profiles/sito/Default/Cookies "$TMPDIR/c.db" && sqlite3 "$TMPDIR/c.db" "select count(*) from cookies;"   # 0 = profilo senza accessi (non «sessione scaduta»)
# MCP sito: si verifica chiamando lo strumento `mcp-adapter-discover-abilities`, non con curl
# (sull'endpoint: 401 = non autenticato, 405 = autenticato con metodo sbagliato per l'handshake MCP;
#  a mano, dopo l'initialize l'endpoint PRETENDE l'header `MCP-Protocol-Version: 2025-06-18`,
#  altrimenti tools/list risponde «Invalid Request: MCP-Protocol-Version header is required»)
```

### Leggere i file delle credenziali

I file delle credenziali (`~/.hermes/.env`, `~/.hermes/secrets/*.env`) contengono **valori con spazi e
caratteri speciali** e non sono pensati per essere letti dalla shell: `set -a; . file` **tronca il valore
al primo spazio** (`letto="${MATON_API_KEY:0:12}"` sembra una verifica, è un campione mutilato). Una
verifica fatta così dà risposte sbagliate in entrambe le direzioni: un controllo di sicurezza ha
«trovato» chiavi in chiaro che non esistevano, e per poco non ne dichiarava assenti di vere.

- Si leggono con un **parser** (una riga = `CHIAVE=valore`, si tolgono le virgolette) e i valori si passano
  ai comandi **come argomenti** (`-u "$UTENTE:$PASSWORD"`), non esportati dalla shell.
- Nei controlli e nei rapporti i valori **non si stampano mai**: si mostra il nome della variabile e basta.
- Cercando un segreto dentro un altro archivio (memoria, skill, documenti) si confrontano i **frammenti
  lunghi** del valore letto dal parser: un URL, un percorso o il nome di un modello che compaiono in un
  testo **non sono segreti** e non vanno segnalati come tali.

| Componente | A cosa serve | Da dove viene | Com'è su questo Mac |
|---|---|---|---|
| **MCP `sito`** | tutte le abilità del sito: SEO (26), Gutenberg (68), contenuti, media, menu, utenti — **273 in tutto** (11/10/2026) | il sito stesso: `https://il-tuo-sito.it/wp-json/mcp/mcp-adapter-default-server` | configurato in `~/.hermes/config.yaml` (`mcp_servers.sito`), autenticazione Basic con `WP_BASIC_AUTH`; espone **3 strumenti** (scopri / leggi / esegui) — le abilità si chiamano *attraverso* quelli |
| **WordPress REST** | creare bozze, caricare media, leggere contenuti | `https://il-tuo-sito.it/wp-json/` | application password in `~/.hermes/secrets/wp-credentials.env` (permessi 600); le password per le applicazioni si creano in `https://il-tuo-sito.it/wp-admin/profile.php` |
| **Maton** | Search Console e Google Analytics 4 | gateway `https://api.maton.ai`, **via `curl`** — verificato l'11/10/2026: `/connections` → 200 e `searchAnalytics` → 200, nessuna skill da installare | `MATON_API_KEY` in `~/.hermes/.env`; le proprietà collegate sono nella tabella «Maton» qui sopra |
| **Scrapling** | leggere pagine che bloccano (stealth, Cloudflare) | `https://github.com/D4Vinci/Scrapling` + skill `scrapling` | pacchetto in `~/seo-content/.venv` (0.4.15, con Playwright 1.63.0). ~22 s per pagina |
| **duckduckgo-search** | ricerca web senza chiavi, seconda opinione sui motori | skill da `skills.sh`: `hermes skills install duckduckgo-search` (autore gamedevCloudy, MIT) | pacchetto `ddgs` 9.16.0 **nel venv di Hermes** (unica eccezione alla regola del venv) |
| **reddit-reading** | leggere Reddit dai feed pubblici | skill da `skills.sh`: `hermes skills install reddit-reading` (autore Teknium, MIT) | lo `scripts/reddit.py` della skill `reddit-reading`; una richiesta al minuto, nessuna chiave |
| **webcmd** | **leggere i siti che richiedono l'accesso** — vedi la sezione qui sotto | `https://github.com/agentrhq/webcmd` · documentazione `https://webcmd.dev/docs` · installazione `npm install -g @agentrhq/webcmd` | daemon locale + profilo `sito` autenticato dall'autore; stato con `webcmd doctor` |
| **Immagini** *(opzionale)* | copertine e infografiche con `gemini-3-pro-image` (Nano Banana) | `https://pypi.org/project/google-genai/` + `GOOGLE_API_KEY` (modalità `vertexai=True`). **Al 11/10/2026 la chiave non c'è e le immagini non sono nel livello gratuito dell'API**: si genera a mano con l'abbonamento Gemini (`immagini-e-stili.md`) | pacchetto in `~/seo-content/.venv` (google-genai 2.24.0), script in `scripts/` |
| **DataForSEO** *(opzionale)* | volume di ricerca esatto, CPC, competizione, **difficoltà (KD)**, intento dichiarato | `https://dataforseo.com` — **a consumo**, con credito di prova | chiave nel file di ambiente (`DATAFORSEO_LOGIN` / `DATAFORSEO_PASSWORD`); script in `scripts/volumes.py`. **Senza, il metodo resta completo** (`parole-chiave.md` §3) |
| **Bing Webmaster** *(opzionale, gratuito)* | impression settimanali sul mercato Bing, per keyword | `https://www.bing.com/webmasters` — gratuito con un account | `BING_WEBMASTER_API_KEY` nel file di ambiente; `bing.py` |
| **Parallel** *(opzionale)* | ricerca web e ricerca approfondita con citazioni | `https://parallel.ai` — a consumo | `PARALLEL_API_KEY` nel file di ambiente; la CLI **non legge il file di ambiente da sola** (`set -a; . ~/.hermes/.env; set +a`) |
| **Script dei dati** *(dentro questa skill)* | `gsc.py`, `volumes.py`, `bing.py`, `suggest.py`, `wikipedia.py`, `check_credentials.py` | in `scripts/` — non serve installare altro | sbloccano i dati di `parole-chiave.md` §3 |
| **Mnemosyne** | memoria a lungo termine fra le sessioni | **provider di memoria di Hermes** (`memory.provider: mnemosyne`), skill `mnemosyne-memory-override` | attiva, database SQLite locale |
| **Skill di supporto** | quando una pagina blocca, l'umanizzazione, le citazioni | installate in Hermes | `blocked-page-recovery` ✅, `humanizer` ✅, `grounded-citations` ✅, `youtube-content`. Il **browser** non è una skill: `browser_exec` è lo strumento interno di Hermes, e **quando una pagina blocca l'automazione non è lui la risposta** — il browser che passa è quello di **`webcmd`** (Cloak, finestra vera) col profilo che ha gli accessi. Verificato il 17/10/2026: i motori AI murano `browser_exec` e rispondono a webcmd |

**Cosa non serve**: `xurl` (la skill c'è ma il binario non è installato, e X ora si legge da webcmd); `gh`
(GitHub non serve al lavoro editoriale); **`rss-feeds` e `blogwatcher` non sono installate** — per un blog
con feed basta `web_extract` sull'URL del feed.

### webcmd — il browser per i siti con accesso

Serve a **una cosa sola**: leggere contenuti che senza login non esistono. Non sostituisce niente di
quanto sopra: il web pubblico si legge con Brave/Exa/Tavily/DuckDuckGo, i siti che bloccano *senza*
chiedere login con Scrapling, la SEO del sito con le abilità MCP.

- **Il giro di ricerca completo** — ambiente e sessione, i programmi (SERP, Quora, Reddit, X, LinkedIn),
  come si legge una SERP, il blocco «Le persone hanno chiesto anche», la controprova dei suggerimenti,
  i segnali da non lasciar passare — sta in **`references/ricerca-webcmd.md`**.

- **Com'è configurato**: modalità locale; daemon sulla porta **9777**; browser proprietario **Cloak**
  (Chromium 145, **140 MB** in `~/.cloakbrowser`); profilo **`sito`** con i cookie in
  `~/.webcmd/cloak/profiles/sito` (decine di MB con gli accessi dentro; **9-10 MB = profilo appena
  creato, cioè vuoto** — sonda in `references/ricerca-webcmd.md`, «Verificare gli accessi»). Il **profilo** è l'identità di autenticazione e i cookie
  vivono lì; la **sessione** è solo la finestra: chiudere la finestra **non** scollega (verificato il
  21/09/2026 chiudendo le sessioni e riaprendone altre).
  **Runtime del browser**: il `package.json` di webcmd **fissa `cloakbrowser` a 0.4.5**, quindi il
  pacchetto globale non viene usato. Il 21/09/2026 è stato portato a **0.5.10** dentro il pacchetto:
  `cd "$(npm root -g)/@agentrhq/webcmd" && npm install cloakbrowser@latest --no-save`,
  poi `webcmd daemon restart` (il `--no-save` lascia intatto il pin, così un reinstallazione di webcmd
  riporta tutto come prima — o forzare con `npm install cloakbrowser@0.4.5 --no-save`). Dopo
  l'aggiornamento gli **accessi hanno retto tutti**, senza dover rifare il login.
  **Aggiornato il 09/10/2026**: runtime a **0.6.0** con lo stesso metodo (`npm install cloakbrowser@latest
  --no-save` dentro `$(npm root -g)/@agentrhq/webcmd`, poi `webcmd daemon restart`). Il percorso del
  pacchetto non è più Homebrew: su questo Mac npm globale usa il prefisso `~/.local/node`, non
  `/opt/homebrew`. Profilo `sito` riconnesso, `webcmd doctor` tutto verde.
- **Chi fa gli accessi**: l'autore, a mano, nella finestra che si apre sul suo Mac. Mai credenziali in chat o
  nei prompt; se una sessione è scaduta `webcmd` risponde `AUTH_REQUIRED` e apre la finestra, e il
  comando di verifica che restituisce va eseguito così com'è.
  **Prima di dire «sessione scaduta»: contare i cookie del profilo.** Reinstallando webcmd il profilo
  `sito` viene ricreato **vuoto** — gli accessi non sono scaduti, sono spariti, e cercare la causa nel
  sito è tempo perso. Sonda, controprova dal vivo e apertura delle pagine di login perché l'autore le trovi
  pronte: «Verificare gli accessi» e «Aprire la finestra degli accessi» in `references/ricerca-webcmd.md`.
- **Regola: sola lettura.** Niente post, commenti, voti, reazioni, inviti, messaggi, iscrizioni, risposte
  o modifiche di profilo. Poche pagine per volta: LinkedIn e X segnalano l'automazione aggressiva, e al
  primo controllo di sicurezza ci si ferma invece di insistere.
- **Siti disponibili oggi** (profilo `sito`): Reddit ✅ (thread completi) · LinkedIn ✅ · X ✅ ·
  Quora italiano ✅ · Google (SERP italiana con AI Overview e «Le persone chiedono») ✅ ·
  **Facebook ❌** — bug dello strumento, non dell'accesso: qualunque URL di `facebook.com` fa fallire il
  runtime (`QuickJS transport delivery failed: 'Buffer' is not defined`); non riprovarlo a ogni ricerca.
  **Aggiornare il browser non serve**: portato il runtime a `cloakbrowser` **0.5.10** e riprovato il
  21/09/2026, l'errore è identico → la causa sta nel trasporto QuickJS di webcmd (0.8.4, l'ultima
  versione), quindi serve una versione nuova di webcmd; il login dell'autore resta salvato nel profilo.
  **Segnalato al progetto il 21/09/2026 come issue #532** (`https://github.com/agentrhq/webcmd/issues/532`, pubblicata dall'account GitHub dell'autore): non serve segnalarlo di nuovo — semmai vale la pena ricontrollarla quando esce una versione nuova.
- **Prove, comandi, cautele e disinstallazione**: `~/seo-content/audits/VALUTAZIONE-webcmd-2026-09-21.md`.

## Maton: proprietà e chiamate

Base `https://api.maton.ai`, header `Authorization: Bearer $MATON_API_KEY`, limite 10 richieste/secondo.

| Risorsa | Valore |
|---|---|
| Search Console | proprietà `https://il-tuo-sito.it/` — permesso **siteOwner** (esempio: la proprietà del proprio sito) |
| Google Analytics 4 (il-tuo-sito.it) | proprietà `properties/<ID-GA4>` (account `<ID-ACCOUNT>`) |
| Altri siti raggiungibili | altri siti dello stesso proprietario, con **identificativi delle proprietà da inserire qui** (esempio: `sc-domain:altro-sito.it`, GA4 `properties/<ID>`) |

`template.il-tuo-sito.it` **non è collegato**: né in Search Console né in Analytics. Se serve, va aggiunto prima.

Esempi di chiamata. **Per l'uso normale di Search Console non si scrive questo curl a mano**: si usa
**`scripts/gsc.py`** (ordina per impression, totalizza il CTR, gestisce la
codifica del percorso della proprietà). I curl qui sotto restano per quello che gli script **non** fanno —
per esempio `urlInspection/index:inspect`, che dice se una URL è indicizzata:
```bash
# Search Console: ultime 28 giornate, query e pagine
curl -s https://api.maton.ai/google-search-console/webmasters/v3/sites/https%3A%2F%2Fil-tuo-sito.it%2F/searchAnalytics/query \
  -H "Authorization: Bearer $MATON_API_KEY" -H 'Content-Type: application/json' \
  -d '{"startDate":"2026-08-22","endDate":"2026-09-18","dimensions":["query"],"rowLimit":50}'

# GA4: sessioni per pagina
curl -s https://api.maton.ai/google-analytics-data/v1beta/properties/<ID-GA4>:runReport \
  -H "Authorization: Bearer $MATON_API_KEY" -H 'Content-Type: application/json' \
  -d '{"dateRanges":[{"startDate":"28daysAgo","endDate":"today"}],"dimensions":[{"name":"pagePath"}],"metrics":[{"name":"sessions"}]}'
```

