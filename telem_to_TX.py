import time
from pymavlink import mavutil

# 1. Establish the UART connection to the Flight Controller
master = mavutil.mavlink_connection('/dev/ttyAMA0', baud=921600)

print("Waiting for ArduPilot heartbeat...")
master.wait_heartbeat()
print("Connected!")

# === THE PERMANENT STREAM FIX ===
# Force ArduPilot's serial scheduler to broadcast data streams over the UART link
# Param 1: Stream ID classification (MAV_DATA_STREAM_ALL = 0)
# Param 2: Forced Transmission Rate in Hz (10 packets per second)
# Param 3: Active State Trigger Flag (1 = ON / Start Stream)
master.mav.request_data_stream_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink_connection.MAV_DATA_STREAM_ALL, 
    10, 
    1   
)
print("Hardware stream rate override injected successfully.")

try:
    while True:
        # Actively clear out incoming background messages to prevent buffer choke
        while master.iorecv.read(1000):
            pass 

        current_time = time.time()

        # Stream your variable to the vacant lane 0x06
        cc_temp = 42.5  
        scaled_value = int(cc_temp * 10)

        master.mav.named_value_float_send(
            time_boot_ms=int(current_time * 1000) & 0xFFFFFFFF,
            name=b'CCompTmp\x00\x00',
            value=float(scaled_value)
        )
        
        print(f"Streaming data line -> {cc_temp}")
        time.sleep(0.2) # Fast 5Hz processing cycle

except KeyboardInterrupt:
    print("Exiting stream...")