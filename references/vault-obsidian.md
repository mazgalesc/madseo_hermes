# Il vault Obsidian: dove vive il progetto editoriale

> **Regola**: il progetto editoriale di questo sito si tiene in un **vault Obsidian** — gratuito, locale, fatto
> di file markdown. Il database (`content_calendar`) dice **cosa** è pianificato; il vault dice **cosa dice
> ogni contenuto**: la promessa, i collegamenti, le fonti, quando ogni dato è stato verificato.
>
> **Vault in uso**: `~/Documents/hermes` (registrato in Obsidian, verificato l'11/10/2026).
> Il percorso si risolve dalla variabile **`OBSIDIAN_VAULT_PATH`** (`~/.hermes/.env`), che è la convenzione
> della skill `obsidian` di Hermes: **non passare mai la variabile a un file tool**, si passa il percorso
> assoluto già risolto.

## 1. Perché serve, su questo sito (non è una preferenza)

I difetti più costosi trovati nell'audit si sarebbero visti **subito** con un vault:

| Difetto trovato | Come lo avrebbe mostrato il vault |
|---|---|
| **Quattro pagine orfane** (`224`, `1441`, `1412`, `1452`) | il **grafo** di Obsidian mostra le note senza collegamenti in entrata |
| **Cannibalizzazione**: `204`/`212` sullo stesso tema, cinque articoli di affiliazione in cerchio | la nota-mappa del cluster mostra due note con la stessa promessa |
| **Promesse non mantenute** (guide citate senza link, contenuti promessi e assenti) | la promessa è scritta in chiaro nella nota: si confronta, non si deduce |
| **Dati che invecchiano** (prezzi, versioni, date) | ogni fonte nella nota porta **la data in cui è stata letta** |
| **Le fonti sparite** (i rapporti di ricerca citati dalla skill e non più presenti) | le note di ricerca vivono nel vault, non in una cartella temporanea |

## 2. Struttura del vault

```
Contenuti/     una nota per contenuto (pubblicato, in bozza, programmato)
Promesse/      l'indice delle promesse: una nota-mappa per cluster
Ricerca/       una nota per giro di ricerca, con le fonti e le date
Fonti/         una nota per fonte citata più di una volta
Idee/          i candidati non ancora entrati in calendario
```

**Nomi dei file**: `Contenuti/<id> <slug>.md` (es. `Contenuti/1452 keyword-research-blog-di-affiliazione.md`) —
l'id all'inizio rende univoco il titolo e collega la nota a WordPress, allo script e al database.

## 3. La nota di un contenuto

Frontmatter (le stesse chiavi del database, così le due fonti non divergono senza accorgersene):

```markdown
---
id: 1452
slug: keyword-research-blog-di-affiliazione
url: https://il-tuo-sito.it/keyword-research-blog-di-affiliazione/
stato: pubblicato          # idea | programmato | bozza | pubblicato
categoria: Affiliazione
keyword_primaria: keyword research blog di affiliazione
intento: informativo
promessa: "spiega come trovare le keyword di un blog di affiliazione partendo dall'intento, non dal volume"
aggiornato: 2026-10-11
---

# Keyword research per un blog di affiliazione

## Promessa
Una riga, scritta come *«promette di…»*. È il campo su cui si confrontano i contenuti nuovi
(`pianificazione-e-duplicati.md`).

## Struttura
- H2 come sono nella pagina, **uno per riga**.

## Collegamenti
- [[1449 prodotti-da-promuovere-affiliazione]] — in uscita: la frase dove sta il link
- [[1412 creare-menu-navigazione-wordpress]] — in entrata: chi la cita
(questi wikilink **sono** la mappa dei link interni: se una nota non ha link in entrata,
la pagina è orfana — è così che si vedono i quattro casi trovati nell'audit)

## Fonti
| Cosa | Fonte | Letta il |
|---|---|---|
| volumi/forma della domanda | suggerimenti Google (frase intera) | 2026-10-11 |
| … | … | … |

## Verifiche fatte
- [ ] promessa non coperta da un altro contenuto
- [ ] conteggi annunciati = voci degli elenchi
- [ ] conti rifatti a mano
- [ ] fonti aperte e lette (non solo link vivi)
- [ ] alt di tutte le immagini
- data dell'ultima verifica: 2026-10-11

## Da fare
- …
```

## 4. Regole d'uso

1. **La nota nasce quando la voce entra in calendario** (stato `programmato`), non quando si scrive: è lì
   che si scrive la promessa, ed è lì che si scoprono i doppioni **prima** di scrivere.
2. **Si aggiorna a ogni modifica dell'articolo** — compreso il cambio di titolo SEO, che è la promessa che
   il lettore vede su Google.
3. **La nota è la fonte del campo `promessa`** del database: se divergono, vince la nota (contiene anche le
   fonti e le date).
4. **Le fonti citate si scrivono nella nota con URL e data di lettura.** Quando un dato invecchia, si sa
   cosa ricontrollare e dove.
5. **I wikilink si mettono come nell'articolo**: le due cose si controllano a vicenda. Una nota senza link
   in entrata è una pagina probabilmente orfana.
6. **Niente doppioni**: prima di creare una nota, si cerca la promessa nel vault (ricerca nei file del
   vault, non nel titolo) — vedi `pianificazione-e-duplicati.md`.
7. **Il vault non è pubblico**: contiene note di lavoro. Se un giorno si pubblica qualcosa, si decide
   nota per nota.

## 5. Come ci si lavora (strumenti)

- **Leggere, cercare, scrivere** le note: i **file tools** di Hermes (`read_file`, `search_files`,
  `write_file`, `patch`) sul percorso assoluto del vault — non la shell. La skill `obsidian` di Hermes
  documenta le stesse operazioni.
- **Il percorso si risolve una volta**: `OBSIDIAN_VAULT_PATH` in `~/.hermes/.env` (impostato l'11/10/2026 su
  `~/Documents/hermes`). La skill `obsidian` ha come ripiego `~/Documents/Obsidian Vault`: su questa
  macchina **non esiste**, quindi la variabile è obbligatoria — senza, la skill cerca nel posto sbagliato.
- **Obsidian è gratuito** e i file sono markdown semplici: si leggono anche senza l'applicazione. Il vault
  si apre in Obsidian quando serve il grafo, i backlink o la ricerca visuale.
- **Titoli, tag e wikilink** restano leggibili da qualunque editor: nessuna funzione dell'app è
  indispensabile, l'integrazione è a livello di file.

## 6. Il ponte con il resto del lavoro

| Cosa | Dove vive | Chi lo aggiorna |
|---|---|---|
| cosa è pianificato, con keyword e intento | `~/seo-content/shared/lavoro.db` | il piano editoriale (§3 del `SKILL.md`) |
| cosa dice ogni contenuto, con fonti e date | il **vault** | chi scrive e chi verifica |
| la promessa, per il confronto anti-duplicato | il **vault** (e copiata nel database) | chi pianifica |
| le note di ricerca con le fonti | il **vault** (`Ricerca/`) | il giro di ricerca |
| le correzioni e i rapporti | `~/seo-content/archivio/correzioni_articoli/` e `correzioni_bozze/` | l'audit |

**Prima di dichiarare pronto un articolo**: la sua nota nel vault ha le fonti con le date, i collegamenti
aggiornati e la lista delle verifiche compilata. Se la nota non è aggiornata, l'articolo non è pronto —
perché nessuno saprà più da dove vengono i suoi numeri.
