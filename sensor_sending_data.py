import network
import espnow
from hcsr04 import HCSR04
from time import sleep

# Initialize WLAN interface for ESP-NOW
sta = network.WLAN(network.STA_IF)  # Or network.AP_IF
sta.active(True)
sta.disconnect()  # For ESP8266

# Initialize ESP-NOW
e = espnow.ESPNow()
e.active(True)

# Define the peer's MAC address (replace with actual MAC)
peer = b'\x14\x2b\x2f\xaf\x02\x58'
peer2 = b'\x10\x06\x1c\x17\x3b\x44' # MAC address of peer's wifi interface
e.add_peer(peer)  # Must add_peer() before send()
e.add_peer(peer2)
# Initialize the HC-SR04 ultrasonic sensor
sensor_middle = HCSR04(trigger_pin=32, echo_pin=14, echo_timeout_us=10000)
sensor_left = HCSR04(trigger_pin=13, echo_pin=12, echo_timeout_us=10000)
sensor_right = HCSR04(trigger_pin=27, echo_pin=33, echo_timeout_us=10000)

# Send a startup message to the peer
e.send(peer, "Starting...")
e.send(peer2, "Starting...")

# Main loop to continuously read distance and send data via ESP-NOW
# Main loop to continuously read distance and send data via ESP-NOW
extra_value = 30  # Start with an initial value

while True:
    d_mid = sensor_middle.distance_cm()  # Read the distance in cm from the sensor
    d_left = sensor_left.distance_cm()
    d_right = sensor_right.distance_cm()
    
    # Oscillate the extra_value between 0 and 1
    extra_value = 31 - extra_value  # Toggle between 0 and 1
    
    
    payload = f"{d_mid:.1f},{d_left:.1f},{d_right:.1f},{extra_value}"
    e.send(peer, payload)
    e.send(peer2, payload)
    print("TX:", payload)

    sleep(0.001)
