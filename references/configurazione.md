# Configurazione: nomi generici qui, valori reali fuori dal repository

> Il testo di questa skill usa **nomi generici**, così il metodo vale per qualunque sito. I valori concreti
> di una installazione (dominio, nomi dei server, percorsi, identificativi delle proprietà) **non stanno
> nel repository**: stanno in un file locale di configurazione, accanto alla cartella di lavoro.
>
> **Dove**: `CONFIGURAZIONE.md` nella cartella di lavoro (la stessa che contiene `shared/` e `audits/`).
> Se il file non c'è, i nomi generici valgono come esempio e vanno adattati prima di usare la skill.

## La mappa dei nomi generici

| Nel testo della skill | Nella installazione | Dove si dichiara |
|---|---|---|
| `il-tuo-sito.it` | il dominio del sito | `SITE_DOMAIN` |
| `sito` | nome del server MCP in Hermes e del profilo del browser | `CONFIGURAZIONE.md` |
| `seo/*` | namespace delle abilità del plugin SEO | `CONFIGURAZIONE.md` |
| `tema`, `tema-blocks` | nome del tema a blocchi e del suo plugin | `CONFIGURAZIONE.md` |
| `~/seo-content/` | cartella di lavoro (`content/`, `audits/`, `distribution/`, `shared/`) | `SEO_WORK_DIR` |
| `shared/lavoro.db` | database del piano editoriale | `CONFIGURAZIONE.md` |
| `wp-credentials.env` | file delle credenziali WordPress (permessi 600) | `WP_CREDENTIALS` |
| `WP_BASIC_AUTH` | credenziale per l'MCP del sito | `~/.hermes/.env` |
| `SITE_MCP_URL` | indirizzo dell'endpoint MCP del sito | `SITE_MCP_URL` |
| `properties/<ID-GA4>` | proprietà di Google Analytics 4 | `GA4_PROPERTY_ID` |
| il vault Obsidian | percorso delle note dei contenuti | `OBSIDIAN_VAULT_PATH` |

## Le variabili d'ambiente che leggono gli script

| Variabile | A cosa serve | Se manca |
|---|---|---|
| `SEO_WORK_DIR` | cartella di lavoro | ripiega su `~/seo-content` |
| `SITE_DOMAIN` | dominio del sito (link interni, intestazioni dei rapporti) | ripiega su `il-tuo-sito.it` |
| `SITE_MCP_URL` | endpoint MCP del sito | ripiega su un indirizzo di esempio |
| `WP_CREDENTIALS` | file delle credenziali WordPress | ripiega su `~/.hermes/secrets/wp-credentials.env` |
| `GA4_PROPERTY_ID` | proprietà Analytics | **obbligatoria** per il report Analytics |
| `OBSIDIAN_VAULT_PATH` | vault delle note | la skill `obsidian` cerca in `~/Documents/Obsidian Vault` |

## Regola

**Nessun valore di una installazione entra nel repository** — né dominio, né percorsi assoluti, né
identificativi di proprietà, né nomi di persona. Il metodo sì: quello è la parte che si condivide.
Quando si trova nel testo un nome concreto al posto di uno generico, è un errore da correggere: quei
dettagli vanno nel file locale di configurazione.
