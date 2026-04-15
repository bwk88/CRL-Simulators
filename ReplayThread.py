#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 13:04:08 2024

@author: root
"""
from PyQt5.QtCore import QThread, pyqtSignal
import time
import struct
from Datastore import datastore
from udpsender import UdpSender
from Configuration import config
from datetime import datetime
import crc_calulator
import math

class ReplayThread(QThread):
    signal_data_sent = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(ReplayThread, self).__init__(parent)
        self.running = False
        self.pause = False
        self.sender = UdpSender()
        self.timestamp_updated = False
        
    def run(self):
        self.running = True
        no_of_messages = datastore.model.rowCount()
        msg_num = 0
        while self.running:
            if not self.pause:
                item = datastore.model.item(msg_num, 2)
                data = bytearray.fromhex(item.text())
                if self.timestamp_updated:
                    data = self.get_time_crc_updated_packet(data)
                print('datastore.model.delta_time_list[row]:',datastore.model.delta_time_list[msg_num])
                time.sleep(datastore.model.delta_time_list[msg_num] / 1000)
    
                if self.pause:
                    continue
                else:
                    if(self.running == True):
                        self.sender.send_packet(data)  
                        msg_num = msg_num + 1
                        if msg_num == no_of_messages:
                            self.running = False
                            message = 'Replay Stopped'
                            self.signal_data_sent.emit(message)
                    else:
                        message = 'Replay Stopped'
                        self.signal_data_sent.emit(message)
                        break
            else:
                print('paused...waiting for stop or resume')
                time.sleep(0.2)

    def stop(self):
        self.running = False
        
    def pause_reply(self):
        print('ReplayThread Paused')
        self.pause = True
        
    def set_timestamp_update_status(self, timestamp_to_be_updated):
        print('timestamp_to_be_updated:', timestamp_to_be_updated)
        self.timestamp_updated = timestamp_to_be_updated        
    
    def resume_reply(self):
        print('ReplayThread Resumed')
        self.pause = False 
        
    def getMsgListFromMsgTuple(self, msgTuple):
        msgList = []
        for x in range(len(msgTuple)):
            msgList.append(msgTuple[x])
        return msgList
    
    def get_time_crc_updated_packet(self, data):
        print('type of data:', type(data))
        header_format_rcv = config.header_formats[0]
        header_length_rcv = struct.calcsize(f'={header_format_rcv}') #getting the header length
        header_tuple_rcv = struct.unpack(f'={header_format_rcv}',data[0:header_length_rcv]) #unpacking only header 
        hdrList = self.getMsgListFromMsgTuple(header_tuple_rcv)
            
        datetime_now = datetime.now()
        unique_message_code = 1
        hdrList[8]  = datetime_now.day
        hdrList[9]  = datetime_now.month
        hdrList[10] = datetime_now.year
        hdrList[11] = datetime_now.hour
        hdrList[12] = datetime_now.minute
        hdrList[13] = datetime_now.second
        hdrList[14] = math.floor(datetime_now.microsecond / 1000)
        hdrList[15] = unique_message_code    
        print('hdrList ', hdrList)    
        header_packet = struct.pack(f'={header_format_rcv}', *tuple(hdrList))
        
        data[:23] = header_packet
        content = data[:-4]
        calculated_crc = crc_calulator.crc_32(content)
        crc_packet = struct.pack('=I',calculated_crc) 
        data[-4:] = crc_packet
        return data    
        
  