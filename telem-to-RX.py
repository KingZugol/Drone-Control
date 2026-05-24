import crc_calc as crc
import serial
import struct
import time


def send_crsf_data(serial_port, payload,subtype_id,frame_type=0x80):
    device_addr = 0xC8 #Flight Controller Adr. 
    payload_bytes = struct.pack('>f', payload)
    id_bytes = struct.pack('>H', subtype_id)
    full_payload = id_bytes + payload_bytes
    length = len(payload_bytes) + 2

    packet_body = bytes([frame_type]) + full_payload
    crc_val = crc.crsf_crc8(packet_body)

    packet = bytes([device_addr, length]) + packet_body + bytes([crc_val])

    serial_port.write(packet)


try:
    ser = serial.Serial('/dev/serial0', baudrate=420000, timeout=1)
    while True:

        print("Sending Data to RX")
        
        send_crsf_data(ser, 55.5, 0x0001)
        time.sleep(1)
except KeyboardInterrupt:
    print("exiting")