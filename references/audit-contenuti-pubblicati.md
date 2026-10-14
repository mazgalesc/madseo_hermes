# Audit dei contenuti già pubblicati

Giro di verifica degli articoli **già pubblicati** su il-tuo-sito.it: si legge, si verifica, si propone.
Non si scrive niente (nessuna correzione si applica senza un ok esplicito per quella singola azione).

## Le regole dell'autore su questo lavoro

- **Si legge tutto, parola per parola.** Nessun campione e nessuna misura al posto della lettura: i
  contatori automatici **sottostimano** (una duplicazione rilevata dove ce n'erano sei) e non vedono
  refusi, incoerenze numeriche, promesse non mantenute, frasi che non significano nulla.
- **Il materiale per il secondo lettore lo prepara l'agente leggendo, ed è la pagina INTERA**: testo
  integrale con i titoli al loro posto, tutte le immagini con `alt`, tutti i link con `rel`,
  title/description/canonical, schema, commenti. Un estratto spogliato **non fa risparmiare tempo**: fa
  inventare difetti, perché il valutatore riempie i buchi con le sue assunzioni, e poi le accuse false
  vanno smontate una per una.
- **Nel prompt al secondo lettore va scritto**: *se ti manca un dato scrivi "DATO MANCANTE" e non
  inventarlo*; *cita le frasi esatte*; *conta ciò che è contabile*. Vanno passati anche i dati che ho
  già verificato io (lui non ha accesso a Search Console, all'API di WordPress.org o alla pagina resa).
- **Ogni accusa si verifica, in entrambe le direzioni**: le sue (comprese le **quantità**, che tende a
  gonfiare: "ogni sezione", "sei volte") **e le mie** — una cifra non verificata che avevo scritto io
  nel dossier è tornata indietro come "errore strutturale grave".
- **I rapporti si consegnano dove l'autore li vede**, non dentro il repo del progetto: una cartella della cartella di lavoro, **un file `.md` per articolo** più un `00-INDICE.md` con il tracker (numerazione, data,
  stato) e i difetti trasversali.
- Un articolo per volta, in ordine cronologico, e un file di rapporto per ciascuno.

## Il giro, in ordine (5 fonti indipendenti)

1. **Google** — ispezione URL via Search Console (Maton): `indexStatusResult.coverageState` e
   `lastCrawlTime`. **URL per URL**: non esiste una regola per articolo (pagina "scansionata e
   indicizzata", "scoperta ma non indicizzata", "scansionata ma non indicizzata", "sconosciuta alla
   sitemap" convivono sullo stesso sito).
2. **Abilità del plugin** — `seo/get-post-seo`, `seo/analyze-post-content`,
   `seo/get-schema-data`; **`content/get-post`** per il **contenuto salvato** (serve a capire se
   un difetto è nel testo o nella resa).
3. **HTML pubblico** — scaricato e **guardato**: struttura dei titoli, immagini, link con `rel`,
   tabelle, commenti, schema reso. È qui che si smontano i falsi difetti (§Trappole).
4. **Passata lingua** — parole bandite (`references/humanizer_config.json`) e frasi oltre 30 parole.
5. **Secondo lettore** — `agy` con la pagina intera (§I comandi). La risposta si salva **per intero** su
   file e si legge tutta: non troncare l'output con `tail` (si perde proprio la parte di analisi).

## I comandi

```bash
# 1. la pagina, così com'è
curl -s --max-time 40 -o /tmp/pNNN.html "https://il-tuo-sito.it/<slug>/"

# 2. stato in Google (una chiamata per URL)
curl -s -X POST "https://api.maton.ai/google-search-console/v1/urlInspection/index:inspect" \
  -H "Authorization: Bearer $MATON_API_KEY" -H 'Content-Type: application/json' \
  -d '{"inspectionUrl":"https://il-tuo-sito.it/<slug>/","siteUrl":"https://il-tuo-sito.it/"}'

# 3. il secondo lettore: prima riga SEMPRE questa (vedi coding-agent-cli-orchestration)
#    "non usare strumenti: rispondi solo dal testo che ti passo"
#    `agy` e il node stanno in ~/.local: senza il PATH il comando non si trova
export PATH="$HOME/.local/node/bin:$HOME/.local/bin:$PATH"
agy -p "$(cat /tmp/invio.md)" > rapporto-gemini.md 2>&1
```

Il testo da leggere e da spedire si prepara convertendo l'HTML: titoli marcati (`#`, `##`, `###`),
immagini come `[IMMAGINE: alt | src]`, link come `[testo -> url]`, entità decodificate. **Quella
conversione è per la lettura — non è la pagina**: serve a me per leggere tutto e al valutatore per
averlo tutto, ma **nessun difetto di formattazione si dichiara sul testo convertito** (§Trappole).

## Le trappole della misurazione (producono difetti FALSI)

| Trappola | Fa credere | Cosa fare invece |
|---|---|---|
| Conversione tag → newline | tabelle "incollate", FAQ "muro di testo", H3 "vuoto", H1 "duplicato", menu "duplicato", data "senza spazio" | guardare l'HTML: `<td>` separati; FAQ in `<dt>/<dd>`; l'H1 è uno (la seconda stringa è il **breadcrumb**); i due menu sono **desktop + mobile** (le classi lo dicono); la data è in **due blocchi** distinti |
| Entità non decodificate | title/description "troppo lunghi" (`&#8217;` conta 7 caratteri) | `unescape()` **prima** di contare: un title "da 72" era da 60 |
| Attributi con apici **singoli** | "immagine senza src né alt", "noindex assente" | pattern `["']…["']` (`src='…'`, `alt='…'`, `name='robots'`): nel sito convivono entrambi gli stili |
| HTML tutto su una riga | `grep -c` conta le **righe**, non le occorrenze ("1 cella" in una tabella da 121) | `grep -o … | wc -l` |
| `??` in una cella | sembra artefatto di console | leggere i **byte**: `3f 3f` = due punti interrogativi veri → il contenuto ha perso l'emoji (bandierine!) |
| python inline con backslash nelle f-string | `SyntaxError: f-string expression part cannot include a backslash` | il python di sistema di macOS è 3.9: tenere le regex in variabili di modulo, o scrivere lo script su file invece che in heredoc |
| "risposta corta" di un CLI | sembra una risposta scarna | controllare **la dimensione** dell'output: sotto i ~1.000 caratteri è un **errore**, non una risposta (tipico: permesso negato in headless) |

## Contare le duplicazioni (il difetto tipico di questo sito)

- Il riquadro **"risposta diretta"** apre ogni sezione e il paragrafo successivo **ripete la stessa
  frase**: letterale, riformulata, o clonata su un elenco.
- **Il contatore sottostima**: contare **leggendo**, e dichiarare il **tipo** (letterale / riformulata /
  elenco clonato), non solo il numero. Un articolo con 15 riquadri può averne 2 letterali e 13 riformulati:
  la differenza cambia la diagnosi (è stato corretto, oppure no).
- Le ripetizioni attraversano le sezioni: la stessa frase può comparire in un riquadro, in un paragrafo
  e in una FAQ.
- **Il caso limite: due risposte intere con parole diverse**, una sotto l'altra, che il contatore a frase
  intera dichiara «0 ripetizioni». `1441`: la risposta *«Si possono cambiare i DNS del proprio computer?»*
  detta due volte di fila (riscritta, non copiata) e AXFR spiegato due volte, riquadro e paragrafo;
  `1412`: il riquadro e il testo sulla personalizzazione del menu. **Rilassare il confronto** (stesse
  parole in ordine diverso, stessa risposta entro ~10 righe) invece di fermarsi al confronto letterale: è
  il caso in cui la lettura a mano trova il difetto e la misura automatica dice zero.
- **Le ripetizioni che contano non sono frasi intere**: sono **gli stessi tre numeri** ripetuti in
  corpo, sintesi e FAQ (il contatore a frase intera dice zero) e **il primo paragrafo ripetuto al
  terzo**, con due parole cambiate. Confrontare i **prefissi** dei paragrafi fra loro e le **terne di
  cifre** cercate nel testo, non solo le frasi identiche.

## Rifare i conti a mano, sempre (il difetto che costa più caro)

- **Ogni numero di un articolo si ricalcola**, anche quando "sembra giusto". È il difetto che distrugge
  l'autorevolezza più di dieci frasi lente, e nessun contatore lo vede.
- **I tre casi verificati**: `219` scrive *"1% di conversione × 50 € di scontrino × 4% di commissione =
  **0,40 €** ogni 1.000 clic"* → il conto giusto con quegli stessi numeri è **20 €** (la tabella sbaglia
  di 50 volte); `209` ha i **totali che non sono la somma delle righe** (915 € contro "60-350 €"); `210`
  presenta 80-245 € come "150-300 €".
- **La controprova più veloce è l'articolo stesso**: un numero si controlla contro un altro punto del
  testo. Su `219` *"con 5.000 visite… circa 100 € al mese"* dà 20 € per 1.000 visite e smaschera la
  tabella. Cercare sempre il punto del testo che dice la stessa cosa con altre parole.
- **La stessa misura con valori diversi nello stesso articolo è un difetto anche quando ogni valore,
  preso da solo, regge**: su `219` convivono 0,40 €, 1-2 €, 1-5 € e 20 € per 1.000 visite.
- **Controllare anche**: i totali contro le righe; le percentuali annunciate (*"guadagna venti volte"*)
  contro i valori in tabella; **l'unità di misura** quando si mescolano €/anno e €/mese nella stessa
  colonna (`212`: SiteGround sembra il più economico ed è il più caro, 3,8× Aruba); i valori che
  contraddicono l'esempio principale (`219`: la tabella delle nicchie dà "prodotti fisici 1-2 €" mentre
  l'esempio dà 20 € per gli stessi prodotti).
- **Se il numero esiste ma è sbagliato, il difetto è del punteggio, non della fonte**: su `224` i due CVE
  citati **esistono davvero** e la descrizione combacia con l'NVD, ma la gravità dichiarata (*9,2*) è
  **8.1** e uno dei due è descritto come XSS persistente mentre l'NVD la classifica DOM-based. I nomi
  *"Click2Shell"* e *"Comment2Shell"* non esistono in nessun database. **Verificare il CVE, poi il suo
  punteggio, poi la sua tipologia.**
- **I quantificatori in parole sono numeri**: *"dieci volte meno traffico"*, *"un decimo"*, *"due ordini
  di grandezza"*, *"la metà"*, *"il doppio"*, *"la percentuale resta simile"* si convertono in cifre e si
  confrontano con la tabella **dello stesso articolo**. Verificato il 11/10/2026 sul `1900`: la sua
  tabella mostra 300 visite contro 60 (**un quinto**, non un decimo), 4,50 € contro 120 € (26,7 volte,
  **≈1,4 ordini di grandezza**, non due) e **commissioni 3% contro 20%** in una frase che dice che le
  percentuali sono simili. Sono affermazioni verificabili quanto un prezzo, e sono quelle che un lettore
  esperto controlla a mente in dieci secondi.
- **Se la prova si rifà su dati copiati dall'articolo, la copia si rilegge prima di giudicare**: un
  elenco trascritto con due voci invertite produce un verdetto **falso** sui dati dell'articolo — è
  successo rifacendo la prova del `1883` sull'autocompletamento, corretto prima di finire nel rapporto.
  Ricontrollare la copia contro la pagina, e dichiarare nel rapporto **il metodo e i suoi limiti**.

## I link, uno per uno (e con l'URL preso dall'HTML)

**Il primo link rotto vero del sito è stato trovato così** (`221`: l'ancora *"l'AGCOM lo applica"* →
**404**, mentre la pagina madre risponde 200). Il plugin ne segnalava quattro, **tutti falsi positivi**, e
non segnalava questo. Due regole:
- **L'URL si copia dall'`href`, mai si ricostruisce a memoria**: un refuso mio (*guide-ai* invece di
  *guida-ai*) ha prodotto un 404 inesistente e una quasi-accusa sbagliata.
- **L'ancora si legge nella frase in cui sta**: i link interni con l'ancora fuori senso sono un difetto a
  sé (`222`: *"Sitemap"* → la guida *come creare un sito*; *"WooCommerce"* → *WordPress per principianti*;
  e nella **matrice di diagnosi** *"Google **Search Console**"* → la **guida all'IA per principianti**;
  `217`: *"studio"* → *WordPress per principianti*). Che l'URL risponda 200 non basta.

## Le etichette di generazione rimaste a video

`"Risposta diretta:"` ×8 nel `223` e ×5 nel `222`; `"Risposta rapida:"` ×6 nel `224`. **In `224` sono la
causa delle duplicazioni**: il riquadro e il paragrafo "risposta rapida" rispondono alla stessa domanda,
per questo le coppie identiche sono cinque. **Non è sistematico** (in `224` i riquadri non hanno etichetta),
quindi si contano e si dichiarano articolo per articolo.

## Lo stato in Google: tre livelli, e la conclusione è a livello di sito

I tre stati misurati con l'ispezione URL non sono equivalenti: `URL is unknown to Google` è peggio di
`Discovered – currently not indexed`, che è peggio di `Crawled – currently not indexed`. **La lettura
utile però è un'altra**: il `217` — l'articolo con i dati più accurati e verificati del sito — è stato
**scansionato il 24 settembre, un mese dopo la pubblicazione, e scartato lo stesso**. Quando anche
l'articolo migliore non passa, il problema **non è l'articolo**: le correzioni servono alla credibilità e
al lettore, non bastano a farsi indicizzare, e il rapporto deve dirlo con chiarezza.

## Verificare i dati dichiarati alla fonte

Molte cifre sono **vere e verificabili**: vanno controllate, non date per buone né sospettate a priori.

| Cosa | Dove si verifica |
|---|---|
| Installazioni, voti e date di aggiornamento di plugin e temi | **API di WordPress.org**: `/wp-json/wp/v2/plugins/info/1.2?action=plugin_information&request[slug]=…` e `…/themes/info/1.2?…` |
| Prezzi e condizioni di un servizio | **la pagina ufficiale**: confermati Shopify Basic 19 €/mese (annuale), SiteGround 2,99 €→15,99 €, Astra 69 $/anno e 279 $/vita, *"3 vendite qualificate in 180 giorni"* di Amazon |
| Provvedimenti di un'autorità italiana | **la pagina dell'autorità**: Garante (`docweb`), delibera **AGCOM 197/25/CONS** |
| Quote di mercato | **W3Techs** (WordPress 58,6%) |
| Vulnerabilità e punteggi di gravità | **NVD**: `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-…` (JSON: descrizione e punteggio) e **WPScan** per le estensioni |
| Leggi italiane | **Normattiva** (`urn:nir:stato:decreto-legge:2018-07-12;87` → l'art. 9 del Decreto Dignità sta nel Capo III sul gioco d'azzardo) |
| Requisiti e versioni di WordPress o PHP | **`wordpress.org/about/requirements/`** (PHP 8.3+, MariaDB 10.11+/MySQL 8.0+ — **cambiano: verificare, non ricordare**; le cifre vecchie restano solo come «legacy») e **`php.net/supported-versions.php`** per le date di fine supporto |
| Una campagna malware citata | la **guida della fonte citata** (Sucuri su AnonymousFox) e il **forum ufficiale di WordPress** |
| **Soglie, tempi, nomi delle colonne di un programma di affiliazione** | le **pagine di aiuto pubbliche** del programma: per Amazon `https://programma-affiliazione.amazon.it/help/node/topic/<ID>` — **non sono dietro login** (dietro il login stanno solo i dati dell'account). Verificato l'11/10/2026 sul `1854`: le soglie *«25 EUR (bonifico o buono regalo) o 50 EUR (assegno), commissioni cumulate con quelle del mese successivo»*, la definizione della colonna *Prezzo* (senza IVA per il retail, **con IVA per i venditori terzi**) e l'esempio dei centesimi (*7,50% → 7,49% o 7,51%*) sono **trascritti parola per parola dall'articolo**: la pagina ufficiale dice le stesse cose. **Le pagine `/help/` si leggono; solo il report dell'account no.** |
| **Se una frase esiste nella ricerca reale** (quando un articolo pubblica un test sulle parole chiave) | l'endpoint pubblico dell'autocompletamento: `https://suggestqueries.google.com/complete/search?client=firefox&hl=it&gl=it&q=<frase>` (JSON: `[0]` = query, `[1]` = suggerimenti). **Attenzione al metodo — vedere la famiglia 18.** |
| **Fisco e previdenza italiana** | le fonti primarie, mai un blog: la **scheda informativa INPS** (riporta le regole verbatim — la franchigia dei 5.000 € è scritta così), le **circolari INPS per numero e data** (la n. 8 del 03/02/2026 conferma l'aliquota della Gestione Separata al **26,07%**), la **scheda Agenzia delle Entrate** del forfettario (85.000 € di ricavi, 20.000 € di spese di lavoro dipendente, sostitutiva 15% → 5% per i primi cinque anni, uscita dall'anno stesso sopra 100.000 €), la **struttura ATECO 2025 dell'ISTAT** per sapere se un codice esiste ancora, le tabelle dei **coefficienti di redditività** per il coefficiente del codice (73.11 → **78%**) |
| **Testi di legge** | **Normattiva** per il decreto e **Brocardi** per l'articolo del TUIR o del codice civile (art. 67 c.1 lett. l) TUIR, art. 2222 c.c.): si cita la lettera, non il riassunto. Un articolo che dà consigli fiscali si verifica **tutto**, e il verdetto si scrive anche quando ha ragione su ogni riga |
| **Le clausole di un contratto di piattaforma** | **il contratto stesso**: Amazon pubblica Operating Agreement e Program Policies su `/help/operating/agreement` e `/help/operating/policies`, e le clausole si ritrovano **parola per parola** (*«material breach»*, *«fail to cure within 7 days»*, *«deemed a material breach»*, *«significant commentary, analysis, or transformation»*, l'esempio 64/128 GB, il 15% abbigliamento, la lista dei siti non idonei, i refusi *«ammazon»/«amaozn»/«kindel»*, *«Creators API or PA API»*, *«we have never authorized… paid set-up or consulting services»*). **Confronto clausola per clausola**: quando l'articolo cita un contratto, la trascrizione fedele è verificabile — e il secondo lettore può contestare come errore quello che è invece il testo ufficiale |
| **Un comportamento del core di WordPress** | **il codice sorgente**: `raw.githubusercontent.com/WordPress/WordPress/master/wp-includes/<file>.php`. Caso modello: `wp_is_maintenance_mode()` in `load.php` restituisce `false` quando il timestamp di `.maintenance` è più vecchio di **10 minuti** — quindi un `.maintenance` dimenticato **non** bloccal sito per giorni, lascia solo l'avviso di aggiornamento fallito in bacheca. Guide e documentazione lo raccontano in modo approssimativo: **sul comportamento la fonte è il codice** |
| **Versioni, annunci e requisiti di WordPress** | `wordpress.org/documentation/article/updating-wordpress/` (contiene il passaggio **«Step 1.5: Remove .maintenance file»** e il *«you don't have to lift a finger»* del 3.7), le **dev note su `make.wordpress.org/core`** per sapere quale versione ha introdotto una funzione, `wordpress.org/about/requirements/` per PHP e database (8.3 · MariaDB 10.11/MySQL 8.0) |
| **Un paper, uno strumento ritirato, una norma europea** | l'**abstract su arXiv** per titolo esatto e autori; **la pagina del fornitore** per un prodotto dismesso (OpenAI: 26% di veri positivi, 9% di falsi positivi, *«As of July 20, 2023… no longer available due to its low rate of accuracy»*); **`artificialintelligenceact.eu`** per il testo di un articolo e le sue **date di applicazione** (art. 50: dal **2 agosto 2026**, adeguamento fino al **2 dicembre 2026** per i sistemi già immessi sul mercato) — le date degli obblighi cambiano con gli omnibus: **verificarle, non ricordarle** |

**Non verificabile dall'automazione** (segnalare come "da controllare a mano", non come difetto):
**Reddit** (il thread risponde anche **200** ma è il guscio JavaScript: il contenuto non si legge — e
**non si legge non è «inventato»**: un thread citato che non si riesce ad aprire si dichiara *non
verificato*, mai falso, e la sua esistenza si controlla per altra via, con una ricerca), **WordPress.com**,
**Wordfence**, **Aruba**, **Keliweb** (pagine JS o blocco scraper).

**Correzione dell'11/10/2026 — Amazon non è in questo elenco.** Il `1603` era stato chiuso con le soglie
di pagamento dichiarate *"non verificabili da qui"*: era sbagliato, le **pagine di aiuto sono pubbliche**
e leggibili (riga in tabella qui sopra). Prima di scrivere "non verificabile", **provare l'URL ufficiale**
— la riga "dietro login" vale per i dati dell'account, non per la documentazione del programma.

## Le famiglie di difetti che ripagano sempre (cercarle in ogni articolo)

1. **Duplicazione riquadro→paragrafo** — il difetto n. 1 del sito (§ sopra).
2. **Numeri**: ricalcolo, totali, unità, coerenza con l'esempio (§ sopra).
3. **Attribuzioni anonime** — *"su Quora la risposta di chi lo fa di mestiere"*, *"gli esperti dicono"*:
   trovate su `209`, `210`, `211` (×4), `212`, `219`. **Ogni citazione vuole nome e link.**
4. **Promesse non mantenute** — rinvii a contenuti che non esistono o che non dicono quello che
   l'articolo promette (`208` sui permessi, `210` sulla "cura del sito").
5. **Contraddizioni interne** — due soglie diverse per la stessa cosa (`219`: "30-50 articoli" contro
   "una ventina"; "due-tre a settimana" contro "uno o due"). E la forma più insidiosa, **una regola
   dichiarata e poi disfatta due sezioni dopo**: `1412` mette i **Contatti** tra le voci da primo livello
   e poi li manda nel footer; `1441` scrive *"la regola da ricordare è una sola: il CNAME non si usa sul
   nome principale del dominio"* e due sezioni dopo consiglia *"oppure con un CNAME"*. **Tenere a mente le
   regole già date e confrontarle con quelle successive** — è il controllo che ha trovato Gemini in
   entrambi i casi e che nessun conteggio automatico fa.
6. **Struttura contro schema** — le FAQ sparse fuori dall'H2 mentre lo schema `FAQPage` le dichiara
   tutte (`219`): il markup può essere valido e la pagina no.
7. **Tre intenti in conflitto** — slug ≠ H1 ≠ title (`219`: "cos'è" / "come nasce" / "come guadagnare").
8. **E-E-A-T dell'autore** — H3 col nome dentro il corpo, ruolo "nerd", avatar predefinito, social del
   footer a `#`, nessuno screenshot reale, nessuna didascalia.
9. **Cannibalizzazione da cluster** — articoli che coprono lo stesso perimetro e si linkano in cerchio
   (`204`↔`212` sull'hosting; `214`/`215`/`219`/`221` sull'affiliazione).
10. **`nofollow` sulle fonti autorevoli** (ISTAT, Commissione europea, MDN, NIST, documentazione
    WordPress) e **`rel="sponsored"` mancante** sui link affiliati. **Il sito è incoerente**: `226` e
    `227` hanno `nofollow` su tutte le fonti, `1412` e `1441` non ne hanno nessuno (solo `noopener`).
    Il difetto non è il singolo articolo, è la regola mancante: va dichiarato come uniformità da fare.
11. **Fonti, dataset e credenziali inventati** — il difetto più grave trovato finora, e non isolato:
    `222` (*"Fonte: dataset del sito, 2024 (n=50.000 siti)"*, *"correlazione sito + Google Webmaster
    2024"*), `223` (*"Dati benchmark Kinsta/WP Engine 2024 (n=10k siti)"*, *"WordPress Hosting Perf
    Survey 2024"*, *"WordPress Backup Best Practices 2024"* — che non è una fonte ma un titolo), `224`
    (*"elaborata dal **team di specialisti del sito**"*, con un solo autore anonimo). Cercare in ogni
    articolo `Fonte:`, `(n=…)`, `team`, `i nostri esperti`, `abbiamo analizzato/testato` e **verificare
    che esistano**. Spia dell'invenzione: **un nome morto** (*"Google Webmaster"* → Search Console dal
    2015). È l'unica famiglia che da sola può portare il contenuto alla valutazione peggiore di Google:
    va **segnalata per prima**, non in fondo all'elenco.
12. **Il numero promesso contro quello elencato** — `215` tre criteri→quattro, `216` tre errori→cinque,
    `218` tre cose→quattro (e otto righe di tabella), `221` tre→quattro *senza una voce in comune*,
    `222` "i 16 errori"→9 righe di matrice, `223` "tutti gli 8"→6, `217` "10 strumenti"→quindici
    trattati. Vale anche dentro un'infografia (`224`: "Hardening 8 step" che ne elenca 6).
    **Contare le voci, sempre.** E contare **quanti numeri diversi descrivono lo stesso elenco** nella
    stessa pagina: nel `1412` la stessa verifica è annunciata come *"quattro controlli"*, riassunta in
    **7** punti e poi sviluppata come *"i dieci controlli"* (che sono dieci, corretti); le voci di primo
    livello sono *"massimo 5-7"*, *"sette al massimo"*, *"da quattro a sette"*. Nel `1441` *"Quattro
    errori coprono quasi tutti i casi"* e sotto ne elenca **sei**. Anche le affermazioni indirette: una
    tabella non può dire "Non esiste" se il testo dice "può non esserci" (`1441`).
13. **Intestazione vuota e blocco fuori posto** — un H2/H3 senza corpo, con il suo testo finito sotto la
    sezione successiva: `220` (le "3 domande" sotto l'H2 dell'IA agentica), `217` (l'H3 "Make" vuoto,
    testo sei paragrafi dopo), `218`, `221` (due volte in un articolo), `223` (il test del ripristino
    sotto la sicurezza, l'isolamento PHP sotto il WP-Cron). **L'H3 vuoto è anche una trappola della
    conversione** (§Trappole): si dichiara solo dopo aver visto che **nell'HTML quel titolo non ha
    davvero un paragrafo sotto**, e che il testo esiste sotto un'altra intestazione. **Aggiornato
    l'11/10/2026: sono nove casi**, si aggiungono `225` (l'H2 «La cache»), `226` (due), `1412` (l'H2
    sulla personalizzazione del menu) e `1441` (l'H2 «Come si verifica che il DNS sia corretto?»).
    **È il difetto più frequente del sito: cercarlo in ogni articolo**, e quasi sempre il testo esiste
    sotto la sezione successiva (quindi la correzione è uno spostamento, non una scrittura).
14. **La frase troncata** — un pezzo di frase senza proposizione principale lasciato nel testo (`224`,
    conclusioni: *"Per chi desidera liberarsi dalla complessità della manutenzione tecnica affidandosi a
    un'infrastruttura con firewall gestito, audit continui e SLA di ripristino garantiti."*). Le
    conclusioni si leggono **per ultime**, ed è lì che i modelli troncano.
15. **Lo stesso fenomeno con due numeri diversi nella stessa pagina** — `224`: l'infografia dice
    *"brute force 43%, plugin 27%"* (vertice: brute force) e la Tabella 1 dice *"plugin 78%"* (vertice:
    plugin), mentre il testo due paragrafi dopo dà ragione alla tabella. Due classifiche incompatibili
    degli stessi dati convivono senza che nessuno le abbia confrontate.
16. **L'articolo che misura sé stesso: i numeri esatti, il dettaglio tecnico falso** — `1412` scrive
    *"il blocco di navigazione della home occupa **3.130 byte**, contiene **3 voci di primo livello**
    (Glossario, Documentazione, Contatti), **nessuna immagine** ... gli attributi ARIA sono **5**:
    aria-label, **aria-expanded e aria-controls**"*. Verificato sulla home: 3.130 byte **esatti**, 3 voci
    **coi nomi esatti**, 0 immagini, la stringa citata (`responsive-container-open`) esiste — **ma
    `aria-expanded` e `aria-controls` valgono ZERO in tutta la pagina**, e nel blocco non c'è nessun
    sottomenu. La misura facile è esatta; **la parte tecnica che l'articolo indica come modello da
    copiare è inventata**. **Verificare voce per voce ogni misura che un articolo dichiara del proprio
    sito** (`1441`: i 13 root server sono davvero 13, confermato da IANA — verificare e confermare fa
    parte del lavoro, non solo smentire). È l'unica famiglia in cui l'articolo si autodenuncia, e un
    lettore esperto la controlla in trenta secondi.
17. **I campi dello schema `HowTo` stampati a video** — `PT2H` nel `222`, `PT10M` nel `1412` e nel
    `1441`: **tre articoli su tre** con la sequenza numerata. Non è un refuso editoriale, è **il template**
    che rende il campo `duration` senza convertirlo ("PT10M" invece di "10 minuti"). Cercare `PT` nel
    testo reso di ogni articolo con la sequenza numerata, e correggere **una volta nel template**
    (§Prima di correggere: dov'è la causa).
18. **Le prove di prima mano non riproducibili** (nuova famiglia, 11/10/2026). Il `1883` è il primo
    articolo del sito che pubblica **test propri con numeri** — la direzione giusta — ma dichiara solo
    *"un modello di fascia normale, non il più potente"* e non riporta **i prompt**. **Senza modello,
    versione, data e testo delle richieste la prova non si può rifare: vale come anestesia, non come
    prova.** Cercare sempre, in un articolo che porta un test: il nome del modello, la versione, la data,
    i prompt, i dati grezzi. Fare la stessa domanda all'E-E-A-T (§famiglia 8) ma **sui dati**, non
    sull'autore.
    **Corollario — se l'articolo insegna un metodo, il metodo si prova.** Il `1883` insegna a verificare
    una parola chiave *"digitando le prime due o tre parole"* nei suggerimenti di Google; rifatta la sua
    prova sulle stesse 20 frasi con l'endpoint pubblico, delle **7 che dichiara esistenti ne confermo 5**
    e delle **13 che dichiara "mai cercate" 4 compaiono davvero**. Il difetto è strutturale: digitando
    solo la radice escono le estensioni più generiche, non la frase in esame — **si digita la frase
    intera**. Limiti da dichiarare sempre: l'endpoint pubblico **non è identico** al box dal vivo, dipende
    dalla personalizzazione e **dal prefisso** (`backup database wordpress` non compare con due parole e
    compare con tre). Quindi non si scrive "l'articolo mente": si scrive **"il numero non è
    riproducibile"**, col metodo e i limiti accanto.
19. **La conclusione che contraddice la prova** (nuova famiglia, 11/10/2026). Il `1883` dimostra che
    **con l'elenco delle pagine** l'IA azzecca i link interni (*"tre su tre corretti, e anche utili"*) e
    poi conclude *"Link interni: no… l'IA non serve per link"*: la sintesi cancella la condizione che la
    prova aveva appena dimostrato essere decisiva. **Leggere sempre "In sintesi" e "Risposta breve"
    contro il corpo**, e cercare la condizione che sparisce ("con l'elenco", "se il plugin è aggiornato",
    "solo sul piano gratuito"). È il gemello rovesciato della famiglia 5.

20. **L'omissione di quello che la fonte già dice** (nuova famiglia). Quando un articolo si appoggia a
    un documento, a una norma o a un contratto che **cita e linka**, il confronto non finisce in «quello
    che dice l'articolo è vero»: si chiede anche **cosa dice la fonte che l'articolo non riporta**, ed è
    lì che stanno le lacune che costano al lettore. Casi modello: un articolo sulle cause di chiusura
    dell'account Amazon che non nomina **la dichiarazione di affiliazione obbligatoria**, **gli
    auto-acquisti** e **la regola delle tre vendite in 180 giorni**, pur citando il contratto che le
    prevede; uno sul regime fiscale che non nomina **la marca da bollo da 2 €** sulle ricevute sopra
    77,47 € né lo **scenario a contributi fissi** (ditta individuale → Gestione Commercianti); uno su
    WordPress che indica il ripristino via FTP e non la **modalità di recupero** nativa (l'email che
    disattiva il plugin colpevole senza toccare i file); uno sui prompt che non riporta **il few-shot**,
    cioè la regola che la pagina del fornitore che lui stesso linka insegna. **Variante normativa:
    l'eccezione che l'articolo non nomina** (un obbligo di legge presentato come generalizzato, quando la
    norma prevede un'esenzione). Procedura: **aprire la fonte citata e leggerne l'indice**, e per ogni
    sezione che riguarda l'argomento chiedersi se l'articolo la copre. Queste lacune vanno **in cima al
    piano di correzione**: un articolo che tace la causa più comune fa più danno di uno che sbaglia un
    numero.

**Un difetto trovato in un articolo ha spesso la correzione in un altro**: il `214` non dice
`rel="sponsored"`, il `219` lo spiega con il link alla documentazione Google. La tabella delle
**correzioni incrociate** va tenuta nell'`00-INDICE.md`, ed è la ragione per cui la verifica si fa per
articoli collegati e non in ordine alfabetico.

## Prima di correggere: dov'è la causa

- **Nel contenuto salvato o nella resa?** `content/get-post` mostra il contenuto vero. Un
  `<div class="direct-answer-box">` con la frase ripetuta sotto è nel testo → si corregge scrivendo.
  Un `class="mw-glossary-term"` con `data-mw-glossary-*` è **generato dal plugin** (auto-linking del
  glossario) → si corregge nella lista dei termini, **una volta per tutto il sito**.
- **Cercare le classi che tradiscono il generatore** nell'HTML (`direct-answer-box`, `mw-glossary-term`,
  `mw-updated-label`) prima di scrivere qualunque piano: se il difetto nasce lì, **una correzione sola
  vale per tutti gli articoli**, e il rapporto deve dirlo — altrimenti si prospettano 45 lavori
  editoriali dove ne basta uno.
- **Misurare la portata su tutti gli articoli** prima di dichiararla: difetti identici in due articoli
  possono essere limitati a un lotto di pubblicazione e non riguardare il resto del sito.
- **Le stringhe di tema non tradotte** ("Updated on", "Table of contents") sono di piattaforma: si
  correggono una volta e valgono per ogni pagina.

## La forma del rapporto (quella accettata)

1. **Tabella di testa**: URL, date, **stato in Google**, verdetto in due righe.
2. Il **difetto principale in evidenza**, poi gli altri in tabella con la frase esatta e il punto in cui sta.
3. **"Le accuse che NON reggono"**: le verifiche respinte, ognuna con la prova. È la parte che dimostra
   che il lavoro è stato fatto davvero (e vale anche per le mie imprecisioni: dichiararle).
4. **Punti forti** onesti — se un articolo è buono va detto, e diventa il metro per gli altri.
5. **Piano di correzione per priorità** (alta/media/bassa, con il tipo di intervento) e una riga
   **"da non toccare"**.
6. **Perché è o non è in indice**, con le ipotesi dichiarate come ipotesi (quelle di Google non sono
   verificabili: budget di scansione, autorità, saturazione del tema).

## Cosa non fare

- Non mandare al valutatore un digest prodotto da uno script, e non spacciare per "la pagina" un testo a
  cui hai tolto struttura, immagini, link e meta.
- Non riportare un difetto di formattazione che non hai verificato sull'HTML (tabella incollata, H1
  doppio, menu doppio, FAQ "muro di testo", entità non decodificate: nascono tutte dalla conversione).
- Non dedurre lo stato di indicizzazione da un campione: Google si interroga per ogni URL.
- Non dichiarare la portata di un difetto senza averlo contato sul sito.
- Non applicare correzioni: il rapporto le propone, l'autore le autorizza.
