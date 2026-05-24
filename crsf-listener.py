import crc_calc as crc
import serial
import struct
import time

def parse_crsf(port):
    if port.in_waiting >=10:
        while port.in_waiting > 0:
            header = port.read(1)
            print(f"header recieved: {header}")
            if header == b'\xC8': #Adresse Flightcontroller
                break
            else:
                return None, None
        raw_len = port.read(1)
        if not raw_len:
            return None,None
            
        length = int.from_bytes(raw_len, byteorder='big')
        packet_body = port.read(length - 1)
        crc_value = port.read(1)

        if crc_value == bytes([crc.crsf_crc8(packet_body)]):
            if packet_body == 0x80:
                subtype_id = struct.unpack('>H', packet_body[1:3])[0]
                payload = packet_body[3:7]
                payload_val = struct.unpack('>i', payload)[0]
                    
                return subtype_id, payload_val
                
    return None, None

try:
    port = serial.Serial('/dev/serial0', baudrate=420000, timeout=0.01)
    while True:
    
        sub_id, val = parse_crsf(port)
        if sub_id == 0x0200:
            print(f'EdgeTX Val: {val}')
        time.sleep(0.001)

except KeyboardInterrupt:
    print('exiting')
finally:
    if 'port' in locals() and port.is_open:
        port.close()