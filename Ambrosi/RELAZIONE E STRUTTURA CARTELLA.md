## 📂 Struttura del Progetto

Il codice e la documentazione del workspace sono organizzati come segue:
* **`FINALS/`**: Contiene i programmi definitivi, ottimizzati e perfettamente stabili.
  * `movement_gui.py`: Pannello HMI di controllo manuale e diagnostica universale.
  * `production.py`: Isola robotica autonoma di smistamento ad anello chiuso con visione artificiale.
* **`BETAS/`**: Raccoglie gli script intermedi, i prototipi parzialmente funzionanti e i test di sviluppo privi delle ottimizzazioni di concorrenza e sicurezza hardware.
* **`dobot.zip`**: File di configurazione, librerie di basso livello ed esempi caricati nell'ambiente di sviluppo per istruire il sistema nell'utilizzo nativo delle API della libreria `DobotEDU`.
* **`DOCUMENTATION.md`**: È la suite software completa in Python usata per connettere, comandare e automatizzare in totale sicurezza sia il modello Magician che la versione Lite.

---

# 📑 RELAZIONE TECNICA

## 🛠️ STRUMENTAZIONE UTILIZZATA

Per la realizzazione dell'architettura hardware-software integrata sono stati impiegati i seguenti componenti:
* **Braccio Robotico Antropomorfo**: Dobot Magician.
* **Effettore di Estremità (End-Effector)**: Ventosa alimentata dal compressore interno del robot.
* **Nastro Trasportatore (Conveyor Belt)**.
* **Sensore di Prossimità**: Sensore digitale a infrarossi (IR) per intercettare il passaggio degli oggetti sul nastro.
* **Periferica di Input Video**: Videocamera/Webcam USB calibrata per l'acquisizione dei frame in tempo reale.
* **Rotaia (Linear Rail)**: Asse di scorrimento supplementare (Asse L) controllato direttamente dal firmware del robot per estendere l'area di lavoro spaziale.
* **Materiale di Lavorazione**: Cubetti industriali colorati calibrati (Rosso, Verde, Blu e Gialli).

---

## 📚 LIBRERIE UTILIZZATE

Il progetto è stato sviluppato interamente in Python, integrando librerie della dotazione standard e moduli specializzati di terze parti per la manipolazione hardware e l'analisi d'immagine:

* **`DobotEDU`**: È la libreria ufficiale del robot che usiamo per fargli fare tutti i movimenti, attivare la ventosa e gestire il nastro o la rotaia.
* **`OpenCV (cv2)`**: Serve per controllare la telecamera, isolare i colori con i filtri e capire quale sia quello dominante contando i pixel.
* **`Tkinter` e `TTK`**: Le abbiamo usate per disegnare tutta la parte visiva dell'interfaccia (come le finestre, i pulsanti e le barre di scorrimento).
* **`Multiprocessing`**: È fondamentale per far girare il robot e la telecamera in parallelo, evitando così che il programma si blocchi o vada a scatti.
* **`NumPy`**: Serve a gestire i dati delle immagini e a creare i filtri matematici per pulire i difetti e i disturbi nel riconoscimento dei colori.
* **`OS` e `Time`**: Ci servono per far avviare all'istante la telecamera senza attese e per gestire il timer dei 20 secondi prima di spegnere il nastro.

---

## 🎯 OBIETTIVI DEL PROGETTO

L'attività ha portato al raggiungimento di due macro-obiettivi, sviluppati in due moduli software indipendenti:
1. **Smistamento Automatico ("Magazzino")**: Creazione di un ciclo continuo autonomo in grado di movimentare il nastro trasportatore, arrestarlo al rilevamento di un pezzo, identificarne il colore e stoccarlo in pile in base al colore.
2. **Interfaccia Grafica di Controllo (HMI / "GUI di Movimento")**: Sviluppo di una GUI capace di pilotare manualmente ogni singolo asse del robot, la velocità dei motori, lo stato degli attuatori pneumatici, l'inversione di marcia del nastro trasportatore e il posizionamento sulla rotaia.

---

## ⚙️ PROCEDIMENTI E ARCHITETTURA SOFTWARE

### 1) SMISTAMENTO AUTOMATICO (Modulo `production.py`)

L'architettura del "Magazzino Automatico" è strutturata come una macchina a stati finiti deterministica guidata dagli eventi dei sensori esterni e dall'analisi d'immagine. 
Per attuare questo primo progetto abbiamo collegato un sensore, una telecamera, un nastro trasportatore e la suction cup al dobot magician.
Una volta messi sopra al nastro dei cubetti colorati si fa partire il programma, questo fa partire il nastro fino a che il sensore non rileva un cubetto e ferma il nastro.
Successivamente il robot preleva il cubetto, lo porta davanti alla telecamera che tramite un IA della libreria opencv per riconoscerne il colore.
In base a quello lo mette nella pila rossa, verde blu o quella degli "scarti" (i cubetti gialli).
Il programma poi continua alla ricezione del sensore di un altro cubetto, altrimenti si ferma da solo dopo non aver rilevato cubetti per 20 secondi.

### 2) INTERFACCIA GRAFICA UNIVERSALE (Modulo `movement_gui.py`)

Il progetto è iniziato per creare una gui per usare il robot tramite un joystick, tuttavia si muoveva solo su un piano, per questo abbiamo rivisto i comandi per muoverlo in ogni direzione, asse z compreso, rendendo la gui simile a dobot lab anche se poi optato per una più user friendly ed aggiunto uno slider per la velocità del robot.
Successivamente abbiamo aggiunto 2 pulsanti per attivare e disattivare la suction cup, ed insieme a questo abbiamo introdotto uno slider che permette di muovere il nastro trasportatore avanti/indietro in base alla velocità dello slider (esempio velocità 100 verso destra o velocità 800 verso sinistra).
Arrivati a questo risultato abbiamo posizionato il robot sopra alla rotaia ed introdotto un ulteriore slider che muove la rotaia posizionando il robot nell'equivalente posizione dell'indicatore dello slider, ed aggiunto un altro slider per la sua velocità.
Abbiamo aggiunto anche dei pulsanti HOME per riportare la rotaia ed il robot nella loro posizione di home, una finestra che mostra le sue coordinate ed un controllo per riconoscere se il robot collegato sia un dobot magician o dobot lite.

---

# 🏁 CONCLUSIONI E RIFLESSIONI

### 1) SMISTAMENTO AUTOMATICO (Modulo `production.py`)
Siamo molto soddisfatti di come funziona il programma di smistamento automatico perché siamo riusciti a fare in modo che il robot crei delle pile perfette in base al colore dei cubetti. Ogni volta che posiziona un cubetto, il programma si ricorda quanti ne ha messi e al giro dopo aumenta l'altezza di rilascio di circa 24,5 millimetri (l'altezza esatta del cubetto). In questo modo il robot non sbatte mai contro i pezzi già posizionati e non rischia di romperli.
Questo programma può ricordare il nostro progetto con dobot lite creato l'anno scorso in seconda superiore (2024/2025), dove creavamo 4 pile di cubetti più piccoli sempre in base al colore ma tramite una programmazione diversa (a blocchi) fornita direttamente da dobotLAB.

### 2) INTERFACCIA GRAFICA UNIVERSALE (Modulo `movement_gui.py`)
Il progetto è nato per creare un interfaccia stile "joystick" per il movimento del dobot magician, tuttavia lo abbiamo migliorato sempre di più implementando movimenti anche sull'asse Z (verticali) e la rotazione della ventosa.
Successivamente abbiamo implementato delle funzioni per il movimento del nastro trasportatore, con una parte dedicata nella GUI, cosa che abbiamo ripetuto successivamente per l'implementazione della rotaia, parte che ha richiesto più tempo per ottenere un movimento fluido e senza errori di posizione (come l'arrivare alla fine della rotaia ma il robot continua a provare a proseguire).

### IMPLEMENTAZIONI FUTURE
Questi 2 programmi possono essere uniti e migliorati in futuro, per esempio, alla ricezione di un cubetto ed al riconoscimento del colore, il robot si sposta sulla rotaria per raggiungere un "are di stoccaggio" con diverse pile di cubetti, ed aggiungendo altri robot si può in modo da creare una sorta di linea di produzione ridotta.

### ORGANIZZAZIONE DEL GRUPPO 
Il mio lavoro è stato svolto in gruppo con Rizzo Franceso ed Osti Gioia, tutti facevamo lo stesso codice fondamentale ed ognuno aggiungeva delle miglioria o piccolezze che poi venivano implementate anche dagli altri membri del gruppo, scambiandoci idee e miglioria a cui gli altri non avevano ancora pensato.
Per questo ogni membro aveva un programma leggermente diverso dagli altri ma con le stesse funzioni, ed alla completamento dei progetti, una volta che tutti i componenti del gruppo raggiungevano le piene funzionalità del proprio programma, veniva stabilito il "migliore" ovvero quello che avremmo tenuto come finale "ufficiale".
