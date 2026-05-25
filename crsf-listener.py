import crc_calc as crc
import serial
import struct
import time
import RPi.GPIO as GPIO

#GPIO numbering mode
GPIO.setmode(GPIO.BOARD)
#Pin 18 als output
GPIO.setup(18,GPIO.OUT)
servo1=GPIO.PWM(18,50) #Pin 18 out, 50hz
servo1.start(0)

def parse_crsf(port):
    if port.in_waiting >=10:
        while port.in_waiting > 0:
            header = port.read(1)
            #print(f"header recieved: {header}")
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
            frame_type = packet_body[0]
            if frame_type == 0x50:
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
            servo1.ChangeDutyCycle(val)
        time.sleep(0.001)

except KeyboardInterrupt:
    print('exiting')
finally:
    servo1.stop()
    GPIO.cleanup()
    if 'port' in locals() and port.is_open:
        port.close()