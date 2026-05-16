import time
from pymavlink import mavutil

# Connect to the Flight Controller UART
master = mavutil.mavlink_connection('/dev/serial0', baud=115200)
master.wait_heartbeat()
print("Connected to ArduPilot!")

try:
    while True:
        # The single sensor metric value you want to trace
        my_metric = 42.5  

        # Scale by 10 to preserve 1 decimal place over integer transmission
        # 42.5 becomes 425 (The Lua script divides this back by 10.0)
        scaled_value = int(my_metric * 10)

        # Pad name out to exactly 10 bytes using null characters (\x00)
        # ArduPilot maps this first sequence strictly to data_id 0x5000
        name_bytes = b'CCompTmp\x00\x00'

        master.mav.named_value_float_send(
            time_boot_ms=int(time.time() * 1000) & 0xFFFFFFFF,
            name=name_bytes,
            value=float(scaled_value)
        )
        
        print(f"Injecting single metric: {my_metric} -> Scaled: {scaled_value}")
        time.sleep(1) # Broadcast rate limit at 1Hz

except KeyboardInterrupt:
    print("Exiting...")