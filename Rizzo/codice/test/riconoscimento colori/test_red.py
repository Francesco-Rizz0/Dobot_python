import cv2
import numpy as np
import os

# 1. Forza OpenCV a ignorare il modulo problematico di Windows (MSMF)
os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"

# 2. Avvia la videocamera usando le API DirectShow (cv2.CAP_DSHOW)
# Se non rileva la cam corretta, prova a cambiare lo 0 con 1
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# Controllo di sicurezza: verifica se la videocamera si è aperta davvero
if not cap.isOpened():
    print("Errore: Impossibile accedere alla videocamera USB.")
    exit()

print("Programma avviato correttamente. Premi 'q' per uscire.")

while True:
    # 3. Cattura il singolo fotogramma
    ret, frame = cap.read()
    if not ret:
        print("Errore: Impossibile leggere i dati dalla videocamera.")
        break

    # 4. Converti il frame da BGR a HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 5. Definisci i limiti del colore ROSSO in HSV
    # Il rosso si trova alle due estremità della scala HSV, quindi servono due intervalli
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # 6. Crea le maschere per isolare il rosso e uniscile
    mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
    mask_red = mask1 + mask2  

    # 7. Pulisci la maschera dai "rumori" di sottofondo (puntini minuscoli fastidiosi)
    kernel = np.ones((5, 5), np.uint8)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)

    # 8. Trova i contorni degli oggetti rossi rilevati
    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Filtra i contorni troppo piccoli per evitare falsi positivi (es. riflessi)
        area = cv2.contourArea(contour)
        if area > 500:
            # Calcola le coordinate del rettangolo che racchiude l'oggetto
            x, y, w, h = cv2.boundingRect(contour)
            
            # Disegna il rettangolo verde intorno all'oggetto rosso rilevato
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Scrivi il testo "ROSSO" sopra il rettangolo
            cv2.putText(frame, "ROSSO", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 9. Mostra i due flussi video: l'originale modificato e la maschera binaria
    cv2.imshow('Rilevatore di Colore', frame)
    cv2.imshow('Maschera Rossa (Vista del computer)', mask_red)

    # 10. Gestione della chiusura pulita con il tasto 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# In chiusura, rilascia la webcam e distruggi le finestre aperte
cap.release()
cv2.destroyAllWindows()