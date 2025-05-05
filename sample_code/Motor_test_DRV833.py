import machine
import utime

# Define motor control pins for the Cytron Maker Drive
MOTOR_M1A_PIN = machine.PWM(machine.Pin(27))
MOTOR_M1B_PIN = machine.PWM(machine.Pin(33))

MOTOR_M2A_PIN = machine.PWM(machine.Pin(13))
MOTOR_M2B_PIN = machine.PWM(machine.Pin(12))

# Motor speed (adjusted for safety)
SPEED = 1023


def m1_motor_forward():
    MOTOR_M1A_PIN.duty(SPEED)
    MOTOR_M1B_PIN.duty(0)

def m1_motor_backward():
    MOTOR_M1A_PIN.duty(0)
    MOTOR_M1B_PIN.duty(SPEED)

def m1_motor_stop():
    MOTOR_M1A_PIN.duty(0)
    MOTOR_M1B_PIN.duty(0)
    
def m2_motor_forward():
    MOTOR_M2A_PIN.duty(SPEED)
    MOTOR_M2B_PIN.duty(0)

def m2_motor_backward():
    MOTOR_M2A_PIN.duty(0)
    MOTOR_M2B_PIN.duty(SPEED)

def m2_motor_stop():
    MOTOR_M2A_PIN.duty(0)
    MOTOR_M2B_PIN.duty(0)

# Main loop
while True:
    #m1_motor_forward()
    #m2_motor_forward()
    #utime.sleep(25)

    #m1_motor_backward()
    m1_motor_forward()
    m2_motor_backward()
    
    utime.sleep(20)

    m1_motor_stop()
    m2_motor_stop()
    utime.sleep(2)
