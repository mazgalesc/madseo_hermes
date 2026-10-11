# Rapporto: le infografiche dentro gli articoli di il-tuo-sito.it

Analisi del 19/09/2026. Gli articoli pubblicati sono 30, **tutti** contengono almeno
un'immagine interna: **105 immagini in totale, tutte distinte**, con nomi tipo
`infographic-…` / `infografica-…`. Ne ho scaricate e misurate **101** (96 MB); 3 non esistono più
con il nome originale e 1 era un riferimento malformato nel codice della pagina.

## 1. Dati misurati

| Cosa | Valore |
|---|---|
| Immagini | 101 analizzate (tutte PNG) |
| Formato | **1264×848** fisso (qualcuna 1200×848, fino a 1264×896) → ~**3:2** orizzontale |
| Luminosità mediana | **215 su 255** → fondo **chiaro** (97 su 101 chiare, **nessuna scura**) |
| Saturazione | **0,085** → colori molto calmi |
| Pixel colorati | **11%** in mediana (da 0% a 45%) → il colore è negli **accenti**, non nel fondo |
| Peso per file | ~1 MB di mediana |
| Fondo | **bianco #ffffff** con riquadri grigio-lavanda chiarissimi (#f0f1f5, #f1f2f6, #eff0f4) |
| Colore d'accento | **blu indaco**: #3343aa, #455abb, #3f44a2, #3340b3, #374389 (e navy #262666) |

## 2. Com'è fatta un'infografica di il-tuo-sito.it

**Tipo**: schemi didattici, non illustrazioni. Le forme ricorrenti:
- **confronto a due colonne** con card affiancate (tema classico / tema a blocchi)
- **card in fila** (4 riquadri orizzontali, uno per concetto, con icona + titolo + riga di testo)
- **matrice / tabella** (per esempio compatibilità plugin × versione PHP, con simboli invece di parole)
- **blocco schematico** con 2-3 card blu navy e didascalie
- **flusso numerato a passi**

**Componenti ricorrenti**:
- fondo grigio chiarissimo, **card bianche con angoli arrotondati e ombra morbida**
- **badge/pill colorati** per le etichette (viola #4F46E5, nero #111827)
- card **blu navy (#26235B) con testo bianco** per i concetti principali
- **icone piatte** blu (ingranaggi, database, monitor, pennello, puzzle, razzo, megafono)
- **simboli di stato**: spunta ✓, triangolo di avvertimento, X in cerchio — usati al posto delle parole
- **link e accenti blu** (#2563EB) accanto al blu indaco del marchio

**Tipografia**: sans-serif moderna (tipo Inter/Roboto), **titolo in maiuscolo e grassetto**,
intestazioni in grassetto nero (#111827), testo di supporto in grigio (#6B7280).

**Testo**: al contrario delle copertine, qui **il testo abbonda** — titolo, sottotitolo, etichette,
spiegazioni, note a piè di pagina in italiano.

## 3. Cosa ho verificato sulla generazione

Ho provato a **generare** un'infografica con il modello di immagini (`gemini-3-pro-image`),
con la stessa ricetta stilistica e con testo italiano dentro.

**Risultato: il testo è uscito corretto e leggibile.** Trascritto dall'immagine generata:

> COSA SERVE PER INIZIARE UN BLOG DI AFFILIAZIONE
> 1. NICCHIA — Identifica un argomento specifico e profittevole per un pubblico mirato.
> 2. CONTENUTI — Crea articoli utili, guide e recensioni di alta qualità e valore.
> 3. HOSTING — Scegli un servizio affidabile e veloce per ospitare il tuo sito web.
> 4. LINK AFFILIAZIONE — Iscriviti a programmi di affiliazione e inserisci i link nei tuoi contenuti.

Nessun errore di ortografia, nessuna lettera sbagliata, niente testo inventato. Quindi la via
"modello di immagini" è **percorribile anche per le infografiche**, non solo per le copertine.

Due avvertenze pratiche:
- il modello ha disposto le 4 card in **2×2** invece che in fila: la disposizione va chiesta in modo
  esplicito e comunque verificata a vista
- il testo è più piccolo se l'immagine viene ridimensionata al formato di casa: conviene generare
  in **2K o 4K** e ridurre a 1264×848, così i caratteri restano nitidi

## 4. Ricetta per generare un'infografica coerente

Parametri: `gemini-3-pro-image`, `aspect_ratio="3:2"`, `image_size="2K"` (o 4K), poi ridimensionare
a **1264×848**.

Struttura del prompt:

> Infografica didattica in italiano, formato orizzontale. Titolo in alto, **in maiuscolo e
> grassetto**. Sotto, **{numero} card** disposte **in fila** su sfondo **grigio chiarissimo**:
> card **bianche, angoli arrotondati, ombra morbida**, ognuna con **icona piatta blu indaco**,
> titolo in grassetto e una riga di spiegazione. Palette **blu indaco #3343aa**, testo nero e
> grigio, tipografia **sans-serif** moderna, stile vettoriale pulito e professionale.
> Titoli delle card: **{elenco}**.

## 5. Confronto con le copertine (le due famiglie)

| | Copertine | Infografiche |
|---|---|---|
| Formato | 1408×768 (~16:9) | 1264×848 (~3:2) |
| Fondo | **scuro** (indaco #292655) | **chiaro** (bianco/grigio) |
| Colori | indaco + **oro** | indaco/blu + bianco e grigio |
| Con o senza testo | **senza testo** | **con molto testo** |
| Genere | illustrazione/metafora | schema didattico |

Le due famiglie **condividono la stessa famiglia di colore** (indaco) ma con ruoli opposti: la
copertina è l'immagine d'impatto dell'articolo, l'infografica è la spiegazione da leggere dentro.
Questo va tenuto distinto nella skill: non sono lo stesso tipo di immagine.

## File di lavoro

- `~/seo-content/audits/infografiche/` — le 101 infografiche scaricate
- `~/seo-content/audits/analisi-infografiche.json` — misure per immagine
- `~/seo-content/audits/immagini-interne.json` — quali immagini stanno in quale articolo
- `~/seo-content/audits/prova-infografica-testo.png` — l'infografica di prova generata
