# Scrittura di un articolo (e delle voci di glossario)

> *Estratto da `SKILL.md` il 24/09/2026 per dimensione, contenuto invariato; le intestazioni sono state aggiunte per rendere il file navigabile.*

## Scrittura di un articolo: formato, blocchi, immagini, SEO/AEO/GEO

### 1. Onboarding (`onboard`)
Se è la prima volta su un progetto: raccogli lingua, nome del marchio, formato di output (`html`
consigliato per WordPress), eventuali categorie con i loro ID, giorni di pubblicazione. Salva in
`~/seo-content/shared/PROJECT_STRATEGY.json`. Verifica le dipendenze: MCP `sito`, `MATON_API_KEY`,
Scrapling, `GOOGLE_API_KEY`. **Avvisa sempre che le credenziali WordPress stanno in un file locale
protetto** e che l'agente non pubblica mai.

### Stato del progetto

**Stato su il-tuo-sito.it (configurato il 19/09/2026)**: `~/seo-content/shared/PROJECT_STRATEGY.json` è
pronto — italiano, brand del sito, output HTML, plugin `plugin-seo`, **2 articoli a settimana (martedì e
venerdì)**, mix funnel 50/30/20. Non serve rifarlo: si aggiorna.

### Categorie del sito e mappatura del funnel

**Categorie del sito e mappatura del funnel** (confermata dall'autore):

| Categoria | ID | Articoli | Funnel |
|---|---|---|---|
| WordPress | 3 | 21 | TOFU + MOFU |
| Affiliazione | 5 | 4 | BOFU + TOFU |
| Guide AI | 2 | 3 | TOFU |
| Strumenti AI | 4 | 2 | MOFU + BOFU |
| Sito (la piattaforma) | 1 | 0 | BOFU — **riservata alla piattaforma** |

### Il contesto della piattaforma

**Il contesto della piattaforma (importante)**: il sito permette di creare blog di affiliazione,
con una versione **gratuita con limitazioni** e una **a pagamento con tutte le funzionalità**.
È **ancora in sviluppo**: le funzionalità definitive le comunicherà l'autore quando saranno pronte e
testate. Quindi **non scrivere articoli che promettono funzionalità**: le tre idee sulla
piattaforma restano in calendario come `Idea` **senza data**, e la categoria del sito (id 1)
è riservata a questo tema.

### Il test prima di scrivere — un articolo deve meritare di esistere

**Va fatto prima di scrivere una riga.** La domanda non è «come lo scrivo» ma «perché questo articolo
deve esistere»: se il test non passa, **non si scrive un articolo più corto o più lungo — si cambia
angolo o non si scrive**. Non è la stessa cosa della «Definizione di pronto» del `SKILL.md` §4 (quella
controlla blocchi, meta, schema, link *dopo*): sono due controlli diversi e servono entrambi.

**Le sei porte.** Un argomento entra in lavorazione solo se le supera tutte e sei:

| # | La porta | La domanda di controllo |
|---|---|---|
| 1 | **Domanda reale** | Qualcuno cerca davvero questa cosa, con queste parole? Verificato, non immaginato → `parole-chiave.md` |
| 2 | **Guadagno** | Cosa aggiungo rispetto alle pagine che già rispondono a quella domanda? |
| 3 | **Esperienza** | Posso dire «l'ho fatto / l'ho visto», o solo «ho letto che»? |
| 4 | **Intento** | La forma del contenuto è quella che chi cerca si aspetta di trovare? → `parole-chiave.md` §2 |
| 5 | **Completezza** | Chi legge esce con il problema risolto, o deve tornare su Google? |
| 6 | **Ritorno** | Cosa porta a me: visite, posizionamento, contatti — o almeno l'articolo successivo? |

**Il questionario, da passare su ogni idea prima di metterla in calendario.** Un solo «no» sulle prime
sei voci vuol dire non scrivere.

- [ ] Questa cosa la sta cercando qualcuno, con parole sue? (l'ho verificato, non immaginato)
- [ ] Ho qualcosa da dire che le prime pagine su questa domanda non dicono?
- [ ] Posso mostrare esperienza diretta — numeri miei, prove, schermate, test?
- [ ] La forma del contenuto corrisponde all'intento di chi cerca?
- [ ] Chi legge esce con la domanda risolta e non deve tornare su Google?
- [ ] C'è almeno una delle tre: **fa fare**, **fa imparare**, **fa sentire**?
- [ ] Il «perché» di questo articolo è aiutare qualcuno, o prendere traffico?
- [ ] La firma c'è, e porta a una persona reale con una competenza dichiarata?
- [ ] Ho dichiarato se e come ho usato l'AI?
- [ ] Il titolo descrive il contenuto invece di esagerarlo?
- [ ] Non sto copiando né traducendo nessuno senza aggiungere niente?
- [ ] Non esiste già un mio articolo che risponde alla stessa domanda? (controllo della **promessa**, `SKILL.md` §3)

Se il punteggio è alto ma la seconda voce è debole, la strada **non** è allungare l'articolo: è cambiare
angolo o non scriverlo.

#### I cinque tipi di articolo che non si scrivono

Verificati su un blog vero (Penna blu, Daniele Imperi), e valgono qui:

1. **News su aggiornamenti di software o eventi** — «letto uno, letti tutti». Una notizia può diventare
   un articolo **se** spinge a un approfondimento; la pura segnalazione no.
2. **Premi, riconoscimenti e catene tra blog** — rimbalzo di link senza utilità per chi legge.
3. **Meme senza valore** — il meme fatto bene è contenuto, quello che non dà niente no.
4. **Segnalazioni di libri, recensioni e concorsi** — «perché devo segnalare un libro quando chiunque
   può trovarselo da solo?» Se non si porta un'esperienza o un taglio proprio, non è un articolo.
5. **Traduzioni di articoli altrui** — sono di chi li ha scritti, non di chi li traduce: si riscrive
   con una tesi propria e si cita la fonte, oppure non si pubblica.

**E i tre casi che Google chiama abuso** (policy ufficiale, link qui sotto): pagine **generate in massa**
per prendere traffico, **contenuto di altri ripubblicato** senza valore aggiunto, e contenuto pubblicato
per sfruttare la reputazione di un sito ospite. Il test rapido: «molte pagine il cui contenuto ha poco o
nessun senso per un lettore ma contiene parole chiave» è esattamente quello che non si fa.

#### L'esperienza si dichiara, non si inventa

- **Mai inventare aneddoti personali**: se serve una voce in prima persona, si chiede all'autore. Un'esperienza
  inventata viola l'E-E-A-T ed è il difetto più grave che un articolo possa avere (la regola è anche nel
  `SKILL.md` §4, «la passata di umanizzazione»).
- **I lettori e Google distinguono** un'esperienza reale da un riassunto di seconda mano: l'esperienza è
  la materia prima, e va mostrata con quello che si vede (schermate, numeri, passi eseguiti).
- **Se si usa l'AI per scrivere o per cercare, si dichiara.** Google non vieta l'AI: chiede che chi legge
  sappia *come* il contenuto è stato prodotto, e punisce l'uso dell'automazione **per manipolare il
  ranking**. La domanda da farsi è quella ufficiale: «l'uso dell'automazione è evidente a chi visita la
  pagina? c'è il contesto di come è stata usata? è spiegato perché è stata utile?»

**Fonti di queste regole (documenti ufficiali Google):**
- contenuti utili e pensati per le persone — `https://developers.google.com/search/docs/fundamentals/creating-helpful-content`
  (anche in italiano: aggiungere `?hl=it`)
- le policy sullo spam (contenuti su scala, scraping, abuso di reputazione del sito) — `https://developers.google.com/search/docs/essentials/spam-policies`
- le linee guida per i valutatori di qualità, da cui viene E-E-A-T — `https://guidelines.raterhub.com/searchqualityevaluatorguidelines.pdf`

### Regole editoriali: formato e lettore

**Regole editoriali (decise dall'autore — valgono per ogni articolo)**

*Livello e lettore (regola dell'autore, 29/09/2026)*
- **Il livello di partenza è «dove clicco e cosa vedo», non il metodo.** Il lettore di il-tuo-sito.it apre
  un blog da zero: non sa cosa sono TTFB, EPC, CTR, «finestra di 5 ore», «dazio per tipologia di
  articolo». Un articolo che parte da lì è scritto per un altro pubblico, e l'autore lo respinge come
  inutile anche quando i dati sono giusti.
- **Come si imposta**: (1) il primo paragrafo dice cosa vedrai e cosa saprai fare alla fine, in
  parole comuni; (2) poi i passi, uno per schermata, con **dove si clicca**, **cosa compare** e
  **cosa significa quella voce**; (3) le tabelle di valori vengono **dopo** che il lettore sa dove
  guardarli; (4) il gergo si spiega **nella riga in cui compare**, oppure si sposta in un H3 di
  approfondimento in fondo.
- **I numeri non spariscono**: restano, ma come prova dentro un passo («qui vedrai circa X»), non come
  tesi dell'articolo. Un articolo per principianti con misurazioni vere è forte; un articolo per
  esperti su un blog per principianti è inutile.
controllo da fare prima di consegnare** (una riga): leggere il titolo e i primi tre paragrafi e
  chiedersi «questo lo capisce chi non ha mai aperto quel pannello?». Se la risposta è no, si riscrive
  l'apertura e i passi, non si cambia l'argomento.

*Lunghezza e completezza*
- **minimo 1.500-2.000 parole**, ma **non è un tetto**: se l'argomento lo richiede si va a **3.000,
  4.000 o più**, senza tagliare contenuto utile. Le regole sono due: **non ripetere** informazioni e
  **non allungare per arrivare al numero**.
- Gli articoli si scrivono **per le persone prima che per Google**: la SEO è il modo in cui il
  contenuto viene trovato, non il motivo per cui esiste. Se un passaggio serve solo a posizionarsi e
  non aiuta chi legge, si toglie.
- Pensare al lettore **alle prime armi**: ogni concetto va spiegato, non dato per scontato.
- Scrivere per essere **leggibile**: frasi brevi, un'idea per paragrafo, niente muri di testo.
  `evaluate-copy` boccia i periodi lunghi: controllarlo sempre.

*Organizzazione (mai muri di testo)*
### I blocchi dell'editor

- **usare quanti più tipi di blocco dell'editor possibile**, variandoli: titoli `h2`/`h3`,
  paragrafi, **elenchi**, **tabelle**, **citazioni**, **riquadri** (`group` con sfondo Base 2),
  **blocchi richiudibili** (`details`) per FAQ e approfondimenti, **colonne** per i confronti,
  **pulsanti** per i rimandi, separatori. Un articolo ben spaccato si legge e si scansiona meglio.

*Solo blocchi veri (regola dell'autore, 19/09/2026)*
- **Negli articoli e nelle pagine si usano solo blocchi dell'editor**. Niente `core/html`, niente
  `wp:figure` (non è un blocco valido: l'editor lo segnala come non valido), niente classi inventate.
  Un `div` con una classe che **non esiste** nel tema — come `direct-answer-box`, usata in 10 punti
  della bozza 1452 — non ha nessuno stile: si vede come un paragrafo normale.
#### Il riquadro di risposta

- **Riquadro di risposta** → blocco `group` con sfondo Base 2 e padding, come nel 1479:
  ```html
  <!-- wp:group {"style":{"spacing":{"padding":{"top":"var:preset|spacing|40","bottom":"var:preset|spacing|40","left":"var:preset|spacing|40","right":"var:preset|spacing|40"}}},"backgroundColor":"base-2"} -->
  <div class="wp-block-group has-base-2-background-color has-background" style="padding-top:var(--wp--preset--spacing--40);padding-right:var(--wp--preset--spacing--40);padding-bottom:var(--wp--preset--spacing--40);padding-left:var(--wp--preset--spacing--40)">…</div>
  <!-- /wp:group -->
  ```
  **Questa è la forma provata**: è la stessa che usano i pattern del tema per un gruppo con sfondo
  (`style` con il padding, `backgroundColor`, il div con le sole classi `wp-block-group has-…-background-color has-background`).
  **Niente `"border"`, niente angoli arrotondati, niente `"layout"` scritti a mano**: il 19/09/2026 i riquadri
  della bozza 1452 con `"border":{"radius":"12px"}` e `"layout":{"type":"constrained"}` sono stati
  segnalati dall'editor come «questo blocco ha un contenuto inaspettato o non valido». La validazione dei
  blocchi è **solo lato editor**: dopo aver scritto markup a mano, far aprire la bozza all'autore e chiedergli
  se il blocco è pulito; per un riquadro con angoli arrotondati, crearlo nell'editor e copiarne il codice.
  (dentro, un blocco `paragraph` con la frase di risposta in `<strong>`; il titolo `h3` solo se serve)
#### Tabella e HTML grezzo

- **Tabella** → blocco `wp:table`, non HTML a mano: così si modifica dall'editor.
- Un contenuto già scritto con HTML grezzo si converte con sostituzioni mirate e poi si **rilegge**
  la bozza (`gutenberg/get-post-blocks`): `wp:html`, `wp:figure` e le classi inesistenti a zero,
  e il blocco `table` al posto delle tabelle.

*Immagini*
### Immagini e infografiche

- **immagine in evidenza sempre**: stile copertine del sito, 1408×768.
- **una infografica ogni 400-500 parole**, senza forzare: se un concetto non ha bisogno di un
  disegno, non si mette.
- **un'infografica deve essere una vera infografica**: un **diagramma, uno schema di flusso, una
  scala, un confronto visivo, un grafico**. Serve a **spiegare meglio un concetto** o ad **aggiungere
  informazione** che nel testo non c'è.
- **non serve a niente un'immagine che ripete le stesse frasi dell'articolo** (elenchi di testo
  dentro delle card): se non aggiunge nulla, non si mette.
- **l'accento mancante non è un motivo per rigenerare**: con o senza accento nelle scritte delle
  immagini va bene, non si sprecano crediti per questo.
- **`alt` sempre compilato** su tutte le immagini.
- **Un articolo non è finito finché non restano segnaposto (imparato il 21/09/2026).** Il giro giusto scrive le immagini prima del testo, e nel testo le cita con un segnaposto (`{{INFOGRAFICA_FLUSSO}}`) finché non sono caricate: se la sostituzione non avviene, l'articolo **pubblicato** mostra immagini rotte. Sull'articolo 1479 sono rimaste tre infografiche con `src="{{INFOGRAFICA_*}}"` per giorni, con i file già pronti in `~/seo-content/content/`. Prima di dichiarare finito: **zero `{{…}}` nel contenuto** e ogni `<img>` con un `src` reale e la classe `wp-image-<id>`. Controllare due volte — sul contenuto salvato e sulla pagina pubblica (le immagini devono rispondere 200 e comparire nel browser) — e sostituire **server-side**, non via REST: il segnaposto si chiama `{{INFOGRAFICA_NOME}}`, quindell'ago è `src="{{INFOGRAFICA_NOME}}"` (senza il prefisso non trova niente), e all'img va aggiunta `class="wp-image-<id>"` più `"id":<id>` negli attributi del blocco.

*SEO, AEO e GEO su ogni articolo*
### SEO, AEO e GEO

- **SEO**: keyword nella prima parte del testo, nei titoli e nei link; meta description scritta;
  link interni 2-5 e esterni 1-3 autorevoli; `alt` descrittivi; schema adatto al contenuto.
#### AEO

- **AEO** (farsi citare dalle risposte): **rispondere subito**, con una frase diretta sotto ogni
  titolo a domanda; mettere una **definizione chiara** in apertura; usare **elenchi** e **passi
  numerati**; chiudere con **"In sintesi"** e una **sezione FAQ** con schema `FAQ`.
#### GEO

- **GEO** (farsi citare dagli assistenti AI): affermazioni **fattuali e verificabili**, orientate a
  entità concrete (nomi di strumenti, standard, organizzazioni); **fonti citate** con link
  autorevoli; contenuto **originale** (esempi, esperienze, dati) che non si trova identico altrove;
  struttura chiara con titoli espliciti e sezioni autonome, così ogni parte si può citare da sola.

### Il blocco FAQ: come si scrive

**La FAQ si scrive col blocco del plugin, non con `core/details` (corretto il 21/09/2026).** Il plugin `plugin-seo` fornisce tre blocchi propri, categoria **plugin SEO**: `seo/faq`, `seo/howto`, `seo/table-of-contents`. La sezione *Domande frequenti* va fatta con **`seo/faq`** (`items`: array di `{question, answer}`, `answer` in HTML tipo `<p>…</p>`; `enableSchema` di default `true`): il blocco rende la lista (`<dl class="seo-faq__list">`) e **al salvataggio del post sincronizza da sé la meta `_sito_seo_faq`**, che è la fonte da cui il modulo schema del plugin genera il `FAQPage` — la stessa meta che legge il controllo di conformità. Con `core/details` la pagina ha le domande ma **nessuno schema FAQ** e il plugin la segnala: è l'errore che l'autore ha trovato nella bozza 1550. Quindi: blocco del plugin, e **non** scrivere a mano la FAQ in `seo/update-schema-data` (la sincronizza il blocco; lasciare lì solo il `schema_type`).

Forma del markup, verificata:
```html
<!-- wp:seo/faq {"items":[{"question":"…","answer":"<p>…</p>"}],"enableSchema":true} /-->
```

#### Non confondere i due blocchi FAQ

**Attenzione a non confondere due blocchi simili** (verificato il 21/09/2026). Il tema ha anche
`tema-blocks/faq-accordion`, che è un'altra cosa: prende le voci dal tipo di contenuto `faq` del
sito, filtrate per categoria (`categoryId`), e ha un suo `schemaOutput`. Serve a una **pagina che
raggruppa le FAQ del sito** — la pagina *Documentazione* (437) lo usa correttamente — **non** alla
sezione *Domande frequenti* di un articolo, che si scrive con `seo/faq`, con le domande
dentro il blocco.

#### La FAQ e la meta: serve un utente collegato

**Il blocco FAQ sincronizza la meta solo se c'e' un utente collegato (imparato il 21/09/2026).**
`sito_seo_sync_faq_block_meta`, il gancio su `save_post` che scrive `_sito_seo_faq`, esce subito
se `current_user_can('edit_post', $post_id)` e' falso. Scrivendo da **wp-cli o da uno script CLI**
non c'e' nessun utente collegato, quindi il salvataggio va a buon fine ma **la meta resta vuota**: il
blocco si vede nella pagina, lo schema `FAQPage` no. Prima di salvare (o di richiamare la
sincronizzazione) serve `wp_set_current_user( 1 )` con un amministratore, poi `wp_update_post`. Da
REST il problema non si presenta, perche' la richiesta e' autenticata. **Dopo ogni scrittura del
blocco FAQ verificare sempre `_sito_seo_faq`**: se e' vuota, lo schema non c'e' anche se la pagina
sembra a posto.

### Non scrivere a mano il commento del blocco

**Non scrivere a mano il commento del blocco quando si salva via REST (imparato il 21/09/2026
sull'articolo 1479).** Un commento `<!-- wp:seo/faq {"items":[…] } /-->` composto a mano e
passato per l'API viene riscritto in salvataggio con gli escape `\u003c`/`\u003e` e gli attributi si
rileggono **vuoti**: il blocco non rende (la pagina pubblica stampa il commento come testo) e la
sincronizzazione, trovando il blocco senza attributi, **cancella** la meta `_sito_seo_faq`, quindi
la schema FAQ sparisce dalla pagina. La forma affidabile è farla generare a WordPress: sul server con
`serialize_block( array( 'blockName' => 'seo/faq', 'attrs' => array( 'items' => …, 'enableSchema' => true ), 'innerBlocks' => array(), 'innerHTML' => '', 'innerContent' => array() ) )`
e poi **`wp_update_post( wp_slash( … ) )`**. Il `wp_slash` non e' un dettaglio: `wp_update_post()`
fa `wp_unslash()` sui dati che riceve (si aspetta dati gia' "slashed", come quelli di `$_POST`),
quindi i backslash delle sequenze `\u003c`/`\u003e` — che sono la forma canonica con cui WordPress
serializza gli attributi (JSON_HEX_TAG) — vengono mangiati e nel contenuto resta `u003cpu003e`:
JSON ancora valido, ma con il testo sbagliato, che il blocco rende come tale (verificato il
21/09/2026 sulla bozza 1577: le risposte in pagina iniziavano con `u003cpu003e` invece di `<p>`).
**E' questa la causa vera dell'incidente del 1479**, non gli escape in se'. oppure inserire il blocco dall'editor. Dopo ogni conversione: **verificare la
pagina pubblica** (deve esserci `<dl class="seo-faq__list">`, non il commento grezzo) e la
meta `_sito_seo_faq`; tenere pronto il backup del contenuto precedente, e se la pagina risulta
rotta ripristinare subito — sulla 1479 è successo esattamente questo.

*Glossario — si scrive insieme agli articoli*

### Il glossario

**Mai inserire a mano i link ai termini del glossario (regola dell'autore, 21/09/2026).** Il tema li
mette da sé, sulla **prima occorrenza** di ogni termine in ogni contenuto: scriverli a mano duplica
il link, lo sposta o lo rompe, e fa concorrenza all'automatismo. Nell'articolo il termine si **nomina
e basta**. L'automatismo vale anche *dentro* le voci del glossario (una voce linka gli altri termini
che contiene: non serve farlo a mano nemmeno lì). Restano da scrivere a mano solo due cose: i **link
fra articoli** (il silo, es. 684 → la guida sulla strategia SEO) e i **link esterni** (le fonti).
Il tema ha un **glossario automatico**: le voci sono contenuti di tipo `glossary` e i termini
vengono **linkati da soli** dentro articoli e pagine, con una **anteprima a comparsa** e il link alla
voce. Regole del meccanismo (dal plugin del tema `class-tema-compagnon-glossary-autolink.php`):
colpisce **la prima occorrenza** di ogni termine per contenuto, ignora maiuscole/minuscole, **non
tocca i titoli**, il testo già dentro un link, gli script e il codice, e non linka un termine sulla
sua stessa pagina.

- **Prima di scrivere**: leggere le voci già presenti —
  `content/list-posts` con `{"post_type": "glossary", "status": "publish"}` (al 19/09/2026 sono
  **54**, fra cui Backlink, Anchor text, E-E-A-T, CTR, Crawl budget, Contenuto duplicato,
  Cannibalizzazione delle keyword, Parola chiave, Permalink, Plugin, Hosting, CMS, Core Web Vitals).
  **Se il glossario spiega già un concetto, nell'articolo non si ripete**: si nomina e basta, il
  link e l'anteprima li mette il tema. Così le due cose non si fanno concorrenza.
- **Dopo aver scritto**: scorrere l'articolo e cercare i **concetti** che meriterebbero una voce e
  non ci sono. Per ognuno si crea la voce con `content/create-post`, `post_type: "glossary"`,
  **come bozza** — l'autore la pubblica quando vuole.
- Un termine va nel glossario se è **un concetto riusabile** in altri articoli (es. PageRank, Domain
  Authority, Nofollow), non se è una frase una tantum.
- Le voci non vanno riempite con la SEO (description/keyword) se non servono: l'anteprima usa
  l'estratto.

### La categoria va sempre messa

**La categoria va sempre messa (imparato il 20/09/2026).** Il tipo `glossary` ha **due tassonomie**:
`glossary_category` (gerarchica, le sei categorie del sito) e `glossary_tag` (vuota, non si usa). Una
voce **senza `glossary_category` non compare fra le categorie** della pagina del glossario. Nel primo
giro di voci — le dodici del silo SEO: PageRank, Domain Authority, Link building, Nofollow, Search
Console, Schema markup, Dati strutturati, JSON-LD, Rich snippet, Microdati, SERP, Knowledge Graph —
la categoria è stata dimenticata e l'autore l'ha dovuta segnalare. Le sei categorie:

| Categoria | slug | a cosa va |
|---|---|---|
| WordPress e Gutenberg | `wordpress-e-gutenberg` | CMS, blocchi, permalink, plugin, temi, REST API |
| SEO | `seo` | posizionamento, link, dati strutturati, Search Console, SERP |
| Hosting e performance | `hosting-e-performance` | hosting, cache, CDN, Core Web Vitals, certificati |
| Sicurezza | `sicurezza` | backup, firewall, XSS, 2FA, CVE |
| Affiliazione | `affiliazione` | programmi, commissioni, CPA, EPC, funnel |
| Intelligenza artificiale | `intelligenza-artificiale` | IA generativa, modelli, prompt, allucinazioni |

`content/create-post` accetta `category_ids` per le categorie del **blog**, non per la tassonomia del
glossario: la categoria della voce si assegna a parte, e poi si **rilegge** (`wp_get_post_terms`) per
confermarlo.

### Come è fatta una voce buona

**Come è fatta una voce buona** (forma misurata sulle voci dell'autore, es. *Backlink*, id 875):

1. **`excerpt`: una frase sola**, 100-160 caratteri, che definisce il termine — è quella che si legge
   nell'anteprima a comparsa dentro il testo.
2. **Corpo: 4-5 paragrafi, ~2.000-2.800 caratteri**, nello stesso ordine: definizione estesa → come
   funziona → un **esempio concreto** → l'**errore** tipico da evitare → la buona pratica. Solo
   blocchi `paragraph`.
3. **Ultima riga, sempre**: `Fonte: <a href="…" target="_blank" rel="noopener nofollow">dominio</a>`
   verso una fonte **autorevole e ufficiale** — Google Search Central
   (`developers.google.com/search/docs`), `schema.org`, `web.dev`, W3C, MDN, la documentazione del
   fornitore. `it.wikipedia.org` è accettabile quando non esiste una fonte ufficiale, **non** come
   prima scelta.
4. Mai la SEO sulla voce: niente title/description/keyword propri.
