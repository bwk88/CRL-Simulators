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
from PyQt5 import QtCore
from csv_dict import names,dict

class UdpMulticastReceiver:
    def __init__(self):
        multicast_port = int(config.sock_multicast_rcv_port)
        multicast_group = config.sock_multicast_group
        self.multicast_recv_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.multicast_recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.multicast_recv_sock.bind(('', multicast_port))
        self.multicast_recv_sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        self.multicast_recv_sock.settimeout(1)
        mreq = struct.pack("=4sl",socket.inet_aton(multicast_group), socket.INADDR_ANY)
        self.multicast_recv_sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    def getDateTimeString(self):
        now = datetime.datetime.now()
        return now
    
    def getMsgListFromMsgTuple(self, msgTuple):
        msgList = []
        for x in range(len(msgTuple)):
            msgList.append(msgTuple[x])
        return msgList
    
    def getStringifiedMsgList(self, input_list):
        msg_list = []
        for x in range(len(input_list)):
            if(isinstance(input_list[x], bytes)):
                string = input_list[x].decode('utf-8').rstrip('\x00')
                msg_list.append(string)
            else:   
                msg_list.append(input_list[x])
        return msg_list
    
    def get_message_name(self,msg_id):
        msg_name = ''
        for key,val in config.id_dictionary.items():
            if(val == msg_id):
                msg_name = key
                return msg_name
        
    def startReceiving(self):
        while True:    
            # self.sock.bind(('',  int(config.sock_rcv_port)))
            # print("Recieve",config.sock_rcv_port )
            if config.keepRunning == False:
                # print("Not Receiving")
                time.sleep(1)
            else:       
                try:
                    data = self.multicast_recv_sock.recv(8000)
                except socket.timeout:
                    # print("Timed Out")
                    continue
                # print(data)
                msg_id = data[config.message_id_index]
                print("Rcvd on Multicast............Message ID",msg_id)
                msg_name = self.get_message_name(msg_id)

                content_format= ''
                header_format= ''
                hdrList = []
                completeList = []
                content_sublist = []
                content_str = ''
                header_str = ''
                
                if(msg_name != ''):
                    content_format = config.content_dictionary[msg_name]
                    header_format = config.header_dictionary[msg_name]
                    print("Header Format",header_format)
                    crc_format = config.crc_dictionary[msg_name]
                    bits_format = config.bits_dictionary[msg_name]
                
                    header_length = struct.calcsize(f'={header_format}') #getting the header length
                    num_elements_header = len(header_format.replace(' ',''))
                    # print("num_elements_header = ", num_elements_header)
                    header_tuple = struct.unpack(f'={header_format}',data[0:header_length]) #unpacking only header 
                    hdrList = self.getMsgListFromMsgTuple(header_tuple)
                    header_str = ' '.join(map(str,hdrList))
                    
                    if bits_format == 'bytes':
                        byte_msg_formats = []
                        listMessageContents = dict[f'{msg_name}']
                        for i,x in enumerate(listMessageContents):
                            byte_msg_formats.append(x[5])
                        content_format = ' '.join(map(str, byte_msg_formats[0:len(byte_msg_formats) - 1]))
                        
                    if(content_format != 'not'):
                        print("Header Format",header_format)
                        print("Content Format",content_format)
                        print("CRC format",crc_format)
                        # print("recv CRC", data[])

                        complete_tuple = struct.unpack(f'={header_format}{content_format}{crc_format}',data)
                        temp_list = self.getMsgListFromMsgTuple(complete_tuple)
                        print('temp_list -> ',temp_list)
                        completeList = self.getStringifiedMsgList( temp_list )
                        content_str = ' '.join(map(str,completeList[num_elements_header:]))
                        content_sublist = completeList[num_elements_header:]
                        
# =============================================================================
# ATS_CBI_CONTROL_MSG	     1
# CBI_IO_MODULE_CONTROL_DATA	13
# MT_CBI_CONTROL_MSG	         8
# MT_RNR_CONTROL_REPLAY	    74
# VDUD_VDUS_CONTROL_MSG	    64
# VDUS_CBI_CONTROL_MSG 	     9
# 
# 
# CBI_ATS_INDICATION_MSG	            32
# CBI_CBI_NEIGHBOUR_INDICATION_MSG	35
# CBI_MT_INDICATION_MSG	            41 //bit chart mt 
# CBI_RATC_INDICATION_MSG	         6
# CBI_VDUS_INDICATION_MSG      	    29
# IO_MODULE_CBI_INDICATION_DATA	    47
# RATC_CBI_INDICATION_MSG      	     7
# VDUS_VDUD_INDICATION_MSG	        58
#
# VDUS_VDUD_ALARM_OF_VDUS	59
#
# =============================================================================


                        # print('completeList[num_elements_header:]--->>>',completeList[num_elements_header:])

                    # print("config.message_selected = ", config.message_selected)
                    
                    if(msg_name == config.message_selected):
                    # EDIT HERE NEXT

                        config.update_display_header(header_str) 
                        config.update_display_content(content_str) 
                        # self.signal_change_text.emit(content_str)
                        # print("bits_format = ", bits_format)
                        if(bits_format == 'control_bits' or bits_format == 'indication_bits'):
                            records = completeList[num_elements_header + 1 : len(completeList)-1]
                            print('records -> ',records)
                            bitPositionList = []
                            for i,x in enumerate(records):
                                if records[i] != 0:
                                    # print(records[i])
                                    for j in range(7, -1, -1):
                                        bit = (records[i]>> j) & 1
                                        if bit == 1:
                                            bitPositionList.append(i*8+j)
                            print("BitPositionList", bitPositionList)
                            config.update_display(bitPositionList,msg_id)

                        # Added by Angchuk
                        if(bits_format == 'mt_indication_bits'):
                            records = completeList[num_elements_header + 1 : len(completeList)-1]
                            print('records -> ',records)
                            bitPositionList = []
                            for i,x in enumerate(records):
                                if records[i] != 0:
                                    # print(records[i])
                                    for j in range(7, -1, -1):
                                        bit = (records[i]>> j) & 1
                                        if bit == 1:
                                            bitPositionList.append(i*8+j)
                            print("BitPositionList", bitPositionList)
                            config.update_display(bitPositionList)


                        elif(bits_format == 'alarm_bits'):
                            records = completeList[num_elements_header : len(completeList)-8]
                            # print('########records -> ',records)
                            bitPositionList = []
                            for i,x in enumerate(records):
                                if records[i] != 0:
                                    # print(records[i])
                                    for j in range(7, -1, -1):
                                        bit = (records[i]>> j) & 1
                                        if bit == 1:
                                            bitPositionList.append(i*8+j)
                            print(bitPositionList)
                            config.update_display(bitPositionList,msg_id)
# =============================================================================
#                             records = completeList[num_elements_header : num_elements_header + 1]
#                             print('records -> ',records)
#                             bitPositionList = []
#                             for i,x in enumerate(records):
#                                 if records[i] != 0:
#                                     # print(records[i])
#                                     for j in range(63, -1, -1):
#                                         bit = (records[i]>> j) & 1
#                                         if bit == 1:
#                                             bitPositionList.append(i*8+j)
#                             print(bitPositionList)
#                             config.update_display(bitPositionList)    
# =============================================================================
                        elif bits_format == 'bytes':
                            # config.update_bytes_display_content(content_str)
                            config.update_bytes_display_content(content_sublist)
                            
                else:
                    print('Msg Not in sim_config.xls. NOT Identifiable')
                    header_format = config.header_formats[0]
                    header_length = struct.calcsize(f'={header_format}') #getting the header length
                    header_tuple = struct.unpack(f'={header_format}',data[0:header_length]) #unpacking only header 
                    hdrList = self.getMsgListFromMsgTuple(header_tuple)
                    header_str = ' '.join(map(str,hdrList))

                config.log(f'Received {header_str} {content_str}')  
                print(f"  Received: {header_str} {content_str}")   
        
rcvr = UdpMulticastReceiver()
