# Documentazione tecnica di sistema
Specifiche delle API, struttura del codice e guida di configurazione per Dobot Magician Lite



## 1. Requisiti di sistema e installazione
L'ambiente operativo richiede la corretta esecuzione in background dell'applicazione **DobotLink** per consentire l'instradamento dei comandi verso la porta seriale.

* **Ambiente Python:** Versione 3.8.x.
* **Installazione delle dipendenze:**
  ```bash
  pip install keyboard pyperclip
  ```

*(Nota: il modulo `DobotEDU` deve essere importato dall'ambiente software fornito dal produttore).*



## 2. Architettura del codice sorgente

Il programma implementa un ciclo di controllo continuo (polling a $10\text{ ms}$ tramite `time.sleep(0.01)`) che verifica lo stato dei tasti e aziona i metodi della libreria `m_lite`.

### Gestione della connessione e configurazione iniziale

All'avvio, il software tenta di stabilire la connessione sulla porta `COM4` impostando la velocità massima degli assi al 100% e la velocità di partenza al 51%:

```python
PORTA = 'COM4'

try:
    m_lite.set_armspeed_ratio(PORTA, set_type=1, set_value=100)
except Exception as e:
    print(f"\n[ERRORE DI CONNESSIONE]: {e}")
    sys.exit()
    
m_lite.set_armspeed_ratio(PORTA, set_type=0, set_value=51)

```



## 3. Specifiche delle funzioni core

### `muovi(coordinata, tasto)`

Questa funzione ottimizza il movimento manuale (JOG). Quando un tasto di direzione viene premuto, viene inviato il comando di movimento sulla coordinata corrispondente. Il ciclo `while` blocca l'esecuzione mantenendo il robot in movimento finché il tasto resta premuto; al rilascio, viene inviato il comando di arresto (`cmd=0`).

```python
def muovi(coordinata, tasto):
    m_lite.set_jogcmd(PORTA, is_joint=0, cmd=coordinata)
    while keyboard.is_pressed(tasto):
        time.sleep(0.01)
    m_lite.set_jogcmd(PORTA, is_joint=0, cmd=0)

```

### `stampaCodice(strCodice)`

Gestisce la finalizzazione della macro. Riceve la stringa contenente le istruzioni accumulate, la mostra a terminale e ne esegue l'esportazione negli appunti di sistema.

```python
def stampaCodice(strCodice):
   print("Codice:\n\n"+strCodice+"\nIl codice è stato copiato negli appunti!\n")
   pyperclip.copy(strCodice)

```



## 4. Analisi delle funzioni di stato e manipolazione stringhe

### Acquisizione e formattazione coordinate PTP

Alla pressione del tasto F, il dizionario restituito da `m_lite.get_pose(PORTA)` viene analizzato per estrarre le chiavi geometriche. Se la variabile `registrazione` è attiva, viene concatenata una stringa di comando Point-To-Point (`ptp_mode=0`):

```python
coordinate = m_lite.get_pose(PORTA)
if registrazione:
    strCodice += "m_lite.set_ptpcmd(ptp_mode=0, x = " + str(coordinate["x"]) + ", y = " + str(coordinate["y"]) + ", z = " + str(coordinate["z"]) + ", r = " + str(coordinate["r"]) + ")\n"

```

### Gestione dello stack di comandi (Funzione cancella)

L'eliminazione dell'ultima riga inserita sfrutta la scomposizione della stringa in una lista di righe tramite `splitlines()`, rimuovendo l'ultimo elemento e ricombinando il testo:

```python
righe = strCodice.splitlines()
del righe[-1]
strCodice = "\n".join(righe)

```



## 5. Routine di chiusura e sicurezza

Alla pressione del tasto ESC, il ciclo principale si interrompe (istruzione `break`). Per garantire la sicurezza dell'hardware, il software esegue automaticamente la disattivazione del sistema di aspirazione della ventosa e invia il braccio robotico alla posizione di riposo (`set_homecmd`) prima di terminare il processo.
