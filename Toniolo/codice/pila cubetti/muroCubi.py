from DobotEDU import DobotEDU  
import time
# Inizializzazione della classe
dobotEdu = DobotEDU()

# --- AGGIRAMENTO BUG DOBOT SENZA ACCOUNT ---
def finto_on_pause(): pass
def finto_on_resume(): pass

dobotEdu.m_lite.on_pause = finto_on_pause
dobotEdu.m_lite.on_resume = finto_on_resume
# --------------------------------------------

# Cerca la porta
res = dobotEdu.m_lite.search_dobot()  
print("Porte trovate:", res)

if not res:
    print("Errore: Nessun robot trovato. Controlla il cavo USB.")

port = res[0]["portName"]  

# Connessione
dobotEdu.m_lite.connect_dobot(port_name=port)  
print(f"Connesso con successo a Magician Lite su {port}")

posXFinale = 335
posZFinale = 0
posX = 316
posY = 30
posZ = -42+11
distCubi = 20
posZ2 =0
posX2 = 0
i=0
x=0



while(x<4):
  while(i<3):
    m_lite.set_ptpcmd(port_name=port,ptp_mode=0, x=posX, y=posY, z=-42, r=0)
    m_lite.set_endeffector_suctioncup(port_name=port,enable=True, on=True)
    time.sleep(1);
    m_lite.set_ptpcmd(port_name=port,ptp_mode=0, x=posXFinale, y=posY, z=posZ, r=0)
    m_lite.set_endeffector_suctioncup(port_name=port,enable=False, on=False)
    time.sleep(1)
    posX-=distCubi
    i+=1
    posZFinale = posZ/1.1
    posZ+=12
  x+=1
  i=0
  if(x!=4):
    posZ=-42+11
    posX=316
    posY-=distCubi

i = 0
x = 0

posX2 = 335-distCubi
posZ2 = -9

while(x<4):
  while( i<3):
    m_lite.set_ptpcmd(port_name=port,ptp_mode=0, x=335, y=posY, z=posZ2, r=0)
    m_lite.set_endeffector_suctioncup(enable=True, on=True)
    time.sleep(1)
    m_lite.set_ptpcmd(port_name=port,ptp_mode=0, x=posX2, y=posY, z=-42, r=0)
    m_lite.set_endeffector_suctioncup(port_name=port,enable=False, on=False)
    time.sleep(1)
    posZ2-=12
    posX2-=distCubi
    i+=1
  i=0
  x+=1
  posY+=distCubi
  posX2=335-distCubi
  posZ2 +=36