import tkinter as tk
from tkinter import ttk, messagebox

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

class UniversalDobotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Dobot Control Panel")
        self.root.geometry("750x760")
        self.root.configure(bg="#2C313C")
        
        self.port = None
        self.is_connected = False
        
        # Variabili di riferimento alle API (vengono caricate dinamicamente)
        self.api_magician = None
        self.api_lite = None
        
        self.setup_styles()
        self.create_widgets()
        
        # Carica le librerie Dobot EDU in modo sicuro
        self.init_dobot_api()
        
        # Stato iniziale delle opzioni dinamiche
        self.on_device_change(None)
        self.port_combo.set("Seleziona dispositivo e clicca 🔄")

    def init_dobot_api(self):
        """Tenta l'importazione di DobotEDU senza far crashare l'applicazione."""
        try:
            from DobotEDU import dobotEdu
            self.api_magician = dobotEdu.magician
            self.api_lite = dobotEdu.m_lite
            print(" LIBRERIA DOBOTEDU CARICATA CON SUCCESSO!")
        except Exception as e:
            messagebox.showerror("Errore Libreria", 
                f"Impossibile caricare il modulo DobotEDU.\n"
                f"Dettaglio errore: {e}\n\n"
                f"Verifica che la versione di Python (32/64 bit) sia compatibile "
                f"con i requisiti del tuo ambiente Dobot.")
            self.root.destroy()

    def get_api(self):
        """Restituisce dinamicamente l'oggetto di dobotEdu selezionato."""
        if self.device_var.get() == "Magician":
            return self.api_magician
        else:
            return self.api_lite

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#2C313C")
        style.configure("TLabel", background="#2C313C", foreground="#ABB2BF", font=("Arial", 11))
        style.configure("TButton", background="#3E4451", foreground="white", borderwidth=0, font=("Arial", 10, "bold"))
        style.map("TButton", background=[("active", "#528BFF")])
        style.configure("DPad.TButton", background="#1E222A", foreground="#ABB2BF", width=5, font=("Arial", 10, "bold"))
        style.map("DPad.TButton", background=[("active", "#404754")])
        style.configure("Suck.TButton", background="#98C379", foreground="black", font=("Arial", 10, "bold"))
        style.map("Suck.TButton", background=[("active", "#A3E287")])
        style.configure("Release.TButton", background="#E06C75", foreground="white", font=("Arial", 10, "bold"))
        style.map("Release.TButton", background=[("active", "#E98B93")])
        style.configure("Custom.TCheckbutton", background="#2C313C", foreground="white", font=("Arial", 10, "bold"))

    def create_widgets(self):
        # Top bar
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")
        
        ttk.Label(top_frame, text="Dispositivo:", font=("Arial", 11, "bold"), foreground="white").pack(side="left", padx=(10, 5))
        self.device_var = tk.StringVar(value="Magician Lite")
        self.device_combo = ttk.Combobox(top_frame, textvariable=self.device_var, values=["Magician", "Magician Lite"], width=13, state="readonly")
        self.device_combo.pack(side="left", padx=(0, 15))
        self.device_combo.bind("<<ComboboxSelected>>", self.on_device_change)
        
        ttk.Label(top_frame, text="Porta:").pack(side="left", padx=(0, 5))
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(top_frame, textvariable=self.port_var, width=15, state="readonly")
        self.port_combo.pack(side="left", padx=(0, 5))
        
        self.btn_refresh = ttk.Button(top_frame, text="🔄", width=3, command=self.update_port_list)
        self.btn_refresh.pack(side="left", padx=5)
        
        self.btn_connect = ttk.Button(top_frame, text="Connetti", command=self.toggle_connection)
        self.btn_connect.pack(side="left", padx=10)
        
        self.btn_clear = ttk.Button(top_frame, text="⚠️ Clear Alarms", command=self.clear_alarms)
        self.btn_clear.pack(side="right", padx=5)
        
        self.btn_home = ttk.Button(top_frame, text="🎯 Home", command=self.go_home)
        self.btn_home.pack(side="right", padx=5)

        # Speed bar
        speed_frame = ttk.Frame(self.root, padding=10)
        speed_frame.pack(fill="x")
        ttk.Label(speed_frame, text="Velocità JOG").pack(side="left", padx=10)
        self.speed_scale = ttk.Scale(speed_frame, from_=1, to=100, orient="horizontal", command=self.update_speed)
        self.speed_scale.set(50)
        self.speed_scale.pack(side="left", fill="x", expand=True, padx=10)

        # Main Controls Frame
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill="both", expand=True)

        # Coordinate
        coords_frame = ttk.Frame(main_frame)
        coords_frame.grid(row=0, column=0, padx=20, sticky="n")
        self.lbl_x = ttk.Label(coords_frame, text="X: 0.00", font=("Consolas", 12))
        self.lbl_x.pack(pady=5)
        self.lbl_y = ttk.Label(coords_frame, text="Y: 0.00", font=("Consolas", 12))
        self.lbl_y.pack(pady=5)
        self.lbl_z = ttk.Label(coords_frame, text="Z: 0.00", font=("Consolas", 12))
        self.lbl_z.pack(pady=5)
        self.lbl_r = ttk.Label(coords_frame, text="R: 0.00", font=("Consolas", 12))
        self.lbl_r.pack(pady=5)

        # D-Pad X/Y
        xy_frame = ttk.Frame(main_frame)
        xy_frame.grid(row=0, column=1, padx=25)
        self.create_dpad_button(xy_frame, "X+", 0, 1, JOG_X_PLUS)
        self.create_dpad_button(xy_frame, "X-", 2, 1, JOG_X_MINUS)
        self.create_dpad_button(xy_frame, "Y+", 1, 2, JOG_Y_PLUS)
        self.create_dpad_button(xy_frame, "Y-", 1, 0, JOG_Y_MINUS)

        # D-Pad Z/R
        zr_frame = ttk.Frame(main_frame)
        zr_frame.grid(row=0, column=2, padx=25)
        self.create_dpad_button(zr_frame, "Z+", 0, 1, JOG_Z_PLUS)
        self.create_dpad_button(zr_frame, "Z-", 2, 1, JOG_Z_MINUS)
        self.create_dpad_button(zr_frame, "R+", 1, 2, JOG_R_PLUS)
        self.create_dpad_button(zr_frame, "R-", 1, 0, JOG_R_MINUS)

        # Conveyor Panel
        self.conveyor_frame = ttk.LabelFrame(self.root, text=" Nastro Trasportatore (Conveyor Belt) ", padding=10)
        self.conv_enabled_var = tk.BooleanVar(value=False)
        self.chk_conveyor = ttk.Checkbutton(self.conveyor_frame, text="Attiva Nastro", variable=self.conv_enabled_var, 
                                            style="Custom.TCheckbutton", command=self.toggle_conveyor_widgets)
        self.chk_conveyor.pack(side="left", padx=10)
        self.lbl_conv_speed = ttk.Label(self.conveyor_frame, text="Velocità: 0")
        self.lbl_conv_speed.pack(side="left", padx=5)
        self.conv_speed_scale = ttk.Scale(self.conveyor_frame, from_=-20000, to=20000, orient="horizontal", command=self.on_conveyor_speed_change)
        self.conv_speed_scale.set(0)
        self.conv_speed_scale.pack(side="left", fill="x", expand=True, padx=10)
        self.btn_stop_conv = ttk.Button(self.conveyor_frame, text="🛑 FERMA", command=self.stop_conveyor)
        self.btn_stop_conv.pack(side="right", padx=10)
        self.conv_speed_scale.config(state="disabled")
        self.btn_stop_conv.config(state="disabled")

        # Slideway Panel
        self.slideway_frame = ttk.LabelFrame(self.root, text=" Slideway (Asse Lineare L) ", padding=10)
        self.slide_enabled_var = tk.BooleanVar(value=False)
        self.chk_slideway = ttk.Checkbutton(self.slideway_frame, text="Attiva Slideway", variable=self.slide_enabled_var,
                                            style="Custom.TCheckbutton", command=self.toggle_slideway_widgets)
        self.chk_slideway.pack(side="left", padx=10)
        ttk.Label(self.slideway_frame, text="Vel:").pack(side="left", padx=(5,2))
        
        self.slide_speed_scale = ttk.Scale(self.slideway_frame, from_=10, to=1000, orient="horizontal", length=80, command=self.on_slide_config_change)
        self.slide_speed_scale.set(100)
        self.slide_speed_scale.pack(side="left", padx=5)
        
        self.lbl_slide_pos = ttk.Label(self.slideway_frame, text="Pos L: 0")
        self.lbl_slide_pos.pack(side="left", padx=(10, 5))
        self.slide_pos_scale = ttk.Scale(self.slideway_frame, from_=0, to=1000, orient="horizontal", command=self.on_slide_pos_change)
        self.slide_pos_scale.set(0)
        self.slide_pos_scale.pack(side="left", fill="x", expand=True, padx=10)
        self.slide_speed_scale.config(state="disabled")
        self.slide_pos_scale.config(state="disabled")

        # Suction Cup Panel
        self.suction_frame = ttk.LabelFrame(self.root, text=f" End Effector: Suction Cup ({self.device_var.get()}) ", padding=10)
        self.suction_frame.pack(fill="x", padx=20, pady=10)
        self.btn_suck = ttk.Button(self.suction_frame, text="🟢 PRENDI (Suck On)", style="Suck.TButton", command=self.suction_on)
        self.btn_suck.pack(side="left", expand=True, fill="x", padx=10)
        self.btn_release = ttk.Button(self.suction_frame, text="🔴 RILASCIA (Suck Off)", style="Release.TButton", command=self.suction_off)
        self.btn_release.pack(side="left", expand=True, fill="x", padx=10)

    def create_dpad_button(self, parent, text, row, col, cmd_id):
        btn = ttk.Button(parent, text=text, style="DPad.TButton")
        btn.grid(row=row, column=col, padx=5, pady=5, ipadx=8, ipady=8)
        btn.bind("<ButtonPress-1>", lambda e: self.start_jog(cmd_id))
        btn.bind("<ButtonRelease-1>", lambda e: self.stop_jog())

    def on_device_change(self, event):
        self.port_combo.set("Clicca 🔄 per cercare")
        self.suction_frame.config(text=f" End Effector: Suction Cup ({self.device_var.get()}) ")
        if self.device_var.get() == "Magician":
            self.suction_frame.pack_forget()
            self.conveyor_frame.pack(fill="x", padx=20, pady=5)
            self.slideway_frame.pack(fill="x", padx=20, pady=5)
            self.suction_frame.pack(fill="x", padx=20, pady=10)
        else:
            self.stop_conveyor()
            self.conv_enabled_var.set(False)
            self.toggle_conveyor_widgets()
            self.slide_enabled_var.set(False)
            self.toggle_slideway_widgets()
            self.conveyor_frame.pack_forget()
            self.slideway_frame.pack_forget()
        
        # Svuota la lista delle porte al cambio del dispositivo per forzare il refresh
        self.port_combo['values'] = []

    # --- SLIDERAIL LOGIC ---
    def toggle_slideway_widgets(self):
        if self.slide_enabled_var.get():
            self.slide_speed_scale.config(state="normal")
            self.slide_pos_scale.config(state="normal")
            if self.is_connected and self.device_var.get() == "Magician":
                try:
                    self.api_magician.set_device_withl(port_name=self.port, enable=True, version=1, is_queued=True)
                    self.on_slide_config_change(self.slide_speed_scale.get())
                except Exception as e: print(f"Errore: {e}")
        else:
            self.slide_speed_scale.config(state="disabled")
            self.slide_pos_scale.config(state="disabled")
            if self.is_connected and self.device_var.get() == "Magician":
                try: self.api_magician.set_device_withl(port_name=self.port, enable=False, version=1, is_queued=True)
                except Exception as e: print(f"Errore: {e}")

    def on_slide_config_change(self, val):
        if self.is_connected and self.device_var.get() == "Magician" and self.slide_enabled_var.get():
            try: self.api_magician.set_ptpl_params(port_name=self.port, velocity=float(val), acceleration=float(val), is_queued=False)
            except Exception as e: print(f"Errore: {e}")

    def on_slide_pos_change(self, val):
        target_l = float(val)
        self.lbl_slide_pos.config(text=f"Pos L: {target_l:.0f}")
        if self.is_connected and self.device_var.get() == "Magician" and self.slide_enabled_var.get():
            try:
                pose = self.api_magician.get_pose(port_name=self.port)
                if pose:
                    self.api_magician.set_ptpwithl_cmd(
                        port_name=self.port, mode=1,
                        x=pose.get('x', 0.0), y=pose.get('y', 0.0), z=pose.get('z', 0.0), r=pose.get('r', 0.0),
                        set_l=target_l, is_queued=True, is_wait=False
                    )
            except Exception as e: print(f"Errore: {e}")

    # --- CONVEYOR LOGIC ---
    def toggle_conveyor_widgets(self):
        if self.conv_enabled_var.get():
            self.conv_speed_scale.config(state="normal")
            self.btn_stop_conv.config(state="normal")
        else:
            self.stop_conveyor()
            self.conv_speed_scale.config(state="disabled")
            self.btn_stop_conv.config(state="disabled")

    def on_conveyor_speed_change(self, val):
        speed_val = int(float(val))
        self.lbl_conv_speed.config(text=f"Velocità: {speed_val}")
        if self.is_connected and self.device_var.get() == "Magician" and self.conv_enabled_var.get():
            try: self.api_magician.set_converyor(port_name=self.port, index=0, enable=True, speed=speed_val, is_queued=False)
            except Exception as e: print(f"Errore: {e}")

    def stop_conveyor(self):
        self.conv_speed_scale.set(0)
        self.lbl_conv_speed.config(text="Velocità: 0")
        if self.is_connected and self.device_var.get() == "Magician":
            try: self.api_magician.set_converyor(port_name=self.port, index=0, enable=False, speed=0, is_queued=False)
            except Exception as e: print(f"Errore: {e}")

    # --- STANDARD APP FUNCS ---
    def update_port_list(self):
        """
        Scansiona le porte COM attive.
        Nota: DobotLink mostrerà tutte le porte seriali compatibili a prescindere dal modello,
        poiché il riconoscimento hardware completo avviene solo dopo la connessione.
        """
        try:
            ports = self.get_api().search_dobot()
            port_names = [p["portName"] for p in ports] if ports else []
            
            self.port_combo['values'] = port_names
            if port_names: 
                self.port_combo.current(0)
            else: 
                self.port_combo.set("Nessun robot trovato")
        except Exception as e: 
            self.port_combo.set("Errore DobotLink")

    def toggle_connection(self):
        current_api = self.get_api()
        selected_device = self.device_var.get()

        if not self.is_connected:
            self.port = self.port_var.get()
            if self.port and self.port not in ["Nessun robot trovato", "Seleziona dispositivo e clicca 🔄", "Clicca 🔄 per cercare", "Errore DobotLink"]:
                try:
                    # Tenta la connessione fisica
                    current_api.connect_dobot(port_name=self.port)
                    
                    # CONTROLLO INCROCIATO DI SICUREZZA DOPO LA CONNESSIONE
                    # Interroghiamo i parametri del dispositivo per verificare l'effettiva identità del robot
                    try:
                        dev_info = current_api.get_device_version(port_name=self.port)
                        # Molte risposte includono il nome del modello, o possiamo dedurlo dai dati.
                        # Cerchiamo di validare in base a stringhe note nel dizionario restituito.
                        device_str = str(dev_info).lower()
                        
                        if selected_device == "Magician" and "lite" in device_str:
                            raise ValueError("Rilevato Magician Lite ma hai selezionato Magician!")
                        elif selected_device == "Magician Lite" and "lite" not in device_str and "magician" in device_str:
                            raise ValueError("Rilevato Magician Standard ma hai selezionato Magician Lite!")
                    except Exception as ver_err:
                        # Se il controllo fallisce esplicitamente a causa del mismatch di modello
                        if "Rilevato" in str(ver_err):
                            current_api.disconnect_dobot(port_name=self.port)
                            messagebox.showerror("Errore Modello", f"Accoppiamento fallito:\n{ver_err}\n\nCambia il tipo di dispositivo nel menu a tendina.")
                            self.port = None
                            return
                        # Altri errori minori di lettura versione vengono ignorati pur di connettere

                    self.is_connected = True
                    self.btn_connect.config(text="Disconnetti")
                    self.port_combo.config(state="disabled")
                    self.device_combo.config(state="disabled")
                    self.update_speed(self.speed_scale.get())
                    self.read_pose_loop()
                except Exception as e: 
                    messagebox.showerror("Errore", f"Impossibile connettersi:\n{e}")
        else:
            self.suction_off()
            if selected_device == "Magician":
                self.stop_conveyor()
                if self.slide_enabled_var.get():
                    try: self.api_magician.set_device_withl(port_name=self.port, enable=False, version=1, is_queued=True)
                    except Exception: pass
            try: 
                current_api.disconnect_dobot(port_name=self.port)
            except Exception: 
                pass
            self.is_connected = False
            self.btn_connect.config(text="Connetti")
            self.port_combo.config(state="readonly")
            self.device_combo.config(state="readonly")
            self.port = None

    def go_home(self):
        if self.is_connected:
            try:
                self.btn_home.config(state="disabled")
                self.get_api().set_homecmd(port_name=self.port)
                self.root.after(15000, lambda: self.btn_home.config(state="normal"))
            except Exception as e: self.btn_home.config(state="normal")

    def clear_alarms(self):
        if self.is_connected:
            try: self.get_api().clear_allalarms_state(port_name=self.port)
            except Exception: pass

    def update_speed(self, val):
        if self.is_connected:
            try: self.get_api().set_jogcommon_params(port_name=self.port, velocity_ratio=float(val), acceleration_ratio=float(val))
            except Exception: pass

    def start_jog(self, cmd_id):
        if self.is_connected:
            try: self.get_api().set_jogcmd(port_name=self.port, is_joint=False, cmd=cmd_id, is_queued=False)
            except Exception: pass

    def stop_jog(self):
        if self.is_connected:
            try: self.get_api().set_jogcmd(port_name=self.port, is_joint=False, cmd=JOG_IDLE, is_queued=False)
            except Exception: pass

    def suction_on(self):
        if self.is_connected:
            try: self.get_api().set_endeffector_suctioncup(port_name=self.port, enable=True, on=True, is_queued=False)
            except Exception: pass

    def suction_off(self):
        if self.is_connected:
            try:
                self.get_api().set_endeffector_suctioncup(port_name=self.port, enable=True, on=False, is_queued=False)
                self.root.after(250, self._turn_off_compressor)
            except Exception: pass

    def _turn_off_compressor(self):
        if self.is_connected:
            try: self.get_api().set_endeffector_suctioncup(port_name=self.port, enable=False, on=False, is_queued=False)
            except Exception: pass

    def read_pose_loop(self):
        if self.is_connected:
            try:
                pose = self.get_api().get_pose(port_name=self.port)
                if pose:
                    self.lbl_x.config(text=f"X: {pose.get('x', 0.0):.2f}")
                    self.lbl_y.config(text=f"Y: {pose.get('y', 0.0):.2f}")
                    self.lbl_z.config(text=f"Z: {pose.get('z', 0.0):.2f}")
                    self.lbl_r.config(text=f"R: {pose.get('r', 0.0):.2f}")
            except Exception: pass
            self.root.after(200, self.read_pose_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalDobotGUI(root)
    root.mainloop()