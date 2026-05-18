import time
from pymavlink import mavutil

# Establish the hardware connection to the Flight Controller UART
master = mavutil.mavlink_connection('/dev/serial0', baud=115200)
master.wait_heartbeat()
print("Connected to ArduPilot! Streaming long-range Tuning telemetry...")

try:
    while True:
        cc_temp = 42.5  

        # Send your raw float directly via the established Tuning1 parameter lane
        master.mav.named_value_float_send(
            time_boot_ms=int(time.time() * 1000) & 0xFFFFFFFF,
            name=b'Tuning1\x00\x00\x00',
            value=float(cc_temp)
        )
        
        print(f"Streaming parameter: {cc_temp}")
        time.sleep(1.0) # Standard 1Hz updates

except KeyboardInterrupt:
    print("Exiting...")