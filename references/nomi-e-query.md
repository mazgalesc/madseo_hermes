# Nomi, query ambigue e varianti delle immagini

Estratto delle verifiche del 24/09/2026 (le nove bozze + il giro sui 33 pubblicati).

## La regola dei nomi (tre casi indipendenti)

**Il pubblico cerca per nome di prodotto; gli articoli di questa casa rispondono per categorie.** Non è
una distrazione di un articolo: è una regola di scrittura, e va segnalata come tale.

| Articolo | Cosa chiede il pubblico | Cosa dice l'articolo |
|---|---|---|
| **1529** (schema markup) | 8 query su 17 sono `plugin` + funzione | **nessun plugin nominato**, `plugin` 8 occorrenze ma tutti generici |
| **1623** (hosting condiviso/VPS) | `hosting condiviso aruba`, `hosting condiviso serverplan`; SERP A = 8 fornitori | **zero nomi**: Aruba 0, Serverplan 0, SiteGround 0, Kinsta 0, Hetzner 0 |
| **1629** (CDN) | `cdn wordpress` = 15 suggerimenti con Cloudflare/Bunny/Azure/Hostinger; `cloudflare` da solo = 15 | **zero nomi**: Cloudflare 0, Bunny 0, Akamai 0 |

**Come si corregge:** i nomi vanno scritti **dove sono informazione, non pubblicità** — dentro le fasce di
prezzo già presenti (1623: 3-15 / 15-40 / 10-60 €), nel capitolo che descrive già quel servizio senza dirlo
(1629: «Il piano gratuito fa già molto» **è** il piano gratuito di Cloudflare), accanto alla funzione confrontata
(1529/226). **Non** trasformare l'articolo in una lista di prodotti.

**Nota correlata:** su `hosting condiviso` (1623) la prima pagina è **tutta vendita** (8 fornitori, con i prezzi),
mentre sulla query comparativa la SERP è **editoriale ma scritta da aziende di hosting** (7 su 8). Il vantaggio
disponibile è **lo stesso confronto scritto da chi non lo vende**.

## Screening delle query: suggerimenti sbagliati e sigle ambigue

1. **`suggestqueries` può restituire suggerimenti sbagliati** per la frase esatta: `cos'è una cdn` →
   `cos è un cdna`, `cos è una cd`. **Non è una prova che la frase non esista**: la SERP per la stessa query
   era piena (Cloudflare, Akamai, AWS, Aruba, IBM). **Prima di concludere «zero domanda», guardare la SERP.**
2. **Le sigle sono ambigue in italiano, e la SERP lo conferma:** `cdn` = Congo (`cdn sigla nazione`,
   `cdn che nazione è`, `cdn stato`), una squadra di calcio (`cdn napoli`), una libreria (`cdnjs`); su `eeat`
   quindici suggerimenti sono meteo e Eataly. La prima domanda del pubblico in SERP era **«Che sigla è CDN?»**.
3. **Ma prima di segnalare «la sigla non è sciolta» come difetto, controllare il testo**: sul 1629 era già
   sciolta alla seconda riga (*«In sigla sta per Content Delivery Network»*). **Controllo negativo, riportato
   come negativo** — è il motivo per cui il Passo 5 va misurato e non dedotto.
4. **La parola «gratis» non è un segnale affidabile** in questi settori: `cdn gratis` = 10 suggerimenti di cui
   televisione (`cdn tv gratis`), icone (`iconos gratis cdn`) e indonesiano (`apakah cdn gratis`); `cms gratuito`
   era per metà spagnolo e portoghese. Gli unici utili contengono **un nome di prodotto**.

## Varianti delle immagini: il suffisso si misura, non si indovina

Su 1629 `-1024x576` e `-768x432` danno **404**; la variante vera è **`-1024x687`**. Prima di correggere in
blocco i `src` di tutte le pagine, **provare i suffissi con `curl -w '%{http_code} %{size_download}'`** e usare
quello che risponde 200.

## Trappole delle abilità MCP (sito)

- `meta/get-post-meta` richiede **`post_id` E `keys`** (una lista di chiavi, es.
  `['_sito_seo_title','_sito_seo_description','_sito_seo_keyword']`). Senza `keys` l'abilità rifiuta.
- **Dopo 3 chiamate rifiutate il server MCP si mette in pausa** (~60 s) e rifiuta anche le chiamate corrette:
  **non insistere**, sistemare gli argomenti e aspettare.
- **`meta/get-post-meta` non è l'unica strada**: `GET /wp-json/wp/v2/posts/{id}?context=edit` espone `meta`
  con **`_sito_seo_faq`, `_sito_seo_howto`, `footnotes`** (le FAQ si leggono per intero, utili per citarle),
  **ma non** il titolo SEO, la description e la keyword: quelle restano solo dall'abilità.
