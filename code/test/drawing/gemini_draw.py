import cv2
import os
import numpy as np
import time
from DobotEDU import *

# =====================================================================
# CONFIGURAZIONE QUOTE Z
# =====================================================================
Z_ALZATA = 20.0       # Quota di sicurezza
Z_SCRITTURA = -35.0   # Quota di contatto penna-foglio

# =====================================================================
# LIMITI REALI FISICI DEL DOBOT (Mantenuti e Sicuri)
# =====================================================================
X_MIN, X_MAX = 143.5, 282.5  
Y_MIN, Y_MAX = -100.0, 122.5 

# Calcoliamo le dimensioni del foglio reale in mm e il suo centro geometrico
LARGHEZZA_FOGLIO_MM = Y_MAX - Y_MIN
ALTEZZA_FOGLIO_MM = X_MAX - X_MIN
CENTRO_ROBOT_X = X_MIN + (ALTEZZA_FOGLIO_MM / 2.0)
CENTRO_ROBOT_Y = Y_MIN + (LARGHEZZA_FOGLIO_MM / 2.0)


# =====================================================================
# FUNZIONE DI MAPPING CON ASSI INVERTITI E LIMITI CORRETTI
# =====================================================================
def mappa_coordinate_centrata(x_pixel, y_pixel, x_offset_px, y_offset_px, w_disegno_px, h_disegno_px, fattore_scala):
    """
    Rimuove l'offset dell'immagine, inverte gli assi X/Y dei pixel e la posiziona
    al centro geometrico del foglio reale rispettando i limiti cartesiani del robot.
    """
    # 1. Spostiamo il punto in pixel rispetto all'inizio reale del disegno (rimuovendo i margini vuoti)
    x_relativo_px = x_pixel - x_offset_px
    y_relativo_px = y_pixel - y_offset_px

    # 2. --- INVERSIONE ASSI RICHIESTA ---
    # La coordinata X del pixel ora calcola lo spostamento in X del robot (profondità)
    # La coordinata Y del pixel ora calcola lo spostamento in Y del robot (laterale)
    x_relativo_mm = x_relativo_px * fattore_scala
    y_relativo_mm = y_relativo_px * fattore_scala

    # Trova il centro del disegno in mm (invertito anch'esso rispetto alle dimensioni dei pixel)
    centro_disegno_x_mm = (w_disegno_px * fattore_scala) / 2.0
    centro_disegno_y_mm = (h_disegno_px * fattore_scala) / 2.0

    # 3. Allineiamo il centro del disegno con il centro reale del foglio del robot
    # Usiamo i segni matematici per centrare la forma in base al nuovo orientamento
    x_robot = CENTRO_ROBOT_X - centro_disegno_x_mm + x_relativo_mm
    y_robot = CENTRO_ROBOT_Y + centro_disegno_y_mm - y_relativo_mm

    # --- BLINDATURA DI SICUREZZA ASSOLUTA (Clipping sui limiti reali) ---
    if x_robot > X_MAX: x_robot = X_MAX
    if x_robot < X_MIN: x_robot = X_MIN
    if y_robot > Y_MAX: y_robot = Y_MAX
    if y_robot < Y_MIN: y_robot = Y_MIN

    return round(x_robot, 2), round(y_robot, 2)


# =====================================================================
# FUNZIONE PRINCIPALE DI DISEGNO
# =====================================================================
def esegui_disegno(port_name, percorso_immagine):
    if not os.path.exists(percorso_immagine):
        print(f"Errore: File '{percorso_immagine}' non trovato.")
        return

    img = cv2.imread(percorso_immagine, cv2.IMREAD_GRAYSCALE)
    print("Immagine originale caricata.")

    # Semplifica l'immagine (linee nere diventano pixel bianchi per OpenCV)
    _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)

    # Trova il riquadro di ingombro minimo (Bounding Box) che contiene SOLO il disegno
    punti_disegno = cv2.findNonZero(thresh)
    if punti_disegno is None:
        print("Errore: L'immagine sembra completamente vuota.")
        return
        
    x_offset_px, y_offset_px, w_disegno_px, h_disegno_px = cv2.boundingRect(punti_disegno)
    print(f"Ingombro reale disegno: {w_disegno_px}x{h_disegno_px}px (Inizio pixel X:{x_offset_px}, Y:{y_offset_px})")

    # Calcoliamo il fattore di scala ottimale basato sull'inversione degli assi (w_disegno su ALTEZZA, h_disegno su LARGHEZZA)
    scala_x = ALTEZZA_FOGLIO_MM / w_disegno_px
    scala_y = LARGHEZZA_FOGLIO_MM / h_disegno_px
    fattore_scala = min(scala_x, scala_y) * 0.85  # Lasciamo un 15% di margine di sicurezza per evitare i bordi estremi

    # Estrazione dei contorni/traiettorie
    contorni, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print(f"Rilevati {len(contorni)} tratti da disegnare.")

    dobotEdu.magician.set_endeffector_params(port_name, x_offset=0, y_offset=0, z_offset=0)
    print("Porto la penna a quota di sicurezza...")
    dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=2, x=180, y=0, z=Z_ALZATA, r=0)

    # Ciclo di disegno sui contorni estratti
    for i, contorno in enumerate(contorni):
        print(f"Disegno tratto {i+1}/{len(contorni)}...")
        
        # --- APPROCCIO AL NUOVO TRATTO ---
        primo_punto = contorno[0][0]
        x_rob, y_rob = mappa_coordinate_centrata(primo_punto[0], primo_punto[1], x_offset_px, y_offset_px, w_disegno_px, h_disegno_px, fattore_scala)
        
        # Si sposta SOPRA l'inizio con la penna ALZATA
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=2, x=x_rob, y=y_rob, z=Z_ALZATA, r=0)
        time.sleep(0.2)
        
        # Abbassa la penna sul foglio
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=2, x=x_rob, y=y_rob, z=Z_SCRITTURA, r=0)
        time.sleep(0.2)

        # --- TRACCIAMENTO DELLA LINEA ---
        for punto in contorno:
            x_px = punto[0][0]
            y_px = punto[0][1]
            
            x_rob, y_rob = mappa_coordinate_centrata(x_px, y_px, x_offset_px, y_offset_px, w_disegno_px, h_disegno_px, fattore_scala)
            dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=2, x=x_rob, y=y_rob, z=Z_SCRITTURA, r=0)
        
        # --- FINE TRATTO ---
        # Alza la penna prima del prossimo spostamento
        dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=2, x=x_rob, y=y_rob, z=Z_ALZATA, r=0)
        time.sleep(0.1)

    print("Disegno centrato con assi invertiti e limiti sicuri completato!")
    dobotEdu.magician.set_ptpcmd(port_name, ptp_mode=2, x=180, y=0, z=Z_ALZATA, r=0)


# =====================================================================
# FUNZIONE MAIN
# =====================================================================
def main():
    port_list = dobotEdu.magician.search_dobot()
    if not port_list:
        print("Errore: Nessun robot trovato.")
        exit()

    port = port_list[0]["portName"]
    dobotEdu.magician.connect_dobot(port_name=port)
    dobotEdu.magician.clear_allalarms_state(port_name=port)
    
    # Esegue l'Homing iniziale per ricalibrare i motori dopo il blocco precedente
    print("Eseguo la calibrazione dei motori (Home)...")
    dobotEdu.magician.set_homecmd(port_name=port)
    time.sleep(15)
    
    percorso_file_immagine = r"C:\Users\User\Downloads\test_disegno.png" 
    
    esegui_disegno(port, percorso_file_immagine)

if __name__ == '__main__':
    main()