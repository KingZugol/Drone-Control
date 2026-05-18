import time
from pymavlink import mavutil

# Establish the hardware connection to the Flight Controller UART
master = mavutil.mavlink_connection('/dev/serial0', baud=115200)
master.wait_heartbeat()
print("Connected to ArduPilot!")

try:
    while True:
        # The exact raw float you want to display on your RadioMaster Boxer
        cc_temp = 42.5  

        # ArduPilot natively routes 'Tuning1' down the 0x5007 parameter slot
        # The string must be exactly 10 bytes padded with null characters
        name_bytes = b'Tuning1\x00\x00\x00'

        master.mav.named_value_float_send(
            time_boot_ms=int(time.time() * 1000) & 0xFFFFFFFF,
            name=name_bytes,
            value=float(cc_temp) # Broadcast your real float metric
        )
        
        print(f"Injecting into ArduPilot Param Slot: {cc_temp}")
        
        # Ingest incoming background data bytes to prevent the Pi's UART buffer from choking
        while master.iorecv.read(1000):
            pass

        time.sleep(1.0) # Maintain a stable 1Hz transmission rate

except KeyboardInterrupt:
    print("Exiting...")