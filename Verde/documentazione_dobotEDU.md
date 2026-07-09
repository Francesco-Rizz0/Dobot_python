# Documentazione ufficiale delle funzionalità di DobotEDU



## 1. Panoramica del software

**DobotEDU** è un ambiente integrato progettato per colmare il divario tra la programmazione didattica e l'automazione industriale reale. Funziona in sinergia con **DobotLink** (il servizio di backend che gestisce i driver e le porte seriali del PC) e permette di controllare l'hardware attraverso diversi livelli di astrazione, dal codice a blocchi fino a script Python avanzati.



## 2. Ambienti di programmazione integrati

DobotEDU offre tre moduli principali di sviluppo all'interno della stessa interfaccia:

### Programmazione a blocchi (Blockly)

* **Descrizione:** Un ambiente visuale basato su Google Blockly pensato per l'introduzione alla robotica.
* **Funzionalità:**
  * Blocchi dedicati per il movimento cinematico del robot (PTP, JOG, Linear).
  * Controllo nativo degli accessori (ventosa, pinza, scrittura).
  * Traduzione in tempo reale del codice a blocchi in codice Python in una finestra laterale.



### Programmazione in Python

* **Descrizione:** Un IDE Python integrato e preconfigurato con le librerie proprietarie per il controllo del braccio.
* **Funzionalità:**
  * Auto-completamento dei comandi specifici del Dobot.
  * Console di debug integrata per la lettura degli errori di sintassi o di timeout hardware.
  * Accesso diretto ai moduli hardware avanzati tramite la libreria `DobotEDU`.



### Scripting per l'intelligenza artificiale (AI Lab)

* **Descrizione:** Moduli dedicati all'integrazione di telecamere e sensori per progetti di machine learning.
* **Funzionalità:**
  * Blocchi e librerie per il riconoscimento dei colori, delle forme e dei codici a barre.
  * Algoritmi di classificazione visiva per compiti di smistamento automatizzato (Pick and Place intelligente).





## 3. Moduli di controllo hardware (Libreria `m_lite` / `magician`)

La suite software espone le API per interagire direttamente con i motori, i giunti e gli end-effector del robot. Le funzionalità principali si dividono in:

### Gestione della cinematica e del movimento

* **`set_ptpcmd` (Point-To-Point):** Permette di muovere il robot verso coordinate assolute ($X, Y, Z, R$) nello spazio cartesiano. Supporta diverse modalità, come il movimento coordinato tra i giunti (`ptp_mode=0`) o lineare interpolato (`ptp_mode=1`).
* **`set_jogcmd`:** Gestisce il movimento continuo lungo un asse specifico finché il comando è attivo (fondamentale per il controllo manuale tramite tastiera o joystick).
* **`set_homecmd`:** Avvia la routine di calibrazione hardware che riporta il robot alle sue coordinate zero di fabbrica (posizione di sicurezza).
* **`get_pose`:** Interroga i sensori di posizione dei motori (encoder) per restituire in tempo reale un dizionario contenente la posizione spaziale attuale ($x, y, z$) e l'angolo di rotazione dell'utensile ($r$).

### Configurazione delle dinamiche

* **`set_armspeed_ratio`:** Controlla i parametri di velocità e accelerazione del braccio. Permette di impostare la velocità massima di trasferimento o la velocità di avvio del posizionamento (`set_type=0` o `set_type=1`) con valori percentuali da 1 a 100.

### Controllo degli end-effector (Attuatori terminali)

* **`set_endeffector_suctioncup`:** Invia segnali digitali alla scheda logica per azionare la pompa pneumatica della ventosa (attivazione dell'effetto vuoto per il prelievo o inversione del flusso per il rilascio dell'oggetto).
* **`set_endeffector_gripper`:** Gestisce l'apertura e la chiusura della pinza motorizzata accessoria.
* **`set_endeffector_laser` / `Pen`:** Attiva o disattiva i moduli per la scrittura, il disegno o l'incisione laser leggera.



## 4. Strumenti di utilità e diagnostica

* **Gestore delle connessioni:** Un pannello grafico per scansionare le porte COM (Windows) o ttyUSB (Linux) e associare istantaneamente il braccio robotico corretto.
* **Insegnamento e riproduzione (Teach and Playback):** Una modalità che permette di muovere fisicamente il braccio robotico con le mani (premendo il tasto di sblocco sul robot) memorizzando i punti nello spazio premendo un pulsante, per poi rieseguire la sequenza registrata in automatico.
* **Aggiornamento firmware:** Strumento integrato per flashare i firmware ufficiali della scheda logica del Dobot direttamente tramite cavo USB, garantendo la compatibilità con le nuove release di DobotEDU.
