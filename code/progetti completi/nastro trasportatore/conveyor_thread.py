from DobotEDU import *
import cv2
import os
import numpy as np
import time
import queue
import threading

# Coda comunicazione
coda = queue.Queue()

# Funzione riconoscimento colore
def get_prevalent_color(red_mask, green_mask, blue_mask):
    # Stringa ritornata
    color_out = ""

    # Valore minimo per ricopnoscere colore
    soglia_dominanza = 0.51

    # Conta quanti pixel ci sono per ogni colore
    red_count = cv2.countNonZero(red_mask)
    green_count = cv2.countNonZero(green_mask)
    blue_count = cv2.countNonZero(blue_mask)

    # Somma totale dei pixel colorati rilevati
    total_colored_pixels = red_count + green_count + blue_count

    # Logica di controllo
    # Soglia minima per dire che un colore "esiste" nell'inquadratura (es. almeno il 5% dell'immagine)
    soglia_presenza = 0.05 

    # Calcola le percentuali relative rispetto ai soli pixel colorati
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

    # controllo presenza colori
    if p_red < soglia_presenza:
        p_red = 0
    if p_green < soglia_presenza:
        p_green = 0
    if p_blue < soglia_presenza:
        p_blue = 0

    #controllo dominanza
    if p_red >= soglia_dominanza:
        color_out = "red"
    elif p_green >= soglia_dominanza:
        color_out = "green"
    elif p_blue >= soglia_dominanza:
        color_out = "blue"
    else:
        color_out = "null"

    return color_out

# Funzione controllante il robot
def dobot():
    # Ricerca delle porte per il Magician standard
    res = dobotEdu.magician.search_dobot() 
    
    print("Porte trovate:", res)
    
    if not res:
        print("Errore: Nessun robot trovato. Controlla il cavo USB e l'alimentazione.")
        return

    port_name = res[0]["portName"]  
    
    # Connessione al Magician standard
    dobotEdu.magician.connect_dobot(port_name=port_name)  
    res = dobotEdu.magician.search_dobot() 
    status_connessione = res[0]['status'] 
    print(status_connessione)

    #posizioni carico-scarico
    carico = {"x": 235,"y": -123, "z":-30.77 }
    scarico = {"x": 265,"y": 154,"z": -29.45}

    #setup sensore infrarossi
    dobotEdu.magician.set_infrared_sensor(port_name=port_name,port=2,enable=True,version=1,is_queued=False)
    continuare = True
    conta = 0
   
    #posizione sicura
    dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=230, y=50, z=0, r=20)

    while conta < 4:
        #inizio nastro
        dobotEdu.magician.set_converyor(port_name=port_name,index=0,enable=True,speed=10000,is_queued=True)
        while continuare:
            #test coda
            print(coda.get())
            #lettura status sensore
            infrared_status = dobotEdu.magician.get_infrared_sensor(port_name=port_name,port=2,is_queued=False)
            if(infrared_status["status"]==1):
                continuare = False
        #fermo nastro
        dobotEdu.magician.set_converyor(port_name=port_name,index=0,enable=False,speed=0,is_queued = True)
        #muovo braccio al cubetto e lo prelevo
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=carico["x"], y=carico["y"], z=carico["z"], r=20)
        dobotEdu.magician.set_endeffector_suctioncup(port_name=port_name,enable=True,on=True)
        time.sleep(1)
        #mi alzo per evitare contatti e mi muovo verso la posizione di scarico
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=carico["x"], y=carico["y"], z=carico["z"]+40, r=20)
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=scarico["x"], y=scarico["y"], z=scarico["z"]+40, r=20)
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=scarico["x"], y=scarico["y"], z=scarico["z"], r=20)
        #rilascio il cubetto
        dobotEdu.magician.set_endeffector_suctioncup(port_name=port_name,enable=False,on=False)
        time.sleep(1)
        #posizione di sicurezza
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=0, x=scarico["x"], y=scarico["y"], z=scarico["z"]+40, r=20)
        continuare = True
        conta += 1

# Funzione opencv
def riconoscimento():
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

        # Intervallo per il colore Verde in OpenCV
        lower_green = np.array([45, 100, 50])
        upper_green = np.array([75, 255, 255])

        # Intervallo per il colore Blu in OpenCV
        lower_blue = np.array([90, 100, 50])
        upper_blue = np.array([130, 255, 255])

        # 6. Crea le maschere per isolare il rosso e uniscile
        mask1 = cv2.inRange(hsv_frame, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv_frame, lower_red2, upper_red2)
        mask_red = mask1 + mask2  

        mask_green = cv2.inRange(hsv_frame, lower_green, upper_green)

        mask_blue = cv2.inRange(hsv_frame, lower_blue, upper_blue)

        # 7. Pulisci la maschera dai "rumori" di sottofondo (puntini minuscoli fastidiosi)
        kernel = np.ones((5, 5), np.uint8)
        mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_OPEN, kernel)
        mask_green = cv2.morphologyEx(mask_green, cv2.MORPH_OPEN, kernel)
        mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)

        # 8. Trova i contorni degli oggetti rossi rilevati
        contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_green, _ = cv2.findContours(mask_green, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours_red:
            # Filtra i contorni troppo piccoli per evitare falsi positivi (es. riflessi)
            area = cv2.contourArea(contour)
            if area > 500:
                # Calcola le coordinate del rettangolo che racchiude l'oggetto
                x, y, w, h = cv2.boundingRect(contour)
                
                # Disegna il rettangolo verde intorno all'oggetto rosso rilevato
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Scrivi il testo "ROSSO" sopra il rettangolo
                cv2.putText(frame, "ROSSO", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        for contour in contours_green:
            # Filtra i contorni troppo piccoli per evitare falsi positivi (es. riflessi)
            area = cv2.contourArea(contour)
            if area > 500:
                # Calcola le coordinate del rettangolo che racchiude l'oggetto
                x, y, w, h = cv2.boundingRect(contour)
                
                # Disegna il rettangolo verde intorno all'oggetto rosso rilevato
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Scrivi il testo "ROSSO" sopra il rettangolo
                cv2.putText(frame, "VERDE", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)  

        for contour in contours_blue:
            # Filtra i contorni troppo piccoli per evitare falsi positivi (es. riflessi)
            area = cv2.contourArea(contour)
            if area > 500:
                # Calcola le coordinate del rettangolo che racchiude l'oggetto
                x, y, w, h = cv2.boundingRect(contour)
                
                # Disegna il rettangolo verde intorno all'oggetto rosso rilevato
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Scrivi il testo "ROSSO" sopra il rettangolo
                cv2.putText(frame, "BLU", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)       

        # 9. Mostra i due flussi video: l'originale modificato e la maschera binaria
        cv2.imshow('Rilevatore di Colore', frame)

        #test coda
        coda.put(get_prevalent_color(mask_red,mask_green,mask_blue))

        # 10. Gestione della chiusura pulita con il tasto 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # In chiusura, rilascia la webcam e distruggi le finestre aperte
    cap.release()
    cv2.destroyAllWindows()


def main():
    dobot_t = threading.Thread(target=dobot)
    opencv_t = threading.Thread(target=riconoscimento)

    dobot_t.start()
    opencv_t.start()

    dobot_t.join()
    opencv_t.join()

if __name__ == '__main__':
    main()