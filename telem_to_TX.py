import time
from pymavlink import mavutil

# 1. Connect to the Flight Controller UART
master = mavutil.mavlink_connection('/dev/serial0', baud=115200)
master.wait_heartbeat()
print("Connected to ArduPilot!")

try:
    while True:
        # Define the custom data you want to display on your Boxer:
        cc_temp = 42.5    # We will map this to Latitude
        gas_ppm = 115.0   # We will map this to Longitude
        humidity = 65.0   # We will map this to Altitude (in meters)

        # MAVLink expects GPS coordinates as integers scaled by 1E7
        # 42.5 degrees becomes 425000000
        lat_encoded = int(cc_temp * 10000000)
        lon_encoded = int(gas_ppm * 10000000)
        
        # Altitude expects millimeters integer
        # 65.0 meters becomes 65000mm
        alt_encoded = int(humidity * 1000)

        # Send GPS_INPUT message to ArduPilot (maps to a secondary GPS unit)
        master.mav.gps_input_send(
            time_usec=int(time.time() * 1000000),
            gps_id=1,                                 # GPS Instance 2
            ignore_flags=0,                           # Don't ignore inputs
            time_week_ms=0,
            time_week=0,
            fix_type=3,                               # 3D Fix (forces data to lock)
            lat=lat_encoded,                          # Holds your CC Temperature
            lon=lon_encoded,                          # Holds your Gas PPM
            alt=alt_encoded,                          # Holds your Humidity
            hdop=1.0, vdop=1.0,
            vn=0, ve=0, vd=0,                         # Speed vectors empty
            speed_accuracy=1, horizontal_accuracy=1, vertical_accuracy=1,
            satellites_visible=10                     # Forces link status active
        )
        
        print(f"Injecting Matrix -> Lat(Tmp):{cc_temp} | Lon(Gas):{gas_ppm} | Alt(Hum):{humidity}")
        time.sleep(1) # Stream at a stable 1Hz frequency

except KeyboardInterrupt:
    print("Exiting...")