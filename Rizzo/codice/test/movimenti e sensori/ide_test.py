from DobotEDU import *

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
    print(f"Connesso con successo a Magician su {port_name}")
    
    dobotEdu.magician.set_homecmd(port_name)
    dobotEdu.magician.set_ptpcmd(port_name,0,250,0,20,0,False,True)
    dobotEdu.magician.set_homecmd(port_name)


if __name__ == '__main__':
    main()