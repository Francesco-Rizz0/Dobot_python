Note ed errori riscontrati

Questa sezione raccoglie i problemi pratici emersi durante lo sviluppo e le relative soluzioni operative.



Il robot interrompe il collegamento perché si connette a DobotLab

Se il robot e collegato a DobotLab, la connessione usata da VSCode può essere occupata o interrotta. I due ambienti non devono contendere contemporaneamente la stessa comunicazione.



Soluzione: chiudere o disconnettere DobotLab prima di riprendere il controllo del robot da VSCode.



Il codice e corretto ma i componenti smettono di funzionare

Questo problema può dipendere da uno stato di errore interno del robot, non necessariamente visibile dal solo script.

Procedura consigliata:

* spegnere il robot;
* riaccenderlo;
* resettarlo tenendo premuto per alcuni secondi il tasto Key posto sul retro;
* attendere il giro di calibrazione;
* attendere il ritorno alla home;
* aspettare il segnale acustico oppure verificare che la luce diventi verde.



Se la luce resta rossa fissa, in alcuni casi il programma può comunque partire da VSCode, ma e preferibile effettuare un controllo aggiuntivo.



Per maggiore sicurezza:

* connettere temporaneamente il robot a DobotLab;
* premere Clear Alarm;
* cancellare tutte le segnalazioni di errore;
* disconnettere nuovamente DobotLab;
* riprendere il lavoro in VSCode.



La rotaia si avvia ma il nastro non si muove

Se il motore vibra ma il nastro non avanza, spesso il problema non e un guasto ma una velocita impostata troppo bassa.

Controllo da fare: verificare il valore di velocita assegnato alla rotaia e aumentarlo gradualmente fino a ottenere un movimento effettivo.



Errore nel nome della funzione del nastro trasportatore

Una nota importante emersa durante lo sviluppo riguarda un'apparente incoerenza nella nomenclatura della funzione. Il comando che logicamente dovrebbe essere scritto come set\_conveyor in alcuni casi risulta riportato o implementato come:

*(python): set\_converyor*



Questa anomalia può generare confusione durante la lettura della documentazione o del codice esistente. Quando si lavora sul progetto, occorre quindi verificare attentamente il nome effettivo della funzione presente nella libreria realmente in uso.



I comandi DobotLab non corrispondono a quelli usati in VSCode

Questo e uno dei punti più importanti dell'intero progetto. La libreria disponibile in DobotLab non coincide con quella utilizzata in VSCode, ad esempio con ambienti o pacchetti come DobotEDU o equivalenti.

Di conseguenza:

* alcuni comandi presenti in DobotLab non vengono riconosciuti in VSCode;
* alcune funzioni esistono in entrambi gli ambienti ma con sintassi differente;
* il passaggio da un ambiente all'altro richiede una riscrittura del codice.



Non bisogna quindi considerare VSCode come un semplice posto alternativo in cui incollare il codice scritto altrove. Il cambio di ambiente comporta un vero cambio di interfaccia software.



Ulteriori note operative

Affidabilità dei jog in VSCode

La sezione di controllo manuale integrata in VSCode può essere utile per test veloci, ma non sempre e il metodo migliore per definire i punti di lavoro con precisione. Nelle applicazioni pratiche, piccoli errori di coordinata possono compromettere la presa del pezzo o la corretta deposizione.

Per questo e consigliabile usare i jog di DobotLab per la taratura iniziale dei punti, specialmente quando si lavora vicino ai limiti fisici del braccio o quando l'oggetto da afferrare e piccolo.



Importanza della calibrazione ambientale per la telecamera

Nel riconoscimento colori non basta che il codice sia corretto. E fondamentale che l'ambiente di acquisizione sia stabile. Cambiamenti nell'illuminazione della stanza, ombre prodotte dal braccio e riflessi sulla superficie dei cubetti possono alterare significativamente il risultato.



Per rendere il sistema più affidabile e utile:

* mantenere costante l'illuminazione;
* fissare la posizione della telecamera;
* definire una zona di acquisizione stabile;
* calibrare le soglie HSV sui colori reali presenti nel laboratorio.



Separare i test per sottosistema

Quando il progetto comprende braccio, ventosa, rotaia, sensore e telecamera, conviene evitare di collaudare tutto insieme alla prima esecuzione. E molto più efficace testare i moduli singolarmente:

* solo movimento del braccio;
* solo ventosa;
* solo rotaia;
* solo sensore;
* solo telecamera.



In questo modo diventa più semplice individuare l'origine dei malfunzionamenti.



Gestione ordinata dei file

Per facilitare la manutenzione del progetto, e consigliabile organizzare i file in cartelle dedicate, ad esempio:

* test base;
* moduli hardware;
* visione artificiale;
* utility;
* GUI;
* programmi completi.



Una struttura ordinata rende più semplice per i futuri studenti capire dove intervenire e quale file usare come punto di partenza.



Conclusione

La programmazione del Dobot Magician tramite VSCode offre un livello di controllo e flessibilità superiore rispetto all'uso esclusivo di DobotLab, ma richiede una comprensione più approfondita della comunicazione software-hardware, delle librerie Python, della gestione delle coordinate e dell'integrazione dei dispositivi esterni.

Il valore principale di questo progetto consiste proprio nell'aver costruito un percorso graduale: dal controllo base del braccio fino all'integrazione di ventosa, rotaia, sensore infrarossi e telecamera per il riconoscimento dei colori. Una documentazione ben organizzata permette a chi proseguirà il lavoro di non ripartire da zero, ma di comprendere sia le soluzioni adottate sia i problemi reali incontrati durante lo sviluppo.



Una scelta molto utile, nella versione finale del manuale, sarà aggiungere anche:

* un indice cliccabile;
* una sezione con tutti i comandi principali;
* esempi di codice commentati;
* schermate di configurazione;
* una tabella con i file del progetto e il loro scopo.


