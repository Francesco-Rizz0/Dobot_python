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


