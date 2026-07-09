Librerie da installare in VSCode e differenze rispetto a DobotLab

Uno degli aspetti più importanti da chiarire e che il codice scritto in DobotLab non può essere trasferito automaticamente in VSCode, e viceversa, in modo diretto e semplice.

Il motivo principale e che le librerie usate nei due ambienti non coincidono. Anche quando i nomi delle funzioni sembrano simili, spesso cambiano:

* sintassi;
* parametri;
* modalità di connessione;
* struttura dei moduli;
* gestione dei dispositivi.



Perché non basta copiare il codice

DobotLab e un ambiente integrato sviluppato per lavorare con una propria struttura interna e con una propria implementazione delle API. VSCode, invece, e solo un editor: per far funzionare il robot bisogna installare e configurare manualmente i pacchetti Python necessari.

Anche se il comportamento desiderato del robot rimane lo stesso, il codice cambia perché cambia il livello di astrazione con cui i comandi vengono espressi.



Librerie da installare

La lista precisa delle librerie dipende dal vostro repository e dalla modalità scelta per pilotare il robot, ma in un progetto di questo tipo di solito occorre distinguere almeno quattro categorie.



1\. Librerie per la comunicazione con il Dobot

Queste librerie servono a inviare comandi al robot, gestire connessione, stato e movimenti. In base alla soluzione adottata nel progetto, potrebbe essere presente una libreria specifica per il Dobot Magician oppure un wrapper Python dedicato.



2\. Librerie per la comunicazione seriale

Una libreria come pyserial e spesso necessaria per gestire la comunicazione tramite porta seriale tra PC e robot o tra PC e moduli intermedi.



3\. Librerie per la visione artificiale

Per la telecamera e l'analisi dei colori e normalmente utile una libreria come OpenCV, che consente:

* acquisizione dei frame;
* conversione tra spazi colore;
* filtraggio;
* sogliatura (metodo di segmentazione);
* riconoscimento basato su maschere.



4\. Librerie di supporto

A seconda del progetto possono servire anche librerie per:

* calcoli numerici;
* gestione GUI;
* manipolazione di array o immagini;
* sincronizzazione temporale e gestione di eventi.



Come installare le librerie dal terminale di VSCode

Nel manuale e opportuno spiegare la procedura in modo operativo.



Passo 1: verificare Python

Nel terminale di VSCode, controllare che Python sia installato correttamente:

*(bash): python --version*



oppure, in alcuni sistemi:

*(bash): python3 --version*



Passo 2: creare un ambiente virtuale

Per evitare conflitti tra librerie di progetti diversi, e consigliabile creare un ambiente virtuale:

*(bash): python -m venv .venv*



Attivazione su Windows:

(bash): .venv\\Scripts\\activate



Attivazione su Linux o macOS:

(bash): source .venv/bin/activate



Passo 3: aggiornare pip

(bash): python -m pip install --upgrade pip



Passo 4: installare i pacchetti necessari

Esempi comuni:

(bash):

* pip install pyserial
* pip install opencv-python
* pip install numpy



Se il progetto usa una libreria specifica per Dobot, questa va installata secondo il nome esatto del pacchetto o secondo le istruzioni del repository.



Passo 5: salvare le dipendenze

Per rendere il progetto replicabile, e utile esportare le dipendenze installate:

(bash): pip freeze > requirements.txt



In questo modo un altro utente potrà installarle con:

(bash): pip install -r requirements.txt



A cosa servono concretamente le librerie

* pyserial: permette di comunicare tramite porta seriale con dispositivi hardware;
* opencv-python: gestisce acquisizione video, elaborazione immagini e riconoscimento colori;
* numpy: supporta operazioni numeriche efficienti, molto utili nella manipolazione delle immagini;
* eventuali librerie Dobot-specifiche: espongono le funzioni per muovere il braccio, attivare la ventosa, controllare la rotaia e leggere lo stato del robot.



Avvertenza fondamentale

Se un comando funziona in DobotLab, non significa che funzionerà con la stessa sintassi in VSCode. Questa e una delle fonti più frequenti di errore. In molti casi e necessario reinterpretare la logica del programma e ricostruirla usando le API disponibili nel nuovo ambiente.

