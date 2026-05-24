import crc_calc as crc
import serial
import struct
import time
import os


def send_crsf_data(serial_port, payload,subtype_id,frame_type=0x80):
    device_addr = 0xC8 #Flight Controller Adr. 
    payload_bytes = struct.pack('>f', payload)
    id_bytes = struct.pack('>H', subtype_id)
    full_payload = id_bytes + payload_bytes
    length = len(full_payload) + 2

    packet_body = bytes([frame_type]) + full_payload
    crc_val = crc.crsf_crc8(packet_body)

    packet = bytes([device_addr, length]) + packet_body + bytes([crc_val])

    serial_port.write(packet)


#Liest linux cpu temperatur aus /thermal/thermal_zone
def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as cpu_file:
           return float(cpu_file.read()) /1000 # Linux speichert CPU Temp in milicelsius
    except:
        return 0.0
#Liest Ram usage aus /proc/meminfo
def get_ram_usage():
    try:
        with open("/proc/meminfo", "r") as ram_file:
            lines = ram_file.readlines()
        ram_total = int(lines[0].split()[1])
        ram_available = int(lines[2].split()[1])
        ram_used = ram_total - ram_available
        return (ram_used/ram_total) * 100.0
    except:
        return 0.0
#Liest CPU auslastung in der letzten 1 minute, Pi Zero verwendet 4 Kern Prozessor werte kommen von 0 - 4.0, 4.0 = 100 auslastung
def get_cpu_usage():
    try:
        load1, _, _ = os.getloadavg()
        cpu_pct = (load1 / 4.0) * 100 # geteilt durch 4 weil 4 kern prozessor, 
        return cpu_pct
    except:
        return 0.0
try:
    ser = serial.Serial('/dev/serial0', baudrate=420000, timeout=1)
    time.sleep(1)
    while True:
        cpu_temp = get_cpu_temp()
        cpu_usage = get_cpu_usage()
        ram_usage = get_ram_usage()
        print("Sending Data to RX")
        
        send_crsf_data(ser, cpu_temp, 0x0001)
        time.sleep(0.01)
        send_crsf_data(ser, cpu_usage, 0x0002)
        time.sleep(0.01)
        send_crsf_data(ser, ram_usage, 0x0003)
        time.sleep(0.01)

        print(f'Sent Temp:{cpu_temp}, CPU%:{cpu_usage}, RAM%:{ram_usage}')
        time.sleep(1)
except KeyboardInterrupt:
    print("exiting")