import time
from pymavlink import mavutil
#Connecting to FC over serial
master = mavutil.mavlink_connection('dev/serial0', baud=115200)

print("Waiting for FC hearbeat...")
master.wait_heartbeat()
print("Connected to FC!")

def send_custom_telemetry(name, value):
    """
    Sends a named float value. 
    ArduPilot maps this to CRSF telemetry which EdgeTX can discover.
    """
    # Ensure the name is exactly 10 characters or fewer
    name_bytes = name.encode('utf-8')[:10].ljust(10, b'\x00')
    
    master.mav.named_value_float_send(
        time_boot_ms=int(time.time() * 1000) & 0xFFFFFFFF,
        name=name_bytes,
        value=float(value)
    )

try:
    while True:
        cc_temp = 42.5

        send_custom_telemetry("TCPU", cc_temp)
        print(b"Sent custom Telemetry: TCPU -> " + str(cc_temp).encode('utf-8'))
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting")