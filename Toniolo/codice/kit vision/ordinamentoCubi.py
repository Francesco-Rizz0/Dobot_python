from domatrice import *
from magician import *
import cv2
import numpy as np
def initMatrice():
    roi_totale = cattura_e_ritaglia_roi(sorgente_camera=1)
    matrice = analizza_colori_roi_hsv(roi_totale)
    for riga in matrice:
        print(riga)
    return matrice


mat = initMatrice()
time.sleep(5)

dimCubi = 26

lastX = 0
lastY = 0

h_pilaRossa = -46
h_pilaBlu = -46
h_pilaGialla = -46
h_pilaVerde = -46
XpilaRossa = 180
XpilaBlu = 180
XpilaVerde = 300
XpilaGialla = 300
YpileGB = 90
YpileRV = -80

posX = 267
posY = 44  #   incrementare
posZ = -46
connect(False)
time.sleep(2)

x = 0
i = 0

setHome()

while (x<4):
    while(i<4):
        move(0,posX,posY,posZ,0)
        setVetosa(True)
        move(1,posX,posY,dimCubi+10,0)

        if(mat[i][x] == 'R'):
            print("Rosso")
            move(0,XpilaRossa,YpileRV,h_pilaRossa,0)
            h_pilaRossa+=dimCubi
            lastX = XpilaRossa
            lastY = YpileRV
        elif(mat[i][x] == 'B'):
            print("Blu")
            move(0,XpilaBlu,YpileGB,h_pilaBlu,0)
            h_pilaBlu += dimCubi
            lastX = XpilaBlu
            lastY = YpileGB
        elif(mat[i][x] == 'G'):
            print("Giallo")
            move(0,XpilaGialla,YpileGB,h_pilaGialla,0)
            h_pilaGialla+=dimCubi
            lastX = XpilaGialla
            lastY = YpileGB
        elif(mat[i][x] == 'V'):
            print("matrice: ",mat[i][x],"Verde")
            move(0,XpilaVerde,YpileRV,h_pilaVerde,0)
            h_pilaVerde+=dimCubi
            lastX = XpilaVerde
            lastY = YpileRV

        setVetosa(False)
        posX-=dimCubi
        i+=1
    x+=1
    i=0
    posX = 267
    posY-=dimCubi
move(1,lastX,lastY,dimCubi+30,0)
setHome()
disconnect(False)