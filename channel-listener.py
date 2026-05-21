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
response = master.recv_match(type='COMMAND_ACK', blocking=True)
pwm_val = 0
gvar_pwm= 0 
if response and response.command == mavutil.mavlink.MAV_CMD_SET_MESSAGE_INTERVAL and response.result == mavutil.mavlink.MAV_RESULT_ACCEPTED:
    print("Command accepted")
    try:
        while True:
            while True:
                channel_response = master.recv_match(type='RC_CHANNELS', blocking=False)
                if not channel_response:
                    break
                pwm_val = channel_response.chan8_raw
                gvar_pwm = channel_response.chan11_raw
            print(f"Channel 8 PWM: {pwm_val}")
            gvar = round((gvar_pwm -1500) * 0.2)
            print(f"Channel 11 PWM: {gvar_pwm}, GVAR: {gvar}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Exiting...")
else:
    print("Command failed")

#### Works ####
