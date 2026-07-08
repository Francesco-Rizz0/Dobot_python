#NON FUNZIONANATE!!!
import tkinter as tk
from tkinter import ttk, messagebox
from DobotEDU import *

# Associazione delle API reali provenienti dalla libreria DobotEDU per i due modelli supportati
api_magician = dobotEdu.magician
api_lite = dobotEdu.m_lite

# --- COSTANTI JOG ---
# Identificativi numerici richiesti dal firmware del robot per definire la direzione del movimento manuale
JOG_IDLE = 0       # Stato di riposo / Arresto del movimento
JOG_X_PLUS = 1     # Movimento in avanti lungo l'asse X
JOG_X_MINUS = 2    # Movimento all'indietro lungo l'asse X
JOG_Y_PLUS = 3     # Movimento verso sinistra lungo l'asse Y
JOG_Y_MINUS = 4    # Movimento verso destra lungo l'asse Y
JOG_Z_PLUS = 5     # Movimento verso l'alto (sollevamento) lungo l'asse Z
JOG_Z_MINUS = 6    # Movimento verso il basso (discesa) lungo l'asse Z
JOG_R_PLUS = 7     # Rotazione dell'end-effector in senso antiorario (asse R)
JOG_R_MINUS = 8    # Rotazione dell'end-effector in senso orario (asse R)

class UniversalDobotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Dobot Control Panel V4")
        self.root.geometry("850x780") 
        self.root.configure(bg="#2C313C")
        
        self.port = None
        self.is_connected = False
        self.user_interacting_with_rail = False 
        
        self.setup_styles()
        self.create_widgets()
        
        self.port_combo.set("Seleziona dispositivo e clicca 🔄")

    def setup_styles(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#2C313C")
        style.configure("Card.TFrame", background="#21252B", relief="solid", borderwidth=1)
        style.configure("TLabel", background="#2C313C", foreground="#ABB2BF", font=("Segoe UI", 10))
        style.configure("Title.TLabel", background="#21252B", foreground="#61AFEF", font=("Segoe UI", 12, "bold"))
        style.configure("Coord.TLabel", background="#21252B", foreground="#98C379", font=("Consolas", 14, "bold"))
        style.configure("Status.TLabel", background="#21252B", foreground="#E5C07B", font=("Segoe UI", 10, "italic"))
        style.configure("TButton", background="#3E4451", foreground="#FFFFFF", font=("Segoe UI", 10, "bold"), borderwidth=0)
        style.map("TButton", background=[("active", "#4C5262"), ("pressed", "#2C313C")])
        style.configure("Accent.TButton", background="#98C379", foreground="#21252B", font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#A3D18A")])
        style.configure("Home.TButton", background="#E06C75", foreground="#FFFFFF", font=("Segoe UI", 11, "bold"))
        style.map("Home.TButton", background=[("active", "#E6818A")])
        style.configure("TRadiobutton", background="#21252B", foreground="#ABB2BF", font=("Segoe UI", 10))

    def create_widgets(self):
        # --- COLONNA SINISTRA ---
        left_container = ttk.Frame(self.root, style="TFrame")
        left_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Box Connessione
        frame_conn = ttk.Frame(left_container, style="Card.TFrame", padding=15)
        frame_conn.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame_conn, text="🔌 CONNESSIONE DISPOSITIVO", style="Title.TLabel").pack(anchor=tk.W, pady=(0, 10))
        self.model_var = tk.StringVar(value="magician")
        
        self.radio_magician = ttk.Radiobutton(frame_conn, text="Dobot Magician (Standard)", variable=self.model_var, value="magician")
        self.radio_magician.pack(anchor=tk.W, pady=2)
        self.radio_lite = ttk.Radiobutton(frame_conn, text="Dobot Magician Lite", variable=self.model_var, value="lite")
        self.radio_lite.pack(anchor=tk.W, pady=(2, 10))
        
        combo_frame = ttk.Frame(frame_conn, style="TFrame")
        combo_frame.pack(fill=tk.X, pady=5)
        self.port_combo = ttk.Combobox(combo_frame, state="readonly", font=("Segoe UI", 10))
        self.port_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(combo_frame, text="🔄", width=4, command=self.update_port_list).pack(side=tk.RIGHT)
        
        self.btn_toggle_connect = ttk.Button(frame_conn, text="CONNETTI ROBOT", style="Accent.TButton", command=self.toggle_connection)
        self.btn_toggle_connect.pack(fill=tk.X, pady=(10, 5))
        
        # Box Posizione Reale
        frame_status = ttk.Frame(left_container, style="Card.TFrame", padding=15)
        frame_status.pack(fill=tk.X, pady=(0, 15))
        
        ttk.Label(frame_status, text="📊 POSIZIONE REALE", style="Title.TLabel").pack(anchor=tk.W, pady=(0, 15))
        self.lbl_x = ttk.Label(frame_status, text="X: 0.00", style="Coord.TLabel")
        self.lbl_x.pack(anchor=tk.W, pady=3)
        self.lbl_y = ttk.Label(frame_status, text="Y: 0.00", style="Coord.TLabel")
        self.lbl_y.pack(anchor=tk.W, pady=3)
        self.lbl_z = ttk.Label(frame_status, text="Z: 0.00", style="Coord.TLabel")
        self.lbl_z.pack(anchor=tk.W, pady=3)
        self.lbl_r = ttk.Label(frame_status, text="R: 0.00", style="Coord.TLabel")
        self.lbl_r.pack(anchor=tk.W, pady=3)
        self.lbl_l = ttk.Label(frame_status, text="L (Rotaia): 0.00", style="Coord.TLabel")
        self.lbl_l.pack(anchor=tk.W, pady=3)
        self.lbl_status_msg = ttk.Label(frame_status, text="Stato: Disconnesso", style="Status.TLabel")
        self.lbl_status_msg.pack(anchor=tk.W, pady=(15, 0))

        # Box: Controllo Nastro Trasportatore
        frame_conveyor = ttk.Frame(left_container, style="Card.TFrame", padding=15)
        frame_conveyor.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame_conveyor, text="🛤️ CONTROLLO NASTRO TRASPORTATORE", style="Title.TLabel").pack(anchor=tk.W, pady=(0, 10))
        ttk.Label(frame_conveyor, text="Velocità Nastro (-10000 a +10000):", background="#21252B").pack(anchor=tk.W, pady=(5, 0))
        
        self.conveyor_slider = tk.Scale(
            frame_conveyor, from_=-10000, to=10000, orient=tk.HORIZONTAL, 
            bg="#21252B", fg="#61AFEF", highlightthickness=0, command=self.update_conveyor_speed
        )
        self.conveyor_slider.set(0)
        self.conveyor_slider.pack(fill=tk.X, pady=(5, 10))
        
        ttk.Button(frame_conveyor, text="STOP NASTRO", command=self.stop_conveyor).pack(fill=tk.X, pady=2)

        # --- COLONNA DESTRA ---
        right_container = ttk.Frame(self.root, style="TFrame")
        right_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        frame_jog = ttk.Frame(right_container, style="Card.TFrame", padding=15)
        frame_jog.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        ttk.Label(frame_jog, text="🕹️ CONTROLLO MANUALE (JOG)", style="Title.TLabel").grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        self.create_jog_button(frame_jog, "X + (Avanti)", JOG_X_PLUS, row=1, col=0)
        self.create_jog_button(frame_jog, "X - (Indietro)", JOG_X_MINUS, row=1, col=1)
        self.create_jog_button(frame_jog, "Y + (Sinistra)", JOG_Y_PLUS, row=2, col=0)
        self.create_jog_button(frame_jog, "Y - (Destra)", JOG_Y_MINUS, row=2, col=1)
        self.create_jog_button(frame_jog, "Z + (Su)", JOG_Z_PLUS, row=3, col=0)
        self.create_jog_button(frame_jog, "Z - (Giù)", JOG_Z_MINUS, row=3, col=1)
        self.create_jog_button(frame_jog, "R + (Rotazione L)", JOG_R_PLUS, row=4, col=0)
        self.create_jog_button(frame_jog, "R - (Rotazione R)", JOG_R_MINUS, row=4, col=1)
        
        ttk.Label(frame_jog, text="Velocità Movimento Braccio:", background="#21252B").grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(15, 2))
        self.speed_slider = tk.Scale(frame_jog, from_=5, to=100, orient=tk.HORIZONTAL, bg="#21252B", fg="#61AFEF", highlightthickness=0, command=self.update_speed)
        self.speed_slider.set(40)
        self.speed_slider.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        
        ttk.Button(frame_jog, text="🏠 RESET & HOME ROBOT", command=self.run_robot_home, style="Home.TButton").grid(row=7, column=0, columnspan=2, pady=(5, 0), sticky="ew", ipady=4)
        
        frame_effector = ttk.Frame(right_container, style="Card.TFrame", padding=15)
        frame_effector.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(frame_effector, text="🧲 SUCTION CUP", style="Title.TLabel").pack(anchor=tk.W, pady=(0, 10))
        suction_frame = ttk.Frame(frame_effector, style="TFrame")
        suction_frame.pack(fill=tk.X)
        ttk.Button(suction_frame, text="VENTOSA ON", style="Accent.TButton", command=self.suction_on).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        ttk.Button(suction_frame, text="VENTOSA OFF", command=self.suction_off).pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        frame_rail = ttk.Frame(right_container, style="Card.TFrame", padding=15)
        frame_rail.pack(fill=tk.X)
        ttk.Label(frame_rail, text="🛤️ CONTROLLO ROTAIA", style="Title.TLabel").pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Button(frame_rail, text="🏠 HOME ROTAIA (L=0)", style="Home.TButton", command=self.home_rail).pack(fill=tk.X, pady=(0, 10), ipady=3)
        
        ttk.Label(frame_rail, text="Velocità Rotaia (%):", background="#21252B").pack(anchor=tk.W, pady=(5, 0))
        self.rail_speed_slider = tk.Scale(frame_rail, from_=5, to=100, orient=tk.HORIZONTAL, bg="#21252B", fg="#E5C07B", highlightthickness=0, command=self.update_rail_speed)
        self.rail_speed_slider.set(40)
        self.rail_speed_slider.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(frame_rail, text="Posizione Target Rotaia (0 - 1000 mm):", background="#21252B").pack(anchor=tk.W, pady=(0, 2))
        self.rail_slider = tk.Scale(frame_rail, from_=0, to=1000, orient=tk.HORIZONTAL, bg="#21252B", fg="#98C379", highlightthickness=0)
        self.rail_slider.pack(fill=tk.X, pady=(0, 5))
        
        self.rail_slider.bind("<ButtonPress-1>", self.start_rail_interaction)
        self.rail_slider.bind("<ButtonRelease-1>", self.move_rail_to_slider_pos)

    def create_jog_button(self, parent, text, cmd_id, row, col):
        btn = ttk.Button(parent, text=text)
        btn.grid(row=row, column=col, padx=5, pady=4, sticky="ew")
        # Il click premuto (<ButtonPress-1>) avvia l'invio continuo del comando JOG
        btn.bind("<ButtonPress-1>", lambda event: self.start_jog(cmd_id))
        # Il rilascio del click (<ButtonRelease-1>) ferma immediatamente il movimento impostando lo stato IDLE
        btn.bind("<ButtonRelease-1>", lambda event: self.stop_jog())

    def get_api(self):
        """
        Restituisce l'istanza corretta delle API di DobotEDU in base al modello selezionato.
        - 'lite': Rimanda all'interfaccia firmware dedicata al Dobot Magician Lite.
        - 'magician': Rimanda all'interfaccia per il Dobot Magician Standard.
        """
        return api_lite if self.model_var.get() == "lite" else api_magician

    def update_port_list(self):
        """
        Scansiona le porte COM del sistema per trovare i dispositivi Dobot connessi.
        Utilizza api.search_dobot() che interroga il sistema operativo e restituisce una
        lista di dizionari, ognuno contenente informazioni come 'portName' (es. 'COM3').
        """
        if self.is_connected: return
        try:
            ports = api_magician.search_dobot()
            if ports:
                self.port_combo["values"] = [p["portName"] for p in ports]
                self.port_combo.current(0)
            else:
                self.port_combo["values"] = []
                self.port_combo.set("Nessun robot rilevato")
        except Exception:
            self.port_combo.set("Errore ricerca porte")

    def toggle_connection(self):
        """Gestisce lo sdoppiamento logico del pulsante unificato di connessione."""
        if self.is_connected:
            self.disconnect_robot()
        else:
            self.connect_robot()

    def connect_robot(self):
        """
        Stabilisce la connessione seriale USB con il robot selezionato.
        In caso di successo, blocca le modifiche alla GUI per preservare la stabilità
        e avvia il thread/ciclo per il monitoraggio in tempo reale della posizione.
        """
        port_selected = self.port_combo.get()
        if not port_selected or "Seleziona" in port_selected or "Nessun" in port_selected:
            messagebox.showwarning("Attenzione", "Seleziona una porta COM valida!")
            return
        
        # --- VERIFICA COERENZA MODELLO RIGIDA ---
        selected_model = self.model_var.get()
        try:
            ports = api_magician.search_dobot()
            device_desc = ""
            found = False
            
            for p in ports:
                if p.get("portName") == port_selected:
                    device_desc = p.get("description", "")
                    found = True
                    break
            
            if not found:
                messagebox.showerror("Errore", f"La porta {port_selected} non è attualmente disponibile o è occupata.")
                return
            
            if selected_model == "magician" and "Silicon Labs CP210x USB to UART Bridge" not in device_desc:
                messagebox.showerror(
                    "Errore di Modello", 
                    f"La porta {port_selected} non corrisponde a un Dobot Magician Standard.\n"
                    f"Dispositivo rilevato: {device_desc if device_desc else 'Sconosciuto'}"
                )
                return
            elif selected_model == "lite" and "Dispositivo seriale USB" not in device_desc:
                messagebox.showerror(
                    "Errore di Modello", 
                    f"La porta {port_selected} non corrisponde a un Dobot Magician Lite.\n"
                    f"Dispositivo rilevato: {device_desc if device_desc else 'Sconosciuto'}"
                )
                return
        except Exception as e:
            messagebox.showwarning("Attenzione", f"Impossibile verificare la descrizione del dispositivo: {e}")
            return 
        # ----------------------------------

        api = self.get_api()
        try:
            self.lbl_status_msg.config(text="Connessione in corso...")
            self.root.update_idletasks()
            
            # Sovrascriviamo le funzioni di callback interne per evitare sovrapposizioni indesiderate
            api.on_pause = lambda: None
            api.on_resume = lambda: None
            
            # api.connect_dobot(port_name): Inizializza la comunicazione sulla porta specificata.
            # Ritorna True se l'handshake seriale va a buon fine, altrimenti False.
            if api.connect_dobot(port_name=port_selected):
                self.port = port_selected
                self.is_connected = True
                
                # Disabilitazione dei selettori hardware per evitare cambi di modello "a caldo" a robot connesso
                self.radio_magician.config(state="disabled")
                self.radio_lite.config(state="disabled")
                self.port_combo.config(state="disabled")
                
                # Transizione grafica del bottone in stato disconnessione
                self.btn_toggle_connect.config(text="DISCONNETTI ROBOT", style="TButton")
                self.lbl_status_msg.config(text=f"Connesso ({selected_model.upper()}) su {self.port}")
                
                # Invia subito le velocità impostate sugli slider al firmware del robot
                self.update_speed()
                self.update_rail_speed()
                
                # Avvia il loop asincrono di lettura delle coordinate cartesiane reali
                self.read_pose_loop()
            else:
                messagebox.showerror("Errore", "Impossibile stabilire la connessione.")
        except Exception as e:
            messagebox.showerror("Errore", f"Eccezione durante la connessione: {e}")

    def disconnect_robot(self):
        """
        Interrompe in modo sicuro la comunicazione con l'hardware.
        Arresta i motori del nastro trasportatore prima dello stacco per ragioni di sicurezza safety.
        """
        self.stop_conveyor()
        
        try: 
            # api.disconnect_dobot(port_name): Chiude il socket seriale associato alla porta specificata
            self.get_api().disconnect_dobot(port_name=self.port)
        except: 
            pass
        
        self.is_connected = False
        self.port = None
        
        # Riabilita i controlli di selezione hardware sulla GUI
        self.radio_magician.config(state="normal")
        self.radio_lite.config(state="normal")
        self.port_combo.config(state="readonly")
        
        # Ripristina l'aspetto iniziale del bottone di connessione
        self.btn_toggle_connect.config(text="CONNETTI ROBOT", style="Accent.TButton")
        self.lbl_status_msg.config(text="Stato: Disconnesso")
        self.root.update_idletasks()

    def update_conveyor_speed(self, val):
        """
        Invia il comando di controllo della velocità al nastro trasportatore.
        
        Parametri della funzione set_converyor:
        - port_name: Stringa identificativa della porta COM attiva.
        - index: Identificativo del canale del motore passo-passo sulla scheda (di norma 0).
        - enable: Booleano. True attiva l'alimentazione del motore del nastro, False lo spegne elettricamente.
        - speed: Intero (da -10000 a +10000) che imposta i passi/impulsi al secondo, definendo direzione e velocità.
        - is_queued: Impostato obbligatoriamente a True. Inserisce il comando nella coda sequenziale del robot.
        """
        if not self.is_connected: return
        speed_val = int(val)
        
        # Ottimizzazione: Se la velocità è 0 disabilitiamo il nastro (enable=False) per preservare i motori
        enable_conveyor = True if speed_val != 0 else False
        
        try:
            self.get_api().set_converyor(
                port_name=self.port,
                index=0,
                enable=enable_conveyor,
                speed=speed_val,
                is_queued=True
            )
        except Exception as e:
            print(f"Errore controllo nastro: {e}")

    def stop_conveyor(self):
        """Azzera istantaneamente la velocità del nastro e ne aggiorna il componente grafico Slider."""
        self.conveyor_slider.set(0)
        if self.is_connected:
            self.update_conveyor_speed(0)

    def update_speed(self, val=None):
        """
        Configura la percentuale di dinamica (velocità ed accelerazione) del braccio robotico.
        
        Funzioni utilizzate:
        - set_jogcommon_params: Configura il rapporto massimo per i movimenti manuali JOG (tasti a schermo).
        - set_ptpcommon_params: Configura il rapporto per i movimenti automatici punto-punto (PTP).
        
        Parametri:
        - velocity_ratio: Valore intero da 1 a 100 che scala la velocità massima del firmware.
        - acceleration_ratio: Valore intero da 1 a 100 che scala l'accelerazione dei motori.
        """
        if self.is_connected:
            speed_val = int(self.speed_slider.get())
            try:
                self.get_api().set_jogcommon_params(port_name=self.port, velocity_ratio=speed_val, acceleration_ratio=speed_val)
                self.get_api().set_ptpcommon_params(port_name=self.port, velocity_ratio=speed_val, acceleration_ratio=speed_val)
            except: pass

    def update_rail_speed(self, val=None):
        """Aggiorna i parametri PTP punto-punto dedicati alle cinematiche di traslazione della rotaia."""
        if self.is_connected:
            speed_val = int(self.rail_speed_slider.get())
            try:
                self.get_api().set_ptpcommon_params(port_name=self.port, velocity_ratio=speed_val, acceleration_ratio=speed_val)
            except: pass

    def start_jog(self, cmd_id):
        """
        Invia l'istruzione di avvio del movimento continuo su un asse (JOG).
        
        Parametri di set_jogcmd:
        - port_name: Porta COM attiva.
        - is_joint: Scelta del sistema di coordinate. False = Coordinate Cartesiane (X, Y, Z, R). True = Giunti del braccio.
        - cmd: ID numerico della direzione (definito nelle costanti in cima al file, es. JOG_X_PLUS).
        - is_queued: Impostato a False per l'esecuzione immediata in tempo reale (bypassando la coda dei movimenti pregressi).
        """
        if self.is_connected:
            try: self.get_api().set_jogcmd(port_name=self.port, is_joint=False, cmd=cmd_id, is_queued=False)
            except: pass

    def stop_jog(self):
        """Invia l'istruzione speciale JOG_IDLE (0) per arrestare immediatamente qualsiasi movimento JOG in corso."""
        if self.is_connected:
            try: self.get_api().set_jogcmd(port_name=self.port, is_joint=False, cmd=JOG_IDLE, is_queued=False)
            except: pass

    def run_robot_home(self):
        """
        Esegue la calibrazione hardware di Homing (azzeramento dei sensori fisici e dei giunti del braccio).
        
        Passaggi e funzioni:
        1. api.clear_allalarms_state(port): Resetta tutti i registri di errore e allarme del firmware (fondamentale 
           se il braccio ha urtato o superato i limiti cartesiani limite, bloccando l'accettazione di nuovi comandi).
        2. api.set_homecmd(port_name): Invia l'ordine nativo al firmware di muovere sequenzialmente ciascun asse 
           fino a intercettare i microinterruttori fisici di finecorsa per ricostruire lo zero macchina assoluto.
        """
        if not self.is_connected: return
        if messagebox.askyesno("Homing", "Avviare la calibrazione Home fisica del braccio robotico?"):
            try:
                api = self.get_api()
                api.clear_allalarms_state(self.port)
                
                # Comando originale nativo della libreria per l'esecuzione dell'Homing del braccio
                api.set_homecmd(port_name=self.port)
            except Exception as e:
                messagebox.showerror("Errore", f"Impossibile completare la calibrazione: {e}")

    def home_rail(self):
        """Forza il riposizionamento lineare della rotaia portandola alla coordinata base L = 0.0 mm."""
        if not self.is_connected: return
        self.rail_slider.set(0) 
        self.move_rail_to_target(0.0) 

    def start_rail_interaction(self, event):
        self.user_interacting_with_rail = True

    def move_rail_to_slider_pos(self, event):
        if not self.is_connected:
            self.user_interacting_with_rail = False
            return
        
        target_l = float(self.rail_slider.get())
        self.move_rail_to_target(target_l)
        self.root.after(500, self._stop_rail_interaction)

    def move_rail_to_target(self, target_l):
        """
        Esegue il movimento interpolato del robot modificando esclusivamente l'asse aggiuntivo della rotaia (L).
        
        Logica e funzioni:
        1. api.set_device_withl(port, True): Comunica esplicitamente alla logica del Dobot che è presente e 
           attivo l'asse di scorrimento extra (Linear Rail).
        2. api.get_pose(port): Recupera la posizione attuale del robot, in modo da mantenere invariate le coordinate 
           cartesiane correnti (X, Y, Z, R) del braccio durante la traslazione sulla base lineare.
        3. Scansione dinamica del comando PTP: A seconda della versione del firmware/libreria installata sul sistema,
           il comando per lo spostamento accoppiato alla rotaia può chiamarsi 'set_ptplcmd' o 'set_ptpwithlcmd'. 
           Il ciclo for analizza i metodi disponibili (tramite dir(api)) ed esegue quello presente.
           
        Parametri del comando PTP con Rotaia:
        - ptp_mode: Impostato a 1 (Movimento di tipo MOVL - Movimento lineare nello spazio cartesiano).
        - x, y, z, r: Coordinate spaziali attuali del braccio (prese da get_pose) per non fargli compiere movimenti asincroni.
        - l: Nuova coordinata millimetrica (target_l) in cui posizionare la base del robot lungo la rotaia.
        - is_queued: Impostato a False per elaborare il movimento istantaneamente.
        """
        self.update_rail_speed()
        try:
            api = self.get_api()
            try:
                api.set_device_withl(self.port, True)
            except:
                pass
                
            pose = api.get_pose(port_name=self.port)
            current_x = pose.get('x', 230.0) if pose else 230.0
            current_y = pose.get('y', 0.0) if pose else 0.0
            current_z = pose.get('z', 0.0) if pose else 0.0
            current_r = pose.get('r', 0.0) if pose else 0.0
            
            self.lbl_status_msg.config(text=f"Muovendo rotaia a L: {target_l} mm")
            
            nomi_api = dir(api)
            comandi_rotaia = [m for m in nomi_api if 'ptp' in m and 'l' in m]
            
            if 'set_ptplcmd' not in comandi_rotaia: comandi_rotaia.append('set_ptplcmd')
            if 'set_ptpwithlcmd' not in comandi_rotaia: comandi_rotaia.append('set_ptpwithlcmd')
            
            for nome_cmd in comandi_rotaia:
                if hasattr(api, nome_cmd):
                    funzione = getattr(api, nome_cmd)
                    try:
                        funzione(port_name=self.port, ptp_mode=1, x=current_x, y=current_y, z=current_z, r=current_r, l=target_l, is_queued=False)
                        break
                    except Exception:
                        try:
                            funzione(self.port, 1, current_x, current_y, current_z, current_r, target_l, False)
                            break
                        except Exception:
                            continue
                
        except Exception as e:
            print(f"Errore PTP Rotaia: {e}")

    def _stop_rail_interaction(self):
        self.user_interacting_with_rail = False

    def suction_on(self):
        """
        Attiva la pompa per la generazione del vuoto nella ventosa (Suction Cup) dell'end-effector.
        
        Parametri di set_endeffector_suctioncup:
        - port_name: Porta COM attiva.
        - enable: Abilitazione generale del modulo attuatore di fine braccio (True = Alimentato / Attivo).
        - on: Stato pneumatico della valvola (True = Avvia l'aspirazione generando il vuoto per afferrare l'oggetto).
        - is_queued: Impostato a False per agire istantaneamente senza attendere la coda dei movimenti.
        """
        if self.is_connected:
            try: self.get_api().set_endeffector_suctioncup(port_name=self.port, enable=True, on=True, is_queued=False)
            except: pass

    def suction_off(self):
        """
        Avvia la procedura di rilascio dell'oggetto dalla ventosa.
        Inverte momentaneamente il flusso (on=False) per rilasciare la presa pneumatica velocemente.
        """
        if self.is_connected:
            try:
                self.get_api().set_endeffector_suctioncup(port_name=self.port, enable=True, on=False, is_queued=False)
                # Un timer asincrono di 250ms spegne del tutto il compressore per non lasciarlo sotto sforzo inutilmente
                self.root.after(250, self._turn_off_compressor)
            except: pass

    def _turn_off_compressor(self):
        """Disabilita completamente l'alimentazione elettrica all'attuatore della ventosa (enable=False)."""
        if self.is_connected:
            try: self.get_api().set_endeffector_suctioncup(port_name=self.port, enable=False, on=False, is_queued=False)
            except: pass

    def read_pose_loop(self):
        """
        Ciclo asincrono di polling temporizzato (ogni 200 ms) che interroga il robot.
        
        Funzioni utilizzate:
        - api.get_pose(port_name): Invia una richiesta al firmware che risponde con un dizionario contenente le 
          coordinate cartesiane reali correnti espresse in millimetri ('x', 'y', 'z', 'l') e gradi sessagesimali ('r').
        """
        if self.is_connected:
            try:
                pose = self.get_api().get_pose(port_name=self.port)
                if pose:
                    real_l = pose.get('l', 0.0)
                    # Aggiornamento grafico delle etichette testuali (Label) formattando il testo a due cifre decimali
                    self.lbl_x.config(text=f"X: {pose.get('x', 0.0):.2f}")
                    self.lbl_y.config(text=f"Y: {pose.get('y', 0.0):.2f}")
                    self.lbl_z.config(text=f"Z: {pose.get('z', 0.0):.2f}")
                    self.lbl_r.config(text=f"R: {pose.get('r', 0.0):.2f}")
                    self.lbl_l.config(text=f"L (Rotaia): {real_l:.2f}")
            except Exception:
                pass
            
            # scheduler asincrono di Tkinter: riesegue ricorsivamente questo metodo tra 200 millisecondi
            self.root.after(200, self.read_pose_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalDobotGUI(root)
    root.mainloop()
