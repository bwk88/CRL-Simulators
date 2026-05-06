#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 13:50:05 2020

@author: root
"""
from pickle import TRUE
from PyQt5 import QtCore, QtGui, QtWidgets
import socket
import struct
import datetime
from Configuration import config
import time
import crc_calulator
from csv_dict import dict
from dynamicStruc import dynamic_struc
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
    
    def recursive_struct(self, i, shadow_dict_index, data, struct_format, label_format, no_of_repeatitions, bits_list): 
        print("################################## RECURSION #################################################")
        format_string_to_be_repeated = shadow_dict_index[i][2]  
        pos_of_repeat_structure = i+1
        no_of_bits = 0
        print("current_data_format=====", struct_format)
        print("no_of_repeatitions inside recursion",no_of_repeatitions, pos_of_repeat_structure, format_string_to_be_repeated)
        
        
        #when struct is not present at all in the data
        if no_of_repeatitions == 0:
            struc_contains = shadow_dict_index[i+1][8].split('.')
            while(format_string_to_be_repeated in struc_contains and i < len(shadow_dict_index)):
                print(struc_contains[-1])
                if i+1 >= len(shadow_dict_index):
                    i=i+1
                    break
                else:
                    struc_contains = shadow_dict_index[i+1][8].split('.')
                    i+=1
        else:
            rep_index = i
            
            
            #iterate the struct
            for idx in range(0, no_of_repeatitions):
                
                i = rep_index+1  
                struc_contains = shadow_dict_index[i][8].split('.')
                print("legnht--", len(shadow_dict_index))
                print(format_string_to_be_repeated)
                
                
                #to iterate till end of current struct only
                while(format_string_to_be_repeated in struc_contains):
                    # isPart of struct
                    
                    
                    print("rep_index", i)   
                    print("struct contains", struc_contains)
                    print("format to be repeated--", format_string_to_be_repeated)
                    
                    format_of_string = shadow_dict_index[i][5] #Extracting thr format 
                    label_string = shadow_dict_index[i][8].split('.')                   


                    #===bits to byte conversion when bits list is non zero===                   
                    #bits_list is zero
                    if bits_list[i] == 0 and no_of_bits == 0:
                        struct_format.append(format_of_string)
                        label_format.append(label_string[-1:])
                        #current_static_format = dynamic_content_format[:i]                          
                        current_data_format = ' '.join(map(str,struct_format[:]))
                        #unpack till current attribute
                        try:
                            fmt_length = struct.calcsize(f'={current_data_format}')
                            fmt_tuple = struct.unpack(f'={current_data_format}',data[0:fmt_length])
                        except Exception as e:
                            print("incorrect data recieved")
                            print("inside recursion==============",e)
                            return                        
                        no_of_repeatitions = fmt_tuple[-1]
                        
                    #when bits list architecture is wrong in the message    
                    elif bits_list[i] == 0 and no_of_bits != 0:
                        print("Wrong bit field in message")
                        return
                    
                    #when bits list is non zero
                    else:
                        no_of_bits+=bits_list[i]
                        if no_of_bits == 8:
                            struct_format.append(format_of_string)
                            label_format.append(label_string[-1:])
                            #current_static_format = dynamic_content_format[:i]                          
                            current_data_format = ' '.join(map(str,struct_format[:]))
                            try:
                                fmt_length = struct.calcsize(f'={current_data_format}')
                                fmt_tuple = struct.unpack(f'={current_data_format}',data[0:fmt_length])
                            except Exception as e:
                                print("incorrect data recieved")
                                print("inside recursion==============",e)
                                return
                            no_of_repeatitions = fmt_tuple[-1]>>(8-bits_list[i])
                            no_of_bits = 0                        
                        


                        
                    #when nested struct, recursion
                    if (shadow_dict_index[i][2] != ''):
                        if shadow_dict_index[i][10]:
                            # if shadow_dict_index[i][10] != no_of_repeatitions:
                            #     print(f"Invalid number of struct {shadow_dict_index[i][2]}")
                            #     return
                            no_of_repeatitions = int(shadow_dict_index[i][10])
                        label_format, struct_format,i = self.recursive_struct(i, shadow_dict_index, data,struct_format, label_format, no_of_repeatitions, bits_list)
                    else:
                        i+=1
                    
                    if i==len(shadow_dict_index):
                        break
                    struc_contains = shadow_dict_index[i][8].split('.')
                    
        return label_format, struct_format, i
    
    
    def startReceiving(self):
        while True:
            error_flag = 0
            if config.keepRunning == False:
                # print("Not Receiving")
                time.sleep(1)
            else:       
                datetime_now = datetime.datetime.now()
                datetime_str = datetime_now.strftime("%Y.%m.%d %H:%M:%S")
                datetime_str = datetime_now.strftime('%F %T.%f')[:-3]
                try:
                    data, address = self.sock.recvfrom(8000)  # Adjust the buffer size as needed
                    # config.data = data
                    print("LEN=========================",len(data))
                    hex_list = [format(val, '02x') for val in data]
                    # print("Raw hex data",hex_list)
                    hex_string = ' '.join(hex_list)
                    # print('hex_string:', hex_string)
                    # config.complete_data = hex_string
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
                
                
                try:
                    header_format_rcv = config.header_formats[0]
                    # header_length_rcv = struct.calcsize(f'={header_format_rcv}') #getting the header length
                    # header_format_list = ['H','B','B','B' ,'I', 'H', 'B', 'H', 'H', 'B'] #ASM project specific
                            # config.dynamic_header_format = ['H','B','B','B' ,'I', 'H', 'B', 'H', 'H', 'B']
                    header_format_list = ['B','B','H','B','H','B','B','B']  #ATS 
                            
                    header_format = ' '.join(map(str,header_format_list[:]))
                    header_length = struct.calcsize(f'={header_format}')
                    print("Header format",header_format,header_length)
                    header_tuple = struct.unpack(f'={header_format}',data[0:header_length])
                    hdrList = self.getMsgListFromMsgTuple(header_tuple)
                    
                    
                    
                    print("--------------------HeaderList------------------", hdrList)
                    src_id = data[config.src_id_index]
                    dest_id = data[config.dest_id_index]
                    msg_id = data[config.message_id_index]
                    msg_name = config.get_message_name_by_msgID(hdrList[2])
                    # hdrList = self.getMsgListFromMsgTuple(header_tuple_rcv)
                    # rcv_msg_len = hdrList[config.message_len_index]
                    print("--------------------------------------------- ")   
                    print("msg_name  ",msg_name)
                    print("src_id  ",src_id)
                    print("msg_id ",hdrList[2])
                    
                    header_tuple_rcv = 12
                except (struct.error, ValueError):
                    msg_name = "UNKNOWN"
                    # if external header
                    # src_id = data[0]
                    # msg_id = data[4]
                    # msg_name = config.get_message_name_of_external(msg_id, src_id)
                    # header_format_rcv = 'B B'
                    # header_length_rcv = struct.calcsize(f'={header_format_rcv}') #getting the header length
                    # rcv_msg_len = len(data)
                    
                # else:
                    
                
                # msg_len_tuple = struct.unpack(f'=H',data[9:11])
                # hdrList = self.getMsgListFromMsgTuple(msg_len_tuple)
                # msg_len_tuple_str = ' '.join(map(str,hdrList))
                
                # print("len unpack ",msg_len_tuple_str)
                
                # if(len(data) == int(msg_len_tuple_str)):
                #     print("CORRECT LEN rcvd")
                # else:
                #     print("Wrong LEn")
                
                #rcv_msg_len = data[config.message_len_index]
                #print(data)
                #print(data[config.message_len_index])
                
                if(msg_name != config.message_selected):
                    config.selected_message_status_on_receiver=0
                content_format= ''
                header_format= ''
                hdrList = []
                completeList = []
                content_sublist = []
                content_str = ''
                header_str = ''
                header_dict = {}
                content_dict = {}
                dynamic_label_list = []
                complete_tuple = {}
                try:
                    if(msg_name != 'UNKNOWN'):#and observation_string != 'MSG LEN Failed'):
                        content_format_list = config.content_dictionary[msg_name]
                    
                        # content_format = ' '.join(map(str,content_format_list[:-1]))
                        header_format = config.header_dictionary[msg_name]
                        crc_format = config.crc_dictionary[msg_name]
                        bits_list = config.bits_list_dictionary[msg_name]
                        bits_format = config.bits_dictionary[msg_name]
                        header_length = struct.calcsize(f'={header_format}') #getting the header length
                        num_elements_header = len(header_format.replace(' ',''))
                        #print("num_elements", bits_list)
        
                        header_tuple = struct.unpack(f'={header_format}',data[0:header_length]) #unpacking only header 
                        hdrList = self.getMsgListFromMsgTuple(header_tuple)
                        header_str = ' '.join(map(str,hdrList))
                        config.dynamic_header_format.clear()
                        config.dynamic_header_format.append(header_str)

                        #********************************************\
                            
                        # no_of_dest_nodes = header_tuple[9]
                        dynamic_content_format = content_format_list.copy()
                        
                        
                        #list that contain list of each message attributes(ARGUMENT_NAME	, ARGUMENT_TYPE, IRS_VALUE, BitField, INPUT_VALUE, FORMAT, ATR_ARRAY_SIZE, ARGUMENT_SIZE)
                        dict_index = dict[f'{msg_name}'].copy()
                        shadow_dict_index = dict_index.copy()
                        
                        #represents how many times the corresponding struct will be repeated
                        no_of_repeatitions =1
                        
                        # dynamic_label_list = config.labels_list_dictionary[msg_name].copy()
                        # print("Labels--------------->",dynamic_label_list)
                        
                        
                
                        shadow_content_str = ''
                        
                        
                        try:
                            #store format of data till current attributes
                            struct_format = []
                            #store attribute names till current attribute
                            label_format = []
        
                            #represent the current index of iteration when recursion exits
                            index_after_recursion = -1
                            no_of_bits = 0
                            
                            #iterate through all attributes
                            for i,x in enumerate(shadow_dict_index):                            
                                if i <= index_after_recursion-1:
        
                                    continue
                                else:
                                    
                                    #format of the current attributes                           
                                    format_of_string = shadow_dict_index[i][5]
                                    
                                    #label name of current attribute
                                    label_string = shadow_dict_index[i][8].split('.')
                                    
                                    
                                    
                                    #===bits to byte conversion when bits list is non zero===
                                    #bits_list is zero
                                    if bits_list[i] == 0 and no_of_bits == 0:
                                        struct_format.append(format_of_string)
                                        label_format.append(label_string[-1:])
                                        #current_static_format = dynamic_content_format[:i]                          
                                        current_data_format = ' '.join(map(str,struct_format[:]))
                                        #unpack till current attribute
                                        try:
                                            fmt_length = struct.calcsize(f'={current_data_format}')
                                            fmt_tuple = struct.unpack(f'={current_data_format}',data[0:fmt_length])
                                        except Exception as e:
                                            print("incorrect data recieved outside")
                                            print("==============",e)
                                            error_flag = 1
                                            break
        
                                        
                                        no_of_repeatitions = fmt_tuple[-1]
                                        
                                    #when bits list architecture is wrong in the message    
                                    elif bits_list[i] == 0 and no_of_bits != 0:
                                        print("Wrong bit field in message")
                                        return
                                    
                                    #when bits list is non zero
                                    else:
                                        no_of_bits+=bits_list[i]
                                        if no_of_bits == 8:
                                            struct_format.append(format_of_string)
                                            label_format.append(label_string[-1:])
                                            #current_static_format = dynamic_content_format[:i]                          
                                            current_data_format = ' '.join(map(str,struct_format[:]))
                                            try:
                                                fmt_length = struct.calcsize(f'={current_data_format}')
                                                fmt_tuple = struct.unpack(f'={current_data_format}',data[0:fmt_length])
                                            except Exception as e:
                                                print("incorrect data recieved outside")
                                                print("==============",e)
                                                error_flag = 1
                                                break
                                            no_of_repeatitions = fmt_tuple[-1]>>(8-bits_list[i])
                                            no_of_bits = 0
                                    

                                    #recursion starts when "ATR_ARRAY_SIZE" is not NULL(struct repeatation required)
                                    if(shadow_dict_index[i][2] != ''):
                                        
                                        #store name of struct to be repeated
                                        format_string_to_be_repeated = shadow_dict_index[i][2]
                                        
                                        #position of the struct to be repeated
                                        pos_of_repeat_structure = i+1
                                        
                                        
                                        #when static number of struct is required
                                        if shadow_dict_index[i][10]:
                                            # if shadow_dict_index[i][10] != no_of_repeatitions:
                                            #     print(f"Invalid number of struct {shadow_dict_index[i][2]}")
                                            #     error_flag = 1
                                            #     break
                                            
                                            no_of_repeatitions = int(shadow_dict_index[i][10])
                                            
                                            
                                        if no_of_bits:
                                            print("Invalid bit field in message")
                                            error_flag = 1
                                            break
                                        
                                        print("no_of_repeatitions outside recursion",no_of_repeatitions, pos_of_repeat_structure, format_string_to_be_repeated)
                                        print("*************************+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                                        
                                        #pop to be added again inside recursion
                                        # struct_format.pop(-1)
                                        # label_format.pop(-1)
                                        
                                        try:
                                            label_format, struct_format, index_after_recursion = self.recursive_struct(i, shadow_dict_index, data, struct_format, label_format, no_of_repeatitions, bits_list)
                                        except Exception as e:
                                            print("Recursion error",e)
                                            error_flag = 1
                                            break
                                            
                                            
                                        print("Recursion output",struct_format, index_after_recursion)
                                        print("*************************+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                        except Exception as e:
                            config.update_table_entry(datetime_str, msg_name,complete_tuple, content_str,dynamic_label_list, observation_string,content_format,hex_string,data)
                            # self.show_error_message(str(e))

                        
                        if error_flag == 0:
                            print('final struct format', struct_format)
                            config.dynamic_label_lsit = label_format.copy()
                            
                            content_format_list = struct_format
        
                            content_format = ' '.join(map(str,content_format_list[:])) ###########
                            # config.final_format = content_format
                            
                            fmt_length = struct.calcsize(f'={content_format}')
                
                            bits_format = config.bits_dictionary[msg_name]
                            if bits_format == 'bytes':
                                complete_tuple = []
                                try:
                                    print("final content format", content_format)
                                    complete_tuple = struct.unpack(f'={content_format}',data)
                                    print('complete_tuple', complete_tuple)
                                    print("config.complete_data",config.complete_data)
                                    observation_string = "RCVD OK"
                                except Exception as e:
                              
                                    datetime_now = datetime.datetime.now()
                                    datetime_str = datetime_now.strftime('%F %T.%f')[:-3]
                                    observation_string = 'ERROR'
                                    print("invalid data recieved")
                                    continue
                                temp_list = self.getMsgListFromMsgTuple(complete_tuple)
                                # print('content_list -> ',temp_list)
                                completeList = self.getStringifiedMsgList( temp_list )
                                content_str = ' '.join(map(str,completeList[:]))
                                
                                num_elements_header = len(header_format_list)
                                print("header_format_list",header_format_list)
                                
                                content_sublist = completeList[num_elements_header:] 
                                print("content_sublist",content_sublist , len(content_sublist))
                                
                                sizeForByte = 0
                                shift = 0
                                modified_value_list = []
                                modified_value_dict = {}
                                content_sublist_index = 0
                                bits_list = config.bits_list_dictionary[msg_name]
                                
                                # print("bits_list",bits_list,len(bits_list))
                                # print("+++++++++",struct_format,len(struct_format))
                                bits_list = bits_list[num_elements_header:]
                                # for y,b in enumerate(bits_list):
                                print("--------",bits_list)
                                    
                                
                                for y,b in enumerate(bits_list):
                                    print('b', b)
                                    if b >= 8 :
                                        modified_value_list.append(content_sublist[content_sublist_index])
                                        content_sublist_index += 1
                                        # print("8888888888888")
                                    else:
                                        # print("9999999999999")
                                        sizeForByte = sizeForByte + b
                                        byteValue = content_sublist[content_sublist_index]
                                        # binaryByteValue = bin(byteValue)
                                        # print('binaryByteValue: ', binaryByteValue)
                                        start = 8 - sizeForByte
                                        end = start + b - 1
                                        shift = sizeForByte - b
                                        print("start",start,"end",end,"shift",shift)
                                        extracted_content = self.extract_bits(byteValue, start, end, shift)
                                        # print('b size:', b, ', Start:', start, ', End:', end,', extracted_bit_content', extracted_content)
                                        modified_value_list.append(extracted_content)
                                        
                                        if sizeForByte == 8:
                                            print('byte complete......')
                                            sizeForByte = 0
                                            content_sublist_index += 1
                                
                                print('Modified_value_list -> ',modified_value_list,len(modified_value_list))
                                
                                content_format_list = config.modified_content_dictionary[msg_name]
                                print('content_format_list',content_format_list) 
                                content_format_string = ' '.join(map(str,dynamic_content_format))
                                content_format_list_len = struct.calcsize(f'={content_format_string}') #getting the content length
            
                                
                                shud_be_msg_len = content_format_list_len
                                rcv_msg_len = data[6] #6th index is MSG LEN
                        
                                datetime_now = datetime.datetime.now()
                                datetime_str = datetime_now.strftime('%F %T.%f')[:-3]
        
                                
                                # Function to UPDATE ALL SAMPLES HEX
                                content_str = ' '.join(map(str,complete_tuple[:]))

                                print(")))))))))))))))))))))))))))))))))))))))))))))))))))))))")
                                config.update_table_entry(datetime_str, msg_name, modified_value_list,content_str,label_format, observation_string,content_format,hex_string,data)
                                # config.display.update_content(content_str)
                                
                                if(msg_name == msg_name):
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
                                    # config.update_bytes_display_content(modified_value_dict) 
        
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
                                if(msg_name == msg_name):
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
                            error_flag==0
                    else:
                        print('MSG NOT Identifiable...')
                        header_format = config.header_formats[0]
                        
                        observation_string = 'MSG LENGTH MISMATCH OR UNKNOWN'
                        
                        
                        
                        # header_format_list = ['H','B','B','B' ,'I', 'H', 'B', 'H', 'H', 'B'] #ASM project specific
                        header_format_list = ['B','B','H','B','H','B','B','B'] #ATS
                        # config.dynamic_header_format = ['H','B','B','B' ,'I', 'H', 'B', 'H', 'H', 'B']
                        
                        header_format = ' '.join(map(str,header_format_list[:]))
                        header_length = struct.calcsize(f'={header_format}')
                        print("Header format",header_format,header_length)
                        try:    
                            header_tuple = struct.unpack(f'={header_format}',data[0:header_length])
                        except Exception as e:
                            datetime_now = datetime.datetime.now()
                            datetime_str = datetime_now.strftime('%F %T.%f')[:-3]
                            config.update_table_entry(datetime_str, msg_name,complete_tuple, content_str,dynamic_label_list, observation_string,content_format,hex_string,data)
                            # self.show_error_message(str(e))
                        
                        hdrList = self.getMsgListFromMsgTuple(header_tuple)
                        header_str = ' '.join(map(str,hdrList))
                        config.dynamic_header_format.clear()
                        config.dynamic_header_format.append(header_str)
                        
                        config.update_table_entry(datetime_str, msg_name,complete_tuple, content_str,dynamic_label_list, observation_string,content_format,hex_string,data)
                except Exception as e:
                    print("EXCEPTION OCCURED")
                    datetime_now = datetime.datetime.now()
                    datetime_str = datetime_now.strftime('%F %T.%f')[:-3]
                    config.update_table_entry(datetime_str, msg_name,complete_tuple, content_str,dynamic_label_list, observation_string,content_format,hex_string,data)
                    # self.show_error_message(str(e))


    def show_error_message(self, error_message):   
        print("Error",error_message)  
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText('Error In Receiving')
        msg.setInformativeText(error_message)
        msg.setWindowTitle('Error')
        msg.exec_()


rcvr = UdpReceiver()
