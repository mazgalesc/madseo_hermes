# Pubblicare la repo e accettare i contributi

> La skill è pensata per essere **pubblica** e aperta ai contributi, con la documentazione **in italiano**
> (il mercato di riferimento è italiano). Questo file è la procedura per prepararla alla pubblicazione e
> per non pubblicare segreti — non sostituisce il `README.md`, che parla a chi legge il repository.

## 1. La scansione dei segreti (prima di ogni pubblicazione o push)

1. Si scansiona **l'insieme esatto dei file che entrerebbe nel commit**, non tutto il disco:

   ```bash
   { git ls-files; git ls-files --others --exclude-standard; } | sort -u
   ```

   Un segreto dentro un file **ignorato** non finisce nella repo: il problema sono solo i file di questo elenco.
2. Le forme da cercare: `sk-…`, `AIza…`, `ghp_…`, `github_pat_…`, `xox[baprs]-`, `eyJ…`,
   `-----BEGIN … PRIVATE KEY-----`, e le righe che nominano `password`/`api_key`/`secret`/`token`
   con un valore accanto.
3. **Il confronto col valore vero si fa con un parser, mai con la shell.** `set -a; . ~/.hermes/.env`
   **tronca il valore al primo spazio**: la credenziale di questo sito è `Basic <base64>` e diventa la
   parola «Basic», che poi combacia con qualsiasi testo contenga «Basic» — decine di falsi positivi che
   fanno credere a una fuga di credenziali. Si legge la riga, si tolgono le virgolette, e si cerca il
   **valore intero** più ogni sua parte lunga (≥16 caratteri). **Vale in ogni direzione**: le stesse
   credenziali servono poi per **chiamare** le API, e vanno passate a `curl` come argomenti letti da un
   parser — prese dal `source` della shell falliscono con un **401** che sembra una credenziale sbagliata
   invece di un troncamento.
4. **Non si stampa mai il valore**, né in chat né in un rapporto: si stampano conteggi e nomi di file,
   con il contesto mascherato.
5. `.gitignore` deve coprire `.env`, `*.env`, `secrets/`, `*.key`, `*.pem`, `*.p12`, `credentials*`,
   `*token*`, `*cookie*`, `*.db`, `*.sqlite`, `__pycache__/`, `.venv/`, `node_modules/`.

## 2. Cosa rendere generico (e come, senza rompere l'installazione)

Regola di fondo: **nel repository solo nomi generici** — dominio, percorsi assoluti, nomi dei server e dei
profili, namespace delle abilità, plugin e tema, nomi dei file di credenziali, identificativi delle
proprietà Analytics, nomi di persona. **I valori reali non spariscono: si spostano.**

1. **Si inventaria prima di toccare.** Per ogni variante (dominio, dominio senza punto, NomeProgetto,
nomeprogetto, nome_progetto, sigle, nomi utente) si contano occorrenze e file, e si scrive la mappa
`concreto → generico`. Senza inventario si sostituisce a metà.
2. **Si applica in ordine: prima i nomi composti, poi quelli semplici.** Il namespace `nome-sito/` e il file
`nome-wp.env` contengono il nome semplice: sostituendo prima quello, i composti si spezzano e la passata
successiva non li riconosce più.
3. **Si rilegge ogni riga cambiata.** Le sostituzioni guastano la grammatica intorno: preposizioni che
collidono con l'articolo del nome generico («di il sito», «brand il sito»), parole saldate («deluna» da
«della» + «una»), intestazioni e tabelle che perdono il soggetto, citazioni dentro i reference. Si cerca
con un grep di controllo delle sequenze impossibili: **il conteggio delle sostituzioni non è una verifica.**
4. **Il frontmatter si rilegge a parte.** `description` è il testo che fa scattare la skill: una
sostituzione meccanica la rende illeggibile e la skill smette di caricarsi per l'argomento giusto. `tags`
non deve contenere il nome del progetto e `homepage` non punta a un segnaposto.
5. **I valori reali vanno in un file di configurazione locale, fuori dalla repo** (nella cartella di
lavoro, non nell'albero della skill): lì sta la corrispondenza generico → reale, e `SKILL.md` punta a quel
file. Nel testo restano i segnaposto.
6. **Gli script leggono percorsi, dominio e identificativi dall'ambiente**, con un ripiego di esempio; il
valore vero sta nella configurazione locale. Un percorso scritto dentro lo script è un valore reale nel
repository, e sostituirlo con un segnaposto senza dargli una variabile lo fa smettere di funzionare.
7. **Un nome che cambia nel testo va cambiato anche sul disco** (database, cartelle). Attenzione: se lo
script apre un percorso inesistente, SQLite **crea un file vuoto** invece di fallire. Prima di rinominare si
controlla che la destinazione non esista già, e si verifica che la **tabella** ci sia (`sqlite_master`,
dimensione), non solo che il file esista. I file vuoti lasciati indietro si cancellano.
8. **La prova è il contenuto pubblicato, non l'albero locale.** Dopo il push si scaricano i blob dal remote
e si cercano lì le stringhe personali: `gh api repos/<owner>/<repo>/git/trees/main?recursive=1` per
l'elenco, poi `gh api repos/<owner>/<repo>/contents/<path> --jq .content | base64 -d` per il testo di ogni
file. **Un grep locale pulito non dice niente su quello che sta sul server.**
9. **Rinominare la skill** (quando il nome contiene il progetto) tocca tre cose: la cartella installata, il
campo `name:` del frontmatter e l'istantanea; poi si verifica che si carichi ancora (`hermes skills list`) e
si riallinea l'istantanea. La repo git dentro la cartella continua a funzionare: il remote non dipende dal
nome della cartella.
10. **Le dimensioni si misurano in byte, non in caratteri**: `wc -c`. Con l'italiano accentato i byte
superano i caratteri, quindi il tetto che la skill si dà si avvicina prima di quanto dica il conteggio a
caratteri.
11. **Una skill generica porta anche la procedura 0 (primo avvio)**: i passi che riconciliano i nomi
generici del testo con i valori reali (cartella di lavoro, database, credenziali, server, variabili
d'ambiente, prova finale), più il modello del file di configurazione locale. Chi la installa sa cosa
configurare e chi l'ha scritta non lascia valori nel repository: senza questa procedura i segnaposto
restano senza corrispondenza e la skill chiede cose che non esistono.

## 2-bis. La storia della repo: un albero pulito non è una storia pulita

Le sostituzioni ripuliscono **l'ultima versione**: le versioni precedenti restano nella storia, e chi clona
le vede tutte. Dopo aver reso generici i file si ricostruisce la storia.

1. **Si cerca in tutte le revisioni, senza distinguere maiuscole**: si clona la repo in una cartella
   temporanea e si lancia `git grep -I -i -l -E '<parola>' $(git rev-list --all)`. Un grep sul solo albero di
   lavoro non dice niente su quello che è pubblicato.
2. **Le varianti con le maiuscole sono la trappola**: una sostituzione fatta solo in minuscolo lascia dietro
   `NomeProgetto`, `NOMEPROGETTO`, `Nome_Progetto` e le sigle. Si inventariano **prima** tutte le forme, e la
   ricerca di controllo si fa **case-insensitive** — compresi i documenti in inglese, dove il nome del
   progetto può comparire in un titolo.
3. **Un commit solo**: `git checkout --orphan <ramo>`, `git add -A`, commit col messaggio della prima
   versione, poi `git branch -D main`, `git branch -m main`, `git push --force origin main`; in locale
   `git reflog expire --expire=now --all && git gc --prune=now` per togliere gli oggetti vecchi.
   **La ricostruzione non deve cambiare l'albero**: si confronta `git rev-parse HEAD^{tree}` prima e dopo —
   hash uguale significa che il commit unico contiene esattamente quello che c'era; se cambia, qualcosa è
   andato perso o aggiunto. Vale anche quando si **fondono più commit in uno** dopo la pubblicazione
   (`git reset --soft HEAD~1` + `git commit --amend`): la prova è di nuovo l'hash dell'albero.
   Dopo il force-push si rilegge il **contenuto dal clone**, non dall'albero locale: che le correzioni
   ci siano davvero (stringhe nuove presenti, vecchie assenti) e che l'elenco dei file sia quello atteso.
4. **GitHub conserva gli oggetti non più raggiungibili**: il force-push toglie i commit dai rami, non
   dall'archivio del server. L'unico modo garantito per azzerare è **cancellare e ricreare la repo** —
   `gh repo delete` richiede lo scope `delete_repo` (`gh auth refresh -h github.com -s delete_repo`, login
   interattivo: **lo fa l'autore**), oppure l'autore cancella dalla pagina GitHub. Poi si ricrea pubblica, si
   rimettono descrizione e argomenti e si spinge il commit unico (senza force: la repo è vuota).
5. **Il nome della repo, e il suo URL nei comandi di installazione, contengono il nome del progetto — ed è
   normale**: è la scelta dell'autore, non una fuga. Nel controllo finale quello si esclude e si guarda al
   resto: dominio vero, percorsi, identificativi, nomi di persona.

**La decisione resta dell'autore**: cosa rendere generico si propone e si applica solo con il suo ok. Una
riga di licenza col suo nome utente GitHub, per esempio, è una scelta sua.

## 3. Licenza

Senza licenza nessuno ha il diritto di riusare il codice e le PR diventano complicate. **MIT** è la scelta
che le rende semplici. Anche questa è una decisione dell'autore.

## 4. Il commit

- Messaggi **descrittivi e in italiano** (la storia di questa repo è in italiano): cosa cambia, in quali
  file, e il perché. Nessun trailer di attribuzione.
- Prima di committare: `git status --short`, il `diff --stat`, e la scansione del §1.
- **Le cancellazioni di file si dichiarano nel messaggio**: una `D` non spiegata sembra un errore.
- Un commit per unità di lavoro coerente. Il commit si fa **solo con l'ok dell'autore per quella singola azione**.
- La cartella della skill è una repo git a sé: non ha un remote finché non lo si crea, e la creazione
  (pubblica o privata) è una decisione sua.

## 5. Cosa deve contenere una PR (e cosa si chiede a chi contribuisce)

1. **Cosa cambia**, in **quale file**, e **il caso reale che l'ha dimostrato** (un articolo, una pagina,
   un errore trovato sul campo). Una regola senza il caso che l'ha generata invecchia male.
2. **Una regola per volta**, nella sezione che possiede già quell'argomento; se non esiste, si crea un
   reference nuovo **e si aggiunge alla mappa in `SKILL.md`** (un reference non citato è invisibile).
3. **Non generalizzare da un caso isolato**, e non introdurre strumenti a pagamento come necessari.
4. Se tocca gli script, va provato su un contenuto vero prima di proporlo.
5. Una modifica di metodo si discute prima in una **issue**: prima si discute, poi si scrive.

## 6. Manutenzione dopo la pubblicazione

Le due copie (installata + istantanea) e il curator restano come descritto in `SKILL.md`: si modifica
la copia **installata**, poi si rigenera l'istantanea. Se la repo diventa il riferimento pubblico,
l'istantanea sul Desktop resta comunque il posto delle versioni precedenti — **mai dentro l'albero della
skill**, che rompe il caricamento per nome.
