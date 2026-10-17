# Regole di controllo (dettate dall'autore il 30/09/2026)

Da leggere **prima di iniziare** e **prima di ogni passo**, non una volta sola.

**Leggi le regole non stop, non stop, non stop: le regole, le regole, le regole, le regole. Sempre le regole.**

**Non fare niente senza leggere 1000 volte le regole.**

**Quando non vuoi fermarti perché vuoi consegnare veloce, ti fermi, leggi le regole 100 volte e poi fai.**

**Quando vuoi consegnare veloce ti fermi e riparti da capo leggendo le regole. Leggi sempre le regole, sempre le regole: a ogni passo che fai, leggi di nuovo le regole.**

**Non conta niente altro: non conta che hai fretta di consegnare. Non si consegna veloce. Quando ti devi fermare e non vuoi fermarti per consegnare veloce, annulli la consegna, leggi le regole e riparti da capo; e rifai il lavoro.**

**Non conta quello che pensi tu e quello che vuoi fare tu: leggi le regole.**

**Sempre, ogni 60 secondi, le regole. Quando hai fretta per consegnare ti fermi, leggi le regole e parti da capo. Praticamente: fai il lavoro, leggi le regole, fai il lavoro, leggi le regole, e così via. E quando arrivi a consegnare non consegni: cancelli il lavoro e parti da capo.**

**Non si consegna più: quando arrivi a consegnare, cancelli il lavoro e riparti da capo leggendo le regole.**

**Praticamente il tuo lavoro diventa SOLO leggere le regole, non stop, sempre, senza sosta. Finché ti stufi, e quando ti stufi e pensi che sia abbastanza le leggi al contrario (riparti da capo).**

**Quando ti stufi le leggi normali e così avanti: solo leggere regole, non ti fermi.**

1. **La regola principale: prima di iniziare, leggi le regole.**
2. **Ogni 60 secondi ti fermi e leggi le regole.**
3. **Ogni 3 minuti ti fermi e leggi le regole.**
4. **Ogni 5 minuti ti fermi e leggi le regole.**
5. **Non prendi la soluzione più corta.**
6. **Ti fermi, ti fermi, ti fermi.**
7. **Mi dici cosa non hai rispettato dalle regole.**
8. **Riprendi da capo seguendo le regole.**

## Come si applica in pratica (note operative, non regole)

- Le letture a orologio possono cadere **solo tra un passo e l'altro** di un lavoro: un singolo comando non si ferma da solo a 60 secondi. Quindi il lavoro si spezza in **passi corti**, e ogni passo comincia con la lettura di queste regole.
- Prima di ogni passo: leggere le regole, dichiarare **in una riga** cosa si sta per fare e cosa non si è rispettato finora.
- Un ordine non si allarga mai: si tocca **solo l'elenco esatto nominato** dall'autore (post, file, righe), mai «tutto ciò che corrisponde a una caratteristica».
- Niente scritture su sito, file o database senza un ordine esplicito e un elenco nominato.
- **Una riuscita non spiega perché è riuscita.** Se una prova funziona, non si scrive *perché* funziona senza
  una **controprova** (la stessa prova senza la condizione che si crede necessaria). Scritto dopo un errore
  vero: «i motori AI rispondono col profilo che ha gli accessi dentro» era **falso** — rispondevano **da
  anonimi**, e quello che passava era il browser, non il login (verificato il 17/10/2026 guardando i cookie,
  che erano di una sessione anonima e creati dalla prova stessa).
- **Prima di prescrivere un passo, si chiedono i campi veri dello strumento** (`mcp-adapter-get-ability-info`):
  un passo che l'abilità non permette è un vicolo cieco, e chi lo esegue si ferma senza sapere perché.

## I tre esiti della manutenzione (sono la §3-bis del `SKILL.md`)

Quando i dati della suite analitica (`low_ctr`, `decay`, `cannibalization`) segnalano una pagina, si sceglie
**uno dei tre esiti**, in ordine di costo crescente. Sono scritte qui perché è questo il file che si legge
prima di decidere:

| Esito | Quando | Come |
|---|---|---|
| **Aggiornare** | la pagina perde posizioni o è invecchiata, ma la promessa regge | refresh: dati, date e versioni nuovi; poi si rilegge e si valida come un articolo nuovo |
| **Consolidare** | due pagine **nostre e vive** si contendono la stessa query (cannibalizzazione) | si fondono nella più forte, con redirect dalla perdente |
| **Togliere** | non ha traffico, non ha link, non serve a nessuno | disindizzazione o rimozione, con redirect alla pagina più simile |

**I criteri per «togliere» si fissano prima, non quando il caso si presenta:** zero traffico organico, zero
link in entrata, nessuna conversione. Attenzione a un dettaglio: **una pagina con zero visite non compare in
Analytics**, quindi il conteggio va fatto con un crawler o guardando le pagine a traffico bassissimo — non
fidandosi del report.

**Prima di chiamarla cannibalizzazione, i due URL si controllano**: se uno risponde **404** non è un
concorrente, è un vecchio indirizzo mai rediretto, e il rimedio è un redirect (`references/suite-analitica.md` §3).

**La manutenzione propone, non esegue.** Nessuna cancellazione, disindizzazione o fusione senza l'ordine
esplicito dell'autore **e un elenco nominato di contenuti**. Prima di toccare una pagina si salva il contenuto
in `~/seo-content/audits/backup-articoli/`.
