# Fonti e ricerca: come si trova un'informazione VERA

> Questo file esiste per una sola ragione: **il difetto più grave trovato nell'audit del sito sono i dati
> e le credenziali inventati.** Casi verificati: dataset attribuiti al sito che non esistono
> (*«dataset del sito, 2024, n=50.000 siti»*), benchmark attribuiti a marchi reali (*«Kinsta/WP Engine
> 2024, n=10k siti»*), un *«team di specialisti del sito»* che è una persona sola, *«dopo anni di…»* su
> un blog nato da un mese, sei attribuzioni senza nome (*«un consulente», «un SEO italiano», «su Quora un
> tecnico»*).
>
> **Il rimedio non è scrivere meglio: è cercare prima.** Quando il dato manca, la soluzione è andarlo a
> prendere — non riempire il vuoto con qualcosa di plausibile.

## 1. La gerarchia delle fonti (si scende solo se il gradino sopra tace)

| # | Fonte | Esempi su questo sito | Come si cita |
|---|---|---|---|
| 1 | **Documento ufficiale del produttore o dell'ente** | documentazione WordPress.org, pagina OpenAI, accordo Amazon Associates, `wp-config.php` nel sorgente | link diretto + data di lettura |
| 2 | **Fonte primaria normativa o scientifica** | Normattiva, Garante privacy, AGCOM, EUR-Lex, paper con DOI o arXiv | numero/articolo o DOI + data |
| 3 | **API e dati ufficiali** | API di WordPress.org (installazioni, recensioni), Stack Exchange API, autocompletamento Google | endpoint + valore letto + data |
| 4 | **Stampa specializzata** | Il Post, Sole 24 Ore, TGcom24 | autore, testata, data, link |
| 5 | **Community** | forum italiano di WordPress, Stack Exchange, Reddit, Quora | **nome utente + thread + data + link** |

**Le community si usano, e a volte sono la fonte migliore** — il `1940` è la bozza con le citazioni
meglio verificabili di tutte (sei, tutte testuali, tutte sulle pagine linkate). La differenza tra quella
bozza e il difetto descritto sopra è una sola: **nome, thread e link**.

## 2. I divieti (verificati, non stilistici)

Non entrano in un articolo, mai:

- *«un utente»*, *«un consulente»*, *«un esperto»*, *«un SEO italiano»*, *«chi lavora nel settore»* — come
  fonte di un dato o di un giudizio. Se la persona c'è, si cita con nome e luogo; se non si può, l'aneddoto
  si toglie;
- **dataset, campioni, benchmark attribuiti al sito** (*«abbiamo analizzato 50.000 siti»*): il sito non ha
  dataset, e il blog è di agosto 2026;
- **benchmark attribuiti a terzi senza URL** (*«Kinsta/WP Engine 2024, n=10k»*): attribuire un test a un
  marchio reale non è un'imprecisione, è una falsa attestazione;
- *«il nostro team»*, *«i nostri esperti»*: c'è un autore solo;
- *«dopo anni»*, *«in anni di»*, *«la nostra esperienza pluriennale»*: si può descrivere l'esperienza che
  si ha, non gli anni che non si hanno;
- **numeri senza fonte**: statistiche, percentuali, «il 90%», «uno su tre». Un numero senza URL si toglie
  o diventa una spiegazione senza numero.

**Nota sul formato**: una percentuale inventata in un articolo che chiede trasparenza è il difetto che
pesa più di dieci frasi lente (nella bozza `1918`, un articolo sui link sponsorizzati, c'era *«il 90% dei
blog che sbagliano non lo fa per furbizia»*).

## 3. Ogni numero ha un URL, e ogni URL si apre

1. **Se il numero c'è, si prende dalla fonte e si mette il link.** Se non c'è, la frase si riscrive senza
   numero (una spiegazione senza cifre è meglio di una cifra inventata).
2. **Si apre la fonte prima di citarla.** Un link che risponde 200 non è una fonte verificata: la fonte
   va **letta**, e va letta la frase precisa che si sta usando.
3. **Le citazioni fra virgolette si confrontano parola per parola** con l'originale, comprese le
   traduzioni: togliere un pezzo *dentro* le virgolette è il modo più silenzioso di far dire alla fonte
   più di quanto dica (`1479`: la citazione di Google tagliata proprio nella parte che qualifica il
   PageRank nel presente).
4. **La fonte che dice l'opposto.** Quando un articolo cita una fonte **a sostegno di una tesi**, la frase
   chiave di quella fonte va letta: il `585` linka la pagina ufficiale dei blocchi riutilizzabili che dice
   testualmente il contrario della tesi dell'articolo.
5. **La data della fonte e la data della lettura.** Se un articolo dichiara quando ha verificato le fonti,
   quella data va confrontata con la data di modifica della pagina: una nota di verifica più vecchia
   dell'ultima revisione è un dato stantio certificato come fresco (`1854`).

## 4. Le verifiche che si pagano care (dal più costoso)

| Cosa si verifica | Come | Caso che l'ha insegnato |
|---|---|---|
| **La legge** | testo consolidato su Normattiva, Garante, AGCOM — mai un riassunto | `221` (DL 87/2018, art. 9) ✅ e `214` (delibera AGCOM citata per numero) ✅: questa parte funziona |
| **I requisiti/dati tecnici** | documentazione ufficiale, trascritta al carattere | `1967` (PHP/MariaDB/MySQL), `1962` (accordo Amazon) |
| **La nazionalità di un prodotto** | pagina ufficiale del produttore | `226`: *«SEOPress è italiano»* → è **francese** |
| **Il nome di una metrica o di una funzione** | sito del produttore | `1479`: *«Zero Authority»* → si chiama **Zoom Authority** |
| **Un dato del proprio sito** | si apre la pagina viva e si conta | `1529` (*«due blocchi JSON-LD»* → sono tre), `1412` (`aria-expanded` assente), `1613` (la data «in cima» che sta in fondo) |
| **Le istruzioni operative** | si eseguono o si verificano sull'interfaccia | `1959`: *«chi non si trova non esiste»* è falso; `1940`: la riparazione consigliata non funziona su InnoDB |
| **Le prove di prima mano** | si rifanno | `1883` (suggerimenti Google), `1967`, `1878` (la trappola del video riprodotta) |

## 5. Le prove di prima mano: quando valgono

Un test pubblicato in un articolo vale **solo se è replicabile**. Deve dichiarare:

1. **lo strumento, con il nome e la versione** (non «un modello di fascia normale»);
2. **la data**;
3. **il comando o il prompt esatto** (per intero, copiabile);
4. **i risultati grezzi**, dove è possibile.

Senza questi quattro pezzi non è una prova: è un aneddoto con i numeri. Quattro bozze su quindici hanno
rifatto un test vero e non hanno dato gli strumenti per rifarlo (il comando ffmpeg assente, i sei modelli
senza nome, plugin e tema non nominati).

**E il metodo proposto va collaudato**: se un articolo insegna un metodo (come verificare una keyword, come
misurare qualcosa), quel metodo si prova prima di scriverlo — la prova del `1883` non era riproducibile
con il criterio che l'articolo stesso indicava.

## 6. Quando la fonte non c'è: si scrive che non c'è

L'articolo migliore del sito per questo è il `1977`: dichiara *«quello che non posso dirti è una
percentuale di errore per l'italiano… chi promette numeri precisi sull'italiano sta inventando»*. E le
bozze migliori fanno lo stesso (`1878`: *«quello che non ho misurato non lo scrivo come se l'avessi
fatto»*).

**La formula da usare**: *«non l'ho potuto verificare»*, *«il fornitore non pubblica il dato»*, *«su questo
non ci sono fonti»*. È sempre meglio di un buco riempito, e su un blog che dichiara un metodo è quello che
costruisce fiducia.

## 7. Dove si cerca (i canali restano quelli della skill)

Questo file dice **a chi credere**, non **dove cercare**: i canali e i programmi sono in
`ricerca-webcmd.md` (SERP, Google, Quora, Reddit, X, LinkedIn) e `ricerca-omnichannel.md` (cosa si cerca
in ciascuno). Le due cose da tenere insieme:

- **si cerca prima, si scrive dopo**: il capitolo che serve (il dato, la norma, il numero) si recupera
  quando si pianifica l'articolo, non quando si è a metà del testo;
- **quando una pagina blocca**, non si rinuncia e **non si inventa**: `blocked-page-recovery`, Scrapling,
  o il browser interno (le pagine dei fornitori che rispondono 403 si leggono nel browser vero).
