from DobotEDU import *

res = dobotEdu.magician.search_dobot()
print(res)
port = res[0]['portName']
dobotEdu.magician.connect_dobot(port)
print(dobot_edu.magician.get_deviceid(port))
