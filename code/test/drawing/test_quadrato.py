from DobotEDU import *

port_list = dobotEdu.magician.search_dobot()
print("Porte trovate: ")
print(port_list)
if not port_list:
    print("Nessun robot trovato")
    exit()
port = port_list[0]["portName"]
dobotEdu.magician.connect_dobot(port_name=port)
port_list = dobotEdu.magician.search_dobot()
print("Status dobot: ",port_list[0]["status"])

# Altezza penna
z_pen = -37.99

# Elimino allarmi
dobotEdu.magician.clear_allalarms_state(port)

# Posizione sicura
dobotEdu.magician.set_ptpcmd(port, ptp_mode=0, x=230, y=50, z=0, r=20)

# Mando alla home per ricalibrare
dobotEdu.magician.set_homecmd(port_name=port)

# Quadrato
dobotEdu.magician.set_ptpcmd(port, ptp_mode=2, x=250, y=100, z=z_pen, r=0)
dobotEdu.magician.set_ptpcmd(port, ptp_mode=2, x=200, y=100, z=z_pen, r=0)
dobotEdu.magician.set_ptpcmd(port, ptp_mode=2, x=200, y=50, z=z_pen, r=0)
dobotEdu.magician.set_ptpcmd(port, ptp_mode=2, x=250, y=50, z=z_pen, r=0)
dobotEdu.magician.set_ptpcmd(port, ptp_mode=2, x=250, y=100, z=z_pen, r=0)

# Posizione sicura
dobotEdu.magician.set_ptpcmd(port, ptp_mode=0, x=230, y=50, z=0, r=20)