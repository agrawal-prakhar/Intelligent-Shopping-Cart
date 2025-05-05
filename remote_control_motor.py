import network, espnow, machine, utime
import math


# ── Motor driver pins (Cytron Maker Drive) ─────────────────────────────────────
SPEED = 1023                           # full PWM (0-1023 for ESP32)

M1A = machine.PWM(machine.Pin(12))
M1B = machine.PWM(machine.Pin(13))
M2A = machine.PWM(machine.Pin(33))
M2B = machine.PWM(machine.Pin(27))

def m1_fwd():   M1A.duty(SPEED); M1B.duty(0)
def m1_rev():   M1A.duty(0);     M1B.duty(SPEED)
def m1_stop():  M1A.duty(0);     M1B.duty(0)

def m2_fwd():   M2A.duty(SPEED); M2B.duty(0)
def m2_rev():   M2A.duty(0);     M2B.duty(SPEED)
def m2_stop():  M2A.duty(0);     M2B.duty(0)

def all_stop():
    m1_stop()
    m2_stop()

# ── ESP-NOW radio setup ────────────────────────────────────────────────────────
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()                       # keep Wi-Fi idle
e = espnow.ESPNow()
e.active(True)

print("Receiver ready … waiting for packets")

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
        
        
            
        if d_left < 20 and d_right < 20 and d_mid < 20:
            all_stop()
            continue
            
        if d_left < 5:
            m1_fwd()
            
            
        elif d_left >=5:
            m1_stop()
            
           
        if d_right < 5:
            m2_fwd()
            
        elif d_left >=5:
            m2_stop()
            
        if d_mid <=5:
            m1_rev()
            m2_rev()
            
        

    except (ValueError, IndexError) as err:
        print("Parse error:", err)
