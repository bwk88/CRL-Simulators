#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 12:37:28 2024

@author: root
"""
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget, QHBoxLayout
from Configuration import config

class UserInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Port Input Dialog')
        self.layout = QVBoxLayout()
        
        self.labelReceivePort = QLabel('Receive Port:')
        self.layout.addWidget(self.labelReceivePort)
        self.lineEditReceivePort = QLineEdit()
        self.lineEditReceivePort.setText(config.sock_rcv_port)
        self.layout.addWidget(self.lineEditReceivePort)
        
        self.labelSendPort = QLabel('Send Port:')
        self.layout.addWidget(self.labelSendPort)
        self.lineEditSendPort = QLineEdit()
        self.lineEditSendPort.setText(config.sock_send_port)
        self.layout.addWidget(self.lineEditSendPort)
        
        self.labelSendIp = QLabel('Send IP:')
        self.layout.addWidget(self.labelSendIp)
        self.lineEditSendIp = QLineEdit()
        self.lineEditSendIp.setText(config.sock_send_ip)
        self.layout.addWidget(self.lineEditSendIp)
        
        self.pushButtonSubmit = QPushButton('Submit')
        self.pushButtonSubmit.clicked.connect(self.process_input)
        self.layout.addWidget(self.pushButtonSubmit)
        
        self.pushButtonCancel = QPushButton('Cancel')
        self.pushButtonCancel.clicked.connect(self.process_cancel)
        self.layout.addWidget(self.pushButtonCancel)
        
        self.setLayout(self.layout)
        
    def process_input(self):
        rcv_port = self.lineEditReceivePort.text()
        snd_port = self.lineEditSendPort.text()
        snd_ip = self.lineEditSendIp.text()
        
        if rcv_port and snd_port and snd_ip:
            try:
                self.receive_port = int(rcv_port)
                self.send_port = int(snd_port)
                self.send_ip = snd_ip
                self.receive_port = rcv_port
                self.send_port = snd_port
                self.accept()
            except Exception as e:
                self.show_error_message(str(e))
        else:  
            self.show_error_message('Fill in all fields.')    
            
    def process_cancel(self):
        self.reject()          
    
    def show_error_message(self, error_message):     
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Error In Input')
        msg.setInformativeText(error_message)
        msg.setWindowTitle('Error')
        msg.exec_()
        
    def get_data(self):
        return self.receive_port, self.send_port, self.send_ip
                
        
