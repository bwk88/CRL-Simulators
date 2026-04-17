import sys
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QSizePolicy, QListWidgetItem, QWidget, QGridLayout, QLabel, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage, QBrush, QIcon
from mainwindow import Ui_MainWindow
from seleniumProcess import seleniumProcess
from publisherProcess import publisherProcess
import json
from datetime import datetime
from collections import OrderedDict
import os, time

from global_data import data
from customWidgets import settingsFieldWidgets, HistoryDataWidget, settingsFieldProjectSelector
from fileOperations import fileOperations
from ui_operations import ui_ops
from debuggerFile import debuggerInstance

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # file1 = "/home/saritajangra@Indigenous.com/Documents/QLM_selenium/IBMuploader_V0.1.2/IBMuploader/qlm_publisher_OLD3.py"
        # file2 = "/home/saritajangra@Indigenous.com/Documents/QLM_selenium/IBMuploader_V0.1.2/IBMuploader/qlm_publisher.py"
        #debuggerInstance.openDifferences(file1, file2)
        
        
        self.startProcessData={
            "excel_path":"",
            "Project_link":"",
            "Login_Username":"",
            "Login_password":"",
            "current_test_plan":""
            }
        
        self.startPublishData={
            "job_id": 0,
            "excel_path_publisher":"",
            "Project_link_publisher":"",
            "Login_Username_publisher":"",
            "Login_password_publisher":"",
            "Current_test_Plan_publisher":""
            }
        
        self.HistoryDataList = {
                # "job_id":{} //data format
            } 
        
        # self.timer = QTimer(self)   
        # self.timer.timeout.connect(self.updateProgressBar)
        
        # self.timer_publisher = QTimer(self)   
        # self.timer_publisher.timeout.connect(self.updatePublisherProgressBar)
        
        self.setMenuIcons()
        self.pushButton.clicked.connect(self.openFileDialog)
        self.pushButtonstart.clicked.connect(self.onStartButtonClickedSelenium)
        # self.pushButtonstart.setCheckable(True)
        self.pushButtonstartPublisher.clicked.connect(self.onStartButtonClickedPublisher)
        # self.pushButtonstartPublisher.setCheckable(True)
        self.pushButtonstopPublisher.clicked.connect(self.stopPublisher)
        self.progressBar.setValue(0)
        
        self.pushButton_2.clicked.connect(lambda:self.switch_page(0))
        self.pushButton_3.clicked.connect(lambda:self.switch_page(0))
        self.pushButton_7.clicked.connect(lambda:self.switch_page(1))
        self.pushButton_8.clicked.connect(lambda:self.switch_page(1))
        self.pushButton_9.clicked.connect(lambda:self.switch_page(2))
        self.pushButton_10.clicked.connect(lambda:self.switch_page(2))
        self.pushButton_5.clicked.connect(lambda:self.switch_page(3))
        self.pushButton_4.clicked.connect(lambda:self.switch_page(3))
        
        self.sortComboBox.currentTextChanged.connect(self.sortHistory)
        
        
        self.FileIOthread = QThread()
        self.FileIOWorker = fileOperations() 
        self.FileIOWorker.moveToThread(self.FileIOthread)
        
        self.FileIOWorker.finishedReadSettingsSignal.connect(self.initLoadSettingsFields)
        self.FileIOWorker.finishedReadHistorySignal.connect(self.initLoadHistoryWidgets)
        self.FileIOWorker.finishedWriteSettingsSignal.connect(self.doNothing)
        self.FileIOWorker.finishedWriteHistorySignal.connect(self.updateHistoryWidget)
        self.FileIOWorker.finishedreadHistoryViewerSignal.connect(self.DisplayHistoryViewerContents)
        self.FileIOthread.start()
        
        self.initWidgets()
        self.initReading()
 
        

    # ON INIT FUNCTIONS  
    def initWidgets(self):
        # Uploader
        self.labelSettingsUploader = QLabel("Uploader Settings")
        self.veritcLayout_10.addWidget(self.labelSettingsUploader)
        self.labelSettingsUploader.setText("UPLOADER SETTINGS")
        self.labelSettingsUploader.setStyleSheet("""
                                                 background-color: #1c1c28;
                                                 font-weight: bold;
                                                 font-size: 20px;
                                                 padding: 15px;
                                                 """)
        self.usernameWidget = settingsFieldWidgets("Login_Username uploader")
        self.usernameWidget.settings_updated_signal.connect(lambda value:self.updateSettings("Login_Username", value))
        self.veritcLayout_10.addWidget(self.usernameWidget)
        self.passwordWidget = settingsFieldWidgets("Login_password")
        self.passwordWidget.settings_updated_signal.connect(lambda value:self.updateSettings("Login_password", value))
        self.veritcLayout_10.addWidget(self.passwordWidget)
        self.linkWidget = settingsFieldWidgets("Project_link")
        self.linkWidget.settings_updated_signal.connect(lambda value:self.updateSettings("Project_link", value))
        self.linkWidget.hideButton()
        self.veritcLayout_10.addWidget(self.linkWidget)
        
        self.projectSelectorWidget = settingsFieldProjectSelector("Current Project")
        self.projectSelectorWidget.settings_updated_signal_combobox.connect(lambda value:self.UpdateLinkAndwriteSettingsData("Current_Project", value))
        self.projectSelectorWidget.user_added_combo_items_signal.connect(lambda value:self.writeRrefreshCombo("Project_list", value)) 
        self.projectSelectorWidget.user_deleted_combo_items_signal.connect(lambda value:self.deleteRrefreshCombo("Project_list", value))
        self.projectSelectorWidget.addComboItem("No Project set")
        self.veritcLayout_10.addWidget(self.projectSelectorWidget)
        
        self.planSelectorWidget = settingsFieldProjectSelector("Current Test Plan")
        self.planSelectorWidget.settings_updated_signal_combobox.connect(lambda value:self.UpdateLinkAndwriteSettingsData("Current_test_Plan", value))
        self.planSelectorWidget.user_added_combo_items_signal.connect(lambda value:self.writeRrefreshCombo("Test_plan_list", value))  
        self.planSelectorWidget.user_deleted_combo_items_signal.connect(lambda value:self.deleteRrefreshCombo("Test_plan_list", value))
        self.planSelectorWidget.addComboItem("No Test Plan set")
        self.veritcLayout_10.addWidget(self.planSelectorWidget)
        self.veritcLayout_10.addStretch()
        
       
        
        # Publisher
        self.labelSettingsPublisher = QLabel("Uploader Settings")
        self.veritcLayout_10Publisher.addWidget(self.labelSettingsPublisher)
        self.labelSettingsPublisher.setText("PUBLISHER SETTINGS")
        self.labelSettingsPublisher.setStyleSheet("""
                                                  background-color: #1c1c28;
                                                  font-weight: bold;
                                                  font-size: 20px;
                                                  padding: 15px;
                                                 """)
        self.usernameWidgetPublisher = settingsFieldWidgets("Login_Username")
        self.usernameWidgetPublisher.settings_updated_signal.connect(lambda value:self.updateSettings("Login_Username_publisher", value))
        self.veritcLayout_10Publisher.addWidget(self.usernameWidgetPublisher)
        self.passwordWidgetPublisher = settingsFieldWidgets("Login_password")
        self.passwordWidgetPublisher.settings_updated_signal.connect(lambda value:self.updateSettings("Login_password_publisher", value))
        self.veritcLayout_10Publisher.addWidget(self.passwordWidgetPublisher)
        self.linkWidgetPublisher = settingsFieldWidgets("Project_link")
        self.linkWidgetPublisher.settings_updated_signal.connect(lambda value:self.updateSettings("Project_link_publisher", value))
        self.linkWidgetPublisher.hideButton()
        self.veritcLayout_10Publisher.addWidget(self.linkWidgetPublisher)
        
        self.projectSelectorWidgetPublisher = settingsFieldProjectSelector("Current Project")
        self.projectSelectorWidgetPublisher.settings_updated_signal_combobox.connect(lambda value:self.UpdateLinkAndwriteSettingsData("Current_Project_publisher", value))
        self.projectSelectorWidgetPublisher.user_added_combo_items_signal.connect(lambda value:self.writeRrefreshCombo("Project_list", value))
        self.projectSelectorWidgetPublisher.user_deleted_combo_items_signal.connect(lambda value:self.deleteRrefreshCombo("Project_list", value))
        self.projectSelectorWidgetPublisher.addComboItem("No Project set")
        # self.projectSelectorWidgetPublisher.addComboItem("iCBTC_ATC")
        # self.projectSelectorWidgetPublisher.addComboItem("iCBTC_ATS")
        # self.projectSelectorWidgetPublisher.addComboItem("iCBTC_CBI")
        self.veritcLayout_10Publisher.addWidget(self.projectSelectorWidgetPublisher)
        
        self.planSelectorWidgetPublisher = settingsFieldProjectSelector("Current Test Plan")
        self.planSelectorWidgetPublisher.settings_updated_signal_combobox.connect(lambda value:self.UpdateLinkAndwriteSettingsData("Current_test_Plan_publisher", value))
        self.planSelectorWidgetPublisher.user_added_combo_items_signal.connect(lambda value:self.writeRrefreshCombo("Test_plan_list", value))
        self.planSelectorWidgetPublisher.user_deleted_combo_items_signal.connect(lambda value:self.deleteRrefreshCombo("Test_plan_list", value))
        self.planSelectorWidgetPublisher.addComboItem("No Test Plan set")
        self.veritcLayout_10Publisher.addWidget(self.planSelectorWidgetPublisher)
        self.veritcLayout_10Publisher.addStretch()
        
    
    def initReading(self):
        # print("Data before reading")
        # print(data.settingsData)
        # print(data.HistoryData)
        
        self.FileIOWorker.readSettingsSignal.emit()
        self.FileIOWorker.readHistorySignal.emit()
        
        
    def initLoadSettingsFields(self):
        # Uploader
        #print(data.settingsData)
        self.usernameWidget.setInitialValues(data.settingsData["Login_Username"] , "Login_Username")
        self.passwordWidget.setInitialValues(data.settingsData["Login_password"], "Login_password")
        self.linkWidget.setInitialValues("", "Project_link")
        data.settingsData["Project_link"] = ""
        self.projectSelectorWidget.selectItem("")
        data.settingsData["Current_Project"] = ""
            
        # PUBLISHER
        self.usernameWidgetPublisher.setInitialValues(data.settingsData["Login_Username_publisher"] , "Login_Username_publisher")
        self.passwordWidgetPublisher.setInitialValues(data.settingsData["Login_password_publisher"], "Login_password_publisher")
        self.linkWidgetPublisher.setInitialValues("", "Project_link_publisher")
        data.settingsData["Project_link_publisher"] = ""
        self.planSelectorWidgetPublisher.selectItem("")
        data.settingsData["Current_Project_publisher"] = ""
        self.refreshWidgets("add")
        
          
    def initLoadHistoryWidgets(self):
        for key, value in data.HistoryDataList.items():
            HistoryType=value["job_type"]
            self.addHistoryItems(value, HistoryType)
    
    
    def refreshWidgets(self, action):   
        if action == "add":
            for value in data.settingsData["Project_list"]:
                self.projectSelectorWidget.addComboItem(value)
                self.projectSelectorWidgetPublisher.addComboItem(value)
            for value in data.settingsData["Test_plan_list"]:
                self.planSelectorWidget.addComboItem(value)
                self.planSelectorWidgetPublisher.addComboItem(value)
   
    
    def onStartButtonClickedPublisher(self):
        if self.pushButtonstartPublisher.isChecked():
            self.pushButtonstartPublisher.setText("STOP")
            self.runPublisher("start")
        else:
            self.stopPublisher("stop")
            self.pushButtonstartPublisher.setText("START")
    
    
    def QuitThreadUploader(self):
        self.thread.quit()
        self.pushButtonstart.setText("START")
        # self.pushButtonstart.blockSignals(False)
        self.pushButtonstart.setEnabled(True)
        self.pushButtonstart.setStyleSheet("""
                                            font-weight: bold;
                                            background-color:#2b2e41;
                                      """)
        print("Uploader thread stopped")
    
    
    
    def onStartButtonClickedSelenium(self):
        print("Clicked start with => ", self.pushButtonstart.text().upper() == "START", self.pushButtonstart.isEnabled())
        
        if self.pushButtonstart.text().upper() == "START" and self.pushButtonstart.isEnabled():
            if self.runSelenium():
                print("Thread started")
                self.pushButtonstart.setText("STOP")
                
        elif self.pushButtonstart.text().upper() == "STOP":
            self.stopSelenium()
        else:
            print("STOPPPING PROCESS")
        

        
    def stopSelenium(self):
        if self.thread and self.thread.isRunning():
            self.updateHomeLiveStatus("Stopping Thread")
            # self.pushButtonstart.blockSignals(True)
            self.pushButtonstart.setEnabled(False)
            self.pushButtonstart.setText("STOPPING")
            self.pushButtonstart.setStyleSheet("""
                                                font-weight: bold;
                                                border-radius: 5px;
                                                background-color:#2b2e41;
                                                border: 5px inset #1c1c28;
                                          """)
            
                
            reply = QMessageBox().question(self.Contentwidget, "STOPPING UPLOADER", "Stopping will cause the partial uploading of the test cases, Do you really want to stop?", QMessageBox().Ok | QMessageBox().Cancel)
            if reply == QMessageBox().Ok:
                self.seleniumWorker.stopQLM()
            else:
                # self.pushButtonstart.blockSignals(False)
                self.pushButtonstart.setEnabled(True)
                self.pushButtonstart.setText("STOP")
                self.pushButtonstart.setStyleSheet("""
                                                    font-weight: bold;
                                                    background-color:#2b2e41;
                                              """)       
        else:
            return False
    
    
    
    
    # UPDATE SETTINGS AND HISTORY FUNCTIONS

    def updateSettings(self, field, value):
        # print("**********************************************************************")
        # print("(((((((((((((((((addHistoryItems))))))))))))))))))")
        # print("**********************************************************************")
        # print("PPGRESS UPDATING:     ",data.HistoryDataList)
        # print("**********************************************************************")
        data.settingsData[field] = value
        self.FileIOWorker.writeSettingsSignal.emit()
    
    def updateHistoryWidget(self, HistoryType):
        print("Histroy Data write successful")
    
    def doNothing(self):
        pass
    
    def UpdateLinkAndwriteSettingsData(self, field, selected_combobox):
        #print("-----settings changes --------->",field, selected_combobox)
        data.settingsData[field] = selected_combobox
        self.FileIOWorker.writeSettingsSignal.emit()
        if field == "Current_Project":
            if selected_combobox=="No Project set":
                data.settingsData["Project_link"] = ""
            if selected_combobox=="iCBTC_ATC":
                data.settingsData["Project_link"] = "https://icbtc-elm.indigenous.com/qm/web/console/iCBTC_ATC"
            if selected_combobox=="iCBTC_ATS":
                data.settingsData["Project_link"] = "https://icbtc-elm.indigenous.com/qm/web/console/iCBTC_ATS"
            if selected_combobox=="iCBTC_CBI":
                data.settingsData["Project_link"] = "https://icbtc-elm.indigenous.com/qm/web/console/iCBTC_CBI"
            self.linkWidget.setfieldValue(data.settingsData["Project_link"])
            
        if field == "Current_Project_publisher":
            if selected_combobox=="No Project set":
                data.settingsData["Project_link_publisher"] = ""
            if selected_combobox=="iCBTC_ATC":
                data.settingsData["Project_link_publisher"] = "https://icbtc-elm.indigenous.com/qm/web/console/iCBTC_ATC"
            if selected_combobox=="iCBTC_ATS":
                data.settingsData["Project_link_publisher"] = "https://icbtc-elm.indigenous.com/qm/web/console/iCBTC_ATS"
            if selected_combobox=="iCBTC_CBI":
                data.settingsData["Project_link_publisher"] = "https://icbtc-elm.indigenous.com/qm/web/console/iCBTC_CBI"
            self.linkWidgetPublisher.setfieldValue(data.settingsData["Project_link_publisher"])
                  
    def writeRrefreshCombo(self, field, value):
        print("settings of test plan added")
        data.settingsData[field].append(value)
        self.refreshWidgets("add")
        self.FileIOWorker.writeSettingsSignal.emit()
        
    
    def deleteRrefreshCombo(self, field, value):
        print("settings of test plan deleted, value")
        data.settingsData[field].remove(value)
        if field=="Project_list":
            self.projectSelectorWidget.deleteComboItem(value)
            self.projectSelectorWidgetPublisher.deleteComboItem(value)
        if field =="Test_plan_list":
            self.planSelectorWidget.deleteComboItem(value)
            self.planSelectorWidgetPublisher.deleteComboItem(value)
            
        self.refreshWidgets("delete")
        self.FileIOWorker.writeSettingsSignal.emit()
        
        
    #MENU SWITCH
    def switch_page(self, index):
        self.stackedWidget.setCurrentIndex(index)
        

    
    def setMenuIcons(self):    
        homeIcon = QPixmap("icons/Home.png")
        home_tinted_pixmap = ui_ops.tint_pixmap(homeIcon, QColor(255,255,255))
        self.pushButton_3.setIcon(QIcon(home_tinted_pixmap))
        self.pushButton_3.setIconSize(QtCore.QSize(25,25))
        
        createIcon = QPixmap("icons/pipeline.png")
        create_tinted_pixmap = ui_ops.tint_pixmap(createIcon, QColor(255,255,255))
        self.pushButton_5.setIcon(QIcon(create_tinted_pixmap))
        self.pushButton_5.setIconSize(QtCore.QSize(25,25))
        
        pipelineIcon = QPixmap("icons/create.png")
        pipeline_tinted_pixmap = ui_ops.tint_pixmap(pipelineIcon, QColor(255,255,255))
        self.pushButton_6.setIcon(QIcon(pipeline_tinted_pixmap))
        self.pushButton_6.setIconSize(QtCore.QSize(25,25))
        
        historyIcon = QPixmap("icons/History.png")
        history_tinted_pixmap = ui_ops.tint_pixmap(historyIcon, QColor(255,255,255))
        self.pushButton_8.setIcon(QIcon(history_tinted_pixmap))
        self.pushButton_8.setIconSize(QtCore.QSize(25,25))
        
        settingsIcon = QPixmap("icons/setting.png")
        settings_tinted_pixmap = ui_ops.tint_pixmap(settingsIcon, QColor(255,255,255))
        self.pushButton_10.setIcon(QIcon(settings_tinted_pixmap))
        self.pushButton_10.setIconSize(QtCore.QSize(25,25))

        
        closeIcon = QPixmap("icons/back.png")
        close_tinted_pixmap = ui_ops.tint_pixmap(closeIcon, QColor(255,255,255))
        self.pushButtonBackHV.setIcon(QIcon(close_tinted_pixmap))
        self.pushButtonBackHV.setIconSize(QtCore.QSize(25,25))
        
        # exitIcon = QPixmap("/home/kuldeepsingh@Indigenous.com/Documents/ATC_TESTING/Selenium/qmUploader/icons/exit.png")
        # tinted_pixmap = self.tint_pixmap(exitIcon, QColor(255,255,255))
        # self.label_3.setPixmap(tinted_pixmap)
        # self.pushButton_3.setIconSize(QtCore.QSize(25,25))
        
    
    # FILE SELECTING
    
    def openFileDialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self.Uploaderwidget,"Open File", "", "All Files (*)")
        if file_path:
            selected_sheet = file_path.split("/")[-1]
            self.label_2.setText(f"{selected_sheet}")
            self.startProcessData["excel_path"]=file_path      
    
    
    def closeHistoryViewer(self):
        self.switch_page(1)
        
        
    def DisplayHistoryViewerContents(self):
        print("---------------------------------------------------------")
        i = 1
        for key,value in data.DetailHistoryData.items():
            self.HistoryDetailsTextBrowser.append(f"{i}: {key}")
            for items in value:
                self.HistoryDetailsTextBrowser.append(items+"\n")
            self.HistoryDetailsTextBrowser.append("\n\n")
            i+=1   
        
        
    def showHistoryDetails(self, job_id):
        #print(f"{job_id} == {data.current_job_uploader} and {data.current_job_uploader}!=0 or {job_id} == {data.current_job_publisher} and {data.current_job_publisher}!=0")
        if (int(job_id) == data.current_job_uploader and data.current_job_uploader!=0) or (int(job_id) == data.current_job_publisher and data.current_job_publisher !=0):
            QMessageBox().critical(self.Contentwidget, "Task Currently Running", "View details in Publisher/Home", QMessageBox().Ok)
        else:
            self.HistoryDetailsTextBrowser.clear()
            self.job_id_HistoryViewer = str(job_id)
            # print(";;;;;;;;;;;;;;;;;;;;;;;;;;")
            # print(job_id)
            # print(self.HistoryDetailsTextBrowser.toPlainText())
            
            # print(data.HistoryDataList)
            # print(data.HistoryDataList[self.job_id_HistoryViewer]["job_type"])
            
            self.labelTitleHV.setText(data.HistoryDataList[self.job_id_HistoryViewer]["job_type"] + " : " + data.HistoryDataList[self.job_id_HistoryViewer]["TestPlan"])
            self.labelTimeValue.setText(data.HistoryDataList[self.job_id_HistoryViewer]["Time"])
            self.labelDateValue.setText(data.HistoryDataList[self.job_id_HistoryViewer]["Date"])
            self.labelProgressValue.setText(str(data.HistoryDataList[self.job_id_HistoryViewer]["ProgressStatus"]))
            self.pushButtonBackHV.clicked.connect(self.closeHistoryViewer)
            self.FileIOWorker.readHistoryViewerSignal.emit(data.HistoryDataList[self.job_id_HistoryViewer]["TestPlan"]+"_"+str(job_id))
            self.switch_page(4)
        

    def addHistoryItems(self, HistoryData, HistoryType):
        # print("**********************************************************************")
        # print("(((((((((((((((((addHistoryItems))))))))))))))))))")
        # print("**********************************************************************")
        # print("PPGRESS UPDATING:     ",data.HistoryDataList)fu
        # print("**********************************************************************")
        item = QListWidgetItem(self.HistorylistWidget)
        
        if HistoryType == "UPLOAD":
            self.HdataWidget = HistoryDataWidget(HistoryData)
            self.HdataWidget.display_history_details_signal.connect(self.showHistoryDetails)
            self.HdataWidget.resume_button_clicked_signal.connect(self.resumeTaskUpload)
            # self.HdataWidget.updateLiveData(0)
            item.setSizeHint(self.HdataWidget.sizeHint())
            self.HistorylistWidget.insertItem(0, item)
            self.HistorylistWidget.setItemWidget(item, self.HdataWidget)
            if HistoryData["Status"] == "Finished":
                self.HdataWidget.enableResume(False)
            
        if HistoryType == "PUBLISH":
            self.HdataPublishWidget = HistoryDataWidget(HistoryData)
            self.HdataPublishWidget.display_history_details_signal.connect(self.showHistoryDetails)
            self.HdataPublishWidget.resume_button_clicked_signal.connect(self.resumeTaskPublish)
            item.setSizeHint(self.HdataPublishWidget.sizeHint())
            self.HistorylistWidget.insertItem(0, item)
            self.HistorylistWidget.setItemWidget(item, self.HdataPublishWidget)
            if HistoryData["Status"] == "Finished":
                self.HdataPublishWidget.enableResume(False)
                
        self.updateSettings("Last_job_id", data.settingsData["Last_job_id"])
        
        
    def createHistory(self, progress, HistoryType):
        # print("**********************************************************************")
        # print("(((((((((((((((((createHistory))))))))))))))))))")
        # print("**********************************************************************")
        # print("PPGRESS UPDATING:     ",data.HistoryDataList)
        # print("**********************************************************************")
        data.HistoryData["job_id"] = str(data.settingsData["Last_job_id"])
        data.HistoryData["job_type"] = HistoryType
        data.HistoryData["Date"]=self.currentDateTime("date")
        data.HistoryData["Time"]=self.currentDateTime("time")
        data.HistoryData["ProgressStatus"]=progress
        data.HistoryData["Status"]="Ongoing"

        
        if HistoryType == "UPLOAD":
            data.HistoryData["username"] = data.settingsData["Login_Username"]
            data.HistoryData["password"] = data.settingsData["Login_password"]
            data.HistoryData["link"] = data.settingsData["Project_link"]
            data.HistoryData["Project"]= data.settingsData["Current_Project"]
            data.HistoryData["TestPlan"] = data.settingsData["Current_test_Plan"]
            self.addHistoryItems(data.HistoryData, "UPLOAD")

        if HistoryType == "PUBLISH":
            data.HistoryData["username"] = data.settingsData["Login_Username_publisher"]
            data.HistoryData["password"] = data.settingsData["Login_password_publisher"]
            data.HistoryData["link"] = data.settingsData["Project_link_publisher"]
            data.HistoryData["Project"]= data.settingsData["Current_Project_publisher"]
            data.HistoryData["TestPlan"] = data.settingsData["Current_test_Plan_publisher"]
            self.addHistoryItems(data.HistoryData, "PUBLISH")
            
        # This signal will trigger the fucntion in fileOperatioin Thread which 
        # will write history data from current global history data state
        self.FileIOWorker.writeHistorySignal.emit(HistoryType)
        
  

        
        
    # UPLOADER: ON START BUTTON CLICKED FUNCTIONS     
    def runSelenium(self):
        if self.label_2.text() == "Your selected file .........":
            QMessageBox().critical(self.Contentwidget, "Error", "Please Choose the Excel file!!", QMessageBox().Ok)
            return False
        else:      
            #print(data.settingsData["Login_Username"],data.settingsData["Login_password"],data.settingsData["Project_link"], data.settingsData["Current_Project"])
            if data.settingsData["Current_Project"] == "" or data.settingsData["Current_Project"] == "No Project set":
                QMessageBox().critical(self.Contentwidget, "Error", "Choose project in uploader settings", QMessageBox().Ok)
                return False
            elif data.settingsData["Login_Username"] == "":
                QMessageBox().critical(self.Contentwidget, "Error", "Please set username in uploader settings", QMessageBox().Ok)
                return False
            elif data.settingsData["Login_password"] == "":
                QMessageBox().critical(self.Contentwidget, "Error", "Please set password in uploader settings", QMessageBox().Ok)
                return False
            elif data.settingsData["Current_test_Plan"] == "" or data.settingsData["Current_test_Plan"] == "No Test Plan set":
                QMessageBox().critical(self.Contentwidget, "Error", "Please set password in uploader settings", QMessageBox().Ok) 
                return False
            else:
                data.settingsData["Last_job_id"]+=1
                data.current_job_uploader = data.settingsData["Last_job_id"]
                
                self.startProcessData["Login_Username"] = data.settingsData["Login_Username"]
                self.startProcessData["Login_password"] = data.settingsData["Login_password"]
                self.startProcessData["Project_link"] = data.settingsData["Project_link"]
                self.startProcessData["current_test_plan"] = data.settingsData["Current_test_Plan"]
                
                
                #  #1c1c28 #2b2e41
                self.thread = QThread()
                self.seleniumWorker = seleniumProcess(self.startProcessData)
                # self.seleniumWorker.finished.connect(self.thread.quit)
                self.seleniumWorker.finished.connect(self.QuitThreadUploader)
                self.seleniumWorker.update_signal.connect(self.updateHomeLiveStatus)
                self.seleniumWorker.progress_signal.connect(self.updateProgressBar)
                self.thread.finished.connect(self.threadFinished)
                self.seleniumWorker.moveToThread(self.thread)
                self.thread.started.connect(self.seleniumWorker.run)
                self.thread.start()
                
                
                # self.seleniumWorker = seleniumProcess(self.startProcessData)
                # self.seleniumWorker.finished.connect(self.QuitThreadUploader)
                # self.seleniumWorker.update_signal.connect(self.updateHomeLiveStatus)
                # self.seleniumWorker.progress_signal.connect(self.updateProgressBar)
                # # self.thread.finished.connect(self.threadFinished)
                # # self.seleniumWorker.moveToThread(self.thread)
                # # self.seleniumWorker.started.connect(self.seleniumWorker.run)
                # self.seleniumWorker.start()
                
                self.createHistory(data.current_progress_value, "UPLOAD")
                
                self.progress = 0
                self.progressBar.setValue(self.progress)
                return True
                # self.timer.start(100)
                
                

    # UPDATE LIVE DATAS   
    def updateProgressBar(self):
        self.progressBar.setValue(data.current_progress_value)
        self.HdataWidget.updateLiveData(data.current_progress_value)
        self.FileIOWorker.writeProgressSignal.emit("UPLOAD")
        
    
    def updateHomeLiveStatus(self,status_data): 
        status_data = self.currentDateTime("date") +" ["+ self.currentDateTime("time")+"] : \n"+status_data+"\n\n"
        self.textBrowser.append(status_data)
        # data.DetailHistoryDataUploader["LiveStatus"].append(status_data)
        # self.FileIOWorker.writeHistoryViewerSignal.emit("UPLOAD")
            
            
    def threadFinished(self):
        print("###############threadFinished")
        self.pushButtonstart.setEnabled(True)
        self.pushButtonstart.setStyleSheet("""
                                         font-weight: bold;
                                         background-color:#2b2e41;
                                       """)
        data.current_job_uploader = 0
        
        self.updateHomeLiveStatus("Thread Stopped")
        
     
    def resumeTaskUpload(self):
        QMessageBox().critical(self.Contentwidget, "Uploader Resume Not supported Yet!", "To be available in next version", QMessageBox().Ok)
        
       
        
       
        
    #  PUBLISHER : ON start publish button clicked 
    def runPublisher(self, task, resume_data={}, resumerObj=None):
        # print("**********************************************************************")
        # print("(((((((((((((((((runPublisher))))))))))))))))))")
        # print("**********************************************************************")
        # print("PPGRESS UPDATING:     ",data.HistoryDataList)
        # print("**********************************************************************")
        self.textBrowserPublisher.clear()
        self.TotalPublishedLabel.setText(f"TOTAL TEST SUITES PUBLISHED: 0")
        
        if data.settingsData["Current_Project_publisher"] == "" or data.settingsData["Current_Project_publisher"] == "No Project set":
            QMessageBox().critical(self.Contentwidget, "Error", "Choose project in publisher settings", QMessageBox().Ok)
        elif data.settingsData["Login_Username_publisher"] == "":
            QMessageBox().critical(self.Contentwidget, "Error", "Please set username in publisher settings", QMessageBox().Ok)
        elif data.settingsData["Login_password_publisher"] == "":
            QMessageBox().critical(self.Contentwidget, "Error", "Please set password in publisher settings", QMessageBox().Ok) 
        elif data.settingsData["Current_test_Plan_publisher"] == "" or data.settingsData["Current_test_Plan_publisher"] == "No Test Plan set":
            QMessageBox().critical(self.Contentwidget, "Error", "Please set Test plan in publisher settings", QMessageBox().Ok) 
        else: 
            
            self.startPublishData["Login_Username_publisher"] = data.settingsData["Login_Username_publisher"]
            self.startPublishData["Login_password_publisher"] = data.settingsData["Login_password_publisher"]
            self.startPublishData["Project_link_publisher"] = data.settingsData["Project_link_publisher"]
            self.startPublishData["Current_test_Plan_publisher"] = data.settingsData["Current_test_Plan_publisher"]
            if task == "start": 
                data.HistoryData["job_id"]=0
                data.HistoryData["job_type"]="" #UPLOAD OR PUBLISH
                data.HistoryData["Date"]=""
                data.HistoryData["Time"]=""
                data.HistoryData["ProgressStatus"]=0
                data.HistoryData["Status"]="" #Finished/Ongoing
                data.HistoryData["username"]=""
                data.HistoryData["password"]=""
                data.HistoryData["link"]=""
                data.HistoryData["Project"]=""
                data.HistoryData["TestPlan"]=""
                                 
                data.settingsData["Last_job_id"] =  data.settingsData["Last_job_id"]+1
                #print(">>>>>>>>>>> NEW JOB TO BEGIN",  data.settingsData["Last_job_id"])
                data.current_job_publisher = data.settingsData["Last_job_id"]
                self.startPublishData["job_id"] = data.settingsData["Last_job_id"]
                
                data.current_publisher_progress_value = 0
                self.createHistory(data.current_publisher_progress_value, "PUBLISH")
                
            if task == "resume":
                data.current_publisher_progress_value = resume_data['ProgressStatus']
                self.startPublishData["job_id"] = resume_data["job_id"]
                self.TotalPublishedLabel.setText(f"TOTAL TEST SUITES PUBLISHED: {data.current_publisher_progress_value}")
                
            if task == "start":
                HistoryWidget = self.HdataPublishWidget

            if task == "resume":
                HistoryWidget = resumerObj
                
            #  #1c1c28 #2b2e41
            self.thread_publish = QThread()
            self.publisherWorker = publisherProcess(self.startPublishData)
            self.publisherWorker.finished.connect(self.thread_publish.quit)
            self.thread_publish.finished.connect(self.thread_publish_Finished)
            self.publisherWorker.update_progress_signal.connect(lambda value:self.updatePublisherProgressBar(value, HistoryWidget))
            self.publisherWorker.update_signal_publish.connect(self.updatePublishLiveStatus)
            self.publisherWorker.error_signal_received_publisher.connect(self.errorOccuredPublisher)
            self.publisherWorker.moveToThread(self.thread_publish)
            self.thread_publish.started.connect(self.publisherWorker.run)
            self.thread_publish.start()
            

            
            # self.pushButtonstartPublisher.setEnabled(False)
            # self.pushButtonstartPublisher.setStyleSheet("""
            #                                    font-weight: bold;
            #                                    border-radius: 5px;
            #                                    background-color:#2b2e41;
            #                                    border: 5px inset #1c1c28;
            #                                    padding: 0px 15px;
            #                                    """)
            

    def errorOccuredPublisher(self, error):
        QMessageBox().critical(self.Contentwidget, "Error", f"{error}", QMessageBox().Ok)
        
    def updatePublisherProgressBar(self, value, resumerObj):
        print("===================================== updatePublisherProgressBar ===============================================")
        if value == "-1":
            # History_data = resumerObj.getObjectData()
            # History_data["Status"] = "Finished"
            data.HistoryDataList[str(data.current_job_publisher)]["Status"] = "Finished"
            resumerObj.enableResume(False)
            self.FileIOWorker.updateHistorySignal.emit("PUBLISH")
        else:
            prev_value = self.TotalPublishedLabel.text().split(": ")[-1]
            #print(prev_value, "akshfdasljflasjdflasjd=>>>>>>>>>>>>>>>>>>")
            self.TotalPublishedLabel.setText(f"TOTAL TEST SUITES PUBLISHED: {data.current_publisher_progress_value}")
            resumerObj.updateLiveData(data.current_publisher_progress_value)
            self.FileIOWorker.writeProgressSignal.emit("PUBLISH")
        
    def updatePublishLiveStatus(self,status_data): 
        print("===================================== updatePublishLiveStatus ===============================================")
        status_data = self.currentDateTime("date") +" ["+ self.currentDateTime("time")+"] : "+status_data+"\n\n"
        self.textBrowserPublisher.append(status_data)

        
    def thread_publish_Finished(self):
        print("###############threadFinished")
        self.pushButtonstartPublisher.setEnabled(True)
        self.pushButtonstartPublisher.setStyleSheet("""
                                         font-weight: bold;
                                         background-color:#2b2e41;
                                       """)
        data.current_job_publisher = 0

        
    def stopPublisher(self):
        self.publisherWorker.stopProcess()
        QMessageBox().critical(self.Contentwidget, "Thread stopped", "To be available in next version", QMessageBox().Ok)
        
    def resumeTaskPublish(self):
        senderObj  = self.sender()
        resumeData = senderObj.getObjectData()
        # print(type(data.current_job_publisher), type(resumeData["job_id"]))
        # print(data.current_job_publisher, resumeData["job_id"])
        if data.current_job_publisher != 0:
             QMessageBox().critical(self.Contentwidget, "Task is already Publishing", "Task Running in Publish Window", QMessageBox().Ok)
        else:
            self.switch_page(3)
            data.current_job_publisher = resumeData["job_id"]
           
            data.settingsData["Project_link_publisher"] = resumeData["link"]
            data.settingsData["Current_Project_publisher"] = resumeData["password"]
            data.settingsData["Current_test_Plan_publisher"] = resumeData["TestPlan"]
           
            # set settings widgets
            self.usernameWidgetPublisher.setfieldValue(resumeData["username"])
            self.passwordWidgetPublisher.setfieldValue(resumeData["password"])
            self.linkWidgetPublisher.setfieldValue(resumeData["link"])
            self.projectSelectorWidgetPublisher.selectItem(resumeData["Project"])
            self.planSelectorWidgetPublisher.selectItem(resumeData["TestPlan"])
           
            self.runPublisher("resume", resumeData, senderObj)
         
       
        
    def currentDateTime(self,requestType):
        now = datetime.now()
        if requestType.lower()=="date":
            return now.strftime("%d-%m-%Y")
        if requestType.lower()=="time":
            return now.strftime("%H:%M:%S")
            

    def sortHistory(self):
        print("sortComboBox")
        sortBy = self.sortComboBox.currentText()
        items = []
        for i in range(self.HistorylistWidget.count()):
            item = self.HistorylistWidget.item(i)
            widget = self.HistorylistWidget.itemWidget(item)
            if widget:
                #print("widget found")
                widget.setParent(None)
                try:
                    id_value = int(widget.get_id()) 
                    historyData = widget.get_Data()
                    #print(id_value)
                    items.append((id_value, historyData))
                except Exception as e:
                    print(f"Error extracting id from widget {e}")
        
            #print(f"Widget {i}: {widget}- ID: {widget.get_id() if widget else 'None'}")
        if sortBy == "Date Latest":
            items.sort(key=lambda x: x[0])
        if sortBy == "Date Oldest":
            items.sort(key=lambda x: x[0], reverse=True)
            
            
        self.HistorylistWidget.clear()
        for id_val, historyData in items:
            newItem = QListWidgetItem()
            widget = HistoryDataWidget(historyData)
            newItem.setSizeHint(widget.sizeHint())
            self.HistorylistWidget.addItem(newItem)
            self.HistorylistWidget.setItemWidget(newItem, widget)

            
    def searchHistory(self):
        print("searching History")
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(app.exec_())
