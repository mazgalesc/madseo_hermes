# Trappole verificate — il sito / il-tuo-sito.it

*Un solo file per tutte le trappole: le cinque sezioni storiche (19-21/09/2026) e le sedici nuove
verificate il 24/09/2026 durante la verifica dei 33 pubblicati e delle 9 bozze. Unite il 24/09/2026
da `SKILL.md` e da `references/trappole.md`: contenuto invariato, solo intestazioni e ordine.*

**In questo file:** Codici HTTP che non sono link rotti · Fonti e autorevolezza · Pagine a zero
impression · Schema · Meta (titolo e description) · Contenuto: marcatori rotti e blocchi ·
Blocchi, media, ambiente · Domanda e query · Bozze: come si verificano.

## Codici HTTP che non sono link rotti

- **`www.wordfence.com` risponde 202 a `curl` e non è un link rotto**: è la sfida anti-bot di AWS WAF
  (`server: CloudFront`, `x-amzn-waf-action: challenge`, `content-length: 0`). Un client vero riceve la
  pagina regolarmente (verificato il 24/09/2026 con `web_extract`: homepage completa, 2.378 caratteri).
  **Non segnalarlo come anomalia**: il codice da controllare è l'intestazione, non il 202.
- **Un 403 su un sito SaaS non significa link rotto**: `cloudflare.com/learning/…` risponde **403** a `curl`
  (protezione anti-bot) e serve la pagina completa a un browser. Verificato il 24/09/2026 sull'articolo 1441.
  **Prima di dichiarare rotto un link, rileggerlo con un client che si comporta come un browser.**
- **Cloudflare risponde 403 "error 1010"** se il client ha la firma di Python (urllib/httpx senza
  User-Agent normale). Con `curl` passa, e il client MCP di Hermes passa. Se una chiamata HTTP al
  sito fallisce con 1010, è quello: usare `curl`.
- **`chat.openai.com` risponde 403**: il servizio è su `chatgpt.com` e il vecchio indirizzo non serve più
  nessuno (verificato il 24/09/2026). Nei contenuti il link giusto è `https://chatgpt.com`. In generale,
  quando un articolo linka un servizio SaaS, controllare che l'URL non sia un vecchio dominio del fornitore:
  risponde 403 o rimanda a una pagina di errore e non si vede dal conteggio dei link.

- **Il 403 su un sito SaaS non significa link rotto.** Cloudflare risponde `403` con l'intestazione
  **`cf-mitigated: challenge`** quando il client non è un browser: verificato il 24/09/2026 su **chatgpt.com,
  claude.ai, perplexity.ai, canva.com, leonardo.ai, make.com** — tutte e sei servono la pagina completa a un
  client vero. Vale anche per il `202` + `x-amzn-waf-action: challenge` di `wordfence.com`. **Prima di
  dichiarare rotto un link, rileggerlo con un client che si comporta come un browser.**

- **`www.wordfence.com` risponde 202 a `curl` e non è un link rotto**: è la sfida anti-bot di AWS WAF
  (`server: CloudFront`, `x-amzn-waf-action: challenge`, `content-length: 0`). Un client vero riceve la
  pagina regolarmente (verificato il 24/09/2026 con `web_extract`: homepage completa, 2.378 caratteri).
  **Non segnalarlo come anomalia**: il codice da controllare è l'intestazione, non il 202.

- **`chat.openai.com` risponde 403**: il servizio è su `chatgpt.com` e il vecchio indirizzo non serve più
  nessuno (verificato il 24/09/2026). Nei contenuti il link giusto è `https://chatgpt.com`. In generale,
  quando un articolo linka un servizio SaaS, controllare che l'URL non sia un vecchio dominio del fornitore:
  risponde 403 o rimanda a una pagina di errore e non si vede dal conteggio dei link.

## Fonti e autorevolezza

- **La fonte primaria batte l'enciclopedia**: nei contenuti che parlano di uno strumento, il primo link
  esterno deve essere la **documentazione ufficiale** del fornitore (per ChatGPT: la pagina *OpenAI
  Academy* in italiano, che è anche il primo risultato di Google su «come usare chatgpt»). Cinque link
  alla Wikipedia italiana e zero alla fonte ufficiale, come sull'articolo 213, è la scelta più debole
  possibile per l'autorevolezza e per la GEO.
- **Lo standard del sito per i link esterni è l'articolo 225**: nove link, **zero Wikipedia**, tutti primari o
  ufficiali — PageSpeed Insights, Search Console, **`php.net/supported-versions.php`**, tre schede di plugin
  su `it.wordpress.org`, MDN Web Performance, **`make.wordpress.org/performance`** (il Performance Team
  ufficiale) e **`web.dev/articles/vitals`**. Da citare come modello quando si dice all'autore quali fonti
  aggiungere: le pagine che un articolo tecnico *dovrebbe* citare esistono quasi sempre e sono già in prima
  pagina. Il contrario sono i sette Wikipedia su otto del 224.
- **Il tetto più alto è l'articolo 1441**: sei link esterni, **ICANN (`lookup.icann.org`), IANA
  (`iana.org/domains/root/servers`), IETF (`rfc1035.txt`), MDN, la documentazione di WordPress.org e
  Cloudflare Learning** — nessuna Wikipedia, nessuna fonte commerciale, la specifica tecnica citata
  direttamente. È il riferimento quando si parla di contenuti divulgativi ma tecnici.
- **Sui contenuti tecnici il metodo viene prima dei rimedi**: il capitolo `Prima misura, poi ottimizza`
  dell'articolo 225 (misura, poi intervieni, poi rimisura) è ciò che distingue una guida da un elenco di
  consigli — ed è esattamente ciò che manca al 223, che elenca errori senza dire come si misurano prima e dopo.

- **La fonte primaria batte l'enciclopedia**: nei contenuti che parlano di uno strumento, il primo link
  esterno deve essere la **documentazione ufficiale** del fornitore (per ChatGPT: la pagina *OpenAI
  Academy* in italiano, che è anche il primo risultato di Google su «come usare chatgpt»). Cinque link
  alla Wikipedia italiana e zero alla fonte ufficiale, come sull'articolo 213, è la scelta più debole
  possibile per l'autorevolezza e per la GEO.

- **Lo standard del sito per i link esterni è l'articolo 225**: nove link, **zero Wikipedia**, tutti primari o
  ufficiali — PageSpeed Insights, Search Console, **`php.net/supported-versions.php`**, tre schede di plugin
  su `it.wordpress.org`, MDN Web Performance, **`make.wordpress.org/performance`** (il Performance Team
  ufficiale) e **`web.dev/articles/vitals`**. Da citare come modello quando si dice all'autore quali fonti
  aggiungere: le pagine che un articolo tecnico *dovrebbe* citare esistono quasi sempre e sono già in prima
  pagina. Il contrario sono i sette Wikipedia su otto del 224.

## Pagine a zero impression

- **Una pagina a zero impression va diagnosticata, non commentata.** Se una pagina pubblicata non compare in
  Search Console (né in 28 né in 90 giorni) mentre le altre sì, l'ordine dei controlli è: `robots.txt`,
  presenza nella sitemap con il suo `lastmod` (`/sitemap.xml` elenca i sotto-sitemap; i post stanno in
  `sitemap-posts.xml`), canonical autodichiarata, meta robots senza noindex, pagina pubblica 200, e — con
  webcmd — tre query di prova: `site:<dominio> <parole del titolo>`, **`site:<dominio> inurl:<slug>`** e il
  **titolo esatto fra virgolette**. Una pagina indicizzata compare in almeno una delle tre. Se passano tutti
  i controlli e la pagina resta invisibile, **l'ipotesi è «non indicizzata»** e la conferma è l'ispezione URL
  in Search Console (richiede il pannello: dichiarare che va fatta lì, non inventare la causa).
  Casi reali del 24/09/2026: **210, 212 e 213** — zero impression in 28 e in 90 giorni, tutto in regola,
  `inurl:` a zero risultati, e la query col titolo esatto che restituisce **altre pagine del sito che linkano
  la pagina mancante** (segno che Google ha scansionato il sito ma non ha indicizzato quella pagina).

  **Il controllo va fatto a livello di sito, non solo di pagina.** Due numeri da mettere sempre accanto:
  **quanti post sono pubblicati** (`REST /wp/v2/posts?per_page=100`) e **quante pagine hanno almeno una
  impression in 90 giorni** (`searchAnalytics/query` con `dimensions:["page"]`). Misurato il 24/09/2026:
  **33 post pubblicati, 9 pagine con impression, 27 post a zero** — con metà degli articoli verificati
  invisibili. Un rapporto solo può essere un caso; il rapporto dice se è il sito. Aggiungere anche il
  controllo con **user-agent Googlebot** (`curl -A 'Mozilla/5.0 (compatible; Googlebot/2.1; …)'`): se
  risponde 200 come a un browser normale, **non c'è blocco lato server** e la diagnosi resta a Search
  Console.

## Schema

- **Il campo `tools` dello HowTo può salvare la stringa `"Array"` al posto degli strumenti** (verificato il
  24/09/2026 sull'articolo 208). La meta `_sito_seo_howto` conteneva `"tools":["Array","Array"]` e il
  JSON-LD **pubblicato** dichiarava due `HowToTool` chiamati letteralmente «Array»: un dato falso servito a
  Google. Scrivendo uno schema HowTo, passare `tools` come **array di stringhe vere** («UpdraftPlus», «un
  account cloud») e poi **rileggere la pagina pubblica**, non solo l'abilità: il difetto si vede solo nel
  JSON-LD reso. La correzione va fatta alla fonte (campo meta), non nell'HTML.
- **I numeri dei plugin si verificano sull'API ufficiale** quando l'articolo ne nomina qualcuno
  (installazioni, voto, ultimo aggiornamento): `api.wordpress.org/plugins/info/1.2/?action=plugin_information&request[slug]=<slug>`
  con `curl --globoff`. Sono dati citabili che alzano l'autorità (e la GEO) senza inventare niente.

- **Lo schema si controlla sul `@type`, non solo sulla presenza.** **Quattro articoli del sito** dichiarano
  `@type: Article` invece di **`BlogPosting`**: **585, 684, 1479, 1529** (verificati il 24/09/2026). **La diagnosi
  è chiusa: NON è un default del plugin.** Le date sono alternate (684 del 12 set e 585 del 18 sono `Article`;
  1441 e 1412 del 14 set e 1452 del 19 sono `BlogPosting`; 1479 del 20 e 1529 del 23 sono di nuovo `Article`),
  due pagine dello stesso giorno hanno tipi diversi, e sono tutte categoria 3: **esclusi data, categoria e
  argomento**, resta un valore **scelto per singola pagina**. Quindi: **quattro campi da cambiare**, non
  un'impostazione da sistemare — e **resta da capire chi o cosa scrive quel campo**, perché in un caso su cinque
  mette il generico. Il caso più ironico è il **1529**, che è **la guida allo schema markup** e sbaglia il proprio;
  il più utile è il **684**, che ha un H3 che spiega «per la maggior parte dei blog WordPress, BlogPosting è la
  scelta corretta» mentre la sua pagina dichiara `Article`. Si trova solo leggendo il `@type`, non guardando la
  pagina.

- **Le promesse di risultati arricchiti vanno controllate nei contenuti pubblicati.** FAQPage e HowTo **non danno
  più risultati arricchiti** (limitate dal 2023; il Rich Results Test non le supporta più da giugno 2026): un
  articolo che scrive «Google mostra le FAQ come sezione espandibile nei risultati» o «gli step come carosello»
  **promette al lettore qualcosa che non esiste**. Verificato sul **684** (12/09/2026): due sezioni superate,
  mentre la regola di fondo che l'articolo enuncia (*lo schema deve corrispondere al testo visibile*) resta valida.
  È il tipo di difetto che **danneggia il lettore**, non solo la SEO: nei rapporti va segnalato per primo, e il
  modo di correggerlo è cambiare la motivazione, non la regola.

## Meta: titolo e description in caratteri

- **I meta si misurano anche in caratteri, oltre a leggerli.** Il **585** ha il **titolo più lungo del sito (65)** e
  una description da **163**, entrambi **oltre la soglia di visualizzazione** (~60 e ~155-160): in SERP sparisce
  «di WordPress» dal titolo e la promessa operativa dalla description. Il taglio non è un vezzo: va scelto il
  contenuto che sta nel limite, e va scritto nel rapporto **quale pezzo si perde**.
- **La description si conta PRIMA di inviarla, non dopo.** Errore ripetuto per quattro articoli di fila il
  29/09/2026 (177, 189, 164, 165 caratteri a fronte del limite di 160): si scrive il testo a memoria, si
  invia con `seo/update-post-seo`, e solo l'analisi successiva rivela che è lungo. Il rimedio è
  meccanico: preparare due o tre varianti in una lista, **stampare `len()`** e inviare solo quella entro
  158 caratteri. Vale identico per il titolo (limite 60) e per il titolo SEO del post.
- **Dentro una bozza non si linka un'altra bozza.** Il 29/09/2026 l'articolo 1889 linkava l'articolo 1883,
  che era ancora in bozza: ai lettori sarebbe stato un **404**. I link interni si mettono solo verso
  **pagine pubblicate**; se il collegamento serve a un articolo in coda, si aspetta la sua pubblicazione o
  si linka un equivalente già pubblico. Verifica: `curl -o /dev/null -w '%{http_code}'` su ogni link
  **della bozza**, non solo su quelli degli articoli pubblicati.

## Contenuto: marcatori rotti e blocchi

- **Prima di modificare un contenuto, scansionare i marcatori con una pila — e riscansire dopo.** Il
  30/09/2026 la 202 aveva una lista **chiusa a metà**: il primo `<ul>` finiva con `</ul>` seguito da
  `<!-- /wp:list-item -->` invece che da `<!-- /wp:list -->`, e si apriva con un `list-item` vuoto.
  Effetto: tutto il contenuto successivo risultava annidato nella lista, e un secondo `<ul>` restava
  **fuori**, con gli `<li>` sciolti. **Il conteggio dei marcatori era bilanciato (44 aperti, 44 chiusi):
  il difetto è nell'ordine, non nel numero** — quindi un controllo di conteggio non lo vede. Lo scanner
  giusto tiene una pila: apre sui marcatori di apertura (saltando quelli auto-chiusi `/-->`), chiude se la
  cima corrisponde, e segnala «chiusura senza apertura» e ciò che resta aperto alla fine. **Da eseguire
  prima e dopo ogni modifica**: dopo l'accorpamento della 202 lo scanner ha trovato una chiusura orfana
  (`<list>` senza apertura) che il conteggio non mostrava.

- **Non modificare per posizione: usare ancore testuali, ricalcolate a ogni passo.** Due trappole nello
  stesso script (30/09/2026): (1) uno splitter per offset di blocco ha inghiottito **48.000 caratteri**
  dentro una lista rotta, cancellando mezza pagina — risolto con `str.find` su intestazioni e su marcatori
  esatti; (2) dopo una prima sostituzione gli offset **calcolati sulla stringa originale** puntavano
  dentro un marcatore della stringa già modificata, troncandolo in `<!-- /wp:list-ite`. **Le ancore si
  ricalcolano sulla stringa corrente, non su quella di partenza.**

- **Caratteri `<` o `>` orfani fra un blocco e l'altro: si vedono in pagina e il validatore li segnala.**
  La 214 ne aveva **quattro** (`freeform_html_outside_blocks`), visibili come una parentesi angolare
  solitaria fra una sezione e l'altra. Si trovano con una ricerca di una riga che contiene solo `<` o `>`
  e si rimuovono; vanno cercati su tutto il sito perché sono residui di modifiche precedenti, non di
  quelle in corso (la 214 era invalida **prima** dell'intervento).

- **Accorpare due pagine senza cambiare URL: una tiene la promessa, l'altra perde il capitolo e guadagna
  un rimando.** È la strada usata il 30/09/2026 sulle tre coppie (684/1529 schema, 202/203 introduzioni
  all'IA, 214/221 affiliazione), scelta al posto del 301 perché **nessun URL viene ritirato e il contenuto
  non si perde**. Tre regole: (1) **si decide chi tiene la promessa in base a chi la copre più in
  profondità**, non a chi è più vecchio; (2) **la pagina che perde il capitolo lo sostituisce con una
  sezione breve che punta all'altra**, non con il vuoto; (3) **si aggiornano titolo e H1 di quella pagina**, se il
  capitolo rimosso era nella promessa — la 684 è passata da *Link Building e Schema Markup* a *guida al
  link building*. Le prove da produrre: `is_valid_gutenberg: true` su entrambe, gli slug **invariati** e
  verificati 200 sull'HTML pubblico, e i rimandi in entrambe le direzioni.

**I blocchi elenco scritti a mano vanno chiusi voce per voce.** Verificato il 29/09/2026 sull'articolo 1924: scrivendo a mano le liste con `<!-- wp:list-item -->\n<li>…</li>` **senza** il `<!-- /wp:list-item -->` di chiusura, il parser segnala `unexpected_closing_block` e `freeform_html_outside_blocks`, e il contenuto risulta **sballato al punto da pesare 107 KB con 24 immagini invece di 16 KB con 2** (il testo viene riletto e rinormalizzato in modo incoerente, con blocchi `core/post-content` che compaiono dal nulla). La forma corretta, per ogni voce, è sempre la terna:
`<!-- wp:list-item -->` + `<li>…</li>` + `<!-- /wp:list-item -->`.
**E non si ripara con un regex che aggiunge le chiusure mancanti**: nel tentativo le chiusure sono finite *prima* delle aperture e il danno è peggiorato (`mismatched_closing_block` a catena). Il rimedio deterministico che ha funzionato: **togliere tutti i marcatori di elenco** (apertura, chiusura, voce), poi **ricalcolarli dall'HTML** — estrarre le voci con `re.findall(r'<li>(.*?)</li>', interno, re.S)` e ricomporre `wp:list` + una voce per riga — e verificare che i conteggi di apertura e chiusura coincidano **prima** di inviare. Dopo la ricostruzione: `is_valid_gutenberg: true`, 0 problemi.
**Controllo minimo da fare su ogni articolo prima di inviarlo** (costa un secondo e ha evitato il problema): i marcatori `wp:paragraph`, `wp:list`, `wp:list-item` devono avere apertura e chiusura in numero identico.

**Lo schema FAQ va ricontrollato DOPO ogni scrittura di contenuto, non solo dopo averlo impostato.** Verificato il
29/09/2026 sull'articolo 1900: dopo un aggiornamento del contenuto via REST (`POST /wp/v2/posts` con il solo
`content`) il blocco `seo/faq` era integro e regolarmente reso in pagina, ma `seo/get-schema-data`
restituiva `faq: []` e l'analisi segnava «Ricchezza Schema: Article» invece di «Article, FAQ». Rimesso con
`update-schema-data` passando le stesse 5 voci: torna `Article, FAQ`. Quindi: **il blocco non è la prova che lo
schema c'è** — la prova è `get-schema-data`, da rileggere a fine lavoro su ogni articolo che contiene una FAQ.

**Il difetto `u003` e la sua correzione (chiuso sul sito il 25/09/2026).** Il testo corrotto è quello
**senza backslash**: nel blocco FAQ si legge `"answer":"u003cpu003eIl dominio è…u003c/pu003e"`, e il lettore
vede letteralmente **`u003cpu003e`** all'inizio della risposta. La forma corretta ha **un backslash per ogni
escape**: `"answer":"\u003cp\u003eIl dominio è…\u003c/p\u003e"`.

**Tre trappole della correzione, imparate sbagliando:**
1. **Sostituire il gruppo intero con un solo backslash non basta**: `u003cpu003e` → `\u003cpu003e` lascia il
   secondo escape scoperto e produce **una corruzione nuova** (il lettore vede `<pu003e`). Il backslash va
   aggiunto **a ogni token**: `\u003cp\u003e`, `\u003c/p\u003e`, e anche `\u003cstrong\u003e`,
   `\u003c/strong\u003e`, le liste e i corsivi — le risposte FAQ contengono grassetti, non solo paragrafi.
2. **Non contare le stringhe: decodificare l'attributo.** Il controllo che dice la verità è
   `json.loads()` del commento `<!-- wp:seo/faq {…} /-->` e la lettura della risposta come la vede il
   lettore. Un conteggio di `u003` resta ambiguo (può contare escape corretti come rotti).
3. **Il blocco e il meta si sincronizzano alla scrittura**: dopo il salvataggio via REST il campo
   `_sito_seo_faq` rispecchia il blocco, quindi si corregge **una volta sola** — ma il meta va riletto per
   confermarlo, perché è quello che alimenta il `FAQPage` (la prova sta anche nel JSON-LD della pagina).

**Dove guardare, in ordine:** il blocco nel contenuto (quello che il lettore vede) → il meta
`_sito_seo_faq`/`_sito_seo_howto` → il JSON-LD della pagina viva → e per chiudere, la scansione di tutto
il sito sul **testo visibile** (non sull'HTML: gli escape corretti dentro il JSON-LD sono normali).
**Stato al 25/09/2026: 33 pagine controllate, zero `u003` visibili** (erano 3: 1441, 1479, 222).

**Due interventi sullo stesso articolo non partono mai dallo stesso snapshot.** Se un articolo riceve due
scritture (per esempio due link in entrata da inserire in punti diversi), costruire il secondo payload dal
contenuto **riletto dopo la prima scrittura**: due payload derivati dalla stessa copia si annullano a
vicenda e la seconda scrittura cancella la prima, senza nessun errore — la risposta è `200` e il controllo
"link al bersaglio: 0" è l'unico che se ne accorge. *(Verificato il 25/09/2026 sui link in entrata: due
donatori che dovevano ricevere due link ciascuno ne avevano uno.)*

**In `uploads/` un glob `nome-1*` non è il doppione: prende anche le varianti ridimensionate.** Il 25/09/2026,
spostando i file del doppione `infographic-dns-timeline-1*`, sono finiti nella cartella di recupero anche
`infographic-dns-timeline-1024x687.png` e `-150x150.png`, che sono varianti dell'immagine **buona**
(`infographic-dns-timeline.png`), perché anche loro cominciano per `…-1`. **I file di un'immagine sono più
di uno per suffisso**: prima di spostare o cancellare si elenca, si confronta il suffisso con la lista
delle dimensioni attese (`-150x150`, `-300x201`, `-400x300`, `-768x515`, `-900x675`, `-1024x687`, `-1536x…`)
e si verificano **tutte** le voci del `srcset` dopo l'operazione, non solo il `src`.
**Rendere reversibile**: si sposta in una cartella di recupero (`/root/<descrizione>-<data>/`) invece di
cancellare, e si dice dove. *(Il controllo che l'ha preso: l'elenco dei file spostati confrontato con i nomi
attesi; i 4 file sbagliati sono stati ripristinati e i 24 URL di immagini di 227 tornano 200.)*

- **Il difetto `u003c`/`u003e` si controlla su tutto il sito, e si vede a occhio nudo in pagina.** È la firma
del blocco scritto via API (`\u003c` rimasto senza backslash dopo `wp_unslash`): il lettore legge
**`u003cpu003e`** all'inizio di una risposta o **`Impostazioni u003e Lettura`** in un passo. La scansione da
fare su ogni articolo pubblicato: contare le occorrenze di **`u003`** che restano **fuori dai commenti HTML,
dagli `<script>` e dai `<style>`** — le occorrenze dentro il JSON-LD sono normali (WordPress serializza con
JSON_HEX_TAG) e i commenti non si vedono. Verificato il 24/09/2026 sui 33 articoli: **3 con testo corrotto
visibile — 1441 (24 occorrenze, tutte le risposte FAQ), 1479 (20, tutte le FAQ) e 222 (1, un passo
HowTo)**. **L'aritmetica del conteggio dà la portata del danno solo se si sa cosa conta:** ogni **elemento
formattato** rotto lascia **4 marcatori** (apertura `u003cpu003e` + chiusura `u003c/pu003e`, cioè 2+2), quindi
**occorrenze ÷ 4 = elementi formattati rotti**. Attenzione: **non sono solo le risposte** — un `<strong>`, un
`<a>` o un `<em>` scritto via API aggiunge **4 marcatori ciascuno**. Verificato sul **1479**: 20 marcatori =
**4 risposte (16) + 1 coppia `<strong>` (4)**, e non 5 risposte come suggeriva il numero. **Se il conto non
torna con le domande dichiarate, la differenza è formattazione inline** — non una domanda in più. Rimedio: far **serializzare il blocco a WordPress** (`serialize_block` +
`wp_update_post(wp_slash( … ) )`) o inserirlo dall'editor — mai scrivere il commento a mano.

- **Il controllo del blocco FAQ si fa su tutto il sito, in un giro solo.** Il blocco rotto non si vede
  guardando la pagina: il commento `<!-- wp:seo/faq … /-->` resta nell'HTML **come commento** (quindi
  invisibile a chi legge) e la sezione esce **vuota**. Il test giusto è scaricare ogni post e cercare due
  stringhe: **`wp:seo/faq`** (blocco presente ma **non reso**) e **`seo-faq`** (classe del
  blocco reso). Se c'è la prima e non la seconda, la FAQ è rotta. Verificato il 24/09/2026 sui 33 articoli
  pubblicati: **1 solo rotto (il 215)**, tutti gli altri 32 a posto. Nello stesso giro si scoprono anche i
  `src` con il parametro di versione accodato due volte (`?v=…?v=…`, sempre su 215): rispondono 200 e non
  rompono niente, ma vanno ripuliti.

- **Sui contenuti tecnici il metodo viene prima dei rimedi**: il capitolo `Prima misura, poi ottimizza`
  dell'articolo 225 (misura, poi intervieni, poi rimisura) è ciò che distingue una guida da un elenco di
  consigli — ed è esattamente ciò che manca al 223, che elenca errori senza dire come si misurano prima e dopo.

## Blocchi, media, ambiente

- **Le liste vanno chiuse bene.** Un `<!-- wp:list-item -->` scritto al posto di `<!-- /wp:list-item -->`
  non dà errore al salvataggio: rompe l'annidamento e `gutenberg/validate-content` risponde
  `is_valid_gutenberg: false` con `unclosed_block`/`mismatched_closing_block`. Prima di salvare, passare
  il markup a un controllo di bilanciamento dei commenti (stack di aperti/chiusi, ignorando i blocchi
  auto-chiusi `<!-- wp:x … /-->`) e non fidarsi dell'occhio: è un refuso che si ripete.
  **Il bilanciamento va contato anche sui tag, non solo sui commenti**: inserendo un blocco paragrafo
  nuovo, il commento può risultare pari mentre il `<p>` resta senza `</p>` (verificato il 26/09/2026
  sul 222: 60 commenti di apertura e 60 di chiusura, ma 60 `<p>` contro 59 `</p>`). Prima di scrivere,
  controllare **tutte e quattro** le coppie: `<!-- wp:paragraph`↔`<!-- /wp:paragraph -->`, `<p>`↔`</p>`,
  `<!-- wp:heading`↔`<!-- /wp:heading -->`, `<!-- wp:list-item`↔`<!-- /wp:list-item -->`.
- **`/wp-json/wp-abilities/v1/abilities` è paginato e parziale**: 50 per pagina per default (`per_page`
  massimo 100) e mostra **87** abilità mentre l'MCP ne vede **288**. Per l'elenco vero:
  `mcp-adapter-discover-abilities`.
- **L'MCP non elenca 87 strumenti**: ne espone 3 (scopri / leggi / esegui). Le abilità si chiamano
  attraverso `mcp-adapter-execute-ability`.
- **L'endpoint delle abilità richiede l'application password**: senza, risponde 401.
- **Un PNG 4K pesa ~16 MB**: per il sito serve la versione ridimensionata (su macOS: `sips -z`).
- **Mai installare pacchetti Python nel venv di Hermes**: usare `~/seo-content/.venv`. Unica eccezione:
  `ddgs`, che la skill `duckduckgo-search` installa nel venv di Hermes e che va lasciato lì.
- **La chiave Google "express" non funziona sull'endpoint `generativelanguage.googleapis.com`**
  (risponde 403, "API non abilitata"): la via giusta è `vertexai=True` con l'SDK `google-genai`.
- **Scrapling stealth è lento**: ~22 s per pagina (browser vero). Per lavori in massa usare la
  modalità HTTP (0,1 s).
- **Sostituire un'immagine tenendo lo stesso nome file non basta**: Cloudflare continua a servire la
  copia in cache (stesso URL, byte vecchi — verificato il 19/09/2026 sulle tre infografiche della
  bozza 1452). Sequenza giusta: cancellare il media vecchio con `media/delete` + `force: true`,
  ricaricare le nuove con `media/upload-base64` **con lo stesso nome**, e poi **aggiungere
  `?v=AAAAMMGG` all'URL dentro l'articolo** (il nome del file non cambia) o purgare la cache di
  Cloudflare. Verificare con `curl -s -o /dev/null -w '%{size_download}'` che i byte siano i nuovi.
- **`content/list-posts` è paginato: un elenco di una pagina non è «l'elenco».** Il glossario ha **133 voci** e la prima pagina ne restituisce **100**, ordinate dalla più recente, quindi **le voci più vecchie non compaiono**. Verificato il 29/09/2026 dichiarando assente la voce **«Allucinazione»** (id **871**, pubblicata l'11 settembre) mentre esisteva ed era pubblicata. **Prima di dire «non esiste»: paginare fino in fondo o usare `search`** — vale per il glossario, per gli articoli e per qualunque elenco. Lo stesso vale per `/wp-json/wp-abilities/v1/abilities` (50 per pagina, 87 visibili su 288 reali).
- **Il campo `meta` dell'API REST **nasconde** i tre metadati SEO più importanti: leggerli da lì fa concludere che non ci siano.** Con `GET /wp-json/wp/v2/posts/<id>?context=edit&_fields=meta` il plugin espone **solo** `_sito_seo_faq`, `_sito_seo_howto` e `footnotes`: **`_sito_seo_title`, `_sito_seo_description` e `_sito_seo_focus_keyword` non compaiono affatto**. Chi legge quei tre campi dal `meta` del REST **non li trova e li dichiara mancanti** — verificato il 29/09/2026 sulla **pubblicata 215**, dichiarata «senza titolo SEO, description e keyword» mentre aveva tutti e tre (51 caratteri, 152 caratteri e `programmi di affiliazione`) più `BlogPosting` e `FAQPage`. **I metadati SEO si leggono solo con `meta/get-post-meta`**, sempre, anche quando il `meta` del REST sembra aver risposto: i due elenchi di chiavi **non coincidono**, e la differenza sono proprio le tre chiavi che contano.
- **Nel contenuto a blocchi non si scrive markdown: `**grassetto**` esce con gli asterischi in pagina, e nessun controllo se ne accorge.** Verificato il 29/09/2026 sulla bozza 1967: 44 occorrenze di `**…**` nel corpo, `validate-content` rispondeva `is_valid_gutenberg: true` con 0 problemi, l'analisi SEO non segnalava niente, **e il lettore vedeva gli asterischi**. Il grassetto è `<strong>` (o il pulsante dell'editor), mai il markdown. **Controllo da fare sull'ultima versione inviata, prima di dire che è pronta:** `contenuto.count('**') == 0`, insieme a `{{` e `u003`.
- **Un'immagine inserita «dopo una frase» finisce dentro il `<p>`: va inserita dopo il commento di chiusura del blocco.** Verificato il 29/09/2026 sulla bozza 1967: ancorando l'inserimento al testo di un paragrafo, il `<figure>` è finito **dentro il `<p>`**, cioè HTML non valido che il browser spezza da solo — e `validate-content` diceva comunque `is_valid_gutenberg: true` con 0 problemi. **L'ancora giusta è `</p>` insieme al suo `<!-- /wp:paragraph -->`**, e il controllo dopo ogni inserimento è una riga: nessun `<figure>`, `<div>`, `<table>`, `<ul>` o `<ol>` dentro un `<p>`.
- **I nomi dei parametri cambiano fra l'abilità MCP e il REST: usare quelli dell'endpoint, non quelli dell'abilità.** Creando una bozza con `POST /wp-json/wp/v2/posts` non si passa `category_ids` né `featured_image_id` (i nomi dell'abilità `content/create-post`) ma **`categories`** e **`featured_media`**: con i nomi dell'abilità **la richiesta risponde `201` e ignora i due campi in silenzio** — la bozza nasce con `categories: [1]` (la categorial sito, che è riservata) e `featured_media: 0` (verificato il 29/09/2026 sull'articolo 1930: servita una `POST` di correzione con `{"categories":[2],"featured_media":1929}`). **Dopo ogni creazione, rileggere sempre `categories` e `featured_media`** e non fidarsi del `201`.
- **La generazione delle immagini può rispondere `429 RESOURCE_EXHAUSTED` e non è un guasto dello script**: è la quota di `gemini-3-pro-image` esaurita (capita subito dopo una generazione riuscita, es. copertina + infografica di fila). **Il rimedio che funziona è aspettare ~90 secondi e rilanciare lo stesso comando** — verificato il 29/09/2026 sulla bozza 1930 (primo tentativo 429, secondo riuscito). Non cambiare prompt né script al primo 429.
- **`media/upload-base64` vuole `filename`, `mime_type` e `base64`** (il campo si chiama `base64`,
  non `data`); con i parametri sbagliati risponde "è una proprietà obbligatoria di input" e non carica
  niente. Accetta anche `title`, `alt_text`, `caption`, `description`, `post_id`.
- **Prima di cancellare un media, cercare chi lo usa**: `wp db query "SELECT ID,post_status FROM
  wp_posts WHERE post_content LIKE '%nome-file%'"` in sola lettura (nella 1452 i tre file erano usati
  solo dalla bozza stessa).
- **Non pubblicare mai**: solo bozze, e ogni scrittura richiede l'ok dell'autore per quella singola azione.

- **Le immagini si controllano una per una su tutto il sito, non a occhio.** Le immagini rotte si vedono solo
  scaricandole: il controllo da fare è elencare i `wp-content/uploads` di ogni articolo pubblicato e chiedere
  il codice a ognuno. Verificato il 24/09/2026 su 33 articoli e **148 immagini: 3 rotte, in 3 articoli**
  (217, 226, 227). **Le due cause tipiche, entrambe con firma riconoscibile:** (a) il **suffisso `-1`** che
  WordPress aggiunge quando carica un file con un nome già occupato — la pagina punta al nome vecchio
  (`…-v3.png` → 404, 217) mentre il file buono è `…-v3-1.png`, ed è riconoscibile perché l'ID nel `class`
  dell'`img` (`wp-image-497`) è lo stesso dell'allegato vero; (b) **underscore invece di trattino** nel nome
  del file: **226** punta a `infographic_impatto_numero.png` mentre in libreria c'è
  `infographic-impatto-numero.png`, e **227** punta a `infographic_flusso_8_passi.png` contro
  `infographic-flusso-8-passi.png` — **stessa causa, stessa serie di file, si sistemano nella stessa
  passata**. Per trovare il file vero: `REST /wp/v2/media?search=<parte del nome>`.

- **Le immagini si servono ridimensionate: il modello è il 585.** È l'**unico** articolo del sito che punta alla
  variante che WordPress genera al caricamento (`-1024x687`): **222 KB in cinque immagini contro 304 KB dei file
  pieni**. Ovunque altrove si serve il file intero (227: 334 KB in cinque; 224: 237 KB in quattro). Il controllo
  da fare è doppio — codice **e** peso della variante servita contro il file pieno — e il risparmio va scritto
  nel rapporto, perché è la prova che la pratica giusta è già in casa.

- **Ma il caso più frequente è il contrario del 585: le varianti ci sono e non si usano.** Sul **684** la pagina
  serve i file pieni (71 + 57 KB) mentre le `-1024x687` **esistono già** sul server (53 + 42 KB): **33 KB
  disponibili e non usati**, e la correzione è **solo il cambio di `src`**, senza ricaricare niente — verificato
  anche sul **1412** (41 KB: 137 → 96) e sul **1452** (68 KB: 242 → 174, **il peso più alto su una singola
  pagina del sito**, con tre immagini). Quindi il controllo va fatto in due tempi: (1) la variante ridimensionata
  **esiste**? (2) la pagina **la usa**? Il risparmio va sempre quantificato in KB nel rapporto. Attenzione al
  caso del 1452: la pagina porta già `?v=AAAAMMGG` sulle immagini (antifurto di cache) **e nello stesso gesto ha
  lasciato il nome del file pieno** — il parametro non sostituisce la variante, si cambia il nome e il `?v=`
  resta.
  **Il terzo esito possibile è «la variante non esiste», e va distinto dal «non si usa»**: sul **1479** le tre
  infografiche `autorita-*` rispondono **404** sulla variante ridimensionata — **niente da cambiare, niente da
  recuperare**. Sul sito convivono **tre pipeline di nomi** (`infographic-` per 226/227, `infografica-` per
  585/1412/1452, `autorita-` per 1479): se la variante manca, va **rigenerata** o **deciso consapevolmente di non
  averla**, ma va scritto nel rapporto che il controllo è stato fatto.

## Domanda e query: i segnali della SERP

- **Il segnale «Mancanti: <parola>» nella SERP dice che una query è scoperta.** Il 24/09/2026, sotto il terzo
  risultato di `keyword research per affiliazione`, Google annotava **«Mancanti: affiliazione · Deve includere:
  affiliazione»**: significa che **le pagine in prima posizione non contengono la parola**. Quando compare, è
  **la prova misurata che la query è sotto-servita** — e va scritta nel rapporto insieme al fatto che il titolo
  dell'articolo **la parola ce l'ha già** (il 1452: `Keyword research per affiliazione: metodo in 10 passi`).

- **I 15 suggerimenti non bastano: guarda CHI digita la frase.** Una query di riferimento può essere un
  **falso amico**: la riga 102 (*Scrivere una recensione di prodotto che converte*) ha per query `come scrivere una
  recensione`, che dà **15 suggerimenti** — ma sono **tutti lato consumatore** («su booking», «su google», «su
  airbnb», «positiva per un medico», «esempio»): chi digita quella frase vuole recensire una *piattaforma*, non
  scrivere un articolo con link di affiliazione. **Il numero di suggerimenti misura la domanda, non l'intento:**
  **prima di scrivere, leggi le cinque completamenti e chiediti se chi li digita è il pubblico dell'articolo**.
  Lo stesso giorno lo stesso schermo: `zerogpt` → 14 suggerimenti fra cui **«è affidabile»**, e *quella* è la
  domanda del pubblico — la riga 119 è stata piegata su di lei (`rilevatore IA`, 15). Casi gemelli già in archivio:
  **`manutenzione wordpress`** (intento «il mio sito è rotto») e **`allucinazioni`** (parola medica).

- **La metrica di sovrapposizione ha falsi negativi quando il vocabolario cambia: il verdetto è la lettura.**
  Tre righe sono passate indenni dall'audit automatico e **solo leggendo le due pagine** si è visto il duplicato:
  **109** vs la pubblicata **227** (che ha già «migrare senza fermare il sito»), **107** vs la bozza **1844** (che
  ha già «Quanto costa ChatGPT Plus in Italia?»), **81** vs **223+1623**. Il segnale grezzo che li avrebbe
  intercettati è **il titolo**, non il corpo: **quando due contenuti condividono due parole di sostanza nel titolo,
  vanno letti**. E vale anche al contrario: la **105** era segnalata con due parole in comune con la **226**, ma
  leggendola la 226 parla di **plugin**, non di temi né page builder — **non era un duplicato**. **Una metrica di
  corpo segna le righe da verificare, non prova il duplicato: non si rimuove senza aver letto le due pagine.**

- **Il REST espone `meta` ma NON le chiavi SEO: il controllo «senza titolo/description/keyword» fatto così è un falso allarme.**
  `GET /wp-json/wp/v2/posts?context=edit&_fields=id,meta` restituisce solo **`_sito_seo_faq`**, **`_sito_seo_howto`**
  e `footnotes` — verificato il 30/09/2026 su 1977, 202, 1623, 1593, tutte con lo stesso elenco.
  `_sito_seo_title`, `_sito_seo_description`, `_sito_seo_focus_keyword` e `_sito_seo_schema_type`
  **non passano dal REST**: chi li cerca nel campo `meta` li trova **vuoti su tutti i contenuti** e conclude
  che 67 articoli sono senza SEO (**esattamente quello che è successo la prima volta**). Le fonti vere sono tre:
  l'**HTML pubblico** (`<title>`, `<meta name="description">`, `<meta name='robots'…` — per i pubblicati),
  **`meta/get-post-meta`** con **`keys` obbligatorio** (per bozze e campi singoli), e
  **`seo/get-schema-data`** per il tipo di schema. Per il quadro d'insieme:
  **`seo/get-site-seo-summary`** (`posts_without_meta`, `posts_without_keyword`) — ma conta
  **articoli + pagine insieme** (`total_published: 45` = 37 articoli + 8 pagine, 30/09/2026), quindi i
  «senza meta» possono essere pagine di servizio.

- **Il calendario non è una fonte: è un documento che va riconciliato col sito.** Verificato il 30/09/2026,
  quattro difetti nella stessa tabella: **una riga fantasma** (id 32, `Draft`, `wp_post_id=577`: il 577 non
  esisteva in nessuno stato e non era una pagina), **3 pubblicati senza riga** (1593, 1603, 1613),
  **34 righe con `article_slug` e `article_title` vuoti** (residui del calendario del 19/09) e **uno slug
  sbagliato**. Prima di dire «la coda è in ordine» va fatto il confronto `wp_post_id ↔ id` nei due sensi,
  con controllo di slug e stato, e vanno riempiti i campi dai dati del sito — non inventati. Dopo la
  riconciliazione: 42 `Scheduled`, 37 `Published`, 30 `Draft`, 13 `Idea`, zero incoerenze.

## Bozze: come si verificano

- **Le bozze si verificano con lo stesso metodo, ma tre passi non si applicano e tre cose si aggiungono.** Non
  applicabili: **Search Console** (una bozza non è indicizzata: **il dato non esiste, non si stima**), i **link in
  entrata** (nessuno può citare una bozza) e la **pagina pubblica** — meta e schema si leggono dai campi con
  `meta/get-post-meta` (**`keys` è obbligatorio**) e `seo/get-schema-data`, le immagini dalla
  **libreria media**. Si aggiungono: (1) **il flusso di creazione, non il singolo articolo**:
  **`_sito_seo_keyword` vuoto, `schema_type: Article` e `howto` vuoto su tutte e nove** (24/09/2026), mentre i
  33 pubblicati hanno la keyword — **va corretto a monte, non nove volte a valle**; (2) **il confronto con i
  pubblicati**, perché la sovrapposizione si può ancora evitare; (3) **la regola dei nomi**: il pubblico cerca
  **per nome** (`cloudflare` 15 suggerimenti, `hosting condiviso aruba`, `plugin` + funzione) e **gli articoli
  rispondono per categorie** — **1629 non nomina Cloudflare né Aruba, 1623 nessun fornitore, 1529 nessun plugin**:
  **tre casi indipendenti, è una regola di scrittura della casa**, i nomi vanno scritti dove sono informazione.
  **L'avviso `faq_schema_missing_risk` su una bozza resta un falso positivo noto**: il campo `faq` dice la verità.
  *(Suggerimenti sbagliati e sigle ambigue, suffissi delle varianti immagine, trappole delle abilità MCP:
  `references/nomi-e-query.md`.)*
