# Verifica di una **bozza** non pubblicata (audit delle bozze)

Lavoro diverso sia dalla scrittura sia dall'audit dei pubblicati. Si legge, si verifica, si propone:
**nessuna modifica alla bozza**, nessuna scrittura, solo rapporti. **La correzione è una fase separata**,
che si apre solo quando l'autore la chiede: procedura in fondo a questo file.

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

Sei schemi, da cercare per primi perché si correggono una volta e valgono per tutte:
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
6. **La promessa di metodo non mantenuta**: l'articolo si presenta come il più aggiornato o il più
trasparente («quello che non ho potuto verificare l'ho scritto») e poi dà per fatti numeri, date e
comportamenti che non ha verificato. Ogni volta che una bozza dichiara un metodo — nomina i modelli, dà il
comando, dichiara i limiti — si controlla che lo mantenga **in tutto il corpo**: i dati non verificati si
dichiarano come tali, non si coprono con una frase di stile. Su un contenuto che insegna a fidarsi delle
fonti è il difetto che pesa più di tutti, ed è anche il più facile da chiudere (due righe di dichiarazione).

**Il difetto tecnico più grave da cercare**: le istruzioni che **non funzionano** per chi legge. Esempio
verificato: mandare a riparare le tabelle da phpMyAdmin quando le tabelle di WordPress sono **InnoDB**, e
`REPAIR TABLE` copre solo MyISAM, Aria, Archive e CSV. Ogni istruzione va controllata contro il motore, la
versione e lo strumento che il lettore ha davvero — non contro l'idea generale.

## Applicare le correzioni (fase separata, su richiesta dell'autore)

La verifica **non tocca niente**: produce rapporti. La **correzione** è un lavoro diverso, che si fa quando
l'autore lo chiede, e ha regole sue. Vale la regola generale delle scritture: si resta in **`draft`**, mai
pubblicare. **L'ok dell'autore copre le modifiche di quel giro su quelle bozze** — contenuto, campi, titolo
SEO — e vale per tutte quando dice di procedere senza fermarsi; **non copre il cambio di stato**, che resta
una decisione sua.

**Procedura provata**, una bozza per volta nell'ordine del calendario:
1. **Si legge solo il «Piano di correzione»** del rapporto (più la riga «Da non toccare»), non tutto il
   rapporto da 8-9 KB: le correzioni sono elencate lì, con priorità e tipo. Se un punto cita un dato che non
   ho (il link di una fonte, il titolo di un caso), si cerca **quel** dato — non si inventa e non si salta.
2. **Si prende il contenuto grezzo**: `curl -u "$WP_USER:$WP_APP_PASSWORD" -s "…/wp/v2/posts/<id>?context=edit"`
   e si legge `content.raw` (**non** `content.rendered`: l'HTML dei blocchi si modifica solo sul grezzo).
3. **Sostituzioni mirate** sull'HTML dei blocchi, una per correzione, **verificando che ognuna sia stata
   trovata** (un `if a not in nuovo: print("❌")` per ogni sostituzione). **Una sostituzione non trovata è un
   errore bloccante: si risolve prima di riscrivere**, mai spedire il contenuto con una correzione applicata a
   metà — le altre passano e quella no, e il difetto resta in pagina mentre il rapporto dice «corretta». Due
   regole che rendono l'aggancio affidabile:
   - **L'aggancio si prende dal testo grezzo, mai dal testo pulito.** Il testo letto senza tag non esiste nel
     contenuto: dentro celle di tabella, voci di elenco, grassetti e link le frasi sono **spezzate dai tag**,
     quindi una frase che si legge intera in pagina non si trova intera nell'HTML. Prima di scrivere la
     sostituzione si stampa la **finestra di grezzo** attorno al punto
     (`repr(raw[max(0,m.start()-300):m.end()+300])`) e si copia da lì.
   - **Prima di sostituire una frase, controllare se è anche un titolo.** `re.findall(r'<h2[^>]*>(.*?)</h2>', raw)`
     dà l'elenco delle sezioni. Il testo di un `<h2>` è una stringa come le altre: un aggancio troppo generico
     lo sostituisce e **la sezione si perde** (ne resta il corpo, senza titolo). Dopo la scrittura **l'elenco
     dei titoli si ricontrolla** insieme al contenuto, ed è il controllo che accorge di un capitolo smontato.
   Se la stringa non combacia ancora (spazi, `\n` fra i commenti di blocco, entità HTML) si isola un frammento
   più corto e più vicino al tag, mai si prosegue «a occhio».
4. **Si riscrive passando solo i campi cambiati** — `{"content": …, "excerpt": …}` — con il corpo JSON
   scritto **su file con `json.dumps`** e inviato con `--data-binary @file`: inline si rompe su apostrofi e
   virgolette.
5. **Si rilegge dal sito** e si verifica **ogni singola modifica**: una riga di esito per correzione
   (c'è la frase nuova, non c'è più quella vecchia) più `status == "draft"`.
6. **Un numero cambiato cambia in tutti i posti in cui vive.** Un conteggio sta nel corpo, nella tabella,
   nel riquadro di sintesi **e** nelle risposte frequenti: aggiornarne uno solo lascia il resto incoerente.
   La prova d'accettazione è la **ricerca del valore vecchio** nel contenuto grezzo riletto: finché compare,
   la correzione non è finita. E quando il numero viene rimisurato, nel testo entrano **il metodo e la data**
   (es. «contati nell'HTML salvato, solo link in uscita, 45 articoli»): metodi diversi danno numeri diversi, e
   senza la dichiarazione il lettore non può rifare il conto.
   Vive anche **fuori dall'articolo**, in tre posti che si dimenticano: il **titolo**, che esiste **due
   volte** — quello del post e quello SEO dell'abilità `update-post-seo` — e correggerne solo uno lascia
   sbagliato proprio quello che si vede in SERP; la **description SEO**, che ripete spesso lo stesso numero
   (si corregge dall'abilità `update-post-seo`, non dal contenuto); e le **frasi-riassunto che ricalcolano una
   riga**.
   Correggere una riga di tabella obbliga a rifare anche il totale che la riassume: altrimenti resta
   l'incoerenza fra il dettaglio giusto e la sintesi sbagliata, che è il punto da cui parte la sfiducia.

7. **Alla fine del giro, un controllo unico su tutte le bozze toccate**: si leggono insieme
   (`…/wp/v2/posts?include=<id,id,…>&status=draft&context=edit&_fields=id,status,title,modified`) e si
   verifica che siano **tutte in `draft`** e tutte toccate. Dimostra in una riga che il giro non ha
   pubblicato niente per sbaglio, e con quindici bozze è il solo controllo che si legge davvero.

**Nel rapporto la correzione si segna.** A lavoro fatto si aggiunge in testa al rapporto, subito sotto il
titolo, una riga `> **✅ CORRETTA — <data>.**` con l'elenco in sintesi di cosa è stato applicato e di cosa
resta (le voci editoriali, i punti che aspettano una risposta dell'autore). Due motivi: l'indice delle bozze
dice a colpo d'occhio quante ne restano e quali, e il giro successivo sa cosa è già stato fatto senza
rileggere il rapporto intero. È una richiesta esplicita dell'autore, non un abbellimento.

**Due trappole di markup, verificate.** Aggiungere una frase dentro un grassetto o un link già aperto produce
markup annidato (`<strong>… <strong>…</strong> …</strong>`): si chiude il tag prima, o si scrive fuori. E se la
correzione tocca **titolo o description SEO**, si passa dall'abilità `update-post-seo` **dopo aver letto lo
schema con `get-ability-info`**: i campi si chiamano `title` e `description` (non `seo_title`) e `post_id` è
obbligatorio — indovinare il nome del campo fa fallire la chiamata senza spiegare perché.

**Le voci editoriali restano una passata a parte.** Ridurre le ripetizioni, uniformare il registro, spostare
un paragrafo: non sono sostituzioni. Se in quel giro non si fanno, si **dichiarano come non fatte** nel
riepilogo (e restano scritte nel rapporto, così il giro dopo sa da dove ripartire).

**La passata sulle ripetizioni, come si fa davvero.** Confrontare le frasi una per una (somiglianza fra
stringhe) **non trova le ripetizioni di questo sito**: sono concettuali, dette con parole diverse, e quel
controllo torna vuoto. Quello che funziona è contare i **gruppi di parole ripetuti** (5-grammi, su testo
normalizzato: minuscole, niente punteggiatura) e guardare dove ricadono. Il verdetto, su otto bozze:
- **Il riquadro → corpo → FAQ → sintesi che ripete i concetti-chiave è il formato del sito, non un difetto.**
  Appiattirlo peggiora l'articolo. Si tocca solo la **ripetizione verbatim** (la stessa frase identica
  quattro-cinque volte): si varia in due punti e si lasciano i blocchi di servizio.
- **Le ricorrenze di un termine tecnico non sono ripetizioni.** Se il gruppo ripetuto è il nome di una cosa
  che l'articolo spiega (i parametri di un comando, «tempo al primo byte», «script e fogli di stile»),
  cambiarlo toglie chiarezza: si lascia così.
- **`alt` e didascalie restano**, anche quando ripetono il testo: descrivono l'immagine e servono a chi
  legge con uno screen reader. Il taglio, se serve, si fa nel corpo.
- **Tre occorrenze con tre ruoli diversi** (apertura, sezione dedicata, chiusura) sono il filo dell'articolo:
  restano.
Nel rapporto la passata si annota con la sua riga (`> **Ripetizioni — verificate il …**`) con l'esito **e il
motivo**, anche quando l'esito è «nessuna da ridurre»: è la riga che impedisce al giro dopo di rifare il
lavoro o, peggio, di appiattire il formato credendolo un difetto.

**Due regole che vengono dall'autore:**
- **Le immagini della bozza restano quelle che ci sono.** Non si rigenerano, non si sostituiscono, non si
  propongono alternative (l'autore non ha credito per generarne di nuove): se una correzione riguarda
  un'immagine, si dichiara e si aspetta.
- **Un caso non verificabile si toglie, non si aggiusta.** In un articolo che insegna a verificare le fonti,
  un esempio senza titolo, autore o link è il primo da rimuovere — e citare l'articolo stesso come motivo
  funziona meglio di qualunque spiegazione. Vale identicamente per un **numero**: se la pagina ufficiale che
  dovrebbe pubblicarlo si apre e non lo contiene (verificato **aprendola**, non ricordandola), il dato si
  **toglie**; lasciarlo senza fonte o appoggiarlo a una fonte qualsiasi sono lo stesso errore.

**Si corregge per prima l'istruzione pericolosa**, anche se è «solo» una frase: rimuovere una filigrana
(vietato dai termini d'uso), cancellare un file senza spegnere il log, un comando usato su un motore che non
lo supporta. È quella che fa danno a chi legge.

## Forma del rapporto

Un file `.md` per bozza, nella **cartella dei rapporti**, dentro la cartella di lavoro (non nel repo del progetto) e in una
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

**In chat vale la regola generale di Mada: Markdown ricco, tabelle comprese** (comunica da Telegram, dove
si leggono). Le tabelle del rapporto stanno anche nel file `.md`; la sintesi in chat serve a decidere cosa
aprire, non a sostituire il rapporto.
