import subprocess
import sys
# Questo comando installa opencv direttamente dall'interno dello script
subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "numpy"])

# dimensioni ROI
# Coordinata X di partenza: 406
# Coordinata Y di partenza: 273
# Larghezza del rettangolo: 178
# Altezza del rettangolo: 175

import cv2
import numpy as np

# Apri la telecamera del Dobot
cap = cv2.VideoCapture(1 + cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

if not cap.isOpened():
    print("Errore: Impossibile aprire la telecamera del Vision Kit. Controlla l'indice o il cavo USB.")
    sys.exit()

def contorno(frame, contours):
    for cnt in contours:
        # Filtra i contorni troppo piccoli
        if cv2.contourArea(cnt) > 500:
            # Approssima il contorno
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)

            # Se ha 4 lati (quadrato/rettangolo) lo disegna in BGR (Viola)
            if len(approx) == 4:
                cv2.drawContours(frame, [cnt], -1, (255, 0, 255), 2)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Impossibile ricevere il frame.")
        break

    # Converti l'immagine da BGR a HSV per il rilevamento corretto dei colori
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# RANGE COLORI IN HSV (Standard OpenCV: H: 0-180, S: 0-255, V: 0-255)
    minColorVerde = np.array([50, 50, 50])
    maxColorVerde = np.array([85, 255, 255])
    
    minColorBlu = np.array([0, 80, 100])
    maxColorBlu = np.array([140, 255, 255])
    
    # Il rosso in HSV si trova all'inizio e alla fine della scala (0-10 e 170-180).
    # Usiamo un range standard iniziale.
    minColorRosso = np.array([0, 50, 30])
    maxColorRosso = np.array([10, 255, 255])
    
    minColorGiallo = np.array([0, 80, 100])
    maxColorGiallo = np.array([40, 255, 255])

    # Crea un'immagine nera delle stesse dimensioni del frame (in BGR per la visualizzazione)
    maskColor = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)

    # Crea le maschere binarie in base ai range HSV definiti sopra
    maskVerde = cv2.inRange(hsv, minColorVerde, maxColorVerde)
    maskBlu = cv2.inRange(hsv, minColorBlu, maxColorBlu)
    maskRossa = cv2.inRange(hsv, minColorRosso, maxColorRosso)
    maskGialla = cv2.inRange(hsv, minColorGiallo, maxColorGiallo)

    # Coloriamo la maschera finale (I colori qui sono in formato BGR)
    maskColor[maskBlu > 0] = (255, 0, 0)     # Blu
    maskColor[maskVerde > 0] = (0, 255, 0)   # Verde
    maskColor[maskRossa > 0] = (0, 0, 255)   # Rosso
    maskColor[maskGialla > 0] = (0, 255, 255) # Giallo
    
    # Trova i contorni sulle maschere e disegnali sul frame originale
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
    immage = cv2.imshow('maschera', maskColor)

    # Premi 'q' per uscire
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #rettangolo = cv2.selectROI("Seleziona la ROI", immagine, fromCenter=False, showCrosshair=True)



cap.release()
cv2.destroyAllWindows()