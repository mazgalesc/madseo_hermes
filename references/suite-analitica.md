# La suite analitica: una chiamata, tre analisi, e cosa fare quando i dati non ci sono

> Riferimento della **§11** del `SKILL.md`. Tutto passa da **Maton**: una sola chiamata a Search
> Console, e cambia solo la dimensione. Lo script che la fa già funzionare è `stato-sito.py`
> (riepilogo del sito) e, per un uso da riga di comando, `scripts/gsc.py`
> (`python3 gsc.py --days 90 --dims query`).

## 1. La chiamata

```
POST /google-search-console/webmasters/v3/sites/<sito>/searchAnalytics/query
```

| Analisi | `dimensions` | Cosa si guarda |
|---|---|---|
| `low_ctr` | `["query"]` | query con molte impression e pochi clic |
| `decay` | `["page"]` | URL che perdono anno su anno |
| `cannibalization` | `["query","page"]` | più URL che si contendono la stessa query |

**La finestra è di 90 giorni, non di 28**: con poche impression il mese singolo non ha materia, e le
soglie sembrano superate solo perché il denominatore è minuscolo. La finestra si dichiara nel
rapporto, perché un numero senza la sua finestra non è confrontabile.

`sites/<sito>` vuole l'URL **codificato** (`https%3A%2F%2Fil-tuo-sito.it%2F`), come fa `stato-sito.py`.
Le date vanno esplicite (`startDate`/`endDate`), non «ultimi 90 giorni»: l'API non lo capisce.

## 2. Le soglie

| Analisi | Soglia | Cosa si propone |
|---|---|---|
| `low_ctr` | impression alte **e** CTR sotto la media della finestra per quella posizione | titolo e schema nuovi — la pagina viene vista e non cliccata |
| `decay` | perdita **oltre il 20%** anno su anno sulla stessa URL | ingresso nella coda di manutenzione (`refresh_at`, §3-bis) |
| `cannibalization` | la stessa query con **due o più** URL nostri, entrambi con impression | uno solo resta, l'altro si consolida |

**Una soglia non è una decisione.** La soglia dice quali pagine *guardare*: l'esito (aggiornare,
consolidare, togliere) si sceglie con i tre criteri della §3-bis, e la manutenzione **propone** —
non si cancella, non si disindicizza e non si fonde niente senza un ordine esplicito dell'autore e
un elenco nominato di contenuti.

## 3. Prima di chiamarla cannibalizzazione: i due URL rispondono?

La regola «301 o canonical sul perdente» presuppone **due pagine vive**. Un URL che Google continua a
mostrare ma che oggi risponde **404** non è un concorrente: è un **vecchio indirizzo mai rediretto**,
e il rimedio è un redirect, non un consolidamento.

```bash
curl -s -o /dev/null -w '%{http_code}\n' <url-1>
curl -s -o /dev/null -w '%{http_code}\n' <url-2>
```

Verificato il 14/10/2026: l'unico caso segnalato era una pagina viva più un 404 senza redirect. Costa
niente e cambia l'intervento.

## 4. Quando i dati non ci sono (è la condizione normale di un sito giovane)

Con poche query nella finestra e meno di un anno di storico, **due analisi su tre non producono
niente**: `low_ctr` non ha candidate (non c'è una media da cui stare sotto), e `decay` non ha la
finestra anno-su-anno. Verificato il 14/10/2026: 12 query in 90 giorni, zero candidate `low_ctr`,
zero righe per il confronto annuale.

**Si dichiara e si passa oltre**: «non c'è ancora materia per `decay`: meno di un anno di storico».
**Non si abbassano le soglie per far uscire qualcosa** — un segnale che nasce da una soglia
abbassata è un segnale che poi va ignorato, e nel frattempo ha fatto perdere un giro di lavoro.

Un avvertimento di Google da tenere presente: **le query a volume molto basso non compaiono affatto**
(passano a «(other)»). L'assenza di una query qui **non prova** che la domanda non esista.

## 5. L'output

Un file per giro in `~/seo-content/audits/`, con dentro: la finestra usata, la data della misura, e
per ogni analisi le righe **con i numeri** (impression, clic, CTR, posizione) — non solo i nomi delle
pagine. Le righe che non hanno prodotto niente si scrivono lo stesso: «zero candidate» è un risultato,
e senza quella riga il giro dopo sembra non essere stato fatto.
