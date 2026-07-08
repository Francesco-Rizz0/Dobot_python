import cv2

# Avvia la videocamera USB (0 è solitamente la webcam predefinita)
cap = cv2.VideoCapture(1)

while True:
    # Cattura frame dopo frame
    ret, frame = cap.read()
    if not ret:
        break

    # Mostra il video in una finestra
    cv2.imshow('Riconoscimento Colori', frame)

    # Premi 'q' sulla tastiera per uscire dal ciclo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia la cam e chiudi le finestre
cap.release()
cv2.destroyAllWindows()