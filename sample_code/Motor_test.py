import machine
import utime

# Direction control pins only
IN1 = machine.Pin(13, machine.Pin.OUT)
IN2 = machine.Pin(12, machine.Pin.OUT)
ENA = machine.Pin(14, machine.Pin.OUT)
  # Half speed (0–1023 range)

IN3 = machine.Pin(27, machine.Pin.OUT)
IN4 = machine.Pin(33, machine.Pin.OUT)

def m1_motor_forward():
    IN1.value(1)
    IN2.value(0)
    ENA.value(1)

def m1_motor_backward():
    IN1.value(0)
    IN2.value(1)

def m1_motor_stop():
    IN1.value(0)
    IN2.value(0)

def m2_motor_forward():
    IN3.value(1)
    IN4.value(0)

def m2_motor_backward():
    IN3.value(0)
    IN4.value(1)

def m2_motor_stop():
    IN3.value(0)
    IN4.value(0)

# Main loop
while True:
    m1_motor_forward()
    m2_motor_backward()
    utime.sleep(20)

    m1_motor_stop()
    m2_motor_stop()
    utime.sleep(2)