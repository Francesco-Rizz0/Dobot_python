from DobotEDU import *

def main():

    port_list = dobotEdu.magician.search_dobot()
    print("Porte trovate: ")
    print(port_list)
    if not port_list:
        print("Nessun robot trovato")
        exit()
    porta = port_list[0]["portName"]
    dobotEdu.magician.connect_dobot(port_name=porta)
    port_list = dobotEdu.magician.search_dobot()
    print("Status dobot: ",port_list[0]["status"])
    dobotEdu.magician.clear_allalarms_state(port_name=porta)
    dobotEdu.magician.set_device_withl(port_name=porta,enable=True,version=1,is_queued=True)
    dobotEdu.magician.set_homecmd(port_name=porta)
    dobotEdu.magician.set_ptpwithl_cmd(port_name=porta,mode=2,x=250,y=20,z=10,r=0,set_l=800)

if __name__ == '__main__':
    main()