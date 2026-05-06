
import struct

CRC_START_32 = 0xFFFFFFFF
CRC_POLY_32 = 0x82608EDB
crc_tab32_init = False

def init_crc32_tab():
    global crc_tab32, crc_tab32_init
    crc_tab32 = [0]*256
    for i in range(256):
        crc = i
        for j in range(8):
            if crc & 1:
                crc = (crc>>1)^CRC_POLY_32
            else:
                crc = crc>>1
        crc_tab32[i] = crc
    crc_tab32_init = True

init_crc32_tab()

def crc_32(input_str, num_bytes):
    global crc_tab32, crc_tab32_init
    crc = CRC_START_32
    ptr = input_str

    if not crc_tab32_init:
        init_crc32_tab()

    if ptr is not None:
        for a in range(num_bytes):
            long_c = 0x000000FF & int(ptr[a])
            tmp    =  crc ^ long_c
            crc    = (crc >> 8) ^ crc_tab32[tmp & 0xff]

    crc = crc & 0xffffffff
    return crc

initial_crc = 0xFFFFFFFF
polynomial = 0x82608EDB

numBytes = 1
data_to_send = [0] * 128
data_to_send[0]=1

crcPack = struct.pack('B128B', numBytes, *tuple(data_to_send))
print(crc_32(crcPack, 129))





