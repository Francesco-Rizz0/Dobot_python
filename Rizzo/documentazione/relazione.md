# Relazione corso POC "One & Two"
## Presentazione
In questo corso abbiamo affrontato la programmazione dei robot Dobot Magician e Magician Lite e dei loro accessori con il linguaggio di programmazzione Python. Riporto qui il sommario dei vari progetti, della loro implementazione e dei problemi riscontrati.
## 1. Interfacciare i dispositivi con VSCode
Il primo obbiettivo che ci siamo posti è stato di riuscire ad interfacciare i dispositivi Dobot con VSCode, senza dover usare Dobot Lab IDE. 
### Implementazione
Per farlo, abbiamo dovuto installare Python e la libreria DobotEDU. Una volta fatto questo, basandoci sulla documentazione presente all'interno dell'IDE Dobot Lab abbiamo potuto interfacciarci e creare programmi per i modelli Magician e Magician Lite.
### Problemi riscontrati
* Compatibilità: inizialmente avevamo installato Python versione 3.12, ma abbiamo scoperto che a causa di alcune dependencies le versioni di Python superiori alla 3.10 non sono campitibili con la libreria DobotEDU. Per risolvere questo problema, abbiamo disinstallato Python, facendo poi il downgrade alla versione 3.8;
* Connettività: a volte, il Dobot Magician si collegava correttamente al programma, ma non eseguiva i comandi. Per risolvere questo problema, bisogna semplicemente spegnere il Magician, riaccenderlo e portarlo alla Home tenendo premuto il tasto Key per alcuni secondi e poi rilasciandolo.
