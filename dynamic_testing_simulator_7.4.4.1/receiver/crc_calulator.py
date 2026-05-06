#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 13 16:49:29 2024

@author: root
"""
CRC_START_32 = 0xFFFFFFFF
CRC_POLY_32 = 0x82608EDB
crc_tab32_init = False

def init_crc32_tab():
    crc_tab32 = [0] * 256
    for i in range(256):
        crc = i
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ CRC_POLY_32
            else:
                crc >>= 1
        crc_tab32[i] = crc
    return crc_tab32

def crc_32(input_str):
    crc_tab32 = init_crc32_tab()
    crc = CRC_START_32
    for char in input_str:
        long_c = 0xFF & char
        tmp = crc ^ long_c
        crc = (crc >> 8) ^ crc_tab32[tmp & 0xFF]
    crc ^= 0xFFFFFFFF
    return crc & 0xFFFFFFFF

def is_crc_ok(byte_stream):
    content = byte_stream[:-4]
    recieved_crc_bytes = byte_stream[-4:]  
    # recieved_crc_int = struct.unpack('=I',recieved_crc) 
    recieved_crc_int = int.from_bytes(recieved_crc_bytes, byteorder='little')
    
    calculated_crc = crc_32(content)   
    # print("calculated_crc",calculated_crc)
    # print("recieved_crc_int",recieved_crc_int)                          
    if recieved_crc_int == calculated_crc:
        return True
    else:
        return False