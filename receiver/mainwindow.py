# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui, QtWidgets
from Configuration import config
import xml.etree.ElementTree as ET
from datetime import datetime
import struct
import readLog
from ReplayThread import ReplayThread
from Datastore import datastore
from udpsender import UdpSender
import subprocess
from UserInputDialog import UserInputDialog
from csv_dict import dict
from send_clicked import send_selected
from searchTab import searchTab,searchButtonHandle
from byteDataParsing import byte_data_parsing
from validate import validate_file
from graph_plots.graph_tab import GraphTab
from graph_plots.message_analytics import MessageAnalytics

tree = ET.parse('config/configuration.xml')
root = tree.getroot()
file_path = './blocked_msgs/file.txt'
        
def getStringifiedMsgList(input_list):
    msg_list = []
    for x in range(len(input_list)):
        if(isinstance(input_list[x], bytes)):
            string = input_list[x].decode('utf-8').rstrip('\x00')
            msg_list.append(string)
        else:   
            msg_list.append(input_list[x])
    return msg_list
     

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1477, 784)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # self.centralwidget.setStyleSheet("background-color: lightblue;")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButtonReceiver = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonReceiver.setObjectName("pushButtonReceiver")
        self.horizontalLayout_5.addWidget(self.pushButtonReceiver)
        self.pushButtonDockableReceiver = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonDockableReceiver.setObjectName("pushButtonDockableReceiver")
        self.horizontalLayout_5.addWidget(self.pushButtonDockableReceiver)
        self.lineEditInfo = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditInfo.setEnabled(False)
        self.lineEditInfo.setText("")
        self.lineEditInfo.setObjectName("lineEditInfo")
        self.horizontalLayout_5.addWidget(self.lineEditInfo)
        self.labelReplayIp = QtWidgets.QLabel(self.centralwidget)
        self.labelReplayIp.setEnabled(True)
        self.labelReplayIp.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelReplayIp.setObjectName("labelReplayIp")
        self.horizontalLayout_5.addWidget(self.labelReplayIp)
        self.lineEditReplayIp = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditReplayIp.setEnabled(True)
        self.lineEditReplayIp.setObjectName("lineEditReplayIp")
        self.horizontalLayout_5.addWidget(self.lineEditReplayIp)
        self.labelReplayPort = QtWidgets.QLabel(self.centralwidget)
        self.labelReplayPort.setEnabled(True)
        self.labelReplayPort.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelReplayPort.setObjectName("labelReplayPort")
        self.horizontalLayout_5.addWidget(self.labelReplayPort)
        self.lineEditReplayPort = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditReplayPort.setEnabled(True)
        self.lineEditReplayPort.setText("")
        self.lineEditReplayPort.setObjectName("lineEditReplayPort")
        self.horizontalLayout_5.addWidget(self.lineEditReplayPort)
        self.pushButtonReplaySetIpPort = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonReplaySetIpPort.setEnabled(True)
        self.pushButtonReplaySetIpPort.setObjectName("pushButtonReplaySetIpPort")
        self.horizontalLayout_5.addWidget(self.pushButtonReplaySetIpPort)
        
        
        self.validateBtn = QtWidgets.QPushButton(self.centralwidget)
        self.validateBtn.setEnabled(True)
        self.validateBtn.setObjectName("validateBtn")
        self.horizontalLayout_5.addWidget(self.validateBtn)
        
        self.pushButtonExit = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonExit.setEnabled(True)
        self.pushButtonExit.setObjectName("pushButtonExit")
        self.horizontalLayout_5.addWidget(self.pushButtonExit)
        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 9)
        self.horizontalLayout_5.setStretch(3, 1)
        self.horizontalLayout_5.setStretch(4, 3)
        self.horizontalLayout_5.setStretch(5, 1)
        self.horizontalLayout_5.setStretch(6, 1)
        self.horizontalLayout_5.setStretch(7, 1)
        self.horizontalLayout_5.setStretch(8, 1)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabSingleSample = QtWidgets.QWidget()
        self.tabSingleSample.setObjectName("tabSingleSample")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tabSingleSample)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelSingleSample = QtWidgets.QLabel(self.tabSingleSample)
        self.labelSingleSample.setObjectName("labelSingleSample")
        self.horizontalLayout.addWidget(self.labelSingleSample)
        self.comboBoxMessages = QtWidgets.QComboBox(self.tabSingleSample)
        self.comboBoxMessages.setObjectName("comboBoxMessages")
        self.horizontalLayout.addWidget(self.comboBoxMessages)
	
	
        # 9-01-2025 
        
        #spacer 
        self.spacerH = QtWidgets.QSpacerItem(40,20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(self.spacerH)
        
        #search button
        self.searchMessageFields = QtWidgets.QLineEdit(self.tabSingleSample)
        self.searchMessageFields.setObjectName("searchMessageFields")
        self.searchMessageFields.setPlaceholderText("Search")
        self.horizontalLayout.addWidget(self.searchMessageFields)
        self.searchMessageFields.textChanged.connect(self.searchMessage)
        
        # 09-01-2025 message status label
        self.labelHeaderSingleSample = QtWidgets.QLabel(self.tabSingleSample)
        self.labelHeaderSingleSample.setObjectName("labelHeaderSingleSample")
        self.horizontalLayout.addWidget(self.labelHeaderSingleSample)
        

        # self.lineEditHeader = QtWidgets.QLineEdit(self.tabSingleSample)
        # self.lineEditHeader.setText("")
        # self.lineEditHeader.setObjectName("lineEditHeader")
        # self.horizontalLayout.addWidget(self.lineEditHeader)
        self.horizontalLayout.setStretch(1, 3)
        self.horizontalLayout.setStretch(3, 4)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.scrollAreaHeader = QtWidgets.QScrollArea(self.tabSingleSample)
        self.scrollAreaHeader.setWidgetResizable(True)
        self.scrollAreaHeader.setObjectName("scrollAreaHeader")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 202, 600))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollAreaHeader.setWidget(self.scrollAreaWidgetContents_2)
        self.horizontalLayout_6.addWidget(self.scrollAreaHeader)
        self.scrollArea = QtWidgets.QScrollArea(self.tabSingleSample)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1219, 600))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_6.addWidget(self.scrollArea)
        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 6)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.lineEditContent = QtWidgets.QLineEdit(self.tabSingleSample)
        self.lineEditContent.setObjectName("lineEditContent")
        self.verticalLayout.addWidget(self.lineEditContent)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tabSingleSample, "")
        self.tabMultiSample = QtWidgets.QWidget()
        self.tabMultiSample.setObjectName("tabMultiSample")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tabMultiSample)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelMultiSample = QtWidgets.QLabel(self.tabMultiSample)
        self.labelMultiSample.setObjectName("labelMultiSample")
        self.horizontalLayout_3.addWidget(self.labelMultiSample)
        self.comboBoxMessagesMultiSample = QtWidgets.QComboBox(self.tabMultiSample)
        self.comboBoxMessagesMultiSample.setObjectName("comboBoxMessagesMultiSample")
        self.horizontalLayout_3.addWidget(self.comboBoxMessagesMultiSample)
        self.horizontalLayout_3.setStretch(1, 3)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.tableViewMultipleSamples = QtWidgets.QTableView(self.tabMultiSample)
        self.tableViewMultipleSamples.setObjectName("tableViewMultipleSamples")
        self.gridLayout_3.addWidget(self.tableViewMultipleSamples, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tabMultiSample, "")
        self.tabAllSamples = QtWidgets.QWidget()
        self.tabAllSamples.setObjectName("tabAllSamples")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tabAllSamples)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButtonOpenSelected = QtWidgets.QPushButton(self.tabAllSamples)
        self.pushButtonOpenSelected.setObjectName("pushButtonOpenSelected")
        self.horizontalLayout_4.addWidget(self.pushButtonOpenSelected)
        self.pushButtonFilter = QtWidgets.QPushButton(self.tabAllSamples)
        self.pushButtonFilter.setObjectName("pushButtonFilter")
        self.horizontalLayout_4.addWidget(self.pushButtonFilter)
        self.pushButtonLiveOffline = QtWidgets.QPushButton(self.tabAllSamples)
        self.pushButtonLiveOffline.setObjectName("pushButtonLiveOffline")
        self.horizontalLayout_4.addWidget(self.pushButtonLiveOffline)
        self.labelStart = QtWidgets.QLabel(self.tabAllSamples)
        self.labelStart.setEnabled(False)
        self.labelStart.setObjectName("labelStart")
        self.horizontalLayout_4.addWidget(self.labelStart)
        # self.dateTimeEditStart = QtWidgets.QDateTimeEdit(self.tabAllSamples)
        # self.dateTimeEditStart.setEnabled(False)
        # self.dateTimeEditStart.setObjectName("dateTimeEditStart")
        # self.horizontalLayout_4.addWidget(self.dateTimeEditStart)
        self.labelEnd = QtWidgets.QLabel(self.tabAllSamples)
        self.labelEnd.setEnabled(False)
        self.labelEnd.setObjectName("labelEnd")
        self.horizontalLayout_4.addWidget(self.labelEnd)
        # self.searchFeild = QtWidgets.QLineEdit(self.tabAllSamples)
        # self.searchFeild.setEnabled(True)
        # self.searchFeild.setObjectName("searchFeild")
        # self.searchFeild.setPlaceholderText("Search Message Name")
        # self.horizontalLayout_4.addWidget(self.searchFeild)
        
        self.blockedComboBoxMessages = QtWidgets.QComboBox(self.tabSingleSample)
        self.blockedComboBoxMessages.setObjectName("blockedComboBoxMessages")
        self.horizontalLayout_4.addWidget(self.blockedComboBoxMessages)
        
        
        self.pushButtonLoad = QtWidgets.QPushButton(self.tabAllSamples)
        self.pushButtonLoad.setEnabled(True)
        self.pushButtonLoad.setObjectName("pushButtonLoad")
        self.horizontalLayout_4.addWidget(self.pushButtonLoad)
        self.gridLayout_4.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        # self.checkBoxTimestampUpdated = QtWidgets.QCheckBox(self.tabAllSamples)
        # self.checkBoxTimestampUpdated.setEnabled(False)
        # self.checkBoxTimestampUpdated.setObjectName("checkBoxTimestampUpdated")
        
        self.msgCountLineEdit = QtWidgets.QLabel(self.tabAllSamples)
        self.msgCountLineEdit.setObjectName("msgCountLineEdit")
        
        self.horizontalLayout_2.addWidget(self.msgCountLineEdit)
        
        # self.pushButtonSendSelected = QtWidgets.QPushButton(self.tabAllSamples)
        # self.pushButtonSendSelected.setEnabled(False)
        # self.pushButtonSendSelected.setObjectName("pushButtonSendSelected")
        # self.horizontalLayout_2.addWidget(self.pushButtonSendSelected)
        self.labelTimeGap = QtWidgets.QLabel(self.tabAllSamples)
        self.labelTimeGap.setEnabled(False)
        self.labelTimeGap.setObjectName("labelTimeGap")
        self.horizontalLayout_2.addWidget(self.labelTimeGap)
        # self.lineEditTimeGap = QtWidgets.QLineEdit(self.tabAllSamples)
        # self.lineEditTimeGap.setEnabled(False)
        # self.lineEditTimeGap.setObjectName("lineEditTimeGap")
        # self.horizontalLayout_2.addWidget(self.lineEditTimeGap)
        # self.pushButtonSpeed = QtWidgets.QPushButton(self.tabAllSamples)
        # self.pushButtonSpeed.setEnabled(False)
        # self.pushButtonSpeed.setObjectName("pushButtonSpeed")
        # self.horizontalLayout_2.addWidget(self.pushButtonSpeed)
        
        self.unBlockedComboBoxMessages = QtWidgets.QComboBox(self.tabSingleSample)
        self.unBlockedComboBoxMessages.setObjectName("unBlockedComboBoxMessages")
        self.unBlockedComboBoxMessages.setEditable(True)
        self.horizontalLayout_2.addWidget(self.unBlockedComboBoxMessages)
        
        
        self.unBlockButton = QtWidgets.QPushButton(self.tabAllSamples)
        self.unBlockButton.setEnabled(True)
        self.unBlockButton.setObjectName("unBlockButton")
        self.horizontalLayout_2.addWidget(self.unBlockButton)
        # self.pushButtonPauseResume = QtWidgets.QPushButton(self.tabAllSamples)
        # self.pushButtonPauseResume.setEnabled(False)
        # self.pushButtonPauseResume.setObjectName("pushButtonPauseResume")
        # self.horizontalLayout_2.addWidget(self.pushButtonPauseResume)
        self.horizontalLayout_2.setStretch(2, 2)
        self.horizontalLayout_2.setStretch(3, 2)
        self.horizontalLayout_2.setStretch(4, 2)
        self.horizontalLayout_2.setStretch(5, 2)
        self.horizontalLayout_2.setStretch(6, 2)
        self.gridLayout_4.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.tableView = QtWidgets.QTableView(self.tabAllSamples)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.AnyKeyPressed|QtWidgets.QAbstractItemView.DoubleClicked|QtWidgets.QAbstractItemView.EditKeyPressed)
        self.tableView.setObjectName("tableView")
        self.gridLayout_4.addWidget(self.tableView, 1, 0, 1, 2)
        self.tabWidget.addTab(self.tabAllSamples, "")
        self.verticalLayout_3.addWidget(self.tabWidget)
        
        self.graph_tab = GraphTab()
        self.tabWidget.addTab(self.graph_tab, "Graphs")
        # self.verticalLayout_3.addWidget(self.tabWidget)
        
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        
        ################################################################################
        self.pushButtonReceiver.setCheckable(True)
        self.pushButtonReceiver.setChecked(True)
        self.pushButtonReceiver.setIcon(QtGui.QIcon('turtle512.png'))
        self.pushButtonReceiver.clicked.connect(self.start_stop_receiver)
        
        # self.pushButtonLiveOffline.setCheckable(True)
        self.pushButtonLiveOffline.setChecked(False)
        self.pushButtonLiveOffline.clicked.connect(self.reset_blocked)
        # self.pushButtonLiveOffline.setEnabled(True)
        self.pushButtonReplaySetIpPort.clicked.connect(lambda:send_selected(self,datastore,self.lineEditReplayIp,self.lineEditReplayPort))
        
        self.validateBtn.clicked.connect(validate_file)
        
        self.pushButtonDockableReceiver.clicked.connect(self.open_receiver)
        
        self.load_message()
 
        self.unBlockButton.clicked.connect(self.unblock_msg)
        self.comboBoxMessages.activated[str].connect(self.comboBoxMessageChanged)
        self.comboBoxMessagesMultiSample.activated[str].connect(self.comboBoxMessageMultiSampleChanged)
        
        
        self.blockedComboBoxMessages.activated[str].connect(self.comboBoxMessageChanged)
        # self.blockedComboBoxMessages.activated[str].connect(self.comboBoxMessageMultiSampleChanged)
        
        

        self.container = QtWidgets.QWidget()
        self.containerLayout = QtWidgets.QGridLayout()
        # self.containerLayout.setColumnStretch(0, 1)
        # self.containerLayout.setColumnStretch(1, 7)
        # self.containerLayout.setColumnStretch(2, 7)
        self.containerLayout.setColumnStretch(0, 7)
        self.containerLayout.setColumnStretch(1, 1)
        self.containerLayout.setColumnStretch(2, 1)
        self.containerLayout.setColumnStretch(3, 7)
        
        # self.containerLayout.setColumnStretch(3, 10)
        self.container.setLayout(self.containerLayout)
        self.scrollArea.setWidget(self.container)
        
        self.listCheckBox = []
        self.liststructlabels = []
        self.listLabels = []
        self.listLineEdits = []
        self.header_labels = []
        self.header_lineEdit = []
        self.selected_byte_msg_formats = []
        self.modified_selected_byte_msg_formats = []
        self.selected_msg_bit_lengths = []
        self.data_index = []
        self.hex_index = []
        self.byte_data = []
        self.blocked_msgs = []
        self.columns = 8
        self.rows = int(len(self.listCheckBox) / self.columns)
        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.update_gui_now)
        self.timer1.start(1000)
        self.load_blocked_msgs()

        self.comboBoxMessages.setEditable(True)
        self.blockedComboBoxMessages.setEditable(True)
        
        self.blockedComboBoxMessages.setInsertPolicy(QtWidgets.QComboBox.NoInsert)#prevents insertion of search text
        self.blockedComboBoxMessages.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        
        self.comboBoxMessages.setInsertPolicy(QtWidgets.QComboBox.NoInsert)#prevents insertion of search text
        self.comboBoxMessages.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        
        
        self.comboBoxMessagesMultiSample.setEditable(True)
        self.comboBoxMessagesMultiSample.setInsertPolicy(QtWidgets.QComboBox.NoInsert)#prevents insertion of search text
        self.comboBoxMessagesMultiSample.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        
        self.play_speed = 1
        # self.pushButtonSpeed.clicked.connect(self.play_speed_clicked)
        # self.pushButtonPauseResume.clicked.connect(self.pause_resume_clicked)
        # self.pushButtonPlayStop.clicked.connect(self.play_stop_clicked)
        # self.pushButtonLoad.clicked.connect(lambda:searchButtonHandle(self,datastore))
        # self.searchFeild.textChanged.connect(searchTab)
        self.pushButtonLoad.clicked.connect(self.block_selected_clicked)
        # self.pushButtonSendSelected.clicked.connect(self.block_selected_clicked)
        # self.pushButtonPlayStop.setCheckable(True)
        # self.pushButtonPauseResume.setCheckable(True)
        # self.pushButtonPlayStop.setChecked(True)
        # self.pushButtonPauseResume.setChecked(False)
        # self.pushButtonPauseResume.setEnabled(False)
        self.labelTimeGap.setDisabled(True)
        # self.lineEditTimeGap.setDisabled(True)

  
        self.tableView.setModel(datastore.model)
        self.tableView.setColumnWidth(0, 180)
        self.tableView.setColumnWidth(1, 170)
        self.tableView.setColumnWidth(2, 70)
        self.tableView.setColumnWidth(3, 70)
        self.tableView.setColumnWidth(4, 300)
        self.tableView.setColumnWidth(5, 780)
        self.tableView.setColumnWidth(6, 0)
        self.tableView.setColumnWidth(7, 0)
        self.tableView.setColumnWidth(8, 0)
        self.tableView.setColumnWidth(9, 0)
        self.table_max_entries = config.live_max_samples_all
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.show_custom_menu)
        
        self.table_msg_max_entries = config.live_max_samples_selected
        self.tableViewMultipleSamples.setModel(datastore.model_multi_samples)
        for i in range(self.table_msg_max_entries):
            self.tableViewMultipleSamples.setColumnWidth(i, 150)
        self.pushButtonOpenSelected.clicked.connect(self.open_selected_messages)
        # self.dateTimeEditStart.setCalendarPopup(True)
        # self.dateTimeEditEnd.setCalendarPopup(True)
        self.tableViewMultipleSamples.setSelectionMode(QtWidgets.QTableView.NoSelection)
        self.lineEditReplayIp.setText(config.sock_send_ip)
        self.lineEditReplayPort.setText(config.sock_send_port)
        
        
        # rigzin header display
        self.containerLayoutHeader = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_2)
        # labels_list = config.header_labels
        # rowCount = 0
        # for i,x in enumerate(labels_list):
        #     label = QtWidgets.QLabel()
        #     label.setText(x)
        #     lineEdit = QtWidgets.QLineEdit()
        #     lineEdit.setFixedWidth(50)
        #     containerLayoutHeader.addWidget(label, rowCount, 0, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        #     containerLayoutHeader.addWidget(lineEdit, rowCount, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        #     rowCount = rowCount + 1
        self.reload_gui(self.comboBoxMessages.currentText())

        self.replay_thread = None
        self.sender = UdpSender()
        self.pushButtonFilter.setEnabled(True)
        self.pushButtonFilter.clicked.connect(self.clearGui)
        self.pushButtonExit.clicked.connect(self.show_blocked_msgs)
        self.pushButtonDockableReceiver.setEnabled(False)
        # self.checkBoxTimestampUpdated.stateChanged.connect(self.set_timestamp_update_status_in_reply)
        ################################################################################
        
       
        self.retranslateUi(MainWindow)
        self.analytics =  MessageAnalytics(datastore.model)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonReceiver.setText(_translate("MainWindow", "Receiver Stop"))
        self.pushButtonDockableReceiver.setText(_translate("MainWindow", "Open a Receiver"))
        self.labelReplayIp.setText(_translate("MainWindow", "Send Ip"))
        self.labelReplayPort.setText(_translate("MainWindow", "Send Port"))
        self.pushButtonReplaySetIpPort.setText(_translate("MainWindow", "Send Selected Packet"))
        self.pushButtonExit.setText(_translate("MainWindow", "Blocked Messages"))
        self.labelSingleSample.setText(_translate("MainWindow", "Select-->"))
        
        self.validateBtn.setText(_translate("MainWindow", "Validate Msg File"))
        
        #Deleted header data diaplay on top dec 30 2024
        #self.labelHeaderSingleSample.setText(_translate("MainWindow", "Header -->"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabSingleSample), _translate("MainWindow", "Single Sample of Selected"))
        self.labelMultiSample.setText(_translate("MainWindow", "Select->"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabMultiSample), _translate("MainWindow", "Multiple Samples of Selected"))
        self.pushButtonOpenSelected.setText(_translate("MainWindow", "Open Selected"))
        self.pushButtonFilter.setText(_translate("MainWindow", "Clear UI"))
        self.pushButtonLiveOffline.setText(_translate("MainWindow", "Reset Blocked"))
        # self.labelStart.setText(_translate("MainWindow", "Start"))
        # self.labelEnd.setText(_translate("MainWindow", " End"))
        self.pushButtonLoad.setText(_translate("MainWindow", "Block Selected "))
        # self.checkBoxTimestampUpdated.setText(_translate("MainWindow", "Send Timestamp Updated"))
        # self.pushButtonSendSelected.setText(_translate("MainWindow", "Block Selected"))
        self.labelTimeGap.setText(_translate("MainWindow", "Time ms"))
        # self.lineEditTimeGap.setText(_translate("MainWindow", "1000"))
        # self.pushButtonSpeed.setText(_translate("MainWindow", "Speed 1 X"))
        self.unBlockButton.setText(_translate("MainWindow", "Unblock Message"))
        # self.pushButtonPauseResume.setText(_translate("MainWindow", "Pause"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabAllSamples), _translate("MainWindow", "All Samples"))
        ################################################################################
        MainWindow.setWindowTitle(_translate("MainWindow", "Receiver on Port:"+config.sock_rcv_port))
        ################################################################################
    
    def clearGui(self):
        for idx in range(0,datastore.model.rowCount()):
            datastore.model.removeRow(0)
    
    def show_blocked_msgs(self):
        try:
            print("Show")
            dialog = QtWidgets.QDialog(self.tableView)
            dialog.setWindowTitle("Blocked Messages")
            dialog.resize(650, 900)
            layout = QtWidgets.QVBoxLayout()
            dialog.setLayout(layout)
            table = QtWidgets.QTableView()
            layout.addWidget(table)
            
            new_model = QtGui.QStandardItemModel()
            new_model.setHorizontalHeaderLabels(['Blocked Messages'])
            
            print("Blocked MSGs",self.blocked_msgs)
            
            for val in self.blocked_msgs:
                items = [QtGui.QStandardItem(f"{val}")]
                new_model.appendRow(items)
                
            table.setModel(new_model)
            table.setColumnWidth(0, 650)
            table.setColumnWidth(1, 950)
            dialog.show()
            
        except Exception as e:
            print("Show Block messagee Error",e)
            
    def open_selected_messages(self):
        try:
            selected_indexes = self.tableView.selectionModel().selectedIndexes()
            for index in selected_indexes:
                row = index.row()
                row_data = []
                for column in range(datastore.model.columnCount()):
                    item = datastore.model.item(row, column)
                    if item:
                        row_data.append(item.text())
                print('Selected row_data:', row_data) 

                dialog = QtWidgets.QDialog(self.tableView)
                dialog.setWindowTitle(f"{row_data[0]} {row_data[1]}")
                dialog.resize(650, 900)
                layout = QtWidgets.QVBoxLayout()
                dialog.setLayout(layout)
                
                row_val = 0
                for index in selected_indexes:
                    row_val = index.row()
                
                table = QtWidgets.QTableView()

                layout.addWidget(table)
                new_model = QtGui.QStandardItemModel()
                new_model.setHorizontalHeaderLabels(['Feild','Value'])
                
                if row_data[6] != 'UNKNOWN': #or row_data[4] == 'MSG LEN Failed':
                    data = row_data[6]
                    print("DATA",data)
                    if(row_data[6]!=''):
                        seleted_msg_label_list = row_data[8].split(',')
                        selected_data_list = data.split(' ')
                        rcvd_format = row_data[-1].split(' ')
                        print("seleted_msg_label_list",seleted_msg_label_list)
                        print("selected_data_list",selected_data_list,rcvd_format)
                        print("data len",len(selected_data_list),"seleted_msg_label_list",len(seleted_msg_label_list))
                        
                        rcvd_data = row_data[4]

                        complete_tuple = self.data_index[row_val]

                        content_list = []
                        
                        
                        value_list = byte_data_parsing(complete_tuple,rcvd_format)
                        try:
                            for i,value in enumerate(seleted_msg_label_list):
                                items = [QtGui.QStandardItem(f"{seleted_msg_label_list[i]}"), QtGui.QStandardItem(f"{value_list[i]}")]
                                new_model.appendRow(items)
                        except Exception as e:
                            data = row_data[6]
                            int_list = [byte for byte in data]
                            for i,value in enumerate(int_list):
                                items = [QtGui.QStandardItem(f"byte {i}"), QtGui.QStandardItem(f"{int_list[i]}")]
                                new_model.appendRow(items)    
                            print("MESSAGE SELECTED ERROR-------->",e)
                    else:
                        data = self.hex_index[row_val]
                        int_list = [byte for byte in data]
                        # print("-----> int list", int_list)
                        
                        # header_label_list = config.labels_list_dictionary[row_data[2]]
                        # print("MSG LABEL LIST ALL SAMPLES",header_label_list)
                        format_generated = row_data[9]
                        byte_data_rcvd = self.byte_data[row_val] 
                        format_size = struct.calcsize(f'={format_generated}')
                        format_generated_list = format_generated.split(' ')
                        
                        # print("format generated",row_data[7],"format_size",format_size,'byte_data_rcvd',byte_data_rcvd)
                        fmt_length = 0
                        complete_tuple = [] 
                        
                        for idx,val in enumerate(format_generated_list):
                            fmt = format_generated_list[:idx+1]
                            current_format = ' '.join(map(str,fmt[:]))
                            # print("fmt",current_format)
                            fmt_length = struct.calcsize(f'={current_format}')
                            try:
                                complete_tuple = struct.unpack(f'={current_format}',byte_data_rcvd[:fmt_length])
                            except Exception as e:
                                print("unpacking error",complete_tuple)
                            
                        print(complete_tuple)
                        value_list = byte_data_parsing(complete_tuple,format_generated_list)
                        label_list = row_data[8].split(',')
                        # print(content_list[10:],"*************************contentList********************", content_list)
                        try:    
                            for i in range(len(format_generated_list)):
                                items = [QtGui.QStandardItem(label_list[i]), QtGui.QStandardItem(f"{value_list[i]}")]
                                new_model.appendRow(items)
                            # for i in range(len(int_list)):
                            #     if i<10:
                            #         items = [QtGui.QStandardItem(header_label_list[i]), QtGui.QStandardItem(f"{header_list[i]}")]
                            #         new_model.appendRow(items)
                            #     else:
                            #         items = [QtGui.QStandardItem(f"byte {i}"), QtGui.QStandardItem(f"{int_list[i]}")]
                            #         new_model.appendRow(items)     
                        except Exception as e:
                            print('Error in For Loop',e)
                        
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Critical)
                    msg.setText('Unknown Messsage Recived')
                    msg.setInformativeText('Message Unknown Error')
                    msg.setWindowTitle('Error')
                    msg.exec_()
                    # labels_list = config.labels_list_dictionary[row_data[1]]
                    # labels_list_with_hdr = ['header'] + labels_list
                    # values_list_with_hdr = self.get_values_from_msg_hex_string(row_data[1], row_data[2])
                    
                    if row_data[1] == 'RATC_CBI_INDICATION_MSG':
                        items = [QtGui.QStandardItem("header"), QtGui.QStandardItem(f"{values_list_with_hdr[0]}")]
                        new_model.appendRow(items)
                        items = [QtGui.QStandardItem("no_of_records"), QtGui.QStandardItem(f"{values_list_with_hdr[1]}")]
                        new_model.appendRow(items)
                        bit_list = []
                        if(len(values_list_with_hdr) > 3):
                            bit_list = values_list_with_hdr[2:-1]
                            print('RATC_CBI_INDICATION_MSG bit_list-->>', bit_list)
                            for i,bit in enumerate(bit_list):
                                items = [QtGui.QStandardItem(f"bit_num_{bit}"), QtGui.QStandardItem(f"{config.ratc_cbi_indication_bit_names[bit]}")]
                                new_model.appendRow(items)
                                items = [QtGui.QStandardItem("crc"), QtGui.QStandardItem(f"{values_list_with_hdr[-1]}")]
                                new_model.appendRow(items)
                        
                    elif row_data[1] == 'CBI_RATC_INDICATION_MSG':
                        items = [QtGui.QStandardItem("header"), QtGui.QStandardItem(f"{values_list_with_hdr[0]}")]
                        new_model.appendRow(items)
                        items = [QtGui.QStandardItem("no_of_records"), QtGui.QStandardItem(f"{values_list_with_hdr[1]}")]
                        new_model.appendRow(items)
                        bit_list = []
                        
                        if(len(values_list_with_hdr) > 3):
                            bit_list = values_list_with_hdr[2:-1]
                            print('CBI_RATC_INDICATION_MSG bit_list-->>', bit_list)
                            for i,bit in enumerate(bit_list):
                                items = [QtGui.QStandardItem(f"bit_num_{bit}"), QtGui.QStandardItem(f"{config.cbi_ratc_indication_bit_names[bit]}")]
                                new_model.appendRow(items)
                        items = [QtGui.QStandardItem("crc"), QtGui.QStandardItem(f"{values_list_with_hdr[-1]}")]
                        new_model.appendRow(items) 
                    else:
                        print("UNKNOWN MSGGG")
                        # for i,label in enumerate(labels_list_with_hdr):
                        #     print(label, ':', values_list_with_hdr[i])
                        #     items = [QtGui.QStandardItem(f"{label}"), QtGui.QStandardItem(f"{values_list_with_hdr[i]}")]
                        #     new_model.appendRow(items)
                            
                table.setModel(new_model)
                table.setColumnWidth(0, 150)
                table.setColumnWidth(1, 350)
                # dialog.exec_()
                dialog.show()
        except Exception as e:
            print("Open Selected error occured",e)
        
    def show_custom_menu(self, pos: QtCore.QPoint):
        index = self.tableView.indexAt(pos)
        if index.isValid():
            menu = QtWidgets.QMenu(self.tableView)
            open_action = QtWidgets.QAction('Open Sample Inspector',self.tableView)
            open_action.triggered.connect(lambda: self.open_new_table_view(index.row()))
            menu.addAction(open_action)
            menu.exec_(self.tableView.viewport().mapToGlobal(pos))
    
    def open_new_table_view(self, row: int):
        self.open_selected_messages()
        
    def add_entry(self, time, msg, hex_string,content, labels, observation_str,content_format,hex_data,data):
        len_data = len(data)
        obs = QtGui.QStandardItem(f"{observation_str}----[Byte Data length recvd ->{len_data}]")
        # obs = QtGui.QStandardItem(f"{observation_str}")
        
        header_data = config.dynamic_header_format[0].split(' ')
        
        
        module_name = {
            '0':''
        }

        try:
            src_text = module_name[header_data[1]]
        except Exception as e:
            src_text = 'NA'
        try:
            dst_text = module_name[header_data[2]]
        except Exception as e:
            dst_text = 'NA'
  
        
        if config.mode == 'live':
            if datastore.model.rowCount() >= self.table_max_entries:
                datastore.model.removeRow(self.table_max_entries - 1)
                
            if observation_str != 'RCVD OK':
                obs.setBackground(QtGui.QColor(200,0,0))
            else:
                obs.setBackground(QtGui.QColor(0,200,0))
            items = [QtGui.QStandardItem(f"{time}"),QtGui.QStandardItem(f"{config.dynamic_header_format}"),QtGui.QStandardItem(f"{header_data[1]} ({src_text})"),QtGui.QStandardItem(f"{header_data[2]} ({dst_text})"),QtGui.QStandardItem(f"{msg}"),obs, QtGui.QStandardItem(f"{content}"),QtGui.QStandardItem(f"{hex_string}"),QtGui.QStandardItem(f"{labels}"),QtGui.QStandardItem(f"{content_format}")]
            
        if msg in self.blocked_msgs:
            print("message needs to be blocked")
        else:
            datastore.model.insertRow(0, items)
            self.data_index.insert(0,hex_string)
            self.hex_index.insert(0,hex_data)
            self.byte_data.insert(0,data)
            config.graph_plot_data(msg,time)
            
            # print("...........",self.data_index)
            
            # if observation_str == 'CRC Failed':
            #     item_to_color = self.model.item(0,2)
            #     item_to_color.setBackground(QtGui.QColor(255,0,0))
        
        if config.message_selected_multi_samples == msg and observation_str != 'MSG LEN Failed': 
            if datastore.model_multi_samples.rowCount() >= self.table_msg_max_entries:
                datastore.model_multi_samples.removeRow(self.table_msg_max_entries - 1)
            values_list_with_hdr = self.get_values_from_msg_hex_string(msg, content,labels)
            items = [QtGui.QStandardItem(f"{time}")]
            
            if msg == 'RATC_CBI_INDICATION_MSG' or msg == 'CBI_RATC_INDICATION_MSG':
                header = values_list_with_hdr[0]
                no_of_records = values_list_with_hdr[1]
                bit_list_string = ''
                crc = values_list_with_hdr[-1]
                if(len(values_list_with_hdr) > 3):
                    bit_list = values_list_with_hdr[2:-1]
                    bit_list_string = ' '.join(map(str,getStringifiedMsgList(bit_list)))
                indication_items = [QtGui.QStandardItem(f"{header}"), QtGui.QStandardItem(f"{no_of_records}"), QtGui.QStandardItem(f"{bit_list_string}"), QtGui.QStandardItem(f"{crc}"), QtGui.QStandardItem(f"{observation_str}")]
                items += indication_items
            else:
                for i,value in enumerate(values_list_with_hdr):
                    item = QtGui.QStandardItem(f"{value}")
                    items.append(item) 
                item = QtGui.QStandardItem(f"{observation_str}")
                items.append(item)    
            datastore.model_multi_samples.insertRow(0, items)
    
    def load_message(self):

        
        
        self.comboBoxMessagesMultiSample.addItem("None")
        for x in config.msg_names:
            self.comboBoxMessages.addItem(x)
            self.blockedComboBoxMessages.addItem(x)
            self.comboBoxMessagesMultiSample.addItem(x)
   
    def update_gui_now(self):
        if config.name_to_header_type[config.message_selected] == 'external':
            self.update_message_status()
            self.update_header(config.header_str)
            self.update_content(config.content_str)
            self.update_bytes_content(config.content_str)
        else:
            if not config.header_str == '':
                self.update_message_status()
                self.update_content(config.content_str)
                # self.update_header(config.header_str)
                bits_format = config.bits_dictionary[config.message_selected]
                if bits_format == 'ratc_cbi_indication_bits' or bits_format == 'cbi_ratc_indication_bits':
                    self.update_gui(config.set_bit_list, config.set_bit_list_msg_id)
                else:
                    self.update_bytes_content(config.fields_list) 
        
    def start_stop_receiver(self):
        if self.pushButtonReceiver.isChecked():
            self.pushButtonReceiver.setText("Receiver Stop")
            config.keepRunning = True
        else:
            self.pushButtonReceiver.setText("Receiver Start") 
            config.keepRunning = False  
        # print('config.keepRunning=',config.keepRunning)   
        
    def replay_live_clicked(self):
        print("Here")

    def open_receiver(self):
        
        dialog = UserInputDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            recv_port, send_port, send_ip = dialog.get_data()
            print('form data:',recv_port, send_port, send_ip)
            command = 'python main.py '+ recv_port + ' ' + send_port + ' ' + send_ip
            subprocess.run(['gnome-terminal', '--', 'bash', '-c', f'{command}; exec bash'])
        else:
            print('Cancelled')
            
    def reload_gui(self,message_selected):
        for k,chkBox in enumerate(self.listCheckBox):
            chkBox.setParent(None)
            chkBox.deleteLater()
            chkBox= None
        self.listCheckBox.clear()
        
        for label in self.liststructlabels:
            label.setParent(None)
            label.deleteLater()
            label= None
        self.liststructlabels.clear()
        
        
        for label in self.listLabels:
            label.setParent(None)
            label.deleteLater()
            label= None
        self.listLabels.clear()
        
        for lineEdit in self.listLineEdits:
            lineEdit.setParent(None)
            lineEdit.deleteLater()
            lineEdit=None
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


        self.selected_byte_msg_formats.clear()
        self.modified_selected_byte_msg_formats.clear()
        self.selected_msg_bit_lengths.clear()
    
        if config.bits_dictionary[config.message_selected] == 'ratc_cbi_indication_bits':
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
        elif config.bits_dictionary[config.message_selected] == 'cbi_ratc_indication_bits':
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
            labels_list = config.labels_list_dictionary[config.message_selected]
            labels_struct_list = config.labels_struct_list_dictionary[config.message_selected]
            print("#################################", config.message_selected, "   -> ",labels_list)
            self.rows = len(labels_list)
            self.listLabels  = labels_list.copy()
            self.listLineEdits = labels_list.copy()
            self.liststructlabels = labels_struct_list.copy()
            rowCount = 0
            
            for i,x in enumerate(labels_list):   
                self.liststructlabels[i] = QtWidgets.QLabel()
                self.liststructlabels[i].setText(labels_struct_list[i])
                
                self.listLabels[i] = QtWidgets.QLabel()
                self.listLabels[i].setText(x)
                
                #hover
                self.listLabels[i].setToolTip(dict[config.message_selected][i][7].replace("_x000D_",""))
                self.listLabels[i].setToolTipDuration(50000)
                self.listLabels[i].setStyleSheet("""
                    QLable {
                        padding-left: 10px;
                        padding-right:10px;
                        }
                    QToolTip{
                        color:#ffffff;
                        background-color:#2a82da;
                        border: 1px solid black;
                        padding:10px;
                        }
                    QLabel:hover{
                        background-color:lightblue;
                        border: 1px solid black;
                        }
                                                 """)
                self.listLineEdits[i] = QtWidgets.QLineEdit()
                self.listLineEdits[i].setFixedWidth(100)
                # self.containerLayout.addWidget(self.liststructlabels[i], rowCount, 0, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
                # self.containerLayout.addWidget(self.listLabels[i], rowCount, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
                # self.containerLayout.addWidget(self.listLineEdits[i], rowCount, 2, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
                rowCount = rowCount + 1
                
    def reload_gui_multi_samples(self,message_selected):
        datastore.model_multi_samples.removeRows(0, datastore.model_multi_samples.rowCount())
        datastore.model_multi_samples.removeColumns(0, datastore.model_multi_samples.columnCount())
        if message_selected != 'None':                    
            print('1 message_selected', message_selected)  
            labels_list = config.labels_list_dictionary[message_selected]
            labels_list_with_hdr = ['Date Time','Header'] + labels_list + ['Observation']
            datastore.model_multi_samples.updateHeader(labels_list_with_hdr)
            for i in range(len(labels_list_with_hdr)):
                self.tableViewMultipleSamples.setColumnWidth(i, 150)
            self.tableViewMultipleSamples.setColumnWidth(0, 170)
            self.tableViewMultipleSamples.setColumnWidth(1, 320)

    def update_gui(self, set_bit_list, msg_id):
        if config.message_selected in set_bit_list:
                
            for i,x in enumerate(self.listCheckBox):
                self.listCheckBox[i].setChecked(False)
                    
            for i,x in enumerate(set_bit_list[config.message_selected]):
                self.listCheckBox[x].setChecked(True)  

    def update_message_status(self):
        if config.selected_message_status_on_receiver == 1:
            self.labelHeaderSingleSample.setStyleSheet("color:green;")
            notification_message = "Data receiving"
            self.labelHeaderSingleSample.setText(notification_message)
        else:
            self.labelHeaderSingleSample.setStyleSheet("color:red;")    
            notification_message = "Data not receving"
            self.labelHeaderSingleSample.setText(notification_message)
            
    def update_content(self,content):
        # print("CONTENT displayed",content)
        #Rigzin 24/12/2024 Adding new datatype to store the header_str and content_str as dictionary where key is message_name
        
        # print("Update Content called",content)
        
        
        if config.message_selected in content:
            # print("CONTENTTT",content[config.message_selected])
            # self.lineEditContent.setText(content[config.message_selected])
            self.lineEditContent.setText("Reciving Data for: " + config.message_selected)
                
    def update_header(self,header):
        #Rigzin 24/12/2024 Adding new datatype to store the header_str and content_str as dictionary where key is message_name
        if config.message_selected in header:
            # self.lineEditHeader.setText(header[config.message_selected])
            header_data_list = header[config.message_selected].split(" ")
            # side header display begin
            i=0
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>header_data_list: ", header_data_list)
            for child in self.scrollAreaWidgetContents_2.findChildren(QtWidgets.QWidget):
                if isinstance(child, QtWidgets.QLineEdit):
                    child.setText(header_data_list[i])
                    i = i+1
                else:
                    pass
            # Rigzin end
        else:
            pass
    
    def update_bytes_content(self, content):
        try:
            content = config.content_str
            # print("content called",content)
            # if len(content) > 0:
            #     print("CONTENT",next(iter(content)),"MSG selected",config.message_selected)
            
                
            while self.containerLayout.count():
                item = self.containerLayout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                    
            if(len(content) > 0 and next(iter(content)) == config.message_selected):
                
                if ( next(iter(content)) == config.message_selected):
                    res = content[config.message_selected].split(' ')
                    # print("res",res)
                    
                rowCount = 0
                label = res.copy()
                info_label = config.dynamic_label_lsit.copy()
                # print("INfo", len(info_label),len(label))
                ui_label = info_label.copy()
                
                
                for i,x in enumerate(res):
                    label[i] = QtWidgets.QLineEdit()
                    label[i].setText(x)
                    ui_label[i] = QtWidgets.QLabel()
                    ui_label[i].setText(str(info_label[i]))
                    
                    # info_label[i].setText("Data")
                    self.containerLayout.addWidget(ui_label[i], rowCount, 0, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
                    self.containerLayout.addWidget(label[i], rowCount, 1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
                    # self.containerLayout.addWidget(self.listLineEdits[i], rowCount, 2, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
                    rowCount = rowCount + 1
        except Exception as e:
            print("Error in data receving",e)
            
    def removeWidgets(self):  
        print("Removing widgets")  
        while self.containerLayout.count():
            item = self.containerLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def comboBoxMessageChanged(self, text):
        config.message_selected = text

        # print('msgSelected ',config.message_selected)
        self.reload_gui(text) 
        self.removeWidgets()
        # self.update_bytes_content([])
        
    def comboBoxMessageMultiSampleChanged(self, text):
        config.message_selected_multi_samples = text
        # print('msgSelected ',config.message_selected)
        self.reload_gui_multi_samples(text)  
       
    def play_speed_clicked(self):
        print('Speed Clicked')
        if self.play_speed == 1:
            self.play_speed = 2
            self.pushButtonSpeed.setText('Speed 2 X')
        elif self.play_speed == 2:
            self.pushButtonSpeed.setText('Speed 4 X')
            self.play_speed = 4
        elif self.play_speed == 4:
            self.pushButtonSpeed.setText('Speed 8 X')
            self.play_speed = 8
        elif self.play_speed == 8:
            self.pushButtonSpeed.setText('Manual')
            self.labelTimeGap.setEnabled(True)
            self.lineEditTimeGap.setEnabled(True)
            self.play_speed = -1  
        elif self.play_speed == -1:
            self.pushButtonSpeed.setText('Speed 1 X')
            self.labelTimeGap.setDisabled(True)
            self.lineEditTimeGap.setDisabled(True)
            self.play_speed = 1             

        # self.mode = 'live'#live / replay
        # self.play_stop_state = 'stop'
        # self.pause_resume_state = 'pause'
        # self.play_speed = 1

    def pause_resume_clicked(self):
        print('pause_resume_clicked')
        if self.pushButtonPauseResume.isChecked():
            self.pushButtonPauseResume.setText("Resume")
            self.pause_in_replay_mode()
            print('Paused')
        else:
            self.pushButtonPauseResume.setText("Pause")
            self.resume_in_replay_mode()
            print('Resumed') 
         
    def play_stop_clicked(self):
        print('play_stop_clicked')   
        if self.pushButtonPlayStop.isChecked():
            self.pushButtonPlayStop.setText("Stop")
            self.pushButtonPauseResume.setEnabled(True)
            self.start_sending_in_replay_mode()
            self.pushButtonLiveOffline.setEnabled(False)
            print('Started')
        else: 
            self.pushButtonPlayStop.setText("Play")
            self.pushButtonPauseResume.setEnabled(False)
            self.pushButtonPauseResume.setChecked(False)
            self.pushButtonPauseResume.setText("Pause")
            self.stop_sending_in_replay_mode()
            self.pushButtonLiveOffline.setEnabled(False)
            print('Stopped') 
            
    def start_sending_in_replay_mode(self):
        if not self.replay_thread or not self.replay_thread.isRunning():
            self.replay_thread = ReplayThread()
            self.replay_thread.signal_data_sent.connect(self.handle_data_sent)
            self.replay_thread.start()
            
    def stop_sending_in_replay_mode(self):
        if self.replay_thread and self.replay_thread.isRunning():
            self.replay_thread.stop()
            self.replay_thread.wait()
            
    def pause_in_replay_mode(self):
        if self.replay_thread and self.replay_thread.isRunning():
            self.replay_thread.pause_reply()
            
    def resume_in_replay_mode(self):
        if self.replay_thread and self.replay_thread.isRunning():
            self.replay_thread.resume_reply()
          
    def closeEvent(self, event):
        if not self.replay_thread and self.replay_thread.isRunning():
            self.replay_thread.stop()
            self.replay_thread.wait()  
       
    def handle_data_sent(self, message):
        if (message == 'Replay Stopped'):
            print('Message From Replay Thread: ', message)  
            self.pushButtonPlayStop.setText("Play")
            self.pushButtonPlayStop.setChecked(False)
            self.pushButtonPauseResume.setEnabled(False)
            self.pushButtonPauseResume.setChecked(False)
            self.pushButtonPauseResume.setText("Pause")
            # self.stop_sending_in_replay_mode()
            # print('Stopped') 

    def load_clicked(self):
        # readLog.example()
        # msglist = readLog.get_replay_packets(startTime, endTime)
        # print(msglist)
        qt_date_time_start = self.dateTimeEditStart.dateTime()
        py_date_time_start = qt_date_time_start.toPyDateTime()
        py_date_time_start = py_date_time_start.replace(second=0, microsecond=0)
        print('Start date time qt:', qt_date_time_start)
        print('Start date time py:', py_date_time_start)
        
        qt_date_time_end = self.dateTimeEditEnd.dateTime()
        py_date_time_end = qt_date_time_end.toPyDateTime()
        py_date_time_end = py_date_time_end.replace(second=0, microsecond=0)
        print('End date time qt:', qt_date_time_end)
        print('End date time py:', py_date_time_end)
        
        msg_list = readLog.get_replay_packets(py_date_time_start, py_date_time_end)
        
        ms_delta_time_list = []
        previous_msg_time = 0
        dateTimeFormat = "%Y-%m-%d %H:%M:%S,%f"
        # 2024-07-13 13:58:00,257 72 04 01 72 04 23 21 00 01 00 0d 07 e8 07 0d 3a 00 ff 00 01 00 00 00 06 00 d3 ab 6b 16\n
        for msg in msg_list:
            timestamp = msg[:23]
            msg_time = datetime.strptime(timestamp, dateTimeFormat)
            if previous_msg_time == 0:
                ms_delta_time = 0
            else:
                delta_time = msg_time - previous_msg_time
                ms_delta_time = delta_time.total_seconds() * 1000
                # ms_delta_time = (delta_time.hour * 3600 + delta_time.min*60 + delta_time.secon) * 1000 + delta_time.microsecond // 1000
            ms_delta_time_list.append(ms_delta_time)
            previous_msg_time = msg_time
            print('timestamp->',timestamp, ms_delta_time)
            hex_string = msg[24:-1]
            data = bytearray.fromhex(hex_string) 
            src_id = data[config.src_id_index]
            msg_id = data[config.message_id_index]
            # rcv_msg_len = data[config.message_len_index]
            # header_format_rcv = config.header_formats[0]
            # header_length_rcv = struct.calcsize(f'={header_format_rcv}') #getting the header length
            # header_tuple_rcv = struct.unpack(f'={header_format_rcv}',data[0:header_length_rcv]) #unpacking only header 
            # hdrList = self.getMsgListFromMsgTuple(header_tuple_rcv)
            # print(' ')
            # print("RCV SRC_ID:",src_id, ",RCV MSG ID:",msg_id, ",RCV MSG LEN:",rcv_msg_len)
            msg_name = config.get_message_name(msg_id, src_id)
            print('MSG->',msg_name, hex_string)
            observation_str = ''
            items = [QtGui.QStandardItem(f"{timestamp}"), QtGui.QStandardItem(f"{msg_name}"), QtGui.QStandardItem(f"{hex_string}"), QtGui.QStandardItem(f"{observation_str}")]
            datastore.model.appendRow(items)
            datastore.model.set_delta_time_list(ms_delta_time_list)

    def unblock_msg(self):
        try:
            val = self.unBlockedComboBoxMessages.currentText()
            idx = self.unBlockedComboBoxMessages.currentIndex()
            print("------>",idx)
            for i,msg in enumerate(self.blocked_msgs):
                if msg == val:
                    print("Msg UNblocked",val)
                    self.blocked_msgs.pop(i)
                    self.unBlockedComboBoxMessages.removeItem(idx)
            # print("MSG Block list",self.blocked_msgs)        
            self.msgCountLineEdit.setText("Blocked message(s) count: " + str(len(self.blocked_msgs)))
        except Exception as e:
            print("unblock Error Occured")

    def load_blocked_msgs(self):
        try:
            print("Loading bloked Messages from txt")
    
            with open(file_path,'r',encoding="utf-8") as file:
                # print(file)
                for val in file:
                    self.blocked_msgs.append(val[:-1])
                    self.unBlockedComboBoxMessages.addItem(val[:-1])
            print(self.blocked_msgs)
            self.msgCountLineEdit.setText("Blocked message(s) count: " + str(len(self.blocked_msgs)))
        except Exception as e:
            print("load_blocked_msgs Error")
        
    def reset_blocked(self):
        try:
            self.blocked_msgs.clear()
            self.unBlockedComboBoxMessages.clear()
            self.msgCountLineEdit.setText("Blocked message(s) count: "+ str(len(self.blocked_msgs)))
            print("Block Message Clear")
            with open(file_path,'w',encoding="utf-8") as file:
                file.flush()
        except Exception as e:
            print("reset_blocked error")

    def block_selected_clicked(self):
        try:
            print("hoihwef",self.blockedComboBoxMessages.currentText())
            item = self.blockedComboBoxMessages.currentText()
            
            if item not in self.blocked_msgs:
                print("Adding")
                self.blocked_msgs.append(item)
                self.unBlockedComboBoxMessages.addItem(item)
                with open(file_path,'w',encoding="utf-8") as file:
                    for val in self.blocked_msgs:
                        file.write(val+'\n')
            else:
                print("Already ADded")
                    
            self.msgCountLineEdit.setText("Blocked message(s) count: "+str(len(self.blocked_msgs)))
        except Exception as e:
            print("block_selected_clicked error")
                
    def send_selected_clicked(self):
        selected_indexes = self.tableView.selectionModel().selectedIndexes()
        for index in selected_indexes:
            row = index.row()
            row_data = []
            for column in range(datastore.model.columnCount()):
                item = datastore.model.item(row, column)
                if item:
                    row_data.append(item.text())
            print('Selected row_data:', row_data)
            data = bytearray.fromhex(row_data[2])
            # if row_data[1] != 'UNKNOWN':
            #     data = bytearray.fromhex(row_data[2])
            data = self.get_time_crc_updated_packet(data)
            self.sender.send_packet(data)     

    def get_values_from_msg_hex_string(self, msg_name, content,lables):
        content_format= ''
        header_format= ''
        hdrList = []
        completeList = []
        content_sublist = []
        content_str = ''
        header_str = ''
        modified_value_list = []
        if(msg_name != ''):
            # content_format_list = config.modified_content_dictionary[msg_name] 
            content_format = ' '.join(map(str,content[:]))
            # header_format = config.header_dictionary[msg_name]
            # crc_format = config.crc_dictionary[msg_name]
            bits_list = config.bits_list_dictionary[msg_name]
            bits_format = config.bits_dictionary[msg_name]
            header_length = struct.calcsize(f'={content_format}') #getting the header length
            # num_elements_header = len(header_format.replace(' ',''))
            data = bytearray.fromhex(content)
            header_tuple = struct.unpack(f'={header_format}',data[0:header_length]) #unpacking only header 
            hdrList = self.getMsgListFromMsgTuple(header_tuple)
            header_str = ' '.join(map(str,hdrList))
            modified_value_list.append(header_str)
            if bits_format == 'bytes':
                # print('    modified content_format list:',content_format)
                complete_tuple = struct.unpack(f'={content_format}',data)
                temp_list = self.getMsgListFromMsgTuple(complete_tuple)
                print('content_list in ADD ENTRY  -> ',temp_list)
                completeList = self.getStringifiedMsgList( temp_list )
                # content_str = ' '.join(map(str,completeList[num_elements_header:]))
                # content_sublist = completeList[num_elements_header:]
                sizeForByte = 0
                shift = 0
                content_sublist_index = 0
                for y,b in enumerate(bits_list):
                    # print('b = ', b)
                    if b >= 8 :
                        modified_value_list.append(content_sublist[content_sublist_index])
                        content_sublist_index += 1
                    else:
                        sizeForByte = sizeForByte + b
                        byteValue = content_sublist[content_sublist_index]
                        # binaryByteValue = bin(byteValue)
                        # print('binaryByteValue: ', binaryByteValue)
                        start = 8 - sizeForByte
                        end = start + b - 1
                        shift = sizeForByte - b
                        extracted_content = self.extract_bits(byteValue, start, end, shift)
                        # print('b size:', b, ', Start:', start, ', End:', end,', extracted_bit_content', extracted_content)
                        modified_value_list.append(extracted_content)
                        if sizeForByte == 8:
                            # print('byte complete......')
                            sizeForByte = 0
                            content_sublist_index += 1
                # print('Modified_value_list -> ',modified_value_list)
                # if(msg_name == config.message_selected): 
                #     labels_list = config.labels_list_dictionary[msg_name]
                #     print(' ')
                #     print('VVV******************* START OF MESSAGE ********************VVV')
                #     print('For Message Name:',msg_name)
                #     for i,label in enumerate(labels_list):
                #         print('    ', label,' : ',modified_value_list[i]) 
                #     print('^^^******************** END OF MESSAGE **********************^^^')
            elif(bits_format == 'ratc_cbi_indication_bits' or bits_format == 'cbi_ratc_indication_bits'):
                print("indication_bits")
                header_length = struct.calcsize(f'={header_format}') #getting the header length
                content_length = struct.calcsize(f'={content_format}') #getting the content length    
                msg_len = header_length + content_length + 4  #4 is CRC length
                print('msg_len:',msg_len, ', header_format:',header_format, ', content_format:',content_format)

                complete_tuple = struct.unpack(f'={header_format}{content_format}{crc_format}',data)
                temp_list = self.getMsgListFromMsgTuple(complete_tuple)
                print('temp_list -> ',temp_list)
                completeList = self.getStringifiedMsgList( temp_list )
                # content_str = ' '.join(map(str,completeList[num_elements_header:]))
                content_sublist = completeList[num_elements_header:]
                
                modified_value_list.append(completeList[num_elements_header])#num records
                
                records = completeList[num_elements_header + 1 : len(completeList)-1]
                print('records -> ',records)
                bitPositionList = []
                for i,x in enumerate(records):
                    if records[i] != 0:
                        # print(records[i])
                        for j in range(7, -1, -1):
                            bit = (records[i]>> j) & 1
                            if bit == 1:
                                bitPositionList.append(i*8+j)
                print('bitPositionList:',bitPositionList)  
                modified_value_list += bitPositionList
                # modified_value_list.append(completeList[len(completeList)-1])
                modified_value_list.append(completeList[-1])
        return modified_value_list                 
        
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
        
    def set_timestamp_update_status_in_reply(self):
        print('set_timestamp_update_status_in_reply:', self.checkBoxTimestampUpdated.isChecked)
        if self.checkBoxTimestampUpdated.isChecked():
            self.replay_thread.set_timestamp_update_status(True)
        else:
            self.replay_thread.set_timestamp_update_status(False)
            
    def searchMessage(self,text):
        print("Searching.qwewq..",text)
        
        
        for i in range(self.containerLayout.count()):
            widget = self.containerLayout.itemAt(i).widget()
            if widget is not None and text.lower() !="":
                if text.lower() in widget.text().lower():
                    widget.setStyleSheet("background-color: pink;")
                    self.scrollArea.ensureWidgetVisible(widget,xMargin=10,yMargin=10)
                else:
                    widget.setStyleSheet("")
