# Parole chiave: quali scegliere e perché

> Regola di casa: **la scelta delle parole chiave decide se un articolo vale la pena prima ancora che
> sia scritto.** Un articolo ben scritto su una keyword sbagliata è lavoro buttato; un articolo onesto
> su una keyword giusta porta visite per anni. Questo file sta **prima** della scrittura, non dopo.
>
> Meccanica degli strumenti (sessione webcmd, programmi per SERP, Quora, Reddit): `ricerca-webcmd.md`.
> Canali della ricerca e cosa si scrive nel rapporto: `ricerca-omnichannel.md`.
> Dove finiscono le keyword scelte: `../SKILL.md` §3 (`plan_strategy`), colonna «intenzione» del piano.

## 1. L'ordine è: prima l'intento, poi il volume

**L'intento viene prima del volume.** Il motivo è pratico: una keyword cercata tantissimo ma con
l'intento sbagliato porta traffico che non legge, non clicca, non si iscrive e non compra. Una keyword
cercata poco ma con l'intento giusto porta poche persone **giuste**, ed è quella che serve a questo
sito. Se le due cose non si possono avere insieme, **si tiene l'intento e si lascia il volume**.

Conseguenza operativa: **non si sceglie una keyword perché «è cercata molto»**. Si sceglie perché
risponde a una domanda che il lettore di il-tuo-sito.it si sta facendo davvero, e la si verifica.

## 2. Le quattro categorie di intento, e come si riconoscono

Le stesse quattro categorie che usa l'abilità del sito `seo/detect-search-intent`
(**informativo, navigazionale, transazionale, commerciale**). Per un blog come questo:

| Intento | Chi cerca | Cosa vuole trovare | Va bene per |
|---|---|---|---|
| **Informativo** | chi vuole capire | una spiegazione, una guida | l'articolo di blog |
| **Commerciale** | chi sta confrontando prima di decidere | confronti, recensioni, «migliore X» | l'articolo di confronto, la pagina di affiliazione |
| **Transazionale** | chi vuole comprare o fare | prodotto, prezzo, «scarica» | la pagina prodotto, non il blog |
| **Navigazionale** | chi cerca un sito preciso | quel sito e basta | **non si lavora**: si scarta |

**L'intento non si indovina: si legge dalla SERP.** Si cerca la keyword sulla SERP vera (in italiano,
via webcmd) e si guarda **cosa Google mostra in prima pagina**: se sono guide e spiegazioni l'intento è
informativo; se sono confronti e recensioni è commerciale; se sono pagine prodotto è transazionale.

- **Regola dura**: il contenuto che scriviamo deve avere **la stessa forma** di quello che sta in prima
  pagina. Se per quella query Google mostra pagine prodotto, il nostro articolo di blog **non si
  posizionerà**, per quanto sia bello.
- **Quando la forma non corrisponde**, le due uscite sono: cambiare keyword (più informativa), oppure
  creare il contenuto che l'intento chiede. Non c'è una terza via.
- Lo stesso controllo si fa con `seo/detect-search-intent` (lettura, via MCP): serve come
  controprova, **non** come sostituto della lettura della SERP.

## 3. Cosa possiamo misurare — due livelli: gratis (sempre) e a pagamento (opzionale)

Questa sezione evita di scrivere numeri inventati. Si legge in **due livelli**, e **il primo basta**:
il secondo aggiunge dati, non cambia il metodo.

### Il livello gratuito — c'è sempre, e il metodo è completo così

Verificato con `GET https://api.maton.ai/connections` → **HTTP 200, 3 connessioni attive**:
`google-analytics-admin`, `google-analytics-data`, `google-search-console`.

| Dato | Ce l'abbiamo? | Da dove |
|---|---|---|
| Query che portano già impression e clic | **sì** | Search Console via Maton (chiamate in `ambiente-setup-maton.md`) |
| Posizione media e pagine che le intercettano | **sì** | Search Console |
| CTR reale di una query | **sì** | Search Console (clic ÷ impression) |
| Impression sul mercato Bing | **sì, se la chiave c'è** | Bing Webmaster Tools (`bing.py` della skill `seo-keyword-research`) |
| Esistenza e forma della domanda | **sì** | i suggerimenti Google, la SERP vera, Reddit, Quora, i forum |
| Quanto un argomento viene letto | **sì** | Pageviews di Wikipedia (`wikipedia.py`) |
| Andamento nel tempo | **parziale** | confronto fra due finestre di Search Console |
| Volume mensile · difficoltà (KD) · CPC | **no** | servono il livello a pagamento, qui sotto |

**Senza il livello a pagamento il metodo non cambia: cambia solo cosa si può misurare.** Quello che al
posto del volume funziona bene — ed è già la prassi di questa skill:

1. **il numero di suggerimenti** che Google restituisce per un seme: molti suggerimenti = domanda vera;
2. **le query che già ci portano impression** (Search Console): sono domanda reale **e** già a portata;
3. **le domande che si ripetono** su Reddit, Quora e nei forum di settore: sono le parole di chi cerca;
4. **il buon senso sulla nicchia**: un blog su WordPress per principianti non deve posizionarsi su
   «hosting» (troppo largo), deve posizionarsi su «quanto costa un hosting WordPress» (è la domanda).

### Il livello a pagamento — **opzionale**, e quando c'è si dichiara

Con la skill sorella **`seo-keyword-research`** installata e `DATAFORSEO_LOGIN` nel file di ambiente si
sbloccano **volume di ricerca esatto, CPC, competizione, difficoltà (KD) e intento dichiarato** per le
keyword che si indicano. È lo stesso dato che vendono i tool SEO, pagato a richiesta invece che in
abbonamento.

**Nessuno è obbligato a installarlo, e questa skill funziona senza.** Se manca, si scrive «volumi non
disponibili» e si prosegue con il livello gratuito: è quello che si è fatto fino a oggi. Se c'è, ogni
numero che entra in un piano, in un rapporto o in un articolo porta accanto **la fonte e la data**.
**Un numero senza fonte resta un numero inventato — gratis o a pagamento che sia.**

**Cosa cambia davvero, in una riga:** si smette di scegliere la keyword per intuito e si sceglie su un
numero verificabile — e si sa **quanto è difficile**, che è il dato che manca di più (senza la difficoltà,
le keyword impossibili si scoprono solo dopo averle scritte).

**Le regole che evitano di sprecare i crediti** — sono poche e non si saltano:

| Regola | Perché |
|---|---|
| **Il sandbox prima di tutto** — ogni endpoint ha un gemello gratuito su `sandbox.dataforseo.com`: stessa richiesta, stessi permessi, **valori finti e costo 0** | si collauda la pipeline senza pagare; si paga una volta sola, sui dati veri |
| **Solo coda `standard`, mai `live`** | $0,06 contro $0,09 per lo stesso dato |
| **Una richiesta porta fino a 1.000 keyword**: si aspetta di avere la lista **intera** e si manda una volta sola | 1 keyword costa quanto 1.000 — mandare liste corte è lo spreco più comune |
| **Saldo prima e dopo** (`GET /v3/appendix/user_data`) | in coda standard il campo `cost` della risposta è **0**: l'addebito si vede solo dal saldo |
| **Mai pagare per scoprire se una chiave funziona** | la prova delle credenziali è gratuita (`check_credentials.py`) |
| **Una richiesta si propone prima di farla** | il credito di prova si esaurisce e **non si ricarica a piccoli importi** (il deposito minimo è alto): si dice quanto costa e cosa dà, e si aspetta l'ok |
| **Sotto ~400 keyword conviene l'altra strada** (endpoint Labs, a consumo) | il prezzo fisso conviene sulle liste lunghe; sulle corte si paga troppo |

**Quale endpoint risponde a quale domanda.** I nomi servono a chiedere la cosa giusta; i comandi stanno
nella skill `seo-keyword-research`.

| Domanda | Endpoint |
|---|---|
| «quante ricerche al mese ha questa keyword?» (una lista che hai già) | `keywords_data/google_ads/search_volume` |
| «quanto è difficile?» | `dataforseo_labs/google/bulk_keyword_difficulty` |
| «che intento ha?» (controprova di quello letto dalla SERP) | `dataforseo_labs/google/search_intent` |
| «che keyword ci sono intorno a questo tema?» | `dataforseo_labs/google/keyword_ideas`, `related_keywords` |

Comandi, prezzi per esteso e dettaglio operativo stanno nella skill **`seo-keyword-research`**
(`volumes.py`, `check_credentials.py`, `references/free-keyword-data-sources.md`): **qui resta il metodo,
là lo strumento.**

## 4. I cinque passi

**Passo 1 — Semi.** 10-20 termini di base: i temi delle 4 categorie attive del sito (WordPress,
affiliazione, guide AI, strumenti AI) e i problemi che il lettore ha davanti. Si pensa a come
digiterebbe lui: «come», «quanto costa», «perché non funziona», «quale scegliere».

**Passo 2 — Espansione con i suggerimenti.** Si usa **`suggest.py`** della skill `seo-keyword-research`
(Google + Bing, senza chiavi, nessun account): dà le varianti in italiano che le persone digitano davvero, e
gestisce da sé la **trappola della decodifica** — la risposta non è sempre UTF-8 valido, e la lettura
rigida muore con `UnicodeDecodeError` o rende gli accenti storti. Se serve a mano:
`suggestqueries.google.com/complete/search?client=chrome&hl=it&gl=it&q=…`.
**La verifica si fa digitando la FRASE INTERA, non la radice** (lezione del `1883`, verificata rifacendo
la prova): con la sola radice compaiono le estensioni più generiche e si crede che esista una frase che
nessuno cerca. E il numero di suggerimenti non è una prova di volume: è un indizio sulla forma della
domanda (§3). **Da leggere con attenzione i suggerimenti "pieni di marca"**: se un suggerimento contiene un
nome di prodotto, il pezzo generico intorno è un hub — cioè una pagina di categoria, non un articolo
(dettaglio già verificato in `ricerca-webcmd.md`).

**Passo 3 — Analisi dell'intento (il passo che non si salta).** Per ogni candidata: SERP vera con
webcmd, forma dei risultati, categoria di intento (§2). Si scartano qui le navigazionali e quelle in cui
la prima pagina è dominata da Wikipedia, Reddit o siti con autorità molto superiore alla nostra.

**Passo 4 — Da keyword a cluster: una keyword primaria = un contenuto.** Keyword con intento simile e
tema simile **stanno nello stesso articolo**: la più chiara diventa la keyword primaria (il campo
`_sito_seo_focus_keyword`), le altre vivono naturalmente nel testo come sinonimi e varianti
semantiche. **Non si crea una pagina per ogni keyword minima**: è così che nasce la cannibalizzazione
(più pagine nostre che si contendono la stessa query).

**Prima di fissare il cluster, il controllo anti-duplicato va fatto sulla «promessa», non sul titolo** —
la regola è nel `SKILL.md` §3 punto 5, con il caso reale del 29/09/2026 (articolo 223). Se la promessa
che la pagina fa al lettore è la stessa, **la voce non entra nel piano**.

**Prima ancora, la domanda che evita il doppione: questa keyword è già nostra?** Si controlla che nessun
contenuto del sito — pubblicato **o in bozza** — presidi già la query: ricerca nel sito (REST, ricerca
interna), `seo/analyze-post-content`, la query in Search Console, e la **promessa** dei contenuti
vicini. Se c'è già chi la presidia, **non si scrive un articolo nuovo: si aggiorna quello**. È la prima
causa di cannibalizzazione e si vede solo così. Procedura completa: `pianificazione-e-duplicati.md`.

**Il controllo non si fa contando le parole in comune.** Un filtro sulla sovrapposizione lessicale segnala
come «già nostre» query che condividono solo parole generiche (`gratis`, `testo`, `come`, `wordpress`) e
nello stesso giro lascia passare il doppione vero: le due cose si vedono leggendo **la promessa per intero**,
non un punteggio. Lo strumento del controllo è l'inventario dei contenuti (titolo + promessa), confrontato a
mano — il punteggio al massimo serve a ordinare la coda di quelli da leggere.

**Passo 5 — Priorità e data.** Si prioritizza con quello che sappiamo misurare:
`impression già esistenti + quanto la domanda è vicina a una decisione d'acquisto` — **non** con una
formula che chiede il volume (vedi §3). Si costruisce prima l'autorità sui temi vicini, poi si attacca
il tema largo. Ogni cluster diventa **una riga** nella tabella `content_calendar`
(`~/seo-content/shared/lavoro.db`, schema in `db-schema.md`), con la sua categoria, il suo `funnel_stage`,
la sua **`keyword_primaria`** e il suo **`intento`**: così si vede dal piano quali pagine si fanno
concorrenza senza aprire WordPress una per una.

## 5. Revisione: la ricerca non si fa una volta sola

- **Ogni 3 mesi** si rilegge Search Console: le query che ci portano impression sono cambiate, e le
  **pagine a zero impression** vanno guardate (procedura in `trappole.md`).
- **Le query in calo** su una pagina sono il segnale del refresh, non della riscrittura da zero.
- **Una ricerca mai aggiornata** resta buona per poco: i prodotti, i prezzi e le versioni dei plugin
  cambiano, e con loro cambiano le query.
- **Il controllo della tendenza** si fa confrontando due finestre di Search Console (es. ultimi 28
  giorni contro gli stessi 28 giorni dell'anno prima). **Non** si cita Google Trends: non è collegato.
- **La controprova a bozza finita**: la keyword primaria si verifica **sul contenuto** con
  `seo/analyze-with-keyword` e si controlla che **title SEO e H1 non divergano** (il `215` è il
  caso buono: identici, 51 caratteri). Una keyword scelta e mai ricontrollata sul testo è dichiarata,
  non verificata.

## 6. Trappole di questo passo (verificate)

- **Non inventare il volume.** Non c'è una fonte: un numero di volume scritto in un piano editoriale
  è un numero inventato, e l'autore lo tratta come tale.
- **Scegliere per volume e non per intento**: è l'errore che costa di più, perché il lavoro è già
  stato fatto quando ci si accorge che la pagina non si posizionerà.
- **Le sigle ambigue** (es. sigle di prodotto o acronimi con più significati): lo screening è in
  `nomi-e-query.md`; una sigla va verificata prima di diventare keyword primaria.
- **Le traduzioni di keyword inglesi**: su un blog italiano la keyword è quella che si digita in
  italiano. L'inglese si usa solo se non esiste un equivalente italiano usato davvero.
- **Il suggerimento pieno di marca** non è una keyword da articolo: è un hub (§4 passo 2).
- **Zero suggerimenti per un seme**: serve la controprova prima di concludere che la domanda non
  esiste (procedura in `ricerca-webcmd.md`) — quasi sempre è il seme a essere sbagliato, non la domanda.
