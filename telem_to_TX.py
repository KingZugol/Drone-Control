import time
from pymavlink import mavutil

# 1. Connect to the Flight Controller UART
master = mavutil.mavlink_connection('/dev/serial0', baud=115200)
master.wait_heartbeat()
print("Connected to ArduPilot!")

try:
    while True:
        master.mav.named_value_float_send(time_boot_ms=int(time.time()*) &0xFFFFFFFF), name=b'TCPU\x00\x00\x00\x00\x00\x00', value = float(42.5)) # 6*x00 to make it 10 chars long
        time.sleep(1) # Stream at a stable 1Hz frequency

except KeyboardInterrupt:
    print("Exiting...")