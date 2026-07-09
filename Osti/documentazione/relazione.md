RELAZIONE FINALE DEL CORSO DI INFORMATICA E ROBOTICA
Oggetto: Programmazione e automazione del braccio robotico Dobot Magician in ambiente Python via VSCode
Coinvolgimento: Opero in collaborazione

1. INTRODUZIONE
La presente relazione descrive le attività svolte durante il corso di informatica focalizzato sulla robotica e sull'automazione industriale. Il percorso si è articolato in più giornate di laboratorio, durante le quali il grado di difficoltà dei problemi proposti è aumentato progressivamente.

L’obiettivo principale del nostro gruppo è stato quello di programmare un braccio robotico Dobot Magician utilizzando il linguaggio di programmazione Python all'interno dell'ambiente di sviluppo Visual Studio Code (VSCode), al fine di fargli eseguire compiti sequenziali di complessità crescente, simulando una vera e propria catena di montaggio e smistamento.

2. DIARIO DELLE ATTIVITÀ GIORNALIERE
Giorno 1: Configurazione dell'ambiente di sviluppo
La prima giornata è stata dedicata alla configurazione iniziale del sistema. Abbiamo studiato come interfacciare il Dobot Magician utilizzando l'editor VSCode, preferendolo all'IDE proprietario DobotLab per avere un controllo più approfondito sul codice. Abbiamo quindi cercato e installato le librerie Python idonee alla gestione del robot e individuato la corretta porta di comunicazione seriale del computer (identificata come COM3 o COM4) necessaria per stabilire il collegamento.

Giorno 2: Risoluzione dei problemi hardware e gestione dei driver
Durante il secondo giorno abbiamo riscontrato alcuni problemi che impedivano il corretto funzionamento del robot. Per risolverli, abbiamo proceduto all'aggiornamento dei driver del dispositivo. Questa operazione ci ha permesso di approfondire la conoscenza dell'hardware, scoprendo che esistono due versioni differenti del driver a seconda del chip montato sul robot: il Silicon Labs CP210x e il CH340 / CH341 (WCH).

Giorno 3: Comunicazione, librerie e primi componenti esterni
In questa giornata abbiamo risolto ulteriori anomalie nella comunicazione tra PC e robot, apprendendo la procedura per resettare il Dobot e studiando il significato diagnostico dei colori del LED lampeggiante sul corpo macchina.
Successivamente, abbiamo iniziato a integrare i primi accessori: il nastro trasportatore per la movimentazione dei cubetti e il sensore a infrarossi (configurato per arrestare il nastro non appena un oggetto interrompe il fascio).
Dal punto di vista del codice, abbiamo notato che la libreria usata da VSCode differisce da quella di DobotLab. In VSCode la sintassi richiede la chiamata esplicita dell'oggetto (es. dobot.magician...), mentre in DobotLab basta scrivere magician.... Abbiamo inoltre analizzato la funzione per muovere il nastro, notando un probabile errore di battitura degli sviluppatori nella libreria, dove la funzione è registrata come set_converyor anziché set_conveyor.

Giorno 4: Ottimizzazione del nastro e introduzione della telecamera (OpenCV)
Il quarto giorno abbiamo finalizzato l'implementazione del nastro e del sensore IR. A causa del malfunzionamento del circuito integrato del nastro e della scarsità di porte fisiche disponibili per collegare contemporaneamente nastro, sensore e circuito, abbiamo optato per l'aggiunta di una telecamera esterna per il riconoscimento visivo. Per gestirla, abbiamo integrato nel codice la libreria di visione artificiale OpenCV, convertendo lo spazio colore dei fotogrammi dalla scala RGB a quella HSV per facilitare la successiva segmentazione e identificazione cromatica dei cubetti.

Giorno 5: Sviluppo del ciclo completo di smistamento e timeout di sicurezza
Abbiamo creato un programma coordinato per gestire l'intero flusso di lavoro:

I cubetti avanzano sul nastro trasportatore.

Il nastro si ferma quando il sensore IR rileva il cubetto.

Il robot si attiva, preleva il cubetto e lo posiziona davanti alla telecamera.

Il sistema OpenCV riconosce il colore e il robot sposta il cubetto nella rispettiva pila (divisa per colore).

Se il colore non viene identificato, il cubetto viene depositato in una pila degli scarti.

Per evitare che il programma rimanesse attivo all'infinito a fine ciclo, abbiamo implementato un controllo di timeout: se per più di 10 secondi non vengono rilevati cubetti davanti al sensore, il codice si arresta automaticamente.

Giorno 6: Routine di disegno e calcolo delle coordinate
In questa giornata abbiamo testato le capacità di scrittura e disegno del robot. Abbiamo dovuto calcolare le proporzioni delle immagini che volevamo riprodurre, riadattandole matematicamente per non superare i limiti fisici del foglio di carta posizionato nell'area di lavoro. Abbiamo quindi scritto uno script capace di tradurre le linee dell'immagine in una serie di punti e coordinate cartesiane interpretabili da VSCode per guidare il braccio del Dobot.

Giorno 7: Progettazione dell'interfaccia grafica (GUI) e comandi base
Abbiamo iniziato a sviluppare un'interfaccia grafica (GUI) in Python per simulare il sistema di controllo manuale (jog) presente originariamente su DobotLab. All'interno di questa interfaccia abbiamo inserito i pulsanti per movimentare manualmente il robot nelle varie direzioni, oltre ai comandi specifici per inviare il robot alla posizione iniziale (Home) e per attivare o disattivare la ventosa di presa.

Giorno 8: Implementazione dell'asse lineare (Sliding Rail)
L'ottavo giorno abbiamo esteso l'area di lavoro del robot implementando la funzione sideway. Questa funzione permette al Dobot Magician di muoversi e scorrere lateralmente lungo una rotaia motorizzata apposita, aggiungendo di fatto un ulteriore grado di libertà ai movimenti del braccio.

Giorno 9: Perfezionamento della GUI e controllo dinamico delle porte
Abbiamo dedicato la giornata alla correzione dei bug e al raffinamento del codice dell'interfaccia grafica. Abbiamo integrato con successo all'interno della GUI i controlli definitivi per la gestione della rotaia lineare, il comando di ritorno alla Home e abbiamo aggiunto un menu a tendina che permette all'utente di selezionare dinamicamente a quale porta seriale (COM3 o COM4) connettere il robot prima di avviare il sistema.

Giorno 10: Documentazione del progetto su GitHub
Verso la conclusione del corso, abbiamo organizzato tutto il lavoro svolto creando un archivio (repository) sulla piattaforma GitHub. Abbiamo redatto la documentazione tecnica del Dobot Magician, inserendo tutti i programmi scritti nei giorni precedenti, i commenti alle funzioni utilizzate e le note relative alla risoluzione dei problemi hardware e software riscontrati.

Giorno 11: Stesura della relazione finale
Nell'ultima giornata ci siamo riuniti per raccogliere i dati, ordinare gli appunti di laboratorio e redigere questa relazione conclusiva per riassumere i risultati ottenuti.

3. CONCLUSIONI
Il corso si è rivelato altamente formativo. Partendo da zero e affrontando difficoltà via via crescenti, il nostro gruppo è riuscito a comprendere non solo le basi della programmazione in Python applicata alla robotica, ma anche l'importanza del problem solving davanti a problemi reali (come i driver non aggiornati, i limiti fisici delle porte hardware o i bug nelle librerie).

La collaborazione all'interno del gruppo ha permesso di dividere i compiti in modo efficiente, portando alla creazione di un sistema di smistamento automatizzato funzionante e di un'interfaccia di controllo flessibile e documentata.

Ringraziamo i docenti per il supporto fornito durante lo svolgimento delle attività.
