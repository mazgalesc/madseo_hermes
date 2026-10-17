# Primo avvio — la configurazione (procedura 0)

**Scopo**: far combaciare i **nomi generici** del testo della skill (`il-tuo-sito.it`, `sito`, `seo/*`,
`tema`, `~/seo-content/`) con l'**installazione vera**. Si fa una volta sola, all'inizio: senza, tutte le
altre procedure chiedono cose che non esistono.

**Chi fa cosa**: l'autore fornisce i valori e fa i login; l'agente crea, verifica e prova. **L'agente non
inventa nessun valore**: quello che non sa, lo chiede.

**Da dove si lanciano i comandi.** I comandi di questa skill usano percorsi **relativi** (`scripts/…`): si
eseguono **dalla cartella della skill** — `~/.hermes/skills/productivity/seo-content/`, o
`~/.hermes/skills/<categoria>/<nome>/` se è installata altrove. Da un'altra cartella si usa il percorso
completo (`python3 ~/.hermes/skills/productivity/seo-content/scripts/verifica-avvio.py`) oppure si entra
prima nella cartella con `cd`. È il primo intoppo di chi arriva da fuori, e non dà un errore che lo spieghi:
dice solo che il file non esiste.

## Prima di cominciare: cosa serve

| # | Cosa | Chi | Obbligatorio? | Se manca |
|---|---|---|---|---|
| 1 | Cartella di lavoro con `content/`, `audits/`, `distribution/`, `shared/`, `archivio/` | agente | sì | si crea (passo 1) |
| 2 | Database del piano: `shared/lavoro.db`, tabella `content_calendar` | agente | sì | si crea (passo 2) |
| 3 | Credenziali WordPress (application password) | **l'autore** | sì, per scrivere bozze | si lavora in sola lettura (pagine pubbliche) e si dichiara |
| 4 | Server MCP del sito in Hermes | agente, valori dall'autore | consigliato | bozze e contenuti via REST, più lento e incompleto |
| 5 | Vault delle note (Obsidian gratuito, locale) | autore (percorso) + agente (cartelle) | consigliato | la skill lavora senza, ma perde il collegamento fra promesse, fonti e contenuti |
| 6 | Variabili d'ambiente in `~/.hermes/.env` | agente | sì | gli script ripiegano su valori di esempio |
| 7 | `CONFIGURAZIONE.md` nella cartella di lavoro | agente, valori dall'autore | sì | i nomi generici restano senza corrispondenza |
| 8 | La prova finale (MCP, REST, Search Console, Analytics) | agente | sì | quello che manca si **dichiara** |
| 9 | Le fonti dei dati delle parole chiave (Search Console via Maton, DataForSEO, Bing) | l'autore le chiavi, l'agente la verifica | no: il metodo resta completo senza | si dichiara il buco (`parole-chiave.md` §3) |
| 10 | **Il primo set di parole chiave** (semi, espansione, volume dove c'è) | agente, con l'autore che risponde sul posizionamento | sì, per poter pianificare | senza, il piano si costruisce a intuito |

## Passo per passo

### 1. La cartella di lavoro
```bash
mkdir -p ~/seo-content/{content,audits,distribution,shared,archivio}
```
È il posto dove vivono i rapporti e il piano editoriale: **fuori dall'albero della skill**, così gli
aggiornamenti della skill non li toccano. Se si sceglie un altro percorso, si scrive in `SEO_WORK_DIR`.

### 2. Il database del piano
Tabella `content_calendar` con le colonne di `db-schema.md` (comprese `promessa` e `copre_gia`). Senza
`promessa` il controllo dei duplicati non ha niente da confrontare: è la colonna che conta.

**Con il comando.** Non si scrive il `CREATE TABLE` a mano: **lo schema completo (17 colonne) è in
`db-schema.md`** e si copia da lì. Il file del database non esiste finché non glielo si fa creare da
`sqlite3`, quindi si passa il blocco direttamente:

```bash
sqlite3 ~/seo-content/shared/lavoro.db < schema.sql   # con il CREATE TABLE di db-schema.md in schema.sql
```

Attenzione a due cose: **lo schema completo include le cinque colonne aggiunte** (`keyword_primaria`,
`intento`, `refresh_at`, `promessa`, `copre_gia`) — crearne una versione ridotta significa rimediare dopo con
cinque `ALTER TABLE`; e il file **non si cancella per sbloccarlo** se risulta `database is locked` (le note
di esercizio sono in `db-schema.md`).

Verifica: la tabella esiste e si apre.

### 3. Le credenziali (le fa l'autore, mai in chat)
- Application password di WordPress (utente → Profilo → Application Passwords): si consegna **fuori dalla
  chat**, in un file con permessi 600 (proposta: `~/.hermes/secrets/wp-credentials.env`).
- Credenziale per l'MCP del sito (Basic auth) in `~/.hermes/.env`.
L'agente **non scrive password in chat, non le ripete, non le mette nel repository**.

**Come si chiamano le voci.** Nel file servono due righe: una che finisce in **`_USER`** (l'utente di
WordPress) e una che finisce in **`_APP_PASSWORD`** (l'application password). **Il prefisso è libero**
(`WP_`, il nome del sito, quel che si vuole): gli script riconoscono la chiave **dal suffisso**, quindi la
seconda metà del nome non è una scelta, la prima sì. Un file vuoto coi permessi già giusti si crea con
`touch ~/.hermes/secrets/wp-credentials.env && chmod 600 ~/.hermes/secrets/wp-credentials.env`.
Verifica: `ls -l` deve mostrare `-rw-------`.

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

### 9. I dati delle parole chiave (e il primo set)

**Prima si prova gratis che le chiavi siano vive** — mai una chiamata a pagamento per scoprire se una
chiave funziona:

```bash
python3 scripts/check_credentials.py
python3 scripts/check_credentials.py --term hosting --country it --language it-IT
```

Prova DataForSEO (`user_data`, costo 0), Bing (`GetKeywordStats`) e Maton (`/connections`, che elenca
Search Console e le due connessioni Analytics) e stampa **presenza e lunghezza, mai i valori**. Le
stesse prove sono già nella §8: qui servono per sapere *cosa si può chiedere* prima di scrivere il piano.

**Poi il primo set**, con l'ordine di `parole-chiave-strumenti.md` (il metodo è in `parole-chiave.md`):

1. **Search Console per prima** — `scripts/gsc.py --days 90 --dims page`: cosa il sito già prende e le
   quasi-vicine (posizioni 5-20) da riscrivere. Se non c'è niente, è un sito nuovo: si dichiara.
2. **Semi** — 10-20 termini dalle categorie attive del sito e dai problemi che il lettore ha davanti.
3. **Espansione gratuita** — `scripts/suggest.py` (Google + Bing, senza chiavi, nessun account).
4. **Volume, dove c'è** — `scripts/bing.py` (impression Bing, gratuito) e, se la chiave c'è,
   `scripts/volumes.py` per volume reale e difficoltà. **La spesa si propone prima di farla.**
5. **Dove finiscono i file** — `shared/keywords/`, un CSV per lotto **con la data nel nome**, più
   l'indice `shared/keywords/README.md` (cosa contiene, fonte, data, costo, comando per rifarlo,
   limiti). Le keyword scelte entrano nel piano (§3) e nel vault.

Un contenuto senza keyword dichiarata non entra nel piano: è il primo campo da riempire, non l'ultimo.

## Il controllo finale

- [ ] cartella di lavoro con le cinque sottocartelle (`content`, `audits`, `distribution`, `shared`, `archivio`) e il database con la tabella
- [ ] credenziali consegnate fuori chat, file con permessi 600
- [ ] server MCP: l'`initialize` risponde
- [ ] variabili d'ambiente impostate e provate con uno script
- [ ] `CONFIGURAZIONE.md` compilato
- [ ] vault collegato (se si usa)
- [ ] le chiavi delle parole chiave provate **gratis** (Maton, DataForSEO, Bing) e il buco dichiarato
- [ ] primo set di parole chiave in `shared/keywords/`, con l'indice `README.md` accanto
- [ ] la prova dice OK su quello che serve; quello che manca è dichiarato
- [ ] **nessun valore reale nel repository**: un `grep` finale dei nomi concreti nei file pubblicabili

## Quello che non si fa

- **Non si inventano valori.** Un nome generico senza corrispondenza reale è un errore di configurazione.
- **Non si chiedono né si scrivono password in chat.**
- **Non si pubblica nulla**: il contenuto lo pubblica solo l'autore (regola 1).
- **Non si mettono percorsi, domini o identificativi nel repository**: stanno nel file locale.
- **Non si spende per scoprire se una chiave funziona**: prima le prove gratuite (Maton `/connections`,
  DataForSEO `user_data`, Bing `GetKeywordStats`) — vedi il passo 9.
