import network, espnow, machine, utime
import math

def angle_from_sides(a, b, c):
    # Law of Cosines: cos(C) = (a² + b² - c²) / (2ab)
    numerator = a**2 + b**2 - c**2
    denominator = 2 * a * b
    if denominator == 0:
        denominator = 0.01
    cos_C = max(min(numerator / denominator, 1), -1)  # Clamp to avoid domain error
    
    angle_C_rad = math.acos(cos_C)
    angle_C_deg = math.degrees(angle_C_rad)
    
    return angle_C_deg, angle_C_rad


# ── Motor driver pins (Cytron Maker Drive) ─────────────────────────────────────
SPEED = 1023                           # full PWM (0-1023 for ESP32)

M1A = machine.PWM(machine.Pin(13))
M1B = machine.PWM(machine.Pin(12))
M2A = machine.PWM(machine.Pin(27))
M2B = machine.PWM(machine.Pin(33))

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
        
        left_angle, left_rad = angle_from_sides(d_left, 17.8, d_right)
        right_angle, right_rad = angle_from_sides(d_right, 17.8, d_left)

        # ── simple steering logic ────────────────────────────────────────────
        if d_mid <= 5:                 # obstacle right ahead → full stop
            m1_rev()
            m2_rev()
            continue

        lr_gap = abs(d_left - d_right)

        if abs(left_angle - right_angle) <= 80:
            # Path is centered → drive straight
            if d_mid >= 20:
                m1_fwd(); m2_fwd()
                continue
            
            else:
                all_stop()
        elif left_angle > right_angle:
            # more space on the left → veer left (slow/stop left motor)
            m1_fwd()                  # left track slow
            m2_stop()
            continue# right track fast
        else:
            # more space on the right → veer right
            m2_fwd()
            m1_stop()
            continue

    except (ValueError, IndexError) as err:
        print("Parse error:", err)