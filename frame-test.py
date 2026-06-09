import crc_calc as crc
import serial
import struct
import time

try:
    # Open real hardware serial port
    ser = serial.Serial('/dev/serial0', baudrate=420000, timeout=1)
    ser.reset_output_buffer()
    
    print("HAMMER SCRIPT ALIVE: Flooding 0x0001 with 42.0...")
    
    # Pre-build a perfect frame so there is zero processor overhead
    payload_bytes = struct.pack('>f', 42.0)
    id_bytes = struct.pack('>H', 0x0001)
    full_payload = id_bytes + payload_bytes
    packet_body = bytes([0x80]) + full_payload
    crc_val = crc.crsf_crc8(packet_body)
    packet = bytes([0xC8, len(full_payload) + 2]) + packet_body + bytes([crc_val])

    while True:
        ser.write(packet)
        time.sleep(0.05) # Send 20 times a second aggressively

except KeyboardInterrupt:
    print("Stopped")