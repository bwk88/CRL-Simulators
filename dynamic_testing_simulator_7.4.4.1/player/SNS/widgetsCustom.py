import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QCompleter, QListView, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QDialog, QGridLayout, QComboBox, QCheckBox, QSizePolicy, QMessageBox, QDialog, QTextEdit, QFormLayout, QDialogButtonBox
from PyQt5.QtCore import pyqtSignal, QSize, Qt, QStringListModel
from SNS.utility import SafeListWidget, ui_ops
from PyQt5.QtGui import QFontMetrics, QFont, QPixmap

CWD = os.getcwd()

# Widget to display functions
class itemsLWFunctions(QWidget):
    open_clicked_signal = pyqtSignal(str)
    edit_clicked_signal = pyqtSignal(str)
    def __init__(self, fieldName, widgetOf):
        super().__init__()
        
        layout_outer = QHBoxLayout(self)
        layout_outer.setContentsMargins(10,0,10,0)
        
        self.container = QWidget()
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
                                QWidget{
                                    background-color: #f6f5f4;
                                    border: 2px solid #eeeeee;
                                }
                                QLabel{
                                    border: 0px;
                                    }
                                QLineEdit{
                                    border: 0px;
                                    }
                                """)
        self.layout = QHBoxLayout(self.container)
        
        self.selectorWidget = QWidget(self)
        self.selectorWidget.setStyleSheet("""
                                          border: 0px;
                                          """)
        self.selectorWidgetLayout = QHBoxLayout(self.selectorWidget)
        self.checkBox = QCheckBox(self.selectorWidget)
        self.selectorWidgetLayout.addWidget(self.checkBox)
        self.checkBox.setStyleSheet("""
                                    QCheckBox {
                                        margin-right: 10px;
                                        }
                                      """)
        self.indexLabel = QLabel(self.selectorWidget)
        self.selectorWidgetLayout.addWidget(self.indexLabel)
        self.indexLabel.setText(str(12))
        self.layout.addWidget(self.selectorWidget)
        
        
        self.labelLineEdit = QLineEdit(f"{fieldName}")
        self.labelLineEdit.setContentsMargins(12,0,12,0)
        self.layout.addWidget(self.labelLineEdit)
        self.labelLineEdit.setCursorPosition(0)
        self.labelLineEdit.setReadOnly(True)
        self.labelLineEdit.setFocusPolicy(Qt.NoFocus)
        self.labelLineEdit.setAttribute(Qt.WA_TransparentForMouseEvents, True)
                
        self.buttonOpenTestCases = QPushButton("Open")
        self.buttonOpenTestCases.setFixedSize(60,40)
        self.buttonOpenTestCases.clicked.connect(self.onButtonOpenClicked)
        self.layout.addWidget(self.buttonOpenTestCases)
        self.buttonOpenTestCases.setStyleSheet("""
                                               QPushButton{
                                                   background-color: #eeeeee;
                                                   color: #000000;
                                                   border: none;
                                                   border-radius: 8px;
                                                   padding 8px 16px;
                                           
                                               }
                                               QPushButton:hover{
                                                   background-color: #424242;
                                                   color: #f5f5f5;
                                               }
                                               """)
        
        # self.buttonEdit = QPushButton(f"Edit {widgetOf}")
        self.buttonEdit = QPushButton()
        self.buttonEdit.setFixedSize(40,40)
        self.buttonEdit.clicked.connect(self.onButtonEditClicked)
        ui_ops.setSVG(self.buttonEdit, "icons/actions/edit_file.svg", 40, 40)
        self.buttonEdit.setStyleSheet("""
                                        QPushButton{
                                            border: 0px;
                                    
                                        }
                                        QPushButton:hover{
                                            border-bottom: 5px solid #990000;
                                        }
                                      
                                      """)
        self.buttonEdit.setToolTip(f"Edit {widgetOf}")
        self.layout.addWidget(self.buttonEdit)
                                      
        layout_outer.addWidget(self.container)
        
        self.setLayout(layout_outer)
    
    def updateIndex(self, index):
        # print("Update index ", index)
        self.indexLabel.setText(str(index))
    
    def onButtonOpenClicked(self):
        print("clicked open")
        
        self.open_clicked_signal.emit(self.labelLineEdit.text())
    
    def onButtonEditClicked(self):
        print("clicked Edit")
        self.edit_clicked_signal.emit(self.labelLineEdit.text())
        
    def getLabelName(self):
        return self.labelLineEdit.text()
    
    def updateLabel(self, newName):
        self.labelLineEdit.setText(newName)
    
    def isCheckboxChecked(self):
        if self.checkBox.isChecked():
            print("ckbox", True)
            return True
        else:
            print("ckbox", False)
            return False
        
    def toggleCheckBox(self, isSelected):
        if isSelected == False:
            self.checkBox.setChecked(True)
        if isSelected == True:
            self.checkBox.setChecked(False)

    def setUnsetCheckBox(self):
        if self.checkBox.isChecked():
            self.checkBox.setChecked(False)
        else:
            self.checkBox.setChecked(True)
            
            

# Widget to display TestCases
class itemsLWTestCase(QWidget):
    open_clicked_signal = pyqtSignal(str)
    edit_clicked_signal = pyqtSignal(str)
    preconditions_clicked_signal = pyqtSignal(str)
    def __init__(self, fieldName, widgetOf):
        super().__init__()
        
        layout_outer = QHBoxLayout(self)
        layout_outer.setContentsMargins(10,0,10,0)
        
        self.container = QWidget()
        self.container.setObjectName("container")
        self.container.setStyleSheet("""
                                QWidget{
                                    background-color: #f6f5f4;
                                    border: 2px solid #eeeeee;
                                }
                                QLabel{
                                    border: 0px;
                                    }
                                QLineEdit{
                                    border: 0px;
                                    }
                                """)
        self.layout = QHBoxLayout(self.container)
        
        self.selectorWidget = QWidget(self)
        self.selectorWidget.setStyleSheet("""
                                          border: 0px;
                                          """)
        self.selectorWidgetLayout = QHBoxLayout(self.selectorWidget)
        self.checkBox = QCheckBox(self.selectorWidget)
        self.selectorWidgetLayout.addWidget(self.checkBox)
        self.checkBox.setStyleSheet("""
                                    QCheckBox {
                                        margin-right: 10px;
                                        }
                                      """)
        self.indexLabel = QLabel(self.selectorWidget)
        self.selectorWidgetLayout.addWidget(self.indexLabel)
        self.indexLabel.setText(str(12))
        self.layout.addWidget(self.selectorWidget)
        
        
        self.labelLineEdit = QLineEdit(f"{fieldName}")
        self.labelLineEdit.setContentsMargins(12,0,12,0)
        self.layout.addWidget(self.labelLineEdit)
        self.labelLineEdit.setCursorPosition(0)
        self.labelLineEdit.setReadOnly(True)
        self.labelLineEdit.setFocusPolicy(Qt.NoFocus)
        self.labelLineEdit.setAttribute(Qt.WA_TransparentForMouseEvents, True)

                 
        self.buttonPreconditionsTestCases = QPushButton("Preconditions")
        self.buttonPreconditionsTestCases.setFixedSize(100,40)
        self.buttonPreconditionsTestCases.clicked.connect(self.onButtonPreconditionsClicked)
        self.layout.addWidget(self.buttonPreconditionsTestCases)
        self.buttonPreconditionsTestCases.setStyleSheet("""
                                               QPushButton{
                                                   background-color: #eeeeee;
                                                   color: #000000;
                                                   border: none;
                                                   border-radius: 8px;
                                                   padding 8px 16px;
                                           
                                               }
                                               QPushButton:hover{
                                                   background-color: #424242;
                                                   color: #f5f5f5;
                                               }
                                               """)
                                               
                                               
        self.buttonOpenTestCases = QPushButton("Open")
        self.buttonOpenTestCases.setFixedSize(60,40)
        self.buttonOpenTestCases.clicked.connect(self.onButtonOpenClicked)
        self.layout.addWidget(self.buttonOpenTestCases)
        self.buttonOpenTestCases.setStyleSheet("""
                                               QPushButton{
                                                   background-color: #eeeeee;
                                                   color: #000000;
                                                   border: none;
                                                   border-radius: 8px;
                                                   padding 8px 16px;
                                           
                                               }
                                               QPushButton:hover{
                                                   background-color: #424242;
                                                   color: #f5f5f5;
                                             onButtonOpenClicked  }
                                               """)
        
        # self.buttonEdit = QPushButton(f"Edit {widgetOf}")
        self.buttonEdit = QPushButton()
        self.buttonEdit.setFixedSize(40,40)
        self.buttonEdit.clicked.connect(self.onButtonEditClicked)
        ui_ops.setSVG(self.buttonEdit, "icons/actions/edit_file.svg", 40, 40)
        self.buttonEdit.setStyleSheet("""
                                        QPushButton{
                                            border: 0px;
                                    
                                        }
                                        QPushButton:hover{
                                            border-bottom: 5px solid #990000;
                                        }
                                      
                                      """)
        self.buttonEdit.setToolTip(f"Edit {widgetOf}")
        self.layout.addWidget(self.buttonEdit)
                                      
        layout_outer.addWidget(self.container)
        
        self.setLayout(layout_outer)
    
    def updateIndex(self, index):
        # print("Update index ", index)
        self.indexLabel.setText(str(index))
    
    def onButtonOpenClicked(self):
        print("clicked open")
        
        self.open_clicked_signal.emit(self.labelLineEdit.text())
        
    def onButtonEditClicked(self):
        print("clicked Edit")
        self.edit_clicked_signal.emit(self.labelLineEdit.text())
        
    def onButtonPreconditionsClicked(self):
        print("clicked Preconditions")
        
        self.preconditions_clicked_signal.emit(self.labelLineEdit.text())
        
    def getLabelName(self):
        return self.labelLineEdit.text()
    
    def updateLabel(self, newName):
        self.labelLineEdit.setText(newName)
    
    def isCheckboxChecked(self):
        if self.checkBox.isChecked():
            print("ckbox", True)
            return True
        else:
            print("ckbox", False)
            return False
        
    def toggleCheckBox(self, isSelected):
        if isSelected == False:
            self.checkBox.setChecked(True)
        if isSelected == True:
            self.checkBox.setChecked(False)

    def setUnsetCheckBox(self):
        if self.checkBox.isChecked():
            self.checkBox.setChecked(False)
        else:
            self.checkBox.setChecked(True)
     
            
class preconditionsWidget(QWidget):
    precondtions_updated_signal = pyqtSignal(list, str, str)
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Test Cases")
        self.setWindowFlags(Qt.Dialog | Qt.Window)
        self.setGeometry(100,100,800,500)
        
        self.suiteComboBox = QComboBox()
        self.suiteComboBox.setObjectName("suiteComboBox")
        self.suiteComboBox.setEditable(True)
        self.suiteComboBox.setInsertPolicy(QComboBox.NoInsert)#prevents insertion of search text
        self.suiteComboBox.completer().setCompletionMode(QCompleter.PopupCompletion)
        
        
        self.caseComboBox = QComboBox()
        self.caseComboBox.setObjectName("caseComboBox")


        self.viewPreconditions = QListView()
        self.viewPreconditions.setStyleSheet("background-color: #f6f5f4;")
        self.modelPreconditions = QStringListModel()
        self.viewPreconditions.setModel(self.modelPreconditions)
        self.viewPreconditions.setSelectionMode(QListView.ExtendedSelection)
        
        
        
        self.addButton = QPushButton("ADD")
        self.addButton.setFixedSize(100,30)
        self.addButton.clicked.connect(self.addClicked)
        self.deleteButton = QPushButton("Delete")
        self.deleteButton.setFixedSize(100,30)
        self.deleteButton.clicked.connect(self.deleteClicked)
        self.saveButton = QPushButton("Save")
        self.saveButton.setFixedSize(100,30)
        self.saveButton.clicked.connect(self.saveClicked)
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setFixedSize(100,30)
        self.cancelButton.clicked.connect(self.cancelClicked)
        

        
        
        layout = QVBoxLayout(self)
        
        self.combolayout = QHBoxLayout()
        self.combolayout.addWidget(self.suiteComboBox)
        self.combolayout.addWidget(self.addButton)
        layout.addLayout(self.combolayout)
        layout.addSpacing(20)

        self.addedListLayout = QHBoxLayout()
        self.addedListLayout.addWidget(self.viewPreconditions)
        self.optionsLayout = QVBoxLayout()
        self.optionsLayout.addWidget(self.deleteButton, alignment=Qt.AlignTop)
        self.optionsLayout.addWidget(self.saveButton, alignment=Qt.AlignTop)
        self.optionsLayout.addWidget(self.cancelButton, alignment=Qt.AlignTop)
        self.optionsLayout.addStretch()
        self.addedListLayout.addLayout(self.optionsLayout)
        layout.addLayout(self.addedListLayout)
        
        self.move((parent.width()-self.width())//2, (parent.height()-self.height())//2)

        self.setLayout(layout)
    
    def run(self, Function, testCaseName, testCaseList, alreadyAddedTcList):
        self.suite = Function
        self.testcase = testCaseName

        self.suiteComboBox.clear()
        self.suiteComboBox.addItems(testCaseList)
        
        self.addedTestCaseList=[]
        self.addedTestCaseList.extend(alreadyAddedTcList)
        self.modelPreconditions.setStringList(self.addedTestCaseList)
        
    def saveClicked(self):
        print("selected Funttion", self.addedTestCaseList)
        self.precondtions_updated_signal.emit(self.addedTestCaseList, self.suite, self.testcase)
        self.close()
        return
    
    def cancelClicked(self):
        self.close()
        return
    
    def addClicked(self):
        selected =  self.suiteComboBox.currentText()
        self.addedTestCaseList.append(selected)
        self.modelPreconditions.setStringList(self.addedTestCaseList)
        print("added")

    def deleteClicked(self):
        selectedIndexes =  self.viewPreconditions.selectedIndexes()
        for index in sorted(selectedIndexes, reverse=True):
            del self.addedTestCaseList[index.row()]

        self.modelPreconditions.setStringList(self.addedTestCaseList)
        print("deleted")
        

           
            
class addItemsWidget(QWidget):
    update_settings_signal = pyqtSignal(str)
    def __init__(self, parent, name):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.Window)
        self.name = name
        self.setGeometry(100,100,500,100)
        self.setWindowTitle(f"Change {name}")
        # self.setSizeGripEnabled(True)
        
        layout = QVBoxLayout()
        
        self.textedit = QTextEdit()
        self.textedit.setPlaceholderText(f"Set {name}")
        layout.addWidget(self.textedit)
        
        self.hlayout = QHBoxLayout()
        self.setButton = QPushButton("Set")
        self.setButton.clicked.connect(self.onSetButtonClicked)
        self.setButton.setFixedHeight(30)
        self.hlayout.addWidget(self.setButton)
        
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.onCancelButtonClicked)
        self.cancelButton.setFixedHeight(30)
        self.hlayout.addWidget(self.cancelButton)
        
        layout.addLayout(self.hlayout)
        
        self.move((parent.width()-self.width())//2, (parent.height()-self.height())//2)
        self.setLayout(layout)
        
        
    def onSetButtonClicked(self):
        newNameValue = self.textedit.toPlainText()
        newNameValue = newNameValue.strip()
        if newNameValue == "":
            QMessageBox().critical(self, "ERROR! FIELD EMPTY", f"{self.name} field cannot be empty value", QMessageBox().Ok)
            self.close()
            return
        else:
            self.update_settings_signal.emit(newNameValue)
            self.textedit.clear()
            self.close()
    
    def onCancelButtonClicked(self):
        self.close()
        return
        
# Widget to display input messages

class LW_items_MessageDetails(QWidget):
    edit_MessageDetails_clicked_signal = pyqtSignal(int)
    add_output_clicked_signal = pyqtSignal(object)
    def __init__(self, MessageIdentifier, MessageName, delay, periodicity):
        super().__init__()
        self.MessageId = MessageIdentifier
        layout_outer = QHBoxLayout(self)
        layout_outer.setContentsMargins(10,0,10,0)
        
        self.container = QWidget()
        self.container.setStyleSheet("""
                                QWidget{
                                    background-color: #f6f5f4;
                                    border: 2px solid #eeeeee;
                                }
                                QLabel{
                                    border: 0px;
                                    }
                                QLineEdit{
                                    border: 0px;
                                    }
                                """)
        self.layout = QHBoxLayout(self.container)
        
        self.selectorWidget = QWidget(self)
        self.selectorWidget.setStyleSheet("""
                                          border: 0px;
                                          """)
        self.selectorWidgetLayout = QHBoxLayout(self.selectorWidget)
        
        self.checkBox = QCheckBox(self.selectorWidget)
        self.selectorWidgetLayout.addWidget(self.checkBox)
        self.checkBox.setStyleSheet("""
                                      margin-right: 10px;
                                      """)
        self.indexLabel = QLabel(self.selectorWidget)
        self.selectorWidgetLayout.addWidget(self.indexLabel)
        self.indexLabel.setText(str(12))
        self.layout.addWidget(self.selectorWidget)
        
        
        self.labelLineEdit = QLineEdit(f"{MessageName}")
        self.labelLineEdit.setContentsMargins(12,0,12,0)
        self.layout.addWidget(self.labelLineEdit)
        self.labelLineEdit.setCursorPosition(0)
        self.labelLineEdit.setReadOnly(True)
        self.labelLineEdit.setFocusPolicy(Qt.NoFocus)
        self.labelLineEdit.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        self.miniInfo = miniInfoWidget(delay, periodicity, True)
        self.layout.addWidget(self.miniInfo)
        self.miniInfo.setFixedSize(80,40)
        
        self.buttonAddOutput = QPushButton("Open Output")
        self.buttonAddOutput.setFixedSize(120,40)
        self.buttonAddOutput.clicked.connect(self.onButtonAddOutputClicked)
        self.layout.addWidget(self.buttonAddOutput)
        self.buttonAddOutput.setStyleSheet("""
                                           QPushButton{
                                               background-color: #eeeeee;
                                               color: #000000;
                                               border: none;
                                               border-radius: 8px;
                                               padding 8px 16px;
                                           }
                                            QPushButton:hover{
                                                background-color: #424242;
                                                color: #f5f5f5;
                                            }
                                           """)
                                           
        self.buttonEditTestCases = QPushButton()
        self.buttonEditTestCases.setFixedSize(40,40)
        ui_ops.setSVG(self.buttonEditTestCases, "icons/actions/edit_file.svg", 30, 30)
        self.buttonEditTestCases.clicked.connect(self.onButtonEditClicked)
        self.buttonEditTestCases.setStyleSheet("""
                                               QPushButton{
                                                   border: 0px;
                                           
                                               }
                                               QPushButton:hover{
                                                   border-bottom: 5px solid #990000;
                                               }
                                           """)
        self.layout.addWidget(self.buttonEditTestCases)
        self.buttonEditTestCases.setToolTip(f"Edit Input Message")

        layout_outer.addWidget(self.container)
        
        self.setLayout(layout_outer)

    
    def updateIndex(self, index):
        self.indexLabel.setText(str(index))
        
    def updateLabel(self, labelText):
        self.labelLineEdit.setText(labelText)
        
    def onButtonEditClicked(self):
        print("clicked Edit: ",self.MessageId)
        self.edit_MessageDetails_clicked_signal.emit(self.MessageId)
    
    def onButtonAddOutputClicked(self):
        print("clicked send")
        self.add_output_clicked_signal.emit([self.MessageId, self.labelLineEdit.text()])
        
    def onButtonSetDelayClicked(self):
        delay = self.delayLineEdit.text()
        print("setting delay: ", delay)
        
    def getLabelName(self):
        return self.labelLineEdit.text()
    
    def isCheckboxChecked(self):
        if self.checkBox.isChecked():
            print("ckbox", True)
            return True
        else:
            print("ckbox", False)
            return False
        
    def setDelay(self, delayInms):
        self.miniInfo.setDelay(delayInms)
    
    def setPeriodicity(self, periodicityInms):
        self.miniInfo.setPeriodicity(periodicityInms)
        
    def toggleCheckBox(self, isSelected):
        if isSelected == False:
            self.checkBox.setChecked(True)
        if isSelected == True:
            self.checkBox.setChecked(False)
        
    def setUnsetCheckBox(self):
        if self.checkBox.isChecked():
            self.checkBox.setChecked(False)
        else:
            self.checkBox.setChecked(True)
            
            
# Widget to display output messages

class LW_items_Output_Message_widget(QWidget):
    edit_MessageDetails_clicked_signal = pyqtSignal(int)
    add_output_clicked_signal = pyqtSignal(str)
    def __init__(self, MessageIdentifier, MessageName, periodicity):
        super().__init__()
        self.MessageName = MessageName
        self.MessageId = MessageIdentifier
        layout_outer = QHBoxLayout(self)
        layout_outer.setContentsMargins(10,0,10,0)
        
        self.container = QWidget()
        self.container.setStyleSheet("""
                                QWidget{
                                    background-color: #f6f5f4;
                                    border: 2px solid #eeeeee;
                                }
                                QLabel{
                                    border: 0px;
                                    }
                                QLineEdit{
                                    border: 0px;
                                    }
                                """)
        self.layout = QHBoxLayout(self.container)
        
        self.selectorWidget = QWidget(self)
        self.selectorWidget.setStyleSheet("""
                                          border: 0px;
                                          """)
        self.selectorWidgetLayout = QHBoxLayout(self.selectorWidget)
        
        self.checkBox = QCheckBox(self.selectorWidget)
        self.selectorWidgetLayout.addWidget(self.checkBox)
        self.checkBox.setStyleSheet("""
                                      margin-right: 10px;
                                      """)
        self.indexLabel = QLabel(self.selectorWidget)
        self.selectorWidgetLayout.addWidget(self.indexLabel)
        self.indexLabel.setText(str(12))
        self.layout.addWidget(self.selectorWidget)
        

        
        if "IMAGE_PATH:" in MessageName:
            self.labelLineEdit = QLineEdit(f"IMAGE_PATH:{MessageName.split('/')[-1]}")
            self.labelLineEdit.setContentsMargins(12,0,12,0)
            self.layout.addWidget(self.labelLineEdit)
            self.labelLineEdit.setCursorPosition(0)
            self.labelLineEdit.setReadOnly(True)
            self.labelLineEdit.setFocusPolicy(Qt.NoFocus)
            self.labelLineEdit.setAttribute(Qt.WA_TransparentForMouseEvents, True)
            self.buttonPreview = QPushButton("preview")
            self.buttonPreview.setFixedSize(120,40)
            self.buttonPreview.clicked.connect(lambda: self.onButtonPreviewClicked(self.MessageName))
            self.layout.addWidget(self.buttonPreview)
            self.buttonPreview.setStyleSheet("""
                                               QPushButton{
                                                   background-color: #eeeeee;
                                                   color: #000000;
                                                   border: none;
                                                   border-radius: 8px;
                                                   padding 8px 16px;
                                               }
                                                QPushButton:hover{
                                                    background-color: #424242;
                                                    color: #f5f5f5;
                                                }
                                               """)
         
            self.layout.addWidget(self.buttonPreview)
            
        else:
            self.labelLineEdit = QLineEdit(MessageName)
            self.labelLineEdit.setContentsMargins(12,0,12,0)
            self.layout.addWidget(self.labelLineEdit)
            self.labelLineEdit.setCursorPosition(0)
            self.labelLineEdit.setReadOnly(True)
            self.labelLineEdit.setFocusPolicy(Qt.NoFocus)
            self.labelLineEdit.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        self.miniInfo = miniInfoWidget(-1, periodicity, False)
        self.layout.addWidget(self.miniInfo)
        self.miniInfo.setFixedSize(80,40)
        self.miniInfo.setStyleSheet("""
                                    border: 0px solid #eeeeee;
                                """)
        
        self.buttonEditTestCases = QPushButton()
        self.buttonEditTestCases.setFixedSize(40,40)
        ui_ops.setSVG(self.buttonEditTestCases, "icons/actions/edit_file.svg", 30, 30)
        self.buttonEditTestCases.clicked.connect(self.onButtonEditClicked)
        self.buttonEditTestCases.setStyleSheet("""
                                               QPushButton{
                                                   border: 0px;
                                           
                                               }
                                               QPushButton:hover{
                                                   border-bottom: 5px solid #990000;
                                               }
                                           """)
        self.layout.addWidget(self.buttonEditTestCases)
        self.buttonEditTestCases.setToolTip(f"Edit Output Message")
        
        
        layout_outer.addWidget(self.container)
        
        self.setLayout(layout_outer)
    
    def onButtonPreviewClicked(self, MessageName):
        self.image_path = MessageName.split("IMAGE_PATH:")[1]
        self.ImageViewerInstance = ImageViewer(self.image_path)
        self.ImageViewerInstance.show()
        
    def updateLabel(self, labelText):
        if "IMAGE_PATH:" in labelText:
            self.labelLineEdit.setText("IMAGE_PATH:"+labelText.split("/")[-1])
        else:
            self.labelLineEdit.setText(labelText)
        self.MessageName = labelText
            
    def updateIndex(self, index):
        self.indexLabel.setText(str(index))
        
    def onButtonEditClicked(self):
        print("clicked Edit: ",self.MessageId)
        self.edit_MessageDetails_clicked_signal.emit(int(self.MessageId))
        
    def getLabelName(self):
        return self.labelLineEdit.text()
    
    def isCheckboxChecked(self):
        if self.checkBox.isChecked():
            print("ckbox", True)
            return True
        else:
            print("ckbox", False)
            return False

    def toggleCheckBox(self, isSelected):
        if isSelected == False:
            self.checkBox.setChecked(True)
        if isSelected == True:
            self.checkBox.setChecked(False)

    def setPeriodicity(self, periodicityInms):
        self.miniInfo.setPeriodicity(periodicityInms)


    def setUnsetCheckBox(self):
        if self.checkBox.isChecked():
            self.checkBox.setChecked(False)
        else:
            self.checkBox.setChecked(True)

# Used in displaying periodicity and delay in input and output 
class miniInfoWidget(QWidget):
    def __init__(self, delay, periodicity, isInput):
        super().__init__()
        layout_outer = QHBoxLayout(self)
        layout_outer.setContentsMargins(0,0,0,0)
         
        self.miniInfoWidgetcontainer = QWidget()
        self.miniInfoWidgetcontainer.setFixedSize(70,40)
        self.miniInfoWidgetcontainer.setStyleSheet("""
                                        background-color: #ffffff;
                                        font-size: 10px;
                                        border-radius: 8px;
                                """)
        self.miniInfoWidgetlayout = QVBoxLayout(self.miniInfoWidgetcontainer)
        self.miniInfoWidgetlayout.setSpacing(2)

        
        # periodicty
        self.periodicityWidget = QWidget()
        self.periodicityWidgetLayout = QHBoxLayout(self.periodicityWidget)
        self.periodicityWidget.setStyleSheet("""
                                  border-radius: 0px;
                                  """)
        self.periodicityWidgetLayout.setSpacing(0)
        self.periodicityWidgetLayout.setContentsMargins(0,0,0,0)
        
        self.pLabel = QLabel()
        self.pLabel.setText("P")
        # self.pLabel.setFixedWidth(20)
        self.pLabel.setAlignment(Qt.AlignCenter)
        # self.pLabel.setStyleSheet("""
        #                           background-color: #ffffff;
        #                           padding: 3px;
        #                           """)
        self.periodicityWidgetLayout.addWidget(self.pLabel)
        
        self.periodicityLineEdit = QLineEdit()
        self.periodicityLineEdit.setReadOnly(True)
        self.periodicityLineEdit.setAlignment(Qt.AlignCenter)
        # self.periodicityLineEdit.setStyleSheet("""
        #                                  background-color: #ffffff;
        #                           """)
        self.periodicityWidgetLayout.addWidget(self.periodicityLineEdit)
        
        self.miniInfoWidgetlayout.addWidget(self.periodicityWidget)

        if isInput:
            # Delay
            self.delayWidget = QWidget()
            self.delayWidgetLayout = QHBoxLayout(self.delayWidget)
            self.delayWidget.setStyleSheet("""
                                      border-radius: 0px;
                                      """)
            self.delayWidgetLayout.setSpacing(0)
            self.delayWidgetLayout.setContentsMargins(0,0,0,0)
            
            self.dLabel = QLabel()
            self.dLabel.setText("D")
            # self.dLabel.setFixedWidth(20)
            self.dLabel.setAlignment(Qt.AlignCenter)
            # self.dLabel.setStyleSheet("""
            #                           background-color: #ffffff;
            #                           padding: 3px;
            #                           """)
            self.delayWidgetLayout.addWidget(self.dLabel)
            
            self.delayLineEdit = QLineEdit()
            self.delayLineEdit.setReadOnly(True)
            self.delayLineEdit.setAlignment(Qt.AlignCenter)
            # self.delayLineEdit.setStyleSheet("""
            #                                  background-color: #ffffff;
            #                           """)
            self.delayWidgetLayout.addWidget(self.delayLineEdit)
        
            self.miniInfoWidgetlayout.addWidget(self.delayWidget)
            layout_outer.addWidget(self.miniInfoWidgetcontainer)
            self.setLayout(layout_outer)
            self.setDelay(delay)
            self.setPeriodicity(periodicity)
        else:
            layout_outer.addWidget(self.miniInfoWidgetcontainer)
            self.setLayout(layout_outer)
            self.setPeriodicity(periodicity)
        


        
    def setDelay(self, delayInms):
        self.delayLineEdit.setText(str(delayInms))
    
    def setPeriodicity(self, periodicityInms):
        self.periodicityLineEdit.setText(str(periodicityInms))


# Dialog box for two inputs used in (add gui input button) 
class twoInputDialog(QDialog):
    def __init__(self, g_title, g_field1, g_field2, default_field1="", default_field2="", parent=None):
        super().__init__(parent)
        self.setWindowTitle(g_title)
        self.resize(600, 120)
        self.input1 = QLineEdit()
        self.input2 = QLineEdit()
        
        if default_field1!="":
            self.input1.setText(default_field1)
            self.input2.setText(str(default_field2))
        else:
            self.input1.setPlaceholderText(f"Enter {g_field1}")
            self.input2.setPlaceholderText(f"Enter {g_field2}")
        
        layout = QFormLayout()
        layout.addRow(f"{g_field1}:", self.input1)
        layout.addRow(f"{g_field2}:", self.input2)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        layout.addWidget(self.buttons)
        self.move((parent.width()-self.width())//2, (parent.height()-self.height())//2)
        self.setLayout(layout)
        
    def getInputs(self):
        if self.input1.text()=="" or self.input2.text()=="":
            print("Fields cannot be empty")
            return "" ""
        else:
            return self.input1.text(), int(self.input2.text())
    
    def setInputs(self, input1, input2):
        self.input1.setText(input1)
        self.input2.setText(str(int(input2)))
   
   
        
# Back button widget

class backButton(QWidget):
    back_clicked_signal = pyqtSignal()
    def __init__(self, isHome=False, parent=None):
        super().__init__(parent)
        layout_outer = QHBoxLayout(self)
        layout_outer.setContentsMargins(0,0,0,0)
        self.back_button = QPushButton("Back")
        
        if isHome:
            self.back_button = QPushButton("SNS")
            ui_ops.setSVG(self.back_button, "icons/actions/home.svg", 15, 15)
        else:
            self.back_button = QPushButton("Back")
            ui_ops.setSVG(self.back_button, "icons/actions/go-previous.svg", 15, 15)
            
        self.back_button.setMinimumSize(QSize(70, 16777215))
        self.back_button.setObjectName("back_button")
        self.back_button.setStyleSheet("""
                                            background-color: #eeeeee;
                                            border: 1px solid #eeeeee;
                                            font-size: 10px;
                                            font-weight: bold;
                                            padding: 5px 0px;
                                            color: #212121;
                                        """)
        layout_outer.addWidget(self.back_button)
        
        self.back_button.clicked.connect(self.backClicked)
        
    def backClicked(self):
        self.back_clicked_signal.emit()



# Widget used to Display the information regarding the page in SNS (function name, testcase name etc)

class snsInfoBar(QWidget):
    back_clicked_signal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
                              font-size: 11px;

                           """)
        self.setMaximumHeight(50)
        self.layout_outer = QHBoxLayout(self)
        self.layout_outer.setContentsMargins(0,10,0,10)
        self.layout_outer.setSpacing(0)
        self.leftWidget = QWidget(self)
        self.leftWidgetVLayout = QHBoxLayout(self.leftWidget)
        self.leftWidgetVLayout.setContentsMargins(0,0,0,0)
        self.leftWidgetVLayout.setSpacing(0)
        self.labelFunction = snsInfoBarlabelBoxes("TEST SUITE:", "")
        self.leftWidgetVLayout.addWidget(self.labelFunction)
        self.labelTestCase = snsInfoBarlabelBoxes("TESTCASE:", "")
        self.leftWidgetVLayout.addWidget(self.labelTestCase)

        self.layout_outer.addWidget(self.leftWidget)
        self.leftWidget.setStyleSheet("""
                                      QWidget{
                                          padding: 2px 20px 2px 20px;
                                          }
                                      """)
        
        self.rightWidget = QWidget(self)
        self.rightWidgetVLayout = QHBoxLayout(self.rightWidget)
        self.rightWidgetVLayout.setContentsMargins(0,0,0,0)
        self.rightWidgetVLayout.setSpacing(0)
        
        self.labelInput = snsInfoBarlabelBoxes("INPUT:", "")
        self.rightWidgetVLayout.addWidget(self.labelInput)
        self.labelOutput = snsInfoBarlabelBoxes("OUTPUT:", "")
        self.rightWidgetVLayout.addWidget(self.labelOutput)
        
        self.layout_outer.addWidget(self.rightWidget)
        self.rightWidget.setStyleSheet("""
                                      padding: 2px 10px 2px 10px;
                                      """)
        
    def setFunctionName(self, functionName):
        self.labelFunction.setValue(functionName)
        self.labelFunction.setToolTip(functionName)

    def setTestCaseName(self, testCaseName):
        self.labelTestCase.setValue(testCaseName)
        self.labelTestCase.setToolTip(testCaseName)

    def setInputName(self, inputName):
        self.labelInput.setValue(inputName)
        self.labelInput.setToolTip(inputName)

    def setOutputName(self, outputName):
        self.labelOutput.setValue(outputName)
        self.labelOutput.setToolTip(outputName)

        
     

class snsInfoBarlabelBoxes(QWidget):
    back_clicked_signal = pyqtSignal()
    def __init__(self, labeler, value, parent=None):
        super().__init__(parent)
        
        label_font = QFont("Courier New", 11, QFont.Bold)
        value_font = QFont("Courier New", 11)
        value_font.setItalic(True)
        # self.setStyleSheet("""
        #                    border: 1px solid grey;
        #                    """)
        self.layout_outer = QHBoxLayout(self)
        self.layout_outer.setContentsMargins(0,0,0,0)
        self.layout_outer.setSpacing(0)
        self.label = QLabel(labeler)
        self.label.setFont(label_font)
        self.label.setStyleSheet("""
                                  padding: 0px;
                                  padding-left: 10px;
                                  margin: 0px;
                                  color: #954535;
                              
                                  """)
        self.label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # self.label.setMaximumWidth(70)
        # self.label.setMinimumWidth(70)
        self.layout_outer.addWidget(self.label)
        self.labelValue = QLabel(value)
        self.labelValue.setMinimumWidth(100)
        self.labelValue.setMaximumWidth(600)
        self.labelValue.setFont(value_font)
        self.labelValue.setStyleSheet("""
                                  padding: 0px;
                                  margin: 0px;
                       
                                  """)
        self.layout_outer.addWidget(self.labelValue)   
    
    def setValue(self, value):
        self.labelValue.setText(str(value))
        
class ElidedLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setWordWrap(False)
        self.setMaximumWidth(1000)
        # self.setAlignment(Qt.AlignCenter)
        
        def resizeEvent(self, event):
            fm = QFontMetrics(self.font())
            elided = fm.elidedText(self.full_text, Qt.ElideRight, self.width()-10)
            self.setText(elided)
            super().resizeEvent(event)


# Used to previed image where there is auto GUI testing
class ImageViewer(QWidget):
    def __init__(self, image_path):
        super().__init__()
        image_path = CWD+image_path
        self.setWindowFlags(Qt.Dialog | Qt.Window)
        self.setWindowTitle(f"Image Preview")
        
        layout = QVBoxLayout()
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setSizePolicy(QSizePolicy().Expanding, QSizePolicy().Expanding)
        self.label.setMinimumSize(1,1)
        
        print("IMage Pagth ->>>>>>", image_path)
        self.orignal_pixmap = QPixmap(image_path)
        # scaled_pixmap = pixmap.scaled(280, 280, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(self.orignal_pixmap)
        
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.resize(400,400)
    def __del__(self):
        print("Widget destroyed, Image viewer")
    def resizeEvent(self, event):
        if not self.orignal_pixmap.isNull():
            scaled_pixmap = self.orignal_pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(scaled_pixmap)
        super().resizeEvent(event)



 # Dialog box for user confirmation(add gui input button)    
class confirmDialog(QDialog):
    def __init__(self, g_title, g_field1, parent=None):
        super().__init__(parent)
        self.setWindowTitle(g_title)
        self.resize(600, 120)
        self.Label = QLabel()
        layout = QFormLayout()
        layout.addRow(f"{g_field1}:", self.Label)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        layout.addWidget(self.buttons)
        self.setLayout(layout)
        
    def updatelabel(self, labelData):
        self.Label.clear()
        self.Label.setText(labelData)



 # Dialog box for user confirmation(add gui input button)  
class savingDialog(QWidget):
    close_save_signal = pyqtSignal(int)
    def __init__(self, g_title, g_field1, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.Dialog | Qt.Window)
        self.setGeometry(100,100,200,100)
        self.setWindowTitle(g_title)
        # self.setSizeGripEnabled(True)
        
        layout = QVBoxLayout()
        
        self.Label = QLabel(g_field1)
        layout.addWidget(self.Label)
        
        self.hlayout = QHBoxLayout()
        self.hlayout.addStretch()
        self.setButton = QPushButton("OK")
        self.setButton.clicked.connect(self.onSetButtonClicked)
        self.setButton.setFixedSize(30, 30)
        self.hlayout.addWidget(self.setButton)
        self.setButton.hide()
        
        layout.addLayout(self.hlayout)
        
        self.move((parent.width()-self.width())//2, (parent.height()-self.height())//2)
        self.setLayout(layout)
        
        
    def updateLabel(self, labelData):
        print("label data", labelData)
        self.Label.setText(labelData)
        self.setButton.show()
        
    
    def onSetButtonClicked(self):
        self.close()
    

class errorDisplay(QWidget):
    def show(parent, errorMessage):
        QMessageBox().critical(parent, "Error!", errorMessage, QMessageBox().Ok)