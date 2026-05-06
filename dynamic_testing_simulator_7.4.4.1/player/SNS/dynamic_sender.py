            #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  6 14:25:37 2025

@author: saritajangra@Indigenous.com
"""

from Configuration import config
import datetime
import math, csv
import crc_calulator
import struct
#from mainwindow import Ui_MainWindow, getStringifiedMsgList
from udpsender import UdpSender
import threading
import time
import re
from SNS.test_data_for_dynamic_testing import data_extraction, output_extraction
import socket
import ast
from PyQt5.QtCore import pyqtSignal, QObject, QEventLoop, QCoreApplication

from SNS.screenshot_Operations import compare_images
from csv_dict import csv_dict
import pandas as pd
import inspect
result = "RESULTS"
#from saveSendPeriodic import 
class Dynamic_Sender(QObject):
    gui_check_signal = pyqtSignal(str)
    gui_check_response_signal = pyqtSignal(int)
    test_result_signal =pyqtSignal(str, str, str, object, object)
    error_signal = pyqtSignal(str)
    stop_sending_signal = pyqtSignal()
    # start_sending_Functions_signal = pyqtSignal(str, object)
    # start_sending_testCase_signal = pyqtSignal(str, object, str)

    def __init__(self):
        super().__init__()
        #self.mainwindow = Ui_MainWindow()
        #self.gui_signal_recieve.connect()
        self.stop_signal = False
        self.sender = UdpSender()
        self.previous_received_message = "NULL"
        self.gui_check_response_signal.connect(self.gui_response)
        self.gui_check_response_signal_value = -1
        self.stop_sending_signal.connect(self.receivedSignal)
        self.process_running = 0
        
        # self.start_sending_Functions_signal.connect(self.send_test_suite)
        # self.start_sending_testCase_signal.connect(self.send_test_case)
        
    def receivedSignal(self):
        print("stop received")
        if self.process_running:
            self.stop_signal = True
        
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

                
    def send_test_suite(self, projectName, test_suite_names):        

        dictionary_data = data_extraction(projectName)
        self.process_running = 1
        for test_suite_name in test_suite_names:

            if test_suite_name in dictionary_data:
                test_cases_name = []
                print(test_suite_name)
                
                #make a list containing all test cases of the given test suite
                for key, value in dictionary_data[test_suite_name].items():
                    if key:
                        test_cases_name.append(key)
                print(test_cases_name)
                self.send_test_case(projectName, test_cases_name, test_suite_name)
                if self.stop_signal == True:
                    self.stop_signal = False
                    self.process_running = 0
                    return

                    
            else:
                print("test suite data not found")
            print(f"\n***Test suite = '{test_suite_name}' completed***")
        self.process_running = 0

            

                       
    def send_test_case(self, projectName, test_case_names, test_suite_name, recursive=False):        
        stack = inspect.stack()

        #extract test suite data
        dictionary_data = data_extraction(projectName)
        result_dictionary = {}
        

        if test_suite_name in dictionary_data:
            
            #extract test case data
            test_case_dictionary = dictionary_data[test_suite_name]
            
            print("\n************!!!!!!!!!!!***********")
           
            if len(stack) == 1:
                self.process_running = 1
            for test_case_name in test_case_names:
                
                #extract input messages and precondition of test case
                input_messages = test_case_dictionary[test_case_name]
                preconditions = input_messages[0]
                input_messages = input_messages[1:]

                preconditions_result = {}
                #Run preconditions---preconditions dictionary of test suite--> test case list generation              
                if  preconditions != 'nan':
                    preconditions = preconditions.strip('[]').replace("'", "").split(',')
                    preconditions_dict = {}
                    for i in preconditions:
                        i = i.strip(" ")
                        pred_list = i.split(" --> ")
                        if pred_list[0] in preconditions_dict:
                            preconditions_dict[pred_list[0]].append(pred_list[1])
                        else:
                            preconditions_dict[pred_list[0]] = []
                            preconditions_dict[pred_list[0]].append(pred_list[1])
                    #print(preconditions_dict)
                    for key, value in preconditions_dict.items():
                        preconditions_result = self.send_test_case(projectName, value, key, recursive=True)
                        #print("lslkkd",preconditions_result)
                        if isinstance(preconditions_result, dict):
                            if 'Fail' in preconditions_result.values() and recursive == True:
                                return preconditions_result
                        else:
                            return
                        #preconditions_result = self.send_test_case(projectName, value, key)
                        # if isinstance(preconditions_result, dict):
                        #     print(preconditions_result)
                        # else:
                        #     break
                
                #extract expected output messages
                output_data = output_extraction(projectName, test_suite_name, test_case_name)
                #convert expected output format
                output_data_generated = []
                dynamic_static_output_data = []
                for key, value in output_data:
                    temp_value = []
                    for ind in value[0]:
                        if ind.isdigit():
                            temp_value.append(int(ind))
                        else:
                            temp_value.append(ind)
                    output_format = list(value[2].replace(" ", ""))
                    temp_output_data, output_format = self.dynamic_message_generator(key, temp_value, output_format)
                    dynamic_static_output_data.append((key,[temp_output_data, int(value[1])]))
                    output_data_generated.append((key, temp_output_data, int(value[1])))         
                #if preconditions failed, print result
                recieved_output_list = []
                for test_name, test_name_result in preconditions_result.items():
                    if test_name_result == 'Fail':
                        recieved_output_list.append((f"Precondition {test_name} failed"))
                        self.test_result_signal.emit(test_suite_name, test_case_name, 'Fail', recieved_output_list, output_data_generated)
                        return
                
                
                # status of each output message recieved correctly or not(1-recieved correcly,0-not recieved or recieved wrong)
                all_unicast_output_messages = []
                unicast_reciever_status = []
                all_multicast_output_messages = []
                multicast_reciever_status = []
                for key, value in output_data:
                    if key and 'NO OUTPUT REQUIRED' not in key:
                        if 'GUI_CHECK' in key or config.comm_types_dictionary[key] == 'U':
                            unicast_reciever_status.append(0)
                            all_unicast_output_messages.append(key)
                        else:
                            all_multicast_output_messages.append(key)
                            multicast_reciever_status.append(0)
                            
                    
                    
                
                if test_case_name in test_case_dictionary:
                    threads = []
                 
                    stop_event = threading.Event()
                    stop_flags_for_periodic_messages = []
                    
                    periodic_messages_list = []

                    
                    # start unicast reciever thread                    
                    unicast_reciever_thread = threading.Thread(target=self.dynamic_reciever, args=(int(config.sock_rcv_port), stop_event, dynamic_static_output_data, all_unicast_output_messages, unicast_reciever_status, recieved_output_list))
                    unicast_reciever_thread.start()
                    threads.append(unicast_reciever_thread)
                    
                    #start multicast reciever thread
                    multicast_reciever_thread = threading.Thread(target=self.dynamic_reciever, args=(int(config.sock_multicast_rcv_port), stop_event, dynamic_static_output_data, all_multicast_output_messages, multicast_reciever_status, recieved_output_list))
                    multicast_reciever_thread.start()
                    threads.append(multicast_reciever_thread)
                    
                    print(f"\nSending Test Suite = '{test_suite_name}'")
                    print(f"\nTest Case = '{test_case_name}'\n")
                    #print(input_messages)
                    

                    
                    #content data generation when whole bits of an indication message is to be sent
                    if 'SEND_EACH_BITS' in test_case_name:
                        self.send_each_bits(input_messages, projectName, test_suite_name, test_case_name)
                
                    else:
                        for j in input_messages:
                            message_name = j[0]
                            header_data = j[1]
                            message_data = j[2]
                            periodicity = int(j[3])
                            delay = int(j[4])
                            
                            message_format = j[5]
                            
                            
                            message_format = list(message_format.replace(" ", ""))
                            message_data, message_format = self.dynamic_message_generator(message_name, message_data, message_format)
                            message_format = " ".join(map(str, message_format))
                            
                            if message_name and 'INPUT NOT REQUIRED' not in message_name:
                                header_format = config.header_dictionary[message_name]
                                num_elements_header = len(header_format.replace(' ',''))
                                if 'GUI_INPUT' in message_name:
                                    self.gui_check_signal.emit(message_name)
                                    while True:
                                        if self.gui_check_response_signal_value>=0:
                                            self.gui_check_response_signal_value = -1
                                            break
                                else:
                                    #handles periodic messages sender
                                    if periodicity != 0:
                                        stop_event_for_periodic = threading.Event()
                                        stop_flags_for_periodic_messages.append(stop_event_for_periodic)
                                        if message_name not in periodic_messages_list:
                                            periodic_messages_list.append(message_name)
                                            t = threading.Thread(target=self.periodic_message_sender, args=(periodicity, stop_event_for_periodic, message_name, message_data[:num_elements_header], message_data[num_elements_header:], message_format))
                                            t.start()
                                            threads.append(t)
                                        else:
                                            #when same periodic message with different data input is required
                                            index = periodic_messages_list.index(message_name)
                                            stop_flags_for_periodic_messages[index].set()
                                            stop_flags_for_periodic_messages.pop(index)
                                            periodic_messages_list.pop(index)
                                            periodic_messages_list.append(message_name)
                                            t = threading.Thread(target=self.periodic_message_sender, args=(periodicity, stop_event_for_periodic, message_name, message_data[:num_elements_header], message_data[num_elements_header:], message_format))
                                            t.start()
                                            threads.append(t)
                                    else:
                                        self.message_sender(message_name, message_data[:num_elements_header], message_data[num_elements_header:], message_format)

                            time.sleep(delay/1000)
                            

                        
                        
                        #sending signal when GUI check ouput is required and waiting for signal from GUI
                        for i in range(len(all_unicast_output_messages)):
                            if 'GUI_CHECK:' in all_unicast_output_messages[i]:
                                self.gui_check_signal.emit(all_unicast_output_messages[i])
                                #time.sleep(delay/1000)
                                while True:
                                    if self.gui_check_response_signal_value>=0:
                                        # reciever_status[msg] = 1
                                        # self.gui_check_response_signal_value = 0
                                        break
                                if self.gui_check_response_signal_value == 2:
                                      unicast_reciever_status[i] = 0
                                      recieved_output_list.append((all_unicast_output_messages[i], "No input from user"))
                                      self.gui_check_response_signal_value = -1
                                elif self.gui_check_response_signal_value == 1:
                                    unicast_reciever_status[i] = 1
                                    recieved_output_list.append((all_unicast_output_messages[i], "Expected result seen in GUI"))
                                    self.gui_check_response_signal_value = -1
                                else:
                                    unicast_reciever_status[i] = 0
                                    recieved_output_list((all_unicast_output_messages[i], "Expected result not seen in GUI"))
                                    self.gui_check_response_signal_value = -1
                                    
                            if "IMAGE_PATH:" in all_unicast_output_messages[i]:
                                expected_image = all_unicast_output_messages[i].split("IMAGE_PATH:")[1]
                                current_image = "/home/kuldeepsingh@Indigenous.com/Documents/ATC_TESTING/DYANAMIC_SIMULATOR/dynamic_testing_simulator_1.9.4/player/SAVEANDSEND/Screenshots_tp1/Captured_Screenshot/"+all_unicast_output_messages[i].split("/")[-1]
                                # print(expected_image, current_image)
                                score, result_gui = compare_images(expected_image, current_image)
                                if result_gui.lower() ==  "pass":
                                    unicast_reciever_status[i] = 1
                                    recieved_output_list.append((all_unicast_output_messages[i], f"Image matched, score{score}"))
                                elif result_gui.lower() == "fail":
                                    unicast_reciever_status[i] = 0
                                    recieved_output_list((all_unicast_output_messages[i], f"Image not matched, score{score}"))
                                else:
                                    print("ERROR in comparing images")
                                    recieved_output_list((all_unicast_output_messages[i], "ERROR IN IMAGE COMPARISION"))
                                
                                print(score, result_gui)
    
                        stop_event.set()
                        for i in stop_flags_for_periodic_messages:
                            i.set() 
                        
                        for i in threads:
                            i.join()
    
                            
                        print(f"\nTest case = '{test_case_name}' completed\n")
                        
                        reciever_status = unicast_reciever_status + multicast_reciever_status
                        #checking recieved status of all output messages
                        print("Reciever Status = ", reciever_status)
                        status = "Pass" if all(x == 1 for x in reciever_status) else "Fail"
                        print(f"\nTest Case = {test_case_name}, status = {status}")
                        
                        result_dictionary[f'{test_suite_name}-->{test_case_name}'] = status
                            
                        if recursive == False:
                            final_result = [test_suite_name, test_case_name, status, recieved_output_list, output_data_generated]
                            self.test_result_signal.emit(test_suite_name, test_case_name, status, recieved_output_list, output_data_generated)
                            #print("mahiyo emitted result signal")
                            with open(f"{result}/{projectName}_result.csv", "a") as file:
                                writer = csv.writer(file)
                                writer.writerow(final_result)
                        


                                
                        print("\n************!!!!!!!!!!!***********")
                    if self.stop_signal == True:
                        if len(stack) == 1:
                            self.stop_signal = False
                            self.process_running = 0
                            return
                        else:
                            return
                    
                else:
                    print(f"test case {test_case_name} data not found")
                    self.error_signal.emit(f"test case {test_case_name} data not found")
            if len(stack) == 1:
                self.process_running = 0
                
                
                 

        else:
            print(f"test suite {test_suite_name} data not found")
            self.error_signal.emit(f"test suite {test_suite_name} data not found")
            return
        
        return result_dictionary
        
        
   




         
    def send_each_bits(self, input_messages, projectName, test_suite_name, test_case_name):

        reciever_status = {}
        recieved_output_list = {}
        for j in input_messages[1]:
            message_name = j[0]
            if message_name in config.bits_dictionary:
                if message_name and 'INPUT NOT REQUIRED' not in message_name:
                    if 'GUI_INPUT' in message_name:
                        print("wrong message type for given test case")
                    else:
                        
                        header_data = j[1]
                        indication_bits = []
                        indication_bits_description = []
                        bits_name = config.bits_dictionary[message_name]
                        if bits_name == "mt_indication_bits":
                            indication_bits = config.mt_indication_bit_names.copy()
                            indication_bits_description = config.mt_indication_bit_description.copy()

                        
                        if bits_name == "cbi_ratc_indication_bits":
                            indication_bits = config.read_cbi_ratc_indication_bit_names.copy()
                            indication_bits_description = config.cbi_ratc_indication_bit_description.copy()
                        
                        if bits_name == "ratc_cbi_indication_bits":
                            indication_bits = config.read_ratc_cbi_indication_bit_names.copy()
                            indication_bits_description = config.ratc_cbi_indication_bit_description.copy()
                        if bits_name == "control_bits":
                            indication_bits = config.control_bit_names.copy()
                            indication_bits_description = config.control_bit_description.copy()
                        if bits_name == "indication_bits":
                            indication_bits = config.indication_bit_names.copy()
                            indication_bits_description = config.indication_bit_description.copy()
                            
                        if bits_name == "alarm_bits":
                            indication_bits = config.alarm_bit_names.copy()
                            indication_bits_description = config.alarm_bit_description.copy()
                    
                        
                        message_data = j[2]
                        message_data = [0 for i in message_data]
                        message_data.pop(0)
                        records = []
                        byteCount = 0
                        bitCount = 0
                        max_no_of_records = 0
                        periodicity = int(j[3])
                        delay = int(j[4])
    
                        
                        
                        for i in range(len(indication_bits)):
                            recieved_output_list = {}
                            reciever_status = {}
                            records = message_data.copy()
                            #maxByteCount = byteCount
                            
                            records[byteCount] = 1 << bitCount
            
            
                                
                            bitCount = bitCount + 1
                            max_no_of_records = byteCount +1
                            if (bitCount == 8):
                                byteCount = byteCount + 1
                                bitCount = 0
                            
                            message_data_final = [max_no_of_records]
                            message_data_final = message_data_final + records
                            threads = []
                            stop_event = threading.Event()
                            if periodicity != 0:
                                t = threading.Thread(target=self.periodic_message_sender, args=(periodicity, stop_event, message_name, header_data, message_data_final))
                                t.start()
                                threads.append(t)
    
                            else:
                                self.message_sender(message_name, header_data, message_data_final)
                             
                             

                            
                                
                            
                            #sending signal for every message sent
                            self.gui_check_signal.emit(f"Is bit '{indication_bits[i]}:{indication_bits_description[i]}' displayed in GUI?")
                            while True:
                                if self.gui_check_response_signal_value>=0:
                                    # reciever_status[msg] = 1
                                    # self.gui_check_response_signal_value = 0
                                    break
                            if self.gui_check_response_signal_value == 2:
                                  reciever_status[indication_bits[i]] = 0
                                  recieved_output_list[indication_bits[i]] = "No input from user"
                                  self.gui_check_response_signal_value = -1
                            elif self.gui_check_response_signal_value == 1:
                                reciever_status[indication_bits[i]] = 1
                                recieved_output_list[indication_bits[i]] = "Expected result seen in GUI"
                                self.gui_check_response_signal_value = -1
                            else:
                                reciever_status[indication_bits[i]] = 0
                                recieved_output_list[indication_bits[i]] = "Expected result not seen in GUI"
                                self.gui_check_response_signal_value = -1
                                
                            #checking recieved status of GUI check
                            print("Reciever Status = ", reciever_status)
                            status = "Pass" if all(reciever_status.values()) else "Fail"
    
                            
                            
                            #sending result for display and saving
                            output_data = f"CHECK_GUI:Is bit '{indication_bits[i]}:{indication_bits_description[i]}' displayed in GUI?"
                            #write results to a csv file
                            final_result = [test_suite_name, test_case_name, status, recieved_output_list, output_data]
                            self.test_result_signal.emit(test_suite_name, test_case_name, status, recieved_output_list, output_data)
                            #print("mahiyo emitted result signal")
                            with open(f"{result}/{projectName}_result.csv", "a") as file:
                                writer = csv.writer(file)
                                writer.writerow(final_result)
                            
                            print("\n************!!!!!!!!!!!***********")
                                
                                
                            time.sleep(delay/1000)
                            stop_event.set()
                            for i in threads:
                                i.join()
                                
                            
                            if self.stop_signal == True:
                                return

    
                            
                            
    
                else:
                        print("wrong message type for given test case")
            else:
                self.error_signal.emit("Input message not present")
                print("Input message not present")
                return
    
            
            
            
            
            
            

    
    def set_bit(self, v, index, x):
        #debuggerInstance.printWhere()
        mask = 1 << index
        v &= ~mask
        if x:
            v |= mask
        return 



    def periodic_message_sender(self, interval, stop_event, message_name, header_data, message_data, message_format):
        
        while not stop_event.is_set():
            if message_name in config.header_dictionary:
                self.message_sender(message_name, header_data, message_data, message_format)
                time.sleep(interval/1000)
            else:
                self.error_signal.emit("Input message not present")
                print("Input message not present")
                return
        
        
        
    def message_sender(self, message_name, header_data, message_data, message_format):

        
        if message_name in config.header_dictionary:
            #self.set_IP_and_socket()
            header_data = [int(x) for x in header_data]
            header_format = config.header_dictionary[message_name]
            # content_format_list = config.modified_content_dictionary[message_name]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
            # content_format = ' '.join(map(str,content_format_list[:-1]))
            if(message_format == 'not' or message_format == ' '):
                message_format = ''
                
            crc_format = config.crc_dictionary[config.message_selected]
            if(crc_format == 'not'  or crc_format == ' '):
                crc_format = ''
            #print('header_format:', header_format, ', content_format:', content_format, ', crc_format:',crc_format)    
            bits_format = config.bits_dictionary[message_name]
            header_list = []
            content_list = []
            crc_data = 0
            
            
            if bits_format == 'cbi_ratc_indication_bits' or bits_format == 'ratc_cbi_indication_bits' or bits_format == 'control_bits' or bits_format == 'indication_bits' or bits_format == 'alarm_bits' or bits_format == "event_bits" or bits_format == 'mt_indication_bits':
                
                header_list = header_list + self.get_header_list(header_data)
                content_list = [int(i) for i in message_data]
                crcPack = struct.pack(f'={message_format}', *tuple(header_list), *tuple(content_list[:-1])) #for CRC on header
                #crcPack = struct.pack(f'= {content_format}', *tuple(content_list))
                crc_data = crc_calulator.crc_32(crcPack)
                content_list[-1] = crc_data
                print(message_name)
                print(content_list)
                self.send_and_log_message_and_update_gui(message_name, message_format, header_list, content_list)
                
            if bits_format == 'bytes':
                
    
                #temp_hdr_list = self.get_header_list(header_data)
       
                
                header_list = header_list + header_data
    
                value_list = []
                format_list = message_format.split(" ")
                format_list = format_list[len(header_data):]
                # for i in range(len(message_data)):
                #     if 's' in format_list[i]:
                #         #print(expected_content[i])
                #         message_data[i] = ast.literal_eval(message_data[i]).decode("utf-8")
    

                for i in range(len(message_data)):
                    value = message_data[i]
                    if 's' in format_list[i]:
                        value = bytes(value, 'utf-8')
                    elif value == '' or value == ' ':
                        # print('empty value')
                        value = 0
                    elif str(value).strip() == 'auto':
                        value = 'auto'    
                    else: 
                        value = int(value)    
                    value_list.append( value )

                crcPack = struct.pack(f'={message_format}', *tuple(header_list), *tuple(value_list)) # for CRC on header
            
                crc_data = crc_calulator.crc_32(crcPack)
                # crc_data = 1;#sarita code for sending wrong CRC
                #value_list[-1] = crc_data
                # else:
                #     content_list.append(modified_value_list[-1])
    
                print(message_name)
                print(header_list)
    
                self.send_and_log_message_and_update_gui(message_name, message_format, header_list, value_list)
        else:
            self.error_signal.emit("Input message not present")
            print("Input message not present")
            return
            

    
    
    def get_header_list(self, header_data):
        header_list = [int(i) for i in header_data]
        datetime_now = datetime.datetime.now()
        unique_message_code = 1

        header_list.append(datetime_now.day)
        header_list.append(datetime_now.month)

        header_list.append(datetime_now.year)
        header_list.append(datetime_now.hour)
        header_list.append(datetime_now.minute)
        header_list.append(datetime_now.second)
        header_list.append(math.floor(datetime_now.microsecond / 1000))
        header_list.append(unique_message_code)
        
        return header_list
    
    def send_and_log_message_and_update_gui(self, message_name, form, header_list, content_list):
        # print(form)
        # print("----", header_list)
        # print("-------", content_list)
        packet = struct.pack(f'={form}',*tuple(header_list), *tuple(content_list))
        self.sender.send_packet(packet)
    

        return
    
    def calculateByte(self,non_standard_bits_values, non_standard_bits_sizes):

        if sum(non_standard_bits_sizes) != 8:
            raise ValueError('Total bit size must be 8')
        packed_byte = 0
        current_bit_index = 8
        
        for number, size in zip(reversed(non_standard_bits_values), reversed(non_standard_bits_sizes)):
            if number >= (1 << size):
                raise ValueError(f'Number {number} exceeds maximum value for bit size {size}')
            current_bit_index -= size
            packed_byte |= (number << current_bit_index)
        return packed_byte
    
    
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
    
    def dynamic_reciever(self, port, stop_event, output_data, all_output_messages, reciever_status, recieved_output_list):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(1)
        sock.bind(('',  port))
        
        #data structure to store message recieved interval for periodic messages
        periodic_interval = {}
        output_messages = []
        temp_periodic_message_content = {}
        for key, value in output_data:
            if key in all_output_messages:
                if value[1]:
                    periodic_interval[key] = []
                else:
                    output_messages.append(key)
        
        sequence_of_message_recieved = 0
        #self.gui_check_signal.emit(output_messages[sequence_of_message_recieved])
        
        #gui_check_threads = []
        
        while not stop_event.is_set():
            error_flag = 0
            #print("9890",sequence_of_message_recieved)
            if sequence_of_message_recieved <= len(all_output_messages)-1:
                if 'GUI_CHECK:' in all_output_messages[sequence_of_message_recieved]:
                    
                    sequence_of_message_recieved = sequence_of_message_recieved+1                     
            try:               
                print(f"listening on port{config.sock_rcv_port}")
                data, address = sock.recvfrom(2000)  # Adjust the buffer size as needed

                hex_list = [format(val, '02x') for val in data]
                #print("Raw hex data",hex_list)
                hex_string = ' '.join(hex_list)

                observation_string = ''

                # if not crc_calulator.is_crc_ok(data):
                #     observation_string = 'CRC Failed'
                    
                
                # self.check_crc(hex_string)
                #config.log(f'{hex_string}')  
            except socket.timeout:
                config.isReceiving=False
                config.selected_message_status_on_receiver=0
                # print("Timed Out")
                continue
            
            header_format_rcv = config.header_formats[0]
            header_length_rcv = struct.calcsize(f'={header_format_rcv}') #getting the header length
            try:
                # if internal header
                header_tuple_rcv = struct.unpack(f'={header_format_rcv}',data[0:header_length_rcv]) #unpacking only header

            except (struct.error, ValueError):
                # if external header
                src_id = data[0]
                msg_id = data[2]
                msg_name = config.get_message_name_of_external(msg_id, src_id)
                header_format_rcv = 'B B'
                header_length_rcv = struct.calcsize(f'={header_format_rcv}') #getting the header length
                rcv_msg_len = len(data)
                
            else:
                src_id = data[config.src_id_index]
                dest_id = data[config.dest_id_index]
                msg_id = struct.unpack_from("H", data, 2)[0]
                #msg_name = config.get_message_name(msg_id, src_id, dest_id)

                
                
                
                hdrList = self.getMsgListFromMsgTuple(header_tuple_rcv)
                rcv_msg_len = hdrList[config.message_len_index]

            
            
                
            
            msg_name = ''
            for key, val in config.id_dictionary.items():
                if val == msg_id:
                    msg_name = key
                    
            # if(msg_name != config.message_selected):
            #     config.selected_message_status_on_receiver=0
    
        
            # if(msg_name != 'UNKNOWN'):
            #     content_format_list = config.modified_content_dictionary[msg_name]
            #     #print(content_format_list)
            #     content_format_string = ' '.join(map(str,content_format_list))
            #     content_format_list_len = struct.calcsize(f'={content_format_string}') #getting the content length
            #     shud_be_msg_len = header_length_rcv + content_format_list_len
            #     #print('content_lenght and header_lenght------------', content_format_list_len, header_length_rcv)
            #     #print("shud_be_msg_len:",shud_be_msg_len,  ",RCV MSG LEN:",rcv_msg_len)
            #     if rcv_msg_len != shud_be_msg_len:
            #         observation_string = 'MSG LEN Failed'
                
            datetime_now = datetime.datetime.now()
            # datetime_str = datetime_now.strftime("%Y.%m.%d %H:%M:%S")
            datetime_str = datetime_now.strftime('%F %T.%f')[:-3]

            
            print("--------------------------------------------- ")   
            print("msg_name  ",msg_name)
            print("src_id  ",src_id)
            print("msg_id ",msg_id)
            print("observation string ",observation_string)

            content_format= ''
            header_format= ''
            hdrList = []
            completeList = []
            content_sublist = []
            content_sublist_without_header = []
            content_str = ''
            header_str = ''
            header_dict = {}
            content_dict = {}
            
            
            #extract expected output data from file
            if msg_name == 'UNKNOWN':
                recieved_output_list.append(('UNKNOWN', 'Wrong message ID/source ID/destination ID'))
            elif msg_name in all_output_messages and observation_string == 'MSG LEN Failed':
                recieved_output_list.append((msg_name, 'Message lenght failed'))
            elif msg_name in all_output_messages and observation_string == 'CRC Failed':
                recieved_output_list.append((msg_name, 'CRC Failed'))
                
            # try:   
            if(msg_name != 'UNKNOWN' and observation_string != 'MSG LEN Failed' and observation_string != 'CRC Failed'):
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
                
                
                #********************************************\
                    
                # no_of_dest_nodes = header_tuple[9]
                dynamic_content_format = content_format_list.copy()
                
                
                #list that contain list of each message attributes(ARGUMENT_NAME	, ARGUMENT_TYPE, IRS_VALUE, BitField, INPUT_VALUE, FORMAT, ATR_ARRAY_SIZE, ARGUMENT_SIZE)
                dict_index = csv_dict[f'{msg_name}'].copy()
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
                                    print("incorrect data recieved")
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
                                        print("incorrect data recieved")
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
                                    
                                print("Recursion output",struct_format, index_after_recursion)
                                print("*************************+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                except Exception as e:
                    #config.update_table_entry(datetime_str, msg_name,complete_tuple, content_str,dynamic_label_list, observation_string,content_format,hex_string,data)
                    print(e)
                if error_flag == 0:
                    print('final struct format', struct_format)
                        
                    config.dynamic_label_lsit = label_format.copy()
                    
                    content_format_list = struct_format
             
    
                    content_format = ' '.join(map(str,content_format_list[:])) ###########
                    # config.final_format = content_format
                    print("---", content_format)
                    
                    fmt_length = struct.calcsize(f'={content_format}')
        
                    bits_format = config.bits_dictionary[msg_name]
                    # print("header-format", header_format)
                    # print("content-format", content_format)
                    ########**********************************                
                                                                              
                    if bits_format == 'bytes':
                        # print('    modified content_format list:',content_format)
                        
                        complete_tuple = struct.unpack(f'={content_format}',data)
                        temp_list = self.getMsgListFromMsgTuple(complete_tuple)
                        # print('content_list -> ',temp_list)
                        completeList = self.getStringifiedMsgList( temp_list )
                        content_str = ' '.join(map(str,completeList[num_elements_header:]))
                        content_sublist = completeList
                        content_sublist_without_header = completeList[num_elements_header:] 
                        
                        print("--", content_sublist_without_header)
                        print('bits_list', bits_list)
                        
                        bits_list = bits_list[len(header_format):]
                        print('bits_list', bits_list)
                        #print('bits_list',bits_list)
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
                        # print('Modified_value_list -> ',modified_value_list)
                        
                        
                        # if(msg_name == config.message_selected):
                        #     #Rigzin 24/12/2024 Adding new datatype to store the header_str and content_str as dictionary where key is message_name
                        #     if self.previous_received_message == msg_name:
                        #         config.selected_message_status_on_receiver = 1
                        #     self.previous_received_message = msg_name
                            
                        #     header_dict[msg_name] = header_str
                        #     content_dict[msg_name] = content_str
                        #     modified_value_dict[msg_name] = modified_value_list
                            #End
       
                    elif(bits_format == 'ratc_cbi_indication_bits' or bits_format == 'cbi_ratc_indication_bits' or bits_format == 'control_bits' or bits_format == 'indication_bits') :
                        #print("RATC_CBI_indication_bits")
                        header_length = struct.calcsize(f'={header_format}') #getting the header length
                        content_length = struct.calcsize(f'={content_format}') #getting the content length    
                        msg_len = header_length + content_length + 4  #4 is CRC length
                        #print('msg_len:',msg_len, ', header_format:',header_format, ', content_format:',content_format)
    
                        complete_tuple = struct.unpack(f'={header_format}{content_format}{crc_format}',data)
                        temp_list = self.getMsgListFromMsgTuple(complete_tuple)
                        #print('temp_list -> ',temp_list)
                        content_sublist = self.getStringifiedMsgList( temp_list )
                        content_str = ' '.join(map(str,completeList[num_elements_header:]))
                        content_sublist_temp = content_sublist[num_elements_header:]
                        records = completeList[num_elements_header + 1 : len(completeList)-1]
                        #print('records -> ',records)
                        bitPositionList = []
                        bitPositionList_dict = {}
                        for i,x in enumerate(records):
                            if records[i] != 0:
                                # print(records[i])
                                for j in range(7, -1, -1):
                                    bit = (records[i]>> j) & 1
                                    if bit == 1:
                                        bitPositionList.append(i*8+j)
                        #print('bitPositionList:',bitPositionList)
                        if(msg_name == config.message_selected):
                            #Rigzin 24/12/2024 Adding new datatype to store the header_str and content_str as dictionary where key is message_name
                            if self.previous_received_message == msg_name:
                                config.selected_message_status_on_receiver = 1    
                            self.previous_received_message = msg_name
                            
                            header_dict[msg_name] = header_str
                            content_dict[msg_name] = content_str
                            bitPositionList_dict[msg_name]= bitPositionList

                #comparison between recieved message and expected message

                if msg_name in all_output_messages:
                    
                    if error_flag == 1:
                        if msg_name in periodic_interval:
                            temp_periodic_message_content[msg_name] = (msg_name, "Invalid data/ invalid bit field recieved")
                        else:
                            recieved_output_list.append((msg_name, "Invalid data/ invalid bit field recieved"))
                    else:
                        if msg_name in periodic_interval:                            
                            periodic_interval[msg_name].append((math.floor(datetime_now.timestamp() * 1000)))
                            
                        for index in range(len(all_output_messages)):
                            if all_output_messages[index] == msg_name and reciever_status[index] == 0:
                                expected_content = output_data[index][1]
                                expected_content = expected_content[0][num_elements_header:]
                        # expected_content.pop()
                        # content_sublist.pop()
                                format_list = config.content_dictionary[msg_name]#expected_content = [int(i) if i.isdigit() else ast.literal_eval(i).decode("utf-8") if isinstance(i, str) else i for i in expected_content]
                                content_sublist_without_header = [x.lower() if isinstance(x, str) else x for x in content_sublist_without_header]
                                
                        
                        
                                for index_of_expected_content in range(len(expected_content)):
                                    #int(i) if i.isdigit() else ast.literal_eval(i).decode("utf-8") if isinstance(i, str) else i for i in expected_content
                                    if str(expected_content[index_of_expected_content]).isdigit:
                                        #print(expected_content[i])
                                        #expected_content[i] = ast.literal_eval(expected_content[i]).decode("utf-8")
                                        expected_content[index_of_expected_content] = int(expected_content[index_of_expected_content])
                                        
                                    else:
                                        expected_content[index_of_expected_content] = expected_content[index_of_expected_content].lower()
                                print('content_sublist',content_sublist_without_header)
                                print('expected_output',expected_content)
                                        
                            
                                
                                #setting if message recieved and content verified successfully for non-periodic messages
    
                                if sequence_of_message_recieved <= len(all_output_messages)-1:
                                    print("Output recieved---", msg_name)
                                    if msg_name != all_output_messages[sequence_of_message_recieved]:
                                        recieved_output_list.append((msg_name, "Expected message recieved in wrong sequence"))
                                        return
                                    if expected_content == content_sublist_without_header:
                                        reciever_status[index] = 1
                                        sequence_of_message_recieved = sequence_of_message_recieved+1
                                        recieved_output_list.append((msg_name, content_sublist,0))
                                        break
                                    else:
                                        if msg_name not in periodic_interval:
                                            recieved_output_list.append((msg_name, content_sublist,0))
                                            sequence_of_message_recieved = sequence_of_message_recieved+1
                                        else:
                                            temp_periodic_message_content[msg_name] = (msg_name, content_sublist,0)
                                        break
                                        
                error_flag == 0
                
        for key, value in temp_periodic_message_content.items():
            for i in range(len(all_output_messages)):
                if key == all_output_messages[i]:
                    if reciever_status[i] == 0:
                        recieved_output_list.append(value)

        print("-----", recieved_output_list)
        
        
        #checking whether interval for periodic message is recieved as per expected
        print(periodic_interval)
        for key, value in periodic_interval.items():

            
            for x in output_data:
                if x[0] == key:
                    periodicity = x[1][1]
                    print(periodicity)
                    tolerance = 200
                    index_of_current_msg = all_output_messages.index(key)
                    if len(value) == 1:
                        reciever_status[index_of_current_msg] = 0
                        recieved_output_list.append((key,'Message recieved is not periodic'))
                        break
                    else:
                        for i in range(len(value)-1):
                            expected_next_interval = ((value[i]+periodicity))
                            #print("----",expected_next_interval)
                            if value[i+1]<expected_next_interval-tolerance or value[i+1]>expected_next_interval+tolerance:
                                reciever_status[index_of_current_msg] = 0
                                for periodic_msg_index in range(len(recieved_output_list)):
                                    if key == output_data[periodic_msg_index][0]: 
                                        recieved_output_list[periodic_msg_index] = ((key, recieved_output_list[periodic_msg_index][1], value[i+1]-value[i]))
                                break
                            if i == len(value)-2:
                                for periodic_msg_index in range(len(recieved_output_list)):
                                    if key == output_data[periodic_msg_index][0]: 
                                        recieved_output_list[periodic_msg_index] = ((key, recieved_output_list[periodic_msg_index][1], value[i+1]-value[i]))
                        
                    print("******************")
                
    
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
                            print("==============",e)
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
                                print("==============",e)
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
    def gui_response(self,msg):
        self.gui_check_response_signal_value = msg
    
    def dynamic_message_generator(self, msg_name, message_data, message_format):
        dict_index = csv_dict[f'{msg_name}'].copy()
        shadow_dict_index = dict_index.copy()
        bits_list = config.bits_list_dictionary[msg_name]
        bits_list = [0 if i == 8 else i for i in bits_list]
        #print(bits_list)
        
        #represents how many times the corresponding struct will be repeated
        no_of_repeatitions =1
        
        # dynamic_label_list = config.labels_list_dictionary[msg_name].copy()
        # print("Labels--------------->",dynamic_label_list)
        
        
    
        shadow_content_str = ''
        
        
        #try:
        #store format of data till current attributes
        struct_format = []
        #store attribute names till current attribute
        label_format = []
        #represent the current index of iteration when recursion exits
        index_after_recursion = -1
        no_of_bits = 0
        index = 0
        
        #iterate through all attributes
        for i,x in enumerate(shadow_dict_index):            
            if i <= index_after_recursion-1:
                continue
            else:
                if index == len(message_data):
                    break
                # print("llllloolll--", i)
                # print("llllloolll--", index)
                
                #value of input                           
                data_value = message_data[index]
                
                #label name of current attribute
                format_of_message = message_format[index]
                #print(shadow_dict_index[i][8],data_value)                
                
                #===bits to byte conversion when bits list is non zero===
                #bits_list is zero
                if bits_list[i] == 0 and no_of_bits == 0:
                    struct_format.append(data_value)
                    label_format.append(format_of_message)                        
                    
                    no_of_repeatitions = data_value
                    index+=1
                    
                #when bits list architecture is wrong in the message    
                elif bits_list[i] == 0 and no_of_bits != 0:
                    print("Wrong bit field in message")
                    return
                
                #when bits list is non zero
                else:
                    no_of_bits+=bits_list[i]
                    if no_of_bits == 8:
                        struct_format.append(data_value)
                        label_format.append(format_of_message)
                        no_of_repeatitions = int(data_value)>>(8-bits_list[i])
                        no_of_bits = 0
                        index+=1
                
                
                
                #print(struct_format)
                #recursion starts when "ATR_ARRAY_SIZE" is not NULL(struct repeatation required)
                if(shadow_dict_index[i][2] != ''):
                    #store name of struct to be repeated
                    format_string_to_be_repeated = shadow_dict_index[i][2]
                    
                    #position of the struct to be repeated
                    pos_of_repeat_structure = i+1
                    
                    
                    #when static number of struct is required
                    static_no_of_repeatations = shadow_dict_index[i][10]
                    if shadow_dict_index[i][10] == 0:
                        static_no_of_repeatations = no_of_repeatitions
                    
                    # if no_of_repeatitions != shadow_dict_index[i][10]:
                    #     if bits_list[i]:
                    #         previous_bit_list = int(struct_format[-1]) & ((1<<(8-bits_list[i]))-1)
                    #         current_bit_list = static_no_of_repeatations << (8-bits_list[i])
                    #         data_value = previous_bit_list | current_bit_list
                    #         #print(previous_bit_list, current_bit_list, data_value)
                    #         #struct_format.pop(-1)
                    #         #struct_format.append(f'{data_value}')
                    #     else:
                    #         struct_format.pop(-1)
                    #         struct_format.append(f'{shadow_dict_index[i][10]}')
                    
                    if no_of_bits:
                        print("Invalid bit field in message")
                        break
                    
                    # print("no_of_repeatitions outside recursion",no_of_repeatitions, pos_of_repeat_structure, format_string_to_be_repeated)
                    # print("*************************+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    

                    
                    try:
                        label_format, struct_format, index_after_recursion, index_after_recursion_message_data = self.recursive_struct_generator(i, index, shadow_dict_index, message_data, message_format, struct_format, label_format, no_of_repeatitions, static_no_of_repeatations, bits_list)
                        index = index_after_recursion_message_data
                    except Exception as e:
                        print("Recursion error outside",e)

        # except:
        #     print("sksl")
        return struct_format, label_format
            
        
    def recursive_struct_generator(self, i, index, shadow_dict_index, message_data, message_format, struct_format, label_format, no_of_repeatitions,static_no_of_repeatations, bits_list): 
        #print("################################## RECURSION #################################################")
        format_string_to_be_repeated = shadow_dict_index[i][2]  
        pos_of_repeat_structure = i+1
        no_of_bits = 0
        # print("current_data_format=====", struct_format)
        # print("no_of_repeatitions inside recursion",no_of_repeatitions, static_no_of_repeatations, pos_of_repeat_structure, format_string_to_be_repeated)
        # print("*************************+++++++++++++++++++++++++++++++++++++++++++++++++++++")                       


        rep_index = i
        message_index = index
        static = int(static_no_of_repeatations)
        dynamic = no_of_repeatitions
        string_to_repeat = format_string_to_be_repeated
        #iterate the struct
        for idx in range(0, static):
            #print(idx, dynamic, static)
            if idx<int(dynamic):
                i = rep_index+1  
                struc_contains = shadow_dict_index[i][8].split('.')             
                #to iterate till end of current struct only
                
                #print("format====struct", string_to_repeat, struc_contains)
                while(string_to_repeat in struc_contains):
                    # isPart of struct
                    
                    
                    # print("rep_index", i)
                    # print("message index", message_index)
                    # print("struct--", struc_contains)
                    
                    #value of input                           
                    data_value = message_data[message_index]
                    #print("data value", data_value)
                    
                    #label name of current attribute
                    format_of_message = message_format[message_index]                    
                    #===bits to byte conversion when bits list is non zero===
                    #bits_list is zero
                    if bits_list[i] == 0 and no_of_bits == 0:
                        struct_format.append(data_value)
                        label_format.append(format_of_message)                        
                        
                        no_of_repeatitions = int(data_value)
                        message_index+=1
                        
                    #when bits list architecture is wrong in the message    
                    elif bits_list[i] == 0 and no_of_bits != 0:
                        print("Wrong bit field in message")
                        return
                    
                    #when bits list is non zero
                    else:
                        no_of_bits+=bits_list[i]
                        if no_of_bits == 8:
                            struct_format.append(data_value)
                            label_format.append(format_of_message)
                            no_of_repeatitions = int(data_value)>>(8-bits_list[i])
                            no_of_bits = 0
                            message_index+=1 
                                                   
                    #print("bit", bits_list[i])
                    #recursion starts when "ATR_ARRAY_SIZE" is not NULL(struct repeatation required)
                    if(shadow_dict_index[i][2] != ''):
                        #store name of struct to be repeated
                        format_string_to_be_repeated = shadow_dict_index[i][2]                        
                        #position of the struct to be repeated
                        pos_of_repeat_structure = i+1
                        #when static number of struct is required
                        static_no_of_repeatations = shadow_dict_index[i][10]
                        if shadow_dict_index[i][10] ==0:
                            static_no_of_repeatations = no_of_repeatitions
                        
                        # if no_of_repeatitions != shadow_dict_index[i][10]:
                        #     if bits_list[i]:
                        #         previous_bit_list = int(struct_format[-1]) << (bits_list[i])
                        #         previous_bit_list = previous_bit_list >>(bits_list[i])
                        #         current_bit_list = static_no_of_repeatations >> (8-bits_list[i])
                        #         data_value = previous_bit_list | current_bit_list
                        #         struct_format.pop(-1)
                        #         struct_format.append(f'{data_value}')
                        #     else:
                        #         print("pppp", f'{shadow_dict_index[i][10]}')  
                        #         struct_format.pop(-1)
                        #         struct_format.append(f'{shadow_dict_index[i][10]}')
                        
                        if no_of_bits:
                            print("Invalid bit field in message")
                            error_flag = 1
                            break                        
                        try:
                            label_format, struct_format, index_after_recursion, index_after_recursion_message_data = self.recursive_struct_generator(i, message_index, shadow_dict_index, message_data, message_format, struct_format, label_format, no_of_repeatitions, static_no_of_repeatations, bits_list)
                            message_index = index_after_recursion_message_data
                            i = index_after_recursion
                        except Exception as e:
                            print("Recursion error inside",e)
                    else:
                        i+=1
                    
                    if i==len(shadow_dict_index):
                        break
                    struc_contains = shadow_dict_index[i][8].split('.')
                    # print("struct contains", struc_contains)
                    # print("format to be repeated--", format_string_to_be_repeated)
            else:
                
                i = rep_index+1
                #format_index = index
                struc_contains = shadow_dict_index[i][8].split('.')             
                #to iterate till end of current struct only
                #print("format====struct", string_to_repeat, struc_contains)
                while(string_to_repeat in struc_contains):
                    # isPart of struct
                    
                    
                    # print("<<rep_index", i) 
                    # print("<<message index", message_index)

                    #print("<<format to be repeated--", format_string_to_be_repeated)
                    
                    #value of input                           
                    data_value = 0
                    
                    #label name of current attribute
                    #format_of_message = message_format[format_index]
                    format_of_message = shadow_dict_index[i][5]                    
                    #===bits to byte conversion when bits list is non zero===
                    #bits_list is zero
                    if bits_list[i] == 0 and no_of_bits == 0:
                        struct_format.append(data_value)
                        label_format.append(format_of_message)
                        #print("<<format index", format_index)
                        # print("<<struct contains", struc_contains)
                        # print("<<format of message\n", format_of_message)                        
                        #format_index+=1
                        
                    #when bits list architecture is wrong in the message    
                    elif bits_list[i] == 0 and no_of_bits != 0:
                        print("Wrong bit field in message")
                        return
                    
                    #when bits list is non zero
                    else:
                        no_of_bits+=bits_list[i]
                        if no_of_bits == 8:
                            struct_format.append(data_value)
                            label_format.append(format_of_message)
                            no_of_bits = 0
                            #print("<<format index", format_index)
                            # print("<<struct contains", struc_contains)
                            # print("<<format of message\n", format_of_message)
                            #format_index+=1                                            
                        
                    #when structure is found, the content of structure will not be added
                    if(shadow_dict_index[i][2] != ''):
                        
                        if shadow_dict_index[i][10]:
                            try:
                                label_format, struct_format, index_after_recursion, index_after_recursion_message_data = self.recursive_struct_generator(i, message_index, shadow_dict_index, message_data, message_format, struct_format, label_format, 0, shadow_dict_index[i][10], bits_list)
                                #format_index = index_after_recursion_message_data
                                i = index_after_recursion
                            except Exception as e:
                                print("Recursion error inside",e)
                        else:
                            i = self.find_index_of_label_format(shadow_dict_index, i, bits_list)
                    else:
                        i+=1
                    
                    if i==len(shadow_dict_index):
                        break
                    struc_contains = shadow_dict_index[i][8].split('.')
            # print("struct format", struct_format)
            # print("label format", label_format)
            # print("format====struct", format_string_to_be_repeated, struc_contains)
            # print("message index ===== index after recursion inside", message_index, i)        
        return label_format, struct_format, i, message_index
    
    def find_index_of_label_format(self, shadow_dict_index, i, bits_list):
        index = i
        to_ignored_string = shadow_dict_index[index][2]
        index+=1
        end_struct = shadow_dict_index[index][8].split('.')
        # print("to ignores", to_ignored_string)
        # print("end struct", end_struct)            
        while(to_ignored_string in end_struct and index < len(shadow_dict_index)):
            if shadow_dict_index[index][2] != '':
                #print("pppppkdkkdj")
                index = self.find_index_of_label_format(shadow_dict_index, index, bits_list)
            else:
                index+=1
            
            end_struct = shadow_dict_index[index][8].split('.')
            #print("end struct\n", end_struct)  
        return index