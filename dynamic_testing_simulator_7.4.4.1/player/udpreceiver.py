#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:50:05 2020

@author: root
"""

import socket
import struct
import datetime
from Configuration import config
import time

class UdpReceiver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
        self.sock.bind(('',  int(config.sock_rcv_port)))
        
    def getDateTimeString(self):
        now = datetime.datetime.now()
        return now
    
    def getMsgListFromMsgTuple(self, msgTuple):
        msgList = []
        for x in range(len(msgTuple)):
            msgList.append(msgTuple[x])
        return msgList
    
    def get_message_name(self,msg_id):
        msg_name = ''
        for key,val in config.id_dictionary.items():
            if(val == msg_id):
                msg_name = key
                return msg_name
        
    def startReceiving(self):
        while True:    
            if config.keepRunning == False:
                # print("Not Receiving")
                time.sleep(1)
            else:       
                try:
                    data, address = self.sock.recvfrom(1000)  # Adjust the buffer size as needed
                except socket.timeout:
                    # print("Timed Out")
                    continue
                # print(data)
                msg_id = data[config.message_id_index]
                msg_name = self.get_message_name(msg_id)

                content_format= ''
                header_format= ''
                hdrList = []
                contentList = []
                
                if(msg_name != ''):
                    content_format = config.content_dictionary[msg_name]
                    header_format = config.header_dictionary[msg_name]
                    bits_format = config.bits_dictionary[msg_name]

                    header_length = struct.calcsize(f'={header_format}') #getting the header length
                    header_tuple = struct.unpack(f'={header_format}',data[0:header_length]) #unpacking only header 
                    hdrList = self.getMsgListFromMsgTuple(header_tuple)
                    if(content_format != 'not'):
                        content_tuple = struct.unpack(f'={content_format}',data[header_length:])
                        contentList = self.getMsgListFromMsgTuple(content_tuple)

                    if(msg_name == config.message_selected):
                        header_string = ' '.join([str(elem) for elem in hdrList]) # converting msglist to string
                        config.update_display_header(header_string)
                        content_string = ' '.join([str(elem) for elem in contentList]) 
                        config.update_display_content(content_string)
                        
                        if(bits_format == 'control_bits' or bits_format == 'alarm_bits' or bits_format == 'indication_bits'):
                            records = contentList[1:len(contentList)-1]
                            bitPositionList = []
                            for i,x in enumerate(records):
                                if records[i] != 0:
                                    # print(records[i])
                                    for j in range(7, -1, -1):
                                        bit = (records[i]>> j) & 1
                                        if bit == 1:
                                            bitPositionList.append(i*8+j)
                                    print(bitPositionList)
                                    config.update_display(bitPositionList)
                                
                else:
                    print('Msg Not in sim_config.xls identifiable')
                    header_format = config.header_formats[0]
                    header_length = struct.calcsize(f'={header_format}') #getting the header length
                    header_tuple = struct.unpack(f'={header_format}',data[0:header_length]) #unpacking only header 
                    hdrList = self.getMsgListFromMsgTuple(header_tuple)
                    
                config.log(f"  Received {hdrList} {contentList}")   
                print(f"  Received: {hdrList} {contentList}")   
        
rcvr = UdpReceiver()
