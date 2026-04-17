#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 27 16:50:42 2025

@author: kuldeepsingh@Indigenous.com
"""

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer, QThread
import time
from qlm_publisher import QLM_Publisher

class publisherProcess(QObject):
    logging_data = pyqtSignal(str)
    finished = pyqtSignal()
    update_signal_publish = pyqtSignal(str)
    update_progress_signal = pyqtSignal(str)
    error_signal_received_publisher = pyqtSignal(str)
    
    
    def __init__(self, startPublishData):
        super().__init__()
        self.Publisher_instance = QLM_Publisher()
        self.startPublishData = startPublishData
        self.Publisher_instance.update_signal_publish.connect(self.sentUpadateSignal)
        self.Publisher_instance.progress_signal.connect(self.sentProgressSignal)
        self.Publisher_instance.error_signal_publish.connect(self.sentErrorSignal)
        
    def sentUpadateSignal(self, data):
        self.update_signal_publish.emit(data)
        
    def sentProgressSignal(self, progress):
        self.update_progress_signal.emit(progress)
    
    def sentErrorSignal(self, error_str):
        self.error_signal_received_publisher.emit(error_str)
    
    def stopProcess(self):
        self.finished.emit()
        
        
    @pyqtSlot()
    def run(self):
        self.Publisher_instance.start_process(self.startPublishData)
        self.finished.emit()