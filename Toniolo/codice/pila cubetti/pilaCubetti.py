import websocket
import json
from magician_lite import *

# WS_URL = "ws://localhost:9090"

def main():
    #             (True)   ->   Simulatore
    #             (False)  ->   Robot vero 
    port = connect(True)
    
    i=0
    x=0

    distCubi = 20
    altezzaCubi = 11

    posX = 278
    posY = -29
    posZ = -45
    altezzaPila = posZ+altezzaCubi
    posXFinale = posX+ (3*distCubi)-4
    setVetosa(False)
    setHome()

    while(x<4):
        while(i<3):
            move(0,posX,posY,posZ,0)
            setVetosa(True)

            move(0,posXFinale,posY,altezzaPila,0)
            setVetosa(False)
            i+=1
            altezzaPila+=altezzaCubi
            posX+=distCubi
        x+=1
        i=0
        altezzaPila = posZ+altezzaCubi
        posY+=distCubi
        posX = 278

    print ("   x:",x,"     i:",i)
    disconnect()

if __name__ == "__main__":

    main()