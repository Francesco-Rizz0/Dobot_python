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
dobotEdu.magician.clear_allalarms_state(port)
dobotEdu.magician.set_homecmd(port_name=port)