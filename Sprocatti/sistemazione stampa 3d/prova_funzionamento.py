from pydobot import Dobot
import time

# 1. Connessione
device = Dobot(port='COM5', verbose=True)
time.sleep(1)

# 2. Reset allarmi
print("Resetto gli allarmi della scheda...")
device.clear_alarms()
time.sleep(0.5)

# 3. FORZATURA ACCENSIONE MOTORI (Nuovo!)
print("Dò corrente e blocco i motori in posizione...")
device.set_motor_status(True)
time.sleep(0.5)

x_avanti = 200.0
y_sinistra = 150.0  # <--- Questo valore alto costringe la base (Stepper 1) a girare a sinistra!
z_altezza = 50.0
r_rotazione = 0.0

print(f"Invio movimento cartesiano: X={x_avanti}, Y={y_sinistra}...")
# Usiamo la modalità 2 (PTP_MOVL_XYZ - Lineare) o prova la modalità 1 (PTP_MOVJ_XYZ)
device.move_to(x_avanti, y_sinistra, z_altezza, r_rotazione, 2)

print("Movimento completato!")