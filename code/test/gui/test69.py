import tkinter as tk
from tkinter import ttk, messagebox
from DobotEDU import *

# Associazione delle API reali
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

class UniversalDobotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Dobot Control Panel (with Rail & Conveyor Belt)")
        self.root.geometry("850x780") # Leggermente aumentata l'altezza per ospitare il nastro
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

        # NUOVO BOX: Controllo Nastro Trasportatore (Sotto la posizione reale)
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
        
        # Bottone rapido per arrestare il nastro
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
        btn.bind("<ButtonPress-1>", lambda event: self.start_jog(cmd_id))
        btn.bind("<ButtonRelease-1>", lambda event: self.stop_jog())

    def get_api(self):
        return api_lite if self.model_var.get() == "lite" else api_magician

    def update_port_list(self):
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
        if self.is_connected:
            self.disconnect_robot()
        else:
            self.connect_robot()

    def connect_robot(self):
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
            api.on_pause = lambda: None
            api.on_resume = lambda: None
            
            if api.connect_dobot(port_name=port_selected):
                self.port = port_selected
                self.is_connected = True
                
                # Blocca la modifica del tipo di dispositivo
                self.radio_magician.config(state="disabled")
                self.radio_lite.config(state="disabled")
                self.port_combo.config(state="disabled")
                
                # Cambia il testo e lo stile del bottone
                self.btn_toggle_connect.config(text="DISCONNETTI ROBOT", style="TButton")
                self.lbl_status_msg.config(text=f"Connesso ({selected_model.upper()}) su {self.port}")
                
                self.update_speed()
                self.update_rail_speed()
                self.read_pose_loop()
            else:
                messagebox.showerror("Errore", "Impossibile stabilire la connessione.")
        except Exception as e:
            messagebox.showerror("Errore", f"Eccezione durante la connessione: {e}")

    def disconnect_robot(self):
        # Ferma il nastro prima di staccare la connessione per sicurezza
        self.stop_conveyor()
        
        try: 
            self.get_api().disconnect_dobot(port_name=self.port)
        except: 
            pass
        
        self.is_connected = False
        self.port = None
        
        # Sblocca la modifica del tipo di dispositivo e riabilita i controlli
        self.radio_magician.config(state="normal")
        self.radio_lite.config(state="normal")
        self.port_combo.config(state="readonly")
        
        # Ripristina il bottone nello stato iniziale
        self.btn_toggle_connect.config(text="CONNETTI ROBOT", style="Accent.TButton")
        self.lbl_status_msg.config(text="Stato: Disconnesso")
        self.root.update_idletasks()

    def update_conveyor_speed(self, val):
        """Invia il comando di controllo della velocità al nastro trasportatore."""
        if not self.is_connected: return
        speed_val = int(val)
        
        # Se la velocità è 0, disabilitiamo il nastro, altrimenti lo teniamo abilitato
        enable_conveyor = True if speed_val != 0 else False
        
        try:
            # index di norma è 0 (o 1 a seconda dell'interfaccia usata sull'hardware)
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
        """Azzera la velocità del nastro e aggiorna la GUI."""
        self.conveyor_slider.set(0)
        if self.is_connected:
            self.update_conveyor_speed(0)

    def update_speed(self, val=None):
        if self.is_connected:
            speed_val = int(self.speed_slider.get())
            try:
                self.get_api().set_jogcommon_params(port_name=self.port, velocity_ratio=speed_val, acceleration_ratio=speed_val)
                self.get_api().set_ptpcommon_params(port_name=self.port, velocity_ratio=speed_val, acceleration_ratio=speed_val)
            except: pass

    def update_rail_speed(self, val=None):
        if self.is_connected:
            speed_val = int(self.rail_speed_slider.get())
            try:
                self.get_api().set_ptpcommon_params(port_name=self.port, velocity_ratio=speed_val, acceleration_ratio=speed_val)
            except: pass

    def start_jog(self, cmd_id):
        if self.is_connected:
            try: self.get_api().set_jogcmd(port_name=self.port, is_joint=False, cmd=cmd_id, is_queued=False)
            except: pass

    def stop_jog(self):
        if self.is_connected:
            try: self.get_api().set_jogcmd(port_name=self.port, is_joint=False, cmd=JOG_IDLE, is_queued=False)
            except: pass

    def run_robot_home(self):
        if not self.is_connected: return
        if messagebox.askyesno("Homing", "Avviare la calibrazione Home fisica del braccio robotico?\n(Il robot eseguirà movimenti di reset hardware)"):
            try:
                api = self.get_api()
                
                # 1. Pulizia drastica di tutti gli allarmi attivi
                api.clear_allalarms_state(self.port)
                self.root.update_idletasks()
                
                # 2. Configurazione dei parametri di Homing (Velocità ed accelerazione di homing)
                # Spesso necessario se la libreria perde i riferimenti dopo una disconnessione
                try:
                    api.set_homeparams(port_name=self.port, x=200, y=0, z=0, r=0, is_queued=False)
                except Exception as e_param:
                    print(f"Nota: Configurazione homeparams non supportata o fallita: {e_param}")

                # 3. Gestione asse Rotaia (L) durante l'Homing
                # Se la rotaia è attiva, forziamo l'Homing generico. Altrimenti, usiamo il comando standard.
                self.lbl_status_msg.config(text="Esecuzione Homing in corso...")
                self.root.update_idletasks()
                
                # Proviamo a invocare il comando Home. Alcuni firmware richiedono is_queued=False esplicito.
                try:
                    api.set_homecmd(port_name=self.port, is_queued=False)
                except TypeError:
                    # Se la versione della libreria installata non accetta keyword arguments o is_queued
                    try:
                        api.set_homecmd(self.port)
                    except Exception as e_inner:
                        raise e_inner
                        
                messagebox.showinfo("Homing Avviato", "Il processo di Homing è iniziato. Attendi che il robot finisca di muoversi e i LED tornino verdi.")
                
            except Exception as e:
                messagebox.showerror("Errore Homing", f"Impossibile completare la calibrazione Home:\n{e}")

    def home_rail(self):
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
        if self.is_connected:
            try: self.get_api().set_endeffector_suctioncup(port_name=self.port, enable=True, on=True, is_queued=False)
            except: pass

    def suction_off(self):
        if self.is_connected:
            try:
                self.get_api().set_endeffector_suctioncup(port_name=self.port, enable=True, on=False, is_queued=False)
                self.root.after(250, self._turn_off_compressor)
            except: pass

    def _turn_off_compressor(self):
        if self.is_connected:
            try: self.get_api().set_endeffector_suctioncup(port_name=self.port, enable=False, on=False, is_queued=False)
            except: pass

    def read_pose_loop(self):
        if self.is_connected:
            try:
                pose = self.get_api().get_pose(port_name=self.port)
                if pose:
                    real_l = pose.get('l', 0.0)
                    self.lbl_x.config(text=f"X: {pose.get('x', 0.0):.2f}")
                    self.lbl_y.config(text=f"Y: {pose.get('y', 0.0):.2f}")
                    self.lbl_z.config(text=f"Z: {pose.get('z', 0.0):.2f}")
                    self.lbl_r.config(text=f"R: {pose.get('r', 0.0):.2f}")
                    self.lbl_l.config(text=f"L (Rotaia): {real_l:.2f}")
            except Exception:
                pass
            
            self.root.after(200, self.read_pose_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalDobotGUI(root)
    root.mainloop()