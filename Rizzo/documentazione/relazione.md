# Relazione corso POC "One & Two"
## Presentazione
In questo corso abbiamo affrontato la programmazione dei robot Dobot Magician e Magician Lite e dei loro accessori con il linguaggio di programmazzione Python. Riporto qui il sommario dei vari progetti, della loro implementazione e dei problemi riscontrati.
## 1. Interfacciare i dispositivi con VSCode
Il primo obiettivo che ci siamo posti è stato di riuscire ad interfacciare i dispositivi Dobot con VSCode, senza dover usare Dobot Lab IDE. 
### Implementazione
Per farlo, abbiamo dovuto installare Python e la libreria DobotEDU. Una volta fatto questo, basandoci sulla documentazione presente all'interno dell'IDE Dobot Lab abbiamo potuto interfacciarci e creare programmi per i modelli Magician e Magician Lite.
### Problemi riscontrati
* Compatibilità: inizialmente avevamo installato Python versione 3.12, ma abbiamo scoperto che a causa di alcune dependencies le versioni di Python superiori alla 3.10 non sono campitibili con la libreria DobotEDU. Per risolvere questo problema, abbiamo disinstallato Python, facendo poi il downgrade alla versione 3.8;
* Connettività: a volte, il Dobot Magician si collegava correttamente al programma, ma non eseguiva i comandi. Per risolvere questo problema, bisogna semplicemente spegnere il Magician, riaccenderlo e portarlo alla Home tenendo premuto il tasto Key per alcuni secondi e poi rilasciandolo.
## 2. Implementare la programmazione del nastro trasportatore
Il secondo obiettivo è stato quello di riuscire a controllare il nastro trasportatore da codice.
### Implementazione
Dopo diversi confronti con Gemini, abbiamo scoperto (uso del verbo giustificato dalla poca documentazione fornita dall'azienda produttrice) che per controllare il nastro è necessario usare la funzione `set_converyor()` (da notare peraltro l'errore di battitura, dove "converyor" sarebbe dovuto essere "conveyor").
### Problemi riscontrati
* Problemi con il nastro: inizialmente, data la poca documentazione, abbiamo avuto molti grattacapi a riuscire a far muovere il nastro per la prima volta. Per configurare correttamente il nastro, il suo cavo connettore deve essere collegato alla porta Stepper1 del Magician, e la funzione `set_converyor()` configurata in questo modo:
  * `index`: deve essere uguale a 0;
  * `is_queued`: deve essere uguale a True.
* Problemi di mobilità: inizialmente il nastro si muoveva pianissimo in entrambe le direzioni. Abbiamo scoperto che il problema era la velocità del nastro impostata dal paramentro `speed` della funzione `set_converyor()`. Avevamo impostato questo paramentro a 50 come prova, ma abbiamo poi scoperto che il nastro può essere settato a velocità che vanno da -10.000 a +10.000. Settandop il parametro a velocità maggiori, abbiamo risolto il problema.
## 3. Implementazione sensore di presenza a raggi infrarossi e riconoscimento del colore con telecamera Dobot
