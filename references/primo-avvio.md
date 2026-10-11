# Primo avvio — la configurazione (procedura 0)

**Scopo**: far combaciare i **nomi generici** del testo della skill (`il-tuo-sito.it`, `sito`, `seo/*`,
`tema`, `~/seo-content/`) con l'**installazione vera**. Si fa una volta sola, all'inizio: senza, tutte le
altre procedure chiedono cose che non esistono.

**Chi fa cosa**: l'autore fornisce i valori e fa i login; l'agente crea, verifica e prova. **L'agente non
inventa nessun valore**: quello che non sa, lo chiede.

## Prima di cominciare: cosa serve

| # | Cosa | Chi | Obbligatorio? | Se manca |
|---|---|---|---|---|
| 1 | Cartella di lavoro con `content/`, `audits/`, `distribution/`, `shared/` | agente | sì | si crea (passo 1) |
| 2 | Database del piano: `shared/lavoro.db`, tabella `content_calendar` | agente | sì | si crea (passo 2) |
| 3 | Credenziali WordPress (application password) | **l'autore** | sì, per scrivere bozze | si lavora in sola lettura (pagine pubbliche) e si dichiara |
| 4 | Server MCP del sito in Hermes | agente, valori dall'autore | consigliato | bozze e contenuti via REST, più lento e incompleto |
| 5 | Vault delle note (Obsidian gratuito, locale) | autore (percorso) + agente (cartelle) | consigliato | la skill lavora senza, ma perde il collegamento fra promesse, fonti e contenuti |
| 6 | Variabili d'ambiente in `~/.hermes/.env` | agente | sì | gli script ripiegano su valori di esempio |
| 7 | `CONFIGURAZIONE.md` nella cartella di lavoro | agente, valori dall'autore | sì | i nomi generici restano senza corrispondenza |
| 8 | La prova finale (MCP, REST, Search Console, Analytics) | agente | sì | quello che manca si **dichiara** |

## Passo per passo

### 1. La cartella di lavoro
```bash
mkdir -p ~/seo-content/{content,audits,distribution,shared}
```
È il posto dove vivono i rapporti e il piano editoriale: **fuori dall'albero della skill**, così gli
aggiornamenti della skill non li toccano. Se si sceglie un altro percorso, si scrive in `SEO_WORK_DIR`.

### 2. Il database del piano
Tabella `content_calendar` con le colonne di `db-schema.md` (comprese `promessa` e `copre_gia`). Senza
`promessa` il controllo dei duplicati non ha niente da confrontare: è la colonna che conta.
Verifica: la tabella esiste e si apre.

### 3. Le credenziali (le fa l'autore, mai in chat)
- Application password di WordPress (utente → Profilo → Application Passwords): si consegna **fuori dalla
  chat**, in un file con permessi 600 (proposta: `~/.hermes/secrets/wp-credentials.env`).
- Credenziale per l'MCP del sito (Basic auth) in `~/.hermes/.env`.
L'agente **non scrive password in chat, non le ripete, non le mette nel repository**.

### 4. Il server MCP del sito
```bash
hermes config set mcp_servers '{sito: {url: "https://il-tuo-sito.it/wp-json/mcp/mcp-adapter-default-server", headers: {Authorization: "${WP_BASIC_AUTH}"}}}'
```
Indizi utili quando non funziona: **401** = header o credenziale sbagliati — **si prova `Authorization` e
poi `Auth`**: nel caso vero di questa installazione `Auth` dà 401 e `Authorization` dà 200; **405** =
credenziali accettate, metodo sbagliato per l'handshake; **400** al primo `initialize` = manca il
protocollo nella richiesta. Se lo si prova **a mano con curl** (cosa che lo script non fa): dopo
l'`initialize` ogni richiesta vuole anche l'header **`MCP-Protocol-Version: 2025-06-18`**, altrimenti
`tools/list` risponde «Invalid Request». **Il modo giusto resta lo strumento di Hermes**, non curl. L'endpoint è quello del **sito** (non del
template/della rete): le abilità di contenuto pubblicano lì.

### 5. Il vault delle note
Percorso in `OBSIDIAN_VAULT_PATH` dentro `~/.hermes/.env` (la skill `obsidian` altrimenti cerca in
`~/Documents/Obsidian Vault`). Cartelle, modello di nota e convenzioni: `vault-obsidian.md`.

### 6. Le variabili d'ambiente
In `~/.hermes/.env`, con i **valori veri** di questa installazione:
`SEO_WORK_DIR`, `SITE_DOMAIN`, `SITE_MCP_URL`, `WP_CREDENTIALS`, `GA4_PROPERTY_ID` (tabella completa in
`configurazione.md`). Verifica: far girare uno script della skill e controllare che trovi la cartella e il
database.

### 7. Il file `CONFIGURAZIONE.md` nella cartella di lavoro
Compilato con i valori reali: dominio, nome del server MCP, namespace delle abilità, plugin e tema,
percorsi, proprietà Analytics. **Non entra nel repository** (nessun valore di una installazione ci entra).

**Modello da copiare e compilare** (le voci che non servono si cancellano):

| Voce | Valore |
|---|---|
| Sito | `https://…` |
| Server MCP in Hermes | nome e header da usare (`Authorization` di norma; `Auth` solo se è quello che risponde) |
| Endpoint MCP | `https://…/wp-json/mcp/mcp-adapter-default-server` |
| Credenziali WordPress | percorso del file con permessi 600 |
| Cartella di lavoro | percorso (`SEO_WORK_DIR`) |
| Database del piano | `…/shared/lavoro.db` |
| Vault delle note | percorso (`OBSIDIAN_VAULT_PATH`) |
| Profilo del browser (`webcmd`) | nome del profilo |
| Namespace delle abilità SEO | `…/*` e quante sono |
| Plugin e tema | nomi |
| Analytics (GA4) | `properties/<ID>` e account |
| Search Console | proprietà e permesso |
| Altri siti dello stesso proprietario | solo se servono alla ricerca |

### 8. La prova finale
**Si fa con uno script**: `python3 scripts/verifica-avvio.py` — cartella di lavoro, database, credenziali
(presenza e permessi, mai i valori), vault, MCP (prova entrambi gli header), REST, Maton e proprietà
Analytics, con il riepilogo di quello che manca. Il resto delle verifiche è in `ambiente-setup-maton.md`: MCP (handshake), REST (con l'header giusto),
Search Console e Analytics (via curl a Maton), browser e `webcmd`. Quello che manca **si dichiara**:
immagini, Scrapling e `ddgs` sono **opzionali** e hanno il loro ripiego — non bloccano il resto.

## Il controllo finale

- [ ] cartella di lavoro con le quattro sottocartelle e il database con la tabella
- [ ] credenziali consegnate fuori chat, file con permessi 600
- [ ] server MCP: l'`initialize` risponde
- [ ] variabili d'ambiente impostate e provate con uno script
- [ ] `CONFIGURAZIONE.md` compilato
- [ ] vault collegato (se si usa)
- [ ] la prova dice OK su quello che serve; quello che manca è dichiarato
- [ ] **nessun valore reale nel repository**: un `grep` finale dei nomi concreti nei file pubblicabili

## Quello che non si fa

- **Non si inventano valori.** Un nome generico senza corrispondenza reale è un errore di configurazione.
- **Non si chiedono né si scrivono password in chat.**
- **Non si pubblica nulla**: il contenuto lo pubblica solo l'autore (regola 1).
- **Non si mettono percorsi, domini o identificativi nel repository**: stanno nel file locale.
