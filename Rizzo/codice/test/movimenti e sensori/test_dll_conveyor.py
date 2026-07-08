import time
import DobotDllType as dType

# Definiamo la porta COM a cui è connesso il Dobot (es. COM3 su Windows, /dev/ttyUSB0 su Linux)
CON_STR = "COM3"

# Carica le API del Dobot
api = dType.load()

# Tenta la connessione con il braccio robotico
state = dType.ConnectDobot(api, CON_STR, 115200)[0]
print("Stato connessione:", "Connesso" if state == dType.DobotConnect.DobotConnect_NoError else "Errore di connessione")

if state == dType.DobotConnect.DobotConnect_NoError:
    # 1. Pulizia della coda dei comandi precedente e avvio di una nuova sessione
    dType.SetQueuedCmdClear(api)
    dType.SetQueuedCmdStartExec(api)

    print("Avvio del nastro trasportatore...")
    
    # 2. Configurazione del motore esterno (Nastro trasportatore)
    # Creiamo l'istanza della struttura dati EMotor
    emotor = dType.EMotor()
    
    # PARAMETRI DEL MOTORE:
    # index: definisce la porta a cui è collegato il nastro (0 = Porta Stepper 1, 1 = Porta Stepper 2)
    emotor.index = 0          
    # isEnabled: 1 per attivare il motore, 0 per fermarlo
    emotor.isEnabled = 1      
    # speed: velocità in impulsi al secondo (valori positivi o negativi cambiano la direzione)
    emotor.speed = 10000      

    # Invia il comando per far partire il nastro (isQueued=1 inserisce il comando in coda)
    dType.SetEMotor(api, emotor, isQueued=1)

    # Lasciamo girare il nastro trasportatore per 5 secondi
    print("Il nastro rimarrà in funzione per 5 secondi.")
    time.sleep(5)

    print("Fermata del nastro trasportatore...")
    
    # 3. Spegnimento del motore (per fermare il nastro)
    emotor_stop = dType.EMotor()
    emotor_stop.index = 0
    emotor_stop.isEnabled = 0  # Disabilita il motore
    emotor_stop.speed = 0      # Velocità a zero
    
    dType.SetEMotor(api, emotor_stop, isQueued=1)

    # Aspetta un momento per assicurarsi che l'ultimo comando venga elaborato prima di chiudere
    time.sleep(1)

    # 4. Ferma l'esecuzione della coda dei comandi e disconnetti il Dobot
    dType.SetQueuedCmdStopExec(api)
    dType.DisconnectDobot(api)
    print("Dobot disconnesso correttamente.")
else:
    print("Impossibile avviare il codice: Dobot non rilevato sulla porta specificata.")