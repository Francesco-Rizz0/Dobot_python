# Documentazione tecnica di sistema
Specifiche delle API, architettura delle funzioni e gestione multimediale



## 1. Requisiti d'installazione e configurazione
Il software richiede il corretto avviamento del servizio **DobotLink** sulla macchina host e l'accessibilità ai canali seriali USB.

* **Interpreter:** Python 3.8.x
* **Installazione moduli esterni:**
  ```bash
  pip install pygame
  ```



## 2. Analisi dell'architettura del codice

### Routine di inizializzazione e sicurezza

Il software esegue un controllo preventivo all'apertura del canale seriale gestendo l'eccezione in caso di disconnessione o porta errata:

```python
PORTA = 'COM4'

try:
    m_lite.set_armspeed_ratio(PORTA, set_type=1, set_value=100)
except Exception as e:
    print(f"\n[ERRORE DI CONNESSIONE]: {e}")
    sys.exit()

```



## 3. Specifiche delle funzioni e modularità audio

La riproduzione audio sfrutta il modulo `pygame.mixer` configurato per operare in modalità non bloccante, permettendo al braccio robotico di muoversi simultaneamente all'esecuzione dei file sonori.

### `canzone(scelta)`

Inizializza il mixer e carica la traccia audio in base all'indice numerico passato come argomento, impostando eventuali parametri interni per la traccia.

* **Argomenti:** `scelta` (int) - Identificativo della traccia.

### `deposita(z, y)`

Sposta il braccio robotico alla posizione di rilascio tramite coordinate assolute e disattiva l'elettrovalvola della ventosa per rilasciare l'oggetto.

```python
def deposita(z, y):
    m_lite.set_ptpcmd(PORTA, ptp_mode=0, x=330, y=y, z=z, r=-110)
    m_lite.set_endeffector_suctioncup(PORTA, enable=False, on=False)

```

### `finale(scelta)`

Imposta la velocità massima del braccio, sposta l'asse terminale in una posizione di riposo prefissata e sicura ed esegue l'effetto sonoro di coda.



## 4. Logica dell'algoritmo di pallettizzazione

Il cuore software della movimentazione è rappresentato da una struttura a tre cicli for nidificati che converte le variabili geometriche in coordinate di prelievo.

```python
for k in range(2):           # Ciclo alternanza semispazio
    canzone(song)
    x = 253
    z = -44                  # Quota iniziale della pila di deposito
    for j in range(4):
        if k % 2 == 0:
            y = 151
            elia = 30        # Coordinata Y di destinazione
        else:
            y = -88
            elia = -30
            
        for i in range(4):   # Ciclo di campionamento singolo blocco
            m_lite.set_ptpcmd(PORTA, ptp_mode=0, x=x, y=y, z=-42, r=-110)
            m_lite.set_endeffector_suctioncup(PORTA, enable=True, on=True)
            y -= 20
            deposita(z, elia)
            z += 10          # Incremento verticale per effetto sovrapposizione
        x += 20              # Avanzamento riga successiva

```



## 5. Routine di arresto e finalizzazione

Al completamento del ciclo iterativo di pallettizzazione, il programma interrompe l'esecuzione del flusso audio principale tramite il metodo `mixer.music.stop()` e invoca immediatamente la routine `finale(sfx)` per garantire la messa in sicurezza finale dell'ambiente e del braccio meccanico.
