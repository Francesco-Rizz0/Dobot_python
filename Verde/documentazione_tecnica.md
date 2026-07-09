# Documentazione tecnica di sistema
Specifiche delle API, struttura del codice e guida di configurazione per Dobot Magician Lite

## 1. Requisiti di sistema e installazione
Per il corretto funzionamento del software di controllo, l'ambiente di runtime deve rispettare i seguenti vincoli di versione:

* **Runtime:** Python 3.8.x (Versioni superiori non garantiscono il caricamento del modulo `DobotEDU`).
* **Pacchetti richiesti:** Installare le dipendenze tramite `pip`:
  ```bash
  pip install pydobot pynput

```



## 2. Struttura del codice sorgente

Il software si basa su un'architettura ad eventi asincroni per l'ascolto della tastiera unito a chiamate sincrone verso la porta seriale del robot.

### Modulo di inizializzazione

```python
import time
from pydobot import Dobot
from pynput import keyboard

# Inizializzazione del braccio robotico (specificare la porta corretta, es. COM3 o /dev/ttyUSB0)
device = Dobot(port='COM3', verbose=False)

# Variabili di stato globali
current_speed = 50
is_recording = False
macro_commands = []

```



## 3. Specifiche delle funzioni e logica di controllo

### `muovi_robot(delta_x, delta_y, delta_z, delta_r)`

Calcola lo spostamento relativo aggiungendo i valori delta alla posizione cartesiana corrente letta in tempo reale dal robot. Invia il comando di tipo `LINEAR_MOVE`.

### Gestione del modulo macro recorder

Se l'ascoltatore di eventi rileva la pressione del tasto `r`, lo stato della variabile `is_recording` viene invertito. Quando è attivo, ogni volta che viene inviato un comando al robot, la stringa corrispondente all'API viene aggiunta alla lista `macro_commands`.

### Callback di cattura input

```python
def on_press(key):
    global current_speed, is_recording, macro_commands
    try:
        if key.char == 'w':
            muovi_robot(10, 0, 0, 0)
        elif key.char == 'e':
            device.suck(True)
            if is_recording:
                macro_commands.append("robot.suck(True)")
        elif key.char == 'r':
            if not is_recording:
                is_recording = True
                macro_commands = []
            else:
                is_recording = False
                stampa_codice_generato()
    except AttributeError:
        if key == keyboard.Key.space:
            muovi_robot(0, 0, 10, 0)

```



## 4. Formato del blocco di codice autogenerato

Il codice stampato in console o salvato in file al termine della registrazione rispetta la sintassi standard della libreria `pydobot`:

```python
#  codice macro generato automaticamente 
from pydobot import Dobot
robot = Dobot(port='COM3')

robot.move_to(210.0, 0.0, 50.0, 0.0, wait=True)
robot.suck(True)
robot.move_to(210.0, 20.0, 60.0, 10.0, wait=True)
robot.suck(False)
robot.go_home()
#  fine macro 

```
