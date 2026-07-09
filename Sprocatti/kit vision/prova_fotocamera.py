import cv2

# L'indice indica quale telecamera aprire. 
# 0 è solitamente la webcam integrata del PC. Prova 1, 2 o 3 per il Vision Kit.
camera_index = 0
cap = cv2.VideoCapture(camera_index)

# Opzionale: Imposta la risoluzione (es. 1080p o quella nativa della fotocamera)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("Errore: Impossibile accedere alla fotocamera del Vision Kit.")
    print("Prova a cambiare il numero di 'camera_index'.")
    exit()

print("Fotocamera avviata. Premi 'q' sulla tastiera per chiudere.")

while True:
    # Cattura il frame frame per frame
    ret, frame = cap.read()
    
    if not ret:
        print("Errore nella ricezione del frame.")
        break

    # Qui puoi inserire i tuoi algoritmi di manipolazione immagine
    # Esempio: conversione in bianco e nero
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Mostra il video in una finestra
    cv2.imshow('Dobot Vision Kit - Python Feed', frame)

    # Interrompi il ciclo se viene premuto il tasto 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia la risorsa e chiudi le finestre
cap.release()
cv2.destroyAllWindows()