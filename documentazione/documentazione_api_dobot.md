# 📘 Documentazione delle API DobotEDU

Questo documento raccoglie, descrive e analizza dettagliatamente tutte le funzioni della libreria `DobotEDU` utilizzate all'interno del codice di controllo per i robot **Dobot Magician** (Standard) e **Dobot Magician Lite**. Ciascuna funzione viene presentata con la propria firma hardware, l'elenco dei parametri e note pratiche sul comportamento in ambiente industriale/didattico.

---

## 🔌 1. Connessione e Inizializzazione

### `search_dobot(self)`
* **Descrizione**: Esegue una scansione a livello di sistema operativo alla ricerca di periferiche seriali USB compatibili con l'hardware Dobot.
* **Valore di ritorno**: Restituisce una lista di dizionari. Ciascun elemento contiene informazioni cruciali sulla porta rilevata:
  * `portName` (str): Il nome logico della porta (es. `"COM3"`, `"/dev/ttyUSB0"`).
  * `description` (str): Stringa descrittiva del chip seriale di comunicazione.
* **Note del programmatore**: Permette di discriminare via codice il modello di robot agganciato. Nel codice, le stringhe descrittive note utilizzate per il filtraggio logico e la validazione preventiva sono:
  * `"Silicon Labs CP210x USB to UART Bridge"` &rarr; Identifica univocamente un **Dobot Magician Standard**.
  * `"Dispositivo seriale USB"` &rarr; Identifica tipicamente un **Dobot Magician Lite**.

### `connect_dobot(self, port_name)`
* **Descrizione**: Apre la comunicazione seriale ed effettua l'handshake software iniziale con la scheda logica del robot sulla porta selezionata.
* **Parametri**:
  * `port_name` (str): La stringa esatta della porta COM (recuperata tramite `search_dobot`).
* **Valore di ritorno**: `True` se la connessione viene stabilita con successo, `False` in caso contrario o se la porta è già occupata da un altro processo.

### `disconnect_dobot(self, port_name)`
* **Descrizione**: Interrompe in modo pulito il socket di comunicazione e rilascia la risorsa seriale sul PC.
* **Parametri**:
  * `port_name` (str): La porta COM da chiudere.

---

## 📊 2. Monitoraggio e Stato

### `get_pose(self, port_name)`
* **Descrizione**: Interroga il firmware per ricevere in tempo reale le coordinate correnti e lo stato spaziale dell'end-effector del robot.
* **Parametri**:
  * `port_name` (str): La porta COM del robot attivo.
* **Valore di ritorno**: Restituisce un dizionario contenente le chiavi cartesiane e angolari:
  * `'x'` (float): Posizione asse X in millimetri (avanti/dietro rispetto alla base).
  * `'y'` (float): Posizione asse Y in millimetri (sinistra/destra).
  * `'z'` (float): Posizione asse Z in millimetri (altezza/elevazione).
  * `'r'` (float): Angolo di rotazione dell'end-effector (asse R) espresso in gradi sessagesimali.
  * `'l'` (float): Posizione lineare assoluta della base del robot lungo l'asse aggiuntivo della rotaia espresso in millimetri.

### `clear_allalarms_state(self, port_name)`
* **Descrizione**: Invia un comando di reset software che cancella i registri di errore e allarme attivi nel firmware del Dobot.
* **Parametri**:
  * `port_name` (str): La porta COM del robot attivo.
* **Note del programmatore**: Questa funzione è di fondamentale importanza prima di eseguire l'Homing o per sbloccare il robot dopo un urto, un superamento dei limiti di giunto meccanico (joint limit) o la pressione di un finecorsa elettrico. Se gli allarmi non vengono azzerati, il robot rifiuta qualsiasi comando successivo di movimento.

---

## 🕹️ 3. Controllo Manuale e Dinamica

### `set_jogcommon_params(self, port_name, velocity_ratio, acceleration_ratio)`
* **Descrizione**: Configura i parametri generali di dinamica (velocità ed accelerazione massima scalata) per i movimenti eseguiti in modalità manuale JOG.
* **Parametri**:
  * `port_name` (str): La porta COM attiva.
  * `velocity_ratio` (int/float): Percentuale della velocità massima consentita dal firmware (valore valido da `1` a `100`).
  * `acceleration_ratio` (int/float): Percentuale dell'accelerazione massima consentita dal firmware (valore valido da `1` a `100`).

### `set_jogcmd(self, port_name, is_joint, cmd, is_queued)`
* **Descrizione**: Avvia o arresta un movimento continuo lungo un asse cartesiano o un giunto specifico.
* **Parametri**:
  * `port_name` (str): La porta COM attiva.
  * `is_joint` (bool): 
    * `False`: Utilizza il sistema di coordinate **Cartesiane** (X, Y, Z, R).
    * `True`: Utilizza il sistema di coordinate dei **Giunti fisici** del braccio (Joints J1, J2, J3, J4).
  * `cmd` (int): L'identificativo numerico della direzione. Costanti standard associate:
    * `0` (`JOG_IDLE`): Arresta immediatamente il movimento.
    * `1` (`JOG_X_PLUS`) / `2` (`JOG_X_MINUS`): Movimento X.
    * `3` (`JOG_Y_PLUS`) / `4` (`JOG_Y_MINUS`): Movimento Y.
    * `5` (`JOG_Z_PLUS`) / `6` (`JOG_Z_MINUS`): Movimento Z.
    * `7` (`JOG_R_PLUS`) / `8` (`JOG_R_MINUS`): Rotazione dell'end-effector R.
  * `is_queued` (bool): Definisce se inserire l'istruzione nella coda FIFO hardware (`True`) o eseguirla istantaneamente scavalcando la coda (`False`). Nel controllo manuale JOG real-time viene tassativamente impostata a `False` per garantire reattività al rilascio del tasto.

---

## 🏠 4. Calibrazione e Posizionamento Automatico

### `set_homecmd(self, port_name)`
* **Descrizione**: Avvia il ciclo hardware nativo di azzeramento (Homing) per calibrare i motori del braccio robotico rispetto ai sensori fisici.
* **Parametri**:
  * `port_name` (str): La porta COM attiva.
* **Note del programmatore**: Il metodo non accetta parametri di coordinate opzionali sovrascritti nell'implementazione standard per evitare conflitti con la memoria del firmware. Riporta il braccio alle coordinate spaziali predefinite impresse nella ROM della scheda logica.

### `set_ptpcommon_params(self, port_name, velocity_ratio, acceleration_ratio)`
* **Descrizione**: Configura la velocità ed accelerazione applicate alle traiettorie punto-punto (PTP) utilizzate per gli spostamenti lineari e della rotaia.
* **Parametri**: Identici a `set_jogcommon_params` (valori percentuali da `1` a `100`).

### `set_device_withl(self, port_name, enable)`
* **Descrizione**: Configura la logica del firmware del robot informandolo sulla presenza fisica dell'asse lineare aggiuntivo (Rotaia di scorrimento).
* **Parametri**:
  * `port_name` (str): La porta COM attiva.
  * `enable` (bool): `True` per attivare la gestione software dell'asse `L`, `False` per disabilitarla.

### `set_ptplcmd(self, port_name, ptp_mode, x, y, z, r, l, is_queued)` *o* `set_ptpwithlcmd(...)`
* **Descrizione**: Esegue una traiettoria coordinata e interpolata che include lo spostamento della base lungo la rotaia lineare senza modificare (o modificando contemporaneamente) la posa cartesiana del braccio.
* **Parametri**:
  * `port_name` (str): La porta COM attiva.
  * `ptp_mode` (int): Specifica la tipologia di traiettoria. Il valore `1` corrisponde alla modalità **MOVL (Move Linear)**: calcola l'interpolazione lineare perfetta nello spazio cartesiano.
  * `x`, `y`, `z`, `r` (float): Coordinate cartesiane target. Nel codice vengono passati i valori attuali restituiti da `get_pose` per isolare il movimento della sola rotaia.
  * `l` (float): Coordinata millimetrica target della base sulla rotaia (campo operativo standard: `0.0` - `1000.0` mm).
  * `is_queued` (bool): `False` per esecuzione immediata dello spostamento.

---

## 🛤️ 5. Controllo Periferiche Esterne (Nastro e Ventosa)

### `set_converyor(self, port_name, index, enable, speed, is_queued=False)`
* **Descrizione**: Controlla lo stato elettrico e la velocità di rotazione del motore passo-passo ausiliario accoppiato al nastro trasportatore.
* **Parametri**:
  * `port_name` (str): La porta COM attiva.
  * `index` (int): L'identificativo dell'interfaccia/canale del motore sulla scheda del robot (il nastro standard si collega all'interfaccia contrassegnata con l'indice `0`).
  * `enable` (bool): `True` per alimentare le bobine del motore (attivazione), `False` per togliere tensione e arrestare l'albero motore.
  * `speed` (int): Velocità di avanzamento definita in passi/impulsi al secondo. Accetta valori discreti compresi nell'intervallo **da `-10000` a `+10000`**. Valori positivi muovono il nastro in avanti, valori negativi invertono il senso di marcia.
  * `is_queued` (bool): Deve essere impostato su **`True`** (inserito in coda) per garantire la sincronizzazione dei comandi del motore ausiliario con il flusso principale di controllo della CPU hardware del Dobot.

### `set_endeffector_suctioncup(self, port_name, enable, on, is_queued)`
* **Descrizione**: Attua lo stato pneumatico del compressore/ventosa di campionamento montato sulla punta del braccio (end-effector).
* **Parametri**:
  * `port_name` (str): La porta COM attiva.
  * `enable` (bool): Controlla l'attivazione elettrica del modulo attuatore (`True` = Acceso/Alimentato, `False` = Totalmente spento/Isolato).
  * `on` (bool): Regola lo stato della valvola pneumatica interna:
    * `True`: Genera la depressione (aspirazione/vuoto), permettendo alla ventosa di afferrare e trattenere saldamente un oggetto.
    * `False`: Interrompe l'aspirazione e inverte brevemente il flusso d'aria (soffiaggio di rilascio) per staccare istantaneamente l'oggetto manipolato.
  * `is_queued` (bool): Impostato su `False` per attivare/disattivare la ventosa in tempo reale.
