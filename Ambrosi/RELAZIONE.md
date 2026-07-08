Nella cartella "FINALS" si trovano i programmi finali perfettamente funzionanti, nella cartella "BETAS" si trovano i programmi funzionanti in parte e senza alcune accortezze finali.
I file presenti nella cartella "dobot.zip" sono stati caricati su gemini per istruirla all'utilizzo della libreria DobotEDU.

# RELAZIONE
Gli obbiettivi raggiunti sono stati : 1) creazione di un "magazzino" di cubetti colorati.
                                      2) creazione di una gui di comandi per muovere il dobot magician.
E' stato attuato un programma per ogni obbiettivo.

# 1) MAGAZZINO
Per attuare questo primo progetto abbiamo collegato un sensore, una telecamera, un nastro trasportatore e la suction cup al dobot magician.
Una volta messi sopra al nastro dei cubetti colorati si fa partire il programma, questo fa partire il nastro fino a che un cubetto non attiva il sensore che ferma il nastro.
Successivamente il robot preleva il cubetto, lo porta davanti alla telecamera che tramite un IA della libreria opencv per riconoscerne il colore.
In base a quello lo mette nella pila rossa, verde blu o quella degli "scarti".
Il programma si ferma da solo dopo che il sensore non rileva cubetti per 20 secondi.

# 2) GUI DI MOVIMENTO
Il progetto è iniziato per creare una gui per usare il robot tramite un joystick, tuttavia si muoveva solo su un piano, per questo abbiamo rivisto i comandi per muoverlo in ogni direzione, asse z compreso, rendendo la gui simile a dobot lab anche se poi optato per una più user friendly ed aggiunto uno slider per la velocità del robot.
Successivamente abbiamo aggiunto 2 pulsanti per attivare e disattivare la suction cup, ed insieme a questo abbiamo introdotto uno slider che permette di muovere il nastro trasportatore avanti/indietro in base alla velocità dello slider (esempio velocità 100 verso destra o velocità 800 verso sinistra).
Arrivati a questo risultato abbiamo posizionato il robot sopra alla rotaia ed introdotto un ulteriore slider che muove la rotaia posizionando il robot nell'equivalente posizione dell'indicatore dello slider, ed aggiunto un altro slider per la sua velocità.
Abbiamo aggiunto anche dei pulsanti HOME per riportare la rotaia ed il robot nella loro posizione di home, una finestra che mostra le sue coordinate ed un controllo per riconoscere se il robot collegato sia un dobot magician o dobot lite.
