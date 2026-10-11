# Verifica di una **bozza** non pubblicata (audit delle bozze)

Lavoro diverso sia dalla scrittura sia dall'audit dei pubblicati. Si legge, si verifica, si propone:
**nessuna modifica alla bozza**, nessuna scrittura, solo rapporti.

## Cosa cambia rispetto agli articoli pubblicati

| Pubblicato | Bozza |
|---|---|
| c'è lo stato su Google (indice, scansione, sitemap), la pagina resa, il template | l'indirizzo risponde **404**: niente indice, niente pagina resa. Al posto dello stato si verifica la **prontezza alla pubblicazione** |
| contano contenuto, schema, meta, resa | contano soprattutto i **campi** (sotto) e i **numeri** |

**Le stringhe inglesi del tema e i marcatori dei blocchi non si valutano.**
- Le etichette del tema (`Activate dark mode`, `Updated on`, `Comments`) e le intestazioni vuote del box
autore sono **del tema**, non della bozza.
- I marcatori dell'editor (`[RIQUADRO]`, `[CITAZIONE]`, `[IMMAGINE — alt: …]`, `[CODICE]`,
`[FAQ — schema: attivo]`) sono i **blocchi del sito**: in pagina vengono resi. Una conversione in testo
li mostra grezzi, e una tabella Markdown perde la riga dei separatori e guadagna un `|` orfano: sono
**artefatti della conversione**, non difetti. Idem per un `alt` che sembra troncato: la conversione lo
taglia, il sito no. **Non riportarli** come problemi.

## I campi da verificare, sempre

| Campo | Atteso | Come si sbaglia |
|---|---|---|
| **Estratto** (`excerpt`) | presente e **di questo articolo** | è il campo più trascurato: può contenere il testo di **un altro** articolo, o essere **vuoto**. È quello che si legge nei risultati e nelle anteprime social: vuoto o sbagliato è un difetto vero |
| Titolo SEO | ≤ 60 caratteri | è già stato trovato a **61** (uno oltre) |
| Description | 120-160 | è già stata trovata a **160 esatti** (al limite) |
| Slug | piatto, senza prefissi | — |
| Immagine in evidenza | presente, con alt descrittivo | — |
| Blocco FAQ | schema attivo se le domande ci sono | nelle bozze è il blocco a generare `FAQPage`; **lo `HowTo` degli articoli pubblicati non c'è** |
| Link interni ed esterni | 200 | un 403 esterno è un blocco anti-bot, non un link rotto; un 202 è il risolutore DOI |

Il controllo dei link si fa **in un passaggio su tutte le bozze insieme**: si estraggono gli indirizzi da
tutti i testi, si deduplicano, si interrogano una volta ciascuno. È il controllo che trova subito un link
sbagliato che si ripete in più bozze.

## I numeri sono il cuore

Tre conteggi da rifare **sempre**, con la calcolatrice, non a occhio:
1. **I conteggi di struttura**: sezioni, passi, voci di tabella, domande frequenti. Un articolo che apre
   con «tre punti» e ne svolge sette è un difetto, non una licenza.
2. **L'aritmetica interna dell'articolo**: percentuali, rapporti, differenze. «129 volte di differenza,
   1,2 contro 154,9» → 154,9/1,2 = 129,08. «Da 0,138 a 0,121 → 17 ms». «124 − 100 = 24 query».
3. **Le parole di un testo citato come esempio** quando la bozza ne dichiara il numero: un campione
   presentato come «160 parole, dentro i limiti» ne aveva **145**, cioè sotto il minimo che la bozza
   stessa chiedeva. Contare con una regex che include apostrofi e accenti, non con `wc -w`.

## Le prove di prima mano vanno rifatte

Quando la bozza dichiara metodo, strumento e numeri, la si riprova. Casi già riprodotti così:
- **servizio pubblico di immagini senza account**: le prime richieste arrivano, poi **402** su tutte —
  il conteggio delle immagini concesse varia, il comportamento no;
- **montaggio da foto con `ffmpeg`**: 6 immagini × 4 s meno 5 dissolvenze da 0,5 s = **21,5 s** (la durata
dichiarata torna); e la trappola del movimento è **vera e facile da prendere**: con l'immagine ripetuta in
ingresso (`-loop 1`) più `zoompan`, il video da 21 secondi esce lungo **minuti** (riprodotto: 8 minuti e 46
secondi). Con `zoompan d=1` per immagine la durata resta quella giusta;
- **traduttore automatico**: la frase tradotta si riproduce identica interrogando l'endpoint pubblico;
- **le immagini del sito** citate come materiale di partenza: verificare che rispondano 200.
- **conteggi sul sito**: per «quanti articoli» o «quanti link in uscita» si rifà il conto su **tutti** i
contenuti pubblicati, non su un campione dichiarato dalla bozza. Un conteggio fatto su un numero vecchio
di articoli non è confrontabile, e va detto **cosa** si è contato (corpo dell'articolo o pagina intera):
la differenza fra i due metodi è di **tre volte** su alcune voci.

## Verificare le citazioni, non i link

**Un link che risponde 200 non dimostra niente sulla frase che gli viene attribuita.** Le tre tecniche
che hanno funzionato:

**Forum italiano di WordPress** (`it.wordpress.org/support/topic/<slug>/`):
```bash
curl -sL -A "Mozilla/5.0" "https://it.wordpress.org/support/topic/<slug>/" -o /tmp/q1.html
# poi in Python: togliere <script>/<style>, togliere i tag, unescape delle entità,
# normalizzare apostrofi tipografici (’ → '), virgolette curve e \xa0, comprimere gli spazi
# e cercare la frase citata in minuscolo.
```
Trappole: una ricerca letterale **fallisce per le entità HTML** (accenti e apostrofi arrivano come
`&#8217;`), quindi se non si trova al primo colpo si allarga a un frammento più corto prima di dichiararla
assente. E la citazione spesso sta su **`/page/2/`** mentre la bozza linka pagina 1: guardare sempre anche
la seconda pagina. **Attribuire la citazione al nome di chi l'ha scritta**: una frase presentata come «un
utente» è quasi sempre attribuibile, e una citazione corretta in silenzio (refuso dell'utente corretto
senza dirlo) va segnalata.

**Fonti che bloccano l'automazione** — al posto di un valore ricordato si usa la **copia canonica** dello
stesso contenuto:
| Serve per | Dove |
|---|---|
| fatti sul core di WordPress | `raw.githubusercontent.com/WordPress/WordPress/master/wp-includes/...` |
| requisiti, costanti, riparazione | documentazione ufficiale (`developer.wordpress.org`, `wordpress.org/documentation`) |
| un paper | `arxiv.org/abs/<id>`: titolo e autori **esatti**, e il prefisso dell'id data l'invio (es. `2509…` = settembre 2025) — serve a confermare una data di pubblicazione quando la pagina del fornitore non si legge |
| una sentenza o un caso | riassunto REST di Wikipedia: `/api/rest_v1/page/summary/<Titolo>` |
| documentazione MySQL/MariaDB | `mariadb.com/kb/en/...` (leggibile dove `dev.mysql.com` può non esserlo) |
| pagine di assistenza dei fornitori | riprovare nel **browser reale** con attesa lunga (vedi skill `blocked-page-recovery`) |

**Se la fonte non si legge**: nel rapporto si scrive **«non verificato»**, mai il valore plausibile al suo
posto. È la stessa regola dell'autore applicata alle fonti invece che ai contenuti.

## Il secondo lettore (Gemini via `agy`)

Alla bozza si manda **il testo intero**, con un preambolo che: vieta l'uso di strumenti e la ricerca sul
web; elenca **tutto quello che ho già verificato** (così non lo rifà e non lo contesta); impone di scrivere
**«DATO MANCANTE»** invece di inventare; chiede un verdetto di pubblicabilità. Il materiale inviato si
salva accanto al rapporto (`<id>-materiale-inviato-a-gemini.md`) e la risposta in `<id>-gemini-revisione.md`.

**Poi si verifica ogni accusa, una per una.** Il secondo lettore trova errori veri che la lettura a mano
non vede, e insieme produce accuse sbagliate. Due categorie da respingere senza esitare:
1. **Artefatti della conversione in testo** (marcatori dei blocchi, `|` orfani, alt «troncati», tabelle
   «malformate»): non esistono in pagina.
2. **Accuse su un dato che ho già letto alla fonte primaria**: se la pagina ufficiale dice «10 al giorno»,
   l'accusa «sono 10 al mese» si respinge **citando la fonte**, non si media.
Nel rapporto le accuse respinte si scrivono **come respinte**: evita che il lettore successivo le rilitighi.

## I difetti che ricorrono in tutte le bozze

Cinque schemi, da cercare per primi perché si correggono una volta e valgono per tutte:
1. **Chi promette replicabilità non dà gli strumenti**: dice «in un comando» e il comando non c'è; non
   nomina i modelli, i servizi o i plugin provati. Senza quelli la prova non è replicabile — ed è il
difetto più facile da correggere e quello che vale di più.
2. **Manca il capitolo per chi monetizza**: uso commerciale dei contenuti generati, trasparenza
   pubblicitaria italiana (Codice del Consumo, AGCM, IAP), dicitura del programma di affiliazione,
   allucinazioni su schede tecniche e prezzi. Su un blog di affiliazione è il buco che pesa di più.
3. **Il testo contraddice i propri numeri**: la sintesi dice una cosa e il corpo un'altra; l'apertura
   promette «tre» e l'articolo ne svolge sette; l'alt di un'immagine dice 15 dove la tabella dice 18.
   Stessa famiglia della verifica contenuto-vs-schema: **leggere la sintesi contro i dati**.
4. **Numeri vecchi o presi dalla fonte sbagliata**: conteggi fatti su un numero di articoli superato,
   soglie attribuite al posto di quelle giuste (controllare la soglia sulla pagina che la pubblica).
5. **Campi SEO da sistemare**: estratto vuoto o di un altro articolo, titolo oltre 60, description a 160.

**Il difetto tecnico più grave da cercare**: le istruzioni che **non funzionano** per chi legge. Esempio
verificato: mandare a riparare le tabelle da phpMyAdmin quando le tabelle di WordPress sono **InnoDB**, e
`REPAIR TABLE` copre solo MyISAM, Aria, Archive e CSV. Ogni istruzione va controllata contro il motore, la
versione e lo strumento che il lettore ha davvero — non contro l'idea generale.

## Forma del rapporto

Un file `.md` per bozza, nella **cartella dei rapporti sul Desktop** (non nel repo del progetto) e in una
cartella separata da quella degli articoli pubblicati, più un indice con il tracker e il bilancio
trasversale. Struttura che ha funzionato:
1. intestazione: **verificata il …, lettura integrale a mano, stato «BOZZA (404)»**;
2. riquadro dei campi (titolo SEO con il numero di caratteri, description, slug, estratto);
3. **Verdetto** in 2-4 righe: cosa regge, cosa va corretto prima di pubblicare;
4. **Verificato alla fonte**: una riga per dato, con la fonte e l'esito;
5. **I difetti**, numerati, ognuno con la marca di chi l'ha trovato e verificato (`✅ mio`, `✅ secondo
   lettore`, `❌ respinta`);
6. **Punti forti**: cosa non va toccato e perché;
7. **Piano di correzione**: priorità (altissima/alta/media), tipo (errore tecnico, contraddizione,
   omissione, rigore, editoriale);
8. **Da non toccare**: l'elenco esplicito, così chi corregge non smonta quello che funziona.

**In chat: righe puntate, nessuna tabella.** Le tabelle stanno nel file; la sintesi serve a decidere cosa
aprire.
