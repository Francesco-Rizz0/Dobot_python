# Documentazione Dobot Magician

### Obiettivo del progetto

Questo progetto nasce con l'obiettivo di fornire una guida pratica e tecnica per la programmazione del Dobot Magician tramite Visual Studio Code, come alternativa all'ambiente proprietario DobotLab.



## Requisiti e prerequisiti

Per utilizzare correttamente il Dobot Magician in questo progetto sono necessari sia componenti hardware sia competenze software.



### Requisiti hardware

Per replicare le prove e i programmi sviluppati servono:

* Dobot Magician;
* alimentatore del braccio robotico;
* end-effector compatibili:
* ventosa;
* pinza;
* penna;
* rotaia / nastro trasportatore;
* sensore a infrarossi;
* telecamera, utilizzata per sostituire il circuito laterale danneggiato o non programmato per il riconoscimento dei colori;
* oggetti di test, ad esempio cubetti colorati, da usare durante le prove di presa, trasporto e riconoscimento.



### Requisiti software

A livello software servono:

* Visual Studio Code;
* Python correttamente installato (versione 3.10 per usare DobotEDU dato che le versioni successive non sono compatibili);
* librerie Python necessarie per comunicare con il robot e con gli eventuali moduli aggiuntivi;
* DobotLink in esecuzione in background, se richiesto dalla comunicazione tra VSCode e Dobot Magician;
* eventuali driver USB/seriali corretti, a seconda del chip di comunicazione montato sul dispositivo.



### Prerequisiti tecnici

Prima di iniziare e consigliato avere familiarità con:

* sintassi di base di Python;
* gestione dell'ambiente di sviluppo in VSCode;
* concetti base di:
* porte seriali;
* coordinate cartesiane;
* gestione di input/output;
* uso di librerie esterne in Python;
* funzionamento generale del Dobot Magician e delle sue modalità operative.





## Architettura di funzionamento: come VSCode comunica con il robot

Per comprendere i programmi sviluppati e fondamentale capire come avviene la comunicazione tra il computer e il Dobot Magician.



Il flusso generale e il seguente:



VSCode -> script Python -> DobotLink (in background) -> Dobot Magician



In questa architettura:

* VSCode e l'ambiente in cui si scrive ed esegue il codice;
* Python contiene le istruzioni operative inviate al robot;
* DobotLink funge da ponte di comunicazione tra software e hardware;
* Dobot Magician riceve i comandi ed esegue i movimenti o le operazioni richieste.



Questa distinzione e importante perché molti problemi apparentemente legati al codice derivano in realtà da:

* connessioni seriali occupate;
* DobotLab aperto in parallelo;
* driver non corretti;
* stato di allarme del robot;
* inizializzazione incompleta del sistema.


# SPECIFICHE HARDWARE E SOFTWARE
## Collegamento corretto dell'hardware

Una delle cause più frequenti di malfunzionamento non riguarda il codice, ma il collegamento fisico dei componenti. Per questo e utile seguire una procedura ordinata.



### 1\. Alimentazione del braccio

Il Dobot Magician deve essere collegato al proprio alimentatore e acceso correttamente prima di tentare la connessione da software. Dopo l'accensione il robot esegue la fase di inizializzazione e porta il sistema in uno stato operativo.



### 2\. Collegamento del robot al computer

Il robot viene collegato al PC tramite connessione dati, generalmente USB. In questa fase il sistema operativo deve riconoscere correttamente il dispositivo seriale; in caso contrario occorre verificare i driver installati.



### 3\. Collegamento degli end-effector

Gli strumenti terminali come ventosa, pinza e penna devono essere montati correttamente e collegati secondo la configurazione prevista dal robot. Una configurazione errata può causare movimenti corretti del braccio ma mancata attivazione dell'end-effector.



### 4\. Collegamento della rotaia o del nastro trasportatore

La rotaia deve essere alimentata e collegata secondo le interfacce previste. Se il motore entra in funzione ma il nastro non si muove, il problema può dipendere non dall'hardware ma dalla velocita impostata, troppo bassa per produrre un movimento visibile o utile.



### 5\. Collegamento del sensore a infrarossi

Il sensore deve essere montato in una posizione coerente con il compito richiesto, ad esempio per rilevare il passaggio o la presenza di un cubetto sulla linea di trasporto. Oltre al collegamento fisico, e necessario verificare che i pin o le porte lette dal programma corrispondano alla configurazione reale.



### 6\. Collegamento della telecamera

La telecamera viene introdotta per sostituire il circuito laterale danneggiato oppure non programmato per riconoscere i colori. Il suo posizionamento e fondamentale: deve inquadrare in modo stabile l'area in cui transitano gli oggetti, con illuminazione il più possibile costante. Variazioni di luce, riflessi e ombre influenzano direttamente il riconoscimento dei colori.





## Significato dei colori della spia del robot

La spia luminosa presente sul corpo del Dobot Magician fornisce indicazioni immediate sullo stato del sistema. Interpretarla correttamente permette di capire se il problema riguarda l'avvio, la connessione o la fase operativa.



Colore spia  |  Significato

\-------------------------------------------------------------------------------------------

Rosso        |  Errore o stato di allarme

\-------------------------------------------------------------------------------------------

Verde	       |  Robot connesso e pronto all'uso

\-------------------------------------------------------------------------------------------

Blu           |  Tentativo di connessione

\-------------------------------------------------------------------------------------------

Giallo        |  Avvio del sistema

\-------------------------------------------------------------------------------------------

Arancione      |  Anomalia di comunicazione, errore nelle coordinate o braccio fuori limite

\-------------------------------------------------------------------------------------------

La spia va sempre interpretata insieme al comportamento del robot. Ad esempio, una luce rossa fissa può indicare un allarme che impedisce il funzionamento corretto di alcuni componenti, anche se il programma risulta sintatticamente corretto.




## Funzionalità principali del progetto

Il lavoro sviluppato e stato organizzato in modo graduale, aggiungendo progressivamente componenti e logiche di controllo.



### 1\. Controllo base del braccio robotico

La prima fase ha riguardato il movimento del Dobot Magician nello spazio, con definizione delle coordinate, degli spostamenti e delle posizioni operative principali.



### 2\. Integrazione della ventosa

Successivamente e stata aggiunta la ventosa, per consentire la presa e il rilascio degli oggetti. Questa parte e fondamentale per apprendere la sincronizzazione tra movimento del braccio e attivazione dell'end-effector.



### 3\. Attivazione della rotaia

In un secondo momento e stata integrata la rotaia / nastro trasportatore, per gestire il trasporto dei cubetti lungo una linea di lavoro. Qui il sistema non controlla più soltanto il braccio, ma coordina il movimento di due sottosistemi differenti.



### 4\. Uso del sensore a infrarossi

Il sensore a infrarossi e stato poi utilizzato per rilevare la presenza di oggetti e rendere il programma più autonomo e reattivo rispetto agli eventi dell'ambiente.



### 5\. Introduzione della telecamera per il riconoscimento dei colori

L'ultima estensione ha previsto l'aggiunta di una telecamera per identificare il colore dei cubetti trasportati dalla rotaia. Questa parte sostituisce il circuito laterale non disponibile o non adeguatamente programmato.



### 6\. Programmi aggiuntivi

Oltre alla sequenza principale, sono stati realizzati altri file dedicati a funzioni specifiche, tra cui:

* programma per riportare il robot alla home;
* gestione del movimento su una rotaia di scorrimento;
* programma con interfaccia GUI;
* script sperimentali per testare singoli sottosistemi separatamente.





## Sistema di coordinate e tracciamento dei punti

Per programmare correttamente il Dobot Magician e indispensabile comprendere il sistema di coordinate con cui il robot si muove.



Le coordinate definiscono la posizione del terminale del braccio nello spazio operativo. In generale, quando si insegna un punto al robot, si lavora su parametri spaziali che descrivono:

* posizione lungo gli assi;
* altezza;
* orientamento dell'end-effector;
* eventuali offset rispetto al piano di lavoro.



La precisione dei punti e un aspetto critico. Se una coordinata e anche solo leggermente errata, il robot può:

* mancare l'oggetto;
* urtare il piano;
* uscire dai limiti di movimento;
* generare errori di allarme.



Osservazione pratica importante

Su VSCode e presente una sezione dedicata al Dobot Magician quando il robot viene collegato al computer. Tuttavia, la sottosezione che contiene i jog del robot non risulta sempre affidabile per rilevare o rifinire con precisione i punti di lavoro.

Per questo motivo e consigliabile usare DobotLab per la ricerca pratica delle coordinate, poiché i suoi controlli manuali risultano generalmente più comodi e stabili per il posizionamento fine del braccio. Una volta ottenuti i punti desiderati, tali coordinate possono essere riportate e adattate negli script sviluppati in VSCode. Questa procedura riduce il rischio di errori di posizionamento e velocizza la fase di test.





## Funzioni principali da conoscere

Per realizzare programmi utili non basta sapere che il robot si muove: occorre conoscere bene le funzioni fondamentali disponibili nelle librerie usate in VSCode.





Indice delle funzioni Python per Dobot Magician

Movimento del braccio

* connessione al robot -> *device = pydobot.Dobot(port='COM3')*;
* inizializzazione -> *device.pose()*;
* movimento verso coordinate assolute -> *device.move_to(x, y, z, r, wait=True)*;
* movimento relativo -> *device.move_to(x + dx, y + dy, z + dz, r + dr, wait=True)*;
* gestione della velocita e dell'accelerazione -> *device.speed(velocity, acceleration)*.



End-effector

* attivazione/disattivazione ventosa -> *device.suck(True) # Attiva l'aspirazione e device.suck(False) # Disattiva l'aspirazione *;
* apertura/chiusura pinza -> *device.grip(True) # Chiude la pinza e device.grip(False) # Apre la pinza*;
* gestione penna o altri utensili -> *device.move_to(x, y, z_contatto, r, wait=True)  # Penna giù e device.move_to(x, y, z_sollevato, r, wait=True) # Penna su*.



Rotaia / nastro trasportatore

* avvio -> *device.conveyor_belt(speed=100) # Avvia il nastro a una determinata velocità*;
* arresto -> *device.conveyor_belt(speed=0)   # Ferma il nastro impostando la velocità a zero*;
* impostazione della velocita -> *device.conveyor_belt(speed=150) # Valore positivo per aumentare la velocità*;
* cambio direzione, se previsto -> *device.conveyor_belt(speed=-100) # Il segno meno inverte la direzione di marcia*.



Sensori

* lettura sensore infrarossi -> *stato_sensore = device.get_infrared_sensor(port=2) # Ritorna 1 se c'è un oggetto, 0 se è vuoto*;
* logiche di attesa basate sul rilevamento oggetti -> *while device.get_infrared_sensor(port=2) == 0:
    time.sleep(0.1) # Attende l'arrivo dell'oggetto (es. sul nastro)*.



Telecamera e visione

* acquisizione immagine -> *cap = cv2.VideoCapture(0) # 0 indica la telecamera predefinita
ret, frame = cap.read()   # 'frame' contiene la matrice di pixel dell'immagine*;
* estrazione del colore -> *hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
maschera = cv2.inRange(hsv, lower_red, upper_red) # Isola i pixel rossi*;
* classificazione del cubetto -> *pixel_colore = cv2.countNonZero(maschera)
if pixel_colore > 500: # Soglia empirica
    colore_rilevato = "Rosso"*.



Gestione errori e stato del robot

* reset -> *device.close()
device = pydobot.Dobot(port='COM3')*;
* clear alarm -> *device.clear_alarms()*;
* verifica della connessione -> *try:
    device.pose()
    connesso = True
except Exception:
    connesso = False*;
* riconoscimento degli stati anomali -> *allarmi_attivi = device.get_alarms()
if len(allarmi_attivi) > 0:
    print(f"Anomalia rilevata! Codici errore: {allarmi_attivi}")*.








## Riconoscimento dei colori: RGB e HSV

Una delle parti più avanzate del progetto riguarda il riconoscimento dei colori dei cubetti trasportati dalla rotaia.



### Scala RGB

La scala RGB rappresenta i colori come combinazione di tre componenti:

* R = rosso;
* G = verde;
* B = blu.



Ogni colore viene descritto assegnando un'intensità a ciascuna di queste tre componenti. Questo modello e molto diffuso nelle immagini digitali, ma non sempre e il più comodo per distinguere i colori in modo robusto, specialmente quando cambiano illuminazione o ombre.



### Limiti pratici della RGB

Nel riconoscimento reale, due oggetti dello stesso colore possono produrre valori RGB diversi se:

* cambia la luce ambientale;
* la superficie riflette diversamente;
* l'oggetto e più vicino o più lontano dalla telecamera;
* sono presenti ombre.



Per questo, in ambito di visione artificiale si preferisce spesso lavorare nello spazio HSV.



### Scala HSV

La scala HSV descrive il colore in modo più vicino alla percezione umana:

* H - Hue: tonalità del colore;
* S - Saturation: saturazione, cioè quanto il colore e intenso o sbiadito;
* V - Value: valore o luminosità.



Questo approccio rende più facile isolare un colore specifico, perché la tonalità può essere separata dalla luminosità.



### Perché HSV e utile nel progetto

Nel caso dei cubetti colorati verde, rosso, giallo e blu, lavorare in HSV permette di definire intervalli di tonalità più stabili rispetto ai semplici valori RGB. In pratica, invece di confrontare un singolo tripletto numerico, il programma verifica se il colore rilevato ricade all'interno di una fascia attesa.



### Conversione da RGB a HSV

La conversione da RGB a HSV consiste nel rielaborare le tre componenti RGB per ottenere:

* la tonalità dominante;
* il livello di saturazione;
* la luminosità complessiva.



Concettualmente:

* si osserva quale componente tra R, G e B e dominante;
* si misura la differenza tra il valore massimo e quello minimo;
* da questi rapporti si ricavano Hue, Saturation e Value.



In pratica, questa conversione viene spesso eseguita con librerie di elaborazione immagini, evitando di implementare manualmente l'algoritmo matematico. Tuttavia e importante comprenderne il significato, perché la scelta delle soglie HSV influenza direttamente la precisione del riconoscimento.



### Logica generale del programma di riconoscimento colori

Il programma con telecamera segue in genere una struttura di questo tipo:

* acquisisce un fotogramma;
* isola la zona di interesse;
* converte l'immagine da RGB o BGR a HSV;
* applica soglie per individuare il colore cercato;
* classifica il cubetto;
* passa al robot l'informazione utile per decidere dove spostarlo.



Il punto più delicato non e tanto la lettura dell'immagine, quanto la taratura delle soglie HSV. Soglie troppo strette fanno perdere oggetti validi; soglie troppo larghe causano classificazioni errate.

## Librerie da installare in VSCode e differenze rispetto a DobotLab

Uno degli aspetti più importanti da chiarire e che il codice scritto in DobotLab non può essere trasferito automaticamente in VSCode, e viceversa, in modo diretto e semplice.

Il motivo principale e che le librerie usate nei due ambienti non coincidono. Anche quando i nomi delle funzioni sembrano simili, spesso cambiano:

* sintassi;
* parametri;
* modalità di connessione;
* struttura dei moduli;
* gestione dei dispositivi.



### Perché non basta copiare il codice

DobotLab è un ambiente integrato sviluppato per lavorare con una propria struttura interna e con una propria implementazione delle API. VSCode, invece, e solo un editor: per far funzionare il robot bisogna installare e configurare manualmente i pacchetti Python necessari.

Anche se il comportamento desiderato del robot rimane lo stesso, il codice cambia perché cambia il livello di astrazione con cui i comandi vengono espressi.



## Librerie da installare

La lista precisa delle librerie dipende dal vostro repository e dalla modalità scelta per pilotare il robot, ma in un progetto di questo tipo di solito occorre distinguere almeno quattro categorie.



### 1\. Librerie per la comunicazione con il Dobot

Queste librerie servono a inviare comandi al robot, gestire connessione, stato e movimenti. In base alla soluzione adottata nel progetto, potrebbe essere presente una libreria specifica per il Dobot Magician oppure un wrapper Python dedicato.



### 2\. Librerie per la comunicazione seriale

Una libreria come *pyserial* e spesso necessaria per gestire la comunicazione tramite porta seriale tra PC e robot o tra PC e moduli intermedi.



### 3\. Librerie per la visione artificiale

Per la telecamera e l'analisi dei colori e normalmente utile una libreria come *OpenCV*, che consente:

* acquisizione dei frame;
* conversione tra spazi colore;
* filtraggio;
* sogliatura (metodo di segmentazione);
* riconoscimento basato su maschere.



### 4\. Librerie di supporto

A seconda del progetto possono servire anche librerie per:

* calcoli numerici -> *math* (già installata) e *numpy* (aggiuntive: *scipy* e *cmath*;
* gestione GUI -> *tkinter*;
* manipolazione di array o immagini -> *numpy*, *opencv-python* (importata come cv2);
* sincronizzazione temporale e gestione di eventi -> *time* (es: *time.sleep()*), *threading*.



### Come installare le librerie dal terminale di VSCode

Nel manuale e opportuno spiegare la procedura in modo operativo.



#### Passo 1: verificare Python

Nel terminale di VSCode, controllare che Python sia installato correttamente:

*(bash): python --version*



oppure, in alcuni sistemi:

*(bash): python3 --version*



#### Passo 2: creare un ambiente virtuale

Per evitare conflitti tra librerie di progetti diversi, e consigliabile creare un ambiente virtuale:

*(bash): python -m venv .venv*



Attivazione su Windows:

*(bash): .venv\\Scripts\\activate*



Attivazione su Linux o macOS:

*(bash): source .venv/bin/activate*



#### Passo 3: aggiornare pip

*(bash): python -m pip install --upgrade pip*



#### Passo 4: installare i pacchetti necessari

Esempi comuni:

*(bash):

* pip install pyserial
* pip install opencv-python
* pip install numpy*



Se il progetto usa una libreria specifica per Dobot, questa va installata secondo il nome esatto del pacchetto o secondo le istruzioni del repository.



#### Passo 5: salvare le dipendenze

Per rendere il progetto replicabile, e utile esportare le dipendenze installate:

*(bash): pip freeze > requirements.txt*



In questo modo un altro utente potrà installarle con:

*(bash): pip install -r requirements.txt*



A cosa servono concretamente le librerie

* pyserial: permette di comunicare tramite porta seriale con dispositivi hardware;
* opencv-python: gestisce acquisizione video, elaborazione immagini e riconoscimento colori;
* numpy: supporta operazioni numeriche efficienti, molto utili nella manipolazione delle immagini;
* eventuali librerie Dobot-specifiche: espongono le funzioni per muovere il braccio, attivare la ventosa, controllare la rotaia e leggere lo stato del robot.



Avvertenza fondamentale

Se un comando funziona in DobotLab, non significa che funzionerà con la stessa sintassi in VSCode. Questa e una delle fonti più frequenti di errore. In molti casi e necessario reinterpretare la logica del programma e ricostruirla usando le API disponibili nel nuovo ambiente.



## Driver del Dobot Magician

Quando il robot viene collegato al computer, il sistema operativo deve riconoscerlo tramite il driver corretto. Nel caso del Dobot Magician possono comparire principalmente due famiglie di driver USB-seriale:

* Silicon Labs CP210x
* CH340 / CH341 (WCH)



### Driver Silicon Labs (CP210x)

Questi driver sono usati quando il dispositivo monta un chip CP210x, prodotto da Silicon Labs. Il loro compito e convertire la comunicazione USB del computer in una comunicazione seriale interpretabile dal robot.



### Driver CH340 / CH341 (WCH)

Questi driver sono invece associati ai chip CH340 o CH341, molto diffusi nei dispositivi seriali USB e nelle schede di controllo economiche o compatibili.



### Differenza pratica tra i due

Dal punto di vista dell'utente finale, entrambi servono allo stesso scopo: permettere al sistema operativo di vedere il dispositivo come una porta seriale. La differenza reale dipende dal chip montato sull'hardware. Non si scelgono arbitrariamente: va installato il driver corrispondente all'interfaccia effettivamente presente sul dispositivo o sull'adattatore usato.



In sintesi:

Driver	     |  Produttore    |  Quando si usa

\---------------------------------------------------------------------------------------------

CP210x	     |  Silicon Labs  |  Se l'interfaccia USB-seriale del dispositivo usa chip CP210x

\---------------------------------------------------------------------------------------------

CH340/CH341  |  WCH           |   Se l'interfaccia USB-seriale usa chip CH340 o CH341

\---------------------------------------------------------------------------------------------



Come capire quale driver usare

In genere si può verificare:

* da Gestione dispositivi su Windows;
* leggendo il nome della periferica collegata;
* controllando l'identificativo hardware;
* consultando documentazione o serigrafia del modulo.



Se il dispositivo non viene riconosciuto correttamente oppure compare come periferica sconosciuta, il problema potrebbe essere proprio l'assenza del driver corretto.



Come aggiornare i driver

La procedura generale consiste nel:

* collegare il Dobot al PC;
* aprire Gestione dispositivi;
* individuare la periferica seriale o sconosciuta;
* verificare il nome del driver attuale;
* aggiornare il driver manualmente o reinstallarlo se necessario.




