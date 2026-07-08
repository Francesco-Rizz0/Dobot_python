import tkinter as tk
from tkinter import ttk, messagebox
from DobotEDU import *

# Associazione diretta delle API
api_magician = dobotEdu.magician
api_lite = dobotEdu.m_lite

# --- COSTANTI JOG ---
JOG_IDLE = 0
JOG_X_PLUS = 1
JOG_X_MINUS = 2
JOG_Y_PLUS = 3
JOG_Y_MINUS = 4
JOG_Z_PLUS = 5
JOG_Z_MINUS = 6
JOG_R_PLUS = 7
JOG_R_MINUS = 8
JOG_L_PLUS = 9
JOG_L_MINUS = 10

class NewUniversalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dobot Control Panel - Pro Layout & Conveyor")
        self.root.geometry("700x650") 
        self.root.configure(bg="#2C313C")
        
        self.port = None
        self.is_connected = False
        
        self.setup_styles()
        self.create_widgets()
        self.update_port_list()

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        
        style.configure("TFrame", background="#2C313C")
        style.configure("TLabel", background="#2C313C", foreground="#ABB2BF", font=("Arial", 11, "bold"))
        style.configure("TButton", background="#3E4451", foreground="white", font=("Arial", 10, "bold"), padding=5)
        style.map("TButton", background=[("active", "#528BFF")])
        style.configure("Horizontal.TScale", background="#2C313C")
        
        # Stili per i pulsanti del nastro
        style.configure("Start.TButton", background="#98C379", foreground="black", font=("Arial", 10, "bold"))
        style.map("Start.TButton", background=[("active", "#A3E287")])
        
        style.configure("Stop.TButton", background="#E06C75", foreground="white", font=("Arial", 10, "bold"))
        style.map("Stop.TButton", background=[("active", "#E98B93")])

    def get_api(self):
        """Ritorna l'API corretta in base al robot selezionato."""
        return api_lite if self.combo_device.get() == "Magician Lite" else api_magician

    def create_widgets(self):
        # --- SEZIONE CONNESSIONE ---
        conn_frame = ttk.Frame(self.root)
        conn_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(conn_frame, text="Robot:").pack(side="left", padx=5)
        self.combo_device = ttk.Combobox(conn_frame, values=["Magician", "Magician Lite"], width=12, state="readonly")
        self.combo_device.set("Magician")
        self.combo_device.pack(side="left", padx=5)
        
        ttk.Label(conn_frame, text="Porta:").pack(side="left", padx=5)
        self.port_combo = ttk.Combobox(conn_frame, state="readonly", width=15)
        self.port_combo.pack(side="left", padx=5)
        
        ttk.Button(conn_frame, text="🔄 Aggiorna", command=self.update_port_list).pack(side="left", padx=5)
        self.btn_connect = ttk.Button(conn_frame, text="🔌 Connetti", command=self.toggle_connection)
        self.btn_connect.pack(side="left", padx=10)

        # --- SEZIONE VELOCITA' ROBOT (SLIDER) ---
        speed_frame = ttk.Frame(self.root)
        speed_frame.pack(fill="x", padx=20, pady=10)
        
        ttk.Label(speed_frame, text="Velocità Robot:").pack(side="left", padx=5)
        self.speed_var = tk.DoubleVar(value=50.0) 
        
        self.speed_slider = ttk.Scale(speed_frame, from_=1, to=100, orient="horizontal", variable=self.speed_var, command=self.update_speed_label)
        self.speed_slider.pack(side="left", fill="x", expand=True, padx=10)
        
        # Il parametro viene applicato al robot automaticamente quando si rilascia il mouse
        self.speed_slider.bind("<ButtonRelease-1>", lambda event: self.apply_speed())
        
        self.lbl_speed_val = ttk.Label(speed_frame, text="50%")
        self.lbl_speed_val.pack(side="left", padx=5)

        # --- SEZIONE MOVIMENTO (LE 2 CROCI) ---
        jog_frame = ttk.Frame(self.root)
        jog_frame.pack(pady=20)

        # Croce Sinistra (X e Y)
        left_cross = ttk.Frame(jog_frame)
        left_cross.grid(row=0, column=0, padx=40)
        
        ttk.Label(left_cross, text="Base / Braccio (X-Y)").grid(row=0, column=0, columnspan=3, pady=(0,10))
        
        btn_x_plus = ttk.Button(left_cross, text="X+ (Avanti)", width=12)
        btn_x_plus.grid(row=1, column=1, pady=2)
        self.bind_jog_button(btn_x_plus, JOG_X_PLUS)

        btn_y_plus = ttk.Button(left_cross, text="Y+ (Sinistra)", width=12)
        btn_y_plus.grid(row=2, column=0, padx=2)
        self.bind_jog_button(btn_y_plus, JOG_Y_PLUS)

        ttk.Label(left_cross, text="✛").grid(row=2, column=1)

        btn_y_minus = ttk.Button(left_cross, text="Y- (Destra)", width=12)
        btn_y_minus.grid(row=2, column=2, padx=2)
        self.bind_jog_button(btn_y_minus, JOG_Y_MINUS)

        btn_x_minus = ttk.Button(left_cross, text="X- (Indietro)", width=12)
        btn_x_minus.grid(row=3, column=1, pady=2)
        self.bind_jog_button(btn_x_minus, JOG_X_MINUS)

        # Croce Destra (Z e R)
        right_cross = ttk.Frame(jog_frame)
        right_cross.grid(row=0, column=1, padx=40)
        
        ttk.Label(right_cross, text="Altezza / Rotazione (Z-R)").grid(row=0, column=0, columnspan=3, pady=(0,10))

        btn_z_plus = ttk.Button(right_cross, text="Z+ (Su)", width=12)
        btn_z_plus.grid(row=1, column=1, pady=2)
        self.bind_jog_button(btn_z_plus, JOG_Z_PLUS)

        btn_r_minus = ttk.Button(right_cross, text="R- (Rot. Sx)", width=12)
        btn_r_minus.grid(row=2, column=0, padx=2)
        self.bind_jog_button(btn_r_minus, JOG_R_MINUS)

        ttk.Label(right_cross, text="⟳").grid(row=2, column=1)

        btn_r_plus = ttk.Button(right_cross, text="R+ (Rot. Dx)", width=12)
        btn_r_plus.grid(row=2, column=2, padx=2)
        self.bind_jog_button(btn_r_plus, JOG_R_PLUS)

        btn_z_minus = ttk.Button(right_cross, text="Z- (Giù)", width=12)
        btn_z_minus.grid(row=3, column=1, pady=2)
        self.bind_jog_button(btn_z_minus, JOG_Z_MINUS)

        # --- DIVISORE ---
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", padx=20, pady=10)

        # --- SEZIONE ROTAIA (RAIL) ---
        rail_frame = ttk.Frame(self.root)
        rail_frame.pack(pady=5)
        
        ttk.Label(rail_frame, text="Controllo Rotaia Lineare (L)").pack(side="top", pady=(0,5))
        
        controls_rail = ttk.Frame(rail_frame)
        controls_rail.pack()
        
        btn_l_minus = ttk.Button(controls_rail, text="⬅ L- (Muovi a Sinistra)", width=20)
        btn_l_minus.grid(row=0, column=0, padx=10)
        self.bind_jog_button(btn_l_minus, JOG_L_MINUS)
        
        btn_l_plus = ttk.Button(controls_rail, text="L+ (Muovi a Destra) ➡", width=20)
        btn_l_plus.grid(row=0, column=1, padx=10)
        self.bind_jog_button(btn_l_plus, JOG_L_PLUS)

        # --- DIVISORE ---
        ttk.Separator(self.root, orient="horizontal").pack(fill="x", padx=20, pady=10)

        # --- SEZIONE NASTRO TRASPORTATORE (CONVEYOR) ---
        conveyor_frame = ttk.Frame(self.root)
        conveyor_frame.pack(fill="x", padx=20, pady=5)
        
        # Etichetta e Slider per la velocità del nastro
        conv_speed_subframe = ttk.Frame(conveyor_frame)
        conv_speed_subframe.pack(fill="x", pady=5)
        
        ttk.Label(conv_speed_subframe, text="Velocità Nastro:").pack(side="left", padx=5)
        self.conv_speed_var = tk.IntVar(value=10000) 
        
        self.conv_slider = ttk.Scale(conv_speed_subframe, from_=1000, to=15000, orient="horizontal", variable=self.conv_speed_var, command=self.update_conv_label)
        self.conv_slider.pack(side="left", fill="x", expand=True, padx=10)
        
        self.lbl_conv_speed_val = ttk.Label(conv_speed_subframe, text="10000 pls/s")
        self.lbl_conv_speed_val.pack(side="left", padx=5)

        # Pulsanti Avvia/Ferma Nastro
        conv_btns_subframe = ttk.Frame(conveyor_frame)
        conv_btns_subframe.pack(pady=10)
        
        btn_start_conv = ttk.Button(conv_btns_subframe, text="▶ AVVIA NASTRO", style="Start.TButton", width=20, command=self.start_conveyor)
        btn_start_conv.grid(row=0, column=0, padx=10)
        
        btn_stop_conv = ttk.Button(conv_btns_subframe, text="⏹ FERMA NASTRO", style="Stop.TButton", width=20, command=self.stop_conveyor)
        btn_stop_conv.grid(row=0, column=1, padx=10)

    # --- METODI LOGICI (CONNESSIONE E VELOCITA') ---

    def update_port_list(self):
        try:
            ports = self.get_api().search_dobot()
            if ports:
                port_names = [p["portName"] for p in ports]
                self.port_combo['values'] = port_names
                self.port_combo.set(port_names[0])
            else:
                self.port_combo.set("Nessun robot")
        except Exception as e:
            self.port_combo.set("Errore API")

    def toggle_connection(self):
        if not self.is_connected:
            self.port = self.port_combo.get()
            if not self.port or self.port == "Nessun robot" or self.port == "Errore API":
                messagebox.showerror("Errore", "Seleziona una porta valida!")
                return
            
            try:
                self.get_api().connect_dobot(port_name=self.port)
                self.is_connected = True
                self.btn_connect.config(text="❌ Disconnetti")
                self.combo_device.config(state="disabled")
                self.apply_speed()
                print(f"Connesso a {self.port}")
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile connettersi: {e}")
        else:
            try:
                # Per sicurezza fermiamo nastro e robot prima di disconnettere
                self.stop_conveyor()
                self.stop_jog()
                
                self.get_api().disconnect_dobot(port_name=self.port)
                self.is_connected = False
                self.btn_connect.config(text="🔌 Connetti")
                self.combo_device.config(state="readonly")
                print("Disconnesso.")
            except Exception as e:
                print(f"Errore in disconnessione: {e}")

    def update_speed_label(self, val):
        self.lbl_speed_val.config(text=f"{int(float(val))}%")

    def apply_speed(self):
        if self.is_connected:
            speed_val = int(self.speed_var.get())
            try:
                self.get_api().set_jogcommon_params(port_name=self.port, velocity_ratio=speed_val, acceleration_ratio=speed_val)
                print(f"Velocità JOG impostata a {speed_val}%")
            except Exception as e:
                print(f"Errore impostazione velocità: {e}")

    # --- METODI LOGICI (JOG E ROTAIA) ---

    def bind_jog_button(self, button, cmd_id):
        button.bind("<ButtonPress-1>", lambda event: self.start_jog(cmd_id))
        button.bind("<ButtonRelease-1>", lambda event: self.stop_jog())

    def start_jog(self, cmd_id):
        if self.is_connected:
            try:
                self.get_api().set_jogcmd(port_name=self.port, is_joint=False, cmd=cmd_id, is_queued=False)
            except Exception as e:
                print(f"Errore JOG start: {e}")

    def stop_jog(self):
        if self.is_connected:
            try:
                self.get_api().set_jogcmd(port_name=self.port, is_joint=False, cmd=JOG_IDLE, is_queued=False)
            except Exception as e:
                print(f"Errore JOG stop: {e}")

    # --- METODI LOGICI (NASTRO TRASPORTATORE) ---

    def update_conv_label(self, val):
        self.lbl_conv_speed_val.config(text=f"{int(float(val))} pls/s")

    def start_conveyor(self):
        if self.is_connected:
            speed_val = int(self.conv_speed_var.get())
            try:
                self.get_api().set_converyor(port_name=self.port, index=0, enable=True, speed=speed_val, is_queued=True)
                print(f"Nastro avviato a {speed_val} pls/s")
            except AttributeError:
                self.get_api().set_conveyor(port_name=self.port, index=0, enable=True, speed=speed_val, is_queued=True)
                print(f"Nastro avviato a {speed_val} pls/s")
            except Exception as e:
                print(f"Errore avvio nastro: {e}")
        else:
            messagebox.showwarning("Attenzione", "Devi prima connetterti al robot!")

    def stop_conveyor(self):
        if self.is_connected:
            try:
                self.get_api().set_converyor(port_name=self.port, index=0, enable=False, speed=0, is_queued=True)
                print("Nastro fermato.")
            except AttributeError:
                self.get_api().set_conveyor(port_name=self.port, index=0, enable=False, speed=0, is_queued=True)
                print("Nastro fermato.")
            except Exception as e:
                print(f"Errore stop nastro: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NewUniversalGUI(root)
    root.mainloop()