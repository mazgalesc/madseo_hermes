# Come si verificano davvero le modifiche SEO (imparato sul campo)

**Estratto da `SKILL.md` il 01/11/2026** (contenuto invariato). Vale per ogni scrittura: schema, campi SEO,
meta, blocchi, link. **La regola che le tiene tutte: la busta del successo non è la prova che il campo è
stato scritto** — `{"success": true}` arriva anche quando il campo è stato ignorato in silenzio, quindi dopo
ogni scrittura si rilegge il campo che si voleva cambiare.

**Lo schema va confrontato col contenuto visibile — ma sulla SOSTANZA, non sulle stringhe.** FAQ e HowTo
sono validi solo se descrivono roba che si vede in pagina. Cercare le stringhe dei passi come testi
letterali **dà falsi allarmi**, perché la pagina dice la stessa cosa con altre parole: verificato il
24/09/2026, i nomi dei passi HowTo di 211 e 212 compaiono **solo dentro il JSON-LD** (posizione nel
sorgente dentro gli intervalli `<script type="application/ld+json">`), e però in entrambe le pagine
esiste la **procedura equivalente, visibile e numerata** (211: l'elenco di `Come provare un tema senza
rischi`; 212: l'elenco di `Le 5 cose da controllare prima di comprare un hosting`). Quindi i due HowTo
sono legittimi.

Procedura giusta, in due passi: (1) ricerca posizionale dei testi nel sorgente, dentro/fuori gli script
JSON-LD; (2) **lettura del contenuto salvato** per trovare la procedura equivalente nel corpo. Si dichiara
il problema **solo se la procedura in pagina non c'è affatto**. Le FAQ invece si controllano in
`<dt class="seo-faq__question">` — attenzione, gli accenti sono in entità HTML: cercare «è» senza
entità le fa sembrare assenti.

**Casi reali dalla stessa verifica:** 208 ha due `HowToTool` chiamati letteralmente `"Array"` (campo meta
`tools` rotto, quello è un difetto vero); 211 ha il titolo dello HowTo più ampio della sezione visibile e
un quarto passo che nel testo non esiste; 212 ha i 5 passi che corrispondono uno a uno all'elenco visibile.
Le abilità di lettura del plugin **non sempre dicono la verità**: la verifica vera è l'HTML pubblico.

**E le abilità di SCRITTURA non dicono cosa hanno fatto.** Una scrittura risponde `{"success": true}`
anche quando ha **ignorato in silenzio** un campo che non conosce: la busta del successo non è la prova che
il campo è stato scritto. Verificato il 14/10/2026 — `seo/update-post-seo` chiamato con un `focus_keyword` in
più ha risposto `success: true` elencando in `updated` **solo** titolo e descrizione, e la keyword è rimasta
vuota. Su un controllo che la §4 dichiara **bloccante** (la keyword), l'esito era «superato» senza esserlo.
Quindi: **dopo ogni scrittura si rilegge il campo che si voleva cambiare**, e se è immutato la scrittura non
è avvenuta.

**Prima di comporre un payload, si chiedono i campi veri dell'abilità** con
`mcp-adapter-get-ability-info`. `mcp-adapter-discover-abilities` elenca nome, etichetta e descrizione, e per
un certo numero di voci **non porta affatto** lo schema dei parametri: «il campo non compare nell'elenco» non
vuol dire «il campo non esiste», e «la chiamata è riuscita» non vuol dire «il campo è stato scritto». Le due
domande si fanno all'endpoint, non alla memoria.

- **`missing_meta` vuole titolo *e* description**: il controllo (`seo-abilities.php`) segnala il
  problema se manca anche **solo** `_sito_seo_title`. Scrivere solo la description non fa
  scendere il conteggio.
- **`get-post-seo` non legge la description personalizzata**: restituisce un estratto del contenuto
  con ellissi anche quando `_sito_seo_description` è valorizzata. **Non fidarsi di quel campo:**
  verificare con
  `curl -s https://il-tuo-sito.it/<slug>/ | grep -o '<meta name="description"[^>]*>'`
  (o con `meta/get-post-meta` su `_sito_seo_description`, che è la fonte vera).
- **Il tag robots usa virgolette singole** nell'HTML di questo sito:
  `<meta name='robots' content='max-image-preview:large, noindex' />`. Cercarlo con virgolette
  doppie fa credere che non ci sia (successo davvero).
- **`noindex` sull'HTML**: si scrive `meta/update-post-meta` con
  `{"_sito_seo_robots": {"noindex": true, "nofollow": false}}`; il plugin lo applica tramite
  il filtro di WordPress `wp_robots`. Il contatore `noindex_posts` del riepilogo resta però a **0**
  per un difetto del plugin (cerca un formato JSON mentre l'editor salva un array PHP): **non usarlo
  per verificare**, guardare l'HTML.
- **Keyword obiettivo**: campo meta `_sito_seo_focus_keyword` (verificato nel sorgente del plugin),
  si scrive con `meta/update-post-meta`. `update-post-seo` **non** ha quel campo.
- **I link rotti si riscansionano da soli** alla prima lettura di `get-broken-links` dopo la
  modifica, quindi il conteggio si aggiorna senza comandi di riscansione.
- **La home (`https://il-tuo-sito.it/`) viene segnalata come link rotto** ma risponde 200: è un falso
  positivo del controllo (non riesce a mapparla a un articolo). Non toccarla.
- **Modificare i link dentro un articolo**: leggere il contenuto con `get-post-blocks`, salvare una
  copia in `~/seo-content/audits/backup-articoli/`, fare la sostituzione esatta sull'HTML degli anchor,
  riscrivere con `gutenberg/update-post-blocks` passando `content`, poi **rileggere e validare**.
  WordPress conserva le revisioni (`content/list-revisions`, `restore-revision`) come rete di
  sicurezza.
