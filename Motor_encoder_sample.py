import machine
import utime

# User-defined settings
ELAPSED_TIME = 30  # Time interval in milliseconds for calculations and state changes
ENCODER_RESOLUTION = 700 # FOr DFRobot 12V DC motor it is 700. 

# Define motor control pins for the Cytron Maker Drive
MOTOR_M1A_PIN = machine.PWM(machine.Pin(27))
MOTOR_M1B_PIN = machine.PWM(machine.Pin(33))

# Define encoder pins
ENCODER_A_PIN = machine.Pin(25, machine.Pin.IN, machine.Pin.PULL_UP)
ENCODER_B_PIN = machine.Pin(26, machine.Pin.IN, machine.Pin.PULL_UP)

# Motor speed
SPEED = 1023  # Set to maximum speed

# Encoder counter
encoder_count = 0

def encoder_handler(pin):
    global encoder_count
    if pin == ENCODER_A_PIN:
        if ENCODER_B_PIN.value():
            encoder_count += 1
        else:
            encoder_count -= 1
    elif pin == ENCODER_B_PIN:
        if ENCODER_A_PIN.value():
            encoder_count -= 1
        else:
            encoder_count += 1

# Attach the interrupt handlers to the encoder pins
ENCODER_A_PIN.irq(trigger=machine.Pin.IRQ_RISING, handler=encoder_handler)
ENCODER_B_PIN.irq(trigger=machine.Pin.IRQ_RISING, handler=encoder_handler)

def read_and_reset_encoder():
    global encoder_count
    irq_state = machine.disable_irq()  # Disable interrupts
    value = encoder_count
    encoder_count = 0
    machine.enable_irq(irq_state)      # Re-enable interrupts
    return value

def motor_forward():
    MOTOR_M1A_PIN.duty(SPEED)
    MOTOR_M1B_PIN.duty(0)

def motor_backward():
    MOTOR_M1A_PIN.duty(0)
    MOTOR_M1B_PIN.duty(SPEED)

def motor_stop():
    MOTOR_M1A_PIN.duty(0)
    MOTOR_M1B_PIN.duty(0)

# Main loop with user-defined elapsed time and labeled output
last_time = utime.ticks_ms()
last_encoder_time = last_time
state = "forward"
while True:
    current_time = utime.ticks_ms()
    time_difference = utime.ticks_diff(current_time, last_time)
    encoder_timer_difference = utime.ticks_diff(current_time, last_encoder_time)

    if encoder_timer_difference >= ELAPSED_TIME:
    # Calculate speed in encoder counts per second
        counts = read_and_reset_encoder()
#         if abs(counts) > 0:
        speed_cps = counts / (ELAPSED_TIME / 1000)
        speed_rev = speed_cps/ENCODER_RESOLUTION
        print(f"Speed: {speed_cps:.2f} counts/second, {speed_rev:.2f} revs/second")
        last_encoder_time = current_time

    #if time_difference >= 2000:  # 2 seconds have passed
        
        #if state == "forward":
        #    motor_backward()
          #  state = "backward"
        #elif state == "backward":
         #   motor_stop()
         #   state = "stop"
        #elif state == "stop":
    motor_forward()
        #    state = "forward"
        
        #last_time = current_time
