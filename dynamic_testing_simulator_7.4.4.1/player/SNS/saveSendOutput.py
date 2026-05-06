from SNS.dynamic_sender import Dynamic_Sender
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QSize, Qt, pyqtBoundSignal, QObject
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtWidgets import QApplication, QTableView ,QVBoxLayout,QHeaderView,QMessageBox,QFileDialog,QHBoxLayout
from PyQt5.QtCore import QTimer, QFileSystemWatcher
import pandas as pd
import csv

class SaveSendOutput(QtWidgets.QWidget):
    test_result_SNS_output_signal = pyqtSignal(str,str,str, object, object)
    def __init__(self):
        super().__init__()
        self.openProjectPushButton = QtWidgets.QPushButton("Load Result File")
        
        self.openProjectPushButton.setMinimumSize(QtCore.QSize(150, 16777215))
        self.openProjectPushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.openProjectPushButton.setObjectName("openProjectPushButton")
        
        
        self.openSavePushButton = QtWidgets.QPushButton("Save Results")
        self.openSavePushButton.setMinimumSize(QtCore.QSize(150, 16777215))
        self.openSavePushButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.openSavePushButton.setObjectName("openSavePushButton")
        
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Function Name","Test case Name","Status","Recieved output","Expected output"])
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()
        # self.table.show()
        
        
        self.openProjectPushButton.clicked.connect(self.openProject)
        self.openSavePushButton.clicked.connect(self.saveFile)
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Interactive)
        header.setStretchLastSection(True)
        self.table.setColumnWidth(0,200)
        self.table.setColumnWidth(1,200)
        self.table.setColumnWidth(3,400)
        
        hLayout = QHBoxLayout()
        
        hLayout.addWidget(self.openProjectPushButton)
        hLayout.addWidget(self.openSavePushButton)

        
        layout = QVBoxLayout()
        layout.addLayout(hLayout)
        
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        # self.watcher = QFileSystemWatcher([self.filepath])
        # self.watcher.fileChanged.connect(self.onFileChanged)
        self.test_data = {}

        self.test_result_SNS_output_signal.connect(self.addOutputnew)
        
    
    def openProject(self):
         # DBUG.printWhere()
         # global COUNTER_INPUT, COUNTER_OUTPUT
          file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self,"Open File", "RESULTS", "All Files (*)")
         
          print("++++++++++++++++++++++",file_path)

          if file_path:
              df = pd.read_csv(file_path)
              print("efwefweffwf",df.head())
              
              for index , row in df.iterrows():
                  self.addOutputnew(row['Function Name'],row['Test case Name'],row['Status'],row['Recieved output'],row['Expected output'])
            
          else:
              QMessageBox().critical(self, "No file selected", "Please choose a Result CSV file", QMessageBox().Ok)
    
    def saveFile(self):
          # file_path = "Output.csv"
          file_path, _ = QFileDialog.getSaveFileName(
              self,
              "Save CSV File",
              "",
              "CSV Files (*.csv);;All Files (*)"
              )
          if not file_path:
              return 
          if not file_path.lower().endswith(".csv"):
              file_path += ".csv"
                                            
          with open(file_path,"w", newline="",encoding="utf-8") as file:
              writer = csv.writer(file)
              
              
              headers = [self.model.headerData(i,1) for i in range(self.model.columnCount())]
              writer.writerow(headers)
              
              for row in range(self.model.rowCount()):
                  row_data = []
                  for col in range(self.model.columnCount()):
                      index = self.model.index(row,col)
                      row_data.append(self.model.data(index))
                  writer.writerow(row_data)
                          
              print(f"Data saved to  {file_path}")
    
    
    def addOutputnew(self,functionName, testCaseName,status, received_output, expected_output):
        func_name = QtGui.QStandardItem(f"{functionName}")
        test_case = QtGui.QStandardItem(f"{testCaseName}")
        sts = QtGui.QStandardItem(f"{status}")
        rcvd_op = QtGui.QStandardItem(f"{received_output}")
        expected_op = QtGui.QStandardItem(f"{expected_output}")
        
        if status == 'Fail':
            sts.setBackground(QtGui.QColor(200,0,0))
        else:
            sts.setBackground(QtGui.QColor(0,200,0))
        
        item = [func_name,test_case,sts,rcvd_op,expected_op]
        
        self.model.insertRow(0,item) 
        # QtWidgets.QApplication.processEvents()