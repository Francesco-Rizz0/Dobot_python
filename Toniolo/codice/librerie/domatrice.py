import cv2
import numpy as np

def cattura_e_ritaglia_roi(sorgente_camera):
    """
    Apre la fotocamera, mostra il video in tempo reale della maschera,
    permette di bloccare il frame con SPAZIO e selezionare una ROI.
    """
    # 1. Inizializza la fotocamera
    cap = cv2.VideoCapture(sorgente_camera)

    # 2. Controlla se si è aperta correttamente
    if not cap.isOpened():
        print("Errore: fotocamera non accessibile")
        return None

    print("\n--- ISTRUZIONI ---")
    print("1. Guarda il video della maschera in tempo reale.")
    print("2. Premi 'SPAZIO' per bloccare l'immagine e iniziare la selezione della ROI.")
    print("3. Nella finestra di selezione, trascina il mouse e premi 'INVIO' per confermare.")
    print("4. Premi 'q' durante il video in tempo reale per uscire senza selezionare.")
    print("------------------\n")

    roi_ritagliata = None

    while True:
        # In un'applicazione reale, doMaschera probabilmente ha bisogno di leggere dal 'cap'.
        # Se doMaschera legge già internamente il frame, usa la tua riga originale:
        # frame, maschera = doMaschera(cap)
        
        # Se invece doMaschera elabora un singolo frame, dovresti fare:
        ret, frame = cap.read()
        if not ret:
            print("Errore nel ricevere il frame.")
            break
            
        # Ipotizzando che doMaschera accetti il frame o il cap, adattalo così.
        # Qui assumiamo che tu ottenga la 'maschera' aggiornata a ogni ciclo:
        _, maschera = doMaschera(cap) 
        
        # Mostra il video della maschera in tempo reale
        cv2.imshow("Video Maschera - Premi SPAZIO per bloccare", maschera)
        
        tasto = cv2.waitKey(1) & 0xFF
        
        # Se l'utente preme SPAZIO, blocchiamo il video e apriamo la ROI
        if tasto == ord(' '):
            print("Video bloccato. Seleziona la ROI...")
            # Chiudiamo la finestra del video live per non fare confusione
            cv2.destroyWindow("Video Maschera - Premi SPAZIO per bloccare")
            
            # Apriamo selectROI sulla maschera corrente (che ora è fissa)
            r = cv2.selectROI("Seleziona la ROI e premi INVIO", maschera, fromCenter=False, showCrosshair=True)
            
            x, y, w, h = r
            if w > 0 and h > 0:
                # Ritagliamo dal frame corrispondente (o dalla maschera, a seconda di cosa ti serve)
                roi_ritagliata = frame[y:y+h, x:x+w]
            break
            
        # Se l'utente preme 'q', esce dal programma
        elif tasto == ord('q'):
            print("Annullato dall'utente.")
            break

    # Rilascia la fotocamera e chiude tutte le finestre rimaste aperte
    cap.release()
    cv2.destroyAllWindows()
    
    return roi_ritagliata

def analizza_colori_roi_hsv(roi_totale):
    # Inizializziamo la matrice 4x4
    matrice_colori = [["" for _ in range(4)] for _ in range(4)]
    
    altezza_roi, larghezza_roi, _ = roi_totale.shape
    w_quadratino = larghezza_roi // 4
    h_quadratino = altezza_roi // 4
    
    # Definiamo i TUOI range HSV in array NumPy
    range_colori = {
        'V': (np.array([50, 50, 50]), np.array([85, 255, 255])),
        'B': (np.array([100, 140, 140]), np.array([140, 255, 255])),
        'G': (np.array([20, 100, 100]), np.array([40, 255, 255])),
        # Per il rosso standard usiamo il tuo primo range (0-10)
        'R': (np.array([0, 70, 50]), np.array([10, 255, 255]))
    }
    
    # Nota: Se il tuo rosso tende al fucsia/cremisi, potrebbe servire anche il range (170-180).
    # Per ora usiamo esattamente quello che hai fornito tu.

    for riga in range(4):
        for colonna in range(4):
            y_start = riga * h_quadratino
            y_end = (riga + 1) * h_quadratino
            x_start = colonna * w_quadratino
            x_end = (colonna + 1) * w_quadratino
            
            # 1. Estraiamo il quadratino in BGR
            quadratino_bgr = roi_totale[y_start:y_end, x_start:x_end]
            
            # 2. Convertiamo il quadratino in HSV (Fondamentale!)
            quadratino_hsv = cv2.cvtColor(quadratino_bgr, cv2.COLOR_BGR2HSV)
            
            colore_rilevato = '?'
            massimo_pixel_bianchi = 0
            
            # 3. Controlliamo quale maschera di colore genera più pixel attivi
            for colore, (min_val, max_val) in range_colori.items():
                # Crea una maschera binaria: i pixel nel range diventano bianchi (255), gli altri neri (0)
                maschera = cv2.inRange(quadratino_hsv, min_val, max_val)
                
                # Contiamo quanti pixel sono diventati bianchi per questo colore
                conteggio_pixel = cv2.countNonZero(maschera)
                
                # Il colore con il maggior numero di pixel "vince"
                if conteggio_pixel > massimo_pixel_bianchi and conteggio_pixel > 0:
                    massimo_pixel_bianchi = conteggio_pixel
                    colore_rilevato = colore
            
            # Inseriamo il risultato nella matrice
            matrice_colori[riga][colonna] = colore_rilevato
            
    return matrice_colori

def doMaschera(cap):
    # 1. Leggi il frame corrente dalla telecamera
    ret, frame = cap.read()
    if not ret:
        return None, None  # Se non riesce a leggere il frame, esce

    # 2. Converti il frame da BGR (standard OpenCV) a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Definizione dei range di colore (i tuoi vanno benissimo)
    minColorVerde = np.array([50, 50, 50])
    maxColorVerde = np.array([85, 255, 255])
    
    minColorBlu = np.array([100, 140, 140])
    maxColorBlu = np.array([140, 255, 255])
    
    minColorRosso = np.array([0, 70, 50])
    maxColorRosso = np.array([10, 255, 255])
    
    minColorGiallo = np.array([20, 100, 100])
    maxColorGiallo = np.array([40, 255, 255])

    # 3. Inizializza la maschera colorata usando le dimensioni corrette del frame
    maskColor = np.zeros((frame.shape[0], frame.shape[1], 3), dtype=np.uint8)

    # 4. Usa cv2.inRange (corretto) passando l'immagine HSV
    maskVerde = cv2.inRange(hsv, minColorVerde, maxColorVerde)
    maskBlu = cv2.inRange(hsv, minColorBlu, maxColorBlu)
    maskRossa = cv2.inRange(hsv, minColorRosso, maxColorRosso)
    maskGialla = cv2.inRange(hsv, minColorGiallo, maxColorGiallo)

    # 5. Applica i colori (Ricorda: OpenCV usa BGR, non RGB!)
    maskColor[maskBlu > 0] = (255, 0, 0)     # Blu (B=255, G=0, R=0)
    maskColor[maskVerde > 0] = (0, 255, 0)   # Verde
    maskColor[maskRossa > 0] = (0, 0, 255)   # Rosso
    maskColor[maskGialla > 0] = (0, 255, 255) # Giallo

    return frame, maskColor