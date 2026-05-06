#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 12:34:24 2025

@author: kuldeepsingh@Indigenous.com
"""

from PyQt5.QtGui import QColor
from debuggerFile import DBUG


def extract_bits( byte, start, end, shift):
    # (byte & ((1<<bits)-1))
    # DBUG.printWhere()
    if start < 0 or end > 7 or start > end:
        raise ValueError('Invalid Start Or End position. Must be 0 <= start <= end <= 7')
    mask = (1 << (end - start + 1)) - 1
    # print('mask:', mask, 'bits: ', bin(mask) )
    shifted_byte = int(byte) >> shift
    # print('shifted_byte:', shifted_byte, 'bits: ', bin(shifted_byte) )
    extracted_bits = shifted_byte & mask
    # print('extracted_bits:', extracted_bits, 'bits: ', bin(extracted_bits) )
    return extracted_bits


def get_bits_from_bytes(bits_list, byteValue):
    sizeForByte=0
    # bits_list = [3,2,3]
    # byteValue = 49
    modified_value_list = []

    for y,b in enumerate(bits_list):
        sizeForByte = sizeForByte + b
        start = 8 - sizeForByte
        end = start + b - 1
        shift = sizeForByte - b
        extracted_content = extract_bits(byteValue, start, end, shift)
        # print('b size:', b, ', Start:', start, ', End:', end,', extracted_bit_content', extracted_content)
        modified_value_list.append(extracted_content)
        if sizeForByte == 8:
            sizeForByte = 0
            return modified_value_list
            # print('byte complete......')
            
        


# x = get_bits_from_bytes()
# print(x)


def depth_color(depth):
    hue = (depth*40)%360
    saturation = int(0.60*255)
    lightness = int(0.45*255)
    
    color = QColor()
    color.setHsl(hue,saturation,lightness)
    return color

def toggle_color(prev):
    colors = [QColor("red"), QColor("green"), QColor("blue")]
    if prev==2:
        prev=0
    else:
        prev+1
        
    return colors[prev], prev

def struct_level_finder(struct_list):
    struct_level_list = struct_list.split(".")
    # print("============",self.attr_stuct_details[i] ,"--------=======", struct_level_list)
    struct_level = len(struct_level_list)
    spaceValue = 0
    if struct_level > 2:
        spaceValue = 20*(struct_level-2)
    
    return spaceValue, struct_level

def clearLayout(layout):
    while layout.count():
        item = layout.takeAt(0)
        w = item.widget()
        if w is not None:        
            item.widget().setParent(None)
            item.widget().deleteLater()
            continue
        
        l = item.layout()
        if l is not None:
            clearLayout(item.layout())
            continue
        
        del item
        
        
def printDict(dict_index, args_list, calledFrom="", value_list=[]): 
    showPrint = False
    if len(args_list)>0:
        DBUG.printDebug(f"\n======= DICT_INDEX {len(dict_index)} {calledFrom} ================", isPrint=showPrint)
        for i in range(len(dict_index)):
            DBUG.printDebugLine(f"{dict_index[i][0]} ", isPrint=showPrint)
            for indx in args_list:
                DBUG.printDebugLine(f"   {dict_index[i][indx]}", isPrint=showPrint)
            DBUG.printDebug("", isPrint=showPrint)
            
        DBUG.printDebug(f"======= END DICT_INDEX {len(dict_index)} ================\n", isPrint=showPrint)
                
    
    
    
    
    
    
    
    