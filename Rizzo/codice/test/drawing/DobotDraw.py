from DobotEDU import *

# Altezza penna
z_pen = -37.99

# Limiti inferiori
lower_bounds = {"x_low": 143.5,"y_low": -116}

# Limiti superiori
upper_bounds = {"x_up": 282.5,"y_up": 122.5}

# Funzione rettangolo
def draw_rectangle(p1,p2,port):
    # Controllo correttezza coordinate
    if ((p1[0]>upper_bounds['x_up'] or p1[0]<lower_bounds["x_low"]) 
    or (p1[1]>upper_bounds['y_up'] or p1[1]<lower_bounds["y_low"])
    or (p2[0]>upper_bounds['x_up'] or p2[0]<lower_bounds["x_low"]) 
    or (p2[1]>upper_bounds['y_up'] or p2[1]<lower_bounds["y_low"])):
        print("Error! Given coordinates exceed maximum or minimun coordinates:")
        print(f"Max x: {upper_bounds['x_up']}, Max y: {upper_bounds['y_up']}, Min x: {lower_bounds['x_low']}, Min y: {lower_bounds['y_low']}")
        return
    
    # Disegno rettangolo
    dobotEdu.magician.set_ptpcmd(port, ptp_mode=2, x=p1[0], y=p1[1], z=z_pen, r=0)
    dobotEdu.magician.set_ptpcmd(port, ptp_mode=2, x=p1[0], y=p2[1], z=z_pen, r=0)
    dobotEdu.magician.set_ptpcmd(port, ptp_mode=2, x=p2[0], y=p2[1], z=z_pen, r=0)
    dobotEdu.magician.set_ptpcmd(port, ptp_mode=2, x=p2[0], y=p1[1], z=z_pen, r=0)
    dobotEdu.magician.set_ptpcmd(port, ptp_mode=2, x=p1[0], y=p1[1], z=z_pen, r=0)