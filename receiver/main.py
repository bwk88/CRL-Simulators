#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
"""
Created on Fri Feb  9 19:12:09 2024

@author: root
"""
from mainwindow import Ui_MainWindow 
import threading
from PyQt5 import QtWidgets
import udpreceiver
# import udp_multicast_receiver
from Configuration import config

def receiver():
    udpreceiver.rcvr.startReceiving()
    
# def multicast_receiver():
#     udp_multicast_receiver.rcvr.startReceiving()    
    
class Threads:
    def __init__(self):
        pass
    def threads_launch(self):
        t2 = threading.Thread(target=receiver) 
        t2.start()
        
        # t3 = threading.Thread(target=multicast_receiver) 
        # t3.start()
        
threads = Threads() 

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 3:
        rcv_port = str(sys.argv[1])
        config.sock_rcv_port = rcv_port
        send_port = str(sys.argv[2])
        config.sock_send_port = send_port
        send_ip = str(sys.argv[3])
        config.sock_send_ip = send_ip
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    config.set_display(ui)
    
    threads.threads_launch()
    sys.exit(app.exec_())
