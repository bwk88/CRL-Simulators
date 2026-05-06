from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QDialog, QToolButton, QMenu, QAction
from PyQt5.QtCore import pyqtSignal, QSize, Qt, pyqtBoundSignal, QThread
from SNS.widgetsCustom import savingDialog, errorDisplay, addItemsWidget, preconditionsWidget, itemsLWFunctions,itemsLWTestCase, LW_items_MessageDetails, LW_items_Output_Message_widget, twoInputDialog, backButton, snsInfoBar, confirmDialog
import pandas as pd
import os, random, json
from debuggerFile import DBUG
from SNS.models import snsMessageDetails, SNS_FileOperations_delete_data, snsOutputMessageDetails, mainWindow_SNS_save_edit_data, copyData, SNS_FileOperations_copy_data
from SNS.utility import listStringToList, toSuperScript
from SNS.customColours import GREY_300, GREY_400, GREY_100
from SNS.fileOperations import fileOperations
from SNS.utility import SafeListWidget, ui_ops
import gc, csv, time
from SNS.dynamic_sender import Dynamic_Sender
from SNS.saveSendOutput import SaveSendOutput
from SNS.saveSendPeriodic import saveSendPeriodic
from Configuration import config
from collections import deque

SNS_FOLDER = "SNS/SAVEANDSEND"
COUNTER_INPUT = 1
COUNTER_OUTPUT = 1

pd.set_option("display.max_columns", None)


class saveAndSend(QtWidgets.QWidget):

    switch_add_periodic_tab = pyqtSignal(int, str, str, bool)    
    switch_tab_signal = pyqtSignal(int, str, str, bool)
    switched_tab_response_function_signal = pyqtSignal()
    switched_tab_response_testcase_signal = pyqtSignal()
    edit_message_sns_signal = pyqtSignal(object, str)
    start_sending_Functions_signal = pyqtSignal(str, object)
    start_sending_testCase_signal = pyqtSignal(str, object, str)
    ip_port_changed_signal = pyqtSignal()
    default_delay_set_signal = pyqtSignal(int)
    default_periodic_set_signal = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.gridLayout_mainWidgetSNSTab = QtWidgets.QGridLayout()
        self.gridLayout_mainWidgetSNSTab.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_mainWidgetSNSTab.setObjectName("gridLayout_mainWidgetSNSTab")
        self.stackedWidgetSNS = QtWidgets.QStackedWidget()
        self.stackedWidgetSNS.setObjectName("stackedWidgetSNS")  
        
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        # Project Page containing project and its Functions details
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        self.projectPageSNS = QtWidgets.QWidget()
        self.projectPageSNS.setObjectName("projectPageSNS")
        self.gridLayout_projectPageSNS = QtWidgets.QGridLayout(self.projectPageSNS)
        self.gridLayout_projectPageSNS.setObjectName("gridLayout_projectPageSNS")
        # self.gridLayout_projectPageSNS.setContentsMargins(0, 0, 0, 0)
        
        self.snsNavTabProject = QtWidgets.QWidget(self.projectPageSNS)
        self.snsNavTabProject.setMaximumSize(QtCore.QSize(16777215, 100))
        # self.snsNavTabProject.setStyleSheet("background-color: #eeeeee;")
        self.snsNavTabProject.setObjectName("snsNavTabProject")
        self.gridLayout_snsNavTabProject = QtWidgets.QGridLayout(self.snsNavTabProject)
        self.gridLayout_snsNavTabProject.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_snsNavTabProject.setObjectName("gridLayout_snsNavTabProject")  
        
        # self.projectPage_back = QtWidgets.QPushButton(self.snsNavTabProject)
        # self.projectPage_back.setMinimumSize(QtCore.QSize(70, 16777215))
        # self.projectPage_back.setObjectName("projectPage_project_back")
        # self.projectPage_back.setStyleSheet("""
        #                                             border: 1px solid #eeeeee;
        #                                             font-size: 10px;
        #                                             font-weight: bold;
        #                                             padding: 5px 0px;
        #                                             """)
        # self.projectPage_back.setText("Back")
        # self.gridLayout_snsNavTabProject.addWidget(self.projectPage_back, 0, 0, 1, 1, Qt.AlignLeft)
        
        
        self.projectPage_back = backButton(True)
        self.gridLayout_snsNavTabProject.addWidget(self.projectPage_back, 0, 0, 1, 1, Qt.AlignLeft)
        
        
        self.projectPage_project_link = QtWidgets.QPushButton(self.snsNavTabProject)
        self.projectPage_project_link.setMinimumSize(QtCore.QSize(150, 16777215))
        # self.titleProjectButtonLabel.setMaximumSize(QtCore.QSize(150, 16777215))
        self.projectPage_project_link.setObjectName("projectPage_project_link")
        self.projectPage_project_link.setStyleSheet("""
                                                    background-color: #eeeeee;
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.projectPage_project_link.setText("Test Plan/Suites")
        self.gridLayout_snsNavTabProject.addWidget(self.projectPage_project_link, 0, 1, 1, 1, Qt.AlignLeft)
        
        self.percondition_periodic_Switch_link = QtWidgets.QPushButton(self.snsNavTabProject)
        self.percondition_periodic_Switch_link.setMinimumSize(QtCore.QSize(150, 16777215))
        self.percondition_periodic_Switch_link.setObjectName("percondition_periodic_Switch_link")
        self.percondition_periodic_Switch_link.setStyleSheet("""
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    background-color: #0c0c0c;
                                                    color:white;
                                                    """)
        self.percondition_periodic_Switch_link.setText("PERIODIC")
        self.gridLayout_snsNavTabProject.addWidget(self.percondition_periodic_Switch_link, 0, 2, 1, 18, Qt.AlignRight)
        
        
        self.result_Switch_link = QtWidgets.QPushButton(self.snsNavTabProject)
        self.result_Switch_link.setMinimumSize(QtCore.QSize(150, 16777215))
        # self.titleProjectButtonLabel.setMaximumSize(QtCore.QSize(150, 16777215))
        self.result_Switch_link.setObjectName("projectPage_project_link")
        self.result_Switch_link.setStyleSheet("""
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    background-color: black;
                                                    color:white;
                                                    """)
        self.result_Switch_link.setText("RESULTS")
        self.gridLayout_snsNavTabProject.addWidget(self.result_Switch_link, 0, 3, 1, 20, Qt.AlignRight)
        
        
        self.gridLayout_projectPageSNS.addWidget(self.snsNavTabProject, 0, 0, 1, 1)
        
        
        self.newProjectWidgetSNS = QtWidgets.QWidget(self.projectPageSNS)
        self.newProjectWidgetSNS.setMaximumSize(QtCore.QSize(16777215, 100))
        self.newProjectWidgetSNS.setStyleSheet("background-color: #eeeeee;")
        self.newProjectWidgetSNS.setObjectName("newProjectWidgetSNS")
        self.gridLayout_newProjectWidgetSNS = QtWidgets.QGridLayout(self.newProjectWidgetSNS)
        self.gridLayout_newProjectWidgetSNS.setContentsMargins(-1, 9, -1, 9)
        self.gridLayout_newProjectWidgetSNS.setObjectName("gridLayout_newProjectWidgetSNS")
        
        self.projectLabelWidgetSNS = QtWidgets.QWidget(self.newProjectWidgetSNS)
        self.projectLabelWidgetSNS.setObjectName("projectLabelWidgetSNS")
        self.VLayout_ProjectLabelWidgetSNS = QtWidgets.QVBoxLayout(self.projectLabelWidgetSNS)
        self.VLayout_ProjectLabelWidgetSNS.setContentsMargins(0, 0, 0, 0)
        self.VLayout_ProjectLabelWidgetSNS.setObjectName("VLayout_ProjectLabelWidgetSNS")
        self.title_projectView = QtWidgets.QLabel(self.projectLabelWidgetSNS)
        self.VLayout_ProjectLabelWidgetSNS.addWidget(self.title_projectView)
        self.title_projectView.setText("TEST PLAN")
        self.gridLayout_newProjectWidgetSNS.addWidget(self.projectLabelWidgetSNS, 0, 0, 1, 1)
        
        self.ProjectMenuWidget = QtWidgets.QWidget(self.newProjectWidgetSNS)
        self.ProjectMenuWidget.setObjectName("ProjectMenuWidget")
        self.ProjectMenuWidget_Hlayout = QtWidgets.QHBoxLayout(self.ProjectMenuWidget)
        
        self.projectNameLabel = QtWidgets.QLabel(self.newProjectWidgetSNS)
        self.projectNameLabel.setObjectName("projectNameLabel")
        self.projectNameLabel.setMinimumSize(QtCore.QSize(16777215, 16777215))
        self.projectNameLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ProjectMenuWidget_Hlayout.addWidget(self.projectNameLabel)
        self.openProjectPushButton = QtWidgets.QPushButton(self.newProjectWidgetSNS)
        self.openProjectPushButton.setMinimumSize(QtCore.QSize(150, 16777215))
        self.openProjectPushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.openProjectPushButton.setObjectName("openProjectPushButton")
        self.ProjectMenuWidget_Hlayout.addWidget(self.openProjectPushButton)
        self.newProjectPushButton = QtWidgets.QPushButton(self.newProjectWidgetSNS)
        self.newProjectPushButton.setMinimumSize(QtCore.QSize(150, 16777215))
        self.newProjectPushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.newProjectPushButton.setObjectName("newProjectPushButton")
        self.ProjectMenuWidget_Hlayout.addWidget(self.newProjectPushButton)
        
        self.menuProjectToolBar = QToolButton(self.newProjectWidgetSNS)
        self.menuProjectToolBar.setText("☰")
        self.menuProjectToolBar.setPopupMode(QToolButton.InstantPopup)
        
        self.menu = QMenu(self.menuProjectToolBar)
        self.menu.addAction("Delete Plan")
        self.menu.addAction("Import Plan")
        self.menu.addSeparator()
        self.menu.addAction("Exit", self.menu.close)
        self.menuProjectToolBar.setMenu(self.menu)
        self.menu.popup(self.menuProjectToolBar.mapToGlobal(self.menuProjectToolBar.rect().bottomLeft()))
        self.ProjectMenuWidget_Hlayout.addWidget(self.menuProjectToolBar)
        
        self.gridLayout_newProjectWidgetSNS.addWidget(self.ProjectMenuWidget,1,0,1,1)
        self.gridLayout_projectPageSNS.addWidget(self.newProjectWidgetSNS, 1, 0, 1, 1)
        
        self.projectContentWidgetSNS = QtWidgets.QWidget(self.projectPageSNS)
        self.projectContentWidgetSNS.setStyleSheet("background-color: #eeeeee")
        self.projectContentWidgetSNS.setObjectName("projectContentWidgetSNS")
        self.verticalLayout_projectContentWidgetSNS = QtWidgets.QVBoxLayout(self.projectContentWidgetSNS)
        self.verticalLayout_projectContentWidgetSNS.setContentsMargins(-1, 9, -1, 9)
        self.verticalLayout_projectContentWidgetSNS.setObjectName("verticalLayout_projectContentWidgetSNS")
        
        self.functionLabelWidgetSNS = QtWidgets.QWidget(self.projectContentWidgetSNS)
        self.functionLabelWidgetSNS.setObjectName("functionLabelWidgetSNS")
        self.HLayout_functionLabelWidgetSNS = QtWidgets.QHBoxLayout(self.functionLabelWidgetSNS)
        self.HLayout_functionLabelWidgetSNS.setContentsMargins(0, 0, 0, 0)
        self.HLayout_functionLabelWidgetSNS.setObjectName("HLayout_functionLabelWidgetSNS")
        self.title_functionView = QtWidgets.QLabel(self.functionLabelWidgetSNS)
        self.HLayout_functionLabelWidgetSNS.addWidget(self.title_functionView)
        self.title_functionView.setText("TEST SUITES")
        
        
        # 11/02/2026 settings
        self.settingsSNS = QtWidgets.QPushButton(self.functionLabelWidgetSNS)
        self.settingsSNS.setFixedSize(QtCore.QSize(40, 35))
        self.settingsSNS.setObjectName("settingsSNS")
        self.settingsSNS.setStyleSheet("""
                                              QPushButton{
                                                  border: 0px;
                                         
                                              }
                                              QPushButton:hover{
                                                  background-color: #ffffff;
                                              }
                                                    """)
        self.menu = QMenu(self.settingsSNS)
        self.setIPPortAction = QAction("Set IP/PORT")
        self.setIPPortAction.triggered.connect(self.setIPPort)
        self.menu.addAction(self.setIPPortAction)
        
        self.setDefaultDelayAction = QAction("Set Defalut Delay")
        self.setDefaultDelayAction.triggered.connect(self.setDefaultDelay)
        self.menu.addAction(self.setDefaultDelayAction)
        
        self.setDefaultPeriodicAction = QAction("Set defalut Periodic")
        self.setDefaultPeriodicAction.triggered.connect(self.setDefaultPeriodic)
        self.menu.addAction(self.setDefaultPeriodicAction)
        
        self.menu.addSeparator()
        self.menu.addAction("Exit", self.menu.close)
        
        self.settingsSNS.setMenu(self.menu)
        self.menu.popup(self.settingsSNS.mapToParent(self.settingsSNS.rect().bottomLeft()))
        
        self.HLayout_functionLabelWidgetSNS.addWidget(self.settingsSNS)
        
        self.verticalLayout_projectContentWidgetSNS.addWidget(self.functionLabelWidgetSNS)
        
        self.functionOperationsWidgetSNS = QtWidgets.QWidget(self.projectContentWidgetSNS)
        self.functionOperationsWidgetSNS.setMinimumSize(QtCore.QSize(0, 40))
        self.functionOperationsWidgetSNS.setMaximumSize(QtCore.QSize(16777215, 40))
        self.functionOperationsWidgetSNS.setObjectName("functionOperationsWidgetSNS")
        self.gridLayout_functionOperationsWidgetSNS = QtWidgets.QGridLayout(self.functionOperationsWidgetSNS)
        self.gridLayout_functionOperationsWidgetSNS.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_functionOperationsWidgetSNS.setObjectName("gridLayout_functionOperationsWidgetSNS")
        self.gridLayout_functionOperationsWidgetSNS.setColumnStretch(1,5)
        
        self.functionAddPushButton = QtWidgets.QPushButton(self.functionOperationsWidgetSNS)
        self.functionAddPushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.functionAddPushButton.setMinimumSize(QtCore.QSize(150, 16777215))
        self.functionAddPushButton.setObjectName("functionAddPushButton")
        self.gridLayout_functionOperationsWidgetSNS.addWidget(self.functionAddPushButton, 0, 6, 1, 1)
       
        
        self.functionSendSelectedPushButton = QtWidgets.QPushButton(self.functionOperationsWidgetSNS)
        self.functionSendSelectedPushButton.setMinimumSize(QtCore.QSize(150, 16777215))
        self.functionSendSelectedPushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.functionSendSelectedPushButton.setObjectName("functionSendSelectedPushButton")
        self.gridLayout_functionOperationsWidgetSNS.addWidget(self.functionSendSelectedPushButton, 0, 7, 1, 1)
        
        self.functionDeleteSelectedPushButton = QtWidgets.QPushButton(self.functionOperationsWidgetSNS)
        self.functionDeleteSelectedPushButton.setMinimumSize(QtCore.QSize(150, 16777215))
        self.functionDeleteSelectedPushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.functionDeleteSelectedPushButton.setObjectName("functionDeleteSelectedPushButton")
        self.gridLayout_functionOperationsWidgetSNS.addWidget(self.functionDeleteSelectedPushButton, 0, 8, 1, 1)
        
        
        self.functionSelectAllPushButton = QtWidgets.QPushButton(self.functionOperationsWidgetSNS)
        self.functionSelectAllPushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.functionSelectAllPushButton.setMinimumSize(QtCore.QSize(150, 16777215))
        self.functionSelectAllPushButton.setObjectName("functionSelectAllPushButton")
        self.gridLayout_functionOperationsWidgetSNS.addWidget(self.functionSelectAllPushButton, 0, 9, 1, 1)
        
        
        self.functionSavePushButton = QtWidgets.QPushButton(self.functionOperationsWidgetSNS)
        self.functionSavePushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.functionSavePushButton.setMinimumSize(QtCore.QSize(150, 16777215))
        self.functionSavePushButton.setObjectName("functionSavePushButton")
        self.gridLayout_functionOperationsWidgetSNS.addWidget(self.functionSavePushButton, 0, 10, 1, 1)
        self.functionSavePushButton.setEnabled(False)
        self.functionSavePushButton.hide()
        
        self.functionCancelPushButton = QtWidgets.QPushButton(self.functionOperationsWidgetSNS)
        self.functionCancelPushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.functionCancelPushButton.setMinimumSize(QtCore.QSize(150, 16777215))
        self.functionCancelPushButton.setObjectName("functionCancelPushButton")
        self.gridLayout_functionOperationsWidgetSNS.addWidget(self.functionCancelPushButton, 0, 11, 1, 1)
        self.functionCancelPushButton.setEnabled(False)
        self.functionCancelPushButton.hide()
        
        self.verticalLayout_projectContentWidgetSNS.addWidget(self.functionOperationsWidgetSNS)
        
        
        
        
        # self.funtionTestCasesListWidgetSNS = QtWidgets.QListWidget(self.projectContentWidgetSNS)
        self.funtionTestCasesListWidgetSNS =  SafeListWidget()
        self.funtionTestCasesListWidgetSNS.setStyleSheet("border-radius: 0px;\n"
                                                         "background-color: #eeeeee;")
        self.funtionTestCasesListWidgetSNS.setObjectName("funtionTestCasesListWidgetSNS")
        
        # self.funtionTestCasesListWidgetSNS.setDragEnabled(True)
        # self.funtionTestCasesListWidgetSNS.setAcceptDrops(True)
        # self.funtionTestCasesListWidgetSNS.setDropIndicatorShown(True)
        # self.funtionTestCasesListWidgetSNS.setDragDropMode(QtWidgets.QListWidget.InternalMove)
        # self.funtionTestCasesListWidgetSNS.setDefaultDropAction(Qt.MoveAction)
        
        self.verticalLayout_projectContentWidgetSNS.addWidget(self.funtionTestCasesListWidgetSNS)
        # self.funtionTestCasesListWidgetSNS.setSelectionMode(QtWidgets.QListWidget.MultiSelection)
        self.gridLayout_projectPageSNS.addWidget(self.projectContentWidgetSNS, 2, 0, 1, 1)
        self.stackedWidgetSNS.addWidget(self.projectPageSNS)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        
        
        
        
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        # Page Test Cases
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        self.TestCasePageSNS = QtWidgets.QWidget()
        self.TestCasePageSNS.setObjectName("TestCasePageSNS")
        self.gridLayout_TestCasePageSNS = QtWidgets.QGridLayout(self.TestCasePageSNS)
        self.gridLayout_TestCasePageSNS.setObjectName("gridLayout_TestCasePageSNS")
        
        # NAV
        self.snsNavTabFunction = QtWidgets.QWidget(self.projectPageSNS)
        self.snsNavTabFunction.setMaximumSize(QtCore.QSize(16777215, 100))
        self.snsNavTabFunction.setObjectName("snsNavTabFunction")
        self.gridLayout_snsNavTabFunction = QtWidgets.QGridLayout(self.snsNavTabFunction)
        self.gridLayout_snsNavTabFunction.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_snsNavTabFunction.setObjectName("gridLayout_snsNavTabFunction")  

        self.testCasePage_back = backButton()
        self.gridLayout_snsNavTabFunction.addWidget(self.testCasePage_back, 0, 0, 1, 1, Qt.AlignLeft)
        
        
        self.functionPage_project_link = QtWidgets.QPushButton(self.snsNavTabFunction)
        self.functionPage_project_link.setMinimumSize(QtCore.QSize(150, 16777215))
        self.functionPage_project_link.setObjectName("functionPage_project_link")
        self.functionPage_project_link.setStyleSheet("""
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.functionPage_project_link.setText("Test Plan/Suites")
        self.gridLayout_snsNavTabFunction.addWidget(self.functionPage_project_link, 0, 1, 1, 1, Qt.AlignLeft)
        
        self.functionPage_function_link = QtWidgets.QPushButton(self.snsNavTabFunction)
        self.functionPage_function_link.setMinimumSize(QtCore.QSize(150, 16777215))
        self.functionPage_function_link.setObjectName("functionPage_function_link")
        self.functionPage_function_link.setStyleSheet("""
                                                    background-color: #eeeeee;
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.functionPage_function_link.setText("Test Cases")
        self.gridLayout_snsNavTabFunction.addWidget(self.functionPage_function_link, 0, 2, 1, 1, Qt.AlignLeft)
        
        
        self.result_Switch_test_case_link = QtWidgets.QPushButton(self.snsNavTabProject)
        self.result_Switch_test_case_link.setMinimumSize(QtCore.QSize(150, 16777215))
        self.result_Switch_test_case_link.setObjectName("projectPage_project_link")
        self.result_Switch_test_case_link.setStyleSheet("""
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    background-color: black;
                                                    color:white;
                                                    """)
        self.result_Switch_test_case_link.setText("RESULTS")
        self.gridLayout_snsNavTabFunction.addWidget(self.result_Switch_test_case_link, 0, 3, 1, 20, Qt.AlignRight)
        
        self.gridLayout_TestCasePageSNS.addWidget(self.snsNavTabFunction, 0, 0, 1, 1)
        
        
        #Top Info Bar
        self.addTestCaseWidget = snsInfoBar()
        # self.addTestCaseWidget = QtWidgets.QWidget(self.TestCasePageSNS)
        # self.addTestCaseWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        # self.addTestCaseWidget.setObjectName("addTestCaseWidget")
        # # self.addTestCaseWidget.setStyleSheet("""
        # #                                      background-color: #464c40;
        # #                                      """)
        # self.gridLayout_addTestCaseWidget = QtWidgets.QGridLayout(self.addTestCaseWidget)
        # self.gridLayout_addTestCaseWidget.setObjectName("gridLayout_addTestCaseWidget")
        
        # self.functionTitleLabel = QtWidgets.QLabel(self.TestCasePageSNS)
        # self.functionTitleLabel.setObjectName("functionTitleLabel")
        # self.functionTitleLabel.setText("FUNCTION NAME")
        # self.functionTitleLabel.setStyleSheet("""
        #                                      font-size: 14px;
        #                                      font-weight: bold;
        #                                      color: #888888;
        #                                      """)
        # self.gridLayout_addTestCaseWidget.addWidget(self.functionTitleLabel, 0, 0, 1, 1)
        
        self.gridLayout_TestCasePageSNS.addWidget(self.addTestCaseWidget, 1, 0)
        

        
        self.TestCasesAddedWidget = QtWidgets.QWidget(self.TestCasePageSNS)
        self.TestCasesAddedWidget.setObjectName("TestCasesAddedWidget")
        self.TestCasesAddedWidget.setStyleSheet("""
                                                QWidget{
                                                    background-color: #eeeeee; 
                                                    }

                                                """)
        self.gridLayout_TestCasesAddedWidget = QtWidgets.QGridLayout(self.TestCasesAddedWidget)
        self.gridLayout_TestCasesAddedWidget.setObjectName("gridLayout_TestCasesAddedWidget")
        
        
                
        self.TestCaseLabelWidgetSNS = QtWidgets.QWidget(self.TestCasesAddedWidget)
        self.TestCaseLabelWidgetSNS.setObjectName("TestCaseLabelWidgetSNS")
        self.VLayout_TestCaseLabelWidgetSNS = QtWidgets.QVBoxLayout(self.TestCaseLabelWidgetSNS)
        self.VLayout_TestCaseLabelWidgetSNS.setContentsMargins(0, 0, 0, 0)
        self.VLayout_TestCaseLabelWidgetSNS.setObjectName("VLayout_TestCaseLabelWidgetSNS")
        self.title_TestCasewView = QtWidgets.QLabel(self.TestCasesAddedWidget)
        self.VLayout_TestCaseLabelWidgetSNS.addWidget(self.title_TestCasewView)
        self.title_TestCasewView.setText("TEST CASES")
        self.gridLayout_TestCasesAddedWidget.addWidget(self.TestCaseLabelWidgetSNS, 0, 0, 1, 1)
        
        self.TestCaseOptions = QtWidgets.QWidget(self.TestCasesAddedWidget)
        self.TestCaseOptionsLayout = QtWidgets.QHBoxLayout(self.TestCaseOptions)
        
        # add
        self.addTestCasePushButton = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.addTestCasePushButton.setObjectName("addTestCasePushButton")
        self.addTestCasePushButton.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.addTestCasePushButton.setMinimumSize(QtCore.QSize(60, 30))
        self.TestCaseOptionsLayout.addWidget(self.addTestCasePushButton)
        
        # send all
        self.addTestCaseSendAll = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.addTestCaseSendAll.setObjectName("addTestCasePushButton")
        self.addTestCaseSendAll.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.addTestCaseSendAll.setMinimumSize(QtCore.QSize(160, 30))
        self.TestCaseOptionsLayout.addWidget(self.addTestCaseSendAll)
        
        # delete all
        self.addTestCaseDeleteAll = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.addTestCaseDeleteAll.setObjectName("addTestCaseDeleteAll")
        self.addTestCaseDeleteAll.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.addTestCaseDeleteAll.setMinimumSize(QtCore.QSize(160, 30))
        self.TestCaseOptionsLayout.addWidget(self.addTestCaseDeleteAll)
        # copy
        self.addTestCaseCopySelected = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.addTestCaseCopySelected.setObjectName("addTestCaseCopySelected")
        self.addTestCaseCopySelected.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.addTestCaseCopySelected.setMinimumSize(QtCore.QSize(160, 30))
        self.TestCaseOptionsLayout.addWidget(self.addTestCaseCopySelected)
        # paste
        self.addTestCasePasteSelected = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.addTestCasePasteSelected.setObjectName("addTestCasePasteSelected")
        self.addTestCasePasteSelected.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.addTestCasePasteSelected.setMinimumSize(QtCore.QSize(160, 30))
        self.TestCaseOptionsLayout.addWidget(self.addTestCasePasteSelected)
        
        # select
        self.addTestCaseSelectAll = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.addTestCaseSelectAll.setObjectName("addTestCaseSelectAll")
        self.addTestCaseSelectAll.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.addTestCaseSelectAll.setMinimumSize(QtCore.QSize(160, 30))
        self.TestCaseOptionsLayout.addWidget(self.addTestCaseSelectAll)
        
        # save
        self.testCaseSavePushButton = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.testCaseSavePushButton.setObjectName("testCaseSavePushButton")
        self.testCaseSavePushButton.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.testCaseSavePushButton.setMinimumSize(QtCore.QSize(160, 30))
        self.TestCaseOptionsLayout.addWidget(self.testCaseSavePushButton)
        self.testCaseSavePushButton.hide()
        
        # cancel
        self.testCaseCancelPushButton = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.testCaseCancelPushButton.setObjectName("addTestCaseSelectAll")
        self.testCaseCancelPushButton.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.testCaseCancelPushButton.setMinimumSize(QtCore.QSize(160, 30))
        self.TestCaseOptionsLayout.addWidget(self.testCaseCancelPushButton)
        self.testCaseCancelPushButton.hide()
        
        
        self.gridLayout_TestCasesAddedWidget.addWidget(self.TestCaseOptions, 1, 0, 1, 1)
        
        
        self.newTestCasesListWidget = SafeListWidget()
        self.newTestCasesListWidget.setObjectName("newTestCasesListWidget")
        self.newTestCasesListWidget.setStyleSheet("""
                                                  border-radius: 0px;
                                                  """)
        self.gridLayout_TestCasesAddedWidget.addWidget(self.newTestCasesListWidget, 2, 0, 1, 1)
        self.gridLayout_TestCasePageSNS.addWidget(self.TestCasesAddedWidget, 2, 0, 1, 1)
        self.stackedWidgetSNS.addWidget(self.TestCasePageSNS)
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        
        

        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        # Page INPUT Messages Details
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        self.MessagePageSNS = QtWidgets.QWidget()
        self.MessagePageSNS.setObjectName("MessagePageSNS")
        self.gridLayout_MessagePageSNS = QtWidgets.QGridLayout(self.MessagePageSNS)
        self.gridLayout_MessagePageSNS.setObjectName("gridLayout_MessagePageSNS")
        
        
        #Nav
        self.snsNavTabTC = QtWidgets.QWidget(self.projectPageSNS)
        self.snsNavTabTC.setMaximumSize(QtCore.QSize(16777215, 100))
        self.snsNavTabTC.setObjectName("snsNavTabTC")
        self.gridLayout_snsNavTabTC = QtWidgets.QGridLayout(self.snsNavTabTC)
        self.gridLayout_snsNavTabTC.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_snsNavTabTC.setObjectName("gridLayout_snsNavTabTC")  
        
        self.inputMessagePage_back = backButton()
        self.gridLayout_snsNavTabTC.addWidget(self.inputMessagePage_back, 0, 0, 1, 1, Qt.AlignLeft)
        
        self.TCPage_project_link = QtWidgets.QPushButton(self.snsNavTabTC)
        self.TCPage_project_link.setMinimumSize(QtCore.QSize(150, 16777215))
        self.TCPage_project_link.setObjectName("TCPage_project_link")
        self.TCPage_project_link.setStyleSheet("""
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.TCPage_project_link.setText("Test Plan/Suites")
        self.gridLayout_snsNavTabTC.addWidget(self.TCPage_project_link, 0, 1, 1, 1, Qt.AlignLeft)
        
        self.TCPage_function_link = QtWidgets.QPushButton(self.snsNavTabTC)
        self.TCPage_function_link.setMinimumSize(QtCore.QSize(150, 16777215))
        self.TCPage_function_link.setObjectName("TCPage_function_link")
        self.TCPage_function_link.setStyleSheet("""
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.TCPage_function_link.setText("Test Cases")
        self.gridLayout_snsNavTabTC.addWidget(self.TCPage_function_link, 0, 2, 1, 1, Qt.AlignLeft)
        
        self.TCPage_TC_link = QtWidgets.QPushButton(self.snsNavTabTC)
        self.TCPage_TC_link.setMinimumSize(QtCore.QSize(150, 16777215))
        self.TCPage_TC_link.setObjectName("TCPage_TC_link")
        self.TCPage_TC_link.setStyleSheet("""
                                                    background-color: #eeeeee;
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.TCPage_TC_link.setText("Input Messages")
        # self.TCPage_TC_link.setDisabled(True)
        self.gridLayout_snsNavTabTC.addWidget(self.TCPage_TC_link, 0, 3, 1, 20, Qt.AlignLeft)
        self.gridLayout_MessagePageSNS.addWidget(self.snsNavTabTC, 0, 0, 1, 1)
        
        #INFO BAR
        self.TestCaseNameInMessagePageWidget = snsInfoBar()
        # self.TestCaseNameInMessagePageWidget = QtWidgets.QWidget(self.MessagePageSNS)
        # self.TestCaseNameInMessagePageWidgetLayout = QtWidgets.QHBoxLayout(self.TestCaseNameInMessagePageWidget)
        # self.TestCaseNameInMessagePageWidget.setStyleSheet("""
        #                                      background-color: #ffffff;
        #                                      """)
        # self.CurrentTCLabel = QtWidgets.QLabel(self.MessagePageSNS)
        # self.CurrentTCLabel.setObjectName("functionTestCaseLabel")
        # self.CurrentTCLabel.setStyleSheet("""
        #                                      font-size: 14px;
        #                                      font-weight: bold;
        #                                      color: #888888;
        #                                   """)
        # self.TestCaseNameInMessagePageWidgetLayout.addWidget(self.CurrentTCLabel)
        # self.CurrentTCLabel.setText("TEST CASE: ")
        self.gridLayout_MessagePageSNS.addWidget(self.TestCaseNameInMessagePageWidget, 1, 0, 1, 1)
        
        #next
        self.messagesAddedWidget = QtWidgets.QWidget(self.MessagePageSNS)
        self.messagesAddedWidget.setObjectName("messagesAddedWidget")
        self.messagesAddedWidget.setStyleSheet("""
                                                QWidget{
                                                    background-color: #eeeeee; 
                                                    }

                                                """)
        self.gridLayout_messagesAddedWidget = QtWidgets.QGridLayout(self.messagesAddedWidget)
        self.gridLayout_messagesAddedWidget.setObjectName("gridLayout_messagesAddedWidget")
        
        
        self.inputMessagesLabelWidgetSNS = QtWidgets.QWidget(self.messagesAddedWidget)
        self.inputMessagesLabelWidgetSNS.setObjectName("inputMessagesLabelWidgetSNS")
        self.VLayout_inputMessagesLabelWidgetSNS = QtWidgets.QVBoxLayout(self.inputMessagesLabelWidgetSNS)
        self.VLayout_inputMessagesLabelWidgetSNS.setContentsMargins(0, 0, 0, 0)
        self.VLayout_inputMessagesLabelWidgetSNS.setObjectName("VLayout_inputMessagesLabelWidgetSNS")
        self.title_InputMessagesView = QtWidgets.QLabel(self.inputMessagesLabelWidgetSNS)
        self.VLayout_inputMessagesLabelWidgetSNS.addWidget(self.title_InputMessagesView)
        self.title_InputMessagesView.setText("INPUT MESSAGES")
        self.gridLayout_messagesAddedWidget.addWidget(self.inputMessagesLabelWidgetSNS, 0, 0, 1, 1)
        
        
        self.messagesOptions = QtWidgets.QWidget(self.messagesAddedWidget)
        self.messagesOptionsLayout = QtWidgets.QHBoxLayout(self.messagesOptions)
        self.addMessagePushButton = QtWidgets.QPushButton(self.messagesOptions)
        self.addMessagePushButton.setObjectName("addMessagePushButton")
        self.addMessagePushButton.setStyleSheet("""
                                                background-color: #ffffff;
                                                """)
        self.addMessagePushButton.setMinimumSize(QtCore.QSize(16777215,40))
        self.messagesOptionsLayout.addWidget(self.addMessagePushButton)
        
        self.addEmptyMessagePushButton = QtWidgets.QPushButton(self.messagesOptions)
        self.addEmptyMessagePushButton.setObjectName("addEmptyMessagePushButton")
        self.addEmptyMessagePushButton.setStyleSheet("""
                                                background-color: #ffffff;
                                                """)
        self.addEmptyMessagePushButton.setMinimumSize(QtCore.QSize(16777215,40))
        self.messagesOptionsLayout.addWidget(self.addEmptyMessagePushButton)
        
        self.addGuiInputMessagePushButton = QtWidgets.QPushButton(self.messagesOptions)
        self.addGuiInputMessagePushButton.setObjectName("addGuiInputMessagePushButton")
        self.addGuiInputMessagePushButton.setStyleSheet("""
                                                background-color: #ffffff;
                                                """)
        self.addGuiInputMessagePushButton.setMinimumSize(QtCore.QSize(16777215,40))
        self.messagesOptionsLayout.addWidget(self.addGuiInputMessagePushButton)
        # self.SendAllTestCasesPushButton = QtWidgets.QPushButton(self.messagesOptions)
        # self.SendAllTestCasesPushButton.setObjectName("SendAllTestCasesPushButton")
        # self.SendAllTestCasesPushButton.setStyleSheet("""
        #                                         background-color: #ffffff;
        #                                         """)
        # self.SendAllTestCasesPushButton.setMinimumSize(QtCore.QSize(16777215,40))
        # self.messagesOptionsLayout.addWidget(self.SendAllTestCasesPushButton)
        
        
        self.deleteAllInputPushButton = QtWidgets.QPushButton(self.messagesOptions)
        self.deleteAllInputPushButton.setObjectName("deleteAllInputPushButton")
        self.deleteAllInputPushButton.setStyleSheet("""
                                                background-color: #ffffff;
                                                """)
        self.deleteAllInputPushButton.setMinimumSize(QtCore.QSize(16777215,40))
        self.messagesOptionsLayout.addWidget(self.deleteAllInputPushButton)
        
        self.selectAllInputPushButton = QtWidgets.QPushButton(self.messagesOptions)
        self.selectAllInputPushButton.setObjectName("selectAllInputPushButton")
        self.selectAllInputPushButton.setStyleSheet("""
                                                background-color: #ffffff;
                                                """)
        self.selectAllInputPushButton.setMinimumSize(QtCore.QSize(16777215,40))
        self.messagesOptionsLayout.addWidget(self.selectAllInputPushButton)
        
        # save
        self.SaveInputPushButton = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.SaveInputPushButton.setObjectName("SaveInputPushButton")
        self.SaveInputPushButton.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.SaveInputPushButton.setMinimumSize(QtCore.QSize(160, 30))
        self.messagesOptionsLayout.addWidget(self.SaveInputPushButton)
        self.SaveInputPushButton.hide()
        
        # cancel
        self.cancelInputPushButton = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.cancelInputPushButton.setObjectName("cancelInputPushButton")
        self.cancelInputPushButton.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.cancelInputPushButton.setMinimumSize(QtCore.QSize(160, 30))
        self.messagesOptionsLayout.addWidget(self.cancelInputPushButton)
        self.cancelInputPushButton.hide()
        
        
        self.gridLayout_messagesAddedWidget.addWidget(self.messagesOptions, 1, 0, 1, 1)
        
        self.newMessagesListWidget = SafeListWidget()
        self.newMessagesListWidget.setStyleSheet("""
                                                 border: 0px;
                                                 """)
        self.newMessagesListWidget.setObjectName("newMessagesListWidget")
        self.gridLayout_messagesAddedWidget.addWidget(self.newMessagesListWidget, 2, 0, 1, 1)
        
        self.gridLayout_MessagePageSNS.addWidget(self.messagesAddedWidget, 2, 0, 1, 1)
        self.stackedWidgetSNS.addWidget(self.MessagePageSNS)    
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        
        
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        # Page OUTPUT Messages Details
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        self.outputMessagePageSNS = QtWidgets.QWidget()
        self.outputMessagePageSNS.setObjectName("outputMessagePageSNS")
        self.gridLayout_outputMessagePageSNS = QtWidgets.QGridLayout(self.outputMessagePageSNS)
        self.gridLayout_outputMessagePageSNS.setObjectName("gridLayout_outputMessagePageSNS")
        
        # >> Nav links
        self.snsNavTabOutput = QtWidgets.QWidget(self.projectPageSNS)
        self.snsNavTabOutput.setMaximumSize(QtCore.QSize(16777215, 100))
        self.snsNavTabOutput.setObjectName("snsNavTabOutput")
        self.gridLayout_snsNavTabOutput = QtWidgets.QGridLayout(self.snsNavTabOutput)
        self.gridLayout_snsNavTabOutput.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_snsNavTabOutput.setObjectName("gridLayout_snsNavTabOutput") 
        
        
        self.outputMessagePage_back = backButton()
        self.gridLayout_snsNavTabOutput.addWidget(self.outputMessagePage_back, 0, 0, 1, 1, Qt.AlignLeft)
        
        self.outputPage_project_link = QtWidgets.QPushButton(self.snsNavTabOutput)
        self.outputPage_project_link.setMinimumSize(QtCore.QSize(150, 16777215))
        self.outputPage_project_link.setObjectName("outputPage_project_link")
        self.outputPage_project_link.setStyleSheet("""
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.outputPage_project_link.setText("Test Plan/Suites")
        self.gridLayout_snsNavTabOutput.addWidget(self.outputPage_project_link, 0, 1, 1, 1, Qt.AlignLeft)
        
        self.outputPage_TestCase_link = QtWidgets.QPushButton(self.snsNavTabOutput)
        self.outputPage_TestCase_link.setMinimumSize(QtCore.QSize(150, 16777215))
        self.outputPage_TestCase_link.setObjectName("outputPage_TestCase_link")
        self.outputPage_TestCase_link.setStyleSheet("""
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.outputPage_TestCase_link.setText("Test Cases")
        self.gridLayout_snsNavTabOutput.addWidget(self.outputPage_TestCase_link, 0, 2, 1, 1, Qt.AlignLeft)
        
        self.outputPage_InputMessage_link = QtWidgets.QPushButton(self.snsNavTabOutput)
        self.outputPage_InputMessage_link.setMinimumSize(QtCore.QSize(150, 16777215))
        self.outputPage_InputMessage_link.setObjectName("outputPage_InputMessage_link")
        self.outputPage_InputMessage_link.setStyleSheet("""
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.outputPage_InputMessage_link.setText("Input Messages")
        # self.TCPage_TC_link.setDisabled(True)
        self.gridLayout_snsNavTabOutput.addWidget(self.outputPage_InputMessage_link, 0, 3, 1, 1, Qt.AlignLeft)
        
        self.outputPage_OutputMessage_link = QtWidgets.QPushButton(self.snsNavTabOutput)
        self.outputPage_OutputMessage_link.setMinimumSize(QtCore.QSize(150, 16777215))
        self.outputPage_OutputMessage_link.setObjectName("outputPage_OutputMessage_link")
        self.outputPage_OutputMessage_link.setStyleSheet("""
                                                    border: 1px solid #eeeeee;
                                                    background-color: #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.outputPage_OutputMessage_link.setText("Output Messages")
        # self.TCPage_TC_link.setDisabled(True)
        self.gridLayout_snsNavTabOutput.addWidget(self.outputPage_OutputMessage_link, 0, 4, 1, 20, Qt.AlignLeft)
        self.gridLayout_outputMessagePageSNS.addWidget(self.snsNavTabOutput, 0, 0, 1, 1)
        
        # >> INFO BAR
        self.outputMessageNameInMessagePageWidget = snsInfoBar()
        # self.outputMessageNameInMessagePageWidget = QtWidgets.QWidget(self.outputMessagePageSNS)
        # self.outputMessageNameInMessagePageWidgetLayout = QtWidgets.QHBoxLayout(self.outputMessageNameInMessagePageWidget)
        # self.outputMessageNameInMessagePageWidget.setStyleSheet("""
        #                                       background-color: #ffffff;
        #                                       """)
        # self.CurrentOutputMessageLabel = QtWidgets.QLabel(self.outputMessagePageSNS)
        # self.CurrentOutputMessageLabel.setObjectName("functionTestCaseLabel")
        # self.CurrentOutputMessageLabel.setStyleSheet("""
        #                                       font-size: 14px;
        #                                       font-weight: bold;
        #                                       color: #888888;
        #                                   """)
        # self.outputMessageNameInMessagePageWidgetLayout.addWidget(self.CurrentOutputMessageLabel)
        # self.CurrentOutputMessageLabel.setText("TEST CASE: ")
        self.gridLayout_outputMessagePageSNS.addWidget(self.outputMessageNameInMessagePageWidget, 1, 0, 1, 1)
        
        #next
        self.OutputMessagesAddedWidget = QtWidgets.QWidget(self.outputMessagePageSNS)
        self.OutputMessagesAddedWidget.setObjectName("OutputMessagesAddedWidget")
        self.OutputMessagesAddedWidget.setStyleSheet("""
                                                QWidget{
                                                    background-color: #eeeeee; 
                                                    }
                                                """)
        self.gridLayout_OutputMessagesAddedWidget = QtWidgets.QGridLayout(self.OutputMessagesAddedWidget)
        self.gridLayout_OutputMessagesAddedWidget.setObjectName("gridLayout_OutputMessagesAddedWidget")
        
        # where are you details
        self.outputMessagesLabelWidgetSNS = QtWidgets.QWidget(self.OutputMessagesAddedWidget)
        self.outputMessagesLabelWidgetSNS.setObjectName("outputMessagesLabelWidgetSNS")
        self.VLayout_outputMessagesLabelWidgetSNS = QtWidgets.QVBoxLayout(self.outputMessagesLabelWidgetSNS)
        self.VLayout_outputMessagesLabelWidgetSNS.setContentsMargins(0, 0, 0, 0)
        self.VLayout_outputMessagesLabelWidgetSNS.setObjectName("VLayout_outputMessagesLabelWidgetSNS")
        self.title_outputMessagesView = QtWidgets.QLabel(self.outputMessagesLabelWidgetSNS)
        self.VLayout_outputMessagesLabelWidgetSNS.addWidget(self.title_outputMessagesView)
        self.title_outputMessagesView.setText("OUTPUT MESSAGES")
        self.gridLayout_OutputMessagesAddedWidget.addWidget(self.outputMessagesLabelWidgetSNS, 0, 0, 1, 1)
        
        
        self.outputMessagesOptions = QtWidgets.QWidget(self.OutputMessagesAddedWidget)
        self.outpuMessagesOptionsLayout = QtWidgets.QHBoxLayout(self.outputMessagesOptions)
        self.addOutputMessagePushButton = QtWidgets.QPushButton(self.outputMessagesOptions)
        self.addOutputMessagePushButton.setObjectName("addOutputMessagePushButton")
        self.addOutputMessagePushButton.setStyleSheet("""
                                                background-color: #ffffff;
                                                """)
        self.addOutputMessagePushButton.setMinimumSize(QtCore.QSize(16777215,40))
        self.outpuMessagesOptionsLayout.addWidget(self.addOutputMessagePushButton)
        
        self.addEmptyOutputMessagePushButton = QtWidgets.QPushButton(self.outputMessagesOptions)
        self.addEmptyOutputMessagePushButton.setObjectName("addEmptyOutputMessagePushButton")
        self.addEmptyOutputMessagePushButton.setStyleSheet("""
                                                background-color: #ffffff;
                                                """)
        self.addEmptyOutputMessagePushButton.setMinimumSize(QtCore.QSize(16777215,40))
        self.outpuMessagesOptionsLayout.addWidget(self.addEmptyOutputMessagePushButton)
        
        self.addGuiOutputMessagePushButton = QtWidgets.QPushButton(self.outputMessagesOptions)
        self.addGuiOutputMessagePushButton.setObjectName("addGuiOutputMessagePushButton")
        self.addGuiOutputMessagePushButton.setStyleSheet("""
                                                background-color: #ffffff;
                                                """)
        self.addGuiOutputMessagePushButton.setMinimumSize(QtCore.QSize(16777215,40))
        self.outpuMessagesOptionsLayout.addWidget(self.addGuiOutputMessagePushButton)
        
        self.addImagePushButton = QtWidgets.QPushButton(self.outputMessagesOptions)
        self.addImagePushButton.setObjectName("addImagePushButton")
        self.addImagePushButton.setStyleSheet("""
                                                background-color: #ffffff;
                                                """)
        self.addImagePushButton.setMinimumSize(QtCore.QSize(16777215,40))
        self.outpuMessagesOptionsLayout.addWidget(self.addImagePushButton)
        
        # self.SendAllOutputMessagePushButton = QtWidgets.QPushButton(self.outputMessagesOptions)
        # self.SendAllOutputMessagePushButton.setObjectName("SendAllOutputMessagePushButton")
        # self.SendAllOutputMessagePushButton.setStyleSheet("""
        #                                         background-color: #ffffff;
        #                                         """)
        # self.SendAllOutputMessagePushButton.setMinimumSize(QtCore.QSize(16777215,40))
        # self.outpuMessagesOptionsLayout.addWidget(self.SendAllOutputMessagePushButton)
        
        
        self.DeleteAllOutoutMessagePushButton = QtWidgets.QPushButton(self.outputMessagesOptions)
        self.DeleteAllOutoutMessagePushButton.setObjectName("DeleteAllOutoutMessagePushButton")
        self.DeleteAllOutoutMessagePushButton.setStyleSheet("""
                                                background-color: #ffffff;
                                                """)
        self.DeleteAllOutoutMessagePushButton.setMinimumSize(QtCore.QSize(16777215,40))
        self.outpuMessagesOptionsLayout.addWidget(self.DeleteAllOutoutMessagePushButton)
        
        self.selectAllOutputMessagePushButton = QtWidgets.QPushButton(self.outputMessagesOptions)
        self.selectAllOutputMessagePushButton.setObjectName("selectAllOutputMessagePushButton")
        self.selectAllOutputMessagePushButton.setStyleSheet("""
                                                background-color: #ffffff;
                                                """)
        self.selectAllOutputMessagePushButton.setMinimumSize(QtCore.QSize(16777215,40))
        self.outpuMessagesOptionsLayout.addWidget(self.selectAllOutputMessagePushButton)
        
        
        
        # save
        self.SaveOutputPushButton = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.SaveOutputPushButton.setObjectName("SaveOutputPushButton")
        self.SaveOutputPushButton.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.SaveOutputPushButton.setMinimumSize(QtCore.QSize(160, 30))
        self.outpuMessagesOptionsLayout.addWidget(self.SaveOutputPushButton)
        self.SaveOutputPushButton.hide()
        
        # cancel
        self.cancelOutputPushButton = QtWidgets.QPushButton(self.TestCasesAddedWidget)
        self.cancelOutputPushButton.setObjectName("cancelOutputPushButton")
        self.cancelOutputPushButton.setStyleSheet("""
                                                     background-color: #ffffff;
                                                     """)
        self.cancelOutputPushButton.setMinimumSize(QtCore.QSize(160, 30))
        self.outpuMessagesOptionsLayout.addWidget(self.cancelOutputPushButton)
        self.cancelOutputPushButton.hide()
        
        self.gridLayout_OutputMessagesAddedWidget.addWidget(self.outputMessagesOptions, 1, 0, 1, 1)
        
        self.newOutputMessagesListWidget = SafeListWidget()
        self.newOutputMessagesListWidget.setStyleSheet("""
                                                    border: 0px;
                                                """)
        self.newOutputMessagesListWidget.setObjectName("newOutputMessagesListWidget")
        self.gridLayout_OutputMessagesAddedWidget.addWidget(self.newOutputMessagesListWidget, 2, 0, 1, 1)
        
        self.gridLayout_outputMessagePageSNS.addWidget(self.OutputMessagesAddedWidget, 2, 0, 1, 1)
        self.stackedWidgetSNS.addWidget(self.outputMessagePageSNS)
        
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        
        
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        # Page RESULTS Details
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        self.resultsPageSNS = QtWidgets.QWidget()
        self.resultsPageSNS.setObjectName("resultsPageSNS")
        self.gridLayout_resultsPageSNS = QtWidgets.QGridLayout(self.resultsPageSNS)
        self.gridLayout_resultsPageSNS.setObjectName("gridLayout_resultsPageSNS")
        
        # >> Nav links
        self.snsNavTabResult = QtWidgets.QWidget(self.projectPageSNS)
        self.snsNavTabResult.setMaximumSize(QtCore.QSize(16777215, 100))
        self.snsNavTabResult.setObjectName("snsNavTabResult")
        self.gridLayout_snsNavTabResult = QtWidgets.QGridLayout(self.snsNavTabResult)
        self.gridLayout_snsNavTabResult.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_snsNavTabResult.setObjectName("gridLayout_snsNavTabResult")  
    
        
        
        self.resultPage_back = backButton()

        self.gridLayout_snsNavTabResult.addWidget(self.resultPage_back, 0, 1, 1, 10, Qt.AlignLeft)
        
        
        self.cancelProcessPushButton = QtWidgets.QPushButton(self.snsNavTabResult)
        self.cancelProcessPushButton.setMinimumSize(QtCore.QSize(150, 16777215))
        self.cancelProcessPushButton.setObjectName("cancelProcessPushButton")
        self.cancelProcessPushButton.setStyleSheet("""
                                                    background-color: #eeeeee;
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.cancelProcessPushButton.setText("Stop Process")
        self.gridLayout_snsNavTabResult.addWidget(self.cancelProcessPushButton, 0, 10, 1, 1, Qt.AlignRight)
        
        self.gridLayout_resultsPageSNS.addWidget(self.snsNavTabResult, 0, 0, 1, 1)
        
        self.snsOutput = SaveSendOutput()
        
        self.gridLayout_resultsPageSNS.addWidget(self.snsOutput, 1, 0, 1, 1)
        self.stackedWidgetSNS.addWidget(self.resultsPageSNS)
        
        
        
        
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        # Page Periodic Details
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=
        self.periodicPageSNS = QtWidgets.QWidget()
        self.periodicPageSNS.setObjectName("periodicPageSNS")
        self.gridLayout_periodicPageSNS = QtWidgets.QGridLayout(self.periodicPageSNS)
        self.gridLayout_periodicPageSNS.setObjectName("gridLayout_periodicPageSNS")
        
        # >> Nav links
        self.snsNavTabPeriodic = QtWidgets.QWidget(self.projectPageSNS)
        self.snsNavTabPeriodic.setMaximumSize(QtCore.QSize(16777215, 100))
        self.snsNavTabPeriodic.setObjectName("snsNavTabPeriodic")
        self.gridLayout_snsNavTabPeriodic = QtWidgets.QGridLayout(self.snsNavTabPeriodic)
        self.gridLayout_snsNavTabPeriodic.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_snsNavTabPeriodic.setObjectName("gridLayout_snsNavTabPeriodic")  
        
        self.periodicPageSNSBack = QtWidgets.QPushButton(self.snsNavTabPeriodic)
        self.periodicPageSNSBack.setMinimumSize(QtCore.QSize(150, 16777215))
        self.periodicPageSNSBack.setObjectName("resultPage_TestCase_link")
        self.periodicPageSNSBack.setStyleSheet("""
                                                    background-color: #eeeeee;
                                                    border: 1px solid #eeeeee;
                                                    font-size: 10px;
                                                    font-weight: bold;
                                                    padding: 5px 0px;
                                                    """)
        self.periodicPageSNSBack.setText("BACK")
        self.gridLayout_snsNavTabPeriodic.addWidget(self.periodicPageSNSBack, 0, 1, 1, 10, Qt.AlignLeft)
        
        self.gridLayout_periodicPageSNS.addWidget(self.snsNavTabPeriodic, 0, 0, 1, 1)
        
        # PLEASE REFER THIS COMENTEDCLASS FOR ADDING NEW WIDGET INSIDE THIS STACK PAGE
        self.snsPeriodics = saveSendPeriodic()
        self.gridLayout_periodicPageSNS.addWidget(self.snsPeriodics, 1, 0, 1, 1)
        
        
        self.stackedWidgetSNS.addWidget(self.periodicPageSNS)
        
        
        
        # Stack pages creations Done Above
 
        self.addIcons()

        self.gridLayout_mainWidgetSNSTab.addWidget(self.stackedWidgetSNS, 0, 0, 1, 1)
        self.setLayout(self.gridLayout_mainWidgetSNSTab)
        
        self.retranslateUi()
        
        # +++++++++++++++++++++++++++++++++ preconditions Widget +++++++++++++++++++++++++++++++
        
        # TO BE IMPLEMENTED
        self.preconditionsWidget = preconditionsWidget(self.projectPageSNS)
        self.preconditionsWidget.setWindowModality(Qt.ApplicationModal)
        self.preconditionsWidget.hide()
        
        # +++++++++++++++++++++++++++++++++ back varibles ++++++++++++++++++++++++++++++++++++++
        
        self.back_queue = deque(maxlen=20)
        self.isBack = False
        
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        self.stackedWidgetSNS.currentChanged.connect(self.onStackedPageChanged)
        self.back_queue.appendleft("p0")
        self.fileOps = fileOperations()
        
        
        # ++++++++++++++++++++++++ dyanamic sending thread +++++++++++++++++++++++++++++++++++++++++
        # create thread + worker setup
        self.thread = QThread()
        self.dynamic_sender_obj = Dynamic_Sender()
        self.dynamic_sender_obj.moveToThread(self.thread)
        
        # connect signals to SNS
        self.dynamic_sender_obj.gui_check_signal.connect(self.user_confirmation_gui)
        self.dynamic_sender_obj.test_result_signal.connect(self.SendOutputToResultGUI)
        self.dynamic_sender_obj.error_signal.connect(self.displayError)
      
        # clean up when finish
        # self.dynamic_sender_obj.all_done_signal.connect(self.thread.quit)
        # self.dynamic_sender_obj.all_done_signal.connect(self.dynamic_sender_obj.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        
        # Signals to trigger the task inside thread
        self.start_sending_Functions_signal.connect(self.dynamic_sender_obj.send_test_suite)
        self.start_sending_testCase_signal.connect(self.dynamic_sender_obj.send_test_case)
        
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
        
        self.newFunction = addItemsWidget(self.projectPageSNS, "Function")
        self.newFunction.hide()
        self.newFunction.setWindowModality(Qt.ApplicationModal)
        self.newProject = addItemsWidget(self.projectPageSNS, "Project")
        self.newProject.hide()
        self.newProject.setWindowModality(Qt.ApplicationModal)
        self.newTestCase = addItemsWidget(self.TestCasePageSNS, "Test_case")
        self.newTestCase.hide()
        self.newTestCase.setWindowModality(Qt.ApplicationModal)
        

        
        
        self.defaultStyleSheet()
        self.signalEvents()
        
        self.currentMessageData = {}
        self.TestCaseList = []
        self.functionList = []
    
        
        # CopyPaste Data
        self.copyData = copyData()
        self.isCopying = False

    





    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.openProjectPushButton.setText(_translate("MainWindow", "Open Test Plan"))
        self.projectNameLabel.setText(_translate("MainWindow", "Click open to open new project..."))
        self.newProjectPushButton.setText(_translate("MainWindow", "New Test Plan"))
        self.functionSendSelectedPushButton.setText(_translate("MainWindow", "SEND SELECTED"))
        self.functionDeleteSelectedPushButton.setText(_translate("MainWindow", "Delete SELECTED"))
        self.functionAddPushButton.setText(_translate("MainWindow", "Add New Test Suite"))
        self.functionSelectAllPushButton.setText(_translate("MainWindow", "Select All"))
        self.functionSavePushButton.setText(_translate("MainWindow", "SAVE"))
        self.functionCancelPushButton.setText(_translate("MainWindow", "CANCEL"))

        # self.enterTestCaseNameLineEdit.setPlaceholderText(_translate("MainWindow", "Enter new Test Case name"))
        self.addTestCasePushButton.setText(_translate("MainWindow", "Add Test Case"))
        self.addTestCaseSendAll.setText(_translate("MainWindow", "Send Selected"))
        self.addTestCaseDeleteAll.setText(_translate("MainWindow", "Delete Selected"))
        self.addTestCaseCopySelected.setText(_translate("MainWindow", "Copy Selected"))
        self.addTestCasePasteSelected.setText(_translate("MainWindow", "Paste"))
        self.addTestCaseSelectAll.setText(_translate("MainWindow", "Select All"))
        self.testCaseSavePushButton.setText(_translate("MainWindow", "SAVE"))
        self.testCaseCancelPushButton.setText(_translate("MainWindow", "CANCEL"))

        # self.functionTitleLabel.setText(_translate("MainWindow", "No Function selected"))
        
        self.addMessagePushButton.setText(_translate("MainWindow", "Add Input Message"))
        self.addEmptyMessagePushButton.setText(_translate("MainWindow", "Add Empty Input Message"))
        self.addGuiInputMessagePushButton.setText(_translate("MainWindow", "Add Manual Input from GUI"))
        # self.SendAllTestCasesPushButton.setText(_translate("MainWindow", "Send Selected Message"))
        self.deleteAllInputPushButton.setText(_translate("MainWindow", "Delete Selected Message"))
        self.selectAllInputPushButton.setText(_translate("MainWindow", "Select All"))
        self.SaveInputPushButton.setText(_translate("MainWindow", "SAVE"))
        self.cancelInputPushButton.setText(_translate("MainWindow", "CANCEL"))
        
        self.addOutputMessagePushButton.setText(_translate("MainWindow", "Add Output Message"))
        self.addEmptyOutputMessagePushButton.setText(_translate("MainWindow", "Add Empty Output Message"))
        self.addGuiOutputMessagePushButton.setText(_translate("MainWindow", "Add Manual user check from GUI"))
        self.addImagePushButton.setText(_translate("MainWindow", "Add Expected Screenshot"))
        # self.SendAllOutputMessagePushButton.setText(_translate("MainWindow", "Send Selected"))
        self.DeleteAllOutoutMessagePushButton.setText(_translate("MainWindow", "Delete Selected"))
        self.selectAllOutputMessagePushButton.setText(_translate("MainWindow", "Select All"))
        self.SaveOutputPushButton.setText(_translate("MainWindow", "SAVE"))
        self.cancelOutputPushButton.setText(_translate("MainWindow", "CANCEL"))
    
    
    def addIcons(self):
        DBUG.printWhere()
        # Open
        ui_ops.setSVG(self.openProjectPushButton, "icons/actions/folder-open.svg", 20, 20)
        
        # New project
        ui_ops.setSVG(self.newProjectPushButton, "icons/actions/folder-new.svg", 20, 20)
        
        # ADD
        ui_ops.setSVG(self.functionAddPushButton, "icons/actions/list-add.svg", 20, 20)
        ui_ops.setSVG(self.addTestCasePushButton, "icons/actions/list-add.svg", 20, 20)
        ui_ops.setSVG(self.addMessagePushButton, "icons/actions/list-add.svg", 20, 20)
        ui_ops.setSVG(self.addEmptyMessagePushButton, "icons/actions/list-add.svg", 20, 20)
        ui_ops.setSVG(self.addGuiInputMessagePushButton, "icons/actions/list-add.svg", 20, 20)
        ui_ops.setSVG(self.addOutputMessagePushButton, "icons/actions/list-add.svg", 20, 20)
        ui_ops.setSVG(self.addEmptyOutputMessagePushButton, "icons/actions/list-add.svg", 20, 20)
        ui_ops.setSVG(self.addGuiOutputMessagePushButton, "icons/actions/list-add.svg", 20, 20)
        ui_ops.setSVG(self.addImagePushButton, "icons/actions/image.svg", 20, 20)

        # SELECT
        ui_ops.setSVG(self.functionSelectAllPushButton, "icons/actions/dialog-ok.svg", 20, 20)
        ui_ops.setSVG(self.addTestCaseSelectAll, "icons/actions/dialog-ok.svg", 20, 20)
        ui_ops.setSVG(self.selectAllInputPushButton, "icons/actions/dialog-ok.svg", 20, 20)
        ui_ops.setSVG(self.selectAllOutputMessagePushButton, "icons/actions/dialog-ok.svg", 20, 20) 
        
        # Send
        ui_ops.setSVG(self.functionSendSelectedPushButton, "icons/actions/mail-forward.svg", 20, 20)
        ui_ops.setSVG(self.addTestCaseSendAll, "icons/actions/mail-forward.svg", 20, 20)
    
        # Delete
        ui_ops.setSVG(self.functionDeleteSelectedPushButton, "icons/places/user-trash.svg", 20, 20)
        ui_ops.setSVG(self.addTestCaseDeleteAll, "icons/places/user-trash.svg", 20, 20)
        ui_ops.setSVG(self.deleteAllInputPushButton, "icons/places/user-trash.svg", 20, 20)
        ui_ops.setSVG(self.DeleteAllOutoutMessagePushButton, "icons/places/user-trash.svg", 20, 20)
        
        # COPY
        ui_ops.setSVG(self.addTestCaseCopySelected, "icons/actions/copy.svg", 20, 20)

        # Paste
        ui_ops.setSVG(self.addTestCasePasteSelected, "icons/actions/edit-paste.svg", 20, 20)
        
        # settings icon in suite,testcase
        ui_ops.setSVG(self.settingsSNS, "icons/actions/settings.svg", 25, 25)
    
    def defaultStyleSheet(self):
        DBUG.printWhere()
        # Function
        self.functionLabelWidgetSNS.setStyleSheet(f"""
                                                  background-color: {GREY_300};
                                                  """)
        self.functionLabelWidgetSNS.setFixedHeight(35)
        self.title_functionView.setStyleSheet(f"""
                                              font-size: 15px;
                                              font-weight: bold;
                                              color: #212121;
                                              """)
        self.HLayout_functionLabelWidgetSNS.setContentsMargins(20, 0, 20, 0)
        self.verticalLayout_projectContentWidgetSNS.setContentsMargins(0, 0, 0, 0)
    
        
        # Project Section
        self.projectLabelWidgetSNS.setStyleSheet(f"""
                                                  background-color: {GREY_300};
                                                  """)
        self.projectLabelWidgetSNS.setFixedHeight(35)
        self.title_projectView.setStyleSheet(f"""
                                              font-size: 15px;
                                              font-weight: bold;
                                              color: #212121;
                                              """)
        self.VLayout_ProjectLabelWidgetSNS.setContentsMargins(20, 0, 20, 0)
        self.gridLayout_newProjectWidgetSNS.setContentsMargins(0, 0, 0, 0)
        
        
        
        # Test Case section
        self.TestCaseLabelWidgetSNS.setStyleSheet(f"""
                                                  background-color: {GREY_300};
                                                  """)
        self.TestCaseLabelWidgetSNS.setFixedHeight(35)
        self.title_TestCasewView.setStyleSheet(f"""
                                              font-size: 15px;
                                              font-weight: bold;
                                              color: #212121;
                                              """)
        self.VLayout_TestCaseLabelWidgetSNS.setContentsMargins(20, 0, 20, 0)
        self.gridLayout_TestCasesAddedWidget.setContentsMargins(0, 0, 0, 0)
        
        
        # Input message section
        self.inputMessagesLabelWidgetSNS.setStyleSheet(f"""
                                                  background-color: {GREY_300};
                                                  """)
        self.inputMessagesLabelWidgetSNS.setFixedHeight(35)
        self.title_InputMessagesView.setStyleSheet(f"""
                                              font-size: 15px;
                                              font-weight: bold;
                                              color: #212121;
                                              """)
        self.VLayout_inputMessagesLabelWidgetSNS.setContentsMargins(20, 0, 20, 0)
        self.gridLayout_messagesAddedWidget.setContentsMargins(0, 0, 0, 0)
        
        # Output message section
        self.outputMessagesLabelWidgetSNS.setStyleSheet(f"""
                                                  background-color: {GREY_300};
                                                  """)
        self.outputMessagesLabelWidgetSNS.setFixedHeight(35)
        self.title_outputMessagesView.setStyleSheet(f"""
                                              font-size: 15px;
                                              font-weight: bold;
                                              color: #212121;
                                              """)
        self.VLayout_outputMessagesLabelWidgetSNS.setContentsMargins(20, 0, 20, 0)
        self.gridLayout_OutputMessagesAddedWidget.setContentsMargins(0, 0, 0, 0)

    
    
        
    def signalEvents(self):
        DBUG.printWhere()
        #mahaiyo
        self.snsPeriodics.periodic_message_selector_signal.connect(self.periodic_sender_signal)
        
        self.result_Switch_link.clicked.connect(lambda:self.switchPage(4))
        self.result_Switch_test_case_link.clicked.connect(lambda:self.switchPage(4))
        
        self.percondition_periodic_Switch_link.clicked.connect(lambda:self.switchPage(5))
        
        # self.projectPage_project_link.clicked.connect(lambda:self.switchPage(0))
        # self.functionPage_project_link.clicked.connect(lambda:self.switchPage(0))
        # self.functionPage_function_link.clicked.connect(lambda:self.switchPage(1))
        # self.TCPage_project_link.clicked.connect(lambda:self.switchPage(0))
        # self.TCPage_function_link.clicked.connect(lambda:self.switchPage(1))
        # self.TCPage_TC_link.clicked.connect(lambda:self.switchPage(2))
        # self.outputPage_project_link.clicked.connect(lambda:self.switchPage(0))
        # self.outputPage_TestCase_link.clicked.connect(lambda:self.switchPage(1))
        # self.outputPage_InputMessage_link.clicked.connect(lambda:self.switchPage(2))
        # self.outputPage_OutputMessage_link.clicked.connect(lambda:self.switchPage(3))
        self.resultPage_back.back_clicked_signal.connect(self.processBack)
        self.periodicPageSNSBack.clicked.connect(lambda: self.switchPage(0))
        
       
        
        self.newProjectPushButton.clicked.connect(self.createNewProjectClicked)
        self.openProjectPushButton.clicked.connect(self.openProject)
        self.functionAddPushButton.clicked.connect(self.createNewFunction)
        self.functionSendSelectedPushButton.clicked.connect(lambda:self.ListSelectedFunctions("SEND"))
        self.functionDeleteSelectedPushButton.clicked.connect(lambda:self.ListSelectedFunctions("DELETE"))
        self.functionSelectAllPushButton.clicked.connect(lambda:self.toggleCheckBoxes(self.funtionTestCasesListWidgetSNS, self.functionSelectAllPushButton.text().upper()))
        self.functionSavePushButton.clicked.connect(self.functionDragDrop)
        self.functionCancelPushButton.clicked.connect(self.cancelFunctionDragDrop)
        
        self.addTestCasePushButton.clicked.connect(self.createNewTestCase)
        self.addTestCaseSendAll.clicked.connect(lambda:self.ListSelectedTestCases("SEND"))
        self.addTestCaseDeleteAll.clicked.connect(lambda:self.ListSelectedTestCases("DELETE"))
        self.addTestCaseSelectAll.clicked.connect(lambda:self.toggleCheckBoxes(self.newTestCasesListWidget, self.addTestCaseSelectAll.text().upper() ))
        self.testCaseSavePushButton.clicked.connect(self.testCaseDragDrop)
        self.testCaseCancelPushButton.clicked.connect(self.cancelTestcaseDragDrop)


        self.addMessagePushButton.clicked.connect(lambda:self.switchTab(1, "input"))
        self.addEmptyMessagePushButton.clicked.connect(lambda:self.setEmptyData("INPUT","SAVE",-1))
        self.addGuiInputMessagePushButton.clicked.connect(lambda:self.setGuiCheckInput("SAVE"))
        self.selectAllInputPushButton.clicked.connect(lambda:self.toggleCheckBoxes(self.newMessagesListWidget, self.selectAllInputPushButton.text().upper()))
        self.deleteAllInputPushButton.clicked.connect(lambda:self.ListSelectedMessages("DELETE"))
        self.SaveInputPushButton.clicked.connect(self.inputDragDrop)
        self.cancelInputPushButton.clicked.connect(self.cancelInputMessageDragDrop)
        
        
        self.addOutputMessagePushButton.clicked.connect(lambda:self.switchTab(1, "output"))
        self.addEmptyOutputMessagePushButton.clicked.connect(lambda:self.setEmptyData("OUTPUT","SAVE",-1))
        self.addGuiOutputMessagePushButton.clicked.connect(lambda:self.setGuiCheck("SAVE"))
        self.addImagePushButton.clicked.connect(lambda:self.addOutputGUIImage("OUTPUT", "SAVE", -1))
        self.DeleteAllOutoutMessagePushButton.clicked.connect(lambda:self.ListSelectedOutputMessages("DELETE"))
        self.selectAllOutputMessagePushButton.clicked.connect(lambda:self.toggleCheckBoxes(self.newOutputMessagesListWidget, self.selectAllOutputMessagePushButton.text().upper()))
        self.SaveOutputPushButton.clicked.connect(self.outputDragDrop)
        self.cancelOutputPushButton.clicked.connect(self.cancelOutputMessageDragDrop)
       
        
       
        self.newProject.update_settings_signal.connect(self.addNewProject)
        self.newFunction.update_settings_signal.connect(self.saveFunction)
        self.newTestCase.update_settings_signal.connect(lambda testCaseName:self.saveTestCaseinFile(testCaseName, True))
        self.fileOps.finishedDeleteFunctionSignal.connect(lambda remove_item:self.DeleteSelectedDataUI(remove_item, "FUNCTION"))
        self.fileOps.finishedDeleteTestCaseSignal.connect(lambda remove_item:self.DeleteSelectedDataUI(remove_item, "TESTCASE"))
        self.fileOps.finishedDeleteMessageSignal.connect(lambda remove_item:self.DeleteSelectedDataUI(remove_item, "MESSAGE"))
        self.fileOps.finishedDeleteOutputMessageSignal.connect(lambda remove_item:self.DeleteSelectedDataUI(remove_item, "OUTPUT_MESSAGE"))
        self.fileOps.finishedCopyTestCaseSignal.connect(self.finishedCopy)
        
        
        # DRAG DROP
        self.funtionTestCasesListWidgetSNS.dragDroppedItemSignal.connect(lambda: self.dragDropOps("FUNCTION"))
        self.newTestCasesListWidget.dragDroppedItemSignal.connect(lambda: self.dragDropOps("TESTCASE"))
        self.newMessagesListWidget.dragDroppedItemSignal.connect(lambda: self.dragDropOps("INPUTMESSAGE"))
        self.newOutputMessagesListWidget.dragDroppedItemSignal.connect(lambda: self.dragDropOps("OUTPUTMESSAGE"))
        
        # COPY PASTE SIGNALS - Testcase
        self.addTestCaseCopySelected.clicked.connect(lambda:self.ListSelectedTestCases("COPY"))
        self.addTestCasePasteSelected.clicked.connect(self.PasteCopiedData)
        
        # Back
        self.projectPage_back.back_clicked_signal.connect(self.processBack)
        self.testCasePage_back.back_clicked_signal.connect(self.processBack)
        self.inputMessagePage_back.back_clicked_signal.connect(self.processBack)
        self.outputMessagePage_back.back_clicked_signal.connect(self.processBack)
        
        # Cancel
        self.cancelProcessPushButton.clicked.connect(self.stopSNSSendingProcess)
        
        # items clicked events inside list widgets
        self.funtionTestCasesListWidgetSNS.itemClicked.connect(lambda item: self.onListWidgetItemClicked(item, "FUNCTION"))
        self.newTestCasesListWidget.itemClicked.connect(lambda item: self.onListWidgetItemClicked(item, "TESTCASE"))
        self.newMessagesListWidget.itemClicked.connect(lambda item: self.onListWidgetItemClicked(item, "INPUTMESSAGE"))
        self.newOutputMessagesListWidget.itemClicked.connect(lambda item: self.onListWidgetItemClicked(item, "OUTPUTMESSAGE"))
        
        # Preconditions for test cases signals
        self.preconditionsWidget.precondtions_updated_signal.connect(self.savePreconditions)

    

 
    ########## menu options ##############
    
    def setIPPort(self):
        dialog_title = "Set IP/PORT"
        dialog_field1 = "IP"
        dialog_field2 = "Port"
        dialog = twoInputDialog(dialog_title,dialog_field1,dialog_field2, config.sock_send_ip, config.sock_send_port, self.projectPageSNS)
        dialog.setWindowModality(Qt.ApplicationModal)

        if dialog.exec_() == QDialog.Accepted: 
            config.sock_send_ip, config.sock_send_port = dialog.getInputs()
            self.ip_port_changed_signal.emit()
        else:
            return
                    
    def setDefaultDelay(self):
        value, ok = QtWidgets.QInputDialog.getInt(None,"Default Delay", "Enter Default Delay value:", 0)
        if ok:
            delay = value
            self.default_delay_set_signal.emit(delay)
        else:
            pass
        
    def setDefaultPeriodic(self):
        value, ok = QtWidgets.QInputDialog.getInt(None,"Default Periodic", "Enter Default Periodic value:", 0)
        if ok:
            periodic = value
            self.default_periodic_set_signal.emit(periodic)
        else:
            pass        
        
    
    def displayError(self, error_str):
        errorDisplay.show(self.stackedWidgetSNS, error_str)
    
    #mahaiyo
    def periodic_sender_signal(self, index, funcType, fromPage, isback):
        self.switch_add_periodic_tab.emit(index, funcType, fromPage, isback)



    def stopSNSSendingProcess(self):
        DBUG.printWhere()
        self.dynamic_sender_obj.stop_sending_signal.emit()
    
    def onStackedPageChanged(self, index):
        DBUG.printWhere()
        print("Page changed to page: ", index)
        if not(self.isBack):
            print("NOt back operation hence added to back queue")
            self.back_queue.appendleft(f"p{index}")
        print("Switch page: back_queue: ", self.back_queue)

    # send data to the result page
    def SendOutputToResultGUI(self, functionName, testCaseName,status, received_output, expected_output):
        DBUG.printWhere()
        print("TIMES RESULT SIGNAL CALLED")
        print("Result outputs: ",functionName, testCaseName,status, received_output, expected_output)
        self.snsOutput.test_result_SNS_output_signal.emit(functionName, testCaseName,status, received_output, expected_output)
    
        
    def processBack(self):
        DBUG.printWhere()
        print(">>>>>>>>>>>>>>",self.back_queue) 
            
        if len(self.back_queue)>1:
            self.back_queue.popleft()
            currentPageIdx = self.back_queue[0]
            
            if currentPageIdx[0]=="p":
                self.switchPage(int(currentPageIdx[1]), True)
            
            if currentPageIdx[0]=="t":
                self.switchTab(int(currentPageIdx[1]), 'input',True)
        else:        
            print("Cannot go back , last page")
          
    
    # def switchToResultPage(self):
    #     DBUG.printWhere()
    #     self.switchPage(4)

        
    # def switchPreviousPageFromResults(self):
    #     DBUG.printWhere()
    #     if self.resultPage_TestCase_link.text() == "Functions":
    #         self.switchPage(0)

    #     elif self.resultPage_TestCase_link.text() == "Test Cases":
    #         self.switchPage(1)

    #     else:
    #         print("unknown page")

    def switchTab(self, index, fromPage, isback=False):
        DBUG.printWhere()
        print("from page = ", fromPage)
         
        if isback:
            self.switch_tab_signal.emit(index, "save", fromPage, True)
        else:
            # self.back_queue.appendleft("t2")
            print(">>>>>>>>>>>>>>",self.back_queue)
            self.switch_tab_signal.emit(index, "save", fromPage, False)
            
    
    def switchPage(self, index, isback=False):
        DBUG.printWhere()
        
        # Reset copy paste data when page changed
        self.copyData = copyData()
        self.addTestCasePasteSelected.setText("Paste")
        
        if isback:
            self.isBack = True
        else:
            self.isBack = False
            
        print(">>>>>>>>>>>>>>",self.back_queue)   
        self.stackedWidgetSNS.setCurrentIndex(index)
       
    def insertDataInbetweenCSV(self,indexTop, indexBottom, df, new_row):
        DBUG.printWhere()
        df_top = df.iloc[:indexTop+1]
        print(df_top.tail())
        
        df_bottom = df.iloc[indexBottom:]
        print(df_bottom.head())
        df = pd.concat([df_top, new_row, df_bottom], ignore_index=True)
        return df
    
    def insertDataEndCSV(self, df, new_row):
        DBUG.printWhere()
        df = pd.concat([df, new_row], ignore_index=True)
        return df
    
    def disconnectAndClearListWidget(self, rcvListWidget):
        DBUG.printWhere()
        for i in range(rcvListWidget.count()):    
            item = rcvListWidget.takeItem(i)
            widget = rcvListWidget.itemWidget(item)
            if widget:
                try:
                    widget.open_clicked_signal.disconnect()
                    DBUG.printDebug(f"Disconnected signals for widget {i}")
                except TypeError:
                    pass
                widget.setParent(None)
                widget.deleteLater()
            del item 
                
                
    def writeIndexLabel(self, ListWidget):
        DBUG.printWhere()
        DBUG.printDebug("write index")
        for i in range(ListWidget.count()):
            itemW = ListWidget.item(i)
            customWidget = ListWidget.itemWidget(itemW)
            customWidget.updateIndex(i+1)
            

    
    def setGuiCheckInput(self, saveEdit):
        DBUG.printWhere()
        print("input addd clicked")

        if saveEdit == "SAVE":
            output_string = ""
            Delay = 0
            dialog_title = "GUI INPUTS"
            dialog_field1 = "GUI action"
            dialog_field2 = "Delay"
            dialog = twoInputDialog(dialog_title,dialog_field1,dialog_field2)
            if dialog.exec_() == QDialog.Accepted: 
                output_string, Delay = dialog.getInputs()
            else:
                return
            
            output_string = "GUI_INPUT: "+ output_string
            
            output_data = mainWindow_SNS_save_edit_data("INPUT", saveEdit, -1, output_string , "", "", "", "", 0, Delay)
            self.currentMessageData = output_data
            self.processMessageData()
        
    def setGuiCheck(self, saveEdit):
        DBUG.printWhere()
        if saveEdit == "SAVE":
            output_string = ""
            value, ok = QtWidgets.QInputDialog.getText(None,"USER CONFIRMATION", "Please Enter What to Check on GUI?")
            if ok:
                value = value.strip()
                if value=="":
                    QMessageBox().information(self.projectPageSNS, "Empty Value", "Field cannot be empty", QMessageBox().Ok)
                    return
            
                output_string = "GUI_CHECK: "+value
            else:
                return
            
            output_data = mainWindow_SNS_save_edit_data("OUTPUT", saveEdit, -1, output_string , "", "", "", "", 0, 10000000)
            self.currentMessageData = output_data
            self.processOutputMessageData()
        
        
    def setEmptyData(self, fromPage, saveEdit, messageIdentifier):
        DBUG.printWhere()
        if fromPage == "INPUT":
            if saveEdit == "SAVE":
                value, ok = QtWidgets.QInputDialog.getInt(None,"Set Delay", "Enter Delay value:")
                if ok:
                    delay = value
                else:
                    return
                input_data = mainWindow_SNS_save_edit_data(fromPage, saveEdit, messageIdentifier, "INPUT NOT REQUIRED", "", "", "", "", 0, delay)
                self.currentMessageData = input_data
                self.processMessageData()
                
        if fromPage == "OUTPUT":
            if saveEdit == "SAVE":
                output_data = mainWindow_SNS_save_edit_data(fromPage, saveEdit, messageIdentifier, "NO OUTPUT REQUIRED", "", "", "", "", 0, 0)
                self.currentMessageData = output_data
                self.processOutputMessageData()
    
    def setData(self,save_data):
        DBUG.printWhere()
        DBUG.printDebug(save_data)
        DBUG.printInfo(self.df.head(6))
        
        self.currentMessageData  = save_data
        
        if self.currentMessageData.input_or_output == "INPUT":
            self.processMessageData()
            # print("######>>>>>>>>>>>>>>",self.back_queue)
            # self.back_queue.popleft()
            # print("######>>>>>>>>>>>>>>",self.back_queue)
            
        if self.currentMessageData.input_or_output == "OUTPUT":
            self.processOutputMessageData()
            # self.back_queue.popleft()
            # print("######>>>>>>>>>>>>>>",self.back_queue)
        return True        
            
    def toggleCheckBoxes(self, list_Widget, changeStateTo):
        DBUG.printWhere()
        DBUG.printInfo(changeStateTo)
        if changeStateTo == "SELECT ALL":
            isSelected = False
        if changeStateTo == "DESELECT ALL":
            isSelected = True
            
        for i in range(list_Widget.count()):
            itemW = list_Widget.item(i)
            customWidget = list_Widget.itemWidget(itemW)
            customWidget.toggleCheckBox(isSelected)
        
        if changeStateTo == "SELECT ALL":
            self.sender().setText("DESELECT ALL")
        if changeStateTo == "DESELECT ALL":
            self.sender().setText("SELECT ALL")
        
    
    # Send clicked functions
    #1 Project page   
    def SendSelectedFunctionClicked(self):
        DBUG.printWhere()
        # self.switchToResultPage("function")
        self.switchPage(4)
        QtWidgets.QApplication.processEvents()
        
        os.makedirs("RESULTS", exist_ok=True)
        file_path = os.path.join("RESULTS", f"{self.currentSNSProject}_result.csv")
        header = ["Function Name", "Test case Name", "Status", "Recieved output", "Expected output"]
        with open(file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(header)
        
        print("send function clicked", self.currentSNSProject, self.functionList )
        
        self.start_sending_Functions_signal.emit(self.currentSNSProject, self.functionList)
        #self.dynamic_sender_obj.send_test_suite(self.currentSNSProject, self.functionList)
         


    
    #2 Test CASE  
    def SendSelectedTestCaseClicked(self, TestCaseList):
        DBUG.printWhere()
        # self.switchToResultPage("testcase")
        self.switchPage(4)
        os.makedirs("RESULTS", exist_ok=True)
        file_path = os.path.join("RESULTS", f"{self.currentSNSProject}_result.csv")
        header = ["Function Name", "Test case Name", "Status", "Recieved output", "Expected output"]
        with open(file_path, "w") as file:
            writer = csv.writer(file)
            writer.writerow(header)
        file.close()
        
        self.start_sending_testCase_signal.emit(self.currentSNSProject, TestCaseList , self.currentSNSFunction)
        #self.dynamic_sender_obj.send_test_case(self.currentSNSProject, self.TestCaseList , self.currentSNSFunction)
        

        
        
    #3 Messages
    def SendSingleMessage(self, messageName):
        DBUG.printWhere()
        DBUG.printDebug("Sending Message.... ", messageName, self.currentSNSFunction, self.currentSNSTestCase)
        
    def SendSelectedMessages(self, messageIdenitiferList):
        DBUG.printWhere()
        DBUG.printDebug("Sending Message List......", messageIdenitiferList, self.currentSNSFunction, self.currentSNSTestCase)
    

    #  GUI dialog
    def user_confirmation_gui(self, confirm_data):
        DBUG.printWhere()
        print("CONFIRM GUI CALLED")
        QuestionReply = QMessageBox().question(self.projectPageSNS, "GUI USER CONFIRMAITION REQUIRED",confirm_data, QMessageBox.Yes | QMessageBox().No)
        if QuestionReply == QMessageBox.Yes:
            self.dynamic_sender_obj.gui_check_response_signal.emit(1)

        elif QuestionReply == QMessageBox.No:
            self.dynamic_sender_obj.gui_check_response_signal.emit(0)
        # print("CONFIRM GUI CALLED")
        # QuestionReply = confirmDialog("GUI USER CONFIRMAITION REQUIRED", confirm_data)
        # QuestionReply.show()
        # if QuestionReply == QMessageBox.Yes:
        #     self.dynamic_sender_obj.gui_check_response_signal.emit(1)

        # elif QuestionReply == QMessageBox.No:
        #     self.dynamic_sender_obj.gui_check_response_signal.emit(0)
 


##########################################################################################################################
################################################### DragDrop Button Show/hide ############################################
##########################################################################################################################
    
    def functionMenuShow(self):
        self.functionSelectAllPushButton.show()
        self.functionDeleteSelectedPushButton.show()
        self.functionSendSelectedPushButton.show()
        self.functionAddPushButton.show()
        
        
        self.functionSavePushButton.setEnabled(False)
        self.functionSavePushButton.hide()
        self.functionCancelPushButton.setEnabled(False)
        self.functionCancelPushButton.hide()
        
    def functionDragDropMenuShow(self):
        self.functionSelectAllPushButton.hide()
        self.functionDeleteSelectedPushButton.hide()
        self.functionSendSelectedPushButton.hide()
        self.functionAddPushButton.hide()
        
        
        self.functionSavePushButton.setEnabled(True)
        self.functionSavePushButton.show()
        self.functionCancelPushButton.setEnabled(True)
        self.functionCancelPushButton.show()


    def testCaseMenuShow(self):
        self.addTestCasePushButton.show()
        self.addTestCaseSendAll.show()
        self.addTestCaseDeleteAll.show()
        self.addTestCaseCopySelected.show()
        self.addTestCasePasteSelected.show()
        self.addTestCaseSelectAll.show()
        
        self.testCaseSavePushButton.setEnabled(False)
        self.testCaseSavePushButton.hide()
        self.testCaseCancelPushButton.setEnabled(False)
        self.testCaseCancelPushButton.hide()
        
    def testCaseDragDropMenuShow(self):
        self.addTestCasePushButton.hide()
        self.addTestCaseSendAll.hide()
        self.addTestCaseCopySelected.hide()
        self.addTestCasePasteSelected.hide()
        self.addTestCaseDeleteAll.hide()
        self.addTestCaseSelectAll.hide()
        
        self.testCaseSavePushButton.show()
        self.testCaseSavePushButton.setEnabled(True)
        self.testCaseCancelPushButton.show()
        self.testCaseCancelPushButton.setEnabled(True)

    def inputMenuShow(self):
        self.addMessagePushButton.show()
        self.addEmptyMessagePushButton.show()
        self.addGuiInputMessagePushButton.show()
        self.deleteAllInputPushButton.show()
        self.selectAllInputPushButton.show()
        
        self.SaveInputPushButton.setEnabled(False)
        self.SaveInputPushButton.hide()
        self.cancelInputPushButton.setEnabled(False)
        self.cancelInputPushButton.hide()
        
    def inputDragDropMenuShow(self):
        self.addMessagePushButton.hide()
        self.addEmptyMessagePushButton.hide()
        self.addGuiInputMessagePushButton.hide()
        self.selectAllInputPushButton.hide()
        self.deleteAllInputPushButton.hide()
        
        self.SaveInputPushButton.show()
        self.SaveInputPushButton.setEnabled(True)
        self.cancelInputPushButton.show()
        self.cancelInputPushButton.setEnabled(True)
    
    def outputMenuShow(self):
        self.addOutputMessagePushButton.show()
        self.addEmptyOutputMessagePushButton.show()
        self.addGuiOutputMessagePushButton.show()
        self.addImagePushButton.show()
        self.DeleteAllOutoutMessagePushButton.show()
        self.selectAllOutputMessagePushButton.show()
        
        self.SaveOutputPushButton.hide()
        self.SaveOutputPushButton.setEnabled(False)
        self.cancelOutputPushButton.hide()
        self.cancelOutputPushButton.setEnabled(False)
        
        
    def outputDragDropMenuShow(self):
        self.addOutputMessagePushButton.hide()
        self.addEmptyOutputMessagePushButton.hide()
        self.addGuiOutputMessagePushButton.hide()
        self.addImagePushButton.hide()
        self.DeleteAllOutoutMessagePushButton.hide()
        self.selectAllOutputMessagePushButton.hide()
        
        self.SaveOutputPushButton.show()
        self.SaveOutputPushButton.setEnabled(True)
        self.cancelOutputPushButton.show()
        self.cancelOutputPushButton.setEnabled(True)

##########################################################################################################################
################################################### Drag Drop ############################################################
##########################################################################################################################

    
    def dragDropOps(self, fromPage):
        DBUG.printWhere()

        if fromPage == "FUNCTION":
            self.functionDragDropMenuShow()
            
        if fromPage == "TESTCASE":
            self.testCaseDragDropMenuShow()

        if fromPage == "INPUTMESSAGE":
            self.inputDragDropMenuShow()

        if fromPage == "OUTPUTMESSAGE":
            self.outputDragDropMenuShow()


    def functionDragDrop(self):
        # create dialog
        self.savingDisplayWidget = savingDialog("DRAG DROP", "Please Wait!!  Saving changes.....", self.projectPageSNS)
        self.savingDisplayWidget.setWindowModality(Qt.ApplicationModal)
        self.savingDisplayWidget.show()
        self.saveFunctionDragDrop()

        
    def saveFunctionDragDrop(self): 
        # get sequence order
        functionList = []
        for i in range(self.funtionTestCasesListWidgetSNS.count()):
            itemW = self.funtionTestCasesListWidgetSNS.item(i)
            customWidget = self.funtionTestCasesListWidgetSNS.itemWidget(itemW)
            functionList.append(customWidget.getLabelName())
        
        # reorder sqeuence list in df 
        function_indexes = {}
        currFunct = ""
        for index, row in self.df.iterrows():
            # print(index, row["Function_Name"])
            if not pd.isna(row["Function_Name"]):
                if index>0:
                    # print(row["Function_Name"])
                    function_indexes[currFunct].append(index)
                    
                function_indexes[row["Function_Name"]] = [index]
                currFunct = row["Function_Name"]
        function_indexes[currFunct].append(index+1)
        # print("HASHIGN OF FUNCTIONS", function_indexes)    
                
        
        rearranged_df = self.df.head(0).copy()
        for items in functionList:
            rows_to_copy = self.df.iloc[function_indexes[items][0]:function_indexes[items][1]].copy()
            rearranged_df = pd.concat([rearranged_df, rows_to_copy], ignore_index=True)
        
        
        self.df = rearranged_df.copy()
        
        # write to file
        self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
        print("DONE")
        
        
        # reindex
        self.savingDisplayWidget.updateLabel("Changes Saved Successfully!!")
        
        self.writeIndexLabel(self.funtionTestCasesListWidgetSNS)
        
        self.functionMenuShow()
        
    def cancelFunctionDragDrop(self):
        self.funtionTestCasesListWidgetSNS.clear()
        self.newTestCasesListWidget.clear()
        self.newMessagesListWidget.clear()
        self.newOutputMessagesListWidget.clear()
                
        for index, row in self.df.iterrows():
            if not pd.isna(row["Function_Name"]):            
                self.addFunctionInListwidget(row["Function_Name"])

        self.functionMenuShow()
       
        
    #TEST CASE
    def testCaseDragDrop(self):
        self.testcaseDisplayWidget = savingDialog("DRAG DROP", "Please Wait!!  Saving changes.....", self.projectPageSNS)
        self.testcaseDisplayWidget.setWindowModality(Qt.ApplicationModal)
        self.testcaseDisplayWidget.show()
        self.saveTestcaseDragDrop()

    def saveTestcaseDragDrop(self): 
        # get sequence order
        testCaseList = []
        for i in range(self.newTestCasesListWidget.count()):
            itemW = self.newTestCasesListWidget.item(i)
            customWidget = self.newTestCasesListWidget.itemWidget(itemW)
            testCaseList.append(customWidget.getLabelName())
            
        # reorder sqeuence list in df 
        testcase_indexes = {}
        currTC = ""
        functionFound = False
        splitDFtopIndex = -1
        splitDFendIndex = -1
        for index, row in self.df.iterrows():
            if row["Function_Name"] == self.currentSNSFunction:
                functionFound = True
                splitDFtopIndex = index
                continue
            
            if functionFound == True and not(pd.isna(row["Function_Name"])):
                testcase_indexes[currTC].append(index)
                functionFound = False
                splitDFendIndex = index
                break
            

            
            if functionFound == True:
                if not(pd.isna(row["Test_Case"])):
                    if currTC == "": 
                        testcase_indexes[row["Test_Case"]] = [index]
                        currTC = row["Test_Case"]
                    else:
                        testcase_indexes[currTC].append(index)
                        testcase_indexes[row["Test_Case"]] = [index]
                        currTC = row["Test_Case"]
                        
                    if(index == len(self.df)-1):
                        testcase_indexes[currTC].append(index+1)
                        splitDFendIndex = index+1
                
                elif(index == len(self.df)-1):
                    testcase_indexes[currTC].append(index+1)
                    splitDFendIndex = index+1
                
                
                        
                    
        print("HASHIGN OF TESTCASES", testcase_indexes)    
                
        
        rearranged_df = self.df.head(0).copy()
        for items in testCaseList:
            rows_to_copy = self.df.iloc[testcase_indexes[items][0]:testcase_indexes[items][1]].copy()
            rearranged_df = pd.concat([rearranged_df, rows_to_copy], ignore_index=True)
        
        self.df_top = self.df[:splitDFtopIndex+1].copy()
        self.df_bottom = self.df[splitDFendIndex:].copy()
        self.df = pd.concat([self.df_top, rearranged_df, self.df_bottom], ignore_index=True)
        self.writeIndexLabel(self.newTestCasesListWidget)
        
        # write to file
        self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
        
        
        # reindex
        self.testcaseDisplayWidget.updateLabel("Changes Saved Successfully!!")
        
        self.writeIndexLabel(self.newTestCasesListWidget)
        
        self.testCaseMenuShow()
        
        
   
    def cancelTestcaseDragDrop(self):
        self.newTestCasesListWidget.clear()
        self.newMessagesListWidget.clear()
        self.newOutputMessagesListWidget.clear()
        
        self.loadPrevTestCases(self.currentSNSFunction)
        
        self.testCaseMenuShow()
        

    # INPUT 
    def inputDragDrop(self):
        
        self.inputDisplayWidget = savingDialog("DRAG DROP", "Please Wait!!  Saving changes.....", self.projectPageSNS)
        self.inputDisplayWidget.setWindowModality(Qt.ApplicationModal)
        self.inputDisplayWidget.show()
        self.saveInputMessageDragDrop()
    
    def saveInputMessageDragDrop(self):  
        # get sequence order
        inputMessageList = []
        for i in range(self.newMessagesListWidget.count()):
            itemW = self.newMessagesListWidget.item(i)
            customWidget = self.newMessagesListWidget.itemWidget(itemW)
            inputMessageList.append(int(customWidget.objectName()))
            
        # # reorder sqeuence list in df 
        inputMessage_indexes = {}
        currINP = ""
        functionFound = False
        splitDFtopIndex = -1
        splitDFendIndex = -1
        
        startF = False
        startTC = False
        for index, rows in self.df.iterrows():
            # DBUG.printDebug(f'{index} {rows["Function_Name"]} {rows["Test_Case"]} {rows["Message"]} {len(self.df)}')
            if (rows["Function_Name"] == self.currentSNSFunction):
                # DBUG.printDebug(f"fuction found {self.currentSNSFunction}")
                startF = True
                continue
             
            if startF == True and rows["Test_Case"] == self.currentSNSTestCase:
                # DBUG.printDebug(f"Test CASE found {self.currentSNSTestCase}")
                splitDFtopIndex = index
                startTC = True
                continue
            
            
            if startTC == True:
                if pd.isna(rows["Test_Case"]) and pd.isna(rows["Function_Name"]): 
                    if (not(pd.isna(rows["Msg_Identifier"]))):
                        if currINP=="":
                            inputMessage_indexes[int(rows["Msg_Identifier"])] = [index]
                            currINP = int(rows["Msg_Identifier"])
                        else:
                            inputMessage_indexes[currINP].append(index)
                            inputMessage_indexes[int(rows["Msg_Identifier"])] = [index]
                            currINP = int(rows["Msg_Identifier"])

                    else:
                        pass
                    
                    if index == len(self.df)-1:
                        inputMessage_indexes[currINP].append(index+1)
                        splitDFendIndex = index+1
                        
                else:
                    startF = False
                    startTC = False
                    inputMessage_indexes[currINP].append(index)
                    splitDFendIndex = index
                    break
                    
  
                
                        
                    
        print("HASHIGN OF INPUT_MESSAGES", inputMessage_indexes)    
        print("inputMessageList", inputMessageList)      
        
        rearranged_df = self.df.head(0).copy()
        for items in inputMessageList:
            rows_to_copy = self.df.iloc[inputMessage_indexes[items][0]:inputMessage_indexes[items][1]].copy()
            rearranged_df = pd.concat([rearranged_df, rows_to_copy], ignore_index=True)
        
        self.df_top = self.df[:splitDFtopIndex+1].copy()
        self.df_bottom = self.df[splitDFendIndex:].copy()
        self.df = pd.concat([self.df_top, rearranged_df, self.df_bottom], ignore_index=True)

        
        # write to file
        self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
        
        
        # reindex
        self.inputDisplayWidget.updateLabel("Changes Saved Successfully!!")
        
        self.writeIndexLabel(self.newMessagesListWidget)
        
        self.inputMenuShow()

        
    def cancelInputMessageDragDrop(self):
        
        self.newMessagesListWidget.clear()
        self.newOutputMessagesListWidget.clear()
        
        self.loadPrevMessages()
        
        self.inputMenuShow()
    
    
    # OUTPUT 
    def outputDragDrop(self):
        self.outputDisplayWidget = savingDialog("DRAG DROP", "Please Wait!!  Saving changes.....", self.projectPageSNS)
        self.outputDisplayWidget.setWindowModality(Qt.ApplicationModal)
        self.outputDisplayWidget.show()
        self.saveOutputMessageDragDrop()
    
    def saveOutputMessageDragDrop(self): 
        
        # get sequence order
        outputMessageList = []
        for i in range(self.newOutputMessagesListWidget.count()):
            itemW = self.newOutputMessagesListWidget.item(i)
            customWidget = self.newOutputMessagesListWidget.itemWidget(itemW)
            outputMessageList.append(int(customWidget.objectName()))
            
        # # reorder sqeuence list in df 
        outputMessage_indexes = {}
        currOut = ""
        functionFound = False
        splitDFtopIndex = -1
        splitDFendIndex = -1
        
        startF = False
        startTC = False
        startInput = False
        
        for index, rows in self.df.iterrows():
            # DBUG.printDebug(f'{index} {rows["Function_Name"]} {rows["Test_Case"]} {rows["Message"]} {len(self.df)}')
            if (rows["Function_Name"] == self.currentSNSFunction):
                # DBUG.printDebug(f"fuction found {self.currentSNSFunction}")
                startF = True
                continue
             
            if startF == True and rows["Test_Case"] == self.currentSNSTestCase:
                # DBUG.printDebug(f"Test CASE found {self.currentSNSTestCase}")
                startTC = True
                continue
            
            if startTC == True and rows["Msg_Identifier"] == self.currentSNSInputMessageID:
                startInput = True
                splitDFtopIndex = index
                continue
             
            
            if startInput == True:
                if pd.isna(rows["Test_Case"]) and pd.isna(rows["Function_Name"]) and pd.isna(rows["Msg_Identifier"]): 
                    if (not(pd.isna(rows["expected_output_message_Identifier"]))):
                        if currOut=="":
                            outputMessage_indexes[int(rows["expected_output_message_Identifier"])] = [index]
                            currOut = int(rows["expected_output_message_Identifier"])
                        else:
                            outputMessage_indexes[currOut].append(index)
                            outputMessage_indexes[int(rows["expected_output_message_Identifier"])] = [index]
                            currOut = int(rows["expected_output_message_Identifier"])

                    else:
                        pass
                    
                    if index == len(self.df)-1:
                        outputMessage_indexes[currOut].append(index+1)
                        splitDFendIndex = index+1
                        
                else:
                    startF = False
                    startTC = False
                    outputMessage_indexes[currOut].append(index)
                    splitDFendIndex = index
                    break
                    
  
                
                        
                    
        print("HASHIGN OF OUPUT_MESSAGES", outputMessage_indexes) 
        print("Top: ",splitDFtopIndex,  " Bottom", splitDFendIndex)
                
        
        rearranged_df = self.df.head(0).copy()
        for items in outputMessageList:
            print(items, " ->>>slice>>>> ", outputMessage_indexes[items][0], outputMessage_indexes[items][1])
            rows_to_copy = self.df.iloc[outputMessage_indexes[items][0]:outputMessage_indexes[items][1]].copy()
            rearranged_df = pd.concat([rearranged_df, rows_to_copy], ignore_index=True)
        
        self.df_top = self.df[:splitDFtopIndex+1].copy()
        self.df_bottom = self.df[splitDFendIndex:].copy()
        self.df = pd.concat([self.df_top, rearranged_df, self.df_bottom], ignore_index=True)

        
        # write to file
        self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
        
        
        # reindex
        self.outputDisplayWidget.updateLabel("Changes Saved Successfully!!")
        
        self.writeIndexLabel(self.newOutputMessagesListWidget)

        self.outputMenuShow()
        
    def cancelOutputMessageDragDrop(self):
        self.newOutputMessagesListWidget.clear()
        
        self.loadPrevOutputMessages([self.currentSNSInputMessageID, self.currentSNSInputMessageName])
        
        self.outputMenuShow()

        
##########################################################################################################################
###################################### DELETE IN FILE ###################################################
##########################################################################################################################   

    #1 Function
    def DeleteSelectedFunction(self, functionList):
        DBUG.printWhere()
        DBUG.printDebug("Deleting Func List......", functionList)
        for func in functionList:
            delete_data = SNS_FileOperations_delete_data(self.df, self.currentSNSProject, func, "", "", -1)
            self.fileOps.deleteFunctionSignal.emit(delete_data)
        
    #2 Test CASE
    def DeleteSelectedTestCase(self, TestCasesList):
        DBUG.printWhere()
        DBUG.printDebug("Deleting TC List......", TestCasesList)
        DBUG.printDebug(self.df)
        for tc in TestCasesList:
            delete_data = SNS_FileOperations_delete_data(self.df, self.currentSNSProject, self.currentSNSFunction, tc, "", -1)
            self.fileOps.deleteTestCaseSignal.emit(delete_data)
        
    #3 Messages
    def DeleteSelectedMessages(self, messageIdenitiferList):
        DBUG.printWhere()
        DBUG.printDebug("Deleting Message List......", messageIdenitiferList)
        for msgIdentifier in messageIdenitiferList:
            delete_data = SNS_FileOperations_delete_data(self.df, self.currentSNSProject, self.currentSNSFunction, self.currentSNSTestCase, msgIdentifier, -1)
            self.fileOps.deleteMessageSignal.emit(delete_data)

    def DeleteSelectedOutputMessages(self, messageIdenitiferList):
        DBUG.printWhere()
        DBUG.printDebug("Deleting Output Message List......", messageIdenitiferList)
        for msgIdentifier in messageIdenitiferList:
            delete_data = SNS_FileOperations_delete_data(self.df, self.currentSNSProject, self.currentSNSFunction, self.currentSNSTestCase, self.currentSNSInputMessageID, msgIdentifier)
            self.fileOps.deleteOutputMessageSignal.emit(delete_data)
       
            
    # DELETE UI   
    def destroyedWidget(self):
        DBUG.printWhere()
        print("destroyed")
        
        
    def disconnect_signals(self, widget):
        DBUG.printWhere()
        for attr_name in dir(widget):
            attr =  getattr(widget, attr_name)
            if isinstance(attr, pyqtBoundSignal):
                try:
                    attr.disconnect()
                except TypeError:
                    pass
                
    def removeEleFromListWidget(self, list_Widget, remove_item):
        DBUG.printWhere()
        # DBUG.printDebug(self.df.head())
        for i in range(list_Widget.count()):
            itemW = list_Widget.item(i)
            customWidget = list_Widget.itemWidget(itemW)
            if customWidget and (customWidget.objectName() == str(remove_item)):  
                print("deleting widget related data: ", remove_item)                  
                self.disconnect_signals(customWidget)
                customWidget.setParent(None)
                list_Widget.removeItemWidget(itemW)
                customWidget.deleteLater()
                customWidget.destroyed.connect(self.destroyedWidget)
                list_Widget.takeItem(i)
                del itemW
                gc.collect()
            self.writeIndexLabel(list_Widget)
                
                
                
    def DeleteSelectedDataUI(self, remove_item, remove_what):
        DBUG.printWhere()
        DBUG.printDebug("remove",remove_item,remove_what)
        if remove_what == "FUNCTION":
            self.removeEleFromListWidget(self.funtionTestCasesListWidgetSNS, remove_item)
        if remove_what == "TESTCASE":
            self.removeEleFromListWidget(self.newTestCasesListWidget, remove_item)
        if remove_what == "MESSAGE":
            self.removeEleFromListWidget(self.newMessagesListWidget, remove_item)
        if remove_what == "OUTPUT_MESSAGE":
            self.removeEleFromListWidget(self.newOutputMessagesListWidget, remove_item)
    
    
    # ####################################### COPY PASTE ###########################################
    # Test Case
    def CopySelected(self, copyDataList, copiedFrom):
        DBUG.printWhere()
        print("data copying", copyDataList)
        self.copyData.location = copiedFrom
        self.copyData.dataList = copyDataList
        
        if self.copyData.location.lower() == "testcase" and len(self.copyData.dataList)>0: 
            self.addTestCasePasteSelected.setText(f"{toSuperScript(len(self.copyData.dataList))}  Paste")
      
        
    def PasteCopiedData(self):
        DBUG.printWhere()
        global COUNTER_INPUT, COUNTER_OUTPUT
        print("pasting ")
        if len(self.copyData.dataList)<=0:
            print("Nothing to paste")
            return
        
        if self.copyData.location.lower() == "testcase":
            if self.isCopying == True:
                print("still copying")
            else:  
                copyData = SNS_FileOperations_copy_data(self.df, self.currentSNSProject, self.currentSNSFunction, "", -1, -1, COUNTER_INPUT, COUNTER_OUTPUT, self.copyData.dataList)
                self.fileOps.copyTestCaseSignal.emit(copyData)
            
        
    def finishedCopy(self, cinp, cout, df, copyList):
        DBUG.printWhere()
        global COUNTER_INPUT, COUNTER_OUTPUT
        print("finished copy ", cinp, cout)
        COUNTER_INPUT = cinp
        COUNTER_OUTPUT = cout
        # print("#########################################################################")
        # print("Before",self.df)
        self.df = df.copy()
        # print("#########################################################################")
        # print("After",self.df)
        with open(f"{SNS_FOLDER}/counters.json", "r") as f:
            counterData = json.load(f)
        counterData[self.currentSNSProject][0] = COUNTER_INPUT
        counterData[self.currentSNSProject][1] = COUNTER_OUTPUT
        with open(f"{SNS_FOLDER}/counters.json", "w") as f:
            json.dump(counterData, f, indent=4)
        
        for data in copyList:
            self.addTestCasesWidgetFunction(data, False)
        print("complete copying")
        self.isCopying = False



    # ########################################## List widgets items clicked check/uncheck checkbox #################################################################################
    
    def onListWidgetItemClicked(self, item, whichListWidget):
        print("Clicked on item in list widget")
        if whichListWidget == "FUNCTION":
            widget = self.funtionTestCasesListWidgetSNS.itemWidget(item)
            widget.setUnsetCheckBox()
            
        if whichListWidget == "TESTCASE":
            widget = self.newTestCasesListWidget.itemWidget(item)
            widget.setUnsetCheckBox()

        if whichListWidget == "INPUTMESSAGE":
            widget = self.newMessagesListWidget.itemWidget(item)
            widget.setUnsetCheckBox()
            
        if whichListWidget == "OUTPUTMESSAGE":
            widget = self.newOutputMessagesListWidget.itemWidget(item)
            widget.setUnsetCheckBox()
            
            
            
            
    # ########################################## PROJECT #################################################################################
    def createNewProjectClicked(self):
        DBUG.printWhere()
        self.newProject.show()
      
    def addNewProject(self, projectName):
        DBUG.printWhere()
        global COUNTER_INPUT, COUNTER_OUTPUT, SNS_FOLDER
    
        if not os.path.exists(SNS_FOLDER):
            os.makedirs(SNS_FOLDER)
 
        if os.path.exists(SNS_FOLDER):  
            # Counter data
            if not os.path.exists(f"{SNS_FOLDER}/counters.json"):
                counterData = {
                    projectName: [COUNTER_INPUT, COUNTER_OUTPUT]
                    }
                with open(f"{SNS_FOLDER}/counters.json", "w") as f:
                    json.dump(counterData, f, indent=4)
            else:
                counterData = {}
                with open(f"{SNS_FOLDER}/counters.json", "r") as f:
                    counterData = json.load(f)
                    
                if projectName in counterData:
                    QuestionReply = QMessageBox().question(self.projectPageSNS, "Project data Already exists","Do you want to remove this project Data and create fresh one?", QMessageBox.Yes | QMessageBox().No)
                    if QuestionReply == QMessageBox.Yes:
                        counterData[projectName] = []
                        counterData[projectName].append(0)
                        counterData[projectName].append(0)
                    else:
                        QMessageBox().information(self.projectPageSNS, "Information", "Please choose different project Name", QMessageBox().Ok)
                        return
                else:
                    counterData[projectName] = []
                    counterData[projectName].append(0)
                    counterData[projectName].append(0)
                
                with open(f"{SNS_FOLDER}/counters.json", "w") as f:
                    json.dump(counterData, f, indent=4)
            
            # NEW Project file
            data = {
                "Function_Name": [],
                "Test_Case": [],
                "Preconditions": [],
                "Msg_Identifier": [],
                "Message": [],
                "Header_Data": [],
                "Input_Data": [],
                "Periodicity": [],
                "Delay": [],
                "Header_fromat":[],
                "content_format":[],
                "expected_output_message_Identifier": [],
                "expected_output_message": [],
                "output_header_data": [],
                "output_content_data": [],
                "output_header_format": [],
                "output_content_format": [],
                "output_periodicity": []
                }
            self.df = pd.DataFrame(data)
            
            self.df.to_csv(f"{SNS_FOLDER}/{projectName}.csv", index=False)
            DBUG.printDebug(projectName)
            self.funtionTestCasesListWidgetSNS.clear()
            self.newTestCasesListWidget.clear()
            self.newMessagesListWidget.clear()
            self.newOutputMessagesListWidget.clear()
            self.projectNameLabel.clear()
            COUNTER_INPUT = 0
            COUNTER_OUTPUT = 0
            self.projectNameLabel.setText(f"{projectName}.csv")
            self.currentSNSProject = projectName
            

            
            COUNTER_INPUT = counterData[projectName][0]
            COUNTER_OUTPUT = counterData[projectName][1]
                    
            QMessageBox().information(self.projectPageSNS, "Project Creattion Successful", "New Project Created in SAVENSEND folder", QMessageBox().Ok)
            
        
    def openProject(self):
        DBUG.printWhere()
        global COUNTER_INPUT, COUNTER_OUTPUT, SNS_FOLDER
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.newProjectWidgetSNS,"Open File", SNS_FOLDER, "All Files (*)")
        

        if file_path:
            with open(f"{SNS_FOLDER}/counters.json", "r") as f:
                counterData = json.load(f)
            
            project = file_path.split("/")[-1].split(".")[0]
            print("++++++++++++++++++++++",project)
            if project not in counterData:
                QMessageBox().critical(self.projectPageSNS, "Unknown project file", "This file is not created using this application, Ask developer how to include such files", QMessageBox().Ok)
            else:

                selected_sheet = file_path.split("/")[-1]
                self.projectNameLabel.setText(f"{selected_sheet}")
                
                self.currentSNSProject = self.projectNameLabel.text().split(".")[0]
                self.df = pd.read_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv")
                print("Open PRoject")
                # DBUG.printDebug(self.df.applymap(type))
    
                # DBUG.printDebug(self.df["Header_Data"][2], type(self.df["Header_Data"][2]))
                listStringToList(self.df)
                
                # da = self.df["Input_Data"][2]
                # print("->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", self.df["Input_Data"][2])
                # for i in da:
                #     print(i, " ====== ", type(i))
                
                # DBUG.printDebug(self.df["Header_Data"][2], type(self.df["Header_Data"][2]))
                # self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
                
                self.funtionTestCasesListWidgetSNS.clear()
                self.newTestCasesListWidget.clear()
                self.newMessagesListWidget.clear()
                self.newOutputMessagesListWidget.clear()
                
                for index, row in self.df.iterrows():
                    if not pd.isna(row["Function_Name"]):            
                        DBUG.printDebug(row["Function_Name"])
                        # self.functionComboBox.addItem(row["Function_Name"])
                        self.addFunctionInListwidget(row["Function_Name"])
                        
    
                    
                COUNTER_INPUT = counterData[self.currentSNSProject][0]
                COUNTER_OUTPUT = counterData[self.currentSNSProject][1]
           
        else:
            DBUG.printDebug("Please choose a csv file")
            QMessageBox().critical(self.projectPageSNS, "No file selected", "Please choose a Project CSV file", QMessageBox().Ok)


    # ###################################### FUNCTIONS #################################################################################
    def createNewFunction(self):
        DBUG.printWhere()
        if self.projectNameLabel.text() == "Click open to open new project...":
            QMessageBox().critical(self.projectPageSNS, "No file selected", "Please choose a Project CSV file", QMessageBox().Ok)
        else:
            self.newFunction.show()


    def saveFunction(self, functionName):
        isFunctionSaved = self.saveFunctionName(functionName, "SAVE")
        if not isFunctionSaved:
            QMessageBox().critical(self.projectPageSNS, "Duplicate Test Suite", f"'{functionName}' is already present", QMessageBox().Ok)
            return
        else:
            self.addFunctionInListwidget(functionName)

    def addFunctionInListwidget(self, functionName):
        DBUG.printWhere()  
        customFunctionItemWidget  = itemsLWFunctions(functionName, "function")
        customFunctionItemWidget.setObjectName(functionName)
        customFunctionItemWidget.open_clicked_signal.connect(self.OpenTestCasePage)
        customFunctionItemWidget.edit_clicked_signal.connect(self.editFunction)
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(customFunctionItemWidget.sizeHint())
        self.funtionTestCasesListWidgetSNS.addItem(item)
        self.funtionTestCasesListWidgetSNS.setItemWidget(item, customFunctionItemWidget)
        self.writeIndexLabel(self.funtionTestCasesListWidgetSNS)   
        
    def saveFunctionName(self, functionName, funcType, oldFunctionName=""):
        DBUG.printWhere()
        DBUG.printDebug("saving function name")
        
        
        if funcType == "SAVE":   
            new_row = pd.DataFrame([{"Function_Name": functionName}])
            if (self.df["Function_Name"] == functionName).any():
                print("FUnction already present>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                return False
            else:
                self.df = pd.concat([self.df, new_row], ignore_index=True)
                self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
                DBUG.printDebug("function append and save to csv")
                return True
        
        if funcType == "EDIT":
            print("Editing function")
            new_row = {"Function_Name": functionName}
            for index, rows in self.df.iterrows():
                if pd.isna(rows["Function_Name"]):
                    continue
                
                # print(rows["Function_Name"], oldFunctionName)
                if rows["Function_Name"] == oldFunctionName:
                    DBUG.printDebug(index, rows["Function_Name"])
                    insertIndex = index
                    print("Inserting data in csv at index", insertIndex)
                    self.df.loc[insertIndex] = new_row
                    self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
                    break
            
                
            
    def ListSelectedFunctions(self, options):
        DBUG.printWhere()
        
        self.functionList = []
        for i in range(self.funtionTestCasesListWidgetSNS.count()):
            itemW = self.funtionTestCasesListWidgetSNS.item(i)
            customWidget = self.funtionTestCasesListWidgetSNS.itemWidget(itemW)
            if customWidget.isCheckboxChecked():  
                self.functionList.append(customWidget.getLabelName())
                
        if options == "SEND":
            self.SendSelectedFunctionClicked()
        if options == "DELETE":
            QuestionReply = QMessageBox().question(self.projectPageSNS, "Confirm Delete","Are you sure you want to delete this item?", QMessageBox.Yes | QMessageBox().No)
            if QuestionReply == QMessageBox.Yes:
                self.DeleteSelectedFunction(self.functionList)

            elif QuestionReply == QMessageBox.No:
                return
             
        
            
        
    def editFunction(self, functionName):
        DBUG.printWhere()
        DBUG.printDebug("Sending Func.... ", functionName)
        
        value, ok = QtWidgets.QInputDialog.getText(None,"EDIT FUNCTION NAME", "Please edit the Function", text=functionName)
        if ok:
            value = value.strip()
            if value == "":
              QMessageBox().information(self.projectPageSNS, "Empty Value", "Field cannot be empty", QMessageBox().Ok)  
              return
          
            newfunctionName = value.strip()  
            self.saveFunctionName(newfunctionName, "EDIT", functionName)
            
            for i in range(self.funtionTestCasesListWidgetSNS.count()):
                item = self.funtionTestCasesListWidgetSNS.item(i)
                widget = self.funtionTestCasesListWidgetSNS.itemWidget(item)
                # print(widget.objectName())
                if widget.objectName() == str(functionName):
                    print("found")
                    widget.setObjectName(newfunctionName)
                    widget.updateLabel(newfunctionName)
                    break
                else:
                    pass
        else:
            return
        
        

    
    # ############################################ TEST CASES #################################################################################
    def OpenTestCasePage(self, functionName):
        DBUG.printWhere()
        DBUG.printDebug("##################### opening")
        self.currentSNSFunction = functionName
        self.newTestCasesListWidget.clear()
        self.disconnectAndClearListWidget(self.newTestCasesListWidget)
        # self.functionTitleLabel.setText(functionName)
        self.addTestCaseWidget.setFunctionName(self.currentSNSFunction)
        self.addTestCaseWidget.setTestCaseName(" Present Below ▼ ")
        self.addTestCaseWidget.setInputName("NA")
        self.addTestCaseWidget.setOutputName("NA")
        self.loadPrevTestCases(functionName)
        self.switchPage(1) 
        
        
        
    def loadPrevTestCases(self, functionName):
        DBUG.printWhere()
        
        DBUG.printDebug("loading test cases of function")
        DBUG.printDebug(self.df)
        # print(f"{self.newTestCasesListWidget.count()} self.newTestCasesListWidget")
        start = False
        for index, rows in self.df.iterrows():
            # print(functionName, "Start", start, rows["Function_Name"])
            if rows["Function_Name"]==functionName:
                start = True
                continue
                # print(rows["Test_Case"], start)     
            if start == True and pd.isna(rows["Function_Name"]) and not(pd.isna(rows["Test_Case"])):
                DBUG.printDebug(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {rows['Test_Case']}")
                self.addTestCasesWidgetFunction(rows["Test_Case"], False)
                
            if start == True and not(pd.isna(rows["Function_Name"])):
                break
        
    def createNewTestCase(self):
        DBUG.printWhere()
        self.newTestCase.show()
    
    def saveTestCaseinFile(self, testCaseName, isSave):
        if isSave:
            isSaved = self.saveTestCase(testCaseName, "SAVE")
            if not isSaved:
                QMessageBox().critical(self.projectPageSNS, "Duplicate Test Case", f"'{testCaseName}' is already present in Test Suite", QMessageBox().Ok)
            else:
                self.addTestCasesWidgetFunction(testCaseName, isSave)
    
    def addTestCasesWidgetFunction(self, testCaseName, isSave):
        DBUG.printWhere()
        customTestCaseItemWidget  = itemsLWTestCase(testCaseName, 'testcase')
        customTestCaseItemWidget.setObjectName(testCaseName)
        customTestCaseItemWidget.open_clicked_signal.connect(self.OpenMessagesPage)
        customTestCaseItemWidget.edit_clicked_signal.connect(self.editTestCase)
        customTestCaseItemWidget.preconditions_clicked_signal.connect(self.preconditionsClicked)
        item = QtWidgets.QListWidgetItem()
        item.setSizeHint(customTestCaseItemWidget.sizeHint())
        self.newTestCasesListWidget.addItem(item)
        self.newTestCasesListWidget.setItemWidget(item, customTestCaseItemWidget)
        self.writeIndexLabel(self.newTestCasesListWidget)


    def saveTestCase(self, newtestCaseName, funcType, oldTestCaseName=""):
        DBUG.printWhere()
        DBUG.printDebug("saving test case")
        
        # IF SAVE OPERATION
        if funcType == "SAVE":
            new_row = pd.DataFrame([{"Test_Case":newtestCaseName}])
            function_name = self.currentSNSFunction
            start = False
            insertIndex = -1
            for index, rows in self.df.iterrows():
                DBUG.printDebug(rows["Function_Name"], function_name)
                # FUNCTION FOUND
                if (rows["Function_Name"] == function_name):
                    start = True
                    DBUG.printDebug("start gets :", start)
                    continue
                # Checking inside function
                if start:
                    if (rows["Test_Case"] == newtestCaseName):
                        return False
                    
                    if (pd.isna(rows["Function_Name"])):
                        continue
                    else:
                        DBUG.printDebug("break index", index)
                        insertIndex = index
                        start = False
                        break
            DBUG.printDebug(insertIndex, start)  
            
            # IF the function is last function
            if start == True and insertIndex== -1:
                self.df = self.insertDataEndCSV(self.df,new_row)
            else:
                # IF function is not last function
                self.df = self.insertDataInbetweenCSV(insertIndex-1,insertIndex,self.df,new_row)
            DBUG.printDebug(self.df.head())
            self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
            return True


        if funcType == "EDIT":
            new_row = {"Test_Case":newtestCaseName}
            function_name = self.currentSNSFunction
            start = False
            insertIndex = -1
            for index, rows in self.df.iterrows():
                DBUG.printDebug(rows["Function_Name"], function_name)
                if (rows["Function_Name"] == function_name):
                    start = True
                    DBUG.printDebug("start gets :", start)
                    continue
                
                if start:
                    if (pd.isna(rows["Test_Case"])):
                        continue
                    elif rows["Test_Case"] == oldTestCaseName :
                        DBUG.printDebug("break index", index)
                        insertIndex = index
                        start = False
                        print("Inserting data in csv at index", insertIndex)
                        self.df.loc[insertIndex] = new_row
                        self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
                        break
            DBUG.printDebug(insertIndex, start)  
            

    def OpenMessagesPage(self, testCaseName):
        DBUG.printWhere()
        DBUG.printDebug("opening")
        self.currentSNSTestCase = testCaseName
        self.newMessagesListWidget.clear()
        self.disconnectAndClearListWidget(self.newMessagesListWidget)
        self.TestCaseNameInMessagePageWidget.setFunctionName(self.currentSNSFunction)
        self.TestCaseNameInMessagePageWidget.setTestCaseName(self.currentSNSTestCase)
        self.TestCaseNameInMessagePageWidget.setInputName(" Present Below ▼ ")
        self.TestCaseNameInMessagePageWidget.setOutputName("NA")
        # self.CurrentTCLabel.setText(f"{self.currentSNSFunction}  >  {testCaseName}")
        self.loadPrevMessages()
        self.switchPage(2)

    

                
    def ListSelectedTestCases(self, options):
        DBUG.printWhere()
        self.TestCaseList = []
        for i in range(self.newTestCasesListWidget.count()):
            itemW = self.newTestCasesListWidget.item(i)
            customWidget = self.newTestCasesListWidget.itemWidget(itemW)
            if customWidget.isCheckboxChecked():  
                self.TestCaseList.append(customWidget.getLabelName())
              
        if options == "SEND":
            self.SendSelectedTestCaseClicked(self.TestCaseList) 
        if options == "DELETE":
            QuestionReply = QMessageBox().question(self.projectPageSNS, "Confirm Delete","Are you sure you want to delete this item?", QMessageBox.Yes | QMessageBox().No)
            if QuestionReply == QMessageBox.Yes:
                self.DeleteSelectedTestCase(self.TestCaseList)
            elif QuestionReply == QMessageBox.No:
                return 
        if options == "COPY":
            self.CopySelected(self.TestCaseList, "testcase")
            

    def editTestCase(self, TestCaseName):
        DBUG.printWhere()
        DBUG.printDebug("Editing TC....", TestCaseName, self.currentSNSFunction)
        
        value, ok = QtWidgets.QInputDialog.getText(None,"EDIT TESTCASE NAME", "Please edit the Test case", text=TestCaseName)
        if ok:
            value = value.strip()
            if value == "":
              QMessageBox().information(self.projectPageSNS, "Empty Value", "Field cannot be empty", QMessageBox().Ok)  
              return
          
            newTestCaseName = value.strip()
            self.saveTestCase(newTestCaseName, "EDIT", TestCaseName)
            
            for i in range(self.newTestCasesListWidget.count()):
                item = self.newTestCasesListWidget.item(i)
                widget = self.newTestCasesListWidget.itemWidget(item)
                # print(widget.objectName())
                if widget.objectName() == str(TestCaseName):
                    print("found")
                    widget.setObjectName(newTestCaseName)
                    widget.updateLabel(newTestCaseName)
                    break
                else:
                    pass
            
        else:
            return


    def preconditionsClicked(self, testCaseName):
        print("Preconditions Opening")
        
        preconditionTestCaseList = []
        currentFunction = ""
        for index, rows in self.df.iterrows():
            if not pd.isna(rows["Function_Name"]):
                currentFunction = rows["Function_Name"]
                
            if not pd.isna(rows["Test_Case"]):
                preconditionTestCaseList.append(currentFunction+" --> "+rows["Test_Case"])
                
        isFunction = True
        alreadyAddedPreconditions = []
        for index, rows in self.df.iterrows():
            if (rows["Function_Name"] == self.currentSNSFunction):
                isFunction = True
            if isFunction and not(pd.isna(rows["Test_Case"])):

                print("check list")
                if rows["Test_Case"] == testCaseName:
                    # print("rows['Preconditions']  ",type(rows["Preconditions"]), " ", rows["Preconditions"])
                    if isinstance(rows["Preconditions"], list):
                        # print("list fonund", )
                        alreadyAddedPreconditions = rows["Preconditions"]
                        
                        
                        
                              
 
                    
                    
        self.preconditionsWidget.show()
        self.preconditionsWidget.run(self.currentSNSFunction, testCaseName, preconditionTestCaseList, alreadyAddedPreconditions)
    
    def savePreconditions(self, preconditions, suite, testcase):
        if len(preconditions)==0:
            preconditions=""
            
        new_row = {"Test_Case":testcase, "Preconditions": preconditions}
        function_name = suite
        start = False
        insertIndex = -1
        for index, rows in self.df.iterrows():
            DBUG.printDebug(rows["Function_Name"], function_name)
            if (rows["Function_Name"] == function_name):
                start = True
                DBUG.printDebug("start gets :", start)
                continue
            
            if start:
                if (pd.isna(rows["Test_Case"])):
                    continue
                elif rows["Test_Case"] == testcase :
                    DBUG.printDebug("break index", index)
                    insertIndex = index
                    start = False
                    print("Inserting data in csv at index", insertIndex)
                    self.df.loc[insertIndex] = new_row
                    self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
                    break
        DBUG.printDebug(insertIndex, start) 
    
    # ################################################ INPUT MESSSAGES #################################################################################
    def loadPrevMessages(self):
        DBUG.printWhere()

        startF = False
        startTC = False
        for index, rows in self.df.iterrows():
            DBUG.printDebug(f'{index} {rows["Function_Name"]} {rows["Test_Case"]} {rows["Message"]} {len(self.df)}')
            if (rows["Function_Name"] == self.currentSNSFunction):
                DBUG.printDebug(f"fuction found {self.currentSNSFunction}")
                startF = True
                continue
             
            if startF == True and rows["Test_Case"] == self.currentSNSTestCase:
                DBUG.printDebug(f"Test CASE found {self.currentSNSTestCase}")
                startTC = True
                continue
            if startF == True and not(pd.isna(rows["Function_Name"])):
                break  
            
            if startTC == True:
                if pd.isna(rows["Test_Case"]) and pd.isna(rows["Function_Name"]): 
                    if (not(pd.isna(rows["Message"]))):
                        DBUG.printDebug("Data Types Header and input data from the loadingfrom csv", type(rows["Header_Data"]),type(rows["Input_Data"]))
                        messageDetails = snsMessageDetails(int(rows["Msg_Identifier"]), rows["Message"], rows["Header_Data"], rows["Input_Data"], rows["Header_fromat"], rows["content_format"], int(rows["Periodicity"]), rows["Delay"])
                        DBUG.printDebug(messageDetails)
                        self.addMessageDetailsWidget(messageDetails, "SAVE")
                        DBUG.printInfo("Loaded Already present Messages from DF")
                    else:
                        pass
                else:
                    startF = False
                    startTC = False
                    break
        
        

    
    
    def processMessageData(self):
        DBUG.printWhere()
        if self.currentMessageData.save_or_edit == "SAVE":
            global COUNTER_INPUT
            self.writeMessageData("SAVE")
            self.DisplayMessageData("SAVE")
            
            COUNTER_INPUT = COUNTER_INPUT + 1
            
            with open(f"{SNS_FOLDER}/counters.json", "r") as f:
                counterData = json.load(f)
            counterData[self.currentSNSProject][0]= COUNTER_INPUT
            with open(f"{SNS_FOLDER}/counters.json", "w") as f:
                json.dump(counterData, f, indent=4)
            
        if self.currentMessageData.save_or_edit == "EDIT":
            self.writeMessageData("EDIT")
            self.DisplayMessageData("EDIT")
    
    
    def writeMessageData(self, data_type):
        DBUG.printWhere()
        if data_type == "SAVE":  
            DBUG.printDebug("saving new message Details")
            global COUNTER_INPUT
            
            new_row = pd.DataFrame([{
                                      "Msg_Identifier": COUNTER_INPUT,
                                      "Message":self.currentMessageData.Message_Name,
                                      "Header_Data":self.currentMessageData.header_data,
                                      "Input_Data":self.currentMessageData.content_data,
                                      "Periodicity":self.currentMessageData.periodicity,
                                      "Delay":self.currentMessageData.delay, 
                                      "Header_fromat":self.currentMessageData.Header_format,
                                      "content_format":self.currentMessageData.content_format
                                      }])
            
            startF = False
            startTC = False
            insertIndex = -1
            
            for index, rows in self.df.iterrows():
                # print(index, self.currentSNSFunction, self.currentSNSTestCase)
                DBUG.printDebug(index, rows["Function_Name"], rows["Test_Case"], rows["Message"], len(self.df))
                if (rows["Function_Name"] == self.currentSNSFunction):
                    DBUG.printDebug("fuction found", self.currentSNSFunction)
                    startF = True
                    continue
                 
                if startF == True and rows["Test_Case"] == self.currentSNSTestCase:
                    DBUG.printDebug("Test CASE found", self.currentSNSTestCase)
                    startTC = True
                    if index==len(self.df)-1:
                        insertIndex = index+1
                        startF = False
                        startTC = False
                        break
                    else:
                        continue
                
                if startTC == True:
                    DBUG.printDebug(pd.isna(rows["Test_Case"]), (not(pd.isna(rows["Message"]))))
            
                    if pd.isna(rows["Test_Case"]) and (not(pd.isna(rows["Message"]))):
                        DBUG.printDebug("Test case empty and input message field is present")
                        if index==len(self.df)-1:
                            DBUG.printDebug("Message present at end of file")
                            insertIndex = index+1
                            startF = False
                            startTC = False
                            break
                        else:
                            continue
                    elif pd.isna(rows["Test_Case"]) and not(pd.isna(rows["expected_output_message"])):
                        DBUG.printDebug("Test case empty and Expected output message is present")
                        if index==len(self.df)-1:
                            DBUG.printDebug("Message present at end of file")
                            insertIndex = index+1
                            startF = False
                            startTC = False
                            break
                        continue
                    else:
                        DBUG.printDebug("Others condtions not met")
                        insertIndex = index
                        startF = False
                        startTC = False
                        break
            
            
            DBUG.printDebug(insertIndex)
            # DBUG.printDebug(self.df.applymap(type))
            self.df = self.insertDataInbetweenCSV(insertIndex-1,insertIndex,self.df,new_row)
            self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
            

        
        
        elif self.currentMessageData.save_or_edit == "EDIT":
            DBUG.printDebug("saving Edited data")
            new_row = {
                        "Msg_Identifier": self.currentMessageData.messageIdenitifer,
                        "Message":self.currentMessageData.Message_Name,
                        "Header_Data":self.currentMessageData.header_data,
                        "Input_Data":self.currentMessageData.content_data,
                        "Periodicity":self.currentMessageData.periodicity,
                        "Delay":self.currentMessageData.delay,
                        "Header_fromat":self.currentMessageData.Header_format,
                        "content_format":self.currentMessageData.content_format
                        }

            DBUG.printDebug("------------------------------------------",self.currentMessageData)
            DBUG.printDebug("Current processing Message ID", self.currentMessageData.messageIdenitifer, type(self.currentMessageData.messageIdenitifer), type("rows['Msg_Identifier']"))
            for index, rows in self.df.iterrows():
                if pd.isna(rows["Msg_Identifier"]):
                    continue
                
                if int(rows["Msg_Identifier"]) == int(self.currentMessageData.messageIdenitifer):
                    DBUG.printDebug(index, rows["Msg_Identifier"], self.currentMessageData.messageIdenitifer)
                    insertIndex = index
                    # df.drop(insertIndex)
                    DBUG.printDebug("Inserting data in csv at index", insertIndex)
                    self.df.loc[insertIndex] = new_row
                    self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
                    break
            
            
    def DisplayMessageData(self, data_type):
        DBUG.printWhere()
        print("Displaying data")
        global COUNTER_INPUTCOUNTER_OUTPUT
        if data_type == "SAVE":
            messageDetails = snsMessageDetails(COUNTER_INPUT, self.currentMessageData.Message_Name, self.currentMessageData.Header_format,self.currentMessageData.content_format,"","",self.currentMessageData.periodicity,self.currentMessageData.delay)
            self.addMessageDetailsWidget(messageDetails, data_type)
        if data_type == "EDIT":
            messageDetails = snsMessageDetails(self.currentMessageData.messageIdenitifer, self.currentMessageData.Message_Name, self.currentMessageData.Header_format, self.currentMessageData.content_format, "", "", self.currentMessageData.periodicity, self.currentMessageData.delay)
            self.addMessageDetailsWidget(messageDetails, data_type)
            
            
    

    
    def addMessageDetailsWidget(self, messageDetails, data_type):
        DBUG.printWhere()
        
        if data_type == "SAVE":
            DBUG.printDebug("SAVE CONDITION")
            DBUG.printInfo(messageDetails)
            DBUG.printDebug("datatype", data_type )
            customMessageItemWidget  = LW_items_MessageDetails(messageDetails.messageIdenitifer, messageDetails.message, int(messageDetails.delay), int(messageDetails.periodicity))
            customMessageItemWidget.setObjectName(str(int(messageDetails.messageIdenitifer)))
            customMessageItemWidget.edit_MessageDetails_clicked_signal.connect(lambda msgIdentifier:self.EditMessage(msgIdentifier, "input"))
            customMessageItemWidget.add_output_clicked_signal.connect(self.openOutputMessage)
            item = QtWidgets.QListWidgetItem()
            item.setSizeHint(customMessageItemWidget.sizeHint())
            self.newMessagesListWidget.addItem(item)
            self.newMessagesListWidget.setItemWidget(item, customMessageItemWidget)
            self.writeIndexLabel(self.newMessagesListWidget)

        if data_type == "EDIT":
            DBUG.printDebug("EDIT CONDITION")
            for i in range(self.newMessagesListWidget.count()):
                item = self.newMessagesListWidget.item(i)
                widget = self.newMessagesListWidget.itemWidget(item)
                print(widget.objectName(), str(messageDetails.messageIdenitifer))
                if widget.objectName() == str(int(messageDetails.messageIdenitifer)):
                    print("found")
                    widget.setDelay(messageDetails.delay)
                    widget.setPeriodicity(messageDetails.periodicity)
                    widget.updateLabel(messageDetails.message)
                else:
                    pass
            
    def ListSelectedMessages(self, options):
        DBUG.printWhere()
        messageIdenitiferList = []
        for i in range(self.newMessagesListWidget.count()):
            itemW = self.newMessagesListWidget.item(i)
            customWidget = self.newMessagesListWidget.itemWidget(itemW)
            if customWidget.isCheckboxChecked():  
                messageIdenitiferList.append(int(customWidget.MessageId))
        
        if options == "SEND":
            self.SendSelectedMessages(messageIdenitiferList) 
        if options == "DELETE":
            QuestionReply = QMessageBox().question(self.projectPageSNS, "Confirm Delete","Are you sure you want to delete this item?", QMessageBox.Yes | QMessageBox().No)
            if QuestionReply == QMessageBox.Yes:
                self.DeleteSelectedMessages(messageIdenitiferList)
            elif QuestionReply == QMessageBox.No:
                return
            
    
    def EditMessage(self, messageId, fromPage):
        DBUG.printWhere()
        DBUG.printDebug("Editing the Input message with id", messageId)
        dff= self.df
        print("Editing the Input message with id", messageId)
        for i, rows in self.df.iterrows():
            if pd.isna(rows["Msg_Identifier"]):
                continue
            
            DBUG.printDebug(int(rows["Msg_Identifier"]),int(messageId))
            if int(rows["Msg_Identifier"]) == int(messageId):
                if rows["Message"] == "INPUT NOT REQUIRED":
                    messageDetails = snsMessageDetails(rows["Msg_Identifier"], rows["Message"], "", "", "", "", "", rows["Delay"])
                    self.editEmptyData(messageDetails)
                    pass
                elif "GUI_INPUT:" in rows["Message"]:
                    messageDetails = snsMessageDetails(rows["Msg_Identifier"], rows["Message"], "", "", "", "", 0, rows["Delay"])
                    self.editGuiInputData(messageDetails)
                else:
                    DBUG.printDebug("Message found in CSV")
                    messageDetails = snsMessageDetails(rows["Msg_Identifier"], rows["Message"], rows["Header_Data"], rows["Input_Data"], rows["Header_fromat"], rows["content_format"], rows["Periodicity"], rows["Delay"])
                    print("Edit messageCalled: before", messageDetails.InputData, messageDetails.message)
                    self.edit_message_sns_signal.emit(messageDetails, fromPage)
                    print("Edit messageCalled: after ", messageDetails.InputData, messageDetails.message)
                break
            # else:
            #     DBUG.printDebug("Message ID not found in data")


    def editGuiInputData(self, messageDetails):
        DBUG.printWhere()
        print("input addd clicked")
        output_string = messageDetails.message.split("GUI_INPUT:")[1].strip()
        Delay = 0
        dialog_title = "GUI INPUTS FROM USER"
        dialog_field1 = "GUI action"
        dialog_field2 = "Delay"
        dialog = twoInputDialog(dialog_title,dialog_field1,dialog_field2)
        dialog.setInputs(output_string, messageDetails.delay)
        if dialog.exec_() == QDialog.Accepted: 
            output_string, Delay = dialog.getInputs()
        else:
            return
        
        output_string = "GUI_INPUT: "+ output_string
        
        output_data = mainWindow_SNS_save_edit_data("INPUT", "EDIT", messageDetails.messageIdenitifer, output_string, "", "", "", "", 0, Delay)
        self.currentMessageData = output_data
        self.processMessageData()
        

        
    def editEmptyData(self, messageDetails):
        DBUG.printWhere()
        delay = messageDetails.delay
        value, ok = QtWidgets.QInputDialog.getInt(None,"Set Delay", "Enter Delay value:", int(messageDetails.delay))
        if ok:
            delay = value

        input_data = mainWindow_SNS_save_edit_data("INPUT", "EDIT", messageDetails.messageIdenitifer, messageDetails.message, "", "", "", "", 0, delay)
        self.currentMessageData = input_data
        self.processMessageData()
        

    # ############ OUTPUT MESSAGES #################################################################################
    def openOutputMessage(self, messageDetails):
        DBUG.printWhere()
        DBUG.printInfo("Opening Output message page, MSG ID: ", messageDetails[0], messageDetails[1])
        self.currentSNSInputMessageID = messageDetails[0]
        self.currentSNSInputMessageName = messageDetails[1]
        self.newOutputMessagesListWidget.clear()
        self.disconnectAndClearListWidget(self.newOutputMessagesListWidget)
        self.outputMessageNameInMessagePageWidget.setFunctionName(self.currentSNSFunction)
        self.outputMessageNameInMessagePageWidget.setTestCaseName(self.currentSNSTestCase)
        self.outputMessageNameInMessagePageWidget.setInputName(self.currentSNSInputMessageName)
        self.outputMessageNameInMessagePageWidget.setOutputName(" Present Below ▼ ")
        # self.CurrentOutputMessageLabel.setText(f"{self.currentSNSFunction}  >  {self.currentSNSTestCase} > {messageDetails[1]}")
        self.loadPrevOutputMessages(messageDetails)
        self.switchPage(3)

        
    def loadPrevOutputMessages(self, messageDetails):
        DBUG.printWhere()
        DBUG.printInfo(f"Adding Output messageID {messageDetails[0]} in GUI")
        # startF = False
        # startTC = False
        startINP = False
        for index, rows in self.df.iterrows():
            # DBUG.printDebug(f'{index} {rows["Function_Name"]} {rows["Test_Case"]} {rows["Message"]} {rows["expected_output_message_Identifier"]} {rows["expected_output_message"]}')
            if not(pd.isna(rows["Msg_Identifier"])):
                DBUG.printDebug("MessageID not null")
                if int(rows["Msg_Identifier"]) == int(messageDetails[0]):
                    DBUG.printDebug("message found in csv")
                    startINP = True
                    continue
                    
            if startINP == True and (not pd.isna(rows["Msg_Identifier"])):
                DBUG.printDebug("Next Input message found")
                startINP = False
                break
            
            if startINP == True and (not pd.isna(rows["expected_output_message_Identifier"])):
                DBUG.printDebug("Expected output data found")
                DBUG.printDebug(rows["expected_output_message_Identifier"], messageDetails[0], type(rows["expected_output_message_Identifier"]), type(messageDetails[0]))

                outputMessageDetails = snsOutputMessageDetails(rows["expected_output_message_Identifier"], rows["expected_output_message"], rows["output_header_data"], rows["output_content_data"], rows["output_header_format"], rows["output_content_format"], rows["output_periodicity"])
                self.addOutputMessageDetailsWidget(outputMessageDetails, "SAVE")
                
    
    def addOutputMessageDetailsWidget(self, messageDetails, data_type):
        DBUG.printWhere()
        
        if data_type == "SAVE":
            DBUG.printDebug("SAVE CONDITION")
            DBUG.printInfo(messageDetails)
            customOutputMessageItemWidget  = LW_items_Output_Message_widget(messageDetails.messageIdenitifer, messageDetails.message, int(messageDetails.periodicity))
            customOutputMessageItemWidget.setObjectName(str(int(messageDetails.messageIdenitifer)))
            customOutputMessageItemWidget.edit_MessageDetails_clicked_signal.connect(lambda msgIdentifier:self.EditOutputMessage(msgIdentifier, "output"))
            self.newOutputMessagesListWidget.add_Item(customOutputMessageItemWidget)
            self.writeIndexLabel(self.newOutputMessagesListWidget)

        if data_type == "EDIT":
            DBUG.printDebug("EDIT CONDITION")
            for i in range(self.newOutputMessagesListWidget.count()):
                item = self.newOutputMessagesListWidget.item(i)
                widget = self.newOutputMessagesListWidget.itemWidget(item)
                print(widget.objectName(), str(messageDetails.messageIdenitifer))
                if widget.objectName() == str(int(messageDetails.messageIdenitifer)):
                    print("found")
                    widget.setPeriodicity(messageDetails.periodicity)
                    widget.updateLabel(messageDetails.message)
                else:
                    pass
    

    
    def processOutputMessageData(self):
        DBUG.printWhere()
        if self.currentMessageData.save_or_edit == "SAVE":
            global COUNTER_OUTPUT
            self.writeOutputMessageData("SAVE")
            self.DisplayOutputMessageData("SAVE")
            
            COUNTER_OUTPUT=COUNTER_OUTPUT+1
            
            with open(f"{SNS_FOLDER}/counters.json", "r") as f:
                counterData = json.load(f)
            counterData[self.currentSNSProject][1] = COUNTER_OUTPUT
            with open(f"{SNS_FOLDER}/counters.json", "w") as f:
                json.dump(counterData, f, indent=4)
            
        if self.currentMessageData.save_or_edit == "EDIT":
            self.writeOutputMessageData("EDIT")
            self.DisplayOutputMessageData("EDIT")


    
    def writeOutputMessageData(self, data_type):
        DBUG.printWhere()
        if data_type == "SAVE":  
            DBUG.printDebug("saving new output message Details")
            global COUNTER_OUTPUT
            new_row = pd.DataFrame([{
                                        "expected_output_message_Identifier": COUNTER_OUTPUT,
                                        "expected_output_message": self.currentMessageData.Message_Name,
                                        "output_header_data": self.currentMessageData.header_data,
                                        "output_content_data": self.currentMessageData.content_data,
                                        "output_header_format": self.currentMessageData.Header_format,
                                        "output_content_format": self.currentMessageData.content_format,
                                        "output_periodicity": self.currentMessageData.periodicity
                                      }])
             
            
            startF = False
            startTC = False
            startINP = False
            insertIndex = -1
            for index, rows in self.df.iterrows():
                # print(index, self.currentSNSFunction, self.currentSNSTestCase)
                DBUG.printDebug(index, rows["Function_Name"], rows["Test_Case"], rows["Message"], len(self.df))
                if (rows["Function_Name"] == self.currentSNSFunction):
                    DBUG.printDebug("fuction found", self.currentSNSFunction)
                    startF = True
                    continue
                 
                if startF == True and rows["Test_Case"] == self.currentSNSTestCase:
                    DBUG.printDebug("Test CASE found", self.currentSNSTestCase)
                    startTC = True
                    continue
                
                if startTC == True and (rows["Msg_Identifier"] == self.currentSNSInputMessageID):
                    startINP = True
                    if index==len(self.df)-1:
                        print("Breaking 1")
                        insertIndex = index+1
                        startF = False
                        startTC = False
                        startINP = False
                        break
                    else:
                        continue
                
                if startINP == True:
                    DBUG.printDebug("INPUT MESSAGE FOUND and index is: ", index , pd.isna(rows["Message"]), (not(pd.isna(rows["expected_output_message"]))))
                    
                    if pd.isna(rows["expected_output_message"]):
                        DBUG.printDebug("Setting index after input message found: ", index)
                        insertIndex = index
                        print("Break")
                        startF = False
                        startTC = False
                        startINP = False
                        break
                    else:
                        if index==len(self.df)-1:
                            print("Breaking 2", len(self.df)-1, index)
                            insertIndex = index+1
                            startF = False
                            startTC = False
                            startINP = False
                            break

                    
                   
            
            
            DBUG.printDebug(insertIndex)
            self.df = self.insertDataInbetweenCSV(insertIndex-1,insertIndex,self.df,new_row)
            self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
            
        
        
        elif self.currentMessageData.save_or_edit == "EDIT":
            DBUG.printDebug("saving Edited data")
            new_row = {
                        "expected_output_message_Identifier": self.currentMessageData.messageIdenitifer,
                        "expected_output_message": self.currentMessageData.Message_Name,
                        "output_header_data": self.currentMessageData.header_data,
                        "output_content_data": self.currentMessageData.content_data,
                        "output_header_format": self.currentMessageData.Header_format,
                        "output_content_format": self.currentMessageData.content_format,
                        "output_periodicity": self.currentMessageData.periodicity
                        }


            DBUG.printDebug("------------------------------------------",self.currentMessageData)
            DBUG.printDebug("Current processing Message ID", self.currentMessageData.messageIdenitifer, type(self.currentMessageData.messageIdenitifer), type("rows['Msg_Identifier']"))
            for index, rows in self.df.iterrows():
                if pd.isna(rows["expected_output_message_Identifier"]):
                    continue
                
                if int(rows["expected_output_message_Identifier"]) == int(self.currentMessageData.messageIdenitifer):
                    DBUG.printDebug(index, rows["expected_output_message_Identifier"], self.currentMessageData.messageIdenitifer)
                    insertIndex = index
                    DBUG.printDebug("Inserting data in csv at index", insertIndex)
                    self.df.loc[insertIndex] = new_row
                    self.df.to_csv(f"{SNS_FOLDER}/{self.currentSNSProject}.csv", index=False)
                    break
            
        
            
    def DisplayOutputMessageData(self, data_type):
        DBUG.printWhere()
        print("Displaying data")
        global COUNTER_OUTPUT
        if data_type == "SAVE":
            messageDetails = snsMessageDetails(COUNTER_OUTPUT, self.currentMessageData.Message_Name, "","","","",self.currentMessageData.periodicity,"")
            self.addOutputMessageDetailsWidget(messageDetails, data_type)
        if data_type == "EDIT":
            messageDetails = snsMessageDetails(self.currentMessageData.messageIdenitifer, self.currentMessageData.Message_Name, self.currentMessageData.Header_format,self.currentMessageData.content_format,"","",self.currentMessageData.periodicity,self.currentMessageData.delay)
            self.addOutputMessageDetailsWidget(messageDetails, data_type)
            
            

    def EditOutputMessage(self, messageId, fromPage):
        DBUG.printWhere()
        DBUG.printDebug("Editing the Output message with id", messageId)
        for i, rows in self.df.iterrows():
            if pd.isna(rows["expected_output_message_Identifier"]):
                continue
            
            DBUG.printDebug(int(rows["expected_output_message_Identifier"]),int(messageId))
            if int(rows["expected_output_message_Identifier"]) == int(messageId):
                if rows["expected_output_message"] == "NO OUTPUT REQUIRED":
                    QMessageBox().critical(self.projectPageSNS, "EDIT DISABLED", "Edit functionality not required for NO OUTPUT", QMessageBox().Ok)
                elif "GUI_CHECK:" in rows["expected_output_message"] :
                    messageDetails = snsMessageDetails(rows["expected_output_message_Identifier"], rows["expected_output_message"], "", "", "", "", 0, -1)
                    self.editGuiCheckData(messageDetails)
                    
                elif "IMAGE_PATH:" in rows["expected_output_message"]:
                        messageDetails = snsMessageDetails(rows["expected_output_message_Identifier"], rows["expected_output_message"], "", "", "", "", 0, -1)
                        self.editOutputGUIImage(messageDetails)
                else:
                    DBUG.printDebug("Message found in CSV")
                    messageDetails = snsMessageDetails(rows["expected_output_message_Identifier"], rows["expected_output_message"], rows["output_header_data"], rows["output_content_data"], "", "", rows["output_periodicity"], -1)
                    DBUG.printInfo(self.df.head(6))
                    self.edit_message_sns_signal.emit(messageDetails, fromPage)
                break

            

    def editGuiCheckData(self, messageDetails):
        DBUG.printWhere()
        GUI_Check_Text = messageDetails.message.split("GUI_CHECK:")[1].strip()
        value, ok = QtWidgets.QInputDialog.getText(None,"USER CONFIRMATION", "Please Enter What to Check on GUI?", text=GUI_Check_Text)
        if ok:
            value = value.strip()
            if value == "":
              QMessageBox().information(self.projectPageSNS, "Empty Value", "Field cannot be empty", QMessageBox().Ok)  
              return
          
            GUI_Check_Text = "GUI_CHECK: " + value.strip()
        else:
            return
        output_data = mainWindow_SNS_save_edit_data("OUTPUT", "EDIT", messageDetails.messageIdenitifer, GUI_Check_Text, "", "", "", "", 0, -1)
        self.currentMessageData = output_data
        self.processOutputMessageData()
        
        
            
    def ListSelectedOutputMessages(self, options):
        DBUG.printWhere()
        messageIdenitiferList = []
        for i in range(self.newOutputMessagesListWidget.count()):
            itemW = self.newOutputMessagesListWidget.item(i)
            customWidget = self.newOutputMessagesListWidget.itemWidget(itemW)
            if customWidget.isCheckboxChecked():  
                messageIdenitiferList.append(int(customWidget.MessageId))
        
        if options == "SEND":
            self.SendSelectedMessages(messageIdenitiferList) 
        if options == "DELETE":        
            QuestionReply = QMessageBox().question(self.projectPageSNS, "Confirm Delete","Are you sure you want to delete this item?", QMessageBox.Yes | QMessageBox().No)
            if QuestionReply == QMessageBox.Yes:
                self.DeleteSelectedOutputMessages(messageIdenitiferList)
            elif QuestionReply == QMessageBox.No:
                return 
            
    def addOutputGUIImage(self, fromPage, saveEdit, messageIdentifier):
        DBUG.printWhere()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.newProjectWidgetSNS,"Select Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        file_path = "/SNS"+file_path.split("SNS")[-1]
        print("Image saving file path =>>>>>", file_path)
        if file_path:
            if saveEdit.lower() == "save":
                output_data = mainWindow_SNS_save_edit_data(fromPage, saveEdit, messageIdentifier, f"IMAGE_PATH:{file_path}", "", "", "", "", 0, 0)
                self.currentMessageData = output_data
                self.processOutputMessageData()
               
        else:
            DBUG.printDebug("Please choose a csv file")
            QMessageBox().critical(self.projectPageSNS, "No file selected", "Please choose a Project CSV file", QMessageBox().Ok)
    
    def editOutputGUIImage(self, messageDetails):
        DBUG.printWhere()
        file_Path_old = messageDetails.message.split("IMAGE_PATH:")[1].strip()
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.newProjectWidgetSNS,"Select Image", "", "All Files (*)")
        if file_path:
            output_data = mainWindow_SNS_save_edit_data("OUTPUT", "EDIT", messageDetails.messageIdenitifer, f"IMAGE_PATH:{file_path}", "", "", "", "", 0, 0)
            self.currentMessageData = output_data
            self.processOutputMessageData()
            
        else:
            DBUG.printDebug("Please choose a Image")
            QMessageBox().critical(self.projectPageSNS, "No Image selected", "Please choose an Image", QMessageBox().Ok)

        