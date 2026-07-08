import tkinter as tk
from tkinter import ttk
from DobotEDU import *

# --- COSTANTI JOG (Dobot Magician) ---
JOG_IDLE = 0
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
        self.root.title("Dobot Arm Control Panel + Suction Cup")
        self.root.geometry("650x530") # Aumentata leggermente l'altezza per ospitare i nuovi controlli
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
        
        style.configure("TButton", background="#3E4451", foreground="white", borderwidth=0, font=("Arial", 10, "bold"))
        style.map("TButton", background=[("active", "#528BFF")])
        
        style.configure("DPad.TButton", background="#1E222A", foreground="#ABB2BF", width=5, font=("Arial", 10, "bold"))
        style.map("DPad.TButton", background=[("active", "#404754")])
        
        # Stili speciali per l'attivazione/disattivazione della ventosa
        style.configure("Suck.TButton", background="#98C379", foreground="black", font=("Arial", 10, "bold"))
        style.map("Suck.TButton", background=[("active", "#A3E287")])
        
        style.configure("Release.TButton", background="#E06C75", foreground="white", font=("Arial", 10, "bold"))
        style.map("Release.TButton", background=[("active", "#E98B93")])

    def create_widgets(self):
        # ==========================================
        # TOP BAR: Connessione e Comandi di Base
        # ==========================================
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")
        
        ttk.Label(top_frame, text="Arm Control Panel", font=("Arial", 14, "bold"), foreground="white").pack(side="left", padx=10)
        
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(top_frame, textvariable=self.port_var, width=15, state="readonly")
        self.port_combo.pack(side="left", padx=10)
        
        self.btn_refresh = ttk.Button(top_frame, text="🔄", width=3, command=self.update_port_list)
        self.btn_refresh.pack(side="left", padx=5)
        
        self.btn_connect = ttk.Button(top_frame, text="Connetti", command=self.toggle_connection)
        self.btn_connect.pack(side="left", padx=10)
        
        self.btn_clear = ttk.Button(top_frame, text="⚠️ Clear Alarms", command=self.clear_alarms)
        self.btn_clear.pack(side="right", padx=5)
        
        self.btn_home = ttk.Button(top_frame, text="🎯 Home", command=self.go_home)
        self.btn_home.pack(side="right", padx=5)

        # ==========================================
        # SPEED BAR: Slider per la velocità
        # ==========================================
        speed_frame = ttk.Frame(self.root, padding=10)
        speed_frame.pack(fill="x")
        
        ttk.Label(speed_frame, text="Speed").pack(side="left", padx=10)
        
        self.speed_scale = ttk.Scale(speed_frame, from_=1, to=100, orient="horizontal", command=self.update_speed)
        self.speed_scale.set(50)
        self.speed_scale.pack(side="left", fill="x", expand=True, padx=10)

        # ==========================================
        # MAIN CONTROLS: Coordinate e D-Pads
        # ==========================================
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)

        # --- Pannello Lettura Coordinate ---
        coords_frame = ttk.Frame(main_frame)
        coords_frame.grid(row=0, column=0, padx=20, sticky="n")
        
        self.lbl_x = ttk.Label(coords_frame, text="X: 0.00", font=("Consolas", 12))
        self.lbl_x.pack(pady=10)
        self.lbl_y = ttk.Label(coords_frame, text="Y: 0.00", font=("Consolas", 12))
        self.lbl_y.pack(pady=10)
        self.lbl_z = ttk.Label(coords_frame, text="Z: 0.00", font=("Consolas", 12))
        self.lbl_z.pack(pady=10)
        self.lbl_r = ttk.Label(coords_frame, text="R: 0.00", font=("Consolas", 12))
        self.lbl_r.pack(pady=10)

        # --- D-Pad: X e Y ---
        xy_frame = ttk.Frame(main_frame)
        xy_frame.grid(row=0, column=1, padx=30)
        
        self.create_dpad_button(xy_frame, "X+", 0, 1, JOG_X_PLUS)
        self.create_dpad_button(xy_frame, "X-", 2, 1, JOG_X_MINUS)
        self.create_dpad_button(xy_frame, "Y+", 1, 2, JOG_Y_PLUS)
        self.create_dpad_button(xy_frame, "Y-", 1, 0, JOG_Y_MINUS)

        # --- D-Pad: Z e R ---
        zr_frame = ttk.Frame(main_frame)
        zr_frame.grid(row=0, column=2, padx=30)
        
        self.create_dpad_button(zr_frame, "Z+", 0, 1, JOG_Z_PLUS)
        self.create_dpad_button(zr_frame, "Z-", 2, 1, JOG_Z_MINUS)
        self.create_dpad_button(zr_frame, "R+", 1, 2, JOG_R_PLUS)
        self.create_dpad_button(zr_frame, "R-", 1, 0, JOG_R_MINUS)

        # ==========================================
        # NEW PANEL: Controlli Ventosa (Suction Cup)
        # ==========================================
        suction_frame = ttk.LabelFrame(self.root, text=" End Effector: Suction Cup ", padding=15)
        suction_frame.pack(fill="x", padx=20, pady=15)
        
        self.btn_suck = ttk.Button(suction_frame, text="🟢 PRENDI (Suck On)", style="Suck.TButton", command=self.suction_on)
        self.btn_suck.pack(side="left", expand=True, fill="x", padx=10)
        
        self.btn_release = ttk.Button(suction_frame, text="🔴 RILASCIA (Suck Off)", style="Release.TButton", command=self.suction_off)
        self.btn_release.pack(side="left", expand=True, fill="x", padx=10)

    def create_dpad_button(self, parent, text, row, col, cmd_id):
        btn = ttk.Button(parent, text=text, style="DPad.TButton")
        btn.grid(row=row, column=col, padx=5, pady=5, ipadx=10, ipady=10)
        btn.bind("<ButtonPress-1>", lambda e: self.start_jog(cmd_id))
        btn.bind("<ButtonRelease-1>", lambda e: self.stop_jog())

    # ==========================================
    # LOGICA E COMANDI DOBOT
    # ==========================================
    def update_port_list(self):
        ports = dobotEdu.magician.search_dobot()
        port_names = [p["portName"] for p in ports] if ports else []
        self.port_combo['values'] = port_names
        if port_names:
            self.port_combo.current(0)
        else:
            self.port_combo.set("Nessun robot")

    def toggle_connection(self):
        if not self.is_connected:
            self.port = self.port_var.get()
            if self.port and self.port != "Nessun robot":
                dobotEdu.magician.connect_dobot(port_name=self.port)
                self.is_connected = True
                self.btn_connect.config(text="Disconnetti")
                self.port_combo.config(state="disabled")
                self.update_speed(self.speed_scale.get())
                self.read_pose_loop()
        else:
            # Spegne preventivamente la ventosa in caso di disconnessione improvvisa
            self.suction_off()
            dobotEdu.magician.disconnect_dobot(port_name=self.port)
            self.is_connected = False
            self.btn_connect.config(text="Connetti")
            self.port_combo.config(state="readonly")
            self.port = None

    def go_home(self):
        if self.is_connected:
            self.btn_home.config(state="disabled")
            dobotEdu.magician.set_homecmd(port_name=self.port)
            self.root.after(15000, lambda: self.btn_home.config(state="normal"))

    def clear_alarms(self):
        if self.is_connected:
            dobotEdu.magician.clear_allalarms_state(port_name=self.port)
            print("Allarmi cancellati.")

    def update_speed(self, val):
        if self.is_connected:
            speed_val = float(val)
            dobotEdu.magician.set_jogcommon_params(port_name=self.port, velocity_ratio=speed_val, acceleration_ratio=speed_val)

    def start_jog(self, cmd_id):
        if self.is_connected:
            dobotEdu.magician.set_jogcmd(port_name=self.port, is_joint=False, cmd=cmd_id, is_queued=False)

    def stop_jog(self):
        if self.is_connected:
            dobotEdu.magician.set_jogcmd(port_name=self.port, is_joint=False, cmd=JOG_IDLE, is_queued=False)

    # --- NUOVE FUNZIONI PER LA VENTOSA ---
    def suction_on(self):
        """Attiva il compressore e avvia l'aspirazione della ventosa."""
        if self.is_connected:
            # enable=True (accende l'attuatore), suck=True (avvia l'aspirazione)
            dobotEdu.magician.set_endeffector_suctioncup(port_name=self.port, enable=True, suck=True, is_queued=False)
            print("Ventosa: Aspirazione ATTIVATA")

# --- FUNZIONI CORRETTE PER LA VENTOSA (Basate su Magician.py) ---
    def suction_on(self):
        """Attiva il compressore e avvia l'aspirazione della ventosa."""
        if self.is_connected:
            try:
                # Usiamo 'on' al posto di 'suck' e passiamo i booleani corretti
                dobotEdu.magician.set_endeffector_suctioncup(
                    port_name=self.port, 
                    enable=True, 
                    on=True, 
                    is_queued=False
                )
                print("Ventosa: Aspirazione ATTIVATA")
            except Exception as e:
                print(f"Errore durante l'attivazione della ventosa: {e}")

    def suction_off(self):
        """Disattiva l'aspirazione ed esegue un breve soffio di rilascio."""
        if self.is_connected:
            try:
                # enable=True (compressore attivo), on=False (soffia/rilascia invece di aspirare)
                dobotEdu.magician.set_endeffector_suctioncup(
                    port_name=self.port, 
                    enable=True, 
                    on=False, 
                    is_queued=False
                )
                print("Ventosa: Rilascio in corso...")
                # Attende 250ms affinché l'oggetto si stacchi, poi spegne l'alimentazione
                self.root.after(250, self._turn_off_compressor)
            except Exception as e:
                print(f"Errore durante il rilascio della ventosa: {e}")

    def _turn_off_compressor(self):
        """Spegne completamente il compressore della ventosa."""
        if self.is_connected:
            try:
                # enable=False, on=False per disattivare e spegnere tutto l'end-effector
                dobotEdu.magician.set_endeffector_suctioncup(
                    port_name=self.port, 
                    enable=False, 
                    on=False, 
                    is_queued=False
                )
                print("Ventosa: Compressore SPENTO")
            except Exception as e:
                print(f"Errore durante lo spegnimento del compressore: {e}")

    def read_pose_loop(self):
        if self.is_connected:
            try:
                pose = dobotEdu.magician.get_pose(port_name=self.port)
                if pose:
                    self.lbl_x.config(text=f"X: {pose.get('x', 0.0):.2f}")
                    self.lbl_y.config(text=f"Y: {pose.get('y', 0.0):.2f}")
                    self.lbl_z.config(text=f"Z: {pose.get('z', 0.0):.2f}")
                    self.lbl_r.config(text=f"R: {pose.get('r', 0.0):.2f}")
            except Exception:
                pass
            self.root.after(200, self.read_pose_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = DobotJoystickGUI(root)
    root.mainloop()