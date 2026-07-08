import time
from DobotEDU import DobotEDU  

dobotEdu = DobotEDU()  

# Configurazione dei callback per il Magician standard
def finto_on_pause(): pass
def finto_on_resume(): pass

dobotEdu.magician.on_pause = finto_on_pause
dobotEdu.magician.on_resume = finto_on_resume

def main():
    # Ricerca delle porte per il Magician standard
    res = dobotEdu.magician.search_dobot() 
    
    print("Porte trovate:", res)
    
    if not res:
        print("Errore: Nessun robot trovato. Controlla il cavo USB e l'alimentazione.")
        return

    port_name = res[0]["portName"]  
    
    # Connessione al Magician standard
    dobotEdu.magician.connect_dobot(port_name=port_name)  
    res = dobotEdu.magician.search_dobot() 
    status_connessione = res[0]['status'] 
    print(status_connessione)
   
    #dobotEdu.magician.set_homecmd(port_name)
    dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=230, y=50, z=0, r=20)
    # index=1 (Stepper 1), enable=True, speed=10000 (valore tipico per i motori del nastro)
    dobotEdu.magician.set_converyor(port_name=port_name,index=0,enable=True,speed=10000,is_queued=True)
    time.sleep(5)
    dobotEdu.magician.set_converyor(port_name=port_name,index=0,enable=False,speed=0,is_queued = True)
    


if __name__ == '__main__':
    main()