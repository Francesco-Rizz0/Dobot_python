import subprocess
import sys

# Questo comando installa opencv direttamente dall'interno dello script
subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "numpy"])

# Ora il tuo codice può continuare normalmente
from pypylon import pylon
import cv2
import numpy as np


# Connessione alla telecamera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
    if grabResult.GrabSucceeded():
        # Converte l'immagine in un formato leggibile da OpenCV
        img = grabResult.Array
        cv2.imshow('Vision Kit', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    grabResult.Release()

camera.Close()
cv2.destroyAllWindows()

# ... resto del codice
# Apri la telecamera del Dobot (prova 0, 1 o 2 a seconda di quale ID ha preso)
cap = cv2.VideoCapture(0)

def contorno(frame, contours):
    for cnt in contours:
        # Filtra i contorni troppo piccoli
        if cv2.contourArea(cnt) > 500:

            # Approssima il contorno
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

            if len(approx) == 4:
                cv2.drawContours(frame, [cnt], -1, (255, 0, 255), 2)

while True:
    #prende 1 frame
    ret, frame = cap.read()

    if not ret:
        print("Impossibile ricevere il frame.")
        break

    #Converti l'immagine da BGR a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 2. Definisci il range del colore da cercare (Esempio: un range per il Verde)
    # Nota: dovrai regolare questi valori in base alla luce della tua stanza
    # lower_color = np.array([35, 50, 50])
    # upper_color = np.array([85, 255, 255])

    minColorVerde = np.array([35, 50, 50])
    maxColorVerde = np.array([85, 255, 255])
    minColorBlu = np.array([100, 50, 50])
    maxColorBlu = np.array([140, 255, 255])
    minColorRosso = np.array([100, 35, 50])
    maxColorRosso = np.array([200, 65, 85])
    minColorGiallo = np.array([20, 100, 100])
    maxColorGiallo = np.array([35, 255, 255])

    maskColor = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)

    # 3. Crea la maschera (isolerà solo il colore scelto)
    maskVerde = cv2.inRange(hsv, minColorVerde ,maxColorVerde)
    maskBlu = cv2.inRange(hsv, minColorBlu, maxColorBlu)
    maskRossa = cv2.inRange(hsv, minColorRosso,maxColorRosso)
    maskGialla = cv2.inRange(hsv, minColorGiallo, maxColorGiallo)

    maskColor[maskBlu > 0] = (255, 0, 0)
    maskColor[maskVerde > 0] = (0, 255, 0)
    maskColor[maskRossa > 0] = (0,0,255)
    maskColor[maskGialla > 0] = (0,255,255)
    # 4. Trova i contorni della forma isolata
    contoursVerde, _ = cv2.findContours(maskVerde, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contorno(frame, contoursVerde)
    contoursBlu, _ = cv2.findContours(maskBlu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contorno(frame, contoursBlu)
    contoursRossi, _ = cv2.findContours(maskRossa, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contorno(frame, contoursRossi)
    contoursGialli, _ = cv2.findContours(maskGialla, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contorno(frame, contoursGialli)
    
    # Mostra i risultati a video
    cv2.imshow('Inquadratura Originale', frame)
    cv2.imshow('maschera',maskColor)

    # Premi 'q' per uscire dal ciclo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
