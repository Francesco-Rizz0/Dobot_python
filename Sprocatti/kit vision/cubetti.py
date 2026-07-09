import time
from DobotEDU import DobotEDU  


# Inizializzazione della classe
dobotEdu = DobotEDU()  


# --- AGGIRAMENTO BUG DOBOT SENZA ACCOUNT ---
def finto_on_pause(): pass
def finto_on_resume(): pass


dobotEdu.m_lite.on_pause = finto_on_pause
dobotEdu.m_lite.on_resume = finto_on_resume
# --------------------------------------------


def main():
    # Cerca la porta
    res = dobotEdu.m_lite.search_dobot()  
    print("Porte trovate:", res)
    
    if not res:
        print("Errore: Nessun robot trovato. Controlla il cavo USB.")
        return

    port_name = res[0]["portName"]  
    
    # Connessione
    dobotEdu.m_lite.connect_dobot(port_name=port_name)  
    print(f"Connesso con successo a Magician Lite su {port_name}")
    res = dobotEdu.m_lite.search_dobot() 
    connessione = res[0]["status"] 
    
    # 2. Movimento di test iniziale
    print("Invio movimento di test...")
    print("Lo stato di connessione è: "+connessione)
    dobotEdu.m_lite.set_ptpcmd(port_name, ptp_mode=0, x=230, y=50, z=0, r=20)
    time.sleep(3) # Tempo per completare il movimento


    # --- LOGICA MOVIMENTO VENTOSA ---
    y = 32


    # Primo blocco di movimenti
    for j in range(4):
        for i in range(3):
            dobotEdu.m_lite.set_ptpcmd(port_name, ptp_mode=0, x=273+19*i, y=y, z=-40, r=0)
            dobotEdu.m_lite.set_endeffector_suctioncup(port_name, enable=True, on=True)
            time.sleep(0.5)
           
            dobotEdu.m_lite.set_ptpcmd(port_name, ptp_mode=0, x=332.5, y=y, z=-40+11*(i+1), r=0)
            dobotEdu.m_lite.set_endeffector_suctioncup(port_name, enable=False, on=False)
            time.sleep(0.5)
        y = y - 20


    y = 32


    # Secondo blocco di movimenti
    for j in range(4):
        for i in range(3):
            dobotEdu.m_lite.set_ptpcmd(port_name, ptp_mode=0, x=332.5, y=y, z=-12-11*i, r=0)
            dobotEdu.m_lite.set_endeffector_suctioncup(port_name, enable=True, on=True)
            time.sleep(0.5)
           
            dobotEdu.m_lite.set_ptpcmd(port_name, ptp_mode=0, x=332.5-20*(i+1), y=y, z=-41, r=0)
            dobotEdu.m_lite.set_endeffector_suctioncup(port_name, enable=False, on=False)
            time.sleep(0.5)
        y = y - 20


    # # --- LOGICAL MOVIMENTO VENTOSA (INVERTITO SU X) ---
    # y = 28


    # # Primo blocco di movimenti
    # for j in range(4):
    #     for i in range(3):
    #         # Prima: 275+19*(3-i) -> Ora invertito: usa la i diretta per invertire la X
    #         dobotEdu.m_lite.set_ptpcmd(port_name, ptp_mode=0, x=275+19*i, y=y, z=-42, r=0)
    #         dobotEdu.m_lite.set_endeffector_suctioncup(port_name, enable=True, on=True)
    #         time.sleep(0.5)
           
    #         dobotEdu.m_lite.set_ptpcmd(port_name, ptp_mode=0, x=275, y=y, z=-42+12*(i+1), r=0)
    #         dobotEdu.m_lite.set_endeffector_suctioncup(port_name, enable=False, on=False)
    #         time.sleep(0.5)
    #     y = y - 20


    # y = 28


    # # Secondo blocco di movimenti
    # for j in range(4):
    #     for i in range(3):
    #         dobotEdu.m_lite.set_ptpcmd(port_name, ptp_mode=0, x=275, y=y, z=-10-12*i, r=0)
    #         dobotEdu.m_lite.set_endeffector_suctioncup(port_name, enable=True, on=True)
    #         time.sleep(0.5)
           
    #         # Prima: 275+19*(i+1) -> Ora invertito: parte da destra e va a sinistra rispetto a prima
    #         dobotEdu.m_lite.set_ptpcmd(port_name, ptp_mode=0, x=275+19*(3-i), y=y, z=-42, r=0)
    #         dobotEdu.m_lite.set_endeffector_suctioncup(port_name, enable=False, on=False)
    #         time.sleep(0.5)
    #     y = y - 20


if __name__ == '__main__':
    main()
