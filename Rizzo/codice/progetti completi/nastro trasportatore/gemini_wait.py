from DobotEDU import *
import cv2
import os
import numpy as np
import time
import multiprocessing  # <--- Sostituito queue e threading con multiprocessing

# Funzione riconoscimento colore (Identica alla tua)
def get_prevalent_color(red_mask, green_mask, blue_mask):

    # Colore ritornato
    color_out = ""

    # Soglia minima percentuale colore dominante
    soglia_dominanza = 0.51

    # Sogli minima percentuale rilevamento colori
    soglia_presenza = 0.05 

    # Conteggio pixel colori
    red_count = cv2.countNonZero(red_mask)
    green_count = cv2.countNonZero(green_mask)
    blue_count = cv2.countNonZero(blue_mask)

    # Conteggio pixel totali
    total_colored_pixels = red_count + green_count + blue_count

    #Calcolo percentuale colori
    try:
        p_red = red_count / total_colored_pixels
    except:
        p_red = 0
    try:
        p_green = green_count / total_colored_pixels
    except:
        p_green = 0
    try:
        p_blue = blue_count / total_colored_pixels
    except:
        p_blue = 0

    # Eliminazione percentuali troppo basse
    if p_red < soglia_presenza:
        p_red = 0
    if p_green < soglia_presenza:
        p_green = 0
    if p_blue < soglia_presenza:
        p_blue = 0

    # Impostazione colore ritornato
    if p_red >= soglia_dominanza:
        color_out = "red"
    elif p_green >= soglia_dominanza:
        color_out = "green"
    elif p_blue >= soglia_dominanza:
        color_out = "blue"
    else:
        color_out = "null"

    return color_out

# Funzione controllante il robot (Ora accetta la coda come argomento)
def dobot(coda_comunicazione,stop_event):
    # NOTA: Non serve più nessun fix per asyncio! Il processo gestisce tutto nativamente.
    # Cerca il dobot tyra le porte seriali
    res = dobotEdu.magician.search_dobot() 
    
    # Stampa le porte trovate
    print("Porte trovate:", res)
    
    # Controllo robot trovati
    if not res:
        print("Errore: Nessun robot trovato. Controlla il cavo USB e l'alimentazione.")
        stop_event.set()
        return

    # Connette il robot
    port_name = res[0]["portName"]  
    dobotEdu.magician.connect_dobot(port_name=port_name)  
    res = dobotEdu.magician.search_dobot()

    # Controllo status connessione 
    status_connessione = res[0]['status'] 
    print("Stato connessione Dobot:", status_connessione)

    # Altezza del cubetto
    delta_z = 24.5

    # Inizio delle pile
    z_start = -85.5

    # Punti di carico/scarico cubetti
    punto_carico = {"x": 222,"y": -112, "z": -31}
    punto_sensore = {"x": 160,"y": -182.5, "z": -19.5}
    punto_rossi = {"x": 70,"y": 201, "z": z_start}
    punto_verdi = {"x": 10,"y": 201, "z": z_start}
    punto_blu = {"x": -58,"y": 201, "z": z_start}
    punto_scarti = {"x": 120,"y": 201, "z": z_start}

    # --- IMPLEMENTAZIONE TIMEOUT ---
    # Tempo massimo di attesa in secondi
    timeout_sensore = 10.0
    tempo_inizio = time.time()

    # Inizializza sensore rilevamento
    dobotEdu.magician.set_infrared_sensor(port_name=port_name,port=2,enable=True,version=1,is_queued=False)

    # Flag ciclo primario
    procedere = True

    # Ciclo smistamento cubetti
    while procedere:
        # Flag sensore rilevamento
        continuare = True

        # Porto il braccio sopra il punto di carico
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_carico["x"], y=punto_carico["y"], z=punto_carico["z"]+20, r=20)

        # Parte il nastro trasportatore
        dobotEdu.magician.set_converyor(port_name=port_name,index=0,enable=True,speed=10000,is_queued=True)

        # Resetto il timer
        tempo_inizio = time.time()

        # Controllo rilevamento
        while continuare:
            infrared_status = dobotEdu.magician.get_infrared_sensor(port_name=port_name,port=2,is_queued=False)
            if(infrared_status["status"]==1):
                continuare = False
            # Controlla se è passato troppo tempo
            if time.time() - tempo_inizio > timeout_sensore:
                print(f"[DOBOT] ATTENZIONE: Timeout di {timeout_sensore}s raggiunto! Nessun oggetto rilevato.")
                procedere = False
                #Esci dal ciclo while del sensore
                continuare = False

        # Ferma il nastro trasportatore
        dobotEdu.magician.set_converyor(port_name=port_name,index=0,enable=False,speed=0,is_queued = True)

        if procedere:      
            # Prendiamo il cubetto dal nastro
            dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_carico["x"], y=punto_carico["y"], z=punto_carico["z"], r=20)
            dobotEdu.magician.set_endeffector_suctioncup(port_name=port_name,enable=True,on=True)
            dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_carico["x"], y=punto_carico["y"], z=punto_carico["z"]+80, r=20)
            time.sleep(0.5)

            # Lo spostiamo sul sensore
            dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_sensore["x"], y=punto_sensore["y"], z=punto_sensore["z"], r=20)

            # Leggiamo il colore dalla coda condivisa del processo
            colore_cubetto = coda_comunicazione.get()
            print(f"[DOBOT] Cubetto rilevato! Colore letto dalla coda: {colore_cubetto}")
            time.sleep(0.5)

            # Lo prendioamo dal sensore e lo impiliamo
            dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_sensore["x"], y=punto_sensore["y"], z=punto_sensore["z"]+100, r=20)
            # Pila rossa
            if colore_cubetto == "red":
                dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_rossi["x"], y=punto_rossi["y"], z=punto_rossi["z"], r=20)
                dobotEdu.magician.set_endeffector_suctioncup(port_name=port_name,enable=False,on=False)
                dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_rossi["x"], y=punto_rossi["y"], z=z_start+150, r=20)
                punto_rossi["z"] = punto_rossi["z"] + delta_z
            # Pila verde
            elif colore_cubetto == "green":
                dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_verdi["x"], y=punto_verdi["y"], z=punto_verdi["z"], r=20)
                dobotEdu.magician.set_endeffector_suctioncup(port_name=port_name,enable=False,on=False)
                dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_verdi["x"], y=punto_verdi["y"], z=z_start+150, r=20)
                punto_verdi["z"] = punto_verdi["z"] + delta_z
            # Pila blu
            elif colore_cubetto == "blue":
                dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_blu["x"], y=punto_blu["y"], z=punto_blu["z"], r=20)
                dobotEdu.magician.set_endeffector_suctioncup(port_name=port_name,enable=False,on=False)
                dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_verdi["x"], y=punto_verdi["y"], z=z_start+150, r=20)
                punto_blu["z"] = punto_blu["z"] + delta_z
            # Pila scarti
            else:
                dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_scarti["x"], y=punto_scarti["y"], z=punto_scarti["z"], r=20)
                dobotEdu.magician.set_endeffector_suctioncup(port_name=port_name,enable=False,on=False)
                dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_scarti["x"], y=punto_scarti["y"], z=z_start+150, r=20)
                punto_scarti["z"] = punto_scarti["z"] + delta_z
                
    
    # Porto il braccio sopra il punto di carico
    dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=punto_carico["x"], y=punto_carico["y"], z=punto_carico["z"]+20, r=20)

    # Fermo l'esecuzione
    stop_event.set()
    
    

# Funzione opencv (Ora accetta la coda come argomento)
def riconoscimento(coda_comunicazione,stop_event):
    # Dice al os di non usare API MSMF
    os.environ["OPENCV_VIDEOIO_PRIORITY_MSMF"] = "0"

    # Apre la cam (senza API cam windows)
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # Controllo corretto avvio cam
    if not cap.isOpened():
        print("Errore: Impossibile accedere alla videocamera USB.")
        exit()

    print("Programma OpenCV avviato correttamente. Premi 'q' per uscire.")

    while True:
        # Prende i frame + controllo errori
        ret, frame = cap.read()
        if not ret:
            print("Errore: Impossibile leggere i dati dalla videocamera.")
            break

        # Converte il frame da RGB a HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Crea valori HSV per i colori rilevati
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])
        lower_green = np.array([45, 100, 50])
        upper_green = np.array([75, 255, 255])
        lower_blue = np.array([90, 100, 50])
        upper_blue = np.array([130, 255, 255])

        # Crea le maschere dei colori
        mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        mask_red = mask1 + mask2  
        mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)
        mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)

        # Elimina rumori di sottofondo
        kernel = np.ones((5, 5), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
        mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)

        # Crea i contorni dei colori
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Disegna i contorni del colore sulla cam
        for contour in contours_red:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "ROSSO", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        for contour in contours_green:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "VERDE", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)  

        for contour in contours_blue:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "BLU", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)       

        # Mostra cosa vede la cam con rilevamento colori
        cv2.imshow('Rilevatore di Colore', frame)

        # Svuotiamo la coda prima di inserire il dato fresco
        while not coda_comunicazione.empty():
            try:
                coda_comunicazione.get_nowait()
            except:
                break
        
        # Mettiamo il dato in coda
        coda_comunicazione.put(get_prevalent_color(mask_red, mask_green, mask_blue))

        # REATTIVITÀ FINESTRA: cv2.waitKey(1) permette alla finestra di aggiornarsi
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[OPENCV] Chiusura manuale tramite tasto 'q'")
            stop_event.set() # Diciamo anche al dobot di fermarsi se necessario
            break

        # Chiudo il processo quando si interrompe il processo del dobot
        if stop_event.is_set():
            break
        

    # Rialscia la cam e chiude la finestra
    cap.release()
    cv2.destroyAllWindows()


def main():
    # Creiamo una coda sicura per il Multiprocessing
    coda = multiprocessing.Queue()

    # Creazione evento di stop
    stop_event = multiprocessing.Event()

    # Avviamo il robot dentro un processo INDIPENDENTE
    # Windows richiede che la coda sia passata esplicitamente come argomento
    dobot_p = multiprocessing.Process(target=dobot, args=(coda,stop_event))
    dobot_p.start()

    # Eseguiamo OpenCV direttamente nel processo principale.
    # Questo è fondamentale per evitare che le finestre di Windows (cv2.imshow) si blocchino.
    riconoscimento(coda,stop_event)

    # Quando chiudi OpenCV con 'q', attendiamo la fine del processo del robot
    dobot_p.join()

if __name__ == '__main__':
    main()