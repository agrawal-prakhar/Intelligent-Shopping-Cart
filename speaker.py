import network, espnow, machine, utime
from machine import Pin, PWM, Timer
import math
from time import sleep

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()                       # keep Wi-Fi idle
e = espnow.ESPNow()
e.active(True)

print("Receiver ready … waiting for packets")

C3 = 131
CS3 = 139
D3 = 147
DS3 = 156
E3 = 165
F3 = 175
FS3 = 185
G3 = 196
GS3 = 208
A3 = 220
AS3 = 233
B3 = 247
C4 = 262
CS4 = 277
D4 = 294
DS4 = 311
E4 = 330
F4 = 349
FS4 = 370
G4 = 392
GS4 = 415
A4 = 440
AS4 = 466
B4 = 494
C5 = 523
CS5 = 554
D5 = 587
DS5 = 622
E5 = 659
F5 = 698
FS5 = 740
G5 = 784
GS5 = 831
A5 = 880
AS5 = 932
B5 = 988
C6 = 1047
CS6 = 1109
D6 = 1175
DS6 = 1245
E6 = 1319
F6 = 1397
FS6 = 1480
G6 = 1568
GS6 = 1661
A6 = 1760
AS6 = 1865
B6 = 1976
C7 = 2093
CS7 = 2217
D7 = 2349
DS7 = 2489
E7 = 2637
F7 = 2794
FS7 = 2960
G7 = 3136
GS7 = 3322
A7 = 3520
AS7 = 3729
B7 = 3951
C8 = 4186
CS8 = 4435
D8 = 4699
DS8 = 4978

music = [
C4, E4, G4, C5, E5, G4, C5, E5, C4, E4, G4, C5, E5, G4, C5, E5,
C4, D4, G4, D5, F5, G4, D5, F5, C4, D4, G4, D5, F5, G4, D5, F5,
B3, D4, G4, D5, F5, G4, D5, F5, B3, D4, G4, D5, F5, G4, D5, F5,
C4, E4, G4, C5, E5, G4, C5, E5, C4, E4, G4, C5, E5, G4, C5, E5,
C4, E4, A4, E5, A5, A4, E5, A4, C4, E4, A4, E5, A5, A4, E5, A4,
C4, D4, FS4, A4, D5, FS4, A4, D5, C4, D4, FS4, A4, D5, FS4, A4, D5,
B3, D4, G4, D5, G5, G4, D5, G5, B3, D4, G4, D5, G5, G4, D5, G5,
B3, C4, E4, G4, C5, E4, G4, C5, B3, C4, E4, G4, C5, E4, G4, C5,
B3, C4, E4, G4, C5, E4, G4, C5, B3, C4, E4, G4, C5, E4, G4, C5,
A3, C4, E4, G4, C5, E4, G4, C5, A3, C4, E4, G4, C5, E4, G4, C5,
D3, A3, D4, FS4, C5, D4, FS4, C5, D3, A3, D4, FS4, C5, D4, FS4, C5,
G3, B3, D4, G4, B4, D4, G4, B4, G3, B3, D4, G4, B4, D4, G4, B4
]



note_index = 0
# This is the callback function
def tcb(timer):
    global duty_cycle
    global note_index
    if note_index < len(music)-1:
        note_index += 1
    else:
        note_index = 0
    
    L1.freq(music[note_index])
    

# ── Motion-control parameters (tweak to taste) ─────────────────────────────────
     # need ≥ 40 cm ahead to keep moving      # (cm) if |left-right| < GAP → treated as “straight”

while True:
    host, msg = e.irecv(1)


    if not msg:
        
        continue                       # loop again

    s = msg.decode()
    if s == "end":
        break

    try:
        d_mid, d_left, d_right, extra = map(float, s.split(","))
        if d_mid == 0 or d_mid == -0:
            d_mid = 250
        
        if d_left == 0 or d_left == -0:
            d_left = 250
            
        if d_right == 0 or d_right == -0:
            d_right = 250
            
        # ── debug print ──
        print("mid %.1f cm  left %.1f cm  right %.1f cm"
              % (d_mid, d_left, d_right))
        
        if d_mid <= 10:
            t1 = Timer(1)
            t1.init(period=500, mode=t1.PERIODIC, callback=tcb)
        
        
        
    except (ValueError, IndexError) as err:
        print("Parse error:", err)