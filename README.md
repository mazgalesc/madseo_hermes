# SEO CONTENT — skill per Hermes Agent

`https://github.com/mazgalesc/madseo_hermes` — licenza MIT, contributi via pull request.

**Una skill per chi scrive contenuti SEO su WordPress in italiano, e vuole che i numeri siano veri.**

Non è un insieme di prompt: è un **metodo di lavoro**, con le sue regole, i suoi controlli e i suoi
strumenti. È nata per un blog italiano di affiliazione su WordPress e si adatta a un altro sito cambiando
i riferimenti agli strumenti — le regole restano.

**Il principio che la tiene insieme: un articolo che pubblica un numero deve poter dimostrare da dove viene
quel numero.** Quando il dato non c'è, si scrive che non c'è. È il difetto che questa skill combatte per
prima, ed è quello che in un audit di 45 articoli e 15 bozze ha fatto la differenza.

---

## Cosa fa

| Giro di lavoro | Cosa produce |
|---|---|
| **Scrivere un articolo** | immagini, bozza su WordPress, campi SEO, schema, controlli incrociati prima di dire «pronto» |
| **Verificare un articolo pubblicato** | un rapporto con correzioni, verdetto e numeri verificati uno per uno |
| **Verificare una bozza** | la stessa disciplina, applicata a campi, fonti e prontezza alla pubblicazione |
| **Pianificare** | il calendario dei contenuti **senza duplicare** quello che il sito ha già, e la scelta delle parole chiave per intento |
| **Ricerca** | come si legge una SERP, i suggerimenti di Google, Reddit/Quora/forum **citati con nome e link**, e a quali fonti credere |
| **Dopo la pubblicazione** | quota di voce nelle risposte AI, Search Console, Analytics, manutenzione trimestrale |

## Le due regole che non si negoziano

1. **Mai pubblicare.** Il massimo consentito è creare una **bozza** su WordPress. Lo stato di un contenuto
   è una decisione di chi firma, mai dell'agente.
2. **Ogni scrittura in produzione** (metadati SEO, schema, redirect, link interni, impostazioni) richiede
   un **ok esplicito per quella singola azione**, con il payload mostrato prima. Tutto il resto è **sola
   lettura** e si può fare liberamente.

## Le regole editoriali che contano (e che sono costate di più)

- **Ogni numero ha una fonte apribile.** Niente dataset, campioni, benchmark o «il nostro team»: se non
  esiste l'URL, il numero non entra.
- **Le fonti anonime non esistono.** «Un consulente», «un esperto», «su Quora un tecnico» non sono fonti.
  Se una persona si cita, si cita con nome, luogo e data — meglio se con il link.
- **Le prove di prima mano dichiarano strumento, versione, data e comando.** Una prova che non si può
  rifare non è una prova.
- **Il testo deve tornare con sé stesso.** Ogni elenco annunciato con un numero viene contato; ogni conto
  viene rifatto a mano; la sintesi non può contraddire la prova che la pagina ha appena portato.
- **Le eccezioni sono la parte che l'IA non scrive.** Ogni guida operativa ha un capitolo «quando non
  serve» e «quando va male».
- **Sull'affiliazione: dichiarazione in chiaro + `rel="sponsored"` sui link in uscita + la dicitura che il
  programma pretende.** Tutte e tre, sempre.
- **Le convenzioni italiane vanno scritte**: IVA nei prezzi, marca da bollo, privacy e cookie policy,
  P.IVA nel footer, contributi INPS quando si parla di guadagni.

## Struttura del repository

```
SKILL.md                      il banco di lavoro: le due regole ⛔, la configurazione,
                              il metodo, le 13 procedure (dalla 0 alla 12)
README.md                     questo file
references/                   35 file, uno per argomento (indice completo in
                              references/indice-file.md)
  pianificazione-e-duplicati.md   inventario, promesse, cannibalizzazione
  parole-chiave.md                quali keyword scegliere e perché
  ricerca-webcmd.md               il giro di ricerca nei siti che chiedono l'accesso
  ricerca-omnichannel.md          i canali della ricerca
  fonti.md                        a chi credere, e cosa scrivere quando la fonte non c'è
  scrittura-articolo.md           come si scrive un articolo (regole, blocchi, FAQ, glossario)
  controlli-verifica.md           i controlli incrociati prima di dire «pronto»
  audit-contenuti-pubblicati.md   come si verifica un articolo pubblicato
  audit-bozze.md                  come si verifica una bozza
  trappole.md                     tutte le trappole verificate in un file solo
  ambiente-setup-maton.md         ambiente, webcmd, Search Console e Analytics
  abilita-mcp.md                  le abilità del sito e lo stile del tema
  indice-file.md                  l'elenco completo dei file e quanto pesa ognuno
  primo-avvio.md                  la procedura 0 passo per passo (primo avvio)
  configurazione.md               i nomi generici del testo e i valori reali di una installazione
  vault-obsidian.md               il progetto editoriale nel vault Obsidian
  pubblicazione-e-contributi.md   pubblicare la repo senza esporre segreti, cosa chiedere a una PR
  immagini-e-stili.md, stile-copertine.md, stile-infografiche.md
  schema-google-support.md, schema-architect-logic.md, db-schema.md
  content-structure-templates.md, title-formulas.md, writer_quality.md, …
LICENSE                       MIT
scripts/
  controlla-articolo.py       i controlli incrociati automatici (candidati da verificare a mano)
  verifica-avvio.py           il controllo d'avvio: cartella, database, credenziali (mai i valori), MCP, REST, Maton
  genera-immagine.py          copertine (16:9, 4K → 1408×768)
  genera-infografica.py       infografiche (3:2, 2K → 1264×848)
  stato-sito.py               riepilogo in sola lettura: SEO + Search Console + Analytics
  calendario.py               il piano editoriale
```

**Regola di manutenzione**: una lezione nuova va nella sezione giusta di `references/`, non in fondo a
`SKILL.md`. `SKILL.md` resta il banco di lavoro (regole, mappa, metodo): se supera i 60.000 byte, si
sposta qualcosa in un reference, e ogni reference nuovo va anche **citato nella mappa**, altrimenti è
invisibile.

**Guide di stile misurate sul sito** (settembre 2026): `stile-copertine.md` (30 copertine: illustrazioni
vettoriali flat, sfondo indaco `#292655`, accenti oro, nessun testo, 1408×768) e `stile-infografiche.md`
(101 infografiche: schemi didattici su fondo chiaro, card bianche, accenti `#3343aa`, molto testo in
italiano, 1264×848).

## Installazione

Richiede [Hermes Agent](https://github.com/NousResearch/hermes-agent).

```bash
git clone https://github.com/mazgalesc/madseo_hermes.git
mkdir -p ~/.hermes/skills/productivity
cp -R madseo_hermes ~/.hermes/skills/productivity/seo-content
hermes skills list | grep seo-content
```

La cartella deve chiamarsi `seo-content` (è il nome dichiarato nella skill). Poi si fa la **procedura 0**.

## Cosa serve perché funzioni

La skill è cablata su strumenti precisi. Sono sostituibili, ma vanno sostituiti **nel testo**, non
ignorati.

1. **Server MCP del sito WordPress** — le abilità del plugin SEO e del block editor si chiamano attraverso
   l'MCP. **L'header di autenticazione dipende dal server: si prova `Authorization` e poi `Auth`**, e si
   tiene quello che risponde — sul sito per cui è nata la skill `Authorization` risponde 200 e `Auth` dà 401:
   ```bash
   hermes config set mcp_servers '{sito: {url: "https://il-tuo-sito.it/wp-json/mcp/mcp-adapter-default-server", headers: {Authorization: "${WP_BASIC_AUTH}"}}}'
   ```
   Se risponde **401** l'header o la credenziale sono sbagliati; **405** significa credenziali accettate e
   metodo sbagliato per l'handshake; **400** che manca il protocollo nella richiesta.
2. **Credenziali WordPress** in `~/.hermes/secrets/wp-credentials.env` (permessi 600): utente e application
   password, per la REST API.
3. **Search Console e Analytics**: qui si usa **Maton** (gateway HTTP). Verificato l'11/10/2026: bastano
   due `curl`, nessuna skill da installare. In alternativa, le API di Google dirette.
4. **Python 3** per gli script — solo libreria standard, nessuna dipendenza da installare — e **`sqlite3`**
   per il database del piano (su macOS c'è di serie; se manca, si installa).
5. **Cartella di lavoro** `~/seo-content/` con `content/`, `audits/`, `distribution/`, `shared/` e il database
   del piano editoriale (`shared/lavoro.db`, schema in `references/db-schema.md`).
6. **Un vault Obsidian gratuito** (locale, fatto di file markdown) per le note dei contenuti: promessa,
   collegamenti, fonti con la data in cui sono state lette. Il percorso si dichiara in
   `OBSIDIAN_VAULT_PATH` dentro `~/.hermes/.env` (la skill `obsidian` di Hermes altrimenti cerca in
   `~/Documents/Obsidian Vault`). Convenzione completa: `references/vault-obsidian.md`.
7. **Opzionali**: [Scrapling](https://github.com/D4Vinci/Scrapling) per le pagine che bloccano, `webcmd`
   per i siti che chiedono l'accesso, il browser interno di Hermes per tutto il resto.

## Configurazione

Il testo della skill usa **nomi generici** (`il-tuo-sito.it`, `sito`, `seo/*`, `~/seo-content/`): valgono
per qualunque sito. **I valori concreti di una installazione non stanno nel repository** — dominio, nomi dei
server, percorsi, identificativi delle proprietà Analytics — ma in un file locale di configurazione
(`CONFIGURAZIONE.md` nella cartella di lavoro). La mappa dei nomi e le variabili d'ambiente che leggono gli
script sono in `references/configurazione.md`.

## Nessun segreto in questo repository

Qui non ci sono chiavi, password o token: solo i **riferimenti** ai file locali che li contengono. Le
credenziali vivono fuori dal repo, in file con permessi 600.

## Come si usa

- **Primo avvio (una volta sola)**: `python3 scripts/verifica-avvio.py` controlla in sola lettura cartella di
  lavoro, database del piano, credenziali (presenza e permessi, **mai i valori**), vault, server MCP (prova
  entrambi gli header), sito, REST, Maton e proprietà Analytics, e riassume quello che manca senza bloccare.
  I passi da fare stanno in `SKILL.md` → **procedura 0**, spiegati per intero (comandi, indizi sugli errori,
  controllo finale, modello di `CONFIGURAZIONE.md`) in `references/primo-avvio.md`. Serve a far combaciare i
  nomi generici del testo con la propria installazione: senza, la skill chiede cose che non esistono.
- **Scrivere**: `SKILL.md` → «Il giro completo di un articolo, passo per passo».
- **Verificare un pubblicato**: `references/audit-contenuti-pubblicati.md`.
- **Verificare una bozza**: `references/audit-bozze.md`.
- **Pianificare senza duplicare**: `references/pianificazione-e-duplicati.md`.
- **Le note dei contenuti**: `references/vault-obsidian.md` (vault Obsidian, gratuito).
- **Prima di dire «pronto»**: `references/controlli-verifica.md` e lo script.

Lo script di controllo **non dà verdetti**: stampa i punti da guardare a mano.

```bash
python3 scripts/controlla-articolo.py bozza.json         # contenuto salvato (JSON del plugin)
python3 scripts/controlla-articolo.py pagina.html        # pagina pubblica
python3 scripts/controlla-articolo.py --parole testo.md  # conteggio parole, PRIMA di creare la bozza
python3 scripts/controlla-articolo.py --json file.html   # output leggibile da altri script
```

Cosa cerca: numeri annunciati contro le voci degli elenchi vicini, uguaglianze aritmetiche da rifare,
artefatti di produzione rimasti nel testo (`u/`, `r/`, `PT2H`, backtick, «Risposta diretta:», «Updated on»),
l'HTML escapato a video, i testi alternativi di tutte le immagini, i link interni con etichetta e
destinazione, le ripetizioni **a mezza frase** (quelle che il confronto a frase intera non vede) e le
intestazioni senza corpo sotto.

## Come contribuire

Le PR sono benvenute, e una buona PR qui è **una lezione verificata**, non un'opinione.

1. Apri una **issue** se la proposta è una modifica di metodo: prima si discute, poi si scrive.
2. Fork, ramo, pull request.
3. In ogni PR: **cosa cambia**, **in quale file**, e **il caso reale che l'ha dimostrato** (un articolo, una
   pagina, un errore trovato sul campo). Una regola senza il caso che l'ha generata invecchia male.
4. **Una regola per volta**, nella sezione che possiede già quell'argomento. Se non esiste, si crea un
   reference nuovo **e si aggiunge alla mappa in `SKILL.md`**.
5. **Non generalizzare da un caso isolato** e non introdurre strumenti a pagamento come necessari.
6. Se tocchi gli script, provali su un contenuto vero prima di proporli.

## Licenza

**MIT** — vedi il file `LICENSE`. È la licenza che rende semplici i contributi: si può usare, modificare e
ridistribuire, anche in progetti commerciali, mantenendo l'avviso di copyright.

## Crediti

Nata come porting di una versione precedente della skill (OpenClaw): nella versione originale i 12 «tool» non
erano codice, ma istruzioni per l'agente con i percorsi dei documenti di conoscenza. Il porting ha
ricablato le dipendenze sugli strumenti di Hermes:

| Nella versione OpenClaw | Qui |
|---|---|
| skill `api-gateway` (Search Console / Analytics) | gateway HTTP via `curl` |
| plugin Rank Math / Yoast | abilità del plugin SEO del sito **via MCP** |
| skill `agent-browser` | il browser interno di Hermes |
| skill `scrapling-official` | Scrapling in un ambiente Python dedicato |
| credenziali nel workspace condiviso | `~/.hermes/secrets/` e `~/.hermes/.env`, file 600 |

I 12 «tool» sono diventati le **13 procedure** descritte in `SKILL.md` (dalla 0 alla 12: la 0 è il primo avvio).
