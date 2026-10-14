# Ricerca: webcmd, SERP vera, Quora e community

> *Estratto da `SKILL.md` il 24/09/2026 per dimensione, contenuto invariato; le intestazioni sono state aggiunte per rendere il file navigabile.*

## Il giro di ricerca: la SERP vera, Quora e le community

### Il giro di ricerca con webcmd — SERP Google vera e Quora (verificato il 24/09/2026)

La ricerca di un articolo **non si ferma ai motori di `web_search`**: quelli restituiscono una SERP
simile, non quella di Google. La SERP vera (italiana, con il profilo `sito` dell'autore) si legge con
`webcmd`, ed è la fonte da usare per i passi «concorrenza» e «vuoti da riempire».

### Verifica dell'ambiente

**Verifica dell'ambiente** (sola lettura, si fa quando qualcosa non torna):
```bash
webcmd doctor            # daemon, runtime Cloak, connettività
webcmd profile list      # profili: `default` e `sito` (quest'ultimo è quello con gli accessi)
```
Il `sito` risulta «not connected» finché non si apre una sessione: è normale, non è scollegato.

### Verificare gli accessi: prima i cookie, poi la pagina

**Un profilo ricreato non è una sessione scaduta.** Reinstallando webcmd il profilo `sito` viene
ricreato **vuoto**: gli accessi non scadono, spariscono. La prima sonda non è una pagina ma il **conteggio
dei cookie**, che è un file SQLite:
```bash
cp ~/.webcmd/cloak/profiles/sito/Default/Cookies "$TMPDIR/c.db"
sqlite3 "$TMPDIR/c.db" "select count(*) from cookies;"
sqlite3 "$TMPDIR/c.db" "select host_key, count(*) from cookies group by host_key;"
du -sh ~/.webcmd/cloak/profiles/sito
```
Zero cookie (o solo i pochi tecnici) = **nessun accesso nel profilo**, e inutile cercare la causa nel
sito. Un profilo con gli accessi dentro pesa **decine di MB**; **9-10 MB è un profilo appena creato**.

La controprova dal vivo dice lo stesso in un colpo, una pagina per sito: Google risponde con la pagina
anti-bot `/sorry/index` («traffico insolito»: senza accesso non si legge la SERP vera), Reddit «Prove your
humanity», LinkedIn rimbalza a `/login/`, Quora alla registrazione, X al flusso di login. **Il captcha di
Google non si aggira: si risolve rifacendo l'accesso.**

### Verificare che gli accessi abbiano retto, sito per sito

Fatto l'accesso, la controprova è **un solo `browser run`** che visita i cinque siti e legge un marcatore per
ciascuno. I marcatori che valgono:

| Sito | Dove guardare | Accesso fatto |
|---|---|---|
| Google | `google.com/search?q=…&hl=it&gl=it` | l'URL **non** finisce su `/sorry/index`, il blocco «Overview dell'AI» c'è, in testa c'è l'avatar dell'account (`a[href*="SignOutOptions"]`) |
| Reddit | `reddit.com` | menu utente, «Create post», i feed For You / Following |
| Quora IT | `it.quora.com` | Home, Rispondi, Notifiche, «Aggiungi domanda» |
| LinkedIn | `linkedin.com/feed/` | l'URL **resta** `/feed/` e il feed si disegna |
| X | `x.com/home` | `[data-testid="SideNav_AccountSwitcher_Button"]` e la timeline |

**Su LinkedIn non fidarsi del selettore di profilo**: `.global-nav__me` e
`[data-testid="nav-settings__dropdown-trigger"]` possono rispondere `false` **anche da loggati** — il segnale
valido è che l'URL non rimbalzi su `/login/` e che il feed abbia contenuto. Un `false` lì non è una prova di
accesso mancante, e dichiararlo tale mandall'autore a rifare un accesso che c'è già.

I cookie stanno su disco (il profilo con gli accessi dentro pesa centinaia di MB), quindi la verifica può
girare **anche in una sessione nuova**; se il conteggio dei cookie è a zero la verifica non serve — è il
profilo ricreato, non la sessione.

### Aprire la finestra degli accessi per l'autore

Gli accessi li fall'autore a mano: quello che serve è **aprirgli le pagine giuste e lasciarle aperte**, una
scheda per sito con `context.newPage()`, in una sessione dedicata che **non si chiude**:
```js
const urls = [
  'https://accounts.google.com/ServiceLogin?hl=it&continue=https%3A%2F%2Fwww.google.com%2F',
  'https://www.reddit.com/login/',
  'https://it.quora.com/',
  'https://www.linkedin.com/login',
  'https://x.com/i/flow/login',
];
const aperti = [];
for (const u of urls) {
  const p = await context.newPage();
  await p.goto(u, { waitUntil: 'domcontentloaded', timeout: 45000 }).catch(function () {});
  let t = '';
  try { t = await p.title(); } catch (e) { t = ''; }
  aperti.push({ sito: u, titolo: String(t).slice(0, 80) });
}
try { print(JSON.stringify(aperti, null, 1)); } catch (e) { console.log(JSON.stringify(aperti, null, 1)); }
```
`session create "accessi-sito"` → `browser run --file <programma>` → `browser tabs` per confermare che
le schede ci siano. Poi **portare la finestra davanti**, altrimenti l'autore non la trova:
`osascript -e 'tell application "System Events" to set frontmost of process "Chromium" to true'`.
Il browser di webcmd **non è headless** (nessun `--headless` nel processo Chromium): la finestra si vede
davvero sul Mac e l'autore ci lavora dentro. Facebook non si apre: bug dello strumento, l'accesso non serve.

### Il 401 che non vuol dire «credenziali sbagliate»

**I file delle credenziali non si leggono con `source`.** In `~/.hermes/.env` e in
`~/.hermes/secrets/wp-credentials.env` i valori sono **senza virgolette** e **contengono spazi**
(`WP_BASIC_AUTH` = `Basic <base64>`; una application password di WordPress è fatta di gruppi di
quattro caratteri separati da spazi): `source file` tronca il valore al primo spazio e `curl` risponde
**401** su un accesso che funziona. Si leggono con un parser vero (`line.split('=', 1)`, `strip()`, via le
virgolette) e si passano a `curl` come argomenti di lista, non dentro una stringa di shell.

**Sull'endpoint MCP, 401 e 405 dicono cose diverse**: `401` = non autenticato, `405` = credenziali
accettate ma metodo sbagliato per l'handshake MCP. E il test che conta **non è `curl` ma la chiamata dello
strumento**: `mcp-adapter-discover-abilities` che risponde con l'elenco delle abilità è la prova che
l'MCP `sito` è autenticato e configurato.

### La sessione: sequenza che funziona

**Sequenza che funziona** (una sessione per ricerca, poi si chiude):
```bash
webcmd --profile sito session create "ricerca-<articolo>" -f json      # → {"id": "ricerca-...-xx"}
webcmd --profile sito --session <id> browser run --timeout 120 --no-snapshot-diff --stdin < programma.js
webcmd --profile sito session close <id>
```
**Il nome dato a `session create` non è il selettore.** `browser run` senza `--session` risponde
`SESSION_REQUIRED`; passandogli il nome invece dell'id risponde `INVALID_SESSION_SELECTOR`. Si usa
**l'id restituito** (`ricerca-jw`), non la parola passata a `session create` (`ricerca`): è la prima cosa da
leggere nella risposta del comando. La sessione resta viva fra una chiamata e l'altra — si crea una volta e
si riusa, non una per `run`.

### Il programma per la SERP Google

**Programma per la SERP Google** (il codice gira fuori dalla pagina: serve `page.evaluate`):
```js
await page.goto('https://www.google.com/search?q=<query>&hl=it&gl=it', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(3000);
const out = await page.evaluate(() => {
  const risultati = [];
  document.querySelectorAll('#search a h3').forEach(h => risultati.push(h.innerText.trim()));
  const corpo = (document.querySelector('#search') || document.body).innerText.replace(/\s+/g, ' ');
  return { titolo: document.title, risultati: risultati.slice(0, 12), corpo: corpo.slice(0, 8000) };
});
try { print(JSON.stringify(out, null, 1)); } catch (e) { console.log(JSON.stringify(out, null, 1)); }
```
Il risultato arriva **in `result`** quando il programma **fa `return`** di una stringa, e in
`logs[0].args[0]` quando usa `print`/`console.log`: **si leggono tutti e due**, non si dà per scontato che
`result` sia vuoto — entrambe le forme sono state osservate funzionare. Se il programma fa `return`, il
valore è una **stringa JSON** da rileggere con `json.loads`. Il blocco `try/catch` serve quando si usa
`print`: non è sempre definito, `console.log` sì.

### Cosa si ricava da una SERP e cosa no

**Cosa si ricava e cosa no** (verificato su `wordpress vs wix`, 24/09/2026):
- **risultati organici con la data** (es. Kinsta «14 mar 2025», Supporthost «26 mag 2022»): la data dice
  subito quanto è vecchio il contenuto che sta davanti — è l'aggancio per la freschezza;
- **thread Reddit in prima pagina** (su quella query ne comparivano due, 50+ e 30+ commenti): sono
  concorrenza, non solo fonte di domande;
- **blocco sponsorizzato** («Spostato»/`Risultato Sponsorizzato`): dice chi paga su quella query —
  segnale di valore commerciale;
- **le pastiglie di raffinamento sotto la barra di ricerca** («Word gratis», «WhatsApp», «iPhone», «Lavoro»,
  «Online»…): sono la coda lunga **vera** di quella query, scritta con le parole del pubblico e non dedotta
  dai suggerimenti. Si leggono insieme ai risultati e finiscono dritte nel passo delle keyword;
- **la forma dei primi dieci decide se l'articolo può posizionarsi** (regola in `parole-chiave.md` §2: il
  contenuto deve avere la stessa forma di chi sta in prima pagina). Qui serve solo il **come si legge**: si
  guardano i titoli e i domini — titoli «gratis/online/illimitato/App» con domini di servizi e assistenza =
  intento transazionale, e una guida «come si fa» non si posiziona; titoli «come/guida/confronto» = intento
  informativo o commerciale, e l'articolo ha spazio. È il controllo che evita di scrivere un pezzo per una
  query che nessun articolo vincerà mai;
- **La SERP dei motori di `web_search` NON è la prima pagina di Google** (verificato il 24/09/2026, articolo 207): per la stessa query in italiano `web_search` restituisce guide in inglese (smartwp, kinsta, hostinger, wpbeginner), mentre la SERP vera di Google è **in italiano** e porta in prima pagina due thread Reddit e uno sponsorizzato locale. Non dedurre mai «la SERP è tutta in inglese» da `web_search`: per i passi 4 e 5 vale **solo** la SERP letta con webcmd, `web_search` resta la seconda opinione.
- **Per Reddit la search di webcmd non serve**: su query WordPress restituisce rumore (thread di sport e cronaca). Per Reddit usare `reddit.py` sui feed pubblici, come da skill.
- **`Le persone chiedono` NON è estraibile con i selettori vecchi** (`div[jsname="yEVEwb"]`,
  `div.related-question-pair`): su questa resa non restituisce nulla. **Ma il blocco può essere leggibile
  nel testo della pagina**: il 24/09/2026 sull'articolo 209 le quattro domande comparivano dentro `corpo`
  (dopo i primi risultati organici, precedute da «Le persone hanno chiesto anche»). Quindi: cercarle prima
  in `corpo`, e **se non ci sono** dichiarare che non sono state estratte — non che il blocco non esiste.
  **La resa migliore le restituisce tutte e quattro**: il 24/09/2026 sul **1441** le «Persone hanno chiesto
  anche» **sono uscite su entrambe le SERP, quattro domande ciascuna**. Quindi: tentare sempre, e
  **registrare il numero di domande estratte** — sono il bersaglio AEO più concreto che si ottenga da una SERP.
- **Le domande del blocco «Le persone hanno chiesto anche» sono il bersaglio AEO più diretto**: se una FAQ
  dell'articolo coincide con una di quelle domande la copertura è giusta; se una resta scoperta è il primo
  contenuto da aggiungere (verificato sul 209: coincidevano tre domande su cinque FAQ).

### Il programma per Quora italiano

**Programma per Quora italiano**: stesso schema su
`https://it.quora.com/search?q=<query>`, estrarre con `document.body.innerText` (i selettori di classe
non sono affidabili): si ottengono domande e risposte reali con autore e ruolo.

### Il programma per Reddit

**Programma per Reddit** (search via webcmd, profilo sito):
```js
await page.goto('https://www.reddit.com/search/?q=<query>&sort=comments', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(4000);
const out = await page.evaluate(() => {
  const trovati = [];
  document.querySelectorAll('a[href*="/comments/"]').forEach(a => {
    const t = (a.innerText || '').trim().replace(/\s+/g, ' ');
    if (t.length > 15 && t.length < 170 && !trovati.some(x => x.titolo === t))
      trovati.push({ titolo: t, url: a.href.split('?')[0] });
  });
  return trovati.slice(0, 8);
});
try { print(JSON.stringify(out, null, 1)); } catch(e) { console.log(JSON.stringify(out, null, 1)); }
```
Risultato: array di `{titolo, url}` — i titoli dei thread pertinenti.
Nota: la search di Reddit tramite webcmd può restituire rumore (thread non pertinents)
se la query non è abbastanza specifica. Usare query in inglese o frammenti chiari.

### Il programma per X

**Programma per X (Twitter)**:
```js
await page.goto('https://x.com/search?q=<query>&src=typed_query&f=top', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(5000);
const out = await page.evaluate(() => {
  const loggato = !!document.querySelector('[data-testid="SideNav_AccountSwitcher_Button"]');
  const tweet = [];
  document.querySelectorAll('article[data-testid="tweet"]').forEach(t => {
    const testo = (t.innerText || '').replace(/\s+/g, ' ').trim();
    if (testo.length > 30) tweet.push(testo.slice(0, 300));
  });
  return { loggato, tweet: tweet.slice(0, 6), url: location.href };
});
try { print(JSON.stringify(out, null, 1)); } catch(e) { console.log(JSON.stringify(out, null, 1)); }
```
Risultato: `{loggato, tweet[], url}` — utile per vedere cosa si dice in tempo reale sull'argomento.

### Il programma per LinkedIn

**Programma per LinkedIn**:
```js
await page.goto('https://www.linkedin.com/search/results/content/?keywords=<query>', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(5000);
const out = await page.evaluate(() => {
  const corpo = (document.body.innerText || '').replace(/\s+/g, ' ');
  return { url: location.href, primi_1500: corpo.slice(0, 1500) };
});
try { print(JSON.stringify(out, null, 1)); } catch(e) { console.log(JSON.stringify(out, null, 1)); }
```
LinkedIn ha caricamento dinamico: l'estrazione è limitata. Utile come conferma veloce, non per
analisi dettagliata. Chiudere dopo una singola pagina.

### Sola lettura: la regola dell'autore

**Regola dell'autore, invariata:** sola lettura. Niente post, commenti, voti, messaggi, iscrizioni. Poche
pagine per sessione, chiudere le sessioni inattive, e niente ricerche in massa su LinkedIn e X.

### Il passo «volumi di ricerca»: si chiude con Search Console

**Il passo «volumi di ricerca» si chiude con Search Console (dal 24/09/2026).** Nei rapporti il passo 3
dichiara «volumi non disponibili» (nessuno strumento a chiave): non è più un buco, **Search Console via
Maton** dà i numeri veri del sito e dice subito se la query dell'articolo ha domanda. Due chiamate:
`dimensions: ["page"]` (impression, clic, posizione media per pagina, da confrontare con le altre pagine
del sito) e `dimensions: ["page","query"]` (le query che portano davvero impression: Google omette
quelle a volume troppo basso). Misurato sull'articolo 207: **3 impression e 1 clic in 28 giorni** contro
le 29 impression della pagina hosting → «domanda debole» **dimostrata**, non dichiarata. Un articolo con
posizione media buona (6,3) e volumi inesistenti non è penalizzato: nessuno cerca quella formulazione.
In quel caso la raccomandazione è **allargare la query** (famiglia più cercata), non riscrivere il pezzo.

### Suggerimenti pieni di marche: il pezzo generico è un hub

**Quando i suggerimenti sono pieni di nomi di marca, il pezzo generico è un hub, non un articolo.**
Verificato il 24/09/2026 sull'articolo 221 («come funziona l'affiliazione»): **13 query su 21** contengono il
nome di un programma (Amazon, Shein, Temu, Booking, TikTok Shop, Zalando, Twitch, Yves Rocher) e l'articolo
non ne nomina **nessuno**. Le query con la marca sono vinte **dalla marca stessa** (su «affiliazione amazon
come funziona» la prima posizione è la pagina ufficiale di Amazon con i sitelinks). Quindi la
raccomandazione non è «aggiungere una classifica» ma: **una sezione «e per le marche?» con una riga per
ognuna e il link al caso specifico**, e la segnalazione dei **casi specifici che mancano** come contenuti da
scrivere (sul 221: Shein e Temu, 13 query insieme fra 219 e 221, zero copertura). La pagina generica vale
come perno del silo, non come pagina di traffico.

### HowTo: i modelli del sito e i tre pattern

**Il HowTo perfetto esiste: passi dello schema = H2 visibili, parola per parola.** Sull'articolo 221 i sei
passi dello schema corrispondono **sei su sei** agli H2 `Passo 1…Passo 6` della pagina. È il riferimento da
imitare quando si scrive uno schema HowTo nuovo: **prendere i nomi dei passi dal testo che si vede**, non
inventarli. E il controllo si fa esattamente così — estrarre i `name` dentro il blocco `HowTo` del JSON-LD
e confrontarli con gli H2 visibili.

**I modelli perfetti sono cinque, e i pattern sono tre.** **passi = H2 visibili** → il **221** (`Passo 1…Passo 6`,
sei su sei). **passi = H3 visibili** → **1441** (`I dieci controlli, in sequenza`), **1412** (`I dieci controlli,
in pratica`) e **1452** (`Il metodo in dieci passi`), dieci su dieci. **passi = voci di un elenco numerato
visibile** → **1529** (`L'implementazione in dieci passi`): è **il pattern più frequente e il più utile**,
perché gli articoli che finiscono con «i sette passi», «la checklist», «il piano in N mosse» **scrivono la
procedura come elenco, non come titoli** — basta che i `name` dello schema siano le voci di quell'elenco. Il
controllo va fatto **sul contenuto che si vede**, e il pattern da copiare dipende da come è scritta la
procedura: H2 se sono sezioni, H3 se sono voci di un elenco lungo, **voci di `<ol>` se sono un elenco numerato**.

### Un difetto trovato: controlla se una pagina più recente lo ha già corretto

**Quando si trova un difetto di contenuto, controllare se un articolo più recente contiene già la correzione.**
Il 24/09/2026 il **684** (12 set) prometteva ancora che Google mostra le FAQ come sezione espandibile e gli
HowTo come carosello; **il 1529 (23 set), undici giorni dopo, spiega che non è più vero**. **La versione
corretta era già in casa**: nei casi così, l'azione non è riscrivere — è **allineare la pagina vecchia a quella
nuova** (e linkarle nei due sensi). Prima di proporre una riscrittura, cercare il tema nei contenuti pubblicati
più recenti.

### Le parole del pubblico assenti dal testo

**Una parola del pubblico che non compare nel testo è un difetto anche quando il contenuto c'è.** Il 1412
spiega benissimo come si annida una voce di menu, ma lo chiama `sottomenu` (11 volte) mentre **cinque query su
otto** e **tutti i titoli in prima pagina** dicono *menu a tendina* (il 1412 lo scrive **2 volte, per caso**) o
*menu a discesa* (0 volte). Il controllo da fare non è «l'argomento è coperto?» ma **«con quali parole lo dice
il pubblico?»**: si prendono le parole delle query e dei titoli in SERP e **si contano nel testo**. Se sono a
zero, la correzione non richiede contenuto nuovo — un H3 con il sinonimo fra parentesi, la parola nei passi, e
il sinonimo nel titolo o nella description. È il rapporto costo/rendimento più alto che esista.

### Procedure visibili senza HowTo

**Il difetto opposto — la procedura visibile senza HowTo — si presenta a grappoli, quindi va cercato su
ogni articolo.** Sulla stessa verifica, **225, 226 e 227 hanno tutti e tre un capitolo finale con la
procedura numerata visibile** («il metodo in 7 passi», «il tuo piano in 5 mosse», «il piano d'azione in 8
mosse») **e nessuno schema HowTo**, mentre il 221 ce l'ha. Il controllo è una riga (`grep HowTo` nei blocchi
JSON-LD publici) e va fatto sempre: una procedura visibile senza HowTo è un'occasione persa che guardando la
pagina non si nota. Il modello da riusare è il 221.

### I sinonimi si verificano uno per uno

**I sinonimi si verificano uno per uno: il termine scelto dall'articolo non è sempre quello che la gente
digita.** Quando un concetto ha più nomi in circolazione, ripetere la chiamata ai suggerimenti su **ogni**
termine e confrontare. Verificato il 24/09/2026 sull'articolo 220 («IA generativa vs IA **analitica**»):
`ia analitica` dà 15 suggerimenti **pieni di rumore** (geometria analitica, chimica analitica, esami del
sangue, spagnolo), `ia predittiva` ne dà 13 **tutti pertinenti** («differenza tra ia predittiva e
generativa» esiste tale e quale) e `ia agentica` 15, il confronto nuovo. Nel testo: **«analitic» 42 volte,
«predittiv» zero**. Il rimedio non è riscrivere: è **aggiungere i sinonimi** (titolo, description, un inciso
in apertura) senza cambiare la voce di glossario. Controllare sempre anche il conteggio delle parole nel
testo: se il termine più cercato ha zero occorrenze, quello è il dato.

### Il primo run di una sessione può fallire

**Il primo `browser run` di una sessione webcmd nuova può fallire.** Sintomo: `runtime_command_failed:
Timed out waiting for Cloak target` e file di output da ~240 byte. Non è la pagina: è il runtime. Verificato
più volte il 24/09/2026 (articoli 216, 217, 219, 220). **Rimedio: ripetere il programma in una sessione
nuova** — alla seconda passa. Conviene aprire la sessione, lanciare subito il primo `run` e non allarmarsi
se fallisce una volta.

### Zero suggerimenti: serve la controprova

**Zero suggerimenti non è un dato: va verificato con una controprova.** Se un seme non restituisce nulla,
ripetere la chiamata su **due semi di controllo** che si sa funzionare (`wordpress`, `affiliazione`): se i
controlli tornano 15 e il seme zero, allora **la frase non esiste nell'autocomplete** — ed è una scoperta,
non un errore. Verificato il 24/09/2026 sull'articolo 219: `blog di affiliazione` (la frase del titolo e dello
slug) dà **0**, mentre `wordpress` e `affiliazione` danno 15 ciascuno. In quel caso la domanda va mappata con
**semi più larghi** (`aprire un blog`, `affiliazione amazon`, i nomi delle piattaforme): sul 219 sono uscite
60 query, con `affiliazione amazon` a 15 varianti e — sorpresa — **Shein (7) e Temu (6)**, due piattaforme
che l'articolo non nominava affatto. Regola: quando la frase dell'articolo non ha autocomplete, il
riposizionamento va proposto **sulla frase che la gente digita davvero**, non su quella che si è scelta.

### Pochi suggerimenti: cambia l'obiettivo dell'articolo

**Quando i suggerimenti sono pochissimi, cambia l'obiettivo dell'ottimizzazione.** Verificato il 24/09/2026
sull'articolo 218 («differenza tra articoli e pagine wordpress»): **3 query in tutto**, due semi a zero.
Non è una query «senza domanda»: è una query **tecnica e precisa**, dove chi cerca scrive la domanda intera
perché sa già cosa vuole sapere. Lì non si vince con il taglio «testato» né con la freschezza — si vince con
la **completezza delle domande derivate**, cioè le voci del blocco «Le persone hanno chiesto anche» e i dubbi
operativi che restano dopo la lettura. Quindi: raccogliere i suggerimenti, **poi incrociarli con il blocco
delle domande di Google**, che su queste query è la vera lista dei capitoli mancanti.

### La domanda vera è quasi sempre un sintomo

**E se la frase dell'articolo parla di «errori», la domanda vera è quasi sempre un SINTOMO.** Verificato due
volte il 24/09/2026: «errori seo wordpress» e «errori hosting wordpress» danno **zero** suggerimenti, e i semi vicini non mostrano nessuna domanda di «errori». Il pubblico **non sa di avere un errore: descrive quello
che vede** — e cercando i semi del sintomo si trova la domanda vera. Le tre specificazioni da provare sempre:
(a) **l'aggettivo dell'utente** (`lentissimo`, `molto lento`, `estremamente lento`); (b) **il contesto**
(`wordpress lento admin`, `elementor lento`, `+ elementor + woocommerce`, `lento su mobile`); (c) **il nome
del provider** (`sito wordpress lento su aruba`, `wordpress lento hostgator`, `errore 500 wordpress aruba`) —
chi ha il problema dice su quale hosting ce l'ha. Sul 223 l'articolo usa «lentezza» **2 volte** mentre
`wordpress lento` + `sito lento` valgono **30 query**, e non nomina nessun provider. La raccomandazione è
sempre la stessa: **non riscrivere, portare le parole del lettore** (titolo, description, un H2, la matrice
sintomo → causa → verifica) accanto a quelle del tecnico.

### Screenshot o infografiche

**Sulle guide «dove sta cosa» gli screenshot battono le infografiche.** L'articolo 218 ha 7 immagini
(una ogni ~350 parole, la densità più alta del sito) e quattro sono **schermate dell'interfaccia** (liste,
homepage, menu, impostazioni di lettura): per spiegare *dove* si clicca valgono più di qualunque diagramma.
Un'infografica che ripete le frasi dell'articolo non aggiunge niente; uno screenshot sì.

### Due segnali da non lasciar passare nei suggerimenti

**Lettura dei suggerimenti: due segnali da non lasciar passare.** Se nelle query compare **`pdf`**
(verificato il 24/09/2026 sull'articolo 216: quattro varianti di «guida wordpress … pdf»), l'intento non è
leggere: è **scaricare e portarsi via** il contenuto — e in prima pagina chi lo cerca trova libri su Amazon.
È il caso in cui la pagina può distinguersi offrendo davvero una versione scaricabile. Se compare
**`in locale`** o nomi di strumenti che l'articolo non cita (Elementor sull'articolo 216, per due query
reali), quello è il capitolo mancante, non un dettaglio.

### Quando si usa cosa, in breve

**Quando si usa cosa, in breve:** `webcmd` (Google, Quora, LinkedIn, X) per la SERP vera e le
community; `reddit.py` per Reddit (la search di webcmd lì restituisce rumore); `web_search` come seconda
opinione; `web_extract` per leggere una pagina specifica.
