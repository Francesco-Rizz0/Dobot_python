Driver del Dobot Magician

Quando il robot viene collegato al computer, il sistema operativo deve riconoscerlo tramite il driver corretto. Nel caso del Dobot Magician possono comparire principalmente due famiglie di driver USB-seriale:

* Silicon Labs CP210x
* CH340 / CH341 (WCH)



Driver Silicon Labs (CP210x)

Questi driver sono usati quando il dispositivo monta un chip CP210x, prodotto da Silicon Labs. Il loro compito e convertire la comunicazione USB del computer in una comunicazione seriale interpretabile dal robot.



Driver CH340 / CH341 (WCH)

Questi driver sono invece associati ai chip CH340 o CH341, molto diffusi nei dispositivi seriali USB e nelle schede di controllo economiche o compatibili.



Differenza pratica tra i due

Dal punto di vista dell'utente finale, entrambi servono allo stesso scopo: permettere al sistema operativo di vedere il dispositivo come una porta seriale. La differenza reale dipende dal chip montato sull'hardware. Non si scelgono arbitrariamente: va installato il driver corrispondente all'interfaccia effettivamente presente sul dispositivo o sull'adattatore usato.



In sintesi:

Driver	     |  Produttore    |  Quando si usa

\---------------------------------------------------------------------------------------------

CP210x	     |  Silicon Labs  |  Se l'interfaccia USB-seriale del dispositivo usa chip CP210x

\---------------------------------------------------------------------------------------------

CH340/CH341  |  WCH           |   Se l'interfaccia USB-seriale usa chip CH340 o CH341

\---------------------------------------------------------------------------------------------



Come capire quale driver usare

In genere si può verificare:

* da Gestione dispositivi su Windows;
* leggendo il nome della periferica collegata;
* controllando l'identificativo hardware;
* consultando documentazione o serigrafia del modulo.



Se il dispositivo non viene riconosciuto correttamente oppure compare come periferica sconosciuta, il problema potrebbe essere proprio l'assenza del driver corretto.



Come aggiornare i driver

La procedura generale consiste nel:

* collegare il Dobot al PC;
* aprire Gestione dispositivi;
* individuare la periferica seriale o sconosciuta;
* verificare il nome del driver attuale;
* aggiornare il driver manualmente o reinstallarlo se necessario.


