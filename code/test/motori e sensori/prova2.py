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
    
    # Movimento iniziale di sicurezza
    dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=230, y=50, z=0, r=20)
    time.sleep(2) 

    y = 28

    #dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=332-19*3, y=y, z=-42, r=0)
    # Comando ventosa specifico per Magician standard
    dobotEdu.magician.set_endeffector_suctioncup(port_name, enable=True, on=True)
    time.sleep(5) 
            
    #dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=332, y=y, z=-42+12, r=0)
    dobotEdu.magician.set_endeffector_suctioncup(port_name, enable=False, on=False)
    time.sleep(0.5)
    dobotEdu.magician.disconnect_dobot()

if __name__ == '__main__':
    main()