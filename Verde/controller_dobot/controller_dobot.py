import sys
import keyboard
from DobotEDU import m_lite 
import time       
import pyperclip   

PORTA = 'COM4'

try:
    m_lite.set_armspeed_ratio(PORTA, set_type=1, set_value=100)
except Exception as e:
    print(f"\n[ERRORE DI CONNESSIONE]: {e}")
    print("Verifica che il robot sia acceso sulla COM4 e che DobotLink sia avviato.")
    sys.exit()
    
m_lite.set_armspeed_ratio(PORTA,set_type=0,set_value=51)

def stampaCodice(strCodice):
   print("Codice:\n\n"+strCodice+"\nIl codice è stato copiato negli appunti!\n")
   pyperclip.copy(strCodice)
    
def muovi(coordinata,tasto):
    m_lite.set_jogcmd(PORTA, is_joint=0, cmd=coordinata)
    while keyboard.is_pressed(tasto):
        time.sleep(0.01)
    m_lite.set_jogcmd(PORTA, is_joint=0, cmd=0)

registrazione=False
strCodice=""
print("Usa:\n- WASD per muovere il robot\n- Shift per abbassarlo\n- Spazio per alzarlo\n- + e - per cambiare la velocità\n- H per farlo tornare alla home\n- E per abilitare la ventosa\n- Q per disabilitare la ventosa\n- F per ottenere le coordinate\n- R per iniziare la registrazione dei movimenti (per andare ad un punto devi prendere le coordinate con F), una volta terminato premi R per avere il codice\n- Backspace per cancellare l'ultima riga di codice\n- ESC per uscire\n- O per ruotare in senso antiorario la ventosa\n- P per ruotare in senso orario la ventosa\n")
while True:
    time.sleep(0.01)
    
    if keyboard.is_pressed("s"):
        muovi(1,"s")
    
    if keyboard.is_pressed("backspace"):
        if registrazione:
            if strCodice:
                righe = strCodice.splitlines()
                print("Riga di codice cancellata: "+righe[-1]+"\n")
                del righe[-1]
                strCodice = "\n".join(righe)
                if strCodice:
                    strCodice+="\n"
            else:
                print("Non ho righe da cancellare\n")
            time.sleep(0.5)
    
    if keyboard.is_pressed("r"):
        if registrazione:
            registrazione=False
            print("Registrazione disattivata\n")
            if strCodice!="":
                stampaCodice(strCodice)
                strCodice=""
        else:
            registrazione=True
            print("Registrazione attivata\n")
        time.sleep(1)

    if keyboard.is_pressed("f"):
        coordinate=m_lite.get_pose(PORTA)
        print("x = "+str(int(coordinate["x"]))+", y = "+str(int(coordinate["y"]))+", z = "+str(int(coordinate["z"]))+", r = "+str(int(coordinate["r"])))
        if registrazione:
            strCodice+="m_lite.set_ptpcmd(ptp_mode=0, x = "+str(coordinate["x"])+", y = "+str(coordinate["y"])+", z = "+str(coordinate["z"])+", r = "+str(coordinate["r"])+")\n"
            print("Coordinata registrata\n")
        else:
            print()

        time.sleep(0.5)
        
    if keyboard.is_pressed("w"):
        muovi(2,"w")
        
    if keyboard.is_pressed("d"):
        muovi(3,"d")
        
    if keyboard.is_pressed("a"):
        muovi(4,"a")
        
    if keyboard.is_pressed("space"):
        muovi(5,"space")
        
    if keyboard.is_pressed("shift"):
        muovi(6,"shift")
        
    if keyboard.is_pressed("o"):
        muovi(7, "o")
        
    if keyboard.is_pressed("p"):
        muovi(8, "p")
        
    if keyboard.is_pressed("+"):
        dati=m_lite.get_armspeed_ratio(PORTA,get_type=0)
        speed=dati["value"]
        if speed==101:
            speed-=10
        m_lite.set_armspeed_ratio(PORTA,set_type=0,set_value=(speed+10))
        print("speed: "+(str(speed+9)))
        time.sleep(0.1)
        
    if keyboard.is_pressed("-"):
        dati=m_lite.get_armspeed_ratio(PORTA,get_type=0)
        speed=dati["value"]
        if speed==1:
            speed+=10
        m_lite.set_armspeed_ratio(PORTA,set_type=0,set_value=(speed-10))
        print("speed: "+(str(speed-11)))
        time.sleep(0.1)
    
    if keyboard.is_pressed("h"):
        m_lite.set_homecmd(PORTA)
        if registrazione:
            strCodice+="m_lite.set_homecmd(PORTA)\n"
            print("Comando home registrato\n")
        time.sleep(0.5)
        
    if keyboard.is_pressed("e"):
        m_lite.set_endeffector_suctioncup(PORTA,enable=True, on=True)
        if registrazione:
            strCodice+="m_lite.set_endeffector_suctioncup(enable=True, on=True)\n"
            print("Attiva ventosa registrata\n")
        time.sleep(0.5)
        
    if keyboard.is_pressed("q"):
        m_lite.set_endeffector_suctioncup(PORTA,enable=False, on=False)
        if registrazione:
            strCodice+="m_lite.set_endeffector_suctioncup(enable=False, on=False)\n"
            print("Disattiva ventosa registrata\n")
        time.sleep(0.5)
        
    if keyboard.is_pressed("esc"):
        if strCodice!="":
            stampaCodice(strCodice)
            strCodice=""
        m_lite.set_endeffector_suctioncup(PORTA,enable=False, on=False)
        m_lite.set_homecmd(PORTA)
        break
