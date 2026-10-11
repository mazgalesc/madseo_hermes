# Rapporto: le immagini in evidenza di il-tuo-sito.it

Analisi del 19/09/2026 su **30 articoli pubblicati** — tutti hanno una copertina, 30 immagini
distinte. Metodo: elenco via REST WordPress, scarico delle immagini originali, misura dei colori
(luminosità, saturazione, palette) e lettura visiva di un campione rappresentativo.

## 1. Dati misurati

| Cosa | Valore |
|---|---|
| Copertine analizzate | 30 (35 MB in totale) |
| Formati più usati | **1408×768** (14 volte), **1376×768** (8) — cioè ~16:9 |
| Altri formati | 1264×848 (4, ~3:2), 768×419 (2), 2528×1696 (1), 1536×1024 (1) |
| Luminosità media | **89 su 255** → copertine scure (minima 50, una sola chiara a 217) |
| Saturazione media | 0,46 → colori pieni ma non accesi |
| Quota di bianco | **0,00** → nessuna area bianca: **non c'è testo sopra le immagini** |
| Colore dominante | **#292655** e famiglia (#282359, #292758, #2c2559, #2f2762) |

## 2. Lo stile di casa (dalla lettura visiva)

**Tipo**: illustrazione **vettoriale flat** con gradienti morbidi e bagliori luminosi — a volte
line-art con effetto neon (contorni sottili luminosi). **Mai fotografie, mai render 3D realistici.**

**Sfondo**: blu notte / viola indaco con **gradiente radiale** (più chiaro al centro, più scuro ai
bordi), spesso con una **griglia a globo**, linee curve concentriche e piccole scintille o
particelle. Superficie piatta, nessuna texture: la profondità la fanno i bagliori.

**Colori**: base blu-viola scura; **oro/giallo caldo riservato alle luci e all'elemento chiave**;
lavanda e lilla per i terreni e le sfumature; bianco puro solo per il logo.

**Logo WordPress**: presente in molte copertine (cerchio blu scuro con la W bianca), come elemento
centrale nel tema "sicurezza/SEO", oppure assente quando il soggetto è una metafora narrativa.

**Testo**: **nessun testo, nessun titolo, nessun wordmark** in nessuna delle copertine viste.

**Composizione**: due schemi ricorrenti —
- **centrale e simmetrica con raggiera** (soggetto al centro, icone disposte ad anello attorno);
- **diagonale narrativa** (un sentiero o una direzione che porta lo sguardo dal basso a sinistra
  verso l'alto a destra, con la luce come guida).

**Metafore usate**: crescita e prosperità (albero con monete d'oro), velocità e prestazioni (razzo,
tachimetro), sicurezza (scudo, lucchetto, impronte), accesso e sblocco (chiave, porta aperta, globo
a wireframe), analisi e SEO (lente, grafici, catena di link).

## 3. Ricetta per generare una copertina coerente

Parametri: `gemini-3-pro-image`, `aspect_ratio="16:9"`, `image_size="4K"`.
Poi si ridimensiona per il web a **1408×768** (il formato di casa) — il 4K resta come master.

Struttura del prompt (in italiano, funziona bene):

> Immagine di copertina per un articolo di blog italiano su **{argomento}**. Illustrazione
> vettoriale flat moderna con gradienti morbidi e bagliori, stile 2.5D, **non fotografica**.
> Sfondo blu notte / viola indaco (#292655) con gradiente radiale più chiaro al centro, sottile
> griglia a globo o linee curve concentriche e piccole scintille. Soggetto centrale: **{metafora}**.
> Accenti **oro/giallo caldo** come unica fonte di luce. Logo WordPress stilizzato (cerchio blu
> scuro con W bianca) se pertinente. Composizione **centrale e simmetrica** (oppure diagonale).
> Ampio spazio negativo. **NESSUN TESTO, nessuna scritta, nessun wordmark.**

## 4. Note pratiche

- il PNG 4K pesa ~16 MB: per il sito serve la versione ridimensionata (1408×768, poche centinaia di KB)
- le copertine del sito sono **scure**: se il tema del sito ha sfondo chiaro, la copertina scura
  resta coerente perché è il formato che i lettori conoscono — non cambiarlo senza motivo
- l'uniformità è alta: 20 copertine su 30 sono nel formato ~16:9, e la palette indaco è presente in
  tutte. Una copertina con colori diversi (per esempio chiara su fondo beige come la 170) è
  l'eccezione, non la regola

## File di lavoro

- `~/seo-content/audits/copertine/` — le 30 copertine originali
- `~/seo-content/audits/analisi-copertine.json` — misure per immagine
- `~/seo-content/audits/articoli.json`, `media.json` — elenchi dal sito
