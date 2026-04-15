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
header_file_path = './config/message_header.txt'

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
    #     msg.setInformativeText(error_message)s
    #     msg.setWindowTitle('Error')
    #     msg.exec_()
    
    def recursive_struct(self, i, shadow_dict_index, data, struct_format, label_format, dynamic_content_format): 
        print("################################## RECURSION #################################################")
        format_string_to_be_repeated = shadow_dict_index[i][2]  
        pos_of_repeat_structure = i+1
        
        label_string = shadow_dict_index[i][8].split('.')
        struct_format.append(shadow_dict_index[i][5])
        label_format.append(label_string[-1:])

        #print("Processing row: ", format_string_to_be_repeated, pos_of_repeat_structure, struct_format)
        
        current_static_format = dynamic_content_format[:pos_of_repeat_structure]
        current_data_format = ' '.join(map(str,struct_format[:]))
        fmt_length = struct.calcsize(f'={current_data_format}')
        

        try:
            #print("sjskkfhffk------------------------", current_data_format)
            fmt_tuple = struct.unpack(f'={current_data_format}',data[:fmt_length])

        except Exception as e:
            print("Error in recursion",e)
            # self.show_error_message(str(e))

        no_of_repeatitions = fmt_tuple[-1]
        print("current_data_format=====", struct_format)
        print("no_of_repeatitions inside recursion",no_of_repeatitions, pos_of_repeat_structure, format_string_to_be_repeated)

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
            print("rep_index", i)
            for idx in range(0, no_of_repeatitions):
                i = rep_index+1                   
                while(i<len(shadow_dict_index)):
                    # isPart of struct
                    
                    struc_contains = shadow_dict_index[i][8].split('.')
                    
                    if (format_string_to_be_repeated in struc_contains and shadow_dict_index[i][2] == ''):
                        format_of_string = shadow_dict_index[i][5] #Extracting thr format 
                        struct_format.append(format_of_string)
                        label_string = shadow_dict_index[i][8].split('.')
                        label_format.append(label_string[-1:])
                    elif (shadow_dict_index[i][2] != '' and format_string_to_be_repeated in struc_contains):
    
                        label_format, struct_format,i = self.recursive_struct(i, shadow_dict_index, data,struct_format, label_format, dynamic_content_format)
                        break
                        
                    else:
                        # (format_string_to_be_repeated not in struc_contains)
                        # format_of_string = shadow_dict_index[i][5] #Extracting thr format 
                        # struct_format.append(format_of_string)
                        # label_string = shadow_dict_index[i][8].split('.')
                        # label_format.append(label_string[-1:])
                        break
                    
                    i=i+1
                
        return label_format, struct_format, i
    
    
    def startReceiving(self):
        while True:
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
                    print("Raw hex data",hex_list)
                    hex_string = ' '.join(hex_list)
                    print('hex_string:', hex_string)
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
                
                header_format_rcv = config.header_formats[0]
                header_format_list = []  

                try:    
                    with open(header_file_path,'r',encoding="utf-8") as file:
                        print(file)
                        for val in file:
                            header_format_list.append(val[:-1])
                except Exception as e:
                    print("Error Occured while reading header_file_path")
                    
                print("header_format_list = []  ",header_format_list)
                
                header_format = ' '.join(map(str,header_format_list[:]))
                header_length = struct.calcsize(f'={header_format}')
                print("Header format",header_format,header_length)
                header_tuple = struct.unpack(f'={header_format}',data[0:header_length])
                hdrList = self.getMsgListFromMsgTuple(header_tuple)
                print("--------------------HeaderList------------------", hdrList)
                

                    
                src_id = hdrList[config.src_id_index]
                dest_id = hdrList[config.dest_id_index]
                msg_id = hdrList[config.message_id_index]
                
                msg_flag = True
                
                for key ,value in config.dictionary_msg.items():
                    if str(value[0]) == 'nan' or str(value[1]) == 'nan' or str(value[0] == str(value[1])):
                        msg_flag = False
                    break;
                if msg_flag == True:
                    print("Getting msg name through src id , dest id")
                    msg_name = config.get_message_name(msg_id,src_id,dest_id)
                else:
                    print("Getting by msg name by ID")
                    msg_name = config.get_message_name_by_msgID(msg_id)
                    
                # print("--------------------------------------------- ")   
                # print("msg_name  ",msg_name)
                # print("src_id  ",src_id)
                # print("msg_id ",data[5])
                
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
        
            
                # print("RCV SRC_ID:",src_id, ",RCV MSG ID:",msg_id, ",RCV MSG LEN:",rcv_msg_len)
                #     content_format_list = config.modified_content_dictionary[msg_name]
                #     print(content_format_list)
                #     content_format_string = ' '.join(map(str,content_format_list))
                #     content_format_list_len = struct.calcsize(f'={content_format_string}') #getting the content length
                #     shud_be_msg_len = header_length_rcv + content_format_list_len
                #     print('content_lenght and header_lenght------------', content_format_list_len, header_length_rcv)
                #     print("shud_be_msg_len:",shud_be_msg_len,  ",RCV MSG LEN:",rcv_msg_len)
                #     if rcv_msg_len != shud_be_msg_len:
                #         observation_string = 'MSG LEN Failed'
                    
                # datetime_now = datetime.datetime.now()
                # # datetime_str = datetime_now.strftime("%Y.%m.%d %H:%M:%S")
                # datetime_str = datetime_now.strftime('%F %T.%f')[:-3]

                
                # # Function to UPDATE ALL SAMPLES HEX
                # config.update_table_entry(datetime_str, msg_name, hex_string, observation_string)
                
                
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
                dynamic_label_list = []
                complete_tuple = {}
                try:
                    if(msg_name != 'UNKNOWN'):#and observation_string != 'MSG LEN Failed'):
                        content_format_list = config.content_dictionary[msg_name]                       
                        header_format = ' '.join(map(str,header_format_list[:]))
                        header_length = struct.calcsize(f'={header_format}')
                        print("Header format",header_format,header_length)
                        try:
                            header_tuple = struct.unpack(f'={header_format}',data[0:header_length])
                        except Exception as e:
                            print("Header Unpack error: ",e)
                        hdrList = self.getMsgListFromMsgTuple(header_tuple)
                        header_str = ' '.join(map(str,hdrList))
                        config.dynamic_header_format.clear()
                        config.dynamic_header_format.append(header_str)
                        msg_content = dict[f'{msg_name}']
                        # print("MSG CONTENT",msg_content)
                        
                        
                        # print("data",header_str)
                        # print("no of dest nodes",header_tuple[9])
                        
                        # no_of_dest_nodes = header_tuple[9]
                        dynamic_content_format = content_format_list.copy()
                        
                        dict_index = dict[f'{msg_name}'].copy()
                        # print("LEN of Dict Index",len(dict_index))
                        
                        no_of_repeatitions =1
                        
                        dynamic_label_list = config.labels_list_dictionary[msg_name].copy()
                        # print("Labels--------------->",dynamic_label_list)
                        
                        shadow_dict_index = dict_index.copy()
                        shadow_content_str = ''
                        try:
                            struct_format = []
                            label_format = []
                            index_after_recursion = -1
                            for i,x in enumerate(shadow_dict_index):
                                
                                if i <= index_after_recursion-1:
                                    #if(shadow_dict_index[i][2] != ''):
                                    # print("7878787887=======",i)
                                    continue
                                else:
                                    
                                    print("not recursion=======",i, shadow_dict_index[i][5])
                                    # print(">>>>>>>>>>>>>",len(shadow_dict_index),i,shadow_dict_index[i]
                                    # print("Inside exact index  data")
                                    #print("current -Index========", i)
                                    format_of_string = shadow_dict_index[i][5]
                                    
                                    label_string = shadow_dict_index[i][8].split('.')


                                    # print("current format of string------", label_string, format_of_string)
                                    
                                    struct_format.append(format_of_string)
                                    label_format.append(label_string[-1:])
                                    current_static_format = dynamic_content_format[:i]   
                                    # (B)   
                                
                                    current_data_format = ' '.join(map(str,struct_format[:]))
                                    print("jsiofofjjd-----", current_data_format)
                                    try:
                                        fmt_length = struct.calcsize(f'={current_data_format}')
                                        fmt_tuple = struct.unpack(f'={current_data_format}',data[0:fmt_length])
                                    except Exception as e:
                                        # print(fmt_tuple)
                                        print("==============",e)
                                        # self.show_error_message(str(e))
                                        # print(fmt_tuple)
                                        
                                    
                                    #print("*******************************", label_string[-1:])
                                    # temp_list = self.getMsgListFromMsgTuple(fmt_tuple)
                                    # # print('content_list -> ',temp_list)
                                    # completeList = self.getStringifiedMsgList( temp_list )
                                    # shadow_content_str = ' '.join(map(str,completeList[:]))
                                    # observation_string = 'kldasldkj'
                                    # config.update_table_entry(datetime_str, msg_name,hex_string, content_str,dynamic_label_list, observation_string)
                                    
                                    if(shadow_dict_index[i][2] != ''):
  
                                        format_string_to_be_repeated = shadow_dict_index[i][2]  
                                        pos_of_repeat_structure = i+1
                                        
                                        current_static_format = dynamic_content_format[:pos_of_repeat_structure]
                                        
                                        current_data_format = ' '.join(map(str,struct_format[:]))
                                        fmt_length = struct.calcsize(f'={current_data_format}')
                                        try:
                                            fmt_tuple = struct.unpack(f'={current_data_format}',data[:fmt_length]) 
                                        except Exception as e:
                                            print(e)
                                            # self.show_error_message(str(e))
                                        no_of_repeatitions = fmt_tuple[-1]
                                        #print("88888888888888888888-----", fmt_tuple)
                                        #print("current_data_format=====", struct_format)
                                        print("no_of_repeatitions outside recursion",no_of_repeatitions, pos_of_repeat_structure, format_string_to_be_repeated)
                                        # print("shadow_dict_index",shadow_dict_index[pos_of_repeat_structure][5],"--",shadow_dict_index[pos_of_repeat_structure][8])
                                        # print("format_string_to_be_repeated",format_string_to_be_repeated)
                                        # format_of_structure = []
                                        # label_of_structure = []
                                        
                                        
                                        print("*************************+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                                        struct_format.pop(-1)
                                        label_format.pop(-1)  
                                        try:
                                            label_format, struct_format, index_after_recursion = self.recursive_struct(i, shadow_dict_index, data, struct_format, label_format, dynamic_content_format)
                                        except Exception as e:
                                            print("Recursion error",e)
                                            
                                        # print("Recursion output",struct_format, index_after_recursion)
    
                                        print("*************************+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                                print("final content_format", struct_format)
                        except Exception as e:
                            config.update_table_entry(datetime_str, msg_name,complete_tuple, content_str,dynamic_label_list, observation_string,content_format,hex_string,data)
                            # self.show_error_message(str(e))
                        config.dynamic_label_lsit = label_format.copy()
                        
                        content_format_list = struct_format

                        content_format = ' '.join(map(str,content_format_list[:])) 
                        # config.final_format = content_format
                        
                        fmt_length = struct.calcsize(f'={content_format}')
            
                        bits_format = config.bits_dictionary[msg_name]
                        if bits_format == 'bytes':
                            # print("jskskhjkdkdkj")
                            complete_tuple = []
                            try:
                                print("final content format", content_format,len(dynamic_content_format))
                                complete_tuple = struct.unpack(f'={content_format}',data)
                                print("complete_tuple",complete_tuple)
                                # config.complete_data = complete_tuple
                                print("config.complete_data",config.complete_data)
                                observation_string = "RCVD OK"
                            except Exception as e:
                                print("UNPACK ERROR",e,content_format,complete_tuple)
                                datetime_now = datetime.datetime.now()
                                datetime_str = datetime_now.strftime('%F %T.%f')[:-3]
                                observation_string = 'ERROR'
                            temp_list = self.getMsgListFromMsgTuple(complete_tuple)
                            # print('content_list -> ',temp_list)
                            completeList = self.getStringifiedMsgList( temp_list )
                            content_str = ' '.join(map(str,completeList[:]))

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
                            
                            
                            # content_format_list = config.modified_content_dictionary[msg_name]
                            # print("-------Final Dynamic------",dynamic_content_format)
                            content_format_string = ' '.join(map(str,dynamic_content_format))
                            content_format_list_len = struct.calcsize(f'={content_format_string}') #getting the content length
                            
                            
                            shud_be_msg_len = content_format_list_len
                            rcv_msg_len = data[6] #6th index is MSG LEN
                            
                            # print('content_lenght and header_lenght------------', content_format_list_len)
                            # print("shud_be_msg_len:",shud_be_msg_len,  ",RCV MSG LEN:",rcv_msg_len)
                            # if rcv_msg_len != shud_be_msg_len:
                            #     observation_string = 'MSG LEN Failed'
                    
                            datetime_now = datetime.datetime.now()
                            # datetime_str = datetime_now.strftime("%Y.%m.%d %H:%M:%S")
                            datetime_str = datetime_now.strftime('%F %T.%f')[:-3]

                            
                            # Function to UPDATE ALL SAMPLES HEX
                            
                            print("***********************FINAL CONTENT FORMAT***************************************",content_format_string,content_format_list_len)
                            # print("CONTENT",content_str)
                            config.update_table_entry(datetime_str, msg_name, complete_tuple,content_str,label_format, observation_string,content_format,hex_string,data)
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
                        print('MSG NOT Identifiable...')
                        header_format = config.header_formats[0]
                        
                        observation_string = 'MSG LENGTH MISMATCH OR UNKNOWN'
                        
                        
                        
                        # header_format_list = ['H','B','B','B' ,'I', 'H', 'B', 'H', 'H', 'B'] #ASM project specific
                        # header_format_list = ['H','H','B','H' ,'H', 'H', 'B', 'B'] 
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
