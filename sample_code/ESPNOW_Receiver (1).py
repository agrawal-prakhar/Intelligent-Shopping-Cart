import network
import espnow
from machine import Pin

# Setup LEDs on GPIO pins 14, 32, 15
led_14 = Pin(14, Pin.OUT)
led_32 = Pin(32, Pin.OUT)
led_15 = Pin(15, Pin.OUT)

# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

e = espnow.ESPNow()
e.active(True)

while True:
    host, msg = e.irecv(1000)  # Wait for message with a timeout of 1000ms
    if msg:  # msg == None if timeout in recv()
        # Convert bytearray to string
        message_str = msg.decode('utf-8')  # Decode bytearray to string

        # Check if the message contains distance and extra information
        if "Distance" in message_str and "Extra" in message_str:
            try:
                # Split message into parts by comma
                parts = message_str.split(',')
                
                # Extract distance value
                distance_str = parts[0].split(':')[1].strip().split()[0]  # Extract the distance value
                distance = float(distance_str)  # Convert to float
                
                # Extract extra value
                extra_str = parts[1].split(':')[1].strip()  # Extract the extra value
                extra = float(extra_str)  # Convert to float if necessary (can keep as string if required)
                
                # Output the parsed data
                print(f"Distance: {distance} cm, Extra: {extra}")
                
                # Turn on/off LEDs based on the distance
                if distance < 20:
                    led_14.value(1)  # Turn on LED 14 for very close distance
                    led_32.value(0)
                    led_15.value(0)
                elif 20 <= distance < 40:
                    led_32.value(1)  # Turn on LED 32 for medium distance
                    led_14.value(0)
                    led_15.value(0)
                else:
                    led_15.value(1)  # Turn on LED 15 for larger distance
                    led_14.value(0)
                    led_32.value(0)
            except ValueError:
                print("Error in parsing distance or extra value")
                
        if message_str == 'end':  # End the loop if message is 'end'
            break
