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

* connessione al robot;
* inizializzazione;
* movimento verso coordinate assolute;
* movimento relativo;
* ritorno alla home;
* gestione della velocita e dell'accelerazione.



End-effector

* attivazione/disattivazione ventosa;
* apertura/chiusura pinza;
* gestione penna o altri utensili.



Rotaia / nastro trasportatore

* avvio;
* arresto;
* impostazione della velocita;
* cambio direzione, se previsto.



Sensori

* lettura sensore infrarossi;
* logiche di attesa basate sul rilevamento oggetti.



Telecamera e visione

* acquisizione immagine;
* estrazione del colore;
* classificazione del cubetto.



Gestione errori e stato del robot

* reset;
* clear alarm;
* verifica della connessione;
* riconoscimento degli stati anomali.








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



