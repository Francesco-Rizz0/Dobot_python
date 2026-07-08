import customtkinter as ctk
from DobotEDU import *

# Imposta il tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DobotJoystickGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dobot Magician Joystick")
        self.geometry("400x400")

        # Titolo
        self.label = ctk.CTkLabel(self, text="Controllo Dobot", font=("Arial", 20))
        self.label.pack(pady=20)

        # Pulsante Avanti (Asse X+)
        self.btn_up = ctk.CTkButton(self, text="▲ Avanti (X+)", command=self.move_forward)
        self.btn_up.pack(pady=10)

        # Pulsante Indietro (Asse X-)
        self.btn_down = ctk.CTkButton(self, text="▼ Indietro (X-)", command=self.move_backward)
        self.btn_down.pack(pady=10)

    def move_forward(self):
        print("Invio comando: Muovi X+")
        # Qui inserirai il codice della libreria pydobot

    def move_backward(self):
        print("Invio comando: Muovi X-")
        # Qui inserirai il codice della libreria pydobot

def main():
    

    app = DobotJoystickGUI()
    app.mainloop()


if __name__ == "__main__":
    main()