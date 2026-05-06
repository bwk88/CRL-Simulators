
"""
Created on Fri Feb  9 19:12:09 2024

unset GTK_PATH

@author: root
"""
from mainwindow import Ui_MainWindow 
import threading
from PyQt5 import QtWidgets
import udpreceiver
from Configuration import config
import sys
from SNS.saveSendPeriodic import saveSendPeriodic

def receiver():
    udpreceiver.rcvr.startReceiving()
    
class Threads:
    def __init__(self):
        pass
    def threads_launch(self):
        t2 = threading.Thread(target=receiver) 
        t2.start()
        
threads = Threads()


def closedThreads():
    for i in saveSendPeriodic.stop_event_list:
        i.set()
    for i in saveSendPeriodic.threads:
        i.join()
      
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    config.set_display(ui)  
    threads.threads_launch()
    sys.exit(app.exec_())