import subprocess
import sys

# Questo comando installa opencv direttamente dall'interno dello script
subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "numpy"])

# Ora il tuo codice può continuare normalmente
import cv2
import numpy as np
# ... resto del codice
# Apri la telecamera del Dobot (prova 0, 1 o 2 a seconda di quale ID ha preso)
cap = cv2.VideoCapture(0)

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

    # 3. Crea la maschera (isolerà solo il colore scelto)
    maskVerde = cv2.inRange(hsv, minColorVerde ,maxColorVerde)
    maskBlu = cv2.inRange(hsv, minColorBlu, maxColorBlu)


    # 4. Trova i contorni della forma isolata
    contours, _ = cv2.findContours(maskVerde, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours, _ = cv2.findContours(maskBlu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    for cnt in contours:
        # Filtra i contorni troppo piccoli (rumore di fondo)
        if cv2.contourArea(cnt) > 500:
            # Disegna il contorno verde attorno all'oggetto trovato nell'immagine originale
            cv2.drawContours(frame, [cnt], -1, (0, 0, 0), 2)
            
            # --- RICONOSCIMENTO FORME ---
            # Approssima il contorno per capire quanti lati ha la forma
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
            
            # Trova le coordinate per scrivere il testo sull'oggetto
            x, y, w, h = cv2.boundingRect(approx)
            
            if len(approx) == 3:
                cv2.putText(frame, "Triangolo", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif len(approx) == 4:
                # Potrebbe essere un quadrato o un rettangolo
                aspect_ratio = float(w)/h
                if 0.95 <= aspect_ratio <= 1.05:
                    cv2.putText(frame, "Quadrato", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                else:
                    cv2.putText(frame, "Rettangolo", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif len(approx) > 4:
                cv2.putText(frame, "Cerchio", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Mostra i risultati a video
    cv2.imshow('Inquadratura Originale', frame)
    cv2.imshow('Maschera Colore', maskVerde)

    # Premi 'q' per uscire dal ciclo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()