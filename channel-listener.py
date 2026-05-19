from pymavlink import mavutil
import time
master = mavutil.mavlink_connection('/dev/serial0', baud=115200)
master.wait_heartbeat()
print("Connected to Ardupilot!")

message= master.mav.command_long_encode(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL,
    0,
    65,  # Command Id: RC_CHANNELS
    50000,  # Interval in ms 50000 = 20hz
    0, 0, 0, 0, 0 # Empty params
)
master.mav.send(message)
response = master.recv_match(type='RC_CHANNELS', blocking=True)
if response and response.command == mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL and response.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
    print("Command accepted")
    pwm_val = response.chan8_raw
    print("Num channels: " + response.chan_count)
    print(f"All message attributes: {response.__dir__()}")
    print(f"Raw PWM recieved: {pwm_val}")
else:
    print("Command failed")
'''
try:
    while True:
        response = master.recv_match(type='RC_CHANNELS', blocking=True)
        print("Num channels: " + response.chan_count)
        print(f"All message attributes: {response.__dir__()}")
        pwm_val = response.chan8_raw
        print(f"Raw PWM recieved: {pwm_val}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Exiting...")
'''