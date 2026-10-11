# Immagini: due famiglie, due stili

Estratto da SKILL.md per dimensione. Contenuto invariato (aggiornato al 23/09/2026).

Entrambe si generano con `gemini-3-pro-image` (SDK `google-genai`, `vertexai=true, api_key=$GOOGLE_API_KEY`).
Script in `scripts/`, da lanciare con `~/seo-content/.venv/bin/python`.

## ⚠️ La chiave delle immagini è OPZIONALE (verificato l'11/10/2026 sulle fonti ufficiali)

La generazione di immagini **non è nel livello gratuito dell'API** e **l'abbonamento consumer non la copre**.
Verificato su `ai.google.dev/gemini-api/docs/pricing` e sulla pagina «Google AI plans»:

- per i modelli di immagini (`gemini-3.1-flash-image`, `gemini-3.1-flash-lite-image`, `gemini-3-pro-image`,
  `gemini-2.5-flash-image` — la famiglia si chiama **Nano Banana**) la colonna **Free Tier dice
  «Not available»**: senza fatturazione cloud non si generano immagini via API;
- **Imagen è spenta** («no longer available through the Gemini API»): i modelli di immagini sono solo i Nano Banana;
- i piani **Google AI Pro / Ultra danno più quota e più modelli dentro AI Studio**, ma **non coprono l'uso
  dell'API**: la pagina ufficiale dice che quando le quote del piano finiscono in AI Studio si continua
  «using a Gemini API key **with Cloud Billing enabled**». Abbonamento e API sono due sistemi di fatturazione
  separati (confermato anche dal forum degli sviluppatori Google).

**Quindi, finché la chiave non c'è, la strada è questa:**

1. **Generazione a mano, con l'abbonamento che c'è già** (Google AI Pro copre l'app Gemini e AI Studio):
   lo script produce il **prompt pronto** nella forma che serve (`--prompt` con lo stile di casa: vedi le
   sezioni «Copertine» e «Infografiche» qui sotto e le ricette in `stile-copertine.md` /
   `stile-infografiche.md`), l'autore genera l'immagine **nella app o in AI Studio**, e il file viene salvato in
   `~/seo-content/content/` con il nome dell'articolo. Da lì il percorso è **identico** (ridimensionare a
   1408×768 o 1264×848, convertire in WebP, caricare).
2. **Chiave API con fatturazione cloud**: ~**0,10 $ per immagine 2K** e ~0,15 $ per la 4K (listino ufficiale:
   $0.101 per 1K, $0.151 per 4K per il modello 3.1 Flash Image). È la strada che rende gli script automatici.
3. **Alternative gratuite**: da esplorare (i servizi gratuiti senza registrazione si fermano con 402 dopo
   poche immagini — vedi il test del `1867`). **Non** promettere all'autore un risultato prima di averlo provato.

**Regola**: la generazione delle immagini **non blocca** il resto del lavoro. Se la chiave non c'è, l'articolo
si scrive lo stesso; si dichiara «immagini: da generare» e si va avanti — mai inventare un'immagine che non
esiste né riusare quella di un altro articolo (regola qui sotto).

## La versione per il web è **WebP**, non PNG (regola dell'autore, 21/09/2026)

**Aggiornamento 23/09/2026: la conversione la fal sito da sé.** Caricando il PNG ridimensionato su
`POST /wp-json/wp/v2/media` (corpo binario + `Content-Disposition: attachment; filename="…-web.png"`),
la risposta torna **già in WebP** (`source_url` che finisce in `-web.webp`, `mime_type: image/webp`) e pesa
30-50 KB contro 1,0-1,2 MB del PNG. Quindi: **non** convertire a mano con `cwebp` prima di caricare, e
non stupirsi se `cwebp` locale non serve. Attenzione: il corpo deve essere **binario**; un JSON con
`{"base64": …}` sull'endpoint `/wp/v2/media` risponde `rest_upload_no_content_disposition` o
`rest_upload_sideload_error`, che sembra un problema di tipo di file e non lo è (`base64` è il parametro
dell'abilità MCP `media/upload-base64`, non dell'endpoint REST).

**L'`alt` va preso dal proprio valore, non dalla risposta dell'upload.** La risposta di `/media` al momento
del caricamento ha `alt_text` vuoto se l'alt lo si imposta dopo con una seconda chiamata: usando quella
risposta per comporre il blocco, l'`<img>` finisce con `alt=""`. Verifica: il controllo `Immagini e Alt
Text` di `seo/analyze-post-content` (che segnala «2 missing alt») e la lettura del contenuto
salvato. Correzione: una `POST /wp/v2/media/<id>` con `alt_text` **e** la sostituzione di `alt=""` nel
contenuto.

**Quello che si carica su WordPress è il file `-web.webp`**, non il PNG. Misurato sui file veri il
21/09/2026: una copertina 1024×687 passa da **595 KB a 22 KB** (−96%), la 768×515 servita ai telefoni da
**346 KB a 16 KB** (−95%), un'infografica resta comunque ampiamente sotto il PNG.

- Lo script salva **tre** file: il PNG originale (la fonte, non si carica), il **`-web.webp`** (quello
  che si carica) e un'anteprima JPEG per guardarla in fretta.
- Qualità: **82** per le copertine, **88** per le infografiche (hanno molto testo: a qualità più bassa le
  lettere si impastano).
- Serve `cwebp` (`brew install webp`). Se manca, lo script **lo dice** e resta il PNG: in quel caso non
  caricare l'immagine, perché pesa circa quindici volte tanto.
- Vale anche per le immagini che si caricano a mano dalla libreria: **prima si converte, poi si carica.**
  La conversione automatica al caricamento lato WordPress è **in preparazione** (va in un plugin — `plugin-seo`
  o `tema-blocks`, decisione dell'autore): finché non c'è, chi carica un'immagine la converte prima.
- Perché conta: su mobile le copertine sono l'elemento LCP, e il punteggio di PageSpeed del sito
  passa da **62/100** a **97/100** soltanto cambiando formato — è la stessa pagina, le stesse immagini.

## Una pagina, le sue immagini: non si riciclano (regola dell'autore, 30/09/2026)

**Le immagini non si usano in due articoli.** Ogni pagina ha le sue immagini e non si prende un'immagine
per portarla altrove. Vale per la copertina **e** per le immagini dentro il testo: ogni articolo genera
le proprie, con il proprio nome, e non si ricicla quella di un altro articolo nemmeno per riempire un
buco o per un articolo che parla dello stesso argomento.

Conseguenze pratiche: (1) **si genera sempre** l'immagine nuova dell'articolo che si sta scrivendo —
non si riusa un file già presente in `~/seo-content/content/` solo perché il tema è simile; (2) **prima di
cancellare un'immagine o una cartella** va verificato se è usata da una pagina viva: cancellare per
somiglianza di nome rompe le immagini di un altro articolo (verificato il 30/09/2026:
`nicchia-3-passi-214-v3.png` e `struttura-articolo-214.png` stanno nella cartella comune ma servono
alla **214 pubblicata**, non alle bozze con nomi simili); (3) lo stato del sito su questa regola è
misurabile e va controllato, non dato per buono.

**Controllo, eseguibile** (nessun duplicato atteso): si leggono tutti i contenuti con
`_fields=id,status,featured_media,content` e si contano le occorrenze per immagine — `featured_media`,
le classi `wp-image-<id>` e gli `src` nella cartella `uploads` — raggruppando per id di media e per nome
file. Se la stessa chiave compare in due contenuti diversi, la regola è violata. Eseguito su tutti i 67
contenuti il 30/09/2026: **0 immagini condivise**.

## Copertine (immagine in evidenza)

Stile misurato su 30 copertine di il-tuo-sito.it: illustrazione **vettoriale flat** con gradienti e
bagliori (2.5D), **mai fotografie**; sfondo **blu notte/viola indaco #292655** con gradiente radiale
più chiaro al centro, griglia a globo, cerchi concentrici, scintille; **oro/giallo caldo** come unica
fonte di luce; lavanda per i terreni; **logo WordPress** (cerchio blu con W bianca) quando pertinente;
**nessun testo**; composizione centrale e simmetrica oppure diagonale. Formato di casa
**1408×768**. Luminosità media 89/255 (scure), saturazione 0,46.
Parametri: `aspect_ratio="16:9"`, `image_size="4K"`, poi ridurre a 1408×768.
Ricetta e misure complete: `references/stile-copertine.md`.

## Infografiche (immagini dentro l'articolo)

Stile misurato su 101 infografiche: **schemi didattici** su fondo **chiaro** (bianco #ffffff con
riquadri grigio-lavanda #f0f1f5), **card bianche con angoli arrotondati e ombra morbida**, schemi a
due colonne, card in fila, matrici, blocchi navy #26235B con testo bianco, **icone piatte blu**,
badge colorati (viola #4F46E5), simboli di stato (spunta, avvertimento, X). Colore d'accento:
**blu indaco #3343aa** e famiglia; il colore copre solo l'11% dell'immagine. Tipografia sans-serif,
titolo in maiuscolo grassetto, testo grigio #6B7280. Formato di casa **1264×848**.
Contengono **molto testo in italiano** — e il modello lo scrive correttamente (verificato), ma la
disposizione richiesta va **verificata a vista** ogni volta.
Parametri: `aspect_ratio="3:2"`, `image_size="2K"` (o 4K), poi ridurre a 1264×848.
Ricetta completa: `references/stile-infografiche.md`.
