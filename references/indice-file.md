# Indice dei file — dove sta cosa

La skill è divisa in due: **`SKILL.md`** (il banco di lavoro: le due regole ⛔, la configurazione, il metodo,
le 13 procedure) e i **file di `references/`** (i cataloghi: ricette, trappole, regole di scrittura). **Se
cerchi una regola e non è in `SKILL.md`, è in uno di questi file.**

Il metodo resta in `SKILL.md`; qui c'è l'elenco completo, con il peso di ogni file e lo stato di
manutenzione. **Il tetto di `SKILL.md` è 60.000 byte**: quando lo si supera, si sposta qui un blocco e si
lascia nel file principale il puntatore.
La skill è divisa in due: **questo file** (il banco di lavoro: regole, strumenti, metodo, indice) e i
**`references/`** (i cataloghi: ricette, trappole, regole di scrittura). **Se cerchi una regola e non è
qui, è in uno di questi file.**

**I 38 file di `references/`, tutti qui** (i pesi misurati: se un peso non torna,
il file è cambiato — aggiornare la riga).

*Il lavoro, nell'ordine in cui si usa:*

| File | Cosa contiene | Peso |
|---|---|---|
| **`references/ricerca-webcmd.md`** | il giro di ricerca: ambiente e sessione, i programmi (SERP, Quora, Reddit, X, LinkedIn), come si legge una SERP, il blocco «Le persone hanno chiesto anche», la controprova dei suggerimenti, i segnali da non lasciar passare | 25 KB |
| **`references/ricerca-omnichannel.md`** | i canali della ricerca in ordine di lavoro, cosa si cerca in ciascuno, cosa si scrive nel rapporto | 10 KB |
| **`references/parole-chiave.md`** | **quali parole chiave scegliere e perché**: prima l'intento poi il volume, le 4 categorie di intento lette dalla SERP, i 5 passi, **cosa possiamo misurare — due livelli: gratis sempre, a pagamento opzionale (DataForSEO) con le regole anti-spreco**, una keyword primaria = un contenuto, la revisione trimestrale | 13 KB |
| **`references/parole-chiave-strumenti.md`** | **il banco degli attrezzi delle parole chiave** (incorporato il 17/10/2026): le regole sui dati, l'ordine del lavoro, l'audit dei contenuti contro le keyword che dichiarano, il giudizio sull'intento sulla SERP vera, i programmi con i comandi (`gsc.py`, `suggest.py`, `bing.py`, `wikipedia.py`, `volumes.py`, `check_urls.py`, `check_credentials.py`), la verifica delle credenziali **gratis prima di spendere**, le trappole, la verifica finale | 22 KB |
| **`references/free-keyword-data-sources.md`** | **la tabella delle fonti delle parole chiave**: cosa dà gratis e cosa a consumo, prezzi e limiti dichiarati (i prezzi si riverificano sulla pagina prima di citarli) | 10 KB |
| **`references/scrittura-articolo.md`** | come si scrive un articolo: **il test prima di scrivere**, le regole editoriali e il livello del lettore, formato e lunghezza, i blocchi dell'editor, il blocco FAQ, il glossario | 23 KB |
| **`references/audit-contenuti-pubblicati.md`** | il giro di verifica degli articoli **già pubblicati**: le 5 fonti, la pagina intera al secondo lettore, le trappole della misurazione (i difetti falsi), dove sta la causa, la forma del rapporto | ≈33 KB |
| **`references/audit-bozze.md`** | il giro di verifica delle **bozze**: cosa cambia rispetto ai pubblicati, i campi da controllare, i comandi che verificano citazioni e dati, i difetti che ricorrono in tutte le bozze, la forma del rapporto | *(peso da misurare)* |
| **`references/ambiente-setup-maton.md`** | **l'ambiente**: comando di controllo, componenti (MCP, REST, Maton, Scrapling, webcmd, immagini, **fonti facoltative: DataForSEO, Bing Webmaster, Parallel**), configurazione webcmd, accessi, siti disponibili, chiamate a Search Console e Analytics | ≈13 KB |
| **`references/abilita-mcp.md`** | **il catalogo MCP**: abilità `seo/*` e `gutenberg/*`, lettura e scrittura a blocchi, la trappola `id`/`post_id`, i valori di stile del tema, i pattern | ≈10 KB |
| **`references/primo-avvio.md`** | **la procedura 0 in dettaglio**: cosa serve, gli 8 passi con i comandi, il controllo finale, il template di `CONFIGURAZIONE.md` | ≈7 KB |
| **`references/configurazione.md`** | **i nomi generici del testo e i valori reali di una installazione**: la mappa dei nomi, le variabili d'ambiente degli script (**comprese le facoltative**), la regola «nessun valore di una installazione entra nel repository» | ≈3 KB |
| **`references/vault-obsidian.md`** | **il progetto editoriale in un vault Obsidian**: la nota di un contenuto (promessa, struttura, collegamenti, fonti con le date, verifiche), la struttura delle cartelle, il ponte col database, e perché il grafo mostra le pagine orfane | ≈7 KB |
| **`references/pianificazione-e-duplicati.md`** | **prima di scegliere un titolo**: l'inventario in quattro elenchi, la promessa di un contenuto, il confronto sui contenuti vivi, la mappa del cluster, le pagine orfane | ≈8 KB |
| **`references/fonti.md`** | **a chi credere**: la gerarchia delle fonti (ufficiale → normativa/scientifica → API → stampa → community), i divieti (attribuzioni anonime, dataset e «team» inventati), le prove di prima mano, il «non l'ho verificato» | ≈8 KB |
| **`references/controlli-verifica.md`** | **prima di dire «pronto»**: i controlli incrociati che mancavano — conteggi annunciati vs elenchi, aritmetica, riquadro vs corpo, sintesi vs prova, promesse, blocchi, artefatti, alt, affiliazione | ≈10 KB |
| **`references/suite-analitica.md`** | **misurare i risultati**: la chiamata di Search Console, le tre analisi con le soglie, il controllo che i due URL esistano prima di parlare di cannibalizzazione, cosa fare quando i dati non ci sono | 4 KB |
| **`references/pubblicazione-e-contributi.md`** | **portare la skill su una repo pubblica**: la scansione dei segreti (e la trappola del valore troncato dalla shell), cosa rendere generico, licenza, igiene del commit, cosa deve contenere una PR | ≈11 KB |
| **`references/trappole.md`** | **tutte** le trappole verificate in un file solo: codici HTTP, fonti, pagine a zero impression, schema, meta, marcatori rotti, blocchi e media, domanda, bozze | 39 KB |
| **`references/regole-di-controllo.md`** | le regole dettate dall'autore il 30/09/2026 e come si applicano a ogni passo, **più i tre esiti della manutenzione** (aggiornare, consolidare, togliere) con i criteri | 4 KB |

*Tecnica e misure di questo sito:*

| File | Cosa contiene | Peso |
|---|---|---|
| **`references/immagini-e-stili.md`** | WebP non PNG, alt, pesi misurati, stile di copertine e infografiche | 9 KB |
| **`references/stile-copertine.md`** | lo stile delle immagini in evidenza, misurato sul sito | 4 KB |
| **`references/stile-infografiche.md`** | lo stile delle infografiche dentro gli articoli, misurato sul sito | 5 KB |
| **`references/nomi-e-query.md`** | la regola dei nomi, i suggerimenti sbagliati, le sigle ambigue, i suffissi delle varianti immagine, le trappole delle abilità MCP | 4 KB |
| **`references/schema-google-support.md`** | cosa Google supporta davvero nello schema (e cosa ha ritirato) | 3 KB |

*Metodo e cataloghi (documenti dell'autore, portati dalla skill OpenClaw — diversi sono in inglese):*

**Stato di ogni file, dichiarato il 01/10/2026** — *vivo* = si usa così com'è; *parziale* = una parte
non vale qui, e la riga dice quale; *da verificare* = non è stata controllata contro questo sito.

| File | Cosa contiene | Peso | Stato |
|---|---|---|---|
| **`references/content-structure-templates.md`** | modelli di struttura degli articoli (blog, pillar, confronti, listicle, how-to, recensione, FAQ) | 17 KB | **vivo** — corretto il 01/10/2026: aveva una sottiglia ``` mancante (un blocco restava aperto e il markdown dopo veniva letto come codice) |
| **`references/title-formulas.md`** | formule di titolo e pattern di CTR | 10 KB | **vivo** |
| **`references/funnel-strategy.md`** | TOFU/MOFU/BOFU, mappatura sulle categorie, motore di riuso | 3 KB | **vivo** — tradotto in italiano e allineato il 17/10/2026: era in inglese con termini non spiegati, e il thread diceva una misura diversa dalla §9 |
| **`references/roadmap-strategy.md`** | roadmap a 3 fasi (fondamenta → autorità → conquista) | 4 KB | **vivo** — le tre fasi valgono; la priorità si calcola **a due velocità** (senza volume e difficoltà è il caso normale, e va bene; con il livello opzionale si aggiungono volume, difficoltà e intento dichiarato) |
| **`references/schema-architect-logic.md`** | logica dello schema JSON-LD | 2 KB | **vivo** |
| **`references/writer_quality.md`** | standard qualitativi e punteggio di audit | 2 KB | **vivo** |
| **`references/author-eeat-benchmarks.md`** | **chi pubblica, e perché credergli**: i segnali che il sito ha davvero (pagina «Chi siamo», box «Chi scrive», archivio, JSON-LD), le tre domande al posto del punteggio, e la regola **«la persona non si inventa»** | 4 KB | **vivo** — riscritto il 17/10/2026: era in inglese, scritto per un autore-persona, e applicato a un sito che pubblica come marchio dava 20/100 spingendo a inventare una biografia |
| **`references/engine_strategy.md`** | framework omnichannel 3.0, quota di voce AI | 1 KB | **parziale** — le 4 fasi e il ricontrollo a 90 giorni valgono; «scrape Discord» e altre fonti **non si usano** |
| **`references/geo-sync-logic.md`** | ancoraggio delle relazioni per l'AI search | 1 KB | **vivo** |
| **`references/local-compliance-benchmarks.md`** | standard di SEO locale e conformità | 1 KB | **da verificare** — il sito non ha Local Business configurato: da controllare prima di usarlo |
| **`references/humanizer_config.json`** | le parole bandite della passata di umanizzazione | 1 KB | **vivo** — usato dal §4 del `SKILL.md` |
| **`references/db-schema.md`** | la tabella `content_calendar`, colonne e stato del riempimento | 6 KB | **vivo** — corretto il 01/10/2026 (mancavano due colonne, e le tre nuove non c'erano) |

**⚠️ Nota sui documenti dell'autore (aggiornato il 14/10/2026).** Due di questi chiedono cose che su
questa macchina **non si usano** e vanno letti con questa avvertenza:
`roadmap-strategy.md` calcola la priorità con **volume mensile e difficoltà**: quei due dati **non
arrivano dal livello gratuito**, quindi la formula si applica solo con il livello opzionale a
pagamento (`parole-chiave-strumenti.md`) — senza, vale `parole-chiave.md` §4 passo 5, ed è il caso
normale; `engine_strategy.md` prescrive di «scrape Discord» e altre fonti che non usiamo;
`funnel-strategy.md` ha esempi americani (la regola 50/30/20 e la mappatura sulle categorie restano
valide).

**Dentro questo file:** le due regole ⛔ · la configurazione · dove stanno le cose · i difetti noti del sito · cosa usare per
cosa · **il metodo** (giro completo di un articolo, verifica delle modifiche, scelta dello schema) ·
l'indice delle 13 procedure (0-12) · **la manutenzione del piano** (§3-bis) · i puntatori a immagini e trappole.
**Fuori, nei `references/`:** l'ambiente e Maton (`ambiente-setup-maton.md`), le abilità MCP e lo stile del
tema (`abilita-mcp.md`), la pianificazione senza duplicati (`pianificazione-e-duplicati.md`), le fonti
(`fonti.md`), i controlli incrociati (`controlli-verifica.md`), il vault (`vault-obsidian.md`).

**Regola di manutenzione — una lezione nuova va nella sezione giusta di `references/`, non in fondo a
questo file.** È così che il 24/09/2026 questo file è arrivato a **99.890 caratteri su un tetto di
100.000** (e le trappole a esistere in due posti diversi). Prima di aggiungere: **cercare la sezione che
possiede già quell'argomento**; se non esiste, crearla con un'intestazione; **solo se è una regola che
serve in ogni sessione** (le due ⛔, il metodo, la mappa) va qui. Dopo ogni aggiunta, leggere
`wc -c SKILL.md`: sopra i 60.000 caratteri si sposta qualcosa in un reference.

**Due trappole di chi riorganizza, imparate riorganizzando (24/09/2026):**
1. **Le intestazioni si contano fuori dai blocchi di codice.** Un `# commento` dentro un ```bash è
   indistinguibile da un titolo per un parser ingenuo: ho scambiato due commenti di shell per due titoli
   di primo livello, creato una sezione che non esisteva e **rotto l'accoppiamento delle sottiglie ```**.
   Prima di dire «questo documento è disordinato»: **escludere i blocchi di codice** e controllare che
   **ogni sottiglia ``` abbia il suo paio** (aperte = chiuse).
2. **La completezza si verifica con l'inventario globale, non con una lista di pezzi fatta a mano.**
   Un controllo «le sezioni che ricordo ci sono tutte» **passa anche se una sezione è sparita** (mi è
   successo con `Il giro di scrittura, verificato end-to-end`, 1.580 caratteri persi e non visti).
   Il controllo che funziona è il **confronto riga per riga fra il file vecchio e il complesso dei file
   nuovi**, con l'elenco esplicito delle righe volutamente diverse: **quelle devono essere solo quelle
   dichiarate** (sul giro di ricerca e sull'onboarding: 3 righe, tutte dichiarate).
3. **Una sostituzione si applica solo se la stringa da cercare compare esattamente una volta.** Le
   sostituzioni si fanno **contando prima le occorrenze**: se il conto non è 1 non si scrive niente. Una
   parola diversa nella stringa «scritta a memoria» fa fallire la sostituzione, e senza il controllo il
   file resta invariato mentre sembra che la modifica sia passata. Dopo aver **spostato** una sezione in
   un reference, si verifica che **ogni riga spostata esista nel file nuovo** (0 righe non ritrovate): è
   il controllo che impedisce di perdere contenuto spostando.
4. **Il conto delle intestazioni si fa fuori dai blocchi di codice** e le sottiglie ``` si controllano
   pari/dispari dopo ogni modifica: una sottiglia spaiata fa leggere il markdown successivo come codice.
