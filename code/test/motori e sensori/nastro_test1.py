import time
from DobotEDU import DobotEDU

dobotEdu = DobotEDU()

def main():
    res = dobotEdu.magician.search_dobot()
    if not res:
        print("Errore: Nessun robot trovato.")
        return

    port_name = res[0]["portName"]
    
    dobotEdu.magician.on_pause = lambda: None
    dobotEdu.magician.on_resume = lambda: None
    
    # Connessione al robot
    print(f"Tentativo di connessione a {port_name}...")
    dobotEdu.magician.connect_dobot(port_name=port_name)
    status_connessione = res[0]['status']
    
    

    # IMPORTANTE: Diamo un secondo al DobotLink per stabilizzare la sessione RPC
    time.sleep(1)
    print(status_connessione)
    dobotEdu.magician.set_homecmd(port_name)
    print(res)
    dobotEdu.magician.set_converyor(port_name=port_name,index=0,enable=True,speed=10000,is_queued=True)
    time.sleep(10)
    dobotEdu.magician.set_converyor(port_name=port_name,index=0,enable=False,speed=0,is_queued=True)
    

if __name__ == '__main__':
    main()