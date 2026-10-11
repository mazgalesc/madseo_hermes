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
