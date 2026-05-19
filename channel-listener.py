from pymavlink import mavutil
import time
master = mavutil.mavlink_connection('/dev/serial0', baud=115200)
master.wait_heartbeat()
print("Connected to Ardupilot!")

try:
    while True:
        message = master.recv_match(type='RC_CHANNELS', blocking=True)
        pwm_val = message.chan9_raw
        print(f"Raw PWM recieved: {rawm_pwm}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Exiting...")
