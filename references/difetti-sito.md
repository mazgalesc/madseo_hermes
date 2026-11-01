# Difetti noti del sito — verificati, da non riscoprire

**Estratto da `SKILL.md` il 01/11/2026** (contenuto invariato). Non è la storia del sito: è l'elenco dei
difetti che sono costati tempo, con la data della verifica accanto a ognuno e il numero misurato. **Si legge
prima di proporre un intervento**, e i numeri si **rifanno**: un conteggio ereditato vale quanto un numero
inventato. Dove la correzione è già stata fatta e verificata è scritto; dove il rischio resta (un plugin
aggiornato senza riportare la protezione) è scritto anche quello.

Le trappole generali — quelle che non dipendono da questo sito — stanno in `references/trappole.md`.

**1. `missing_alt` — corretto in `plugin-seo` 3.0.31 (19/09/2026); l'11/10/2026 la versione attiva è la 3.0.34** — si legge con `curl -u … 'https://il-tuo-sito.it/wp-json/wp/v2/plugins?context=edit'`, che dà nome e `version` (il tema a blocchi è nella stessa risposta) — **ma non fidarsi del suo `status`**: quella lista riporta lo stato **per-sito**, quindi su un multisite un plugin attivo a livello di **rete** lì compare `inactive`. Lo stato vero è sul singolo plugin, `…/wp/v2/plugins/<cartella>/<slug>` → `network-active`, ed è quello che si legge. **Mai dichiarare «disattivato per sbaglio» guardando solo la lista** (verificato il 13/10/2026: tre plugin riferiti come spenti erano attivi a livello di rete, e su quella lettura sbagliata è stato programmato un intervento inutile).
Il controllo era
`preg_match('/<img[^>]+(?!alt=)[^>]*>/i', …)`: il lookahead negativo viene valutato dopo che `[^>]+`
ha già consumato il tag, quindi combaciava con **qualsiasi** `<img>` — 31 contenuti segnalati a
fronte di 5 immagini davvero senza alt. Ora tutto passa da
`sito_seo_count_images_without_alt()` in `includes/common/helpers.php`, che esamina **ogni** tag
`<img>` (attributo assente o vuoto = mancante, `data-alt` non conta, ignora `>` dentro un attributo
quotato). Stessa funzione usata dal pannello e dall'elenco articoli, che prima contavano al
contrario (solo `alt=""`). Test: `php scripts/test-alt-check.php` (35 controlli).
Correzione giusta: `'/<img(?![^>]*\balt=)[^>]*>/i'`.

**Il conteggio si rifà, non si eredita.** Al **11/10/2026**, sui **45 articoli pubblicati** contati con
`scripts/controlla-articolo.py`: **134 immagini, 0 senza alt** (il caso del `585` è chiuso), più **2
immagini nelle 8 pagine**. Due avvertenze: lo script legge `alt` con **apici singoli e doppi** (un
controllo scritto a mano che accetta solo i doppi trova falsi «senza alt»), e il numero delle **pagine
renderizzate** (logo, avatar, template) è più alto e non confrontabile con quello del contenuto — il
19/09/2026 erano 168.

**2. Il link automatico del glossario riscrive anche dentro i tag.** In
`tema-blocks/inc/glossary/class-tema-compagnon-glossary-autolink.php` (righe 161-167) i
segmenti protetti sono link, script, style, pre/code e titoli: **manca la protezione dei tag
stessi**, quindi un termine del glossario che compare in un attributo (`src`, `alt`) viene
sostituito con `<a class="mw-glossary-term">` **dentro l'attributo**. Effetto: immagine rotta o alt
distrutto nella pagina pubblica. Il contenuto nel database resta integro: è un danno di resa.
Verificato il 19/09/2026 su 2 pagine (215: `src` rotto, immagine non visibile; 224: `alt` rotto).
**Corretto e verificato l'11/10/2026**: sui due contenuti i link del glossario non compaiono più dentro
`src`/`alt` (0 casi) e i termini evidenziati funzionano ancora (14 e 27). Il rischio resta se il plugin
viene aggiornato senza riportare la protezione dei tag.
Rischio alto: **66 file della libreria hanno un termine del glossario nel nome** (epc, backup,
hosting, cache, plugin, affiliazione, Gutenberg...). Correzione: aggiungere `'<[^>]+>'` all'array
`$protected` (in coda, dopo il pattern dei link). Quando è corretto, non serve toccare i contenuti.

**3. I difetti di SITO trovati nell'audit dell'11/10/2026 (45 articoli + 15 bozze) — si correggono UNA
volta, non su 45 pagine.** L'elenco completo con i casi e i numeri è in `~/seo-content/archivio/rapporto-difetti-audit.md`
e in `~/seo-content/archivio/correzioni_articoli/00-INDICE.md` (§1-98). Quelli che sono di sito, non di articolo:

- **`HowTo` nello schema di molti articoli del lotto di fine settembre** (verificato l'11/10/2026: presente
  in `1952`, `1967`, `204`; **assente** in `1854` e `1883`): funzionalità ritirata da Google nel 2023 (e il
  sito lo spiega da sé nel `1529`). Da togliere **dove c'è, uno per uno** — non «su tutti»: il tipo
  principale va uniformato su **`BlogPosting`** (all'11/10/2026 usano ancora `Article` il `1854` e il `1883`;
  il `1952` è già a posto).
- **`FAQPage` su tutti**: i rich result FAQ sono ritirati dal **7 maggio 2026** — il markup resta valido,
  ma non promette più niente in SERP.
- **La dichiarazione di affiliazione non esiste su nessuna pagina**, mentre quattro articoli la insegnano
  (`1593`, `1603`, `1900`, `1962`) e Amazon ne impone una formula propria. È il difetto più costoso.
- **`nofollow` sulle fonti autorevoli**: incoerente fra articoli (`226`/`227` ce l'hanno, `1412` no). Le
  fonti si linkano normali; `nofollow`/`sponsored` solo per i link commerciali.
- **Duplicazione riquadro + primo paragrafo**: **352 riquadri** sul sito, **29 con ripetizione**
  (`204` 9, `206` 7, `202` 5, `203` 4). Dal `209` in poi zero: `213` dimostra che si può fare bene.
- **Etichette di tema non tradotte**: «Updated on» sotto la data italiana, «Table of contents».
- **Campi dello schema a video**: `PT2H`/`PT10M` nei blocchi HowTo (`222`, `1412`, `1441`) — si corregge
  nel template.
- **Cannibalizzazione**: `204`/`212` sullo stesso tema (il `212` linka il `204` 7 volte ed è mai
  scansionato); cinque articoli di affiliazione che si linkano in cerchio; **quattro pagine orfane**
  (`224`, `1441`, `1412`, `1452`).
- **Identità del sito**: autore anonimo (uno pseudonimo, senza credenziali dichiarate), Gravatar predefinito, social del
  footer a `href="#"`, commenti = solo auto-pingback. E il `217` — l'articolo più accurato del sito,
  dieci affermazioni verificabili tutte esatte — **è stato scartato da Google**: il problema è di dominio,
  non di singolo articolo.

*Indirizzi*
- **piatti** come il resto del sito: `https://il-tuo-sito.it/slug-dell-articolo/` — niente prefissi
  gerarchici tipo `/seo/…`.
