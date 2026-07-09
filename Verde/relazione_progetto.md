# Relazione tecnica di progetto: robotica FSL
Controllo remoto e automazione di Dobot Magician Lite tramite Python

## 1. Obiettivo del progetto
L'obiettivo principale del progetto è stato lo sviluppo di un software in Python per il controllo remoto e in tempo reale del braccio robotico **Dobot Magician Lite**. Utilizzando la tastiera del PC come interfaccia di input, si è riusciti a mappare i movimenti sui tre assi spaziali ($X, Y, Z$), a gestire l'effetto terminale (ventosa) e a implementare una funzione avanzata di registrazione e generazione di codice dei movimenti eseguiti.

## 2. Architettura hardware e ambiente di sviluppo
Il sistema è basato sull'interazione tra il PC (host) e il braccio robotico tramite connessione seriale.

* **Hardware:** Braccio robotico Dobot Magician Lite equipaggiato con modulo ventosa.
* **IDE di sviluppo:** Visual Studio Code (VS Code).
* **Linguaggio di programmazione:** Python 3.8.

### Nota sulla compatibilità del software
> [!IMPORTANT]
> **Criticità riscontrata:** Durante la fase di setup, l'utilizzo dell'ultima versione disponibile di Python ha causato conflitti di compatibilità con il software e i driver nativi.
> 
> **Soluzione:** È stato necessario effettuare un downgrade dell'ambiente d'esecuzione a **Python 3.8**, versione stabile e pienamente supportata dalla libreria e dall'ambiente **DobotEDU**.

Le librerie fondamentali importate e utilizzate nel codice sono state:
* `pydobot`: Per la comunicazione a basso livello e l'invio dei comandi di movimento al robot.
* `DobotEDU`: Per l'integrazione con l'ecosistema didattico del braccio.
* Librerie di sistema per l'ascolto degli input della tastiera in tempo reale (es. `pynput` o `keyboard`).

## 3. Mappatura dei comandi (interfaccia utente)
L'interazione con il robot avviene interamente da tastiera secondo lo schema seguente:

| Tasto | Azione / movimento |
| :---: | :--- |
| <kbd>W</kbd> / <kbd>S</kbd> | Movimento avanti / indietro (asse X) |
| <kbd>A</kbd> / <kbd>D</kbd> | Movimento sinistra / destra (asse Y) |
| <kbd>Spazio</kbd> / <kbd>Shift</kbd> | Movimento su / giù (asse Z) |
| <kbd>O</kbd> / <kbd>P</kbd> | Rotazione ventosa (antioraria / oraria) |
| <kbd>E</kbd> / <kbd>Q</kbd> | Abilita / disabilita ventosa (aspirazione) |
| <kbd>+</kbd> / <kbd>-</kbd> | Incrementa / decrementa velocità di spostamento |
| <kbd>H</kbd> | Ritorno alla posizione di home |
| <kbd>R</kbd> | Avvia / arresta registrazione movimenti |
| <kbd>F</kbd> | Registra e stampa a schermo le coordinate del punto in cui si trova il robot |
| <kbd>Backspace</kbd> | Elimina l'ultima riga registrata |
| <kbd>ESC</kbd> | Chiusura del programma e disconnessione |

## 4. Implementazione della funzione di registrazione (macro recorder)
Una delle funzionalità più avanzate del progetto è il sistema di **registrazione dei movimenti (<kbd>R</kbd>)**:

1. **Attivazione:** L'utente preme il tasto `R` per avviare il tracciamento in tempo reale.
2. **Cattura dei dati:** Ad ogni comando da tastiera, il programma muove il braccio e l'utente può salvare le coordinate spaziali o lo stato della ventosa in una struttura dati dinamica.
3. **Generazione del codice:** Al termine della sessione (ripremendo `R`), l'utente riceve in output un blocco di codice Python formattato.
4. **Esecuzione:** Il codice generato può essere inserito direttamente in uno script automatico per far ripetere al robot la sequenza registrata in autonomia.

## 5. Conclusioni
Il progetto ha dimostrato con successo come sia possibile bypassare le interfacce grafiche standard per creare un sistema di controllo personalizzato, efficiente e reattivo. La scelta della versione 3.8 ha permesso di stabilizzare il link con le librerie del Dobot, portando al completamento di tutti gli obiettivi prefissati.
