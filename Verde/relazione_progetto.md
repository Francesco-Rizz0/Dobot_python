# Relazione tecnica di progetto: robotica FSL
Controllo remoto e automazione di Dobot Magician Lite tramite Python



## 1. Obiettivo del progetto
L'obiettivo principale del progetto è stato lo sviluppo di un software in Python per il controllo remoto e in tempo reale del braccio robotico **Dobot Magician Lite**. Utilizzando la tastiera del PC come interfaccia di input, si è riusciti a mappare i movimenti in modalità JOG sui tre assi spaziali e la rotazione dell'utensile, a gestire l'effetto terminale (ventosa) e a implementare un sistema di registrazione dei punti d'interesse per generare automaticamente blocchi di codice pronti all'uso.



## 2. Architettura hardware e ambiente di sviluppo
Il sistema sfrutta la connessione seriale tra l'elaboratore host e il controller del braccio robotico tramite una porta di comunicazione dedicata (`COM4`).

* **Hardware:** Braccio robotico Dobot Magician Lite con modulo ventosa.
* **IDE di sviluppo:** Visual Studio Code (VS Code).
* **Linguaggio di programmazione:** Python 3.8.

### Nota sulla compatibilità del software
> [!IMPORTANT]
> **Criticità riscontrata:** Durante la fase di configurazione, l'utilizzo dell'ultima versione di Python ha causato incompatibilità strutturali con il software di backend DobotLink e le relative librerie.
> 
> **Soluzione:** È stato effettuato un downgrade dell'ambiente d'esecuzione a **Python 3.8**, che ha garantito la piena stabilità e il corretto funzionamento del framework **DobotEDU**.

Le librerie integrate nello script sono:
* `DobotEDU (m_lite)`: Libreria software ufficiale per l'invio dei comandi cinematici, di posizionamento e di controllo degli attuatori del robot.
* `keyboard`: Per l'intercettazione e la gestione in tempo reale degli input da tastiera senza bloccare l'esecuzione del ciclo principale.
* `pyperclip`: Utilizzata per interagire con il sistema operativo al fine di copiare automaticamente il codice generato negli appunti del PC.



## 3. Mappatura dei comandi (interfaccia utente)
L'interazione con il robot è gestita interamente tramite tastiera in tempo reale:

| Tasto | Azione |
| :---: | :--- |
| <kbd>W</kbd> / <kbd>S</kbd> | Movimento avanti / indietro (asse X) |
| <kbd>A</kbd> / <kbd>D</kbd> | Movimento sinistra / destra (asse Y) |
| <kbd>Spazio</kbd> / <kbd>Shift</kbd> | Movimento su / giù (asse Z) |
| <kbd>O</kbd> / <kbd>P</kbd> | Rotazione ventosa (antioraria / oraria) |
| <kbd>E</kbd> / <kbd>Q</kbd> | Abilita / disabilita ventosa (aspirazione) |
| <kbd>+</kbd> / <kbd>-</kbd> | Incrementa / decrementa il rapporto di velocità |
| <kbd>H</kbd> | Ritorno immediato alla posizione di home |
| <kbd>F</kbd> | Acquisizione delle coordinate correnti ($x, y, z, r$) |
| <kbd>R</kbd> | Attiva / disattiva la modalità registrazione macro |
| <kbd>Backspace</kbd> | Cancella l'ultima riga di codice memorizzata (in registrazione) |
| <kbd>ESC</kbd> | Disattivazione ventosa, ritorno in home e chiusura programma |



## 4. Implementazione della funzione di registrazione (macro recorder)
La funzionalità di automazione permette di generare codice riproducibile attraverso i seguenti step logici:

1. **Inizio sessione:** L'utente attiva la registrazione premendo <kbd>R</kbd>.
2. **Campionamento dei punti:** Muovendo il robot con i controlli JOG, l'utente preme <kbd>F</kbd> nei punti desiderati. Il programma interroga il firmware tramite `get_pose()`, stampa a schermo le coordinate reali e genera la riga di comando `set_ptpcmd()` corrispondente.
3. **Azioni immediate:** Comandi come l'attivazione della ventosa (<kbd>E</kbd>/<kbd>Q</kbd>) o il ritorno in home (<kbd>H</kbd>) vengono aggiunti direttamente alla stringa del codice in fase di registrazione.
4. **Correzione degli errori:** Tramite il tasto <kbd>Backspace</kbd> è possibile eliminare l'ultima istruzione registrata in caso di manovre errate.
5. **Esportazione automatica:** Al termine (premendo nuovamente <kbd>R</kbd> o uscendo con <kbd>ESC</kbd>), la stringa viene stampata a terminale e copiata automaticamente negli appunti tramite `pyperclip`.



## 5. Conclusioni
L'applicazione sviluppata ha raggiunto gli obiettivi prefissati, fornendo un controllo manuale fluido grazie alla gestione dei comandi JOG associati al rilascio dei tasti. Il sistema di registrazione a coordinate puntuali (PTP) unito all'interazione con gli appunti di sistema ottimizza i processi di programmazione del braccio robotico, aggirando i limiti operativi dell'interfaccia grafica standard.
