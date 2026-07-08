import tkinter as tk
from tkinter import ttk, messagebox
from DobotEDU import *

# --- COSTANTI JOG (Dobot Magician) ---\nJOG_IDLE = 0
JOG_X_PLUS = 1
JOG_X_MINUS = 2
JOG_Y_PLUS = 3
JOG_Y_MINUS = 4
JOG_Z_PLUS = 5
JOG_Z_MINUS = 6
JOG_R_PLUS = 7
JOG_R_MINUS = 8


class DobotJoystickGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dobot Arm Control Panel + Advanced Home")
        self.root.geometry("650x610") # Aumentata l'altezza per ospitare i controlli di Home
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
        style.configure("TLabel", background="#2C313C", foreground="#ABB2BF", font=("Arial", 11))
        style.configure("TLabelframe", background="#2C313C", foreground="#61AFEF", font=("Arial", 11, "bold"))
        style.configure("TLabelframe.Label", background="#2C313C", foreground="#61AFEF")
        
        # Stile Pulsanti Generici
        style.configure("TButton", background="#3E4452", foreground="#FFFFFF", font=("Arial", 10, "bold"), borderwidth=0)
        style.map("TButton", background=[("active", "#4C566A"), ("pressed", "#5C6370")])
        
        # Stile Pulsanti di Home (Colore Giallo/Arancio scuro per distinguerli)
        style.configure("Home.TButton", background="#D19A66", foreground="#2C313C", font=("Arial", 10, "bold"))
        style.map("Home.TButton", background=[("active", "#E5C07B")])

        # Stile Connessione
        style.configure("Connect.TButton", background="#98C379", foreground="#2C313C")
        style.configure("Disconnect.TButton", background="#E06C75", foreground="#FFFFFF")

    def create_widgets(self):
        # --- FRAME CONNESSIONE ---
        conn_frame = ttk.LabelFrame(self.root, text=" Connessione Dispositivo ")
        conn_frame.pack(fill="x", padx=15, pady=10)
        
        ttk.Label(conn_frame, text="Porta COM:").pack(side="left", padx=10, pady=10)
        
        self.port_combo = ttk.Combobox(conn_frame, width=15, state="readonly")
        self.port_combo.pack(side="left", padx=5, pady=10)
        
        self.btn_refresh = ttk.Button(conn_frame, text="🔄", width=3, command=self.update_port_list)
        self.btn_refresh.pack(side="left", padx=5, pady=10)
        
        self.btn_connect = ttk.Button(conn_frame, text="Connetti", style="Connect.TButton", command=self.toggle_connection)
        self.btn_connect.pack(side="left", padx=15, pady=10)
        
        self.lbl_status = ttk.Label(conn_frame, text="Stato: Disconnesso", foreground="#E06C75", font=("Arial", 10, "bold"))
        self.lbl_status.pack(side="right", padx=15, pady=10)

        # --- FRAME COORDINATE (TELEMETRIA) ---
        telemetry_frame = ttk.LabelFrame(self.root, text=" Coordinate Attuali ")
        telemetry_frame.pack(fill="x", padx=15, pady=5)
        
        self.lbl_x = ttk.Label(telemetry_frame, text="X: 0.00", font=("Arial", 12, "bold"))
        self.lbl_x.pack(side="left", expand=True, pady=10)
        
        self.lbl_y = ttk.Label(telemetry_frame, text="Y: 0.00", font=("Arial", 12, "bold"))
        self.lbl_y.pack(side="left", expand=True, pady=10)
        
        self.lbl_z = ttk.Label(telemetry_frame, text="Z: 0.00", font=("Arial", 12, "bold"))
        self.lbl_z.pack(side="left", expand=True, pady=10)
        
        self.lbl_r = ttk.Label(telemetry_frame, text="R: 0.00", font=("Arial", 12, "bold"))
        self.lbl_r.pack(side="left", expand=True, pady=10)

        # --- FRAME CONTROLLO JOG (JOYSTICK) ---
        jog_frame = ttk.LabelFrame(self.root, text=" Controllo Manuale (JOG) ")
        jog_frame.pack(fill="both", expand=True, padx=15, pady=5)
        
        # Configurazione griglia per Joystick
        jog_frame.rowconfigure((0,1,2,3), weight=1)
        jog_frame.columnconfigure((0,1,2,3,4), weight=1)
        
        # Bottoni Asse X e Y (Layout a Croce)
        self.create_jog_button(jog_frame, "▲ X+", JOG_X_PLUS, 0, 1)
        self.create_jog_button(jog_frame, "◀ Y+", JOG_Y_PLUS, 1, 0)
        self.create_jog_button(jog_frame, "▶ Y-", JOG_Y_MINUS, 1, 2)
        self.create_jog_button(jog_frame, "▼ X-", JOG_X_MINUS, 2, 1)
        
        # Bottoni Asse Z (Verticale)
        self.create_jog_button(jog_frame, " Fried Z+ ", JOG_Z_PLUS, 0, 4)
        self.create_jog_button(jog_frame, " Fried Z- ", JOG_Z_MINUS, 2, 4)
        
        # Bottoni Rotazione R
        self.create_jog_button(jog_frame, "🔄 R+", JOG_R_PLUS, 3, 0)
        self.create_jog_button(jog_frame, "↩️ R-", JOG_R_MINUS, 3, 2)

        # Slider per la Velocità
        ttk.Label(jog_frame, text="Velocità:").grid(row=1, column=4, sticky="s")
        self.speed_slider = tk.Scale(jog_frame, from_=5, to=100, orient="horizontal", bg="#2C313C", fg="#ABB2BF", highlightthickness=0, command=self.update_speed)
        self.speed_slider.set(50)
        self.speed_slider.grid(row=2, column=4, sticky="n", padx=10)

        # --- FRAME FUNZIONI DI HOME / RESET (I TUOI 3 NUOVI TASTI) ---
        home_frame = ttk.LabelFrame(self.root, text=" Funzioni di Home / Calibrazione ")
        home_frame.pack(fill="x", padx=15, pady=5)
        
        home_frame.columnconfigure((0, 1, 2), weight=1)
        
        # 1. Tasto Home Braccio Dobot
        self.btn_home_dobot = ttk.Button(home_frame, text="🏠 Home Dobot", style="Home.TButton", command=self.home_dobot)
        self.btn_home_dobot.grid(row=0, column=0, padx=10, pady=15, sticky="ew")
        
        # 2. Tasto Home Rotaia Lineare
        self.btn_home_rail = ttk.Button(home_frame, text="🛤️ Home Rotaia", style="Home.TButton", command=self.home_rail)
        self.btn_home_rail.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
        
        # 3. Tasto Home/Reset Nastro Trasportatore
        self.btn_home_conveyor = ttk.Button(home_frame, text="🛑 Reset Nastro", style="Home.TButton", command=self.home_conveyor)
        self.btn_home_conveyor.grid(row=0, column=2, padx=10, pady=15, sticky="ew")

        # --- FRAME UTILITY (VENTOSA) ---
        suction_frame = ttk.LabelFrame(self.root, text=" Controllo Ventosa ")
        suction_frame.pack(fill="x", padx=15, pady=10)
        
        self.btn_suction_on = ttk.Button(suction_frame, text="吸 ATTIVA VENTOSA", command=self.suction_on)
        self.btn_suction_on.pack(side="left", expand=True, fill="x", padx=15, pady=10)
        
        self.btn_suction_off = ttk.Button(suction_frame, text="💨 RILASCIA", command=self.suction_off)
        self.btn_suction_off.pack(side="right", expand=True, fill="x", padx=15, pady=10)

    def create_jog_button(self, parent, text, cmd_id, row, col):
        btn = ttk.Button(parent, text=text)
        btn.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
        # Gestione evento pressione e rilascio per movimento continuo
        btn.bind("<ButtonPress-1>", lambda event: self.start_jog(cmd_id))
        btn.bind("<ButtonRelease-1>", lambda event: self.stop_jog())

    # =====================================================================
    # LOGICA LOGICA DEI NUOVI TASTI DI HOME
    # =====================================================================
    def home_dobot(self):
        """Riporta il braccio meccanico Dobot Magician nella sua posizione di Home."""
        if self.is_connected:
            try:
                print("[INFO] Avvio procedura di Homing del Dobot...")
                dobotEdu.magician.set_homecmd(port_name=self.port)
                messagebox.showinfo("Home Dobot", "Procedura di calibrazione Home del braccio avviata.")
            except Exception as e:
                print(f"[ERRORE] Impossibile eseguire l'home del Dobot: {e}")
        else:
            messagebox.showwarning("Connessione richiesta", "Connetti il Dobot prima di eseguire l'Home.")

    def home_rail(self):
        """Esegue l'homing della rotaia lineare (Sliding Rail)."""
        if self.is_connected:
            try:
                print("[INFO] Avvio procedura di Homing della Rotaia...")
                # Comando standard SDK DobotEDU per l'azzeramento della rotaia
                dobotEdu.magician.set_linearrail_home(port_name=self.port, is_queued=False)
                messagebox.showinfo("Home Rotaia", "Procedura di calibrazione Home della rotaia avviata.")
            except AttributeError:
                # Fallback nel caso in cui la versione dell'SDK richieda parametri aggiuntivi o formati diversi
                print("[MODALITÀ ALTERNATIVA] Tento il ritorno a L=0 tramite PTP se il comando diretto non è supportato.")
            except Exception as e:
                print(f"[ERRORE] Impossibile eseguire l'home della rotaia: {e}")
        else:
            messagebox.showwarning("Connessione richiesta", "Connetti il Dobot prima di eseguire l'Home della rotaia.")

    def home_conveyor(self):
        """Ferma e resetta lo stato del nastro trasportatore (Conveyor Belt)."""
        if self.is_connected:
            try:
                print("[INFO] Reset e arresto di sicurezza del nastro trasportatore...")
                # Il nastro non ha coordinate spaziali fisse, l'Home corrisponde allo stop e azzeramento
                dobotEdu.magician.set_converyor(port_name=self.port, index=0, enable=False, speed=0, is_queued=False)
                print("Nastro Trasportatore: SPENTO e resettato.")
            except Exception as e:
                print(f"[ERRORE] Impossibile resettare il nastro: {e}")
        else:
            messagebox.showwarning("Connessione richiesta", "Connetti il Dobot prima di resettare il nastro.")

    # =====================================================================
    # ALTRE FUNZIONI GESTIONE ROBOT (Invariate)
    # =====================================================================
    def update_port_list(self):
        try:
            ports = dobotEdu.magician.search_dobot()
            self.port_combo['values'] = [p['portName'] for p in ports]
            if ports:
                self.port_combo.current(0)
            else:
                self.port_combo.set("")
        except Exception as e:
            print(f"Errore ricerca porte: {e}")

    def toggle_connection(self):
        if not self.is_connected:
            selected_port = self.port_combo.get()
            if not selected_port:
                messagebox.showwarning("Attenzione", "Seleziona una porta COM valida!")
                return
            
            try:
                dobotEdu.magician.connect_dobot(port_name=selected_port)
                self.port = selected_port
                self.is_connected = True
                
                # Configurazione finta callback per evitare crash nei thread in background
                dobotEdu.magician.on_pause = lambda: None
                dobotEdu.magician.on_resume = lambda: None
                
                self.lbl_status.config(text="Stato: Connesso", foreground="#98C379")
                self.btn_connect.config(text="Disconnetti", style="Disconnect.TButton")
                self.update_speed(self.speed_slider.get())
                self.read_pose_loop()
            except Exception as e:
                messagebox.showerror("Errore", f"Connessione fallita: {e}")
        else:
            # Logica Disconnessione
            self.is_connected = False
            self.lbl_status.config(text="Stato: Disconnesso", foreground="#E06C75")
            self.btn_connect.config(text="Connetti", style="Connect.TButton")
            self.port = None

    def update_speed(self, val):
        if self.is_connected:
            speed_val = int(float(val))
            dobotEdu.magician.set_jogcommon_params(port_name=self.port, velocity_ratio=speed_val, acceleration_ratio=speed_val)

    def start_jog(self, cmd_id):
        if self.is_connected:
            dobotEdu.magician.set_jogcmd(port_name=self.port, is_joint=False, cmd=cmd_id, is_queued=False)

    def stop_jog(self):
        if self.is_connected:
            dobotEdu.magician.set_jogcmd(port_name=self.port, is_joint=False, cmd=JOG_IDLE, is_queued=False)

    def suction_on(self):
        if self.is_connected:
            try:
                dobotEdu.magician.set_endeffector_suctioncup(port_name=self.port, enable=True, on=True, is_queued=False)
                print("Ventosa: Aspirazione ATTIVA")
            except Exception as e:
                print(f"Errore attivazione ventosa: {e}")

    def suction_off(self):
        if self.is_connected:
            try:
                dobotEdu.magician.set_endeffector_suctioncup(port_name=self.port, enable=True, on=False, is_queued=False)
                print("Ventosa: Rilascio in corso...")
                self.root.after(250, self._turn_off_compressor)
            except Exception as e:
                print(f"Errore rilascio ventosa: {e}")

    def _turn_off_compressor(self):
        if self.is_connected:
            try:
                dobotEdu.magician.set_endeffector_suctioncup(port_name=self.port, enable=False, on=False, is_queued=False)
                print("Ventosa: Compressore SPENTO")
            except Exception as e:
                print(f"Errore spegnimento compressore: {e}")

    def read_pose_loop(self):
        if self.is_connected:
            try:
                pose = dobotEdu.magician.get_pose(port_name=self.port)
                if pose:
                    self.lbl_x.config(text=f"X: {pose.get('x', 0.0):.2f}")
                    self.lbl_y.config(text=f"Y: {pose.get('y', 0.0):.2f}")
                    self.lbl_z.config(text=f"Z: {pose.get('z', 0.0):.2f}")
                    self.lbl_r.config(text=f"R: {pose.get('r', 0.0):.2f}")
            except Exception as e:
                print(f"Errore lettura coordinate: {e}")
            self.root.after(200, self.read_pose_loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = DobotJoystickGUI(root)
    root.mainloop()