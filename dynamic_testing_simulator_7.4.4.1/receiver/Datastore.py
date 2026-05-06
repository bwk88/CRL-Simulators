#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 15:48:04 2024

@author: root
"""
from PyQt5 import QtGui

class TableModel(QtGui.QStandardItemModel):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.setHorizontalHeaderLabels(["Date Time", "Message Header", "Src CSI ID","Dest CSI ID","Message Name", "Observation","Parsed Data" ,"Bytes Hex Content","NA","NA"])
        self.delta_time_list = []
        
    def updateHeader(self, listHeaderLabels):
        self.setHorizontalHeaderLabels(listHeaderLabels)
        
    def get_delta_time_list(self):
        return self.delta_time_list
    
    def set_delta_time_list(self, updated_delta_time_list):
        self.delta_time_list = updated_delta_time_list

class TableMessageModel(QtGui.QStandardItemModel):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.setHorizontalHeaderLabels(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
        
    def updateHeader(self, listHeaderLabels):
        self.setHorizontalHeaderLabels(listHeaderLabels)
        
class TableSingleSampleModel(QtGui.QStandardItemModel):
    def __init__(self, rows, columns):
        super().__init__(rows, columns)
        self.setHorizontalHeaderLabels(["Bit Size", "Data Type", "Field", "Value", "Info"])
        
class Datastore():
    __instance = None
    def __init__(self):
        self.model = TableModel(0, 4)
        self.model_multi_samples = TableMessageModel(0, 0)
        self.model_single_sample = TableSingleSampleModel(0, 5)
        
datastore = Datastore()