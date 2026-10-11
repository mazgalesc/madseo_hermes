# I controlli incrociati: prima di dire «pronto»

> La checklist «Definizione di pronto» del `SKILL.md` controlla **la forma** (link, meta, schema, blocchi,
> immagini, punteggio, privacy). Questi sono i controlli che mancavano: **quelli che confrontano le parti
> dell'articolo fra loro.** Sono i difetti che l'audit ha trovato di più — e nessun controllo automatico
> attuale li vede, perché ognuno dei due pezzi, preso da solo, è corretto.
>
> **Regola d'ordine**: si eseguono **tutti**, e i primi quattro sono **bloccanti** (l'articolo non è
> pronto finché non passano). Non si dichiara «pronto» con la maggior parte dei controlli passati.

## 1. Conteggi annunciati vs elenchi (bloccante)

Per **ogni** «i N …», «le N cose», «i N errori», «N controlli», «la tabella qui sotto elenca N»:

1. conta le voci di ogni elenco o tabella che dovrebbe contenerli;
2. confronta con il numero annunciato **in ogni punto in cui è annunciato**: titolo, riquadro di apertura,
   sintesi, FAQ, didascalie delle immagini, schema;
3. se i valori sono più di uno, **l'articolo non è pronto**: si allinea il numero o si allinea l'elenco.

Casi reali: `1452` — **cinque** liste contate in modi diversi nella stessa pagina; `221` — riquadro e
paragrafo con **zero voci in comune**; `217` — «i 10 migliori» con 15 trattati; `222` — «16 errori» con 9
righe; `1412` — la stessa verifica annunciata «quattro», riassunta in 7, sviluppata in 10.

## 2. Aritmetica (bloccante)

1. **Ogni conto si rifà a mano**, compreso quello che sembra ovvio.
2. **Ogni percentuale convertita in numeri** (visite, ordini, euro) si rifà: `1603` dichiarava «3.000
   visite per un ordine» con l'1% di conversione (sono 100); `219` sbagliava di **50 volte**; `215` aveva
   la formula dell'EPC ribaltata fra riquadro e testo.
3. **Ogni formula** («si calcola così», «basta dividere») si rifà con numeri veri: due percentuali
   moltiplicate non danno euro per clic.
4. **Le somme delle tabelle** si rifanno e si confrontano con i totali dichiarati (`209`: 915 € contro
   «60-350 €»).
5. **Le unità di misura si uniformano** prima di confrontare (€/anno contro €/mese nella stessa colonna:
   `212` faceva sembrare il più caro il più economico).
6. **Un solo listino del sito**: ogni prezzo (hosting, manutenzione, dominio) si confronta con lo stesso
   prezzo negli altri articoli — `216` diceva 100-300 €/anno di manutenzione, `209` diceva 300-1.500 €.
7. **L'IVA si dichiara** in ogni articolo di prezzi per l'Italia (nel `209` non c'era).

## 3. Riquadro vs corpo, e sintesi vs prova (bloccante)

- **Riquadro e paragrafo**: si confrontano voce per voce. Se il riquadro risponde alla stessa domanda del
  paragrafo, uno dei due si toglie, oppure il secondo **aggiunge** qualcosa (un esempio, un numero, un
  caso). 352 riquadri sul sito, 29 con ripetizione: il difetto strutturale del sito è questo.
- **Sintesi vs prova**: la conclusione non deve cancellare la condizione che rende vera la prova. Il
  `1883` dimostrava che con l'elenco delle pagine l'IA azzecca i link interni e poi concludeva «l'IA non
  serve per link». Il `1959` diceva «dal 2% al 6% anche sui modelli migliori» contro i propri 1,8%.
- **Regola dichiarata e poi disfatta**: per ogni affermazione normativa («si fa così», «non si usa»,
  «va messo lì»), cercare nel resto della pagina se qualcosa la contraddice. Tre casi: `1412`, `1441`,
  `1603`.

## 4. Promesse (bloccante)

Ogni frase che promette qualcosa va verificata **aprendo la destinazione**:

- *«lo trovi nella nostra guida X»* → la guida X contiene davvero quella cosa? (`208` prometteva i
  permessi in una guida che non ne parlava: i valori stanno nel `206`);
- *«è ciò che la nostra guida alla sicurezza chiama…»* → quella frase esiste nella guida? (`210`: **no**);
- *«un corso gratuito e in italiano»* → è in italiano? (`213`: era in inglese);
- *«le istruzioni personalizzate»*, *«con i conti in chiaro»*, *«N usi che non avevi considerato»* → ci
  sono davvero? (`213`: quattro usi, non sei; `220`: i numeri erano dichiarati «illustrativi»);
- ogni **menzione di un altro articolo del sito** va linkata nello stesso punto (`205`, `206`, `207`,
  `209`, `210`: guide citate senza link).

## 5. Blocchi e struttura

| Controllo | Cosa si cerca | Prove |
|---|---|---|
| **Intestazioni vuote** | ogni H2/H3 ha almeno un paragrafo **immediatamente** sotto | `217`, `218`, `220` |
| **Blocchi sotto la sezione sbagliata** | il testo che appartiene a un titolo sta sotto quel titolo | `220`, `217`, `218` |
| **FAQ e schema** | le domande dichiarate nello schema sono quelle visibili sotto l'H2 delle FAQ, **una per domanda** | `218`, `1452` |
| **Un solo `<h1>`** e il `<title>` SEO non ripetuto nel corpo | contare gli `<h1>` | `684` |
| **Schema coerente col contenuto** | niente FAQ/HowTo se non si vedono; **`HowTo` fuori** (ritirato da Google nel 2023); tipo principale **`BlogPosting`** | tutto il sito |
| **Alt di tutte le immagini**, copertina compresa | elencare ogni `<img>` e stampare l'alt; nessuno vuoto, nessuno che descriva un'altra immagine | `1550` (copertina vuota), `207` (alt di un'altra immagine) |
| **Nofollow sulle fonti** | le fonti autorevoli si linkano normali (al più `noopener`); `nofollow`/`sponsored` solo per i link commerciali | `226`/`227` contro `1412` |

## 6. Artefatti di produzione (si cercano con una ricerca nel testo)

Da cercare **nel contenuto salvato e nella pagina resa**:

| Cerca | Perché |
|---|---|
| `PT` (durata ISO dello schema: `PT2H`, `PT10M`) | finisce a video il campo tecnico del blocco HowTo (`222`, `1412`, `1441`) |
| `la <N> stessa`, `post_id`, `ID` | l'ID del post rimasto nel testo (`226`) |
| `u/`, `r/` | note di fonte Reddit non ripulite (`1479`) |
| `&lt;`, `</`, `<p>` | HTML escapato stampato a video (`1529`) |
| `` ` ``, `**`, `[]` | markdown non convertito (`227`) |
| «Risposta diretta:», «Risposta rapida:» | etichetta di layout rimasta visibile (`222`, `223`, `224`) |
| «Updated on», «Table of contents», «(which is better?)» | inglese rimasto in produzione (`204`, `205`, `208`) |
| `query`, `SERP`, `in prima pagina`, `posizione N` | linguaggio da analisi di ricerca rimasto nel testo (`227`) |
| `??` | bandierine perse (`204`) |
| *«come detto sopra»*, *«la settimana scorsa»*, *«di recente»* | riferimenti relativi che invecchiano male |

## 7. Il testo: le regole di scrittura che l'audit ha confermato

- **Il conteggio delle parole si fa PRIMA di creare la bozza** (non dopo): 11-12 sezioni × 160-170 parole
  ≈ 1.800-2.000. Quattro articoli creati a 1.253-1.423 parole e allungati a mano: il doppio del lavoro.
- **I capitoli che mancano sempre** e che vanno previsti in pianificazione, non aggiunti dopo:
  1. **le eccezioni** («quando non serve», «quando va male») — è la parte che l'IA non scrive;
  2. **i costi e gli obblighi italiani** (INPS, marca da bollo, privacy/cookie, P.IVA nel footer);
  3. **l'affiliazione, per intero**: dichiarazione di trasparenza + `rel="sponsored"` sui link in uscita
     + la dicitura richiesta dal programma (Amazon ha la sua) + le deroghe a favore dell'affiliato
     (la regola dei 90 giorni sul carrello che il `1603` ometteva);
  4. **le domande di chi legge** (FAQ) — e il numero delle risposte deve coincidere con lo schema.
- **Le conclusioni si leggono per ultime**: è il punto in cui un testo troncato si vede di più (`224`:
  una conclusione senza proposizione principale).

## 8. Lo script `scripts/controlla-articolo.py` (scritto l'11/10/2026)

I controlli automatizzabili sono dentro **`scripts/controlla-articolo.py`** (solo libreria standard,
nessuna rete, nessuna dipendenza). Stampa **candidati da verificare a mano**, mai verdetti:

```bash
python3 scripts/controlla-articolo.py <file>        # .json del plugin, .html, .md o .txt
python3 scripts/controlla-articolo.py --testo < t.md # legge da stdin
python3 scripts/controlla-articolo.py --json <file>  # per usarlo da altri script
python3 scripts/controlla-articolo.py --parole <file># solo il conteggio parole (da fare PRIMA di creare la bozza)
```

Controlla, e stampa con il contesto:

1. i numeri annunciati (`i \d+`, `le \d+`, `\d+ (errori|cose|controlli|passi)`) con i conteggi degli
   elenchi e delle tabelle vicini;
2. le uguaglianze aritmetiche (espressioni con `%`, `×`, `=`) da rifare;
3. le occorrenze di `u/`, `r/`, `PT[0-9MH]`, backtick, `**`, `&lt;`, `Risposta diretta:`, `la \d+ stessa`,
   `Updated on`;
4. tutte le `<img>` con l'alt (per trovare i vuoti e i duplicati);
5. tutti i link interni con l'etichetta e il titolo della pagina di destinazione, per il controllo
   «l'etichetta corrisponde alla destinazione»;
6. le ripetizioni a **mezza frase** (il confronto a frase intera è cieco a metà delle duplicazioni: da
   `209` dava 1 dove le ripetizioni erano 2, e il secondo lettore ne ha trovate altre quattro volte).

**Nessuno di questi controlli sostituisce la lettura**: sono la lista di dove guardare, come i numeri del
plugin SEO non sostituiscono l'HTML pubblico. Provato l'11/10/2026 su pagine vere: trova le note `u/`/`r/`
rimaste in pagina (`1479`), l'HTML escapato a video (`1529`), le «Updated on» in inglese, gli elenchi che
non corrispondono al numero annunciato (`1452`) e le intestazioni senza corpo sotto (`1930`).

**Due limiti da conoscere**: sul testo semplice (`.md`/`.txt`) i controlli su elenchi, tabelle,
intestazioni e immagini **non sono possibili** (manca la struttura) — lo script lo dichiara; e la «voce
vicina» è quella più prossima, quindi su elenchi annidati può indicare il numero sbagliato: è un indizio
da aprire, non un verdetto.
