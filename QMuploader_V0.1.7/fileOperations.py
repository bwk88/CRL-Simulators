#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 12:30:11 2025

@author: kuldeepsingh@Indigenous.com
"""
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer, QThread
import time, os, json
from global_data import data


class fileOperations(QObject):
    readSettingsSignal = pyqtSignal()
    readHistorySignal = pyqtSignal()
    writeSettingsSignal = pyqtSignal()
    writeHistorySignal = pyqtSignal(str)
    writeProgressSignal = pyqtSignal(str)
    readHistoryViewerSignal = pyqtSignal(str)
    updateHistorySignal = pyqtSignal(str)
    
    
    finishedReadSettingsSignal = pyqtSignal()
    finishedReadHistorySignal = pyqtSignal()
    finishedWriteSettingsSignal = pyqtSignal()
    finishedWriteHistorySignal = pyqtSignal(str)
    finishedreadHistoryViewerSignal = pyqtSignal()
    finishedupdateHistorySignal = pyqtSignal()    
    
    def __init__(self):
        super().__init__()
        self.readSettingsSignal.connect(self.readSettingsData)
        self.readHistorySignal.connect(self.readLoadHistoryData)
        self.writeSettingsSignal.connect(self.writeSettingsData)
        self.writeHistorySignal.connect(self.writeHistoryData)
        self.writeProgressSignal.connect(self.writeProgressValue)
        self.readHistoryViewerSignal.connect(self.readHistoryViewerData)
        self.updateHistorySignal.connect(self.updateHistory)
      
    @pyqtSlot()    
    def readSettingsData(self):
        if os.path.exists("settingsData.json"):
            with open("settingsData.json", "r") as file:
                data.settingsData = json.load(file)
                #print("File Opertaion", data.settingsData)
            file.close()
        self.finishedReadSettingsSignal.emit()
    
    @pyqtSlot() 
    def readLoadHistoryData(self):
        if os.path.exists("HistoryDataList.json") and os.path.getsize("HistoryDataList.json")!=0:
            with open("HistoryDataList.json", "r") as file:  
                data.HistoryDataList = json.load(file)  
                #print("File operation History", data.HistoryData)
            file.close()
        self.finishedReadHistorySignal.emit()
         
    @pyqtSlot() 
    def writeSettingsData(self):
        # print("**********************************************************************")
        # print("(((((((((((((((((writeSettingsData))))))))))))))))))")
        # print("-------------------------------settings changes-------------------------------------")
        # print(data.settingsData)
        # print("------------------------------------------------------------------------------------")
        with open("settingsData.json", "w") as file:
            json.dump(data.settingsData, file, indent=4)
        file.close()
        self.finishedWriteSettingsSignal.emit()
    
        
    @pyqtSlot(str) 
    def writeHistoryData(self, HistoryType):
        # print("**********************************************************************")
        # print("(((((((((((((((((writeHistoryData))))))))))))))))))")
        # print("**********************************************************************")
        # print("updating History for id: ", data.current_job_publisher)
        # print("**********************************************************************")
        # print("INSERTING:     ",data.HistoryData)
        # print("**********************************************************************")
        if HistoryType == "UPLOAD":
            data.HistoryDataList[str(data.current_job_uploader)] = data.HistoryData
        if HistoryType == "PUBLISH":
            data.HistoryDataList[str(data.current_job_publisher)] = data.HistoryData
        # Save it to json file
        with open("HistoryDataList.json","w") as file:
            json.dump(data.HistoryDataList,file,indent=4)
        file.close()
        self.finishedWriteHistorySignal.emit(HistoryType)
        
        
    @pyqtSlot(str) 
    def writeProgressValue(self, HistoryType):
        # print("**********************************************************************")
        # print("(((((((((((((((((writeProgressValue))))))))))))))))))")
        # print("**********************************************************************")
        # print("updating progress for id: ", data.current_job_publisher)
        # print("**********************************************************************")
        # print("PPGRESS UPDATING:     ",data.HistoryDataList)
        # print("**********************************************************************")
        # print(data.HistoryDataList)
        if HistoryType == "UPLOAD":
            data.HistoryDataList[str(data.current_job_uploader)]["ProgressStatus"] = data.current_progress_value
        if HistoryType == "PUBLISH":
            data.HistoryDataList[str(data.current_job_publisher)]["ProgressStatus"] = data.current_publisher_progress_value
        # Save it to json file
        with open("HistoryDataList.json","w") as file:
            json.dump(data.HistoryDataList,file,indent=4)
        file.close()
        
    @pyqtSlot(str) 
    def updateHistory(self, HistoryType):
        # Save it to json file
        # print("**********************************************************************")
        # print("(((((((((((((((((updateHistory))))))))))))))))))")
        # print("**********************************************************************")
        # print("**********************************************************************")
        # print("UPDATING:     ",data.HistoryData)
        # print("**********************************************************************")
        with open("HistoryDataList.json","w") as file:
            json.dump(data.HistoryDataList,file,indent=4)
        file.close()
        self.finishedupdateHistorySignal.emit()

    @pyqtSlot(str) 
    def readHistoryViewerData(self, Filename):
        folder = Filename.split("_")[0]
        #print(f"=>>>>>>>>>>>>>>>>>>>>>>>>>{folder}/{Filename}.json")
        if os.path.exists(f"{folder}/{Filename}.json") and os.path.getsize(f"{folder}/{Filename}.json")!=0:
            with open(f"{folder}/{Filename}.json", "r") as file:  
                data.DetailHistoryData = json.load(file)
                #print("Read data")
            file.close()
            self.finishedreadHistoryViewerSignal.emit()



    
 
      
    