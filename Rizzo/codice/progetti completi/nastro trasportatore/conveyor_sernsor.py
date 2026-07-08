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

    #posizioni carico-scarico
    carico = {"x": 235,"y": -123, "z":-30.77 }
    scarico = {"x": 265,"y": 154,"z": -29.45}

    #setup sensore infrarossi
    dobotEdu.magician.set_infrared_sensor(port_name=port_name,port=2,enable=True,version=1,is_queued=False)
    continuare = True
    conta = 0
   
    #posizione sicura
    dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=230, y=50, z=0, r=20)

    while conta < 4:
        #inizio nastro
        dobotEdu.magician.set_converyor(port_name=port_name,index=0,enable=True,speed=10000,is_queued=True)
        while continuare:
            #lettura status sensore
            infrared_status = dobotEdu.magician.get_infrared_sensor(port_name=port_name,port=2,is_queued=False)
            if(infrared_status["status"]==1):
                continuare = False
        #fermo nastro
        dobotEdu.magician.set_converyor(port_name=port_name,index=0,enable=False,speed=0,is_queued = True)
        #muovo braccio al cubetto e lo prelevo
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=carico["x"], y=carico["y"], z=carico["z"], r=20)
        dobotEdu.magician.set_endeffector_suctioncup(port_name=port_name,enable=True,on=True)
        time.sleep(1)
        #mi alzo per evitare contatti e mi muovo verso la posizione di scarico
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=carico["x"], y=carico["y"], z=carico["z"]+40, r=20)
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=scarico["x"], y=scarico["y"], z=scarico["z"]+40, r=20)
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=scarico["x"], y=scarico["y"], z=scarico["z"], r=20)
        #rilascio il cubetto
        dobotEdu.magician.set_endeffector_suctioncup(port_name=port_name,enable=False,on=False)
        time.sleep(1)
        #posizione di sicurezza
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=scarico["x"], y=scarico["y"], z=scarico["z"]+40, r=20)
        continuare = True
        conta += 1

    
    


if __name__ == '__main__':
    main()