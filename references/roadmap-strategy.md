# l'autore SEO: 12-Month Strategic Roadmap Logic

This reference governs the autonomous generation of long-term SEO growth plans. It uses a phased approach to build authority and displace competitors, integrated with WordPress category taxonomies.

## 1. Come si calcola la priorità

**La formula completa** — `Priority Score = (Volume mensile + Valore di business [1-10]) / Difficoltà` —
chiede volume e difficoltà, che **non arrivano dal livello gratuito**: si ottengono solo dal livello a
pagamento **opzionale** descritto in `parole-chiave.md` §3. Quindi la priorità si calcola **a due
velocità**, e la seconda non è «meglio» della prima: è la prima con due numeri in più.

**Senza volume e senza difficoltà** — il caso normale, e va benissimo così:

1. **La domanda già misurata (Search Console).** Per ogni candidata si legge quello che esiste già:
   **impression** (quanta domanda intercettiamo), **posizione media** (quanto siamo vicini), **clic e
   CTR** (se il clic lo vinciamo). Il caso d'oro è **impression alte + posizione 5-20**: è la distanza
   più corta fra noi e la prima pagina.
2. **Il valore di business dichiarato (1-10).** Un numero che decide **l'autore**, non l'agente: quanto
   quella domanda è vicina a un contatto o a un acquisto. Va scritto accanto alla voce di piano, così
   resta confrontabile fra voci diverse.

**Le tre famiglie di priorità:**

- **Vittoria vicina**: impression già presenti, posizione 5-20, valore dichiarato ≥ 6 → si lavora subito.
- **Costruzione**: nessuna impression (domanda nuova per il sito), valore alto → si lavora **dopo**,
  perché prima serve autorità sull'argomento.
- **Da non fare**: valore dichiarato 0-2, oppure intento **navigazionale** → non entra in piano.

**Con volume e difficoltà disponibili** (skill `seo-keyword-research` e `DATAFORSEO_LOGIN` nel file di
ambiente) ai due passaggi se ne aggiungono tre, e cambia il peso delle decisioni:

- **volume = filtro, non obiettivo.** Circa il 95% delle keyword sta sotto le 10 ricerche al mese: la
  coda lunga è quella che converte, e shortlistare per volume la butta via.
- **difficoltà = cancello d'ingresso.** Scarta in partenza ciò che non si può vincere, invece di
  scoprirlo dopo aver scritto l'articolo.
- **intento dichiarato = controprova** di quello letto dalla SERP, non un sostituto.

La formula si applica **solo alle candidate già filtrate per intento**: un punteggio alto su una keyword
con l'intento sbagliato resta un articolo che non porta nessuno. E i crediti si usano con le regole di
`parole-chiave.md` §3 — sandbox prima, lista intera in una richiesta, mai la coda `live`.

- **Topical Clusters**: Grouping keywords into silos to boost authority. *(resta valido: è la ragione
  per cui si costruiscono prima i temi vicini e poi quelli larghi.)*

Il dettaglio dei fattori, delle metriche e delle trappole sta in `parole-chiave.md`.

## 2. The 3-Phase Roadmap

### Phase 1: Foundations (Months 1-3)
**Objective**: Establish a footprint and secure early traffic.
- **Focus**: Long-tail keywords, Low competition (Difficulty < 30).
- **Strategy**: 
    - Focus on **TOFU (Awareness)** content.
    - Map to general WordPress categories (e.g., "Guides", "News").
    - Establish Topical Authority by covering basic concepts.

### Phase 2: Authority Building (Months 4-6)
**Objective**: Command topical authority in core clusters.
- **Focus**: Mid-difficulty keywords (Difficulty 30-60).
- **Strategy**:
    - Shift towards **MOFU (Consideration)** content.
    - Map to technical/specific WordPress categories (e.g., "SEO", "Plugins").
    - Create "Skyscraper" Pillar content (2500+ words) to anchor clusters.

### Phase 3: Competitive Acquisition (Months 7-12)
**Objective**: Displace market leaders for high-volume terms.
- **Focus**: High difficulty keywords (Difficulty 60+).
- **Strategy**:
    - Increase **BOFU (Decision)** content ratio.
    - Map to conversion categories (e.g., "Case Studies", "Tools").
    - Targeted "Thin Spot" takeover articles based on competitor gaps found via WordPress content audits.

## 3. Publication Frequency
The roadmap does not assume a fixed number of posts. It adapts to the user's configured **`publication_days`**:
- **1 Day/Week**: ~52 posts/year.
- **3 Days/Week**: ~156 posts/year.
- **5 Days/Week**: ~260 posts/year.

The 50/30/20 Funnel Rule remains the guiding principle for distribution regardless of frequency.
