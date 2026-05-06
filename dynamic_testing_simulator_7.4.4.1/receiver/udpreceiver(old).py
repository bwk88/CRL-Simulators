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
import crc_calulator
# from PyQt5 import QtWidgets

class UdpReceiver:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(1)
        self.sock.bind(('',  int(config.sock_rcv_port)))
        self.previous_received_message = "NULL"
        # print("Will Receive",config.sock_rcv_port)
        # self.signal_change_text = QtCore.pyqtSignal(str)
        # self.signal_change_text.connect(config.display.update_content)
        
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
    
    
    def unpack_numbers(self, packed_data, bit_sizes):
        total_bits = sum(bit_sizes)
        packed_data = int.from_bytes(packed_data, byteorder='big')
        numbers = []
        shift = total_bits
        for bits in bit_sizes:
            shift -= bits
            mask = (1 << bits) - 1
            number = (packed_data >> shift) & mask
            numbers.append(number)
        return numbers    

    def extract_bits(self, byte, start, end, shift):
        if start < 0 or end > 7 or start > end:
            raise ValueError('Invalid Start Or End position. Must be 0 <= start <= end <= 7')
        mask = (1 << (end - start + 1)) - 1
        # print('mask:', mask, 'bits: ', bin(mask) )
        shifted_byte = byte >> shift
        # print('shifted_byte:', shifted_byte, 'bits: ', bin(shifted_byte) )
        extracted_bits = shifted_byte & mask
        # print('extracted_bits:', extracted_bits, 'bits: ', bin(extracted_bits) )
        return extracted_bits

    # def show_error_message(self, error_message):     
    #     msg = QtWidgets.QMessageBox()
    #     msg.setIcon(QtWidgets.QMessageBox.Critical)
    #     msg.setText('Error In Receiving')
    #     msg.setInformativeText(error_message)
    #     msg.setWindowTitle('Error')
    #     msg.exec_()
        
    def startReceiving(self):
        
        while True:
            if config.keepRunning == False:
                # print("Not Receiving")
                time.sleep(1)
                
            else:       
                try:
                    data, address = self.sock.recvfrom(2000)  # Adjust the buffer size as needed
    
                    hex_list = [format(val, '02x') for val in data]
                    print("Raw hex data",hex_list)
                    hex_string = ' '.join(hex_list)
                    print('hex_string:', hex_string)
                    # int_list = []
                    # for hex_val in hex_string.split(' '):
                    #     # print('hex_val = ', hex_val)
                    #     int_val = int('0x'+hex_val, 16)
                    #     int_list.append(int_val)
                    # print('int_list:', int_list)  
                    # data_from_hex_string = ''.join(hex_list)  
                    # print("DATA     :", str(data))
                    # print('bytearray:', bytearray.fromhex(data_from_hex_string))  
                    observation_string = ''
                    # print('is_crc_ok ? ', )
                    if not crc_calulator.is_crc_ok(data):
                        observation_string = 'CRC Failed'
                        
                    
                    # self.check_crc(hex_string)
                    config.log(f'{hex_string}')  
                except socket.timeout:
                    config.isReceiving=False
                    config.selected_message_status_on_receiver=0
                    # print("Timed Out")
                    continue
                
                header_format_rcv = config.header_formats[0]
                # header_length_rcv = struct.calcsize(f'={header_format_rcv}') #getting the header length
                
                
                try:
                    # if internal header
                    # header_tuple_rcv = struct.unpack(f'=',data[0:header_length_rcv]) #unpacking only header
                    header_tuple_rcv = 12
                except (struct.error, ValueError):
                    # if external header
                    src_id = data[0]
                    msg_id = data[4]
                    msg_name = config.get_message_name_of_external(msg_id, src_id)
                    header_format_rcv = 'B B'
                    header_length_rcv = struct.calcsize(f'={header_format_rcv}') #getting the header length
                    rcv_msg_len = len(data)
                    
                else:
                    src_id = data[config.src_id_index]
                    dest_id = data[config.dest_id_index]
                    msg_id = data[config.message_id_index]
                    msg_name = config.get_message_name_by_msgID(data[5])
                    # hdrList = self.getMsgListFromMsgTuple(header_tuple_rcv)
                    # rcv_msg_len = hdrList[config.message_len_index]
                print("--------------------------------------------- ")   
                print("msg_name  ",msg_name)
                print("src_id  ",src_id)
                print("msg_id ",data[5])
                
                #rcv_msg_len = data[config.message_len_index]
                #print(data)
                #print(data[config.message_len_index])
                
                if(msg_name != config.message_selected):
                    config.selected_message_status_on_receiver=0
        
            
                # print("RCV SRC_ID:",src_id, ",RCV MSG ID:",msg_id, ",RCV MSG LEN:",rcv_msg_len)

                print()
                if(msg_name != 'UNKNOWN'):
                    content_format_list = config.modified_content_dictionary[msg_name]
                    print(content_format_list)
                    content_format_string = ' '.join(map(str,content_format_list))
                    content_format_list_len = struct.calcsize(f'={content_format_string}') #getting the content length
                    # shud_be_msg_len = header_length_rcv + content_format_list_len
                    # print('content_lenght and header_lenght------------', content_format_list_len, header_length_rcv)
                    # print("shud_be_msg_len:",shud_be_msg_len,  ",RCV MSG LEN:",rcv_msg_len)
                    # if rcv_msg_len != shud_be_msg_len:
                    #     observation_string = 'MSG LEN Failed'
                    
                datetime_now = datetime.datetime.now()
                # datetime_str = datetime_now.strftime("%Y.%m.%d %H:%M:%S")
                datetime_str = datetime_now.strftime('%F %T.%f')[:-3]
    
                config.update_table_entry(datetime_str, msg_name, hex_string, observation_string)
                
                
                # print('Message found with msg_name : ',msg_name)
                
                # 'VATC_RATC_ATP_REPORT_MESSAGE'
                # if msg_name not in ['RATC_CBI_INDICATION_MSG','RATC_VATC_ATP_COMMAND_MSG','VATC_RATC_ATP_REPORT_MESSAGE','RCP_VATC_INFO','VATC_RATC_ATO_REPORT_MESSSAGE','VATC_DMI_COMMAND_MESSAGE']:
                #     continue

                content_format= ''
                header_format= ''
                hdrList = []
                completeList = []
                content_sublist = []
                content_str = ''
                header_str = ''
                header_dict = {}
                content_dict = {}
                
                # try:   
                if(msg_name != 'UNKNOWN' and observation_string != 'MSG LEN Failed'):
                    content_format_list = config.modified_content_dictionary[msg_name]
                    
                    content_format = ' '.join(map(str,content_format_list[:])) ###########
                    header_format = config.header_dictionary[msg_name]
                    crc_format = config.crc_dictionary[msg_name]
                    bits_list = config.bits_list_dictionary[msg_name]
                    bits_format = config.bits_dictionary[msg_name]
                    # header_length = struct.calcsize(f'={header_format}') #getting the header length
                    # num_elements_header = len(header_format.replace(' ',''))
                    # header_tuple = struct.unpack(f'={header_format}',data[0:header_length]) #unpacking only header 
                    # hdrList = self.getMsgListFromMsgTuple(header_tuple)
                    # header_str = ' '.join(map(str,hdrList))

                    
                    if bits_format == 'bytes':
                        # print('    modified content_format list:',content_format)
                        complete_tuple = struct.unpack(f'={content_format}',data[0:])
                        temp_list = self.getMsgListFromMsgTuple(complete_tuple)
                        # print('content_list -> ',temp_list)
                        completeList = self.getStringifiedMsgList( temp_list )
                        content_str = ' '.join(map(str,completeList[:]))
                        # content_sublist = completeList[num_elements_header:] 

                        sizeForByte = 0
                        shift = 0
                        modified_value_list = []
                        modified_value_dict = {}
                        content_sublist_index = 0

                        # for y,b in enumerate(bits_list):
                        #     # print('b = ', b)
                        #     if b >= 8 :
                        #         modified_value_list.append(content_sublist[content_sublist_index])
                        #         content_sublist_index += 1
                        #     else:
                        #         sizeForByte = sizeForByte + b
                        #         byteValue = content_sublist[content_sublist_index]
                        #         # binaryByteValue = bin(byteValue)
                        #         # print('binaryByteValue: ', binaryByteValue)
                        #         start = 8 - sizeForByte
                        #         end = start + b - 1
                        #         shift = sizeForByte - b
                        #         extracted_content = self.extract_bits(byteValue, start, end, shift)
                        #         # print('b size:', b, ', Start:', start, ', End:', end,', extracted_bit_content', extracted_content)
                        #         modified_value_list.append(extracted_content)
                                
                        #         if sizeForByte == 8:
                        #             # print('byte complete......')
                        #             sizeForByte = 0
                        #             content_sublist_index += 1
                        # # print('Modified_value_list -> ',modified_value_list)
                        
                        if(msg_name == config.message_selected):
                            #Rigzin 24/12/2024 Adding new datatype to store the header_str and content_str as dictionary where key is message_name
                            if self.previous_received_message == msg_name:
                                config.selected_message_status_on_receiver = 1
                            self.previous_received_message = msg_name
                            
                            header_dict[msg_name] = header_str
                            content_dict[msg_name] = content_str
                            modified_value_dict[msg_name] = content_str
                            #End
                            
                            # config.update_display_header(header_dict)
                            config.update_display_content(content_dict)
                            config.update_bytes_display_content(modified_value_dict) 

                            # labels_list = config.labels_list_dictionary[msg_name]
                            # print(' ')
                            # print('VVV******************* START OF MESSAGE ********************VVV')
                            # print('For Message Name:',msg_name)
                            # for i,label in enumerate(labels_list):
                            #     print('    ', label,' : ',modified_value_list[i]) 
                            # print('^^^******************** END OF MESSAGE **********************^^^')  
                        
                    elif(bits_format == 'ratc_cbi_indication_bits' or bits_format == 'cbi_ratc_indication_bits') :
                        print("RATC_CBI_indication_bits")
                        header_length = struct.calcsize(f'={header_format}') #getting the header length
                        content_length = struct.calcsize(f'={content_format}') #getting the content length    
                        msg_len = header_length + content_length + 4  #4 is CRC length
                        print('msg_len:',msg_len, ', header_format:',header_format, ', content_format:',content_format)

                        complete_tuple = struct.unpack(f'={header_format}{content_format}{crc_format}',data)
                        temp_list = self.getMsgListFromMsgTuple(complete_tuple)
                        print('temp_list -> ',temp_list)
                        completeList = self.getStringifiedMsgList( temp_list )
                        content_str = ' '.join(map(str,completeList[num_elements_header:]))
                        content_sublist = completeList[num_elements_header:]
                        records = completeList[num_elements_header + 1 : len(completeList)-1]
                        print('records -> ',records)
                        bitPositionList = []
                        bitPositionList_dict = {}
                        for i,x in enumerate(records):
                            if records[i] != 0:
                                # print(records[i])
                                for j in range(7, -1, -1):
                                    bit = (records[i]>> j) & 1
                                    if bit == 1:
                                        bitPositionList.append(i*8+j)
                        print('bitPositionList:',bitPositionList)
                        if(msg_name == config.message_selected):
                            #Rigzin 24/12/2024 Adding new datatype to store the header_str and content_str as dictionary where key is message_name
                            if self.previous_received_message == msg_name:
                                config.selected_message_status_on_receiver = 1    
                            self.previous_received_message = msg_name
                            
                            header_dict[msg_name] = header_str
                            content_dict[msg_name] = content_str
                            bitPositionList_dict[msg_name]= bitPositionList
                            config.update_display_header(header_dict)
                            config.update_display_content(content_dict)
                            config.update_set_bit_list_msg_id_for_display(bitPositionList_dict, msg_id)
                            
                else:
                    print('MSG NOT Identifiable...')
                    header_format = config.header_formats[0]
                    # header_length = struct.calcsize(f'={header_format}') #getting the header length
                    # header_tuple = struct.unpack(f'={header_format}',data[0:header_length]) #unpacking only header 
                    # hdrList = self.getMsgListFromMsgTuple(header_tuple)
                    # header_str = ' '.join(map(str,hdrList)) 
                # except Exception as e:
                #     self.show_error_message(str(e))
            


rcvr = UdpReceiver()
