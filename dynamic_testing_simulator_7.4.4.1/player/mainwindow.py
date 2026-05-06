# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5.QtWidgets import QCompleter, QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets
from xml.etree.ElementTree import ElementTree, Element, SubElement
from Configuration import config
from udpsender import UdpSender
import time 
import struct
import datetime
import math
import pandas as pd

from csv_dict import csv_dict
# from bitstring import BitArray
import crc_calulator
from UserInputDialog import UserInputDialog
from handleChange import handleChange
import subprocess

from debuggerFile import DBUG
from SNS.widgetsCustom import backButton
from SNS.SNS import saveAndSend
from SNS.models import mainWindow_SNS_save_edit_data
from SNS.customColours import GREY_700, GREY_800, GREY_900
from dyanamic_structs import loadDyanamic_data, generate_dyanamic_data
from utilities import depth_color, struct_level_finder, clearLayout, get_bits_from_bytes, printDict
from mainCustomwidgets import errorDisplay

from API_Client.API_invoke import api_invoke



GLOBAL_DELAY = 0
MSG_LEN_INDEX = 4
NESTED_STRUCT_IDENTIFIER = "<<NestedStruct>>"


class Ui_MainWindow(object):   
    def setupUi(self, MainWindow):
    
        DBUG.setDebuggingMode(True)
        DBUG.setWhereMode(False)
        DBUG.setInfomationMode(False)
        DBUG.setCallerPrintMode(False)

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1481, 786)
        self.colr = "#e0e0e0"
        self.index_value = 0
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        
        # Tab Player
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButtonLoad = QtWidgets.QPushButton(self.tab)
        self.pushButtonLoad.setObjectName("pushButtonLoad")
        self.horizontalLayout_6.addWidget(self.pushButtonLoad)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.checkBoxTimestampUpdated = QtWidgets.QCheckBox(self.tab)
        self.checkBoxTimestampUpdated.setObjectName("checkBoxTimestampUpdated")
        self.horizontalLayout_6.addWidget(self.checkBoxTimestampUpdated)
        self.pushButtonSendSelected = QtWidgets.QPushButton(self.tab)
        self.pushButtonSendSelected.setObjectName("pushButtonSendSelected")
        self.horizontalLayout_6.addWidget(self.pushButtonSendSelected)
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_6.addWidget(self.label_3)
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_6.addWidget(self.lineEdit)
        self.pushButtonSendSelectNext = QtWidgets.QPushButton(self.tab)
        self.pushButtonSendSelectNext.setObjectName("pushButtonSendSelectNext")
        self.horizontalLayout_6.addWidget(self.pushButtonSendSelectNext)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 6)
        self.horizontalLayout_6.setStretch(2, 1)
        self.horizontalLayout_6.setStretch(3, 1)
        self.horizontalLayout_6.setStretch(4, 1)
        self.horizontalLayout_6.setStretch(5, 1)
        self.horizontalLayout_6.setStretch(6, 1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_6)
        self.tableWidgetMessages = QtWidgets.QTableWidget(self.tab)
        self.tableWidgetMessages.setObjectName("tableWidgetMessages")
        self.tableWidgetMessages.setColumnCount(0)
        self.tableWidgetMessages.setRowCount(0)
        self.verticalLayout_9.addWidget(self.tableWidgetMessages)
        self.gridLayout_2.addLayout(self.verticalLayout_9, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        
        # TAB SENDER
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.backButton = backButton(self.tab_2)
        self.horizontalLayout.addWidget(self.backButton)
        self.backButton.hide()
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxMessages = QtWidgets.QComboBox(self.tab_2)
        self.comboBoxMessages.setObjectName("comboBoxMessages")
        self.horizontalLayout.addWidget(self.comboBoxMessages)
        # self.label_2 = QtWidgets.QLabel(self.tab_2)
        # self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        # self.label_2.setObjectName("label_2")
        # self.horizontalLayout.addWidget(self.label_2)
        # self.lineEditHeader = QtWidgets.QLineEdit(self.tab_2)
        # self.lineEditHeader.setText("")
        # self.lineEditHeader.setObjectName("lineEditHeader")
        # self.horizontalLayout.addWidget(self.lineEditHeader)
        self.pushButtonSend = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonSend.setObjectName("pushButtonSend")
        self.horizontalLayout.addWidget(self.pushButtonSend)
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.lineEditTime = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditTime.setObjectName("lineEditTime")
        self.horizontalLayout.addWidget(self.lineEditTime)
        self.pushButtonPeriodic = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonPeriodic.setObjectName("pushButtonPeriodic")
        self.horizontalLayout.addWidget(self.pushButtonPeriodic)
        
        #mahaiyo
        self.pushButtonAddPeriodicMessage = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonAddPeriodicMessage.setObjectName("pushButtonAddPeriodicMessage")
        self.horizontalLayout.addWidget(self.pushButtonAddPeriodicMessage)
        self.pushButtonAddPeriodicMessage.clicked.connect(self.addPeriodicMessage)
        self.pushButtonAddPeriodicMessage.hide()

        # SNS
        self.snsWidget = QtWidgets.QWidget()
        self.snsWidget.setStyleSheet(f"""
                                QPushButton{{
                                    background-color: {GREY_900};
                                    color: #ffffff;
                                }}
                                QPushButton:hover{{
                                    background-color: #eeeddd;
                                    color: #000000;
                                }}
                                QLineEdit{{
                                    background-color: #ffffff;
                                    padding: 2px 5px 2px 5px;
                                    }}
                                """)
        self.snsLayout = QtWidgets.QHBoxLayout(self.snsWidget)
        self.snsLayout.setObjectName("horizontalLayout")
        self.DelayLabel = QtWidgets.QLabel(self.tab_2)
        # self.DelayLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DelayLabel.setObjectName("DelayLabel")
        self.snsLayout.addWidget(self.DelayLabel)
        
        self.delayLineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.delayLineEdit.setObjectName("delayLineEdit")
        self.snsLayout.addWidget(self.delayLineEdit)
        self.delayLineEdit.setPlaceholderText("Delay (ms)")
        self.pushButtonSaveEdit = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonSaveEdit.setObjectName("pushButtonSavePeriodic")
        self.snsLayout.addWidget(self.pushButtonSaveEdit)
        self.pushButtonSaveEdit.setFixedWidth(140)
        self.horizontalLayout.addWidget(self.snsWidget)
        self.snsWidget.hide() 
        
        self.verticalLayout_10.addLayout(self.horizontalLayout)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.pushButtonClearValues = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonClearValues.setEnabled(True)
        self.pushButtonClearValues.setObjectName("pushButtonClearValues")
        self.horizontalLayout_9.addWidget(self.pushButtonClearValues)
        self.pushButtonSaveValues = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonSaveValues.setEnabled(False)
        self.pushButtonSaveValues.setObjectName("pushButtonSaveValues")
        self.horizontalLayout_9.addWidget(self.pushButtonSaveValues)
        
        #Load values
        self.comboBoxLoadValues = QtWidgets.QComboBox(self.tab_2)
        self.comboBoxLoadValues.setObjectName("comboBoxLoadValues")
        self.horizontalLayout_9.addWidget(self.comboBoxLoadValues)
        self.comboBoxLoadValues.addItem("Load value From Sheet")
        self.comboBoxLoadValues.addItem("Load value 1")
        
        self.pushButtonLoadValues = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonLoadValues.setEnabled(True)
        self.pushButtonLoadValues.setObjectName("pushButtonLoadValues")
        self.horizontalLayout_9.addWidget(self.pushButtonLoadValues)
        
        self.pushButtonExtra1 = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonExtra1.setEnabled(True)
        self.pushButtonExtra1.setObjectName("pushButtonExtra1")
        self.horizontalLayout_9.addWidget(self.pushButtonExtra1)
        self.pushButtonExtra2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonExtra2.setEnabled(False)
        self.pushButtonExtra2.setObjectName("pushButtonExtra2")
        self.horizontalLayout_9.addWidget(self.pushButtonExtra2)
        self.pushButtonExtra3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonExtra3.setEnabled(False)
        self.pushButtonExtra3.setObjectName("pushButtonExtra3")
        self.horizontalLayout_9.addWidget(self.pushButtonExtra3)
        self.label_10 = QtWidgets.QLabel(self.tab_2)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_9.addWidget(self.label_10)
        self.lineEditIp = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditIp.setObjectName("lineEditIp")
        self.horizontalLayout_9.addWidget(self.lineEditIp)
        self.lineEditIp.setFixedWidth(150)
        self.label_11 = QtWidgets.QLabel(self.tab_2)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_9.addWidget(self.label_11)
        self.lineEditPort = QtWidgets.QLineEdit(self.tab_2)
        self.lineEditPort.setObjectName("lineEditPort")
        self.horizontalLayout_9.addWidget(self.lineEditPort)
        self.pushButtonSetIpPort = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonSetIpPort.setObjectName("pushButtonSetIpPort")
        self.horizontalLayout_9.addWidget(self.pushButtonSetIpPort)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.horizontalLayout_9.setStretch(6, 1)
        self.horizontalLayout_9.setStretch(7, 3)
        self.horizontalLayout_9.setStretch(8, 1)
        self.horizontalLayout_9.setStretch(9, 1)
        self.horizontalLayout_9.setStretch(10, 2)
        self.horizontalLayout_9.setStretch(11, 3)
        self.verticalLayout_10.addLayout(self.horizontalLayout_9)
        self.gridLayout_4.addLayout(self.verticalLayout_10, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollAreaHeader = QtWidgets.QScrollArea(self.tab_2)
        self.scrollAreaHeader.setWidgetResizable(True)
        self.scrollAreaHeader.setObjectName("scrollAreaHeader")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 246, 558))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.scrollAreaHeader.setWidget(self.scrollAreaWidgetContents_3)
        self.horizontalLayout_2.addWidget(self.scrollAreaHeader)
        self.scrollArea = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea.setWidgetResizable(True)
        
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1178, 558))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_2.setStretch(1, 8)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButtonGenerate = QtWidgets.QPushButton(self.tab_2)
        self.pushButtonGenerate.setObjectName("pushButtonGenerate")
        self.horizontalLayout_5.addWidget(self.pushButtonGenerate)
        self.plainTextEditContent = QtWidgets.QPlainTextEdit(self.tab_2)
        self.plainTextEditContent.setObjectName("plainTextEditContent")
        self.horizontalLayout_5.addWidget(self.plainTextEditContent)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.verticalLayout.setStretch(0, 9)
        self.verticalLayout.setStretch(1, 1)
        self.gridLayout_4.addLayout(self.verticalLayout, 1, 0, 1, 1)
        
        self.tabWidget.addTab(self.tab_2, "")
        
        # Tab: Save and Send 
        self.SNS = saveAndSend()
        self.SNS.switch_tab_signal.connect(self.switchTabSNS)
        self.SNS.edit_message_sns_signal.connect(self.edit_message_reload_gui)
        self.SNS.ip_port_changed_signal.connect(self.ip_port_updated)
        self.SNS.default_delay_set_signal.connect(self.setDefaultDelay)
        self.SNS.default_periodic_set_signal.connect(self.setDefaultPeriodic)
        self.tabWidget.addTab(self.SNS, "")
        
        #mahaiyo
        # self.periodic_sender = saveSendPeriodic()
        # self.periodic_sender.periodic_message_selector_signal.connect(self.switchTabSNS)

        self.SNS.switch_add_periodic_tab.connect(self.periodic_message_selection)
        
        
        # Tab Create Message
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_h1 = QtWidgets.QLabel(self.tab_3)
        self.label_h1.setObjectName("label_h1")
        self.gridLayout.addWidget(self.label_h1, 0, 0, 1, 1)
        self.lineEditContent1 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditContent1.setObjectName("lineEditContent1")
        self.gridLayout.addWidget(self.lineEditContent1, 0, 1, 1, 1)
        self.pushButtonOnce1 = QtWidgets.QPushButton(self.tab_3)
        self.pushButtonOnce1.setObjectName("pushButtonOnce1")
        self.gridLayout.addWidget(self.pushButtonOnce1, 0, 2, 1, 1)
        self.lineEdit_h1 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_h1.setObjectName("lineEdit_h1")
        self.gridLayout.addWidget(self.lineEdit_h1, 0, 3, 1, 1)
        self.pushButton_h1 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_h1.setObjectName("pushButton_h1")
        self.gridLayout.addWidget(self.pushButton_h1, 0, 4, 1, 1)
        self.label_h2 = QtWidgets.QLabel(self.tab_3)
        self.label_h2.setObjectName("label_h2")
        self.gridLayout.addWidget(self.label_h2, 1, 0, 1, 1)
        self.lineEditContent2 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditContent2.setObjectName("lineEditContent2")
        self.gridLayout.addWidget(self.lineEditContent2, 1, 1, 1, 1)
        self.pushButtonOnce2 = QtWidgets.QPushButton(self.tab_3)
        self.pushButtonOnce2.setObjectName("pushButtonOnce2")
        self.gridLayout.addWidget(self.pushButtonOnce2, 1, 2, 1, 1)
        self.lineEdit_h2 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_h2.setObjectName("lineEdit_h2")
        self.gridLayout.addWidget(self.lineEdit_h2, 1, 3, 1, 1)
        self.pushButton_h2 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_h2.setObjectName("pushButton_h2")
        self.gridLayout.addWidget(self.pushButton_h2, 1, 4, 1, 1)
        self.label_h3 = QtWidgets.QLabel(self.tab_3)
        self.label_h3.setObjectName("label_h3")
        self.gridLayout.addWidget(self.label_h3, 2, 0, 1, 1)
        self.lineEditContent3 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditContent3.setObjectName("lineEditContent3")
        self.gridLayout.addWidget(self.lineEditContent3, 2, 1, 1, 1)
        self.pushButtonOnce3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButtonOnce3.setObjectName("pushButtonOnce3")
        self.gridLayout.addWidget(self.pushButtonOnce3, 2, 2, 1, 1)
        self.lineEdit_h3 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_h3.setObjectName("lineEdit_h3")
        self.gridLayout.addWidget(self.lineEdit_h3, 2, 3, 1, 1)
        self.pushButton_h3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_h3.setObjectName("pushButton_h3")
        self.gridLayout.addWidget(self.pushButton_h3, 2, 4, 1, 1)
        self.label_h4 = QtWidgets.QLabel(self.tab_3)
        self.label_h4.setObjectName("label_h4")
        self.gridLayout.addWidget(self.label_h4, 3, 0, 1, 1)
        self.lineEditContent4 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditContent4.setObjectName("lineEditContent4")
        self.gridLayout.addWidget(self.lineEditContent4, 3, 1, 1, 1)
        self.pushButtonOnce4 = QtWidgets.QPushButton(self.tab_3)
        self.pushButtonOnce4.setObjectName("pushButtonOnce4")
        self.gridLayout.addWidget(self.pushButtonOnce4, 3, 2, 1, 1)
        self.lineEdit_h4 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_h4.setObjectName("lineEdit_h4")
        self.gridLayout.addWidget(self.lineEdit_h4, 3, 3, 1, 1)
        self.pushButton_h4 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_h4.setObjectName("pushButton_h4")
        self.gridLayout.addWidget(self.pushButton_h4, 3, 4, 1, 1)
        self.label_h5 = QtWidgets.QLabel(self.tab_3)
        self.label_h5.setObjectName("label_h5")
        self.gridLayout.addWidget(self.label_h5, 4, 0, 1, 1)
        self.lineEditContent5 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditContent5.setObjectName("lineEditContent5")
        self.gridLayout.addWidget(self.lineEditContent5, 4, 1, 1, 1)
        self.pushButtonOnce5 = QtWidgets.QPushButton(self.tab_3)
        self.pushButtonOnce5.setObjectName("pushButtonOnce5")
        self.gridLayout.addWidget(self.pushButtonOnce5, 4, 2, 1, 1)
        self.lineEdit_h5 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_h5.setObjectName("lineEdit_h5")
        self.gridLayout.addWidget(self.lineEdit_h5, 4, 3, 1, 1)
        self.pushButton_h5 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_h5.setObjectName("pushButton_h5")
        self.gridLayout.addWidget(self.pushButton_h5, 4, 4, 1, 1)
        self.label_h6 = QtWidgets.QLabel(self.tab_3)
        self.label_h6.setObjectName("label_h6")
        self.gridLayout.addWidget(self.label_h6, 5, 0, 1, 1)
        self.lineEditContent6 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEditContent6.setObjectName("lineEditContent6")
        self.gridLayout.addWidget(self.lineEditContent6, 5, 1, 1, 1)
        self.pushButtonOnce6 = QtWidgets.QPushButton(self.tab_3)
        self.pushButtonOnce6.setObjectName("pushButtonOnce6")
        self.gridLayout.addWidget(self.pushButtonOnce6, 5, 2, 1, 1)
        self.lineEdit_h6 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_h6.setObjectName("lineEdit_h6")
        self.gridLayout.addWidget(self.lineEdit_h6, 5, 3, 1, 1)
        self.pushButton_h6 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_h6.setObjectName("pushButton_h6")
        self.gridLayout.addWidget(self.pushButton_h6, 5, 4, 1, 1)
        self.gridLayout.setColumnStretch(0, 3)
        self.gridLayout.setColumnStretch(1, 15)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 1)
        self.gridLayout_5.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.tab_3)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_4.addWidget(self.label_6)
        self.label_7 = QtWidgets.QLabel(self.tab_3)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_4.addWidget(self.label_7)
        self.horizontalLayout_10.addLayout(self.verticalLayout_4)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.plainTextEdit_g1_header = QtWidgets.QPlainTextEdit(self.tab_3)
        self.plainTextEdit_g1_header.setObjectName("plainTextEdit_g1_header")
        self.verticalLayout_2.addWidget(self.plainTextEdit_g1_header)
        self.plainTextEdit_g1 = QtWidgets.QPlainTextEdit(self.tab_3)
        self.plainTextEdit_g1.setObjectName("plainTextEdit_g1")
        self.verticalLayout_2.addWidget(self.plainTextEdit_g1)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 2)
        self.horizontalLayout_10.addLayout(self.verticalLayout_2)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pushButton_g1_once = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_g1_once.setObjectName("pushButton_g1_once")
        self.verticalLayout_7.addWidget(self.pushButton_g1_once)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_g1 = QtWidgets.QLabel(self.tab_3)
        self.label_g1.setObjectName("label_g1")
        self.horizontalLayout_8.addWidget(self.label_g1)
        self.lineEdit_g1 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_g1.setObjectName("lineEdit_g1")
        self.horizontalLayout_8.addWidget(self.lineEdit_g1)
        self.pushButton_g1 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_g1.setObjectName("pushButton_g1")
        self.horizontalLayout_8.addWidget(self.pushButton_g1)
        self.verticalLayout_7.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_10.addLayout(self.verticalLayout_7)
        self.horizontalLayout_10.setStretch(0, 1)
        self.horizontalLayout_10.setStretch(1, 15)
        self.horizontalLayout_10.setStretch(2, 3)
        self.verticalLayout_8.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_8 = QtWidgets.QLabel(self.tab_3)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_5.addWidget(self.label_8)
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_5.addWidget(self.label_9)
        self.horizontalLayout_11.addLayout(self.verticalLayout_5)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.plainTextEdit_g2_header = QtWidgets.QPlainTextEdit(self.tab_3)
        self.plainTextEdit_g2_header.setObjectName("plainTextEdit_g2_header")
        self.verticalLayout_3.addWidget(self.plainTextEdit_g2_header)
        self.plainTextEdit_g2 = QtWidgets.QPlainTextEdit(self.tab_3)
        self.plainTextEdit_g2.setObjectName("plainTextEdit_g2")
        self.verticalLayout_3.addWidget(self.plainTextEdit_g2)
        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 2)
        self.horizontalLayout_11.addLayout(self.verticalLayout_3)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pushButton_g2_once = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_g2_once.setObjectName("pushButton_g2_once")
        self.verticalLayout_6.addWidget(self.pushButton_g2_once)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_g2 = QtWidgets.QLabel(self.tab_3)
        self.label_g2.setObjectName("label_g2")
        self.horizontalLayout_7.addWidget(self.label_g2)
        self.lineEdit_g2 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_g2.setObjectName("lineEdit_g2")
        self.horizontalLayout_7.addWidget(self.lineEdit_g2)
        self.pushButton_g2 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_g2.setObjectName("pushButton_g2")
        self.horizontalLayout_7.addWidget(self.pushButton_g2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_11.addLayout(self.verticalLayout_6)
        self.horizontalLayout_11.setStretch(0, 1)
        self.horizontalLayout_11.setStretch(1, 15)
        self.horizontalLayout_11.setStretch(2, 3)
        self.verticalLayout_8.addLayout(self.horizontalLayout_11)
        self.gridLayout_5.addLayout(self.verticalLayout_8, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_3, "")
        
        # Tab: More Options
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.API_button = QtWidgets.QPushButton(self.tab_4)
        self.API_button.setObjectName("API_button")
        self.horizontalLayout_12.addWidget(self.API_button)
        self.pushButtonMore2 = QtWidgets.QPushButton(self.tab_4)
        self.pushButtonMore2.setObjectName("pushButtonMore2")
        self.horizontalLayout_12.addWidget(self.pushButtonMore2)
        self.pushButtonMore3 = QtWidgets.QPushButton(self.tab_4)
        self.pushButtonMore3.setObjectName("pushButtonMore3")
        self.horizontalLayout_12.addWidget(self.pushButtonMore3)
        self.pushButtonMore4 = QtWidgets.QPushButton(self.tab_4)
        self.pushButtonMore4.setObjectName("pushButtonMore4")
        self.horizontalLayout_12.addWidget(self.pushButtonMore4)
        self.pushButtonMore5 = QtWidgets.QPushButton(self.tab_4)
        self.pushButtonMore5.setObjectName("pushButtonMore5")
        self.horizontalLayout_12.addWidget(self.pushButtonMore5)
        self.pushButtonMore6 = QtWidgets.QPushButton(self.tab_4)
        self.pushButtonMore6.setObjectName("pushButtonMore6")
        self.horizontalLayout_12.addWidget(self.pushButtonMore6)
        self.pushButtonMore7 = QtWidgets.QPushButton(self.tab_4)
        self.pushButtonMore7.setObjectName("pushButtonMore7")
        self.horizontalLayout_12.addWidget(self.pushButtonMore7)
        self.pushButtonMore8 = QtWidgets.QPushButton(self.tab_4)
        self.pushButtonMore8.setObjectName("pushButtonMore8")
        self.horizontalLayout_12.addWidget(self.pushButtonMore8)
        self.pushButtonMore9 = QtWidgets.QPushButton(self.tab_4)
        self.pushButtonMore9.setObjectName("pushButtonMore9")
        self.horizontalLayout_12.addWidget(self.pushButtonMore9)
        self.pushButtonMore10 = QtWidgets.QPushButton(self.tab_4)
        self.pushButtonMore10.setObjectName("pushButtonMore10")
        self.horizontalLayout_12.addWidget(self.pushButtonMore10)
        self.gridLayout_6.addLayout(self.horizontalLayout_12, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_4, "")
        self.gridLayout_3.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        ##################################################################################################
        self.API_button.clicked.connect(api_invoke)
        self.pushButton_h1.clicked.connect(self.h1_clicked)
        self.pushButton_h2.clicked.connect(self.h2_clicked)
        self.pushButton_h3.clicked.connect(self.h3_clicked)
        self.pushButton_h4.clicked.connect(self.h4_clicked)
        self.pushButton_h5.clicked.connect(self.h5_clicked)
        self.pushButton_h6.clicked.connect(self.h6_clicked)
        self.pushButton_g1.clicked.connect(self.g1_clicked)
        self.pushButton_g2.clicked.connect(self.g2_clicked)
        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.send_h1)
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.send_h2)
        self.timer3 = QtCore.QTimer()
        self.timer3.timeout.connect(self.send_h3)
        self.timer4 = QtCore.QTimer()
        self.timer4.timeout.connect(self.send_h4)
        self.timer5 = QtCore.QTimer()
        self.timer5.timeout.connect(self.send_h5)
        self.timer6 = QtCore.QTimer()
        self.timer6.timeout.connect(self.send_h6)
        self.timer_g1 = QtCore.QTimer()
        self.timer_g1.timeout.connect(self.send_g1)
        self.timer_g2 = QtCore.QTimer()
        self.timer_g2.timeout.connect(self.send_g2)
        
        # self.pushButtonLoadValues.clicked.connect(self.loadOnButtonClicked)
        self.pushButtonClearValues.clicked.connect(self.clearOnBUttonClicked)
        
        self.timer_selected_messages = QtCore.QTimer()
        self.timer_selected_messages.timeout.connect(self.send_selected_clicked)
        
        self.pushButton_g1_once.clicked.connect(self.send_g1)
        self.pushButton_g2_once.clicked.connect(self.send_g2)
        
        self.pushButton_h1.setCheckable(True)
        self.pushButton_h1.setChecked(False)
        self.pushButton_h2.setCheckable(True)
        self.pushButton_h2.setChecked(False)
        self.pushButton_h3.setCheckable(True)
        self.pushButton_h3.setChecked(False)
        self.pushButton_h4.setCheckable(True)
        self.pushButton_h4.setChecked(False)
        self.pushButton_h5.setCheckable(True)
        self.pushButton_h5.setChecked(False)
        self.pushButton_h6.setCheckable(True)
        self.pushButton_h6.setChecked(False)
        self.pushButton_g1.setCheckable(True)
        self.pushButton_g1.setChecked(False)
        self.pushButton_g2.setCheckable(True)
        self.pushButton_g2.setChecked(False)
        self.lineEdit_g1.setText(str(200))
        self.lineEdit_g2.setText(str(200))
        self.lineEdit_h1.setText(str(200))
        self.lineEdit_h2.setText(str(200))
        self.lineEdit_h3.setText(str(200))
        self.lineEdit_h4.setText(str(200))
        self.lineEdit_h5.setText(str(200))
        self.lineEdit_h6.setText(str(200))
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.send_clicked)
        self.senderUDP = UdpSender()
        self.pushButtonSetIpPort.clicked.connect(self.set_IP_and_socket)
        self.pushButtonPeriodic.clicked.connect(self.periodic_clicked)
        self.pushButtonSendSelectNext.clicked.connect(self.send_selected_peridocally_clicked)
        
        self.pushButtonSend.clicked.connect(self.send_clicked)
        self.pushButtonGenerate.clicked.connect(self.generate_clicked)
        self.pushButtonLoad.clicked.connect(self.load_clicked)
        self.pushButtonSendSelected.clicked.connect(self.send_selected_clicked)
        self.pushButtonPeriodic.setCheckable(True)
        self.pushButtonPeriodic.setChecked(False)
        self.pushButtonSendSelectNext.setCheckable(True)
        self.pushButtonSendSelectNext.setChecked(False)

        self.lineEditTime.setText(str(500))
        self.lineEdit.setText(str(500))#periodic time ms in player tab
        self.load_message()
        # self.comboBoxMessages.currentTextChanged.connect(self.comboBoxMessageChanged)
        self.comboBoxMessages.activated[str].connect(self.comboBoxMessageChanged)
        
        self.container = QtWidgets.QWidget()
        self.containerLayout = QtWidgets.QVBoxLayout()
        self.containerLayout.setSpacing(5)
        self.containerLayout.setContentsMargins(0,0,0,0)
        # self.containerLayout.setColumnStretch(0, 7)
        # self.containerLayout.setColumnStretch(1, 1)
        # self.containerLayout.setColumnStretch(2, 1)
        # self.containerLayout.setColumnStretch(3, 7)
        self.container.setLayout(self.containerLayout)
        self.scrollArea.setWidget(self.container)
        self.listCheckBox = []
        self.listLabels = []
        self.listLineEdits = []
        self.header_labels = []
        self.header_lineEdit = []
        self.listDyanamicVaribleButton = []
        self.listDyanamicRemoveButton = []
        self.listExpandButton = []
        self.listisExpand = []
        self.attr_stuct_details = []
        self.headerLabels = config.header_labels

        self.selected_byte_msg_formats = []
        self.modified_selected_byte_msg_formats = []
        self.selected_msg_bit_lengths = []
        self.header_value = []
        self.struct_stack = []
        # self.repeating_structs_names_list = []
        
        self.columns = 6
        self.rows = int(len(self.listCheckBox) / self.columns)
        self.lineEditIp.setText(config.sock_send_ip)
        self.lineEditPort.setText(config.sock_send_port)

        self.comboBoxMessages.setEditable(True)
        self.comboBoxMessages.setInsertPolicy(QtWidgets.QComboBox.NoInsert)#prevents insertion of search text
        self.comboBoxMessages.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

        self.tableWidgetMessages.setColumnCount(3)
        self.tableWidgetMessages.setColumnWidth(0, 170)
        self.tableWidgetMessages.setColumnWidth(1, 200)
        self.tableWidgetMessages.setColumnWidth(2, 1080)
        
        self.strucChkBox = QtWidgets.QCheckBox('val')
        
        
        # creating left header items (reminder seperate function is better)
        self.containerLayoutHeader = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_3)
        # labels_list = config.header_labels
        # rowCount = 0
        # for i,x in enumerate(labels_list):
        #     label = QtWidgets.QLabel()
        #     label.setText(x)
        #     lineEdit = QtWidgets.QLineEdit()
        #     lineEdit.setFixedWidth(70)
        #     containerLayoutHeader.addWidget(label, rowCount, 0, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        #     containerLayoutHeader.addWidget(lineEdit, rowCount, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        #     rowCount = rowCount + 1
            
        # self.lineEditHeader.setEnabled(False)
        generate_dyanamic_data("config/message_details.xlsx")
        self.dyanamicStructre, self.dynamicAttributesIrs = loadDyanamic_data("dyanmaic_data.json","dyanmaic_irs.json")
        
        
        self.reload_gui()
        

        self.searchMessageFields = QtWidgets.QLineEdit(self.tab_2)
        self.searchMessageFields.setObjectName("searchMessageFields")
        self.searchMessageFields.setPlaceholderText("Search")
        #self.searchMessageFields.setText("Search")
        self.horizontalLayout_9.addWidget(self.searchMessageFields)
        self.searchMessageFields.textChanged.connect(self.searchMessage)
        
        
        
        
        # self.listLineEdits.textChanged.connect(self.dynamicLength)
        
        # self.pushButtonExtra3.setEnabled(True)
        # self.pushButtonExtra3.clicked.connect(self.open_receiver)
        ######################################################################################################
        
        ######################################################################################################
        self.pushButtonSaveEdit.clicked.connect(lambda: self.save_edit_clicked(self.pushButtonSaveEdit.text().upper()))
        
        
        
        ################################## SNS VARIBLE #################################################
        self.currentSNSEditMsdID = -1
        self.tabWidget.currentChanged.connect(self.onTabChanged)
        self.tabWidget.setCurrentIndex(1)
        # self.switchTabSNS(1, "", "tabs", False)
        self.backButton.back_clicked_signal.connect(self.backClicked)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sender"))
        self.pushButtonLoad.setText(_translate("MainWindow", "Load Messages"))
        self.checkBoxTimestampUpdated.setText(_translate("MainWindow", "Send Timestamp Updated"))
        self.pushButtonSendSelected.setText(_translate("MainWindow", "Send Selected Once"))
        self.label_3.setText(_translate("MainWindow", "Periodicity(ms)"))
        self.pushButtonSendSelectNext.setText(_translate("MainWindow", "Send Selected Periodically"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Player"))
        self.label.setText(_translate("MainWindow", "Select Msg"))
        # self.label_2.setText(_translate("MainWindow", "Header"))
        self.DelayLabel.setText(_translate("MainWindow", "Delay(ms)"))
        self.pushButtonSaveEdit.setText(_translate("MainWindow", "SAVE"))
        self.pushButtonSend.setText(_translate("MainWindow", "Send"))
        self.label_5.setText(_translate("MainWindow", "Periodicity(ms)"))
        self.pushButtonPeriodic.setText(_translate("MainWindow", "Periodic"))
        #mahaiyo
        self.pushButtonAddPeriodicMessage.setText(_translate("MainWindow", "Add"))
        
        self.pushButtonClearValues.setText(_translate("MainWindow", "Clear Values"))
        self.pushButtonSaveValues.setText(_translate("MainWindow", "Save Values"))
        self.pushButtonLoadValues.setText(_translate("MainWindow", "Load Values"))
        self.pushButtonExtra1.setText(_translate("MainWindow", "Set Dynamic Length"))
        self.pushButtonExtra2.setText(_translate("MainWindow", "Extra2"))
        self.pushButtonExtra3.setText(_translate("MainWindow", "Extra3"))
        self.label_10.setText(_translate("MainWindow", "Ip"))
        self.label_11.setText(_translate("MainWindow", "Port"))
        self.pushButtonSetIpPort.setText(_translate("MainWindow", "Set Ip Port"))
        self.pushButtonGenerate.setText(_translate("MainWindow", "Generate"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Sender"))
        self.label_h1.setText(_translate("MainWindow", "Message 1"))
        self.pushButtonOnce1.setText(_translate("MainWindow", "Send Once"))
        self.lineEdit_h1.setText(_translate("MainWindow", "500"))
        self.pushButton_h1.setText(_translate("MainWindow", "Periodic"))
        self.label_h2.setText(_translate("MainWindow", "Message 2"))
        self.pushButtonOnce2.setText(_translate("MainWindow", "Send Once"))
        self.lineEdit_h2.setText(_translate("MainWindow", "500"))
        self.pushButton_h2.setText(_translate("MainWindow", "Periodic"))
        self.label_h3.setText(_translate("MainWindow", "Message 3"))
        self.pushButtonOnce3.setText(_translate("MainWindow", "Send Once"))
        self.lineEdit_h3.setText(_translate("MainWindow", "500"))
        self.pushButton_h3.setText(_translate("MainWindow", "Periodic"))
        self.label_h4.setText(_translate("MainWindow", "Message 4"))
        self.pushButtonOnce4.setText(_translate("MainWindow", "Send Once"))
        self.lineEdit_h4.setText(_translate("MainWindow", "500"))
        self.pushButton_h4.setText(_translate("MainWindow", "Periodic"))
        self.label_h5.setText(_translate("MainWindow", "Message 5"))
        self.pushButtonOnce5.setText(_translate("MainWindow", "Send Once"))
        self.lineEdit_h5.setText(_translate("MainWindow", "500"))
        self.pushButton_h5.setText(_translate("MainWindow", "Periodic"))
        self.label_h6.setText(_translate("MainWindow", "Message 6"))
        self.pushButtonOnce6.setText(_translate("MainWindow", "Send Once"))
        self.lineEdit_h6.setText(_translate("MainWindow", "500"))
        self.pushButton_h6.setText(_translate("MainWindow", "Periodic"))
        self.label_6.setText(_translate("MainWindow", "Format"))
        self.label_7.setText(_translate("MainWindow", "Value"))
        self.pushButton_g1_once.setText(_translate("MainWindow", "Send Once"))
        self.label_g1.setText(_translate("MainWindow", "Time ms"))
        self.pushButton_g1.setText(_translate("MainWindow", "Periodic"))
        self.label_8.setText(_translate("MainWindow", "Format"))
        self.label_9.setText(_translate("MainWindow", "Value"))
        self.pushButton_g2_once.setText(_translate("MainWindow", "Send Once"))
        self.label_g2.setText(_translate("MainWindow", "Time ms"))
        self.pushButton_g2.setText(_translate("MainWindow", "Periodic"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Create Message"))
        self.API_button.setText(_translate("MainWindow", "API GUI INVOKE"))
        self.pushButtonMore2.setText(_translate("MainWindow", "2"))
        self.pushButtonMore3.setText(_translate("MainWindow", "3"))
        self.pushButtonMore4.setText(_translate("MainWindow", "4"))
        self.pushButtonMore5.setText(_translate("MainWindow", "5"))
        self.pushButtonMore6.setText(_translate("MainWindow", "6"))
        self.pushButtonMore7.setText(_translate("MainWindow", "7"))
        self.pushButtonMore8.setText(_translate("MainWindow", "8"))
        self.pushButtonMore9.setText(_translate("MainWindow", "9"))
        self.pushButtonMore10.setText(_translate("MainWindow", "10"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "More Options"))
        # self.pushButtonExtra3.setText("Open Receiver")
        
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SNS), _translate("MainWindow", "SNS"))


    def setDefaultDelay(self, value):
        global GLOBAL_DELAY 
        GLOBAL_DELAY = value
        self.delayLineEdit.setText(str(GLOBAL_DELAY))
        
    def setDefaultPeriodic(self, value):
        global GLOBAL_PERIODIC
        GLOBAL_PERIODIC = value  
        self.lineEditTime.setText(str(GLOBAL_PERIODIC))


    def set_IP_and_socket(self):
        print("IP",self.lineEditIp.text())
        print("Port",self.lineEditPort.text())
        config.sock_send_ip = self.lineEditIp.text()
        config.sock_send_port = self.lineEditPort.text()
        print("IP & Port Set")


    def ip_port_updated(self):
        self.lineEditIp.setText(config.sock_send_ip)
        self.lineEditPort.setText(str(config.sock_send_port))
        
        
    def comboBoxMessageChanged(self):
        config.message_selected = self.comboBoxMessages.currentText()
        print('msgSelected ',config.message_selected)
        # self.stop_periodic_sending_if_on()

        self.reload_gui()


        # for index in range(len(self.dict_index)):
        #     if(self.dict_index[index][2] != ''):
        #         self.struct_stack.append(self.dict_index[index][2])

        # print("Stack",self.struct_stack)

    def clearOnBUttonClicked(self):
        for lineEdit in (self.listLineEdits):
            lineEdit.setText(str(0))
    
    def dynamicLength(self):
        if(self.strucChkBox.isChecked()):
            print("Line edit Value",self.listLineEdits[1].text())
        # print("The Length",text)
        
    def loadOnButtonClicked(self):
        print("Load Button clicked")
        msg_content = csv_dict[f'{config.message_selected}']
        
        if self.comboBoxLoadValues.currentText() == "Load value 1": 
            for i,x in enumerate(self.listLineEdits):
                if i == 4 or i == 5:  #not filling the msg ID and msg LEN feild
                    continue
                else :
                    x.setText("1")
        if self.comboBoxLoadValues.currentText() == "Load value From Sheet":
            for i,x in enumerate(self.listLineEdits):
                if i == 4 or i == 5:  #not filling the msg ID and msg LEN feild
                    continue
                else :
                    # print("Msg Contents",msg_content[i][4])
                    x.setText(str(int(msg_content[i][4])))

    def h1_clicked(self):
        if self.pushButton_h1.isChecked():
            self.pushButton_h1.setText("Stop")
            self.timer1.start(int(self.lineEdit_h1.text()))
        else:
            self.pushButton_h1.setText("Start")
            self.timer1.stop()
            
    def h2_clicked(self):
        if self.pushButton_h2.isChecked():
            self.pushButton_h2.setText("Stop")
            self.timer2.start(int(self.lineEdit_h2.text()))
        else:
            self.pushButton_h2.setText("Start")
            self.timer2.stop()    
            
    def h3_clicked(self):
        if self.pushButton_h3.isChecked():
            self.pushButton_h3.setText("Stop")
            self.timer3.start(int(self.lineEdit_h3.text()))
        else:
            self.pushButton_h3.setText("Start")
            self.timer3.stop()
            
    def h4_clicked(self):
        if self.pushButton_h4.isChecked():
            self.pushButton_h4.setText("Stop")
            self.timer4.start(int(self.lineEdit_h4.text()))
        else:
            self.pushButton_h4.setText("Start")
            self.timer4.stop()  
            
    def h5_clicked(self):
        if self.pushButton_h5.isChecked():
            self.pushButton_h5.setText("Stop")
            self.timer5.start(int(self.lineEdit_h5.text()))
        else:
            self.pushButton_h5.setText("Start")
            self.timer5.stop()
            
    def h6_clicked(self):
        if self.pushButton_h6.isChecked():
            self.pushButton_h6.setText("Stop")
            self.timer6.start(int(self.lineEdit_h6.text()))
        else:
            self.pushButton_h6.setText("Start")
            self.timer6.stop() 
            
    def g1_clicked(self):
        if self.pushButton_g1.isChecked():
            self.pushButton_g1.setText("Stop")
            self.timer_g1.start(int(self.lineEdit_g1.text()))
        else:
            self.pushButton_g1.setText("Start")
            self.timer_g1.stop()
            
    def g2_clicked(self):
        if self.pushButton_g2.isChecked():
            self.pushButton_g2.setText("Stop")
            self.timer_g2.start(int(self.lineEdit_g2.text()))
        else:
            self.pushButton_g2.setText("Start")
            self.timer_g2.stop()             

    def periodic_clicked(self):
        if self.pushButtonPeriodic.isChecked():
            self.pushButtonPeriodic.setText("Periodic Stop")
            self.timer.start(int(self.lineEditTime.text()))
            print('Periodic Started')
        else:
            self.pushButtonPeriodic.setText("Periodic Start")
            self.timer.stop()
            print('Periodic Stopped')
            
    def send_selected_peridocally_clicked(self):
        if self.pushButtonSendSelectNext.isChecked():
            self.pushButtonSendSelectNext.setText("Periodic Stop")
            self.timer_selected_messages.start(int(self.lineEdit.text()))
            print('Periodic Started')
        else:
            self.pushButtonSendSelectNext.setText("Periodic Start")
            self.timer_selected_messages.stop()
            print('Periodic Stopped')             

    def send_Clicked_three_times(self):
        # t = 50
        # while t:
        #     mins, secs = divmod(t, 60)
        #     timer = '{:02d}:{:02d}'.format(mins, secs) 
        #     print(timer, end="\r") 
        #     time.sleep(1) 
        #     t -= 1
        for i in range(3):
            print(i)
            self.send_clicked()
            time.sleep(0.2)
     
    def send_h1(self):
        print('send_CBI_VDUS')  
        datetime_now = datetime.datetime.now()
        header_list = [0] * 8
        header_list[0]  = datetime_now.day
        header_list[1]  = datetime_now.month
        header_list[2] = datetime_now.year
        header_list[3] = datetime_now.hour
        header_list[4] = datetime_now.minute
        header_list[5] = datetime_now.second
        header_list[6] = math.floor(datetime_now.microsecond / 1000)
        header_list[7] = 1
        header_tuple = tuple(header_list)
        packet = struct.pack('=BBBBBBHHBBHBBBHL',102,8,1,102,10,25,23,1,*header_tuple)
        self.senderUDP.send_packet(packet)
  
    def send_h2(self):
        print('send_VDUS_CBI')  
        datetime_now = datetime.datetime.now()
        header_list = [0] * 8
        header_list[0]  = datetime_now.day
        header_list[1]  = datetime_now.month
        header_list[2] = datetime_now.year
        header_list[3] = datetime_now.hour
        header_list[4] = datetime_now.minute
        header_list[5] = datetime_now.second
        header_list[6] = math.floor(datetime_now.microsecond / 1000)
        header_list[7] = 1
        header_tuple = tuple(header_list)
        packet = struct.pack('=BBBBBBHHBBHBBBHL',102,10,1,102,8,21,23,1,*header_tuple)
        self.senderUDP.send_packet(packet)

    def send_h3(self):
        print('send_MT_CBI_HEALTH') 
        datetime_now = datetime.datetime.now()
        header_list = [0] * 8
        header_list[0]  = datetime_now.day
        header_list[1]  = datetime_now.month
        header_list[2] = datetime_now.year
        header_list[3] = datetime_now.hour
        header_list[4] = datetime_now.minute
        header_list[5] = datetime_now.second
        header_list[6] = math.floor(datetime_now.microsecond / 1000)
        header_list[7] = 1
        header_tuple = tuple(header_list)
        packet = struct.pack('=BBBBBBHHBBHBBBHL',102,10,1,102,8,19,23,1,*header_tuple)
        self.senderUDP.send_packet(packet)     
        
    def send_h4(self):
        print('send_h4') 
        print('send_MT_VDUS_HEALTH') 
        datetime_now = datetime.datetime.now()
        header_list = [0] * 8
        header_list[0]  = datetime_now.day
        header_list[1]  = datetime_now.month
        header_list[2] = datetime_now.year
        header_list[3] = datetime_now.hour
        header_list[4] = datetime_now.minute
        header_list[5] = datetime_now.second
        header_list[6] = math.floor(datetime_now.microsecond / 1000)
        header_list[7] = 1
        header_tuple = tuple(header_list)
        packet = struct.pack('=BBBBBBHHBBHBBBHL',102,10,1,102,8,21,23,1,*header_tuple)
        self.senderUDP.send_packet(packet)
        
    def send_h5(self):
        print('send_h5')
        print('send__HEALTH') 
        datetime_now = datetime.datetime.now()
        header_list = [0] * 8
        header_list[0]  = datetime_now.day
        header_list[1]  = datetime_now.month
        header_list[2] = datetime_now.year
        header_list[3] = datetime_now.hour
        header_list[4] = datetime_now.minute
        header_list[5] = datetime_now.second
        header_list[6] = math.floor(datetime_now.microsecond / 1000)
        header_list[7] = 1
        header_tuple = tuple(header_list)
        packet = struct.pack('=BBBBBBHHBBHBBBHL',102,10,1,102,8,19,23,1,*header_tuple)
        self.senderUDP.send_packet(packet)      
        
    def send_h6(self):
        print('send_h6') 

    def send_g1(self):
        print('send_g1') 
        
        format_string = self.plainTextEdit_g1_header.toPlainText()
        
        item_content_text = self.plainTextEdit_g1.toPlainText()
        value_list = []
        for value in item_content_text.split(','):
            if value.isdigit():
                value = int(value)
            else:
                value = bytes(value, 'utf-8')
            value_list.append( value )  
        datetime_now = datetime.datetime.now()
        unique_message_code = 1
        value_list[8]  = datetime_now.day
        value_list[9]  = datetime_now.month
        value_list[10] = datetime_now.year
        value_list[11] = datetime_now.hour
        value_list[12] = datetime_now.minute
        value_list[13] = datetime_now.second
        value_list[14] = math.floor(datetime_now.microsecond / 1000)
        value_list[15] = unique_message_code    
        print('value list', value_list)    
        packet = struct.pack(f'={format_string}', *tuple(value_list))
        self.senderUDP.send_packet(packet)
        
    def send_g2(self):
        print('send_g2')  
        format_string = self.plainTextEdit_g2_header.toPlainText()
        
        item_content_text = self.plainTextEdit_g2.toPlainText()
        value_list = []
        for value in item_content_text.split(','):
            if value.isdigit():
                value = int(value)
            else:
                value = bytes(value, 'utf-8')
            value_list.append( value )  
        datetime_now = datetime.datetime.now()
        unique_message_code = 1
        value_list[8]  = datetime_now.day
        value_list[9]  = datetime_now.month
        value_list[10] = datetime_now.year
        value_list[11] = datetime_now.hour
        value_list[12] = datetime_now.minute
        value_list[13] = datetime_now.second
        value_list[14] = math.floor(datetime_now.microsecond / 1000)
        value_list[15] = unique_message_code    
        print('value list', value_list)    
        packet = struct.pack(f'={format_string}', *tuple(value_list))
        self.senderUDP.send_packet(packet)
         
    def get_header_list(self): 	
        header_list = []     
        if config.name_to_header_type[config.message_selected] == 'external':
            for child in self.scrollAreaWidgetContents_3.findChildren(QtWidgets.QWidget):
                if isinstance(child, QtWidgets.QLineEdit):
                    header_list.append(int(child.text()))
                else:
                    pass
            return header_list       	
        else:
            for child in self.scrollAreaWidgetContents_3.findChildren(QtWidgets.QWidget):
                if isinstance(child, QtWidgets.QLineEdit):
                    header_list.append(int(child.text()))
                else:
                    pass
            datetime_now = datetime.datetime.now()
            unique_message_code = 1
      		# header_string = self.lineEditHeader.text()
      		# header_list = [0] * 16
      		# header_list = [int(i) for i in header_string.split(" ")]
            header_list[8]  = datetime_now.day
            header_list[9]  = datetime_now.month
      	       # header_list[9] = 10
            header_list[10] = datetime_now.year
            header_list[11] = datetime_now.hour
            header_list[12] = datetime_now.minute
            header_list[13] = datetime_now.second
            header_list[14] = math.floor(datetime_now.microsecond / 1000)
            header_list[15] = unique_message_code
            # print('header_list = ', header_list)
            return header_list
        
    def get_num_records_and_records_list(self):
        records = []
        maxRecords = 128
        records = [0] * maxRecords
        byteCount = 0
        bitCount = 0
        maxByteCount = 0
        setBitList = []
        max_no_of_records = 0
        atleast_a_bit_set = False
        for i,checkBox in enumerate(self.listCheckBox):
            val = 0
            if checkBox.isChecked():
                val = 1
                setBitList.append(i)
                maxByteCount = byteCount
                atleast_a_bit_set = True
                records[byteCount] = self.set_bit( records[byteCount], bitCount, val)
            # print("Byte value = ",records[byteCount])
            bitCount = bitCount + 1
            if (bitCount == 8):
                # print("Byte value = ",records[byteCount])
                byteCount = byteCount + 1
                bitCount = 0
        if atleast_a_bit_set:
            max_no_of_records = maxByteCount + 1
        return max_no_of_records, records  
    
    def get_list_set_bit_list(self):
        selected_bit_list = []
        for i,checkBox in enumerate(self.listCheckBox):
            if checkBox.isChecked():
                selected_bit_list.append(i)

        message_num = 0
        bit_list = []
        list_of_bit_lists = []
        start_bit_for_next_msg = -1
        
        for i,bit_num in enumerate(selected_bit_list):
            print('Index i = ', i,' ############### For Bit Num ', bit_num)
            updated_message_num = math.floor(bit_num / 1024)
            print(' ------------------>>>>>>>>>> updated_message_num = ', updated_message_num)
            print('bit list : ', bit_list)
            if (message_num < updated_message_num):
                print('Changing msg number to ',updated_message_num)
                difference_of_msg_num = updated_message_num - message_num
                message_num = updated_message_num
                start_bit_for_next_msg = bit_num
                list_of_bit_lists.append(bit_list.copy())
                bit_list.clear()
                if difference_of_msg_num > 1:
                    for p in range(difference_of_msg_num - 1):
                        list_of_bit_lists.append([])
                bit_list.append(start_bit_for_next_msg)
            else:
                print('Message_Num = ',message_num,', Appending to bit list = ',bit_num)
                bit_list.append(bit_num)
            if (i == len(selected_bit_list) - 1 ):
                list_of_bit_lists.append(bit_list.copy())    
        print(list_of_bit_lists)  
        return list_of_bit_lists
    
    def send_and_log_message_and_update_gui(self, form, content_list):
        #if config.message_selected == "PSD_RATC_INFO_MSG":
        #    print(">>>>>>>>>>>>>>", form, header_list, content_list)
        #    form = "BBBHBIII"
        #    packet = struct.pack(f'={form}', *tuple(content_list))
        #else:
        print("-------",form,content_list)
        packet = struct.pack(f'={form}', *tuple(content_list))
        self.senderUDP.send_packet(packet)
    
        if config.name_to_header_type[config.message_selected] != 'external':
            print("================================")
            
            # header_str = ' '.join(map(str,header_list))
            content_str = ' '.join(map(str, self.getStringifiedMsgList(content_list)))
            # self.update_header(header_str) 
            self.update_content(content_str) 
            config.log(f'{config.message_selected}{content_str}')
        return

    def calculateByte(self,non_standard_bits_values, non_standard_bits_sizes):
        # print(">>>non_standard_bits_values", non_standard_bits_values, non_standard_bits_sizes)
        # print(">>> reversed", reversed(non_standard_bits_values), reversed(non_standard_bits_sizes))
        # print(">>> zip reversed", zip(reversed(non_standard_bits_values), reversed(non_standard_bits_sizes)))
        if sum(non_standard_bits_sizes) != 8:
            raise ValueError('Total bit size must be 8')
        packed_byte = 0
        current_bit_index = 8
        
        for number, size in zip(reversed(non_standard_bits_values), reversed(non_standard_bits_sizes)):
            if number >= (1 << int(size)):
                errorDisplay.show(self.centralwidget, f"Bit Value {number} exceeds the maximum value for bit-size {size}")
                return -1
                # error = raise ValueError(f'Number {number} exceeds maximum value for bit size {size}')
            else:
                current_bit_index -= size
                packed_byte |= (number << current_bit_index)
                
        return packed_byte
    
    def show_error_message(self, error_message):     
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText('Error In Sending')
        msg.setInformativeText(error_message)
        msg.setWindowTitle('Error')
        msg.exec_()
  
    def generate_clicked(self):
        try:
            self.set_IP_and_socket()
            header_format = config.header_dictionary[config.message_selected]
            content_format_list = config.modified_content_dictionary[config.message_selected] 
            content_format = ' '.join(map(str,content_format_list[:-1]))
            if(content_format == 'not' or content_format == ' '):
                content_format = ''
            crc_format = config.crc_dictionary[config.message_selected]
            if(crc_format == 'not'  or crc_format == ' '):
                crc_format = ''
            print('header_format:', header_format, ', content_format:', content_format, ', crc_format:',crc_format)    
            bits_format = config.bits_dictionary[config.message_selected]
            header_list = []
            content_list = []
            crc_data = 0
    
            if bits_format == 'indication_bits':
                header_list = header_list + self.get_header_list()
                max_byte_number, records_list = self.get_num_records_and_records_list()
                content_list.append(max_byte_number)
                content_list = content_list + records_list
                crcPack = struct.pack(f'={header_format} {content_format}', *tuple(header_list), *tuple(content_list)) #for CRC on header
                crcPack = struct.pack(f'= {content_format}', *tuple(content_list))
                crc_data = crc_calulator.crc_32(crcPack)
                content_list.append(crc_data)
                
                # self.send_and_log_message_and_update_gui(header_format+content_format+crc_format, header_list, content_list)
                
            elif bits_format == 'bytes':
                header_list = header_list + self.get_header_list()
                value_list = []
                format_list = config.content_dictionary[config.message_selected]
                for i,lineEdit in enumerate(self.listLineEdits):
                    value = lineEdit.text()
                    if 's' in format_list[i]:
                        value = bytes(value, 'utf-8')
                    elif value == '' or value == ' ':
                        # print('empty value')
                        value = 0
                    elif value == 'auto':
                        value = 'auto'    
                    else: 
                        value = int(value)    
                    value_list.append( value )
                    
                sizeForByte = 0
                modified_value_list = []
                non_standard_bits_values = []
                non_standard_bits_sizes = []
                bit_length_list = config.bits_list_dictionary[config.message_selected]
                for y,b in enumerate(bit_length_list):
                    # print('b = ', b)
                    if b >= 8 :
                        modified_value_list.append(value_list[y])
                    else:
                        sizeForByte = sizeForByte + b
                        non_standard_bits_values.append(value_list[y])
                        non_standard_bits_sizes.append(b)
                        if sizeForByte == 8:
                            # print('byte complete......')
                            sizeForByte = 0
                            byteValue = self.calculateByte(non_standard_bits_values, non_standard_bits_sizes)

                            # print('byte = ',byteValue, 'bits:',bin(byteValue))
                            modified_value_list.append(byteValue)
                            non_standard_bits_values.clear()
                            non_standard_bits_sizes.clear()
                # print('selected_byte_msg_formats: ', self.selected_byte_msg_formats)             
                # print('modified_selected_byte_msg_formats: ', self.modified_selected_byte_msg_formats)            
                # print('modified_value_list = ',modified_value_list)
                # print('modified_content_format : ',modified_content_format)
                content_list = modified_value_list[:-1]
                # print('content_list : ',content_list)
                crcPack = struct.pack(f'={header_format} {content_format}', *tuple(header_list), *tuple(content_list)) # for CRC on header
                # #crcPack = struct.pack(f'= {content_format}', *tuple(content_list))
                crc_data = crc_calulator.crc_32(crcPack)
                # content_list.append(crc_data)
                # self.send_and_log_message_and_update_gui(header_format+content_format+crc_format, header_list, content_list)
        except Exception as e:
            self.stop_periodic_sending_if_on()
            self.show_error_message(str(e))
     
        header_str = ' '.join(map(str,header_list))
        content_str = ' '.join(map(str,self.getStringifiedMsgList(content_list)))
        for k,content_val in enumerate(content_list):
            if type(content_val) == bytes:
                content_val = content_val.decode()
                content_list[k] = content_val
        delim = ","
        commafied_header_str = str(delim.join(list(map(str, header_list))))
        commafied_content_str = str(delim.join(list(map(str, content_list))))
        
        if crc_data == 0:
            crc_str = ''
        else:
            crc_str = str(crc_data)
        content_str += f' {crc_str}'
        # commafied_content_str += ','+crc_str
        self.update_content(header_str+' '+content_str) 
        self.plainTextEdit_g1_header.setPlainText(header_format+' '+content_format+' '+crc_format)
        if len(content_list) == 0:
            self.plainTextEdit_g1.setPlainText(commafied_header_str+','+crc_str)
            self.save_message_in_load_file(header_format+' '+content_format+' '+crc_format, f'{commafied_header_str},{crc_str}')
        else:
            self.plainTextEdit_g1.setPlainText(commafied_header_str+','+commafied_content_str+','+crc_str)
            self.save_message_in_load_file(header_format+' '+content_format+' '+crc_format, f'{commafied_header_str},{commafied_content_str},{crc_str}')
   
    def save_message_in_load_file(self, msg_format, msg_content):
        print('save_message_in_load_file')
        msg_name, done = QtWidgets.QInputDialog.getText(None, 'Input Dialog', 'Save Message As : ')
        if done:
            print('msg_name:', msg_name,' msg_format:',msg_format, ' msg_content:', msg_content)
            config.write_saved_messages(msg_name, msg_format, msg_content)
            
    def send_selected_clicked(self):
        selected_items = self.tableWidgetMessages.selectedItems()
        selected_rows = set(item.row() for item in selected_items)
        print('selected_rows: ', selected_rows)
        
        for row in selected_rows:
            format_string = self.tableWidgetMessages.item(row, 1).text()
            item_content_text = self.tableWidgetMessages.item(row, 2).text()
            value_list = []
            for value in item_content_text.split(','):
                if value.isdigit():
                    value = int(value)
                else:
                    value = bytes(value, 'utf-8')
                value_list.append( value )
            packet = struct.pack(f'={format_string}', *tuple(value_list))
            if self.checkBoxTimestampUpdated.isChecked():
                print('Sending after updating time...')
                packet = self.get_time_crc_updated_packet(packet)
            self.senderUDP.send_packet(packet)
         
    def load_clicked(self):
        print('load_clicked')   
        row = 0                 
        for i,saved_msg_name in enumerate(config.saved_msg_names):
            saved_msg_format = config.saved_msg_formats[i]
            saved_msg_content = config.saved_msg_contents[i]
            print('saved_msg_format', saved_msg_format)
            print('saved_msg_content', saved_msg_content)
            self.tableWidgetMessages.insertRow(row)
            self.tableWidgetMessages.setItem(row, 0, QtWidgets.labels_list_dictionaryQTableWidgetItem(saved_msg_name))
            self.tableWidgetMessages.setItem(row, 1, QtWidgets.QTableWidgetItem(saved_msg_format))
            self.tableWidgetMessages.setItem(row, 2, QtWidgets.QTableWidgetItem(saved_msg_content))  
            row = row + 1
        self.tableWidgetMessages.selectRow(0)
        
    def getMsgListFromMsgTuple(self, msgTuple):
        msgList = []
        for x in range(len(msgTuple)):
            msgList.append(msgTuple[x])
        return msgList
    
    def set_bit(self, v, index, x):
        mask = 1 << index
        v &= ~mask
        if x:
            v |= mask
        return v     
   
    def searchMessage(self,text):
        print("Searching...",text)
        
        for i in range(self.containerLayout.count()):
            # widget = self.containerLayout.itemAt(i).widget()
            
            layout = self.containerLayout.itemAt(i)
            for i in range(layout.count()):
                tempWidget = layout.itemAt(i).widget() 
                if isinstance(tempWidget, QtWidgets.QLabel):    
                    widget = tempWidget
                # else:
                #     widget = None
            # widget.setStyleSheet("")
            if widget is not None and text.lower() !="":
                if text.lower() in widget.text().lower():
                    widget.setStyleSheet("background-color: pink;")
                    self.scrollArea.ensureWidgetVisible(widget,xMargin=10,yMargin=10)
                else:
                    widget.setStyleSheet("")
                
    def load_message(self):
        # print('dictionary', config.msg_dictionary) 
        print('messages', config.msg_names) 
        for x in config.msg_names:
            self.comboBoxMessages.addItem(x)
            
    def update_gui(self, set_bit_list):
        print('Ui_MainWindow update_gui called')
        for i,x in enumerate(self.listCheckBox):
            self.listCheckBox[i].setChecked(False)
            
        for i,x in enumerate(set_bit_list):
            self.listCheckBox[x].setChecked(True)   
            
    def update_header(self,header):
        # self.lineEditHeader.setText(header)
        header_data_list = header.split(" ")
        print('header_data_list = ', header_data_list)
        i=0
        for child in self.scrollAreaWidgetContents_3.findChildren(QtWidgets.QWidget):
            if i<len(header_data_list):
                if isinstance(child, QtWidgets.QLineEdit):
                    if( 6 < i ):
                        print(header_data_list[i])
                        child.setText(header_data_list[i])
                    i = i+1
                else:
                    pass
            
    def get_time_crc_updated_packet(self, data):
        data = bytearray(data)
        header_format_rcv = config.header_formats[0]
        header_length_rcv = struct.calcsize(f'={header_format_rcv}') #getting the header length
        header_tuple_rcv = struct.unpack(f'={header_format_rcv}',data[0:header_length_rcv]) #unpacking only header 
        hdrList = self.getMsgListFromMsgTuple(header_tuple_rcv)
            
        datetime_now = datetime.datetime.now()
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

    def open_receiver(self):
        dialog = UserInputDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            recv_port, send_port, send_ip = dialog.get_data()
            print('form data:',recv_port, send_port, send_ip)
            commands = ['cd ../receiver', 'python main.py '+ recv_port + ' ' + send_port + ' ' + send_ip]
            commands_string = "; ".join(commands)
            subprocess.run(['gnome-terminal', '--', 'bash', '-c', f'{commands_string}'])
        else:
            print('Cancelled')

    
    def getStringifiedMsgList(self, input_list):
        msg_list = []
        for x in range(len(input_list)):
            if(isinstance(input_list[x], bytes)):
                string = input_list[x].decode('utf-8').rstrip('\x00')
                msg_list.append(string)
            else:   
                msg_list.append(input_list[x])
        return msg_list
    
    def clear_widget(self, i):
        for col in range(self.containerLayout.count()):
            item = self.containerLayout.itemAtPosition(i,col)
            if item is not None:
                # print("---",item)
                widget = item.widget()
                if widget:
                    self.containerLayout.removeWidget(widget)
                    widget.deleteLater()
    
    def deleteAction(self,btnObjectName):
        
        print("------clicked", btnObjectName)
        # i = int(btnObjectName)
    
        # repeat_count = self.listLineEdits[i].text()
        # if repeat_count == '':
        #     repeat_count = 0
        # else:
        #     repeat_count = int(repeat_count)
            
        # label = self.listLabels[i].text()   
        # print("Deleting",label) 
            
        # struct_item = self.dict_index[i][2]
        # print("LAbels Seleted",self.listLabels[i].text(),'struct_item',struct_item)
        
        # start_idx = i + 1
        # end_idx = 0
        # for idx in range(i+1,len(self.listLabels)):
        #     print("Items---",self.listLabels[idx].text(),"--",idx,"--",len(self.listLabels))
        #     struct_contains = self.dict_index[idx][8].split('.')
    
        #     if struct_item in struct_contains:
        #         # print("struct_contains",struct_contains)
        #         end_idx = idx
        #         self.clear_widget(idx)
        #         # self.listLabels.pop(idx)
        #     else:
        #         break
    
        # del self.listLabels[start_idx:end_idx+1]
        # del self.listLineEdits[start_idx:end_idx+1]
        # del self.listDyanamicVaribleButton[start_idx:end_idx+1]
        # del self.dict_index[start_idx:end_idx+1]
        # del self.dynamic_contentFormat[start_idx:end_idx+1]
    
        # for idx in range(len(self.listLabels)):
        #     print("Deletion---",self.listLabels[idx].text())
    
        # print("LEN after deleteion",len(self.listLabels))
    
        # self.refresh_gui(self)
    
    
    # def ExpandStructs(self, i):
    #     print(f"Expand clicked index{i}, dict_index label {self.dict_index[i][0]}")
    #     self.listExpandButton[i].setText("▼")
    #     structure_name = self.dict_index[i][2]
    #     base_struct_level = self.dict_index[i][8].split(".")
        
    #     i=i+1
    #     # for j, item in enumerate(self.listExpandButton):
    #         # print(">>", j," ",item.text())
    #     # zz = self.dict_index
        
    #     while i<len(self.listisExpand):
    #         spaceValue, struct_level = struct_level_finder(self.attr_stuct_details[i])
    #         if struct_level<=len(base_struct_level):
    #             break
    #         if structure_name in self.attr_stuct_details[i] and struct_level<=len(base_struct_level)+1: 
    #             self.listisExpand[i]=True
    #             self.listLabels[i].show()
    #             self.listLineEdits[i].show()
    #             self.listDyanamicVaribleButton[i].show()
    #             self.listDyanamicRemoveButton[i].show()
    #             self.listExpandButton[i].show()
    #         i+=1
    #     self.refresh_Buttons_status()
        
        
    def ExpandStructs(self, i):
        showPrint = True
        s_time = time.time()  
        
        
        self.listExpandButton[i].setText("▼")
        structure_name = self.dict_index[i][2]
        stack_nested = [structure_name]
               
        i=i+1
        
        # zz = self.dict_index
        # zy = self.listisExpand

        while True:
            # print(self.dict_index[i][0])
            if structure_name not in self.attr_stuct_details[i]:
                break
            
            if stack_nested[-1] not in self.attr_stuct_details[i]:
                stack_nested.pop()
                
            if self.dict_index[i][2] != "" and stack_nested[-1] == structure_name:
                self.listisExpand[i]=True
                self.listLabels[i].show()
                self.listLineEdits[i].show()
                self.listDyanamicVaribleButton[i].show()
                self.listDyanamicRemoveButton[i].show()
                self.listExpandButton[i].show()
                
                stack_nested.append(self.dict_index[i][2])
                
            elif self.dict_index[i][2] == "" and stack_nested[-1] == structure_name:
                self.listisExpand[i]=True
                self.listLabels[i].show()
                self.listLineEdits[i].show()
                self.listDyanamicVaribleButton[i].show()
                self.listDyanamicRemoveButton[i].show()
                self.listExpandButton[i].show()
                
            else:
                pass
            
            if i>=len(self.dict_index)-1:
                break
                
            i+=1
            
            
        e_time = time.time()
        DBUG.printDebug(">>>>TIME>>>>>>> Expand function before button refresh: ",e_time-s_time, isPrint=showPrint)
        
        s_time = time.time()
        self.refresh_Buttons_status()
        e_time = time.time()
        DBUG.printDebug(">>>>TIME>>>>>>> Expand function button refresh function",e_time-s_time, isPrint=showPrint)
        
        
    
    def CollaspStructs(self, i):
        showPrint = True
        print(f"Collasp clicked index{i}, dict_index label {self.dict_index[i]}")
        self.listExpandButton[i].setText("▶")
        structure_name = self.dict_index[i][2]
        base_struct_level = self.dict_index[i][8].split(".")
        i=i+1
        while i<len(self.listisExpand):
            spaceValue, struct_level = struct_level_finder(self.attr_stuct_details[i])
            if struct_level<=len(base_struct_level):
                break
            if structure_name in self.attr_stuct_details[i] and struct_level>len(base_struct_level):
                self.listisExpand[i]=False
                self.listLabels[i].hide()
                self.listLineEdits[i].hide()
                self.listDyanamicVaribleButton[i].hide()
                self.listDyanamicRemoveButton[i].hide()
                self.listExpandButton[i].hide()
                if self.listExpandButton[i].isEnabled():
                    self.listExpandButton[i].setText("▶")
            i+=1
        
        s_time = time.time()
        self.refresh_Buttons_status()
        e_time = time.time()
        DBUG.printDebug(">>>>TIME>>>>>>> Collasp function button refresh function",e_time-s_time, isPrint=showPrint)
        
    def getUpdatedattributes(self, idx, struct_name, current_expand_level, firstEle): 
        showPrint = False
        repeating_struct_attributes = self.dyanamicStructre[struct_name]
        # print("vvvvvvvvvvvvvvvvvvvvv", len(repeating_struct_attributes))
        
        for items in repeating_struct_attributes:
            DBUG.printDebug(">>>>>items", idx, items["name"], isPrint=showPrint)

            if NESTED_STRUCT_IDENTIFIER in items["name"]:
                key = items["name"].split(NESTED_STRUCT_IDENTIFIER)[1]
                value = ""
                DBUG.printDebug("++++++++++++ recusion in ",items["name"],"++++++++++++++++++++++++++++\n", isPrint=showPrint)
                idx = self.getUpdatedattributes(idx, key, current_expand_level, True)
                DBUG.printDebug("----------- recusion out ",key,"---------------------\n", isPrint=showPrint)
    
            else:
                key = items["name"]
                val1 = self.dynamicAttributesIrs[key]
                value = items.copy()
                value.update(val1)
                
                # Struct detailss
                self.attr_stuct_details.insert(idx, value['structures'] )
                
                # Label
                rep_label = QtWidgets.QLabel()
                rep_label.setFixedSize(300, 20)
                rep_label.setToolTip(value['irsValue'].replace("_x000D_",""))
                rep_label.setToolTipDuration(50000)
                rep_label.setStyleSheet("""
                                            QLabel{ padding-left: 10px; 
                                                      padding-right:10px;
                                                      background-color:{self.colr}
                                                      }
                                            QToolTip{ color:#ffffff; background-color:#2a82da;
                                                      border: 1px solid black;
                                                      padding:10px;}
                                            QLabel:hover{background-color:lightblue;border: 1px solid black;}""")
                rep_label.setText(key)
                
                if(firstEle == True):
                    self.colr = "Green"
                    firstEle = False
                else:
                    self.colr = "black"
                    
                rep_label.setStyleSheet(f"color:{self.colr}")
                self.listLabels.insert(idx, rep_label)

                    
                
                
                # LineEdit
                # print("value", value['dyanamicStruct'])
                rep_lineEdit = QtWidgets.QLineEdit()
                rep_lineEdit.setFixedSize(100, 20) 
                if value['dyanamicStruct']!='':
                    rep_lineEdit.setText(str(1))
                    rep_lineEdit.setReadOnly(True)
                self.listLineEdits.insert(idx, rep_lineEdit)
                
                # Add
                addBtn = QtWidgets.QPushButton('')
                addBtn.setEnabled(False)
                addBtn.setFixedSize(50, 20) 
     
                if(value['dyanamicStruct'] != ''):
                    addBtn.setEnabled(True)
                    addBtn.setText("+")
                else:
                    addBtn.setText("")
                    addBtn.setEnabled(False)
                self.listDyanamicVaribleButton.insert(idx, addBtn)
                
                # Delete
                deleteBtn = QtWidgets.QPushButton('')
                deleteBtn.setEnabled(False)
                deleteBtn.setFixedSize(50, 20) 
     
                if(value['dyanamicStruct'] != ''):
                    deleteBtn.setEnabled(True)
                    deleteBtn.setText("-")
                else:
                    deleteBtn.setText("")
                    deleteBtn.setEnabled(False)
                self.listDyanamicRemoveButton.insert(idx, deleteBtn)
                
                
                # Expand/collasp
                expandBtn = QtWidgets.QPushButton("")
                expandBtn.setEnabled(False)
                expandBtn.setFixedSize(50, 20)
                
                if value['dyanamicStruct'] !='':
                    # print("------------fldskjflk---",value['dyanamicStruct'])
                    expandBtn.setEnabled(True)
                    expandBtn.setText("▶")
                    # self.listisExpand.insert(idx,True)
                else:
                    expandBtn.setText("")
                    expandBtn.setEnabled(False)
                    # self.listisExpand.insert(idx, True)
                self.listExpandButton.insert(idx, expandBtn) 
                

                self.listisExpand.insert(idx, True)
                
                
                self.dynamic_contentFormat.insert(idx,value['AttributeFormat'])
                
                
                self.attrHlayout = QtWidgets.QHBoxLayout()
                self.attrHlayout.setAlignment(QtCore.Qt.AlignRight)
                
                self.attrHlayout.addStretch()   
                spaceValue, structLevel = struct_level_finder(value['structures'])                                  
                self.listLabels[idx].setStyleSheet(f"margin-left: {spaceValue}px; background-color: #e0e0e0;"+self.listLabels[idx].styleSheet())
                self.attrHlayout.addWidget(self.listLabels[idx])
                self.attrHlayout.addWidget(self.listLineEdits[idx])
                self.attrHlayout.addWidget(self.listDyanamicVaribleButton[idx])
                self.attrHlayout.addWidget(self.listDyanamicRemoveButton[idx])
                self.attrHlayout.addWidget(self.listExpandButton[idx])
                

                self.attrHlayout.addStretch()
                
                self.containerLayout.insertLayout(idx, self.attrHlayout)
                
                # print("OUTPUT ADDED: ", self.listLabels[idx].text(), self.listDyanamicVaribleButton[idx].text(), self.listExpandButton[idx].text(), self.attr_stuct_details[idx])
                # print("DICT INDEX: ", self.dict_index[i])
                # [ARGUMENT_NAME, ARGUMENT_TYPE, ATR_ARRAY_SIZE, ARGUMENT_SIZE, INPUT_VALUE, FORMAT, BitField, IRS_VALUE, StructureName, ATR_ARRAY_SIZE]
                data_index = [value['structures'].split(".")[-1], "", value["dyanamicStruct"], value["arg_size"] ,value["defaultInput"], value["AttributeFormat"], value["bitField"], value["irsValue"], value["structures"], value["dyanamicStruct"], value["staticStructSize"]]
                self.dict_index.insert(idx, data_index)
                
                
                idx+=1
        return idx
        
    def addStructureitems(self,idx,val):
        DBUG.printWhere()
        showPrint = False
        
        # printDict(self.dict_index, [10], "Start addStructureitems")
        
        i = idx

        rep_struct_name = self.dict_index[i-1][2]
        DBUG.printDebug("structure repeating>>>>>>", rep_struct_name, isPrint=showPrint)
        
        self.listExpandButton[i-1].setText("▼")
        current_expand_level = len(self.dict_index[i-1][8].split("."))+1
        DBUG.printDebug(f"current_expand_level = {current_expand_level}")
        if i<len(self.dict_index):
            while(rep_struct_name in self.dict_index[i][8].split(".")):
                if i==len(self.dict_index)-1:
                    i+=1
                    idx+=1
                    break
                i+=1
                idx+=1
        
        DBUG.printDebug(f"Adding new structure from: At Index {idx}", isPrint=showPrint)
        s_time = time.time()  
        idx = self.getUpdatedattributes(idx, rep_struct_name, current_expand_level, True)
        e_time = time.time()
        DBUG.printDebug(">>>>TIME>>>>>>> getUpdatedattributes TIME TAKEN: ",e_time-s_time, isPrint=showPrint)
        
        self.refresh_Buttons_status()
        
        DBUG.printDebug("After adding data", isPrint=showPrint)
        # printDict(self.dict_index, [10], "End of addStructureitems")
        
        
    def formatTextView(self):    
        for i,x in enumerate(self.dynamic_contentFormat):   
            label =  QtWidgets.QLabel()
            
            if(self.dynamic_contentFormat[i] == 'B'or self.dynamic_contentFormat[i] == 'b'):
                label.setText("1 Byte")
            if(self.dynamic_contentFormat[i] == 'H'or self.dynamic_contentFormat[i] == 'h'):
                label.setText("2 Byte")
            if(self.dynamic_contentFormat[i] == 'I'or self.dynamic_contentFormat[i] == 'i'or self.dynamic_contentFormat[i] == 'f'):
                label.setText("4 Byte")
            if(self.dynamic_contentFormat[i] == 'Q'or self.dynamic_contentFormat[i] == 'q' or self.dynamic_contentFormat[i] == 'd'):
                label.setText("8 Byte")
            elif('s' in self.dynamic_contentFormat[i]):
                split_str = self.dynamic_contentFormat[i].split('s')
                label.setText(split_str[0]+' Byte')  
                
            self.format_label_text.insert(i,label)
        
    def dyanamicUpdate(self,btnObjectName):
        showPrint = True
        k = self.dict_index
        debugSelfdict = self.dict_index
        # DBUG.printDebug("------clicked", btnObjectName, isPrint=showPrint)
        clickedButtonIndex = int(btnObjectName)
        # DBUG.printDebug("Dictinary index", self.dict_index[i][9], isPrint=showPrint)
    
        repeat_count = self.listLineEdits[clickedButtonIndex].text()
        if repeat_count == '':
            repeat_count = 0
        else:
            repeat_count = int(repeat_count)
        # pos = clickedButtonIndex
        

        # # checking nested struct
        # for index in range(0,i):
        #     if(self.dict_index[index][2] != ''):
        #         if(self.dict_index[index][2] == 'NA'):
        #             continue
        #         else:
        #             self.struct_stack.append(self.dict_index[index][2]) 
    
        if(self.dict_index[clickedButtonIndex][2] != ''):
            val = int(self.listLineEdits[clickedButtonIndex].text())

            val = val + 1
  
            if (self.dict_index[clickedButtonIndex][10] != 0) and (val>self.dict_index[clickedButtonIndex][10]):
                # DBUG.printDebug("Exceeds thae max structure limit", isPrint=showPrint)
                errorDisplay.show(self.centralwidget, f"Maximum Limit is {self.dict_index[clickedButtonIndex][10]}")
                return 
            start_time = time.time()
            self.addStructureitems(clickedButtonIndex+1,val)  

            # DBUG.printDebug(f"#ADDING# Layout: {self.containerLayout.count()}, Labels: {len(self.listLabels)}, dictIndex: {len(self.dict_index)}", isPrint=showPrint)
            self.listLineEdits[clickedButtonIndex].setText(str(val)) 
            
            end_time = time.time()
            DBUG.printDebug(">>>>TIME>>>>>>> TOTAL ADDING FUNCTION TIME TAKEN: ", end_time - start_time, isPrint=showPrint)
            # msg_len = self.calculate_dyanamic_length()
            # self.listLineEdits[MSG_LEN_INDEX].setText(str(msg_len))
            
            
   
    
        
    def dyanamicRemove(self, index):
        k = self.dict_index
        # klabel = self.listLabels
        # kLineEdits = self.listLineEdits
        # kContiainer = self.containerLayout
        rep_index = index
        rep_struct_name = self.dict_index[index][2]
        initial_rep_count = int(self.listLineEdits[index].text())
        rep_count = initial_rep_count
        if rep_count == 0:
            return
        
        index+=1
        firstEle = self.dict_index[index][8]
        deleteStartIndex = -1
        deleteEndIndex = -1

        while(rep_struct_name in self.dict_index[index][8].split(".")):
            if firstEle == self.dict_index[index][8]:
                if rep_count == 1:
                    deleteStartIndex = index
                    if index==len(self.dict_index)-1:
                        print("Reached end")
                        index+=1
                        break
                    else:
                        index+=1
                        continue 
                else:
                    rep_count-=1

            if index==len(self.dict_index)-1:
                print("Reached end")
                index+=1
                break
            index+=1
            
        deleteEndIndex = index
        print("DELETING FROM INDEX: startIndex, endIndex: ", deleteStartIndex, deleteEndIndex)
        
        # for j, itm in enumerate(self.listLabels):
        #     print(j, itm.text())
        
        
        print(f"## Layout: {self.containerLayout.count()}, Labels: {len(self.listLabels)}, dictIndex: {len(self.dict_index)}")
        i=deleteStartIndex
        while deleteStartIndex < deleteEndIndex:
            print("To be deleted", self.listLabels[i].text())
            item = self.containerLayout.takeAt(i)
            if item.layout():
                print(">> Layout found")
                child_layout = item.layout()
                
                self.listLabels[i].setParent(None)
                self.listLabels[i].deleteLater()
                self.listLabels[i]=None
                del self.listLabels[i]
                
                self.listLineEdits[i].setParent(None)
                self.listLineEdits[i].deleteLater()
                self.listLineEdits[i]=None
                del self.listLineEdits[i]
                
                self.listDyanamicVaribleButton[i].setParent(None)
                self.listDyanamicVaribleButton[i].deleteLater()
                self.listDyanamicVaribleButton[i]=None
                del self.listDyanamicVaribleButton[i]
                
                self.listDyanamicRemoveButton[i].setParent(None)
                self.listDyanamicRemoveButton[i].deleteLater()
                self.listDyanamicRemoveButton[i]=None
                del self.listDyanamicRemoveButton[i]
                
                self.listExpandButton[i].setParent(None)
                self.listExpandButton[i].deleteLater()
                self.listExpandButton[i]=None
                del self.listExpandButton[i]
                
                child_layout.deleteLater()
                deleteStartIndex+=1
            else:
                del item
                print("NOT LAYOUT ")
                deleteStartIndex+=1
   
        deleteStartIndex = i   
        del self.dict_index[deleteStartIndex:deleteEndIndex]
        del self.attr_stuct_details[deleteStartIndex:deleteEndIndex]
        del self.listisExpand[deleteStartIndex:deleteEndIndex]
        del self.dynamic_contentFormat[deleteStartIndex:deleteEndIndex]
        
        # for k, itm in enumerate(self.listLabels):
        #     print(">> ", k, itm.text(), self.dict_index[k][0])
        self.refresh_Buttons_status()
        self.listLineEdits[rep_index].setText(str(initial_rep_count-1))
        
        printDict(self.dict_index, [10], "remove before size cal")
        msg_len = self.calculate_dyanamic_length()
        self.listLineEdits[MSG_LEN_INDEX].setText(str(msg_len))
        printDict(self.dict_index, [10], "remove after size cal")
        
    def refresh_gui(self):
        
        print("REFRESH_GUI")
        printDict(self.dict_index, [10], "Refresh GUI")
        
        # msg_len = self.calculate_dyanamic_length()
        # content_format_string = ' '.join(map(str,self.getStringifiedMsgList(self.dynamic_contentFormat)))
        # msg_len = 0
        # print(">>content_format_string", content_format_string)
        # if(len(self.dynamic_contentFormat) != 0):
        #     msg_len = struct.calcsize(f'={content_format_string}') #getting the content length    
        # rowCount = 0
        
        # msg_content = csv_dict[f'{config.message_selected}']
        # clearLayout(self.containerLayout)
        
        # for i,item in enumerate(self.dict_index):
        #     print(i,"---LLLL---",item[6])
    
        # print("**************88", len(self.attr_stuct_details))
        # for i,item in enumerate(self.attr_stuct_details):
        #     print(".............>>",i, item)
        print(f"Layout: {self.containerLayout.count()}, Labels: {len(self.listLabels)}, dictIndex: {len(self.dict_index)}")
        for i,x in enumerate(self.listLabels):   
            # print(len(self.attr_stuct_details), len(self.listLabels), self.attr_stuct_details[i])
            # struct_level_list = self.attr_stuct_details[i].split(".")
            # print("============",self.attr_stuct_details[i] ,"--------=======", struct_level_list)
            # struct_level = len(struct_level_list)
            # spaceValue = 0
            # if struct_level > 2:
            #     spaceValue = 40*(struct_level-2)
            
            # ATS 
            # if i == MSG_LEN_INDEX:
            #     self.listLineEdits[MSG_LEN_INDEX].setText(str(msg_len))
                
            spaceValue, struct_level = struct_level_finder(self.attr_stuct_details[i])
            # print("---------------->>>>", self.attr_stuct_details[i]," >>> ", struct_level," >> ", spaceValue)
            # self.rowWidget = QtWidgets.QWidget()
            # self.attrHlayout = QtWidgets.QHBoxLayout(self.rowWidget)
            self.attrHlayout = QtWidgets.QHBoxLayout()
            self.attrHlayout.setAlignment(QtCore.Qt.AlignRight)
            
            self.attrHlayout.addStretch()
            # self.attrHlayout.addSpacing(spaceValue)
            # self.containerLayout.addWidget(self.listLabels[i], rowCount, 0,alignment=QtCore.Qt.AlignmentFlag.AlignRight)
            # self.containerLayout.addWidget(self.listLineEdits[i], rowCount, 1,alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
            # self.containerLayout.addWidget(self.listDyanamicVaribleButton[i], rowCount, 2,alignment=QtCore.Qt.AlignmentFlag.AlignLeft) 

            # spaceValue, struct_level = struct_level_finder(self.attr_stuct_details, i)

        # colr = depth_color(struct_level).name()
        # self.listLabels[i].setStyleSheet(f"background-color:{colr};")
        
            # if(i == 4):  #Automatically filling MSG ID
            #     self.listLineEdits[i].setText(str(int(msg_len)))
            
            
            if self.listisExpand[i]==True:
                # self.rowWidget.show()
                self.listLabels[i].show()
                self.listLineEdits[i].show()
                
                self.listDyanamicVaribleButton[i].show()
                self.listDyanamicRemoveButton[i].show()
                self.listExpandButton[i].show()
            else:
                # self.rowWidget.hide()
                self.listLabels[i].hide()
                self.listLineEdits[i].hide()
                self.listDyanamicVaribleButton[i].hide()
                self.listDyanamicRemoveButton[i].hide()
                self.listExpandButton[i].hide()


                
            # if not self.listExpandButton[i].isEnabled():
            #     self.listExpandButton.hide()
            # spaceValue = 300 - spaceValue

            # self.listLabels[i].setStyleSheet(f"padding-left:{spaceValue}")
                # self.listLabels[i].setStyleSheet("""
                #                                  QLabel{ padding-left: 10px; 
                #                                           padding-right:10px;
                #                                           background-color: #e0e0e0;}
                #                                  QToolTip{ color:#ffffff; background-color:#2a82da;
                #                                           border: 1px solid black;
                #                                           padding:10px;}
                #                                  QLabel:hover{background-color:lightblue; border: 1px solid black;}""")
                                                 
            self.listLabels[i].setStyleSheet(f"margin-left: {spaceValue}px; padding-left: 10px; padding-right:10px; background-color: #e0e0e0;"+self.listLabels[i].styleSheet())
            self.attrHlayout.addWidget(self.listLabels[i])
            self.attrHlayout.addWidget(self.listLineEdits[i])
            self.attrHlayout.addWidget(self.listDyanamicVaribleButton[i])
            self.attrHlayout.addWidget(self.listDyanamicRemoveButton[i])
            self.attrHlayout.addWidget(self.listExpandButton[i])


            self.attrHlayout.addStretch()
            self.containerLayout.addLayout(self.attrHlayout)
            # self.containerLayout.addWidget(self.rowWidget)

            

                
            # rowCount = rowCount+1

            
        self.refresh_Buttons_status()
        
        
    def refresh_Buttons_status(self):
        for idx in range(0, len(self.listDyanamicVaribleButton)):
            self.listDyanamicVaribleButton[idx].setObjectName(str(idx))
            self.listDyanamicRemoveButton[idx].setObjectName(str(idx))
            self.listExpandButton[idx].setObjectName(str(idx))
            try:
                self.listDyanamicVaribleButton[idx].clicked.disconnect()
                self.listDyanamicRemoveButton[idx].clicked.disconnect()
                self.listExpandButton[idx].clicked.disconnect()
            except TypeError:
                pass
            
            if(self.listDyanamicVaribleButton[idx].text() == '+'):
                self.listDyanamicVaribleButton[idx].clicked.connect(lambda _, idx=idx: self.dyanamicUpdate(idx))
            else:
                pass

            if(self.listDyanamicRemoveButton[idx].text() == '-'):
                self.listDyanamicRemoveButton[idx].clicked.connect(lambda _, idx=idx: self.dyanamicRemove(idx))
            else:
                pass
            
            if(self.listExpandButton[idx].text() == "▶"):
                self.listExpandButton[idx].clicked.connect(lambda _, idx=idx: self.ExpandStructs(idx))
            elif self.listExpandButton[idx].text() == "▼":
                self.listExpandButton[idx].clicked.connect(lambda _, idx=idx: self.CollaspStructs(idx))
            else:
                pass
                


                
                
    def reload_gui(self, dict_index = [], dict_default_values = []):
        print("RELOADING.....")
        # self.strucChkBox.setChecked(False)
        
        
        for k,chkBox in enumerate(self.listCheckBox):
            chkBox.setParent(None)
            chkBox.deleteLater()
            chkBox= None
        self.listCheckBox.clear()
        
        for label in self.listLabels:
            label.setParent(None)
            label.deleteLater()
            label= None
        self.listLabels.clear()
        
        for lineEdit in self.listLineEdits:
            lineEdit.setParent(None)
            lineEdit.deleteLater()
            lineEdit= None
        self.listLineEdits.clear()
        
        for h_label in self.header_labels:
            h_label.setParent(None)
            h_label.deleteLater()
            h_label = None
        self.header_labels.clear()
        
        for h_linedit in self.header_lineEdit:
            h_linedit.setParent(None)
            h_linedit.deleteLater()
            h_linedit= None
        self.header_lineEdit.clear()
        
        for DButton in self.listDyanamicVaribleButton:
            DButton.setParent(None)
            DButton.deleteLater()
            DButton= None
        self.listDyanamicVaribleButton.clear()
        
        for DRButton in self.listDyanamicRemoveButton:
            DRButton.setParent(None)
            DRButton.deleteLater()
            DRButton= None
        self.listDyanamicRemoveButton.clear()
        
        for EButton in self.listExpandButton:
            EButton.setParent(None)
            EButton.deleteLater()
            EButton= None
        self.listExpandButton.clear()
        
        self.listisExpand.clear()
        
        self.attr_stuct_details.clear()

        
        
        self.selected_byte_msg_formats.clear()
        self.modified_selected_byte_msg_formats.clear()
        self.selected_msg_bit_lengths.clear()
        
        while self.containerLayout.count():
            item = self.containerLayout.takeAt(0)
            if item.layout():
                del item
        
        
        # if self.comboBoxMessages.currentText() in config.msg_names:
        
        #Normal reload / editing reload
        # try:
        if len(dict_index)==0:
            self.dict_index = csv_dict[f'{config.message_selected}'].copy()
        else:
            self.dict_index = dict_index.copy()

        
    
        # Bits List
        self.bit_list = []
        
        for i,item in enumerate(self.dict_index):
            # print(item)
            self.bit_list.append(item[6])
        print("BIT LIST",self.bit_list)
        
        
        
        if len(dict_index)>0:
            # pass
            self.dynamic_contentFormat.clear()
            for x in dict_index:
                # print(x[5])
                self.dynamic_contentFormat.append(x[5])
        else:
            content_format_list = config.content_dictionary[config.message_selected]
            print(">content_format_list",content_format_list)
            content_format_string = ' '.join(map(str,self.getStringifiedMsgList(content_format_list)))
            self.dynamic_contentFormat = content_format_list.copy()
                    
        # except:
        #     print("not found")
    
        if config.message_selected == 'RATC_CBI_INDICATION_MSG':
            self.listCheckBox = config.ratc_cbi_indication_bit_names.copy()
            self.rows = int(len(self.listCheckBox) / self.columns)
            rowCount = 0 
            colCount = 0
            for i,x in enumerate(self.listCheckBox):
                self.listCheckBox[i] = QtWidgets.QCheckBox(str(i)+' '+x)
                self.listCheckBox[i].setStyleSheet("QCheckBox::checked"
                                                    "{"
                                                    "background-color : pink;"
                                                    "}"
                    )
                self.containerLayout.addWidget(self.listCheckBox[i], rowCount, colCount)
                rowCount = rowCount + 1
                if rowCount == self.rows:
                    rowCount = 0
                    colCount = colCount + 1 
                    
        elif config.message_selected == 'CBI_RATC_INDICATION_MSG':
            self.listCheckBox = config.cbi_ratc_indication_bit_names.copy()
            self.rows = int(len(self.listCheckBox) / self.columns)
            rowCount = 0 
            colCount = 0
            for i,x in enumerate(self.listCheckBox):
                self.listCheckBox[i] = QtWidgets.QCheckBox(str(i)+' '+x)
                self.listCheckBox[i].setStyleSheet("QCheckBox::checked"
                                                    "{"
                                                    "background-color : pink;"
                                                    "}"
                    )
                self.containerLayout.addWidget(self.listCheckBox[i], rowCount, colCount)
                rowCount = rowCount + 1
                if rowCount == self.rows:
                    rowCount = 0
                    colCount = colCount + 1  
    
        elif config.bits_dictionary[config.message_selected] == 'bytes':
            self.rows = len(self.dict_index)
            self.listLabels = self.dict_index.copy()
            self.listLineEdits = self.dict_index.copy()
            self.listDyanamicVaribleButton = self.dict_index.copy()
            self.listDyanamicRemoveButton = self.dict_index.copy()
            self.listExpandButton = self.dict_index.copy()
            self.listisExpand = self.dict_index.copy()
            self.attr_stuct_details = self.dict_index.copy()
            rowCount = 0
            
            # track_var = config.message_selected.split("_")
                
            # self.dict_index = csv_dict[f'{config.message_selected}']
            current_expand_level = 10
            print("DICT",len(self.dict_index))
            for i,x in enumerate(self.dict_index):
                # z=self.dict_index
                self.attr_stuct_details[i]=self.dict_index[i][8]
                

                self.listLabels[i] = QtWidgets.QLabel()
                self.listLabels[i].setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
                self.listLabels[i].setText(self.dict_index[i][0])
                self.listLabels[i].setFixedSize(300, 20)
                # widget.setStyleSheet("background-color: pink;")
                # hover
                self.listLabels[i].setToolTip(self.dict_index[i][7].replace("_x000D_",""))
                self.listLabels[i].setToolTipDuration(50000)
                self.listLabels[i].setStyleSheet("""
                                                 QLabel{ padding-left: 10px; 
                                                          padding-right:10px;
                                                          background-color: #e0e0e0;}
                                                 QToolTip{ color:#ffffff; background-color:#2a82da;
                                                          border: 1px solid black;
                                                          padding:10px;}
                                                 QLabel:hover{background-color:lightblue; border: 1px solid black;}""")


 
                self.listLineEdits[i] = QtWidgets.QLineEdit()
                if len(dict_default_values)>0:
                    self.listLineEdits[i].setText(str(dict_default_values[i]))
                else:
                    self.listLineEdits[i] = QtWidgets.QLineEdit()
                    if self.dict_index[i][2]!='':
                        self.listLineEdits[i].setText('1')
                        self.listLineEdits[i].setReadOnly(True)
                self.listLineEdits[i].setFixedSize(100, 20)    
                    
                
                if self.dict_index[i][2]!='':
                    self.listDyanamicVaribleButton[i] = QtWidgets.QPushButton('+')
                    self.listDyanamicVaribleButton[i].setEnabled(True)
                    # self.listLineEdits[i].setText('1')
                    # self.repeating_structs_names_list.append(x)
                else:
                    self.listDyanamicVaribleButton[i] = QtWidgets.QPushButton('')
                    self.listDyanamicVaribleButton[i].hide()
                    self.listDyanamicVaribleButton[i].setEnabled(False)
                self.listDyanamicVaribleButton[i].setFixedSize(50, 20)
                self.listDyanamicVaribleButton[i].setObjectName(str(i))


                if self.dict_index[i][2]!='':
                    self.listDyanamicRemoveButton[i] = QtWidgets.QPushButton('-')
                    self.listDyanamicRemoveButton[i].setEnabled(True)
                    # self.listLineEdits[i].setText('1')
                    # self.repeating_structs_names_list.append(x)
                else:
                    self.listDyanamicRemoveButton[i] = QtWidgets.QPushButton('')
                    self.listDyanamicRemoveButton[i].hide()
                    self.listDyanamicRemoveButton[i].setEnabled(False)
                self.listDyanamicRemoveButton[i].setFixedSize(50, 20)
                self.listDyanamicRemoveButton[i].setObjectName(str(i))
                
                
                if self.dict_index[i][2]!='':
                    self.listExpandButton[i] = QtWidgets.QPushButton("▼")
                    self.listExpandButton[i].setEnabled(True) 
                    self.listExpandButton[i].setObjectName(str(i))
                    self.listExpandButton[i].setFixedSize(50, 20)
                else:
                    self.listExpandButton[i] = QtWidgets.QPushButton("")
                    self.listExpandButton[i].setFixedSize(50, 20)
                    self.listExpandButton[i].setObjectName(str(i))
                    self.listExpandButton[i].setEnabled(False)
                    
                                    
                
 
                
                
                spaceValue, struct_level = struct_level_finder(self.attr_stuct_details[i])
                # if struct_level>current_expand_level:
                #     self.listisExpand[i]=False
                # else:
                #     self.listisExpand[i] = True
                self.listisExpand[i] = True
                
                    
                # dyanamicBtn.clicked.connect(lambda _,btnobjName=dyanamicBtn.objectName(): dyanamicUpdate(self,btnobjName,ui))
                
                # ATS
                if(i == 2):  #Automatically filling MSG ID
                    msg_id = config.id_dictionary[config.message_selected]
                    self.listLineEdits[i].setText(str(int(msg_id)))  #4 is index of MSG ID
                    
                
                    
                # if(i == 5):    
                #     content_format_list = config.modified_content_dictionary[config.message_selected]
                #     content_format_string = ' '.join(map(str,getStringifiedMsgList(content_format_list)))
                #     content_length = 0
                #     if(len(content_format_list) != 0):
                #         content_length = struct.calcsize(f'={content_format_string}') #getting the content length    
                #     msg_len = content_length 
                    
                #     self.listLineEdits[i].setText(str(msg_len))  #5 is index ID of MSG LEN
                    
                # if(i == 9):
                #     self.listLineEdits[9].setText(str(1)) #By defalult no of dest nodes is 1
    
                rowCount = rowCount + 1
                
        
        # content_format_list = config.content_dictionary[config.message_selected]
        # print("LIST Cntnt frmt",content_format_list)
        
        
        # print("**************88",self.attr_stuct_details)
        # for i,item in enumerate(self.attr_stuct_details):
        #     print(".............>>",i,type(item),self.attr_stuct_details[i])
    
        self.refresh_gui()
    
            
        # print("Initial Count", len(self.listLabels))
        # content_format_string = ' '.join(map(str,getStringifiedMsgList(content_format_list)))
        # print("CONTENT",type(content_format_list))
        
        # # print("CONTENT INDEX",self.content_format_index)
        
        # content_length = 0
        # if(len(content_format_list) != 0):
        #     content_length = struct.calcsize(f'={content_format_string}') #getting the content length    
        
        # # print('header_length',header_length,' content_length',content_length)
        # msg_id = config.id_dictionary[config.message_selected]
        # msg_len = content_length # + 4  #4 is CRC length
        # print("MSG_ID",config.message_selected)
        # msg_seq = 1 
        
        # header_string = config.header_values_dictionary[config.message_selected]
        # datetime_now = datetime.datetime.now()
        # day = datetime_now.day
        # month = datetime_now.month
        # year = datetime_now.year
        # hour = datetime_now.hour
        # minute = datetime_now.minute
        # seconds = datetime_now.second
        # milli_seconds = math.floor(datetime_now.microsecond / 1000)
        # unique_message_code = 1
        # # header_string += (f' {msg_id} {msg_len} {msg_seq} {day} {month} {year} {hour} {minute} {seconds} {milli_seconds} {unique_message_code}')
        # print('header_string = ', header_string)
        
    def smallRecursion(self, send_dict_index, dynamic_format, value_list, nested_stack, i):
        showPrint = False
        DBUG.printDebug("\nSMALL RECURSION FUNCTION", isPrint=showPrint)
        isRecursive = False
        currentSkipDynamic = ""
        for j in range(0,nested_stack[-1][1]): 
            DBUG.printDebug(f"INSERTING {nested_stack[-1][0]} zero padding required Times {nested_stack[-1][1]}  CURRENT COUNT: ", j+1, isPrint=showPrint)
            # for key,value in self.dyanamicStructre[nested_stack[-1][0]].items(): 
                
            for items in self.dyanamicStructre[nested_stack[-1][0]]: 
                if NESTED_STRUCT_IDENTIFIER in items["name"]:    
                    key = items["name"].split(NESTED_STRUCT_IDENTIFIER)[1]
                    value = ""
                else:
                    key = items["name"]
                    val1 = self.dynamicAttributesIrs[key]
                    value = items.copy()
                    value.update(val1)
                    
                # print("IMPORTANT",key, value)
                  
                if value == "" and isRecursive:
                    DBUG.printDebug("NEW RECURSIVE CALL FOR :", value, isPrint=showPrint)
                    self.smallRecursion(send_dict_index, dynamic_format, value_list, nested_stack, i)
                else:
                    if currentSkipDynamic != "" and currentSkipDynamic == key :
                        continue
                    else:
                        currentSkipDynamic = ""
                        
                    DBUG.printDebug(f"Index {i}, Processing attribute:", key, isPrint=showPrint)
                    DBUG.printDebug(i, value, isPrint=showPrint)
                    
                    if value["staticStructSize"]>0:
                        isRecursive = True 
                        structRepTup = (value["dyanamicStruct"], value["staticStructSize"])
                        nested_stack.append(structRepTup)
                    elif value["dyanamicStruct"] != "":
                        currentSkipDynamic = value["dyanamicStruct"]
                    else:
                        isRecursive = False
                        
                    data_index = [value['structures'].split(".")[-1], "", value["dyanamicStruct"], value["arg_size"] ,value["defaultInput"], value["AttributeFormat"], value["bitField"], value["irsValue"], value["structures"], value["dyanamicStruct"], value["staticStructSize"]]
                    send_dict_index.insert(i, data_index)
                    dynamic_format.insert(i, value["AttributeFormat"])
                    value_list.insert(i, 0)
                    i+=1
            DBUG.printDebug("\n\n", isPrint=showPrint)
        nested_stack.pop()
        return i
            

            
        
        
        
    def paddingStaticZeroData(self, send_dict_index, value_list, dynamic_format):
        showPrint = False
        
        DBUG.printDebug("Padding Zero init data lengths : dictIndex ",len(send_dict_index)," dynamicFormat ", len(dynamic_format), isPrint=showPrint)
        DBUG.printDebug("VALUE LIST: ", value_list, isPrint=showPrint)
        printDict(send_dict_index, [10], "Inside paddingStaticZeroData")
        
        i=0
        nested_stack = []
        
        # Find the already inserted and insert renaining at end (if the end is not end of structure)
        while i<len(send_dict_index):
            # Check if current attribute is part of stack top struct, if not insert the remaining zeros data for static array
            DBUG.printDebug(f"Index: {i}, Processing attribute:", send_dict_index[i][0], isPrint=showPrint)
            if len(nested_stack)>0:
                # find end of the current nested structure top
                if nested_stack[-1][0] not in send_dict_index[i][8]:
                    DBUG.printDebug(f"{nested_stack[-1][0]} not in {send_dict_index[i][8]}", isPrint=showPrint)
                    # print(">> Index:",i," Insert struct : ", nested_stack[-1][0], " Times:", nested_stack[-1][1])
                    
                    # i_bef=i
                    i = self.smallRecursion(send_dict_index, dynamic_format, value_list, nested_stack, i)
                    # print("INDEX after recursion", i, " And before recursion: ",i_bef)
                    continue
                    
                    
            if send_dict_index[i][10]!=0:
                Total_rep = send_dict_index[i][10]
                Total_inserted_already = value_list[i]
                
                DBUG.printDebug("Structure: ", send_dict_index[i][2], " Total_rep - Total_inserted_already", Total_rep,Total_inserted_already, isPrint=showPrint)
                
                # print("\n---------------------------")
                # print("Adding to nested_stack for padding: ", send_dict_index[i][2])
                # print(f"Total struct: {Total_rep}, Already inserted: {Total_inserted_already}")
                # print("---------------------------\n")
                
                structRepTup = (send_dict_index[i][2], Total_rep - Total_inserted_already)
                
                nested_stack.append(structRepTup)
                DBUG.printDebug("NESTED STACK", nested_stack, isPrint=showPrint)
            i+=1
            
        # insert renaining nested struct items at end (if the end of structure)   
        if len(nested_stack)>0:
            i=len(send_dict_index)
            DBUG.printDebug(">> Index:",i," Insert struct : ", nested_stack[-1][0], " Times:", nested_stack[-1][1], isPrint=showPrint)
            # Traverse all remaining elements of nestesd stack
            if nested_stack[-1][1]>0:
                # No of times remaining for particular structure
                for j in range(0,nested_stack[-1][1]):
                    # All elements of particular structure
                    for item in self.dyanamicStructre[nested_stack[-1][0]]:
                        
                        if NESTED_STRUCT_IDENTIFIER in item["name"]:    
                            key = item["name"].split(NESTED_STRUCT_IDENTIFIER)[1]
                            value = ""
                        else:
                            key = item["name"]
                            val1 = self.dynamicAttributesIrs[key]
                            value = item.copy()
                            value.update(val1)
                                                
                        if value == "":    
                            continue
                        else:
                            DBUG.printDebug(i, value, isPrint=showPrint)
                            data_index = [value['structures'].split(".")[-1], "", value["dyanamicStruct"], value["arg_size"] ,value["defaultInput"], value["AttributeFormat"], value["bitField"], value["irsValue"], value["structures"], value["dyanamicStruct"], value["staticStructSize"]]
                            send_dict_index.insert(i, data_index)
                            dynamic_format.insert(i, value["AttributeFormat"])
                            value_list.insert(i, 0)
                            i+=1
            nested_stack.pop()

        DBUG.printDebug("Length of dict_index after zero padding: ", len(send_dict_index), isPrint=showPrint)
        DBUG.printDebug("Length of dyanamic format after zero padding: ", len(dynamic_format), isPrint=showPrint)
        DBUG.printDebug("Length of value list after zero padding: ", len(value_list), isPrint=showPrint)
        # for i, dat in enumerate(send_dict_index):
        #     print(f"{i}  {value_list[i]}  {dynamic_format[i]}  {send_dict_index[i][0].split('.')[-1]}")
        printDict(send_dict_index, [10], "End paddingStaticZeroData")
        return send_dict_index, dynamic_format, value_list
    

    def calculate_dyanamic_length(self):
        isPrint = False
        # header_format = config.header_dictionary[config.message_selected]
        # content_format_list = config.modified_content_dictionary[config.message_selected] 
        # content_format = ' '.join(map(str,content_format_list[:]))
        # if(content_format == 'not' or content_format == ' '):
        #     content_format = ''
        # crc_format = config.crc_dictionary[config.message_selected]
        # if(crc_format == 'not'  or crc_format == ' '):
        #     crc_format = ''
        # # print('header_format:', header_format, ', content_format:', content_format, ', crc_format:',crc_format)    
        bits_format = config.bits_dictionary[config.message_selected]
        # header_list = []
        # content_list = []
        # crc_data = 0
        # print("BITS FMT",bits_format)
        
        if bits_format == 'cbi_ratc_indication_bits' or bits_format == 'ratc_cbi_indication_bits':
            
            header_format = config.header_dictionary[config.message_selected]
            content_format_list = config.modified_content_dictionary[config.message_selected] 
            content_format = ' '.join(map(str,content_format_list[:]))
            if(content_format == 'not' or content_format == ' '):
                content_format = ''
            crc_format = config.crc_dictionary[config.message_selected]
            if(crc_format == 'not'  or crc_format == ' '):
                crc_format = ''
            # print('header_format:', header_format, ', content_format:', content_format, ', crc_format:',crc_format)    
            bits_format = config.bits_dictionary[config.message_selected]
            header_list = []
            content_list = []
            crc_data = 0
            # print("BITS FMT",bits_format)
            
            
            
            
            header_list = header_list + self.get_header_list()
            max_byte_number, records_list = self.get_num_records_and_records_list()
            content_list.append(max_byte_number)
            content_list = content_list + records_list
            DBUG.printDebug("content formats", content_format, isPrint=isPrint)
            crcPack = struct.pack(f'={header_format} {content_format}', *tuple(header_list), *tuple(content_list)) #for CRC on header
            #crcPack = struct.pack(f'= {content_format}', *tuple(content_list))
            crc_data = crc_calulator.crc_32(crcPack)
            content_list.append(crc_data)
            DBUG.printDebug("________________________________________",content_list, isPrint=isPrint)
            DBUG.printDebug("max_byte_number: ", max_byte_number, isPrint=isPrint)
            DBUG.printDebug("size of record: ", len(records_list), isPrint=isPrint)

            
        elif bits_format == 'bytes':
            value_list = []
            format_list = self.dynamic_contentFormat
            
            for i,lineEdit in enumerate(self.listLineEdits):
                value = lineEdit.text()
                if 's' in format_list[i]:
                    value = bytes(value, 'utf-8')
                elif value == '' or value == ' ':
                    # print('empty value')
                    value = 0
                elif value == 'auto':
                    value = 'auto'    
                else: 
                    value = int(value)    
                value_list.append( value )
                
            # print("VALUE LIST",value_list)
            
            sizeForByte = 0
            modified_value_list = []
            non_standard_bits_values = []
            non_standard_bits_sizes = []
            bit_length_list = []
            modified_content_format_list = []
            
            send_dict_index, send_dynamic_format, send_value_list = self.paddingStaticZeroData(self.dict_index.copy(), value_list.copy(), self.dynamic_contentFormat.copy())

            
   
            for i in range(0, len(send_dict_index)):
                bit_length_list.append(int(send_dict_index[i][6]))
            # bit_length_list = config.bits_list_dictionary[config.message_selected]
            # print("bit_length_list",bit_length_list)
            
            isPrevBits = False
            for y,b in enumerate(bit_length_list):
                # print('b => ', b)
                if (b == 8 or b==0) and isPrevBits==False :
                    modified_value_list.append(send_value_list[y])
                    modified_content_format_list.append(send_dict_index[y][5])
                    isPrevBits=False
                    
                elif isPrevBits==True and (b==0):
                    errorDisplay.show(self.centralwidget, f"Incomplete {sizeForByte} bits for {send_dict_index[y-1][0]},\nPlease correct it in message_details file in config folder")
                    return
                
                else:
                    sizeForByte = sizeForByte + b
                    non_standard_bits_values.append(send_value_list[y])
                    non_standard_bits_sizes.append(b)
                    isPrevBits=True
                    if sizeForByte > 8:
                        errorDisplay.show(self.centralwidget, f"Incomplete {sizeForByte} bits for {send_dict_index[y-1][0]},\nPlease correct it in message_details file in config folder")
                        return
                    if sizeForByte == 8:
                        # print('byte complete......')
                        sizeForByte = 0
                        byteValue = self.calculateByte(non_standard_bits_values, non_standard_bits_sizes)
                        # print('byte = ',byteValue, 'bits:',bin(byteValue))
                        if byteValue == -1:
                            return
                        modified_value_list.append(byteValue)
                        modified_content_format_list.append(send_dict_index[y][5])
                        non_standard_bits_values.clear()
                        non_standard_bits_sizes.clear()
                        isPrevBits=False
            if sizeForByte != 0:
                errorDisplay.show(self.centralwidget, f"Incomplete {sizeForByte} bits at end,\nPlease correct it in message_details file in config folder")
                return
            # print('selected_byte_msg_formats: ', self.selected_byte_msg_formats)             
            # print('modified_selected_byte_msg_formats: ', self.modified_selected_byte_msg_formats)            
            # print('modified_value_list = ',modified_value_list)
            # print('modified_content_format : ',modified_content_format)
            
            # content_list = value_list[:]
            content_list = modified_value_list
            # print("content list",content_list)
            # print("Format modified",modified_content_format_list)
            modified_content_format = ' '.join(map(str,modified_content_format_list[:]))
            
            print("Format determined for messagelength calculation: ", modified_content_format)
            
            return struct.calcsize(f'={modified_content_format}')
 
            

     
    def send_clicked(self):
        print("From Send Clicked File")
        # try:
        self.set_IP_and_socket()
        header_format = config.header_dictionary[config.message_selected]
        content_format_list = config.modified_content_dictionary[config.message_selected] 
        content_format = ' '.join(map(str,content_format_list[:]))
        if(content_format == 'not' or content_format == ' '):
            content_format = ''
        crc_format = config.crc_dictionary[config.message_selected]
        if(crc_format == 'not'  or crc_format == ' '):
            crc_format = ''
        print('header_format:', header_format, ', content_format:', content_format, ', crc_format:',crc_format)    
        bits_format = config.bits_dictionary[config.message_selected]
        header_list = []
        content_list = []
        crc_data = 0
        print("BITS FMT",bits_format)
        
        if bits_format == 'cbi_ratc_indication_bits' or bits_format == 'ratc_cbi_indication_bits':
            header_list = header_list + self.get_header_list()
            max_byte_number, records_list = self.get_num_records_and_records_list()
            content_list.append(max_byte_number)
            content_list = content_list + records_list
            print("content formats", content_format)
            crcPack = struct.pack(f'={header_format} {content_format}', *tuple(header_list), *tuple(content_list)) #for CRC on header
            #crcPack = struct.pack(f'= {content_format}', *tuple(content_list))
            crc_data = crc_calulator.crc_32(crcPack)
            content_list.append(crc_data)
            print("________________________________________",content_list)
            print("max_byte_number: ", max_byte_number)
            print("size of record: ", len(records_list))
            self.send_and_log_message_and_update_gui(content_format, content_list)
            
        elif bits_format == 'bytes':
            
            header_list = header_list 
    
            value_list = []
            format_list = config.content_dictionary[config.message_selected]
            format_list = self.dynamic_contentFormat
            print("LENNNN",len(self.listLineEdits))
            
            for i,lineEdit in enumerate(self.listLineEdits):
                value = lineEdit.text()
                if 's' in format_list[i]:
                    value = bytes(value, 'utf-8')
                elif value == '' or value == ' ':
                    # print('empty value')
                    value = 0
                elif value == 'auto':
                    value = 'auto'    
                else: 
                    value = int(value)    
                value_list.append( value )
                
            print("VALUE LIST",value_list)
            
            sizeForByte = 0
            modified_value_list = []
            non_standard_bits_values = []
            non_standard_bits_sizes = []
            bit_length_list = []
            modified_content_format_list = []
            
            send_dict_index, send_dynamic_format, send_value_list = self.paddingStaticZeroData(self.dict_index.copy(), value_list.copy(), self.dynamic_contentFormat.copy())

            
   
            for i in range(0, len(send_dict_index)):
                bit_length_list.append(int(send_dict_index[i][6]))
            # bit_length_list = config.bits_list_dictionary[config.message_selected]
            print("bit_length_list",bit_length_list)
            
            isPrevBits = False
            for y,b in enumerate(bit_length_list):
                print('b => ', b)
                if (b == 8 or b==0) and isPrevBits==False :
                    modified_value_list.append(send_value_list[y])
                    modified_content_format_list.append(send_dict_index[y][5])
                    isPrevBits=False
                    
                elif isPrevBits==True and (b==0):
                    errorDisplay.show(self.centralwidget, f"Incomplete {sizeForByte} bits for {send_dict_index[y-1][0]},\nPlease correct it in message_details file in config folder")
                    return
                
                else:
                    sizeForByte = sizeForByte + b
                    non_standard_bits_values.append(send_value_list[y])
                    non_standard_bits_sizes.append(b)
                    isPrevBits=True
                    if sizeForByte > 8:
                        errorDisplay.show(self.centralwidget, f"Incomplete {sizeForByte} bits for {send_dict_index[y-1][0]},\nPlease correct it in message_details file in config folder")
                        return
                    if sizeForByte == 8:
                        # print('byte complete......')
                        sizeForByte = 0
                        byteValue = self.calculateByte(non_standard_bits_values, non_standard_bits_sizes)
                        # print('byte = ',byteValue, 'bits:',bin(byteValue))
                        if byteValue == -1:
                            return
                        modified_value_list.append(byteValue)
                        modified_content_format_list.append(send_dict_index[y][5])
                        non_standard_bits_values.clear()
                        non_standard_bits_sizes.clear()
                        isPrevBits=False
            if sizeForByte != 0:
                errorDisplay.show(self.centralwidget, f"Incomplete {sizeForByte} bits at end,\nPlease correct it in message_details file in config folder")
                return
            # print('selected_byte_msg_formats: ', self.selected_byte_msg_formats)             
            # print('modified_selected_byte_msg_formats: ', self.modified_selected_byte_msg_formats)            
            # print('modified_value_list = ',modified_value_list)
            # print('modified_content_format : ',modified_content_format)
            
            # content_list = value_list[:]
            content_list = modified_value_list
            print("content modified",content_list)
            print("Format modified",modified_content_format_list)
            modified_content_format = ' '.join(map(str,modified_content_format_list[:]))
        
            formantCount = len(modified_content_format_list)
            dataCount = len(content_list)
            
            # print('header_format : ',header_format,crc_format)
            # print('content_format : ',content_format)
            # print('header_list : ',header_list)
            # print('content_list : ',content_list)
            # content_list.append(3)
            # content_list = 
            
            print("Dynamic Content Format List :",len(self.dynamic_contentFormat), self.dynamic_contentFormat )
            
            # content_format = ' '.join(map(str,self.dynamic_contentFormat))
            self.send_and_log_message_and_update_gui(modified_content_format, content_list, formantCount,dataCount)

            
    def send_and_log_message_and_update_gui(self, form, content_list, formantCount=0, dataCount=0):
        #if config.message_selected == "PSD_RATC_INFO_MSG":
        #    print(">>>>>>>>>>>>>>", form, header_list, content_list)
        #    form = "BBBHBIII"
        #    packet = struct.pack(f'={form}', *tuple(content_list))
        #else:

        packet = struct.pack(f'={form}', *tuple(content_list))
        self.senderUDP.send_packet(packet)
    
        if config.name_to_header_type[config.message_selected] != 'external':
            print("================================")
            
            # header_str = ' '.join(map(str,header_list))
            content_str = ' '.join(map(str, self.getStringifiedMsgList(content_list)))
            # self.update_header(header_str) 
            self.update_content(f"Format({formantCount}): {form} \nContent({dataCount}): {content_str}") 
            config.log(f'{config.message_selected}{content_str}')
        return
    

    def update_content(self,content):
        # self.lineEditContent.setText(content)
        self.plainTextEditContent.setPlainText(content)
        
        
        


# ========================================================== Saving and Sending ===================================================================
    
    def onTabChanged(self, index):
        print("tab changed to index: ", index)
        
        
        #mahaiyo
        self.pushButtonAddPeriodicMessage.hide()
        self.pushButtonPeriodic.show()
        
        
        if index == 2:
            # Tab: Save and Send      
            print("SNS WIDGET TAB SHOWN")
        else:
            print("SNS WIDGET ALREADY PRESENT")

    
    def switchTabSNS(self, index, funcType, fromPage, isback):
        DBUG.printWhere()
        # self.reload_gui()
        
        print("->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", fromPage)
        if fromPage.lower() == "tabs":
            self.tabWidget.setCurrentIndex(index)

        if fromPage.lower() == "output":
            self.pushButtonSaveEdit.setText(f"{funcType} {fromPage}")
            self.pushButtonSend.hide() 
            self.pushButtonPeriodic.hide()
            self.snsWidget.show()
            self.backButton.show()
            if funcType.lower() == "save":
                self.lineEditTime.setText(str(GLOBAL_PERIODIC))
            self.delayLineEdit.hide()
            self.DelayLabel.hide()
            self.tabWidget.setCurrentIndex(index)
            self.tabWidget.setTabEnabled(0, False)
            self.tabWidget.setTabEnabled(2, False)
            self.tabWidget.setTabEnabled(3, False)
            self.tabWidget.setTabEnabled(4, False)
                
        
        if fromPage.lower() == "input":
            self.pushButtonSaveEdit.setText(f"{funcType} {fromPage}")
            self.pushButtonSend.hide() 
            self.pushButtonPeriodic.hide()
            self.backButton.show()
            self.delayLineEdit.show()
            if funcType.lower() == "save":
                self.delayLineEdit.setText(str(GLOBAL_DELAY))
                self.lineEditTime.setText(str(GLOBAL_PERIODIC))
            self.DelayLabel.show()
            self.snsWidget.show()
            self.tabWidget.setCurrentIndex(index)
            self.tabWidget.setTabEnabled(0, False)
            self.tabWidget.setTabEnabled(2, False)
            self.tabWidget.setTabEnabled(3, False)
            self.tabWidget.setTabEnabled(4, False)
            
            


    #mahaiyo
    def periodic_message_selection(self, index, funcType, fromPage, isback):
        self.tabWidget.setCurrentIndex(index)
        self.pushButtonPeriodic.hide()
        self.pushButtonAddPeriodicMessage.show()
        

     #mahaiyo      
    def addPeriodicMessage(self):
        #mahaiyo
        ##########################
        header_format = config.header_dictionary[config.message_selected]
        content_format_list = config.modified_content_dictionary[config.message_selected] 
        content_format = ' '.join(map(str,content_format_list[:]))
        if(content_format == 'not' or content_format == ' '):
            content_format = ''
        crc_format = config.crc_dictionary[config.message_selected]
        if(crc_format == 'not'  or crc_format == ' '):
            crc_format = ''
        print('header_format:', header_format, ', content_format:', content_format, ', crc_format:',crc_format)    
        bits_format = config.bits_dictionary[config.message_selected]
        header_list = []
        content_list = []
        print("BITS FMT",bits_format)
        content_format = content_format[len(header_format):]
            
            
        if bits_format == 'mt_indication_bits' or bits_format == 'indication_bits' or bits_format == 'control_bits' or bits_format == 'alarm_bits':
            header_list = header_list + self.get_header_list()
            maxRecords = 128
    
            if config.message_selected  == 'CBI_MT_INDICATION_MSG':
                maxRecords=512
            if config.message_selected == 'CBI_VDUS_INDICATION_MSG' or config.message_selected == 'VDUS_VDUD_INDICATION_MSG' or config.message_selected == 'CBI_ATS_INDICATION_MSG':
                maxRecords = 256
                
                # max_byte_number = 34
    
            max_byte_number, records_list = self.get_num_records_and_records_list(maxRecords)
            print(max_byte_number, len(records_list))
            
            content_list.append(max_byte_number)
            content_list = content_list + records_list
            print("content formats", len(content_format), content_format)
            print("header list", header_list)
            print("content list", content_list)
            crcPack = struct.pack(f'={header_format} {content_format}', *tuple(header_list), *tuple(content_list)) #for CRC on header
            #crcPack = struct.pack(f'= {content_format}', *tuple(content_list))
            crc_data = crc_calulator.crc_32(crcPack)
            content_list.append(crc_data)
            print("________________________________________",content_list)
            print("max_byte_number: ", max_byte_number)
            print("size of record: ", len(records_list))
            #self.send_and_log_message_and_update_gui(header_format+content_format+crc_format, header_list, content_list)
            

        elif bits_format == 'cbi_ratc_indication_bits' or bits_format == 'ratc_cbi_indication_bits':
            maxRecords = 128
            header_list = header_list + self.get_header_list()
            max_byte_number, records_list = self.get_num_records_and_records_list(maxRecords)
            content_list.append(max_byte_number)
            content_list = content_list + records_list
            DBUG.printDebug("content formats", content_format)
            crcPack = struct.pack(f'={header_format} {content_format}', *tuple(header_list), *tuple(content_list)) #for CRC on header
            #crcPack = struct.pack(f'= {content_format}', *tuple(content_list))
            crc_data = crc_calulator.crc_32(crcPack)
            content_list.append(crc_data)
            DBUG.printDebug("________________________________________",content_list)
            DBUG.printDebug("max_byte_number: ", max_byte_number)
            DBUG.printDebug("size of record: ", len(records_list))
            # self.send_and_log_message_and_update_gui(header_format+content_format+crc_format, header_list, content_list)

                
                
        elif bits_format == 'bytes':

            # temp_hdr_list = self.get_header_list()
            # print("hdr lst",temp_hdr_list)
            
            header_list = header_list 
    
            value_list = []
            format_list = config.content_dictionary[config.message_selected]
            format_list = self.dynamic_contentFormat
            print("LENNNN",len(self.listLineEdits))
            
            for i,lineEdit in enumerate(self.listLineEdits):
                value = lineEdit.text()
                if 's' in format_list[i]:
                    value = bytes(value, 'utf-8')
                elif value == '' or value == ' ':
                    # print('empty value')
                    value = 0
                elif value == 'auto':
                    value = 'auto'    
                else: 
                    value = int(value)    
                value_list.append( value )
                
            print("VALUE LIST",value_list)
            
            sizeForByte = 0
            modified_value_list = []
            non_standard_bits_values = []
            non_standard_bits_sizes = []
            bit_length_list = []
            modified_content_format_list = []
            
            send_dict_index, send_dynamic_format, send_value_list = self.paddingStaticZeroData(self.dict_index.copy(), value_list.copy(), self.dynamic_contentFormat.copy())

            
   
            for i in range(0, len(send_dict_index)):
                bit_length_list.append(int(send_dict_index[i][6]))
            # bit_length_list = config.bits_list_dictionary[config.message_selected]
            print("bit_length_list",bit_length_list)
            
            isPrevBits = False
            for y,b in enumerate(bit_length_list):
                print('b => ', b)
                if (b == 8 or b==0) and isPrevBits==False :
                    modified_value_list.append(send_value_list[y])
                    modified_content_format_list.append(send_dict_index[y][5])
                    isPrevBits=False
                    
                elif isPrevBits==True and (b==0):
                    errorDisplay.show(self.centralwidget, f"Incomplete {sizeForByte} bits for {send_dict_index[y-1][0]},\nPlease correct it in message_details file in config folder")
                    return
                
                else:
                    sizeForByte = sizeForByte + b
                    non_standard_bits_values.append(send_value_list[y])
                    non_standard_bits_sizes.append(b)
                    isPrevBits=True
                    if sizeForByte > 8:
                        errorDisplay.show(self.centralwidget, f"Incomplete {sizeForByte} bits for {send_dict_index[y-1][0]},\nPlease correct it in message_details file in config folder")
                        return
                    if sizeForByte == 8:
                        # print('byte complete......')
                        sizeForByte = 0
                        byteValue = self.calculateByte(non_standard_bits_values, non_standard_bits_sizes)
                        # print('byte = ',byteValue, 'bits:',bin(byteValue))
                        if byteValue == -1:
                            return
                        modified_value_list.append(byteValue)
                        modified_content_format_list.append(send_dict_index[y][5])
                        non_standard_bits_values.clear()
                        non_standard_bits_sizes.clear()
                        isPrevBits=False
            if sizeForByte != 0:
                errorDisplay.show(self.centralwidget, f"Incomplete {sizeForByte} bits at end,\nPlease correct it in message_details file in config folder")
                return
            # print('selected_byte_msg_formats: ', self.selected_byte_msg_formats)             
            # print('modified_selected_byte_msg_formats: ', self.modified_selected_byte_msg_formats)            
            # print('modified_value_list = ',modified_value_list)
            # print('modified_content_format : ',modified_content_format)
            
            # content_list = value_list[:]
            content_list = modified_value_list
            print("content modified",content_list)
            print("Format modified",modified_content_format_list)
            modified_content_format = ' '.join(map(str,modified_content_format_list[:]))
        
            formantCount = len(modified_content_format_list)
            dataCount = len(content_list)
            header_list = content_list[:len(header_format)]
            content_list = content_list[len(header_format):]
            content_format = modified_content_format[len(header_format):]
                     
        
        # Saving functionality
        if int(self.lineEditTime.text()) > 0:
            periodic_value = int(self.lineEditTime.text())
            print(f"MESSAGE IS PERIODIC AND VALUE IS {periodic_value}")
        else:
            periodic_value = 0                              
        
        #print('main sender', id(saveSendPeriodicObject))
        self.pushButtonPeriodic.show()
        self.pushButtonAddPeriodicMessage.hide()
        temp_msg_data = [config.message_selected, header_format, content_format, header_list, content_list, periodic_value]
        self.SNS.snsPeriodics.periodic_message_list.append(temp_msg_data)
        print(self.SNS.snsPeriodics.periodic_message_list)
        self.SNS.snsPeriodics.addRow(config.message_selected, self.lineEditIp.text(), self.lineEditPort.text(), periodic_value)
        self.tabWidget.setCurrentIndex(2)


    def save_edit_clicked(self, funcType):
        DBUG.printWhere()
        
        
        self.set_IP_and_socket()
        # header_format = config.header_dictionary[config.message_selected]
        header_format = ''
        content_format_list = config.modified_content_dictionary[config.message_selected] 
        content_format = ' '.join(map(str,content_format_list[:]))
        if(content_format == 'not' or content_format == ' '):
            content_format = ''
        crc_format = config.crc_dictionary[config.message_selected]
        if(crc_format == 'not'  or crc_format == ' '):
            crc_format = ''
        print('header_format:', header_format, ', content_format:', content_format, ', crc_format:',crc_format)    
        bits_format = config.bits_dictionary[config.message_selected]
        header_list = []
        content_list = []
        print("BITS FMT",bits_format)
            
            
        if bits_format == 'mt_indication_bits' or bits_format == 'indication_bits' or bits_format == 'control_bits' or bits_format == 'alarm_bits':
            header_list = header_list + self.get_header_list()
            maxRecords = 128
    
            if config.message_selected  == 'CBI_MT_INDICATION_MSG':
                maxRecords=512
            if config.message_selected == 'CBI_VDUS_INDICATION_MSG' or config.message_selected == 'VDUS_VDUD_INDICATION_MSG' or config.message_selected == 'CBI_ATS_INDICATION_MSG':
                maxRecords = 256
                
                # max_byte_number = 34
    
            max_byte_number, records_list = self.get_num_records_and_records_list(maxRecords)
            print(max_byte_number, len(records_list))
            
            content_list.append(max_byte_number)
            content_list = content_list + records_list
            print("content formats", len(content_format), content_format)
            print("header list", header_list)
            print("content list", content_list)
            crcPack = struct.pack(f'={header_format} {content_format}', *tuple(header_list), *tuple(content_list)) #for CRC on header
            #crcPack = struct.pack(f'= {content_format}', *tuple(content_list))
            crc_data = crc_calulator.crc_32(crcPack)
            content_list.append(crc_data)
            print("________________________________________",content_list)
            print("max_byte_number: ", max_byte_number)
            print("size of record: ", len(records_list))
            #self.send_and_log_message_and_update_gui(header_format+content_format+crc_format, header_list, content_list)
            

        elif bits_format == 'cbi_ratc_indication_bits' or bits_format == 'ratc_cbi_indication_bits':
            maxRecords = 128
            header_list = header_list + self.get_header_list()
            max_byte_number, records_list = self.get_num_records_and_records_list(maxRecords)
            content_list.append(max_byte_number)
            content_list = content_list + records_list
            DBUG.printDebug("content formats", content_format)
            crcPack = struct.pack(f'={header_format} {content_format}', *tuple(header_list), *tuple(content_list)) #for CRC on header
            #crcPack = struct.pack(f'= {content_format}', *tuple(content_list))
            crc_data = crc_calulator.crc_32(crcPack)
            content_list.append(crc_data)
            DBUG.printDebug("________________________________________",content_list)
            DBUG.printDebug("max_byte_number: ", max_byte_number)
            DBUG.printDebug("size of record: ", len(records_list))
            # self.send_and_log_message_and_update_gui(header_format+content_format+crc_format, header_list, content_list)

                
                
        elif bits_format == 'bytes':

            # temp_hdr_list = self.get_header_list()
            # DBUG.printDebug("hdr lst",temp_hdr_list)
            
            # header_list = header_list + temp_hdr_list

            value_list = []
            format_list = config.content_dictionary[config.message_selected]
            format_list = self.dynamic_contentFormat
            
            for i,lineEdit in enumerate(self.listLineEdits):
                value = lineEdit.text()
                if 's' in format_list[i]:
                    value = value
                elif value == '' or value == ' ':
                    # print('empty value')
                    value = 0
                elif value == 'auto':
                    value = 'auto'    
                else: 
                    value = int(value)    
                value_list.append( value )

            
            
            
            print("Dynamic Content Format List :",len(self.dynamic_contentFormat))
            
            content_format = ' '.join(map(str,self.dynamic_contentFormat))
            # self.send_and_log_message_and_update_gui(content_format, content_list)
            
            
            sizeForByte = 0
            modified_value_list = []
            non_standard_bits_values = []
            non_standard_bits_sizes = []
            bit_length_list = []
            modified_content_format_list = []
            
            for i in range(0, len(self.dict_index)):
                bit_length_list.append(self.dict_index[i][6])
       
            
            isPrevBits = False
            for y,b in enumerate(bit_length_list):
                print('b = ', b)

                
                if (b == 8 or b==0) and isPrevBits==False :
                    modified_value_list.append(value_list[y])
                    modified_content_format_list.append(self.dict_index[y][5])
                    isPrevBits=False
                    
                elif isPrevBits==True and (b==0):
                    errorDisplay.show(self.centralwidget, f"Incomplete {sizeForByte} bits for {self.dict_index[y-1][0]},\nPlease correct it in message_details file in config folder")
                    return
                
                else:
                    sizeForByte = sizeForByte + b
                    non_standard_bits_values.append(value_list[y])
                    non_standard_bits_sizes.append(b)
                    isPrevBits=True
                    if sizeForByte == 8:
                        # print('byte complete......')
                        sizeForByte = 0
                        byteValue = self.calculateByte(non_standard_bits_values, non_standard_bits_sizes)
                        # print('byte = ',byteValue, 'bits:',bin(byteValue))
                        if byteValue == -1:
                            return
                        modified_value_list.append(byteValue)
                        modified_content_format_list.append(self.dict_index[y][5])
                        non_standard_bits_values.clear()
                        non_standard_bits_sizes.clear()
                        isPrevBits=False
            if sizeForByte != 0:
                errorDisplay.show(self.centralwidget, f"Incomplete {sizeForByte} bits at end,\nPlease correct it in message_details file in config folder")
                return
            
            # content_list = value_list[:]
            content_list = modified_value_list
            print("content modified",content_list)
            print("Format modified",modified_content_format_list)
            modified_content_format = ' '.join(map(str,modified_content_format_list[:]))
        
            formantCount = len(modified_content_format_list)
            dataCount = len(content_list)
            content_str = ' '.join(map(str, self.getStringifiedMsgList(content_list)))
            
            
            
            
        
        # Saving functionality
        if int(self.lineEditTime.text()) > 0:
            periodic_value = int(self.lineEditTime.text())
            print(f"MESSAGE IS PERIODIC AND VALUE IS {periodic_value}")
        else:
            periodic_value = 0
        
        # To determine if it is edit or add(save) for Input/output message
        saveOrEdit = funcType.split(" ")[0]
        inputOrOutput = funcType.split(" ")[1]
        # print("stringified")
        # print("stringified", self.getStringifiedMsgList(header_list), type(self.getStringifiedMsgList(header_list)[1]), header_list[1])
        # print("stringified", self.getStringifiedMsgList(content_list), type(self.getStringifiedMsgList(content_list)))
        
        global GLOBAL_DELAY
        delay = GLOBAL_DELAY 
        if self.delayLineEdit.text() == "":
            pass
        else:
            delay = int(self.delayLineEdit.text())
            print("DELAY ____________ mainwindow", delay)
            
        saveEditData = mainWindow_SNS_save_edit_data(inputOrOutput, saveOrEdit, self.currentSNSEditMsdID, config.message_selected, header_format, modified_content_format, header_list, content_list, periodic_value, delay)

        
        DBUG.printInfo(f"DATA Before actually writing to csv and display =>  {saveEditData}")
        
        
        if self.SNS.setData(saveEditData):
            self.update_content(f"Format({formantCount}): {modified_content_format} \nContent({dataCount}): {content_str}")
            self.switchTabSNS(2, "", "tabs", False)
            self.currentSNSEditMsdID = -1
        else:
            DBUG.printDebug("Wrong")
            
        self.snsWidget.hide()
        self.backButton.hide()
        self.pushButtonSend.show() 
        self.pushButtonPeriodic.show()
        self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setTabEnabled(2, True)
        self.tabWidget.setTabEnabled(3, True)
        self.tabWidget.setTabEnabled(4, True)
        # except Exception as e:
        #     # self.stop_periodic_sending_if_on()
        #     self.show_error_message(str(e)+" saved Clicked")
            
            
    
    def extract_bits(self, byte, start, end, shift):
        # DBUG.printWhere()
        if start < 0 or end > 7 or start > end:
            raise ValueError('Invalid Start Or End position. Must be 0 <= start <= end <= 7')
        mask = (1 << (end - start + 1)) - 1
        # print('mask:', mask, 'bits: ', bin(mask) )
        shifted_byte = int(byte) >> shift
        # print('shifted_byte:', shifted_byte, 'bits: ', bin(shifted_byte) )
        extracted_bits = shifted_byte & mask
        # print('extracted_bits:', extracted_bits, 'bits: ', bin(extracted_bits) )
        return extracted_bits

        
    def gui_fill_content_data(self, msg_name, cData):
        DBUG.printWhere()
        content_format_list = config.modified_content_dictionary[msg_name]
        
        content_format = ' '.join(map(str,content_format_list[:-1]))
        header_format = config.header_dictionary[msg_name]
        crc_format = config.crc_dictionary[msg_name]
        bits_list = config.bits_list_dictionary[msg_name]
        bits_format = config.bits_dictionary[msg_name]
        # header_length = struct.calcsize(f'={header_format}') #getting the header length
        # num_elements_header = len(header_format.replace(' ',''))
        # header_tuple = struct.unpack(f'={header_format}',data[0:header_length]) #unpacking only header 
        # hdrList = self.getMsgListFromMsgTuple(header_tuple)
        # header_str = ' '.join(map(str,hdrList))
        
        DBUG.printDebug("header format: ", header_format)
        DBUG.printDebug("content format: ", content_format)
        DBUG.printDebug("crc format: ", crc_format)
        DBUG.printDebug("bits list: ", bits_list)
        DBUG.printDebug("bits format: ", bits_format)
    
        
        if bits_format == 'bytes':
            # print('    modified content_format list:',content_format)
            # complete_tuple = struct.unpack(f'={header_format}{content_format}{crc_format}',data[:rcv_msg_len])
            # temp_list = self.getMsgListFromMsgTuple(complete_tuple)
            # # print('content_list -> ',temp_list)
            # completeList = self.getStringifiedMsgList( temp_list )
            # content_str = ' '.join(map(str,completeList[num_elements_header:]))
            # content_sublist = completeList[num_elements_header:] 
            
            content_sublist = cData
            sizeForByte = 0
            shift = 0
            modified_value_list = []
            modified_value_dict = {}
            content_sublist_index = 0
            
            print("Bits list: ", bits_list)
            for y,b in enumerate(bits_list):
                # DBUG.printDebug('b = ', b)
                if b >= 8 :
                    print("greater equal")
                    extracted_content = content_sublist[content_sublist_index]
                    if type(extracted_content) == bytes: 
                        extracted_content = extracted_content.decode('utf-8')
                        print("Extracted content >>>>>>>>>>", extracted_content, type(extracted_content))
                    modified_value_list.append(extracted_content)
                    content_sublist_index += 1
                else:
                    sizeForByte = sizeForByte + b
                    byteValue = content_sublist[content_sublist_index]
                    # binaryByteValue = bin(byteValue)
                    # DBUG.printDebug('binaryByteValue: ', byteValue)
                    start = 8 - sizeForByte
                    end = start + b - 1
                    shift = sizeForByte - b
                    extracted_content = self.extract_bits(byteValue, start, end, shift)
                    # print('b size:', b, ', Start:', start, ', End:', end,', extracted_bit_content', extracted_content)
                    print(b, " == > extracted content - > ", extracted_content)
                    # if isinstance(extracted_content, (bytes, bytearray)):
                    #     extracted_content = extracted_content.decode("utf-8")
                    # else:
                    #     extracted_content = extracted_content
                        
                    modified_value_list.append(extracted_content)
                    # print("Extracted content >>>>>>>>>>", extracted_content, type(extracted_content), extracted_content.decode("utf-8"))
                    # extracted_content.decode("utf-8")
                    if sizeForByte == 8:
                        # print('byte complete......')
                        sizeForByte = 0
                        content_sublist_index += 1
            DBUG.printDebug('Modified_value_list -> ',modified_value_list)
            return modified_value_list
            
        #     if(msg_name == config.message_selected):
        #         #Rigzin 24/12/2024 Adding new datatype to store the header_str and content_str as dictionary where key is message_name
        #         if self.previous_received_message == msg_name:
        #             config.selected_message_status_on_receiver = 1
        #         self.previous_received_message = msg_name
                
        #         header_dict[msg_name] = header_str
        #         content_dict[msg_name] = content_str
        #         modified_value_dict[msg_name] = modified_value_list
        #         #End
                
        #         config.update_display_header(header_dict)
        #         config.update_display_content(content_dict)
        #         config.update_bytes_display_content(modified_value_dict) 
    
        #         # labels_list = config.labels_list_dictionary[msg_name]
        #         # print(' ')
        #         # print('VVV******************* START OF MESSAGE ********************VVV')
        #         # print('For Message Name:',msg_name)
        #         # for i,label in enumerate(labels_list):
        #         #     print('    ', label,' : ',modified_value_list[i]) 
        #         # print('^^^******************** END OF MESSAGE **********************^^^')  
            
        elif(bits_format == 'ratc_cbi_indication_bits' or bits_format == 'cbi_ratc_indication_bits' or bits_format == 'indication_bits' or bits_format == 'mt_indication_bits' or bits_format == 'control_bits' or bits_format == 'alarm_bits') :

            # header_length = struct.calcsize(f'={header_format}') #getting the header length
            # content_length = struct.calcsize(f'={content_format}') #getting the content length    
            # msg_len = header_length + content_length + 4  #4 is CRC length
            # print('msg_len:',msg_len, ', header_format:',header_format, ', content_format:',content_format)
    
            # complete_tuple = struct.unpack(f'={header_format}{content_format}{crc_format}',cData)
            # temp_list = self.getMsgListFromMsgTuple(complete_tuple)
            # print('temp_list -> ',temp_list)
            # completeList = self.getStringifiedMsgList( temp_list )
            # content_str = ' '.join(map(str,completeList[num_elements_header:]))
            # content_sublist = completeList[num_elements_header:]
            # records = completeList[num_elements_header + 1 : len(completeList)-1]
            
            records = cData[1:-1]
            print('records -> ',records)
            bitPositionList = []
            bitPositionList_dict = {}
            for i,x in enumerate(records):
                if records[i] != 0:
                    print(records[i], type(records[i]))
                    for j in range(7, -1, -1):
                        bit = (records[i]>> j) & 1
                        if bit == 1:
                            bitPositionList.append((i*8)+j)
                            print((i*8)+j)
                            # print('bitPositionList:',bitPositionList)
            print('Final bitPositionList:',bitPositionList)
            return bitPositionList
            # if(msg_name == config.message_selected):
            #     #Rigzin 24/12/2024 Adding new datatype to store the header_str and content_str as dictionary where key is message_name
            #     if self.previous_received_message == msg_name:
            #         config.selected_message_status_on_receiver = 1    
            #     self.previous_received_message = msg_name
                
            #     header_dict[msg_name] = header_str
            #     content_dict[msg_name] = content_str
            #     bitPositionList_dict[msg_name]= bitPositionList
            #     config.update_display_header(header_dict)
            #     config.update_display_content(content_dict)
            #     config.update_set_bit_list_msg_id_for_display(bitPositionList_dict, msg_id)
                
            # else:
            #     print('MSG NOT Identifiable...')
            #     header_format = config.header_formats[0]
            #     header_length = struct.calcsize(f'={header_format}') #getting the header length
            #     header_tuple = struct.unpack(f'={header_format}',data[0:header_length]) #unpacking only header 
            #     hdrList = self.getMsgListFromMsgTuple(header_tuple)
            #     header_str = ' '.join(map(str,hdrList)) 
            # # except Exception as e:
            #     self.show_error_message(str(e))

    def skipRecursion(self, i, struct_to_be_repeated):
        non_repeating_struct = self.dyanamicStructre[struct_to_be_repeated]
        for item in non_repeating_struct:
            if NESTED_STRUCT_IDENTIFIER in item["name"]:
                i = self.skipRecursion(i, item["name"])
            else:
                i+=1
        return i

    def recursive_struct(self, i, shadow_default_message_data, cData, new_message_data, data_i): 
        print("################################## RECURSION #################################################")
        struct_to_be_repeated = shadow_default_message_data[i][2]  
        pos_of_repeat_structure = i+1
        
        # label_string = shadow_dict_index[i][8].split('.')
        # struct_format.append(shadow_dict_index[i][5])
        # label_format.append(shadow_dict_index[i][0])
        # button_sign.append("+")
        # attr_struct.append(shadow_dict_index[i][8])
        

        no_of_repeatitions = cData[data_i-1]
        print("Current Attribute:", shadow_default_message_data[i][0] , "No of repetations:",no_of_repeatitions, " From index:", i, " Struct to be repeated:", struct_to_be_repeated)

        if no_of_repeatitions > 0:
            for idx in range(0, no_of_repeatitions):
                i = pos_of_repeat_structure   
                byteValue = 0    
                while True:
                    if i>=len(shadow_default_message_data): 
                        break
                    if (struct_to_be_repeated not in shadow_default_message_data[i][8].split('.')):
                        break
                    print("processing", shadow_default_message_data[i])
                    current_attr_parent_sturcts = shadow_default_message_data[i][8].split('.')
                    # if (struct_to_be_repeated in current_attr_parent_sturcts and shadow_default_message_data[i][2] == ''):
                        
                    if shadow_default_message_data[i][6]!=0:
                        byteValue = cData[data_i]
                        bits_list = []
                        sizeForByte = 0
                        j=i
                        
                        while j<len(shadow_default_message_data):
                            print("processing", shadow_default_message_data[i])
                            sizeForByte+=shadow_default_message_data[j][6]
                            bits_list.append(shadow_default_message_data[j][6])
                            new_message_data.append(shadow_default_message_data[j])
                            if sizeForByte == 8:
                                extracted_bits_list_from_byte = get_bits_from_bytes(bits_list, byteValue)
                                leftData = cData[0:data_i]
                                rightData = cData[data_i+1:]
                                cData.clear()
                                cData = leftData+extracted_bits_list_from_byte+rightData
                                data_i = (data_i + len(extracted_bits_list_from_byte))
                                i = j
                                break   
                            j+=1
                    else:
                         new_message_data.append(shadow_default_message_data[i])
                         data_i+=1

                    if (shadow_default_message_data[i][2] != '' and struct_to_be_repeated in current_attr_parent_sturcts):
                        i, data_i, cData, shadow_default_message_data = self.recursive_struct(i, shadow_default_message_data, cData, new_message_data, data_i)
                    else:    
                        i+=1
        else:
            i=i+1
            i = self.skipRecursion(i, struct_to_be_repeated)
                
                
                
        return i, data_i, cData, shadow_default_message_data
    
    

    def refill_gui(self, data_format, data_label, data_value, button_sign, attr_struct):
        print("Reloading", len(data_format), len(data_label), len(data_value), len(button_sign), len(attr_struct))
        # print("------------------------------------>", data_label)
        # self.strucChkBox.setChecked(False)
        
        for k,chkBox in enumerate(self.listCheckBox):
            chkBox.setParent(None)
            chkBox.deleteLater()
            chkBox= None
        self.listCheckBox.clear()
        
        for label in self.listLabels:
            label.setParent(None)
            label.deleteLater()
            label= None
        self.listLabels.clear()
        
        for lineEdit in self.listLineEdits:
            lineEdit.setParent(None)
            lineEdit.deleteLater()
            lineEdit= None
        self.listLineEdits.clear()
        
        for h_label in self.header_labels:
            h_label.setParent(None)
            h_label.deleteLater()
            h_label = None
        self.header_labels.clear()
        
        for h_linedit in self.header_lineEdit:
            h_linedit.setParent(None)
            h_linedit.deleteLater()
            h_linedit= None
        self.header_lineEdit.clear()
        
        for DButton in self.listDyanamicVaribleButton:
            DButton.setParent(None)
            DButton.deleteLater()
            DButton= None
        self.listDyanamicVaribleButton.clear()
        
        for EButton in self.listExpandButton:
            EButton.setParent(None)
            EButton.deleteLater()
            EButton= None
        self.listExpandButton.clear()
        
        self.selected_byte_msg_formats.clear()
        self.modified_selected_byte_msg_formats.clear()
        self.selected_msg_bit_lengths.clear()
        # self.dict_index.clear()
        self.dict_index = csv_dict[f'{config.message_selected}'].copy()
        self.bit_list = []
        
        for i,item in enumerate(self.dict_index):
            print(item)
            self.bit_list.append(item[6])
        print("BIT LIST",self.bit_list)
        
        content_format_list = data_format
        content_format_string = ' '.join(map(str,self.getStringifiedMsgList(content_format_list)))
        self.dynamic_contentFormat = content_format_list.copy()
    
        if config.message_selected == 'RATC_CBI_INDICATION_MSG':
            self.listCheckBox = config.ratc_cbi_indication_bit_names.copy()
            self.rows = int(len(self.listCheckBox) / self.columns)
            rowCount = 0 
            colCount = 0
            for i,x in enumerate(self.listCheckBox):
                self.listCheckBox[i] = QtWidgets.QCheckBox(str(i)+' '+x)
                self.listCheckBox[i].setStyleSheet("QCheckBox::checked"
                                                    "{"
                                                    "background-color : pink;"
                                                    "}"
                    )
                self.containerLayout.addWidget(self.listCheckBox[i], rowCount, colCount)
                rowCount = rowCount + 1
                if rowCount == self.rows:
                    rowCount = 0
                    colCount = colCount + 1 
                    
        elif config.message_selected == 'CBI_RATC_INDICATION_MSG':
            self.listCheckBox = config.cbi_ratc_indication_bit_names.copy()
            self.rows = int(len(self.listCheckBox) / self.columns)
            rowCount = 0 
            colCount = 0
            for i,x in enumerate(self.listCheckBox):
                self.listCheckBox[i] = QtWidgets.QCheckBox(str(i)+' '+x)
                self.listCheckBox[i].setStyleSheet("QCheckBox::checked"
                                                    "{"
                                                    "background-color : pink;"
                                                    "}"
                    )
                self.containerLayout.addWidget(self.listCheckBox[i], rowCount, colCount)
                rowCount = rowCount + 1
                if rowCount == self.rows:
                    rowCount = 0
                    colCount = colCount + 1  
    
        elif config.bits_dictionary[config.message_selected] == 'bytes':
            labels_list = data_label
            self.rows = len(labels_list)
            self.listLabels = labels_list.copy()
            self.listLineEdits = labels_list.copy()
            self.listDyanamicVaribleButton = labels_list.copy()
            self.listExpandButton = labels_list.copy()
            self.attr_stuct_details = labels_list.copy()
            rowCount = 0
            
            # track_var = config.message_selected.split("_")
                
            # self.dict_index = csv_dict[f'{config.message_selected}']
            print("DICT",len(self.dict_index))
            for i,x in enumerate(labels_list):
                self.listLabels[i] = QtWidgets.QLabel()
                self.listLabels[i].setText(x)
                self.listLabels[i].setFixedWidth(200)
                self.listLabels[i].setStyleSheet("""
                                                 QLabel{ padding-left: 10px; 
                                                          padding-right:10px;
                                                          background-color: #e0e0e0;}
                                                 QToolTip{ color:#ffffff; background-color:#2a82da;
                                                          border: 1px solid black;
                                                          padding:10px;}
                                                 QLabel:hover{background-color:lightblue;border: 1px solid black;}""")
                # hover
                # self.listLabels[i].setToolTip(self.dict_index[i][7].replace("_x000D_",""))
                # self.listLabels[i].setToolTipDuration(50000)
                # self.listLabels[i].setStyleSheet("""QLable { padding-left: 10px; padding-right:10px; } QToolTip{ color:#ffffff; background-color:#2a82da;
                #         border: 1px solid black;
                #         padding:10px;}QLabel:hover{background-color:lightblue;border: 1px solid black;}""")
                self.listLineEdits[i] = QtWidgets.QLineEdit()
                self.listLineEdits[i].setFixedWidth(100)  
                self.listLineEdits[i].setText(str(data_value[i]))
    
                dyanamicBtn = QtWidgets.QPushButton(button_sign[i])
                dyanamicBtn.setEnabled(False)
                            
                if(button_sign[i] == "+"):
                    dyanamicBtn.setEnabled(True)
                #     self.listLineEdits[i].setText('1')        
                
                # if(self.dict_index[i][2] != ''):
                #     dyanamicBtn.setEnabled(True)  
                
                self.listDyanamicVaribleButton[i] = dyanamicBtn
                btnObjName = str(i)
                self.listDyanamicVaribleButton[i].setObjectName(btnObjName)
                self.listDyanamicVaribleButton[i].setFixedWidth(50) 
                
                
                
                expandBtn = QtWidgets.QPushButton('+')
                expandBtn.setEnabled(False)
                expandBtn.setFixedWidth(20)
                            
                if(self.dict_index[i][9] != ''):
                    expandBtn.setEnabled(True)
                
                if(self.dict_index[i][2] != ''):
                    dyanamicBtn.setEnabled(True)  
                
                self.listExpandButton[i] = expandBtn
                btnObjName = str(i)
                self.listExpandButton[i].setObjectName(btnObjName)
                self.listExpandButton[i].setFixedWidth(50)
                # dyanamicBtn.clicked.connect(lambda _,btnobjName=dyanamicBtn.objectName(): dyanamicUpdate(self,btnobjName,ui))
                
                # if(i == 2):  #Automatically filling MSG ID
                #     msg_id = config.id_dictionary[config.message_selected]
                #     self.listLineEdits[i].setText(str(int(msg_id)))  #4 is index of MSG ID
                    
                # if(i == 5):    
                #     content_format_list = config.modified_content_dictionary[config.message_selected]
                #     content_format_string = ' '.join(map(str,getStringifiedMsgList(content_format_list)))
                #     content_length = 0
                #     if(len(content_format_list) != 0):
                #         content_length = struct.calcsize(f'={content_format_string}') #getting the content length    
                #     msg_len = content_length 
                    
                #     self.listLineEdits[i].setText(str(msg_len))  #5 is index ID of MSG LEN
                    
                # if(i == 9):
                #     self.listLineEdits[9].setText(str(1)) #By defalult no of dest nodes is 1
    
                rowCount = rowCount + 1
                
        
        content_format_list = config.content_dictionary[config.message_selected]
        print("LIST Cntnt frmt",content_format_list)
        self.attr_stuct_details.clear()
        self.attr_stuct_details = attr_struct
        self.refresh_gui()
        
        # elif config.bits_dictionary[config.message_selected] == 'bytes':
        #     labels_list = config.labels_list_dictionary[config.message_selected]
        #     self.rows = len(labels_list)
        #     self.listLabels = labels_list.copy()
        #     self.listLineEdits = labels_list.copy()
        #     self.listDyanamicVaribleButton = labels_list.copy()
        #     self.attr_stuct_details = labels_list.copy()
        #     rowCount = 0
            
        #     # track_var = config.message_selected.split("_")
                
        #     # self.dict_index = csv_dict[f'{config.message_selected}']
        #     print("DICT",len(self.dict_index))
        #     for i,x in enumerate(labels_list):
        #         self.attr_stuct_details[i]=self.dict_index[i][8]
                
        #         self.listLabels[i] = QtWidgets.QLabel()
        #         self.listLabels[i].setText(x)
        #         self.listLabels[i].setFixedWidth(200)
        #         # widget.setStyleSheet("background-color: pink;")
        #         # hover
        #         self.listLabels[i].setToolTip(self.dict_index[i][7].replace("_x000D_",""))
        #         self.listLabels[i].setToolTipDuration(50000)
        #         self.listLabels[i].setStyleSheet("""
        #                                          QLabel{ padding-left: 10px; 
        #                                                   padding-right:10px;
        #                                                   background-color: #e0e0e0;}
        #                                          QToolTip{ color:#ffffff; background-color:#2a82da;
        #                                                   border: 1px solid black;
        #                                                   padding:10px;}
        #                                          QLabel:hover{background-color:lightblue;border: 1px solid black;}""")
        #         self.listLineEdits[i] = QtWidgets.QLineEdit()
        #         self.listLineEdits[i].setFixedWidth(100)       
    
        #         dyanamicBtn = QtWidgets.QPushButton('+')
        #         dyanamicBtn.setEnabled(False)
        #         dyanamicBtn.setFixedWidth(20)
                            
        #         if(self.dict_index[i][9] != ''):
        #             dyanamicBtn.setEnabled(True)
        #             self.listLineEdits[i].setText('1')
        #             self.repeating_structs_names_list.append(x)
                
        #         if(self.dict_index[i][2] != ''):
        #             dyanamicBtn.setEnabled(True)  
                
        #         self.listDyanamicVaribleButton[i] = dyanamicBtn
        #         btnObjName = str(i)
        #         self.listDyanamicVaribleButton[i].setObjectName(btnObjName)
        #         self.listDyanamicVaribleButton[i].setFixedWidth(50) 
        #         # dyanamicBtn.clicked.connect(lambda _,btnobjName=dyanamicBtn.objectName(): dyanamicUpdate(self,btnobjName,ui))
                
        #         if(i == 2):  #Automatically filling MSG ID
        #             msg_id = config.id_dictionary[config.message_selected]
        #             self.listLineEdits[i].setText(str(int(msg_id)))  #4 is index of MSG ID
                    
        #         # if(i == 5):    
        #         #     content_format_list = config.modified_content_dictionary[config.message_selected]
        #         #     content_format_string = ' '.join(map(str,getStringifiedMsgList(content_format_list)))
        #         #     content_length = 0
        #         #     if(len(content_format_list) != 0):
        #         #         content_length = struct.calcsize(f'={content_format_string}') #getting the content length    
        #         #     msg_len = content_length 
                    
        #         #     self.listLineEdits[i].setText(str(msg_len))  #5 is index ID of MSG LEN
                    
        #         # if(i == 9):
        #         #     self.listLineEdits[9].setText(str(1)) #By defalult no of dest nodes is 1
    
        #         rowCount = rowCount + 1
                
        
        # content_format_list = config.content_dictionary[config.message_selected]
        # print("LIST Cntnt frmt",content_format_list)
            
        # # print("Initial Count", len(self.listLabels))
        # # content_format_string = ' '.join(map(str,getStringifiedMsgList(content_format_list)))
        # print("CONTENT",type(content_format_list))
        
        # # print("CONTENT INDEX",self.content_format_index)
        
        # content_length = 0
        # if(len(content_format_list) != 0):
        #     content_length = struct.calcsize(f'={content_format_string}') #getting the content length    
        
        # # print('header_length',header_length,' content_length',content_length)
        # msg_id = config.id_dictionary[config.message_selected]
        # msg_len = content_length # + 4  #4 is CRC length
        # print("MSG_ID",config.message_selected)
        # msg_seq = 1 
        
        # header_string = config.header_values_dictionary[config.message_selected]
        # datetime_now = datetime.datetime.now()
        # day = datetime_now.day
        # month = datetime_now.month
        # year = datetime_now.year
        # hour = datetime_now.hour
        # minute = datetime_now.minute
        # seconds = datetime_now.second
        # milli_seconds = math.floor(datetime_now.microsecond / 1000)
        # unique_message_code = 1
        # # header_string += (f' {msg_id} {msg_len} {msg_seq} {day} {month} {year} {hour} {minute} {seconds} {milli_seconds} {unique_message_code}')
        # print('header_string = ', header_string)
        
        
        
        
        
    def edit_message_reload_gui(self, messageDetails, fromPage):
        DBUG.printWhere()
        
        DBUG.printDebug("received message data", messageDetails)
        
        config.message_selected = messageDetails.message
        
        self.comboBoxMessages.blockSignals(True)
        self.comboBoxMessages.setCurrentText(config.message_selected)
        self.comboBoxMessages.blockSignals(False)
        
        self.lineEditTime.setText(str(int(messageDetails.periodicity)))
        if int(messageDetails.delay) <= 0:
            self.delayLineEdit.setText("")
        else:
            self.delayLineEdit.setText(str(int(messageDetails.delay)))
        
        DBUG.printDebug("checking the type of the Header data: ", type(messageDetails.HeaderData),type(messageDetails.HeaderData[1:-1]))
        
        
        
        hData = messageDetails.HeaderData.copy()
        cData = messageDetails.InputData.copy()
        self.currentSNSEditMsdID = messageDetails.messageIdenitifer
        
        print("cData ", cData)
        print("messageDetails.InputData ", messageDetails.InputData)
        
        new_message_data = []
        shadow_default_message_data = csv_dict[config.message_selected].copy()
        
        index_after_recursion = -1
        data_i = 0
        i = 0
        
        while (i<len(shadow_default_message_data)):
            print("processing", shadow_default_message_data[i])
            if i <= index_after_recursion-1:
                continue
            else:
                if shadow_default_message_data[i][6]!=0:
                    byteValue = cData[data_i]
                    bits_list = []
                    sizeForByte = 0
                    j=i
                    
                    while j<len(shadow_default_message_data):
                        print("processing", shadow_default_message_data[i])
                        sizeForByte+=shadow_default_message_data[j][6]
                        bits_list.append(shadow_default_message_data[j][6])
                        new_message_data.append(shadow_default_message_data[j])
                        if sizeForByte == 8:
                            extracted_bits_list_from_byte = get_bits_from_bytes(bits_list, byteValue)
                            leftData = cData[0:data_i]
                            rightData = cData[data_i+1:]
                            cData.clear()
                            cData = leftData+extracted_bits_list_from_byte+rightData
                            data_i = (data_i + len(extracted_bits_list_from_byte))
                            i = j
                            break
                        j+=1
                else:
                     new_message_data.append(shadow_default_message_data[i])
                     data_i+=1
                     
                        
                if(shadow_default_message_data[i][2] != ''):
                    try:
                        i, data_i, cData, shadow_default_message_data = self.recursive_struct(i, shadow_default_message_data, cData, new_message_data, data_i)
                        index_after_recursion = i
                    except Exception as e:
                        print("Recursion error",e)
                        
                        
                    

                    print("*************************+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print("Recursion output",len(new_message_data), len(shadow_default_message_data), len(cData), index_after_recursion)
                    print("*************************+++++++++++++++++++++++++++++++++++++++++++++++++++++")
                else:
                    i+=1
                # data_i += 1   
                    # If not structure
                    # print("NoN recursion attribute ======= ",i, shadow_default_message_data[i][5])
                    # attribute_format = shadow_default_message_data[i][5]
                    # attribute_label = shadow_default_message_data[i][0]
                    # print("Current attribute format and label ------", attribute_format, attribute_label)
                    
                    # label_format.append(attribute_label)
                    # button_sign.append("-")
                    # struct_format.append(attribute_format) 
                    # attr_struct.append(shadow_default_message_data[i][8])  
            
        
        print("*************************+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("DATA BEFORE REFILL")
        print(len(new_message_data), len(shadow_default_message_data), len(cData))
        for ind, items in enumerate(new_message_data):
            print(i, items[0])   
        print("*************************+++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        # for items in shadow_default_message_data:
        #     print items[6]
        
        self.switchTabSNS(1, "edit", fromPage, False)
        self.reload_gui(new_message_data, cData)
        
        
        # self.refill_gui(struct_format, label_format, self.cData, button_sign, attr_struct)
        
          
        
        
        
    def backClicked(self):
        print("back clicked from sender")
        self.switchTabSNS(2,"", "tabs", False)
        self.snsWidget.hide()
        self.backButton.hide()
        self.pushButtonSend.show() 
        self.pushButtonPeriodic.show()
        self.tabWidget.setTabEnabled(0, True)
        self.tabWidget.setTabEnabled(2, True)
        self.tabWidget.setTabEnabled(3, True)
        self.tabWidget.setTabEnabled(4, True)