# Ricerca omnichannel

> *Estratto da `SKILL.md` il 24/09/2026 per dimensione, contenuto invariato; le intestazioni sono state aggiunte per rendere il file navigabile.*
> **A chi credere** (la gerarchia delle fonti, i divieti, le prove di prima mano): `fonti.md`.
> **Dove finiscono le note di ricerca**: il vault, cartella `Ricerca/` (`vault-obsidian.md`).

## Ricerca omnichannel: i canali e cosa si cerca

### 2. Ricerca omnichannel (`research_strategy`)

**Prima di cercare: le domande.** La ricerca non si fa «sul tema», si fa sulle **domande a cui l'articolo deve
rispondere** — ricavate dalla promessa e dai capitoli previsti (`vault-obsidian.md` §3). Per ogni domanda si
sa già **a quale gradino di fonte appartiene** (`fonti.md` §1). La ricerca è finita quando ogni capitolo
pianificato ha la sua fonte **oppure** la dichiarazione che quella fonte non esiste: un capitolo senza né
fonte né dichiarazione non si scrive.

**La ricerca di un articolo si fa su TUTTI i canali disponibili, non su uno.** Ordine di lavoro:
### I canali, in ordine di lavoro

1. suggerimenti Google (query reali in italiano);

2. **SERP vera** con `webcmd` sul profilo `sito` (Google italiano, con date e sponsorizzati) — vedi
   `references/ricerca-webcmd.md`;
3. `web_search` come seconda opinione sulla SERP, e `web_extract` per leggere le pagine che contano;

4. **Reddit**: `reddit.py` per i feed pubblici, `webcmd` per i thread completi quando serve;

5. **Quora italiano** con `webcmd` (domande e risposte con autore e ruolo);

6. **LinkedIn** e **X** con `webcmd` quando l'argomento è di lavoro o di attualità;
7. fonti tecniche: WordPress.org API, Stack Exchange (sezione `wordpress`), forum italiano
   (`it.wordpress.org/support/feed/`), GitHub, Hacker News.

### Ogni canale va nominato nel rapporto

**Ogni canale va nominato nel rapporto, con quello che ha restituito.** Se un canale non dà risultati
utili, si scrive «nessun risultato pertinente» — **non si inventa** e non si sostituisce con quello che si
sapeva già. Se un canale non è stato usato (perché non pertinente all'argomento), va dichiarato fra i
passi non eseguiti.

### Il dettaglio dei canali

1. **Espandi le query** con **`scripts/suggest.py`**
   (`client=chrome&hl=it&gl=it`): dà le varianti che le persone digitano davvero, **in italiano**. Con un
   seme italiano i risultati sono italiani; con un seme internazionale ("strategia seo") arrivano
   anche varianti straniere.
   **La decodifica è la trappola di questo endpoint** — **verificato il 29/09/2026**: in `latin-1` gli
   accenti escono rotti (`perchÃ¨` al posto di `perché`); la resa è **UTF-8**. Si legge
   `decode("utf-8", "replace")` (ed è quello che `suggest.py` fa già) e, se il testo mostra mojibake, si
   cambia decodifica invece di incolpare Google.

2. **Contesto interno letto per PROMESSE, non per titoli**: inventario dei contenuti pubblicati, in bozza,
   programmati e cestinati, e per ognuno la promessa (titolo SEO + description + H2 vivi) — l'elenco dei
   titoli non dice cosa promette la pagina. Procedura: `pianificazione-e-duplicati.md`. Le promesse stanno
   in chiaro nel **vault** (`Promesse/`).

3. SERP: analizza i primi 10 risultati (`web_search`, `web_extract`) e cerca i vuoti da riempire
   ("Skyscraper 3.0"). La SERP **non viene da Google** (i motori sono Brave/Exa/Tavily): per una
   seconda opinione usare la skill **`duckduckgo-search`** (`ddgs text -q "…" -m 10 -r it-it`).
   Se un concorrente blocca, usare la skill `blocked-page-recovery`.

4. Problemi reali delle persone, non solo SERP:
   - **Reddit**: skill **`reddit-reading`** (`python3 scripts/reddit.py search "…" --limit 20`,
     oppure `sub`, `thread`, `user`, `doctor`). **`--json` va PRIMA del sottocomando**
     (`reddit.py --json thread <url>`): dopo, argparse lo rifiuta con `unrecognized arguments` e
     il file di output resta a zero byte (successo il 29/09/2026 su sette chiamate di fila). Non serve account né chiave: usa i feed pubblici
     Atom, a **una richiesta al minuto** (la skill aspetta da sola quando prende un 429).
     **Non perdere tempo a registrare un'app Reddit**: dal 2025 la creazione di applicazioni passa
     dall'approvazione manuale (Responsible Builder Policy) — la pagina `reddit.com/prefs/apps`
     mostra solo il testo della policy, senza modulo, anche con l'email verificata (verificato il
     21/09/2026). Quindi niente `REDDIT_CLIENT_ID`/`REDDIT_CLIENT_SECRET`: ci si tiene al feed
     anonimo. Per leggere più thread in una volta, o si spaziano le chiamate, o si usa il pannello
     browser loggato **in sola lettura** con l'ok dell'autore.
   - **Siti che richiedono l'accesso, via `webcmd`** (installato il 21/09/2026). `webcmd` è un browser per agenti con profili che sopravvivono fra le sessioni: su questo Mac è in modalità locale col suo Chromium (Cloak) e ha un profilo **`sito` già autenticato su Reddit** dall'autore. Con l'accesso attivo la barriera «Prove your humanity» sparisce e le ricerche Reddit restituiscono thread reali (verificato il 21/09/2026 su r/SEO). Comandi: `webcmd --profile sito session create "<nome>" -f json` → `webcmd --profile sito --session <id> browser run --timeout 90 --no-snapshot-diff --stdin` con un programma Playwright (**il codice gira fuori dalla pagina: dentro servono `page.evaluate`**), `webcmd --profile sito --session <id> browser snapshot`, `webcmd doctor`, `webcmd auth status`, `webcmd auth refresh` (tiene viva la sessione). **Regola dell'autore: sola lettura** — niente post, commenti, voti, messaggi, iscrizioni o modifiche di profilo; se un compito richiedesse una scrittura, fermarsi e chiedere. Non usare il profilo `sito` per altri accessi senza chiedere. Se il profilo risultasse scollegato, `webcmd` risponde `AUTH_REQUIRED` e apre una finestra: **l'accesso lo fall'autore a mano lì**, mai credenziali in chat.
     **Stato al 21/09/2026**: profilo `sito` autenticato dall'autore **sia su Reddit sia su LinkedIn** (verificato: su Reddit la barriera «Prove your humanity» sparisce e le ricerche danno thread reali; su LinkedIn l'URL resta `/feed/` e la pagina mostra la barra Home/My Network/Jobs e il profilo dell'autore). Sessioni usate: `reddit-5q`, `linkedin-7i`. Con LinkedIn si leggono **anche i contenuti degli altri** (post, commenti, ricerca per parola chiave) — cosa che l'API di Maton non permette, lì si legge solo il proprio profilo.
     **Come si estrae il testo (imparato sul campo)**: usare `document.body.innerText` e i ruoli ARIA, **non** i selettori di classe — i nomi delle classi di LinkedIn cambiano di continuo e i selettori indovinati non trovano niente (è successo il 21/09/2026). `x.innerText.replace(/\s+/g,' ').slice(0, 400)` basta a capire dove si è e se si è autenticati.
     **Siti autenticati nel profilo `sito` (verificato il 21/09/2026)**: funzionano **Reddit** (thread completi), **LinkedIn** (`/feed/`), **X** (`x.com/home`: timeline leggibile, i tweet sono `article[data-testid="tweet"]`, autenticazione riconoscibile da `[data-testid="SideNav_AccountSwitcher_Button"]`), **Quora italiano** (`it.quora.com`: nav con Rispondi/Spazi/Aggiungi domanda) e **Google** (SERP italiana leggibile: 9 risultati organici con `#search a h3` e l'**AI Overview** nel testo — ottimo per «Le persone chiedono» e ricerche correlate). **Facebook NON funziona**: qualunque URL di `facebook.com` fa fallire il runtime con `QuickJS transport delivery failed: 'Buffer' is not defined` (provati home, `/groups/feed/` e `mbasic.facebook.com`, con e senza valore di ritorno) — è un bug della 0.8.4, che è l'ultima versione (9/09/2026). Il login dell'autore è comunque salvato nel profilo e servirà quando lo sistemano: **non riprovare Facebook a ogni ricerca**, usare Reddit, LinkedIn, X, Quora e la SERP Google.
     **Andarci piano**: LinkedIn limita e segnala l'automazione aggressiva. Poche pagine per sessione, niente raccolta in massa, nessuna scrittura. Se l'account dovesse essere segnalato, si cancella il profilo `sito` e si torna ai feed pubblici di Reddit e alla sola API per LinkedIn.
     **Regole d'uso (dalla documentazione ufficiale, 21/09/2026)**: il **profilo** è l'identità di autenticazione e i **cookie vivono lì**, la **sessione** è solo la finestra — chiudere la sessione non scollega (verificato il 21/09/2026: chiuse le sessioni, riaperte altre due, Reddit e LinkedIn risultavano ancora autenticati). Una sola sessione per ricerca correlata (conserva lo stato e l'autenticazione). Chiudere le sessioni inattive: c'è un tetto di sessioni concorrenti e su 8 GB RAM conviene non lasciarne aperte. Per le note di ricerca chiedere sempre **URL della fonte**, **null** esplicito per i dati che non ci sono e la **data del controllo**; la pagina viva vince su qualunque cosa ricordata. Il passaggio all'utente appartiene alla sessione che l'ha avviato e il comando di verifica restituito va eseguito così com'è; `session close` è bloccato finché quel passaggio è aperto. Diagnostica: `webcmd doctor -v` e `webcmd setup --status`. La cattura delle chiamate di rete sta in `~/.webcmd/cache/browser-network/` — utile per scoprire API non documentate di un sito.
     `api.stackexchange.com/2.3/search/advanced?order=desc&sort=votes&q=<tema>&site=wordpress`.
   - **Forum italiano**: `it.wordpress.org/support/feed/` (RSS).
   - **WordPress.org**: `api.wordpress.org/plugins/info/1.2/?action=query_plugins&request[search]=…`
     (serve `curl --globoff`) per sapere cosa usa davvero il mercato, con installazioni e date.
   - **GitHub** (issue dei plugin) e **Hacker News** (`hn.algolia.com/api/v1/search?query=…`).
     Per seguire blog e feed: `web_extract` sull'URL del feed RSS. **Le skill `rss-feeds` e `blogwatcher` non sono installate** su questo Mac (verificato il 21/09/2026): non citarle come se ci fossero.

5. LinkedIn: su Maton (OAuth gestito, già collegato) si legge **il proprio profilo e si può
   pubblicare** — `/linkedin/v2/me` funziona, `/linkedin/v2/userinfo` no (scope OpenID assente).
   Contenuti di **altri** non sono leggibili via API: per quelli serve il pannello browser, in
   sola lettura e con l'ok dell'autore. **Non** usare skill che riusano cookie o sessioni del browser.

6. **Output: la nota di ricerca va nel vault** (`Ricerca/`, convenzione in `vault-obsidian.md`), con per
   ogni dato la **fonte con URL** e **la data in cui è stata letta**; una copia in `~/seo-content/audits/`
   quando serve al rapporto. Un dato che non ha una riga nella nota di ricerca non entra nell'articolo.

### Riferimenti

Riferimenti: `references/engine_strategy.md`, `references/local-compliance-benchmarks.md`.
Fonti verificate e comandi esatti: `~/seo-content/audits/RAPPORTO-FONTI-RICERCA-2026-09-21.md`.
