import network

def get_mac_address():
    # Create a WLAN object in station mode.
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    
    # Retrieve the MAC address (returned as a bytes object).
    mac = sta_if.config('mac')
    
    # Format the MAC address as a human-readable string.
    formatted_mac = ':'.join('{:02x}'.format(b) for b in mac)
    return formatted_mac

# Print the MAC address.
print("MAC Address:", get_mac_address())