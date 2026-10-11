# Prima di pianificare: l'inventario, la promessa, i duplicati

> Questo file risponde a una cosa sola: **come si sceglie un titolo senza pestare i piedi a quello che
> il sito ha già.** È il punto in cui il sito ha sbagliato di più: due articoli sullo stesso tema
> (`204` *Miglior hosting WordPress in Italia* e `212` *Hosting WordPress: cosa sapere*), un cluster di
> **cinque** articoli di affiliazione che si linkano in cerchio, e quattro pagine orfane.
>
> Sta **prima** di `parole-chiave.md` (che sceglie la keyword) e prima della scrittura.
> Ricava la sua materia da: inventario dei contenuti, `seo/get-post-seo` (titolo e description
> vivi), le intestazioni della pagina, Search Console.

## 1. La regola che conta più di tutte: si confrontano le PROMESSE

Il confronto **non si fa sui titoli**. Un titolo è una stringa; la promessa è quello che la pagina dice
al lettore che troverà. Due titoli diversi possono promettere la stessa cosa, e due titoli simili
possono promettere cose diverse.

**Il caso reale che ha insegnato la regola (29/09/2026).** Il controllo automatico del piano dava
*«nessun conflitto»* sul candidato *«WordPress è lento: i 6 collo di bottiglia in ordine di quanto
costano»*. Ma l'articolo `223` aveva **in pagina** il tag SEO *«WordPress lento: cause e rimedi del sito
che rallenta»* e una description che prometteva *«in che ordine controllarle… e come misurare»* — cioè
**la stessa promessa**. La riga del database portava ancora il titolo vecchio (*«Errori comuni con
WordPress hosting…»*), quindi il controllo automatico non poteva vederlo.

**Conseguenza operativa**: la riga del database non è la verità. La verità è quello che c'è in pagina.

## 2. Inventario: quattro elenchi, non uno

Prima di qualsiasi scelta si costruiscono **tutti e quattro** gli elenchi. Un contenuto che si dimentica
è un contenuto che si duplica.

| Elenco | Da dove | Perché serve |
|---|---|---|
| **Pubblicati** | REST `posts?status=publish&per_page=100` (via MCP o curl con application password) | è la base: le promesse già mantenute |
| **Bozze** | `posts?status=draft` | ⚠️ **una bozza già copre una promessa**: se è in coda, il titolo nuovo non entra |
| **Programmati** | `posts?status=future` | sono promessi al lettore e a Google |
| **Cestinato** | `posts?status=trash` | serve a non riproporre qualcosa scartato di proposito |
| Pagine (non post) | `pages?per_page=100` | glossario, documentazione, contatti: occupano query anche loro |

L'inventario si salva in un file rigenerabile (`INVENTARIO.md` nella cartella di lavoro condivisa), con
per ogni voce: **id, stato, slug, titolo nativo, titolo SEO, description, categoria**.

**Poi** si aggiungono le due liste che nessun elenco di WordPress dà:
- le **pagine orfane** (zero link in entrata) — servono alla §8 del `SKILL.md`;
- le promesse **già scritte ma non linkate** (*«le trovi nella nostra guida…»* senza link): sono promesse
  a metà, e vanno risolte prima di aggiungere contenuti nuovi.

## 3. Estrarre la promessa di un contenuto

Per ogni contenuto (esistente o candidato) la promessa si legge da tre cose, in quest'ordine:

1. **titolo SEO** (`seo/get-post-seo` → `title`) — è quello che il lettore vede su Google;
2. **description** — è la promessa in chiaro, quasi sempre scritta come *«come fare X, in che ordine, e
   quanto costa»*;
3. **le intestazioni H2/H3 della pagina** — sono l'indice di quello che la pagina consegna davvero.

Si scrive la promessa in **una riga**, in forma *«promette di: …»*. Due promesse si confrontano solo se
sono scritte così: *«promette di spiegare in che ordine controllare le cause di un sito lento, con le
misure»* contro *«promette di elencare i collo di bottiglia in ordine di costo»* → **coincidono**.

## 4. Il confronto, con tre esiti possibili

Per ogni voce in arrivo:

| Esito | Quando | Cosa si fa |
|---|---|---|
| **Coincide** | la promessa è la stessa di un contenuto pubblicato o in bozza | **la voce non entra nel piano.** Non si «differenzia il titolo»: si aggiorna il contenuto che c'è |
| **Coincide in parte** | c'è una sovrapposizione reale, ma la pagina esistente non copre la domanda | la voce entra **solo se si scrive nel piano quale parte copre ognuno** (una riga per contenuto) — e poi quelle due righe vanno rispettate scrivendo |
| **Libera** | nessuna promessa esistente la copre | la voce entra |

Il confronto si fa con i **contenuti semanticamente vicini** (10-15, non tutti i 45): stessa categoria,
stessa area, e i più recenti. Si leggono in blocco con `seo/get-post-seo`, non uno per uno a mano.

## 5. La mappa del cluster (per non far crescere un silo in cerchio)

Per ogni cluster attivo (hosting, affiliazione, guide AI, strumenti AI) si tiene una riga per contenuto:

| Contenuto | Promessa | Stadio (TOFU/MOFU/BOFU) | È la pagina perno? | Quanti link riceve / manda |
|---|---|---|---|---|

Serve a due cose: capire **chi copre cosa** (e quindi cosa non va riscritto), e vedere i **hub che non
distribuiscono** (ricevono link da mezza categoria e non ne mandano: il caso del `214`).

**Regola**: nel cluster non si aggiunge un contenuto nuovo finché la mappa non dice quale promessa copre
che gli altri non coprono. Il cluster affiliazione è arrivato a cinque articoli senza questa mappa.

## 6. Il database del calendario: due colonne che mancano

Alla tabella `content_calendar` servono due colonne (schema aggiornato in `db-schema.md`):

| Colonna | A cosa serve |
|---|---|
| `promessa` | la promessa in una riga, come in §3 — è il campo su cui si confronta |
| `copre_gia` | l'id del contenuto con cui la voce è vicina (o vuoto) — così la decisione resta scritta |

**Le righe senza `promessa` sono le righe da ricontrollare prima di scrivere**: sono quelle per cui non
si è ancora stabilito cosa la pagina promette. Non si inventa la promessa dopo: si ricava dal titolo SEO
del contenuto, quando esiste.

## 7. Il controllo in uscita (prima di pubblicare)

Il controllo non si fa solo all'ingresso. Prima di dire che un articolo è pronto:

1. la sua promessa **non è coperta da un altro contenuto** (ril eggendo l'inventario aggiornato);
2. **non ripete** un altro articolo: si confrontano gli H2 del nuovo con quelli dei vicini;
3. **linka i vicini di cluster** (e le pagine orfane se pertinenti) — un contenuto nuovo chiude il cerchio
   invece di aprirne uno;
4. se un altro articolo prometteva la stessa cosa, **la voce vecchia va aggiornata o fusa** (con redirect):
   la manutenzione del piano è in `SKILL.md` §3-bis e si propone, non si esegue senza ordine.

## 8. Trappole di questo passo (verificate sul sito)

- **La riga del database porta il titolo vecchio.** Non usarla per il confronto: il titolo SEO in pagina
  può essere stato cambiato dopo (§1).
- **Le bozze contano.** Una promessa coperta da una bozza è coperta: altrimenti si scrivono due volte.
- **Il cestinato non conta**, ma va letto: se una voce è stata scartata per un buon motivo, riproporla è
  ripercorrere lo stesso vicolo cieco.
- **Due articoli «diversi» sullo stesso tema si riconoscono dalla tabella**: se due contenuti hanno la
  stessa tabella di confronto (i provider nel `204`/`212`), sono lo stesso articolo scritto due volte.
- **Le pagine che non sono articoli** (glossario, documentazione) occupano query: vanno nell'inventario.
- **La cannibalizzazione si vede anche dai link**: se il più nuovo linka il più vecchio 7 volte sullo
  stesso argomento, Google li tratta come pagina + satellite (`212` verso `204`).
