import crc_calc as crc
import serial
import struct


def send_crsf_data(serial_port, val):
    device_addr = 0xC8
    type_id = 0x51

    payload_bytes = struct.pack('>f', val)

    length = len(payload_bytes) + 2

    packet_body = bytes([type_id]) + payload_bytes
    crc_val = crc.crsf_crc8(packet_body)

    packet = bytes([device_addr, len]) + packet_body + bytes([crc])

    serial_port.write(packet)

ser = serial.Serial('dev/serial0', baudrate=420000, timeout=1)
send_crsf_data(ser, 55.5)