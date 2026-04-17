#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 12:30:11 2025

@author: kuldeepsingh@Indigenous.com
"""
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer, QThread
import time
from scrapper_mahai import QLM_Uploader

class seleniumProcess(QObject):
    logging_data = pyqtSignal(str)
    finished = pyqtSignal()
    update_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(str)
    request_stop_signal = pyqtSignal()
    
    def __init__(self, startProcessData):
        super().__init__()
        self.request_stop_signal.connect(self.stopQLM)
        
        self.QLM_instance = QLM_Uploader()
        self.startProcessData = startProcessData
        self.QLM_instance.update_scrapper_signal.connect(self.sentUpadateSignal)
        self.QLM_instance.updated_uploader_progress_signal.connect(self.sentProgressSignal)
        self.QLM_instance.force_stopped_signal.connect(self.stoppedUploader)
    
    @pyqtSlot(str)
    def sentUpadateSignal(self, value):
        self.update_signal.emit(value)
    
    @pyqtSlot(str)
    def sentProgressSignal(self, value):
        self.progress_signal.emit(value)
    
    @pyqtSlot()
    def stoppedUploader(self):
        self.finished.emit()
        
    @pyqtSlot()
    def stopQLM(self):
        print("Stopping QLM Instance")
        self.QLM_instance.quit()
    
    @pyqtSlot()
    def run(self):
        # try:
        self.QLM_instance.start_process(self.startProcessData)
        # except Exception as e:
        #     print(f"Error: {e}")
        # finally:
        #     self.finished.emit()



        