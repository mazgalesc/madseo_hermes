# Funnel e ripubblicazione: come si classifica un contenuto e cosa se ne ricava

> Riferimento della **§3** (piano) e della **§9** (ripubblicazione) del `SKILL.md`.
> Era in inglese con termini non spiegati (`Statistical Burstiness`, `Authority Post`): tradotto e
> allineato alle misure che la skill usa davvero.

## 1. Lo stadio di funnel (TOFU / MOFU / BOFU)

Ogni voce del piano ricade in uno dei tre stadi, e **lo stadio si deriva dall'intento** della voce (colonna
«intenzione» del piano), non si sceglie a parte:

| Stadio | Intento | Cosa si scrive | Esempio di forma |
|---|---|---|---|
| **TOFU** — consapevolezza | informativo | guide ampie, «cos'è», «come funziona», problemi generali | «Guida completa a X nel 2026» |
| **MOFU** — valutazione | problem solving, commerciale | tutorial passo passo, confronti «X contro Y», scomposizioni di metodo | «X contro Y: confronto su 20 punti» |
| **BOFU** — decisione | transazionale | casi concreti, conti in chiaro, prove fatte sul campo | «Quanto rende X: i conti con i numeri veri» |

**Regola del piano**: un calendario sano sta intorno al **50% TOFU, 30% MOFU, 20% BOFU**. Il mix si controlla
sulla colonna `funnel_stage` del database, non a memoria.

## 2. Le categorie del sito e il loro stadio

Le categorie del blog sono quelle del sito (`wp_category_id` nel database), e la corrispondenza con gli stadi
**si legge dal sito**, non si inventa: `GET …/wp-json/wp/v2/categories?per_page=100&_fields=id,name,count`.
Un sito può avere una categoria **riservata alla piattaforma** (BOFU) che non è un tema editoriale: le sue voci
non si contano nel mix dei contenuti.

Il **nome** della categoria si legge, non si deduce, e **i conteggi cambiano a ogni pubblicazione**: nel piano
si scrivono gli ID, i numeri si leggono quando servono (`X-WP-Total`).

## 3. La ripubblicazione: da un articolo a tre pezzi

Per ogni articolo portato a termine si ricava un pacchetto di distribuzione:

| Pezzo | Misura | Come |
|---|---|---|
| **Thread per X** | **7-10 tweet** | l'articolo si **spezza** in passaggi: uno per concetto, il primo che promette qualcosa di concreto, l'ultimo che linka. Non è l'articolo riassunto in tre righe |
| **Post LinkedIn** | 150-250 parole | narrativo: un episodio, una prova, un numero dell'articolo, poi il link |
| **Teaser newsletter** | 150 parole | introduce la curiosità e linka l'articolo — è l'unico dei tre che può finire in chat così com'è |

L'articolo **non si riassume tre volte**: ogni pezzo prende un angolo diverso, altrimenti i tre canali dicono la
stessa cosa e nessuno dei tre porta traffico.

**La regola dello sforzo**: 80% del lavoro sulla distribuzione del 20% dei contenuti che valgono — cioè un
pilastro si ripubblica, dieci articoli minori no. Si salva tutto in `~/seo-content/distribution/`.

**Prima di consegnare** valgono i tre controlli della §9: nessun termine della lista bandita
(`references/humanizer_config.json`), nessun aneddoto inventato (la voce in prima persona è dell'autore), e i
numeri del pezzo uguali a quelli dell'articolo.
