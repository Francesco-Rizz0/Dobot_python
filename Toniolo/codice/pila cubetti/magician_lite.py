import websocket
import json
import time
# from DobotEDU import *

# Porta simulatore:   VSP1
# Porta Robot :       COMx

WS_URL = "ws://localhost:9090"
port = ""
ws = None  # Inizializziamo a None che è più corretto per gli oggetti

def send(method, params):
    # Usa il ws globale senza che venga passato come parametro
    cmd = {"id": 1, "jsonrpc": "2.0", "method": method, "params": params}
    ws.send(json.dumps(cmd))
    return json.loads(ws.recv())

def move(mode, x, y, z, r):
    #global port
    r = send("dobotlink.MagicianLite.SetPTPCmd", {
        "portName": port,
        "ptpMode": mode,
        "x": x, "y": y, "z": z, "r": r,
        "isQueued": True,
        "isWaitForFinish": True,
        "timeout": 90000
    })
    print("Risposta move: ", r)

def setHome():
    global port
    send("dobotlink.MagicianLite.SetHOMECmd", {
        "portName": port,
        "isQueued": True,
        "isWaitForFinish": True,
        "timeout": 90000
    })

def setVetosa (enable):
    send("dobotlink.MagicianLite.SetEndEffectorSuctionCup", {
        "portName": port,
        "enable": enable,
        "on": enable,
        "isQueued": True,
        "isWaitForFinish": True,
        "timeout": 90000
    })


def connect(isSimulator):
    global ws, port  # FONDAMENTALE: dice a Python di modificare le variabili globali in alto
    
    ws = websocket.create_connection(WS_URL, timeout=30)
    
    if isSimulator:
        print("stai usando il simulatore")
        port = "VSP1"
        send("dobotlink.MagicianLite.QueuedCmdStart", {"portName": "VSP1"})
    else:
        # Se scommenti DobotEDU, ricordati di scommentare anche l'import in alto!
        dobotEdu = DobotEDU()
        
        # --- AGGIRAMENTO BUG DOBOT SENZA ACCOUNT ---
        def finto_on_pause(): pass
        def finto_on_resume(): pass

        dobotEdu.m_lite.on_pause = finto_on_pause
        dobotEdu.m_lite.on_resume = finto_on_resume

        res = dobotEdu.m_lite.search_dobot()  
        print("Porte trovate:", res)
        if not res:
            print("Errore: Nessun robot trovato. Controlla il cavo USB.")
            return "NO_COM"

        port = res[0]["portName"]  

        # Connessione tramite DobotLink via WebSocket per il braccio fisico
        send("dobotlink.MagicianLite.ConnectDobot", {"portName": port})  
    
    # Avvia la coda in automatico dopo la connessione (valido per entrambi)
    send("dobotlink.MagicianLite.QueuedCmdStart", {"portName": port})
    
    return port # CORRETTO: tolta la 'ù' finale

def disconnect(isSimulator=True):
    global ws, port # Accede alle variabili globali
    
    if ws:
        # Se stavi usando il robot fisico, dice a DobotLink di liberare la porta COM
        if not isSimulator and port and port != "VSP1":
            try:
                send("dobotlink.MagicianLite.DisconnectDobot", {"portName": port})
                print(f"🔌 Porta {port} rilasciata correttamente.")
            except Exception:
                pass # Evita che il programma si blocchi se il robot era già staccato
        
        # Chiude effettivamente la connessione WebSocket
        ws.close()
        print("- Connessione WebSocket chiusa. -")