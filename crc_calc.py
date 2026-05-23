
import struct
#Berechnen von CRC Wert anhand CRC-8/DVB-S2, verwendet von CRSF
def crsf_crc8(data):
    crc = 0

    for byte in data: 
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^0xD5 ) &0xFF
            else:
                crc = (crc << 1) &0xFF 
        crc &= 0xFF
    return crc



