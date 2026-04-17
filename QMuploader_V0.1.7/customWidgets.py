#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 16 14:52:14 2025

@author: kuldeepsingh@Indigenous.com
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QDialog, QGridLayout, QComboBox
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QColor, QImage, QBrush, QIcon
from global_data import data
from ui_operations import ui_ops




class settingsFieldWidgets(QWidget):
    settings_updated_signal = pyqtSignal(str)
    def __init__(self, fieldName):
        super().__init__()
        layout = QHBoxLayout()
        
        self.fieldName = fieldName  
        self.label = QLabel(f"{self.fieldName}")
        self.label.setFixedWidth(200)
        self.fieldValue = QLineEdit()
        self.fieldValue.setPlaceholderText(f"Set {self.fieldName}")
        self.fieldValue.setReadOnly(True)
        self.label.setFixedHeight(40)
        self.fieldValue.setFixedHeight(40)
        self.fieldValue.setStyleSheet("""
                                          padding: 0px 10px 0px 10px;
                                          background-color: #1c1c28;
                                          """)
        layout.addWidget(self.label)
        layout.addWidget(self.fieldValue) 
        self.button = QPushButton("Edit")
        self.button.setFixedSize(60,40)
        self.button.clicked.connect(self.onButtonClicked)
        layout.addWidget(self.button)

        self.setLayout(layout)    
       
    
    def hideButton(self):
        self.button.hide()
        
    def onButtonClicked(self):
        self.editSettingsWidget = editSettingsWidget(self.fieldName)
        self.editSettingsWidget.show()
        self.editSettingsWidget.update_settings_signal.connect(self.setfieldValue)

    def setInitialValues(self, value, name):
        self.fieldValue.setText(value)          
            
    def setfieldValue(self,value):
        print("kasjhdfksajfhd")
        self.fieldValue.setText(value)
        self.settings_updated_signal.emit(value)
    




class settingsFieldProjectSelector(QWidget):
    user_added_combo_items_signal = pyqtSignal(str)
    user_deleted_combo_items_signal = pyqtSignal(str)
    settings_updated_signal_combobox = pyqtSignal(str)
    def __init__(self, fieldName):
        super().__init__() 
    
        layout = QHBoxLayout()
        self.fieldName = fieldName
        self.label = QLabel(f"{self.fieldName}")
        self.projectCombobox = QComboBox()
        self.label.setFixedHeight(40)
        self.projectCombobox.setFixedHeight(40)
        self.projectCombobox.setStyleSheet("""
                                          padding: 0px 10px 0px 10px;
                                          background-color: #1c1c28;
                                          """)
        layout.addWidget(self.label)
        layout.addWidget(self.projectCombobox)
        
        self.button = QPushButton("Set")
        self.button.setFixedSize(60,40)
        self.button.clicked.connect(self.onButtonClicked)
        layout.addWidget(self.button)
                
        self.addButton = QPushButton("")
        self.addButton.setFixedSize(40,40)
        self.addButton.setStyleSheet("""
                                        background-color: transparent;
                                        color: #d2d3df;
                                        font-weight: bold;
                                        font-size: 15px;
                                        border: 0px;
                                   """) 
        self.addButton.clicked.connect(self.onAddClicked)
        layout.addWidget(self.addButton)

        
        self.delButton = QPushButton("")
        self.delButton.setFixedSize(40,40)
        self.delButton.setStyleSheet("""
                                        background-color: transparent;
                                        color: #d2d3df;
                                        font-weight: bold;
                                        font-size: 15px;
                                        border: 0px;
                                     """)
        self.delButton.clicked.connect(self.onDelClicked)
        layout.addWidget(self.delButton)

        self.setLayout(layout)
        self.setIcons()
                        
        
    def setIcons(self):
        addIcon =  QPixmap("icons/add.png")
        addIcon_pixmap = ui_ops.tint_pixmap(addIcon, QColor(76,175,80))
        self.addButton.setIcon(QIcon(addIcon_pixmap))
        self.addButton.setIconSize(QSize(35,35))
        
        deleteIcon = QPixmap("icons/delete.png")
        deleteIcon_pixmap = ui_ops.tint_pixmap(deleteIcon, QColor(255,77,77))
        self.delButton.setIcon(QIcon(deleteIcon_pixmap))
        self.delButton.setIconSize(QSize(25,25))

    
    def onAddClicked(self):
        print("adding new test_paln")
        self.editSettingsWidget = editSettingsWidget(self.fieldName)
        self.editSettingsWidget.show()
        self.editSettingsWidget.update_settings_signal.connect(self.addComboItemsUser)
        
    def onDelClicked(self):
        print("deleting combo item")
        item = self.projectCombobox.currentText()
        self.user_deleted_combo_items_signal.emit(item)

        
    def addComboItemsUser(self,value):
        print("alsjdflsajkfdlsakjflsjalfkjsalkjf")
        self.projectCombobox.addItem(value)
        self.projectCombobox.setCurrentText(value)
        self.user_added_combo_items_signal.emit(value)
      
    def addComboItem(self, item):
        if self.projectCombobox.findText(item)==-1:
            self.projectCombobox.addItem(item)
    
    def deleteComboItem(self, item):
        index =  self.projectCombobox.findText(item)
        if index != -1:
            self.projectCombobox.removeItem(index)
        else: 
            print("cannot remove")
        
    def onButtonClicked(self):
        selected_combobox = self.projectCombobox.currentText()
        print("alskdflaskjfdlaskj", selected_combobox)
        self.settings_updated_signal_combobox.emit(selected_combobox)
    
    def selectItem(self,item):
        self.projectCombobox.setCurrentText(item)
        print("current text selected", item)
        

        
class editSettingsWidget(QWidget):
    update_settings_signal = pyqtSignal(str)
    def __init__(self, name):
        super().__init__()
        # self.setModal(True)
        self.name = name
        self.setFixedSize(300,100)
        self.setWindowTitle(f"Change {name}")
        
        layout = QHBoxLayout()
        
        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(f"Set {name}")
        
        layout.addWidget(self.line_edit)
        
        self.button = QPushButton("Set")
        self.button.clicked.connect(self.onButtonClicked)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
        
        
    def onButtonClicked(self):
        print("12314214")
        newNameValue = self.line_edit.text()
        self.update_settings_signal.emit(newNameValue)
        self.close()
       
        
       
    
class HistoryDataWidget(QWidget):
    display_history_details_signal = pyqtSignal(str)
    resume_button_clicked_signal = pyqtSignal(str)
    def __init__(self, HistoryData):
        super().__init__()
        self.History = HistoryData
        self.mainlayout = QHBoxLayout()
        self.labelId = QLabel(f"{HistoryData['job_id']}")
        self.labelId.setStyleSheet("""
                                        background-color: transparent;
                                        font-weight: bold;
                                        font-size: 12px;
                                        color: #d2d3df;
                                     """)
        self.labelId.setFixedHeight(25)
        self.labelId.setFixedWidth(30)
        self.mainlayout.addWidget(self.labelId)
        
        self.vlayoout = QVBoxLayout()
        self.labelName = QLabel(f"{HistoryData['job_type']}  {HistoryData['Project']} - {HistoryData['TestPlan']}")
        self.labelName.setStyleSheet("""
                                        background-color: transparent;
                                        font-weight: bold;
                                        font-size: 12px;
                                        color: #d2d3df;
                                     """)
        
        self.labelExecutionTime = QLabel(f"{HistoryData['Time']} {HistoryData['Date']}")
        self.labelExecutionTime.setStyleSheet("""
                                        background-color: transparent;
                                        color: #d2d3df;
                                     """)
        self.labelName.setFixedHeight(25)
        
        self.labelExecutionTime.setFixedHeight(15)

        self.vlayoout.addWidget(self.labelName)
        self.vlayoout.addWidget(self.labelExecutionTime)
        self.mainlayout.addLayout(self.vlayoout)
        self.Hlayout = QHBoxLayout()
        self.labelProgress = QLabel(f"{HistoryData['ProgressStatus']}%")
        self.labelProgress.setStyleSheet("""
                                        background-color: transparent;
                                        color: #d2d3df;
                                     """)
        self.labelProgress.setFixedSize(60,40)
        self.buttonResume = QPushButton("Resume")
        self.buttonResume.setStyleSheet("""
                                        background-color: #1c1c28;
                                        color: #d2d3df;
                                     """)
        self.buttonResume.setFixedSize(60,40)
        self.button = QPushButton("View")
        self.button.setStyleSheet("""
                                        background-color: #1c1c28;
                                        color: #d2d3df;
                                     """)
        self.button.setFixedSize(60,40)
        self.Hlayout.addWidget(self.labelProgress)
        self.Hlayout.addWidget(self.buttonResume)
        self.Hlayout.addWidget(self.button)
        self.mainlayout.addLayout(self.Hlayout)
        self.button.clicked.connect(self.onButtonClicked)
        self.buttonResume.clicked.connect(self.onResumeButtonClicked)
        self.setLayout(self.mainlayout)
     
    def onButtonClicked(self):
        print("clickerd  view")
        self.display_history_details_signal.emit(str(self.History['job_id']))
    
    def onResumeButtonClicked(self):
        print("clickerd resume")
        self.resume_button_clicked_signal.emit(str(self.History['job_id']))
        
    def updateLiveData(self, progress):
        #print("updating progress value in history", progress)
        self.labelProgress.setText(f"{progress}%")
    
    def getObjectData(self):
        return self.History

    def enableResume(self, status):
        print(f"{status} disabled resume")
        self.buttonResume.setEnabled(status)
        self.buttonResume.setStyleSheet("""
                                         background-color: #0f0f16;
                                        """)
    def get_id(self):
        return int(self.labelId.text())
    
    def get_Data(self):
        return self.History 
        
        
    