import network, espnow, machine, utime

# ── Motor driver pins (Cytron Maker Drive) ─────────────────────────────────────
SPEED = 1023                           # full PWM (0-1023 for ESP32)

M1A = machine.PWM(machine.Pin(27))
M1B = machine.PWM(machine.Pin(33))
M2A = machine.PWM(machine.Pin(13))
M2B = machine.PWM(machine.Pin(12))

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
FWD_THRESHOLD   = 40      # need ≥ 40 cm ahead to keep moving
SIDE_MATCH_GAP  = 4       # (cm) if |left-right| < GAP → treated as “straight”

while True:
    host, msg = e.irecv(1000)          # 1-s timeout
    if not msg:
        
        continue                       # loop again

    s = msg.decode()
    if s == "end":
        break

    try:
        d_mid, d_left, d_right, extra = map(float, s.split(","))
        # ── debug print ──
        print("mid %.1f cm  left %.1f cm  right %.1f cm  extra %.0f"
              % (d_mid, d_left, d_right, extra))

        # ── simple steering logic ────────────────────────────────────────────
        if d_mid < 20:                 # obstacle right ahead → full stop
            all_stop()
            continue

        lr_gap = abs(d_left - d_right)

        if lr_gap <= SIDE_MATCH_GAP:
            # Path is centered → drive straight
            if d_mid >= FWD_THRESHOLD:
                m1_fwd(); m2_fwd()
            else:
                all_stop()
        elif d_left > d_right:
            # more space on the left → veer left (slow/stop left motor)
            m1_stop()                  # left track slow
            m2_fwd()                   # right track fast
        else:
            # more space on the right → veer right
            m2_stop()
            m1_fwd()

    except (ValueError, IndexError) as err:
        print("Parse error:", err)