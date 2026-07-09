# Relazione di Progetto: Sviluppo e Sperimentazione con Bracci Robotici DOBOT

## 1. Introduzione
Il presente documento illustra le attività svolte durante un percorso progettuale di robotica della durata complessiva di **12 giorni**. Il progetto si è concentrato sull'utilizzo, l'integrazione hardware e la programmazione in Python di bracci robotici della serie **DOBOT (modello Magician Lite)**. 

Il percorso ha coperto un ampio spettro di applicazioni, articolate nelle seguenti aree macro-tematiche:
* **Manipolazione di base:** Operazioni di *Pick and Place* e ottimizzazione dei cicli di presa.
* **Fabbricazione digitale:** Configurazione e test del braccio in modalità stampa 3D.
* **Intelligenza Artificiale:** Integrazione di moduli di *computer vision* e algoritmi OCR per il *text detection*.
* **Automazione e Multimedialità:** Sincronizzazione audio-motoria e gestione di routine di eventi.
* **Sviluppo Software:** Progettazione e implementazione di un tool di controllo manuale (*Action Controller*) con generazione automatica di codice Python.

---

## 2. Mappatura dei Comandi e Interfaccia di Controllo
Per consentire l'interazione in tempo reale con il DOBOT e la successiva automazione dei processi, è stato sviluppato un sistema di controllo da tastiera denominato **Action Controller**. Di seguito viene riportata la specifica tecnica dei comandi implementati nel software per la movimentazione e la programmazione guidata:

### Movimentazione Spaziale
| Tasto | Azione / Funzione |
| :---: | :--- |
| **W, A, S, D** | Movimento del robot lungo gli assi principali del piano ($X$, $Y$). |
| **Spazio** | Innalzamento del braccio robotico (Asse $Z+$). |
| **Shift** | Abbassamento del braccio robotico (Asse $Z-$). |
| **+ / -** | Incremento o decremento della velocità di spostamento dei motori. |
| **H (Home)** | Comando di rientro automatico del robot alla posizione iniziale di calibrazione. |

### Gestione End-Effector (Ventosa)
| Tasto | Azione / Funzione |
| :---: | :--- |
| **E** | Abilitazione e attivazione della ventosa per la presa degli oggetti. |
| **Q** | Disabilitazione della ventosa per il rilascio degli oggetti. |
| **O** | Rotazione della ventosa in senso antiorario. |
| **P** | Rotazione della ventosa in senso orario. |

### Registrazione e Generazione del Codice
| Tasto | Azione / Funzione |
| :---: | :--- |
| **F** | Acquisizione e visualizzazione a schermo delle coordinate spaziali correnti. |
| **R** | **Modalità Registrazione:** Avvia/Interrompe la sessione. Durante la fase attiva, l'acquisizione dei punti critici tramite il tasto **F** permette di salvare le coordinate. Alla seconda pressione di **R**, il sistema restituisce il codice sorgente Python ottimizzato ed eseguibile. |
| **Backspace** | Funzione di **Undo**: cancella l'ultima riga di codice registrata in caso di errore di posizionamento. |
| **ESC** | Chiusura in sicurezza dell'applicazione e uscita dal programma. |

---

## 3. Diario di Bordo delle Attività

### Giorno 1: Introduzione e Setup Iniziale
* Setup della postazione di lavoro con il braccio robotico Magician Lite.
* Studio approfondito della documentazione tecnica e familiarizzazione con le API di comunicazione DOBOT.
* Scrittura dei primi script in Python per testare i movimenti cinematici di base.

### Giorno 2: Logica "Pick and Place"
* Sviluppo di un algoritmo in Python focalizzato sulla manipolazione degli oggetti.
* Programmazione del robot per eseguire cicli ripetitivi di impilamento e disimpilamento di cubetti colorati.
* Ottimizzazione della traiettoria e della precisione della ventosa in fase di presa.

### Giorno 3: Integrazione su Asse Lineare
* Estensione dell'area di lavoro (User Frame) mediante il montaggio del DOBOT su una rotaia motorizzata.
* Sostituzione dell'end-effector con una pinza meccanica.
* Test hardware e software per l'afferraggio, lo spostamento su asse e l'evacuazione di una bottiglia lungo il percorso.

### Giorno 4: Visione Artificiale e AI (Text Detection)
* Inizio del modulo dedicato all'Intelligenza Artificiale.
* Progettazione di un sistema di visione computerizzata tramite telecamera fissa sulla postazione.
* Implementazione di modelli AI per il riconoscimento e l'identificazione di testo (OCR) all'interno dell'area di lavoro.

### Giorno 5: Calcolo delle Coordinate Spaziali
* Continuazione del progetto di computer vision.
* Sviluppo e applicazione delle formule matematiche di calibrazione (omografia/trasformazione di coordinate).
* Conversione dei punti espressi in pixel della fotocamera nelle coordinate spaziali reali $(X, Y, Z)$ del DOBOT, consentendo il raggiungimento autonomo del target.

### Giorno 6: Fabbricazione Digitale (Stampa 3D)
* Riconfigurazione hardware del DOBOT tramite l'installazione di un kit estrusore per la stampa 3D.
* Esecuzione dei test di calibrazione del piano di lavoro.
* Prove pratiche di estrusione e stampa di geometrie elementari per valutare la precisione millimetrica e la costanza del braccio durante movimenti coordinati complessi.

### Giorno 7: Integrazione Multimediale e Gestione Audio
* Avvio della sezione dedicata alle interfacce multimediali interattive.
* Studio e integrazione della libreria `pygame.mixer` in Python per la gestione di flussi audio esterni in parallelo ai thread di movimento.
* Sviluppo di funzioni per l'inizializzazione del motore sonoro, regolazione del volume e caricamento dinamico di tracce musicali basate sull'input dell'utente.

### Giorno 8: Sincronizzazione Audio-Motoria e Routine di Eventi
* Evoluzione del software multimediale tramite lo sviluppo di una macro-routine coreografica.
* Programmazione di movimenti Point-to-Point (`ptp_mode`) complessi a velocità variabile.
* Sincronizzazione in tempo reale tra l'attivazione della ventosa ed effetti sonori situazionali (es. simulazioni acustiche ed eventi di interazione spaziale), conclusa con una sequenza di riposizionamento e un effetto sonoro finale personalizzato.

### Giorno 9: Sviluppo dell'Action Controller
* Sviluppo dell'architettura software principale per il controllo da tastiera (comandi descritti nella Sezione 2).
* Progettazione del modulo di cattura degli input e del parser logico in grado di tradurre istantaneamente le azioni manuali in uno script Python autonomo, pulito e riutilizzabile.

### Giorno 10: Assenza
* *Studente non presente all'attività.*

### Giorno 11: Testing, Debugging e Ottimizzazione
* Ripresa delle attività focalizzata sul collaudo intensivo del modulo *Action Controller* sviluppato il Giorno 9.
* Risoluzione di bug legati alla telemetria e alla sincronizzazione dei comandi inviati.
* Introduzione della funzione di cancellazione dell'ultima riga di codice generata (**Backspace**) e ottimizzazione delle performance dello script Python risultante.

### Giorno 12: Conclusioni Finali e Saluti
* Chiusura formale del progetto.
* Redazione e revisione della presente documentazione tecnica.
* Verifica finale dei risultati rispetto agli obiettivi prefissati e saluti con il team di supervisione.

---

## 4. Conclusioni Finali
Il progetto ha dimostrato l'estrema versatilità dei sistemi DOBOT se integrati ad ecosistemi software flessibili in Python. Le competenze sviluppate abbracciano discipline trasversali quali la cinematica lineare, la computer vision applicata alla robotica industriale, e lo sviluppo multimediale sincronizzato multithread.

Il principale valore aggiunto del lavoro è rappresentato dall'**Action Controller** (Giorno 9 e 11): uno strumento concreto che abbassa drasticamente la curva di apprendimento della robotica. Consentendo a utenti non programmatori di generare codice eseguibile semplicemente guidando il robot tramite una comune interfaccia tastiera, il tool apre prospettive interessanti in contesti di *rapid prototyping* e didattica. Il bilancio del percorso è ampiamente positivo, avendo combinato con successo hardware industriale, automazione e ingegneria del software.
