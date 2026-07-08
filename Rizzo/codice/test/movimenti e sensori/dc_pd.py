import time
from DobotEDU import DobotEDU  

dobotEdu = DobotEDU()  

# Configurazione dei callback per il Magician standard
def finto_on_pause(): pass
def finto_on_resume(): pass

dobotEdu.magician.on_pause = finto_on_pause
dobotEdu.magician.on_resume = finto_on_resume

def main():
    # 1. Ricerca delle porte
    res = dobotEdu.magician.search_dobot() 
    print("Porte trovate:", res)
    
    if not res:
        print("Errore: Nessun robot trovato. Controlla il cavo USB e l'alimentazione.")
        return

    port_name = res[0]["portName"]  
    
    # 2. Connessione al Magician standard
    print(f"Tentativo di connessione su: {port_name}...")
    dobotEdu.magician.connect_dobot(port_name=port_name)  
    
    # IMPORTANTE: Dai tempo al WebSocket di DobotLink di stabilire la connessione reale
    time.sleep(2) 
    
    # Verifica lo stato post-connessione
    res_check = dobotEdu.magician.search_dobot() 
    status_connessione = res_check[0]['status'] 
    print("Stato connessione attuale:", status_connessione)
   
    # 3. Movimento PTP
    print("Inviando comando PTP...")
    dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=230, y=50, z=0, r=20)
    
    # Attendi che il movimento termini prima di far partire il nastro (opzionale ma consigliato)
    #time.sleep(2) 

    # 4. Controllo del Conveyor (Nastro trasportatore)
    # Correggi 'any' con l'ID del motore (0 di solito) e verifica se la funzione si chiama 'set_converyor' o 'set_conveyor'
    print("Attivazione nastro trasportatore...")
    try:
        # Usiamo 0 al posto di any. Il typo 'set_converyor' è presente in alcune versioni dell'SDK Dobot
        status_conveyor = dobotEdu.magician.set_converyor(port_name, motor_id=0, IsEnable=True, Speed=50, IsForward=False)
        print("Stato conveyor:", status_conveyor)
    except AttributeError:
        # Se la tua versione ha corretto il typo, userà 'set_conveyor'
        status_conveyor = dobotEdu.magician.set_conveyor(port_name, motor_id=0, IsEnable=True, Speed=50, IsForward=False)
        print("Stato conveyor:", status_conveyor)

    # Lascia girare il nastro per qualche secondo prima che lo script termini
    time.sleep(5)
    
    # Opzionale: spegni il nastro alla fine
    try:
        dobotEdu.magician.set_converyor(port_name, 0, False, 0, False)
    except:
        dobotEdu.magician.set_conveyor(port_name, 0, False, 0, False)

if __name__ == '__main__':
    main()