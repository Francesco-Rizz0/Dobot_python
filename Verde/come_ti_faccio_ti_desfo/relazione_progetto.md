# Relazione tecnica di progetto: robotica FSL
Automazione ciclica e integrazione multimediale con Dobot Magician Lite tramite Python



## 1. Obiettivo del progetto
L'obiettivo del progetto è la realizzazione di un sistema di automazione industriale simulato attraverso il braccio robotico **Dobot Magician Lite**. Il software esegue una routine ciclica di manipolazione e pallettizzazione di oggetti (Pick and Place) strutturata su coordinate cartesiane Point-To-Point (PTP). Al fine di arricchire l'interazione uomo-macchina, la routine cinematica è stata sincronizzata in tempo reale con tracce audio e riproduzioni multimediali gestite tramite script.



## 2. Architettura hardware e ambiente di sviluppo
L'architettura di sistema prevede il controllo diretto del braccio robotico da parte della stazione host mediante interfaccia seriale.

* **Hardware:** Braccio robotico Dobot Magician Lite provvisto di attuatore terminale a ventosa.
* **IDE di sviluppo:** Visual Studio Code (VS Code).
* **Linguaggio di programmazione:** Python 3.8.

### Nota sulla compatibilità del software
> [!IMPORTANT]
> **Criticità riscontrata:** Nelle fasi iniziali di sviluppo, le versioni più recenti dell'interprete Python hanno mostrato incompatibilità con i moduli di collegamento ed esecuzione di DobotLink.
> 
> **Soluzione:** L'ambiente è stato configurato sulla versione **Python 3.8**, che garantisce la stabilità operativa dei moduli didattici e l'interfacciamento corretto con il firmware.

Le librerie integrate nell'applicazione sono:
* `DobotEDU (m_lite)`: Libreria proprietaria per il controllo cinematico degli assi e dell'attuatore pneumatico.
* `pygame (mixer)`: Sottosistema multimediale ottimizzato per il caricamento e lo streaming asincrono di tracce audio (MP3).



## 3. Logica operativa e sequenza cinematica
Il programma adotta un approccio procedurale guidato dall'input dell'operatore, articolandosi nelle seguenti fasi:

1. **Configurazione iniziale:** Inizializzazione della porta seriale `COM4` e calibrazione della velocità assi al 100%.
2. **Interfaccia di scelta:** L'utente seleziona tramite terminale la traccia musicale di sottofondo e l'effetto sonoro finale da riprodurre.
3. **Routine di pallettizzazione ciclica:** Un sistema di tre cicli nidificati calcola dinamicamente le coordinate geometriche per prelevare gli oggetti disposti in griglia e depositarli in una struttura a pila, modificando progressivamente le coordinate $X, Y, Z$.
4. **Fase finale:** Riposizionamento del robot nelle coordinate di sicurezza, arresto della musica di sottofondo e riproduzione dell'effetto sonoro di conclusione selezionato.



## 4. Tabella dei parametri operativi e geometrie

| Parametro / asse | Valore iniziale | Modifica per ciclo | Scopo operativo |
| :---: | :---: | :---: | :---: |
| **Porta seriale** | `COM4` | Costante | Canale di comunicazione seriale |
| **Coordinata X** | $253\text{ mm}$ | $+20\text{ mm}$ per ciclo esterno | Avanzamento fila di prelievo |
| **Coordinata Y** | $151\text{ mm}$ / $-88\text{ mm}$ | $-20\text{ mm}$ per ciclo interno | Spostamento laterale di prelievo |
| **Coordinata Z** | $-44\text{ mm}$ | $+10\text{ mm}$ per deposito | Incremento altezza della pila |
| **Velocità standard** | $100\%$ | Costante | Esecuzione rapida dei cicli di lavoro |



## 5. Conclusioni
Il progetto ha permesso di analizzare le problematiche di posizionamento spaziale assoluto e relativo tramite i comandi PTP della libreria `m_lite`. L'integrazione del motore audio di `pygame` dimostra la versatilità di Python nell'unire l'automazione industriale a componenti software di terze parti, garantendo la precisione dei cicli di lavoro e la corretta gestione delle eccezioni hardware.
