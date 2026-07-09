# Relazione Tecnica: Sperimentazione, Programmazione e Integrazione con Robotica DOBOT

## 1. Introduzione

In questo documento viene analizzato il percorso sperimentale e applicativo della durata di **12 giorni**, incentrato sulla robotica industriale e sull'automazione software. Attraverso l'impiego del **DOBOT Magician Lite** e del linguaggio **Python**, l'attività ha permesso di esplorare soluzioni ingegneristiche che spaziano dalla manipolazione elementare di oggetti fino all'integrazione di moduli di intelligenza artificiale, sistemi di calibrazione spaziale, stampa 3D e logiche multimediali sincronizzate.

Una parte significativa del progetto è stata dedicata alla collaborazione in laboratorio, al debugging assistito e all'ottimizzazione continua del codice, culminando nella creazione di un **Action Controller** per il pilotaggio manuale e la generazione automatizzata di script.

---

# 2. Configurazione dell'Interfaccia di Controllo (Action Controller)

Per abilitare l'interazione diretta uomo-macchina e registrare routine di movimento riutilizzabili, è stata sviluppata un'interfaccia di comando basata su input da tastiera.

## Controllo Assiale e Dinamico

| Tasto | Funzione |
|-------|----------|
| **W / A / S / D** | Spostamento del braccio robotico lungo gli assi cartesiani del piano di lavoro |
| **Spazio** | Movimento verso l'alto (asse Z) |
| **Shift** | Movimento verso il basso (asse Z) |
| **+ / -** | Regolazione dinamica della velocità dei motori |
| **H** | Ritorno alla posizione Home (calibrazione iniziale) |

## Gestione della Ventosa (End-Effector)

| Tasto | Funzione |
|-------|----------|
| **E** | Attivazione della ventosa (presa) |
| **Q** | Disattivazione della ventosa (rilascio) |
| **O** | Rotazione antioraria della ventosa |
| **P** | Rotazione oraria della ventosa |

## Scripting e Autocompilazione

| Tasto | Funzione |
|-------|----------|
| **F** | Visualizza e registra le coordinate correnti |
| **R** | Avvia/termina la registrazione ed esporta automaticamente uno script Python |
| **Backspace** | Elimina l'ultima istruzione registrata (Undo) |
| **ESC** | Arresto sicuro del programma |

---

# 3. Diario di Bordo delle Attività

## Giorno 1 – Introduzione e Configurazione Hardware

Fase iniziale dedicata alla predisposizione della postazione di lavoro con il **DOBOT Magician Lite**. Studio della documentazione, configurazione dell'ambiente Python ed esecuzione dei primi script di test per verificare i movimenti fondamentali del braccio robotico.

---

## Giorno 2 – Sviluppo della Logica "Pick and Place"

Implementazione di un algoritmo per la manipolazione automatica dei cubetti. Il robot è stato programmato per eseguire cicli continui di impilamento e disimpilamento, calibrando precisione e affidabilità della ventosa.

---

## Giorno 3 – Miglioramento e Ottimizzazione

Revisione del codice sviluppato il giorno precedente. Sono state migliorate le traiettorie di movimento e ottimizzati i tempi di attivazione della ventosa, aumentando fluidità e precisione.

---

## Giorno 4 – Supporto Tecnico e Peer Debugging

Giornata dedicata alla collaborazione con un compagno di corso. È stato fornito supporto nell'analisi logica del software e nella risoluzione di errori tramite attività di debugging condiviso.

---

## Giorno 5 – Integrazione Hardware su Asse Lineare

Installazione del robot su una rotaia motorizzata per ampliare l'area operativa. Configurazione della cinematica combinata e montaggio di una pinza meccanica per movimentare una bottiglia lungo la guida lineare.

---

## Giorno 6 – Visione Artificiale e OCR

Introduzione ai sistemi di intelligenza artificiale applicati alla robotica. Configurazione di una telecamera e sviluppo di script Python basati su **OCR (Optical Character Recognition)** per il riconoscimento di testo.

---

## Giorno 7 – Calibrazione delle Coordinate

Sviluppo del sistema di conversione tra coordinate in pixel e coordinate cartesiane reali. Attraverso trasformazioni geometriche il robot è stato in grado di raggiungere automaticamente gli oggetti individuati dalla telecamera.

---

## Giorno 8 – Stampa 3D

Trasformazione del DOBOT in una stampante 3D mediante il montaggio dell'estrusore. Taratura del piano di stampa ed esecuzione di prove per verificare precisione e continuità dei movimenti.

---

## Giorno 9 – Sviluppo dell'Action Controller

Progettazione dell'applicazione per il controllo manuale del robot tramite tastiera. Il software è stato sviluppato per intercettare gli input dell'utente e convertirli automaticamente in istruzioni Python salvate su file.

---

## Giorno 10 – Ottimizzazione del Software

Sessione dedicata al refactoring del codice. Sono state migliorate l'organizzazione del progetto, la leggibilità delle funzioni e le prestazioni complessive dell'applicazione.

---

## Giorno 11 – Testing e Debugging Finale

Collaudo completo dell'Action Controller. Sono stati verificati:

- correttezza della registrazione delle coordinate;
- funzionamento del comando **Undo**;
- generazione automatica dello script Python;
- corrispondenza tra movimenti manuali ed esecuzione automatica.

---

## Giorno 12 – Documentazione e Conclusione

Conclusione delle attività di laboratorio con verifica finale del progetto, redazione della documentazione tecnica e confronto conclusivo con i supervisori e il team di lavoro.

---

# 4. Conclusioni Finali

L'esperienza svolta con il **DOBOT Magician Lite** ha evidenziato l'importanza dell'integrazione tra hardware industriale e sviluppo software in **Python**.

Durante il progetto sono state acquisite competenze in numerosi ambiti:

- manipolazione robotica (*pick and place*);
- ottimizzazione del codice;
- debugging e lavoro collaborativo;
- integrazione con assi lineari;
- visione artificiale e OCR;
- trasformazioni geometriche e calibrazione spaziale;
- stampa 3D;
- progettazione di interfacce di controllo.

Particolare rilevanza ha assunto lo sviluppo dell'**Action Controller**, progettato e perfezionato tra il **Giorno 9** e il **Giorno 11**. Lo strumento consente di controllare manualmente il robot, registrare le traiettorie ed esportare automaticamente uno script Python riutilizzabile, semplificando notevolmente la programmazione delle operazioni.

Nel complesso, il percorso si è rivelato estremamente formativo, permettendo di consolidare competenze pratiche nella robotica industriale, nello sviluppo software e nell'integrazione tra sistemi hardware e algoritmi di automazione.
