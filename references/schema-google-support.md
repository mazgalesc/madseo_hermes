# Tipi di schema Google: cosa supporta davvero (verificato 19/09/2026)

Fonte: galleria ufficiale `https://developers.google.com/search/docs/appearance/structured-data/search-gallery?hl=it`
(aggiornata 24/06/2026). Le 25 funzionalità valgono **globalmente**: non esistono funzionalità
riservate ad altri paesi che l'Italia non abbia.

## Le 25 funzionalità supportate

Articolo · Breadcrumb · Carosello · Elenco di corsi · Set di dati · Forum di discussione ·
Domande e risposte didattiche · Valutazione complessiva del datore di lavoro · Evento ·
Metadati immagine · Offerta di lavoro · Attività locali · Risolutore matematico · Film ·
Organizzazione · Prodotto · Pagina del profilo · Domande e risposte · Ricetta · Snippet recensione ·
App software · Speakable · Contenuti in abbonamento/paywall · Casa vacanze · Video

## Ritirate: non producono più nulla di visibile

| Funzionalità | Quando | Cosa fare nel contenuto |
|---|---|---|
| **FAQ** | 7 maggio 2026 (limitate dal 2023 a siti governativi/sanitari) | Dichiarare `FAQPage` per far capire la pagina alle AI; **non promettere** il menu a tendina |
| **HowTo** | 2023 | Uguale: utile come descrizione per le macchine |
| **Casella di ricerca nei sitelinks** | 21 novembre 2024 | Il `WebSite` + `potentialAction` è diventato codice morto: innocuo |

Il markup ritirato resta valido: nessun errore in Search Console, nessuna penalizzazione.

## Proprietà obbligatorie da non dimenticare

- **Ricetta**: `name`, **`image`**, `recipeIngredient`, `recipeInstructions` (immagine obbligatoria!)
- **Prodotto**: `name` + almeno uno tra `offers` / `review` / `aggregateRating`
- **Evento**: `name`, `startDate`, `location`
- **Offerta di lavoro**: `title`, `description`, `datePosted`, `hiringOrganization`, `jobLocation`
- **Corso**: `name`, `description`, **`provider`**
- **Attività locale**: `name` (+ indirizzo, telefono, orari consigliati)
- **Video**: `name`, `thumbnailUrl`, `uploadDate` + `contentUrl`/`embedUrl`
- **Articolo**: `author`, `datePublished`, `headline` (+ `image`, `publisher.logo` consigliati)
- **Breadcrumb**: `itemListElement` con `position`, `name`, `item`

## Solo per l'SEE (Italia inclusa), e solo per aggregatori

Unità di aggregatori, unità di fornitori, carosello di ecosistemi, siti di offerte di lavoro,
caroselli di dati strutturati: valgono per hotel, voli, treni a lunga percorrenza, prodotti,
meteo/sport/finanza, attività locali — ma **solo per VSS/OTA/servizi di shopping comparativo/
directory approvati con feed di dati**. Non si ottengono con il markup e non riguardano un blog.

## Promemoria per gli articoli

Per un blog le funzionalità che contano sono poche: **Articolo**, **Breadcrumb**,
**Organizzazione**, **Video** (se c'è un video) e i dati che servono a farsi citare dalle AI
(FAQ, HowTo). Tutto il resto (Prodotto, Ricetta, Corso, Evento, Offerta di lavoro, Attività locale)
solo se il sito ospita davvero quei contenuti.

## Quale schema scegliere, articolo per articolo

**Se cerchi solo «cosa non dà più risultati visibili», la tabella è qui sopra.** Questa sezione è la
scelta tipo per tipo, con i nomi dei campi veri dell'abilità e le regole pratiche.

**Decidere lo schema fa parte della scrittura dell'articolo, non è un passaggio a parte.** Si imposta
con `seo/update-schema-data`, che ha **14 campi** (i nomi veri, come li restituisce
`mcp-adapter-get-ability-info`): `post_id`, `schema_type`, `speakable`, `faq`, `howto`, `video`,
`product`, `job`, `event`, `course`, `recipe`, `robots`, `canonical_override`, `breadcrumb_label`.

Valori ammessi per `schema_type`: `''` (usa il default del sito), `Article`, `BlogPosting`,
`NewsArticle`, `TechArticle`, `ScholarlyArticle`, `Report`, `WebPage`, `Product`, `JobPosting`,
`Event`, `Course`, `Recipe`, `LocalBusiness`.

**`FAQ` e `HowTo` non sono tipi**: sono blocchi che si aggiungono al tipo. Si mettono **solo se il
contenuto si vede davvero nella pagina** (regola di Google): la FAQ per una sezione di domande e
risposte, lo HowTo per una procedura numerata passo passo.

| Tipo di articolo | `schema_type` | Blocchi aggiuntivi |
|---|---|---|
| Articolo di blog o guida (il caso normale) | `BlogPosting` | — |
| Pagina lunga di approfondimento che non è un post di blog | `Article` | — |
| Guida molto tecnica, per chi già conosce l'argomento | `TechArticle` | — |
| Articolo con sezione domande e risposte | `BlogPosting` | **FAQ** (una voce per domanda) |
| Procedura passo passo ("come installare…", "come migrare…") | `BlogPosting` | **HowTo** (con i passi reali) |
| Confronto o recensione di uno strumento/prodotto | `BlogPosting` | `product` se riguarda un prodotto specifico |
| Contenuto con video incorporato | `BlogPosting` | **video** |
| Pagina di servizio (contatti, documentazione) | `WebPage` | — |

**Aggiornamento 2026 — FAQ e HowTo non danno più risultati arricchiti (verificato il 19/09/2026):**
Google ha ritirato i risultati delle **FAQ il 7 maggio 2026** (dopo averli già limitati nel 2023 ai siti
governativi e sanitari) e delle **HowTo** già nel 2023. Dal giugno 2026 il Rich Results Test non
supporta più le FAQ e il rapporto dedicato è stato tolto da Search Console. **Il markup resta valido**
(non genera errori, non è una violazione, Google continua a leggerlo per capire la pagina) ma **non
promettere risultati visibili**: nell'articolo si dichiara FAQ/HowTo per far capire la pagina alle
macchine e alle risposte AI, non per il menu a tendina. Fonte:
`https://developers.google.com/search/updates` (voce del 7 maggio 2026).
Chi vuole un risultato visibile investe su Article, Product e recensioni, Event, LocalBusiness,
Breadcrumb, Video: quelli ci sono ancora.

**Regole pratiche**
- **gli articoli di questo sito sono `BlogPosting`**: è il sottotipo di `Article` previsto per un post di
  blog, ed è quello che il sito usa — verificato il 17/10/2026 su **10 articoli su 10** (pubblicati e bozze).
  Il valore `''` lascia il default del sito: si scrive `BlogPosting`, e **si rilegge** per confermarlo
- **se l'articolo contiene una FAQ, lo schema FAQ va messo** (verificarlo sul contenuto o con
  `seo/get-schema-data`, non sulla pagina resa di una bozza)
- lo schema deve **descrivere quello che si vede**: niente FAQ o HowTo su contenuti che non li hanno
- **nei blocchi `howto` i campi che non servono si lasciano fuori, non si riempiono con un default.** Un
  HowTo salvato senza dire niente sui costi resta con **`cost_currency: "USD"`**: verificato il 17/10/2026, gli
  articoli **1441** e **1479** hanno il blocco con `total_time: ""`, `estimated_cost: ""` e
  **`cost_currency: "USD"`**, mentre il **224** — dove i campi sono stati riempiti — è in **`EUR`**
  (`total_time: "PT4H"`). Quindi il dollaro è il default che resta quando non si sceglie niente. Se il
  contenuto non parla di costi, i campi di costo non si mandano; e dopo la scrittura si rilegge il blocco
- i breadcrumb sono disattivati sul sito e Local Business non è configurato: non impostarli per ora
- dopo la scrittura, **rileggere** con `seo/get-schema-data` per confermare
