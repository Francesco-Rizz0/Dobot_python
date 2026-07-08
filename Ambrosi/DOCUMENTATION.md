# Dobot Magician Automation & Control Suite

Questo repository contiene una soluzione software in Python per interfacciare, controllare e automatizzare i bracci robotici Dobot Magician e Dobot Magician Lite.

---

## 📁 Struttura del Progetto

### 1. Controllo Manuale (`movement_gui.py`)
Un'interfaccia grafica sviluppata in Tkinter e progettata per il controllo manuale dei parametri del robot da parte di un operatore.
* **Rilevamento e Connessione**: Esegue la scansione delle porte COM attive tramite `search_dobot()` e convalida rigidamente il modello selezionato (Standard o Lite) per evitare conflitti di driver.
* **Movimento JOG**: Fornisce pulsanti interattivi per muovere il braccio lungo gli assi cartesiani ($X, Y, Z$) e per gestire la rotazione dell'end-effector ($R$).
* **Gestione Rotaia Lineare**: Permette il controllo accurato dell'asse aggiuntivo di scorrimento della slitta (asse $L$) in un range da 0 a 1000 mm.
* **Controllo Nastro Trasportatore**: Include uno slider per regolare manualmente la velocità del nastro da -10000 a +10000, insieme a un comando di arresto immediato.
* **Attuatore (Ventosa)**: Gestisce l'accensione e lo spegnimento della pompa a vuoto, integrando un sistema di spegnimento ritardato del compressore per preservare l'hardware.

### 2. Ciclo di Produzione Automatizzato (`production.py`)
Un'applicazione industriale focalizzata sullo smistamento automatico a ciclo continuo basata su visione artificiale.
* **Architettura Multiprocessing**: Separa l'esecuzione dei comandi del robot e l'elaborazione dei frame di OpenCV in processi indipendenti per evitare il congelamento della GUI su Windows, scambiando i dati tramite una `multiprocessing.Queue` sicura.
* **Visione Artificiale**: Converte il flusso video della telecamera nello spazio colore HSV per isolare le maschere cromatiche associate ai cubetti Rossi, Verdi e Blu.
* **Loop di Smistamento**: Avvia il nastro trasportatore, attende il rilevamento del cubetto tramite sensore a infrarossi, lo sposta sotto la telecamera per l'analisi del colore e lo impila nella colonna corretta aggiornando dinamicamente la coordinata $Z$.

---

## 📑 Mapping delle API `DobotEDU` Utilizzate

Il progetto si interfaccia con l'hardware Dobot sfruttando le seguenti funzioni native della libreria:

| Funzione API | Descrizione | Utilizzo nel Codice |
| :--- | :--- | :--- |
| `search_dobot()` | Scansiona le porte seriali di sistema alla ricerca di dispositivi connessi. | Identificazione e verifica iniziale del robot. |
| `connect_dobot()` | Inizializza la connessione logica con la porta seriale specificata. | Apertura del canale di comunicazione. |
| `disconnect_dobot()`| Disconnette in sicurezza il dispositivo interrompendo la sessione. | Chiusura della comunicazione da interfaccia grafica. |
| `get_pose()` | Restituisce un dizionario contenente le coordinate correnti ($X, Y, Z, R, L$). | Loop di aggiornamento della posizione in tempo reale sulla GUI. |
| `set_ptpcmd()` | Invia un comando di movimento Point-to-Point (PTP). | Movimento del braccio verso i punti di carico, ispezione e pile. |
| `set_jogcmd()` | Attiva il movimento continuo lungo una specifica direzione. | Gestione della movimentazione manuale tramite i pulsanti JOG. |
| `set_converyor()` | Configura lo stato di attivazione e la velocità del nastro trasportatore. | Avanzamento dei cubetti nel ciclo e controllo manuale. |
| `set_infrared_sensor()`| Abilita o disabilita il sensore a infrarossi collegato a una determinata porta. | Inizializzazione del sensore fotoelettrico sul nastro. |
| `get_infrared_sensor()`| Restituisce lo stato logico di attivazione (0 o 1) del sensore. | Loop di attesa del cubetto prima del blocco del nastro. |
| `set_endeffector_suctioncup()`| Controlla lo stato della valvola di aspirazione della ventosa. | Presa e rilascio dei blocchi durante le manipolazioni. |
| `set_homecmd()` | Avvia la procedura fisica di homing e calibrazione degli assi. | Reset hardware del braccio robotico tramite comando dedicato. |
| `set_device_withl()`| Abilita o disabilita la presenza logica della rotaia lineare. | Attivazione dei parametri per la slitta di scorrimento. |

---

## 💻 Dettagli Algoritmici: Colore Prevalente

Per garantire l'accuratezza dello smistamento ed evitare che il rumore di fondo influenzi il sistema, la funzione `get_prevalent_color()` applica un filtro basato su percentuali relative di pixel colorati rispetto al totale dei pixel non nulli individuati dalle maschere HSV:

$$P_{colore} = \frac{\text{Pixel della Maschera Specificata}}{\text{Totale Pixel Rilevati (Maschera R + G + B)}}$$

* **Soglia di Presenza**: Se la percentuale calcolata è inferiore al $5\%$, il colore viene scartato per azzerare i piccoli residui visivi ambientali.
* **Soglia di Dominanza**: Un colore viene ufficialmente convalidato e restituito al robot solo se la sua percentuale relativa è strettamente maggiore o uguale al $51\%$. In caso contrario, il cubetto viene marcato come `"null"` e indirizzato alla pila degli scarti.
