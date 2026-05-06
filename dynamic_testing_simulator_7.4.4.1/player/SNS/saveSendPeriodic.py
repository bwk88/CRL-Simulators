from PyQt5 import QtCore, QtGui, QtWidgets
import time
import struct, threading
from Configuration import config
import socket, math
import datetime 
import crc_calulator


CRC_START_32 = 0xFFFFFFFF
CRC_POLY_32 = 0x82608EDB
crc_tab32_init = False
GLOBAL_DELAY = 0

class saveSendPeriodic(QtWidgets.QWidget):
    periodic_message_selector_signal = QtCore.pyqtSignal(int, str, str, bool)
    error_signal = QtCore.pyqtSignal(str)
    periodic_message_list = []
    stop_event_list = []
    threads = []
    sending_index_list = []
    senderIpPortList = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    multicast_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    multicast_send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    def __init__(self):
        super().__init__()
        print('periodic sender', id(self))
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.addbutton = QtWidgets.QPushButton('Add message')
        self.layout.addWidget(self.addbutton, alignment = QtCore.Qt.AlignLeft)
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        
        self.row_widget = QtWidgets.QWidget()
        self.scroll_area_layout = QtWidgets.QVBoxLayout(self.row_widget)
        self.scroll_area_layout.setContentsMargins(8,4,8,4)
        self.scroll_area_layout.setAlignment(QtCore.Qt.AlignTop)
        #self.layout.addStretch()
        self.scroll_area.setWidget(self.row_widget)
        self.setLayout(self.layout)
        self.addbutton.clicked.connect(self.addMessageFunction)
        self.layout.addWidget(self.scroll_area)

    def addMessageFunction(self):
        self.periodic_message_selector_signal.emit(1, 'sender', 'periodic_sender', True)
        
    def addRow(self, text, Ip, port, periodicity):
        row_content = QtWidgets.QWidget()
        row_content.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        row_content.setFixedHeight(40)
        row_content.setStyleSheet("""
                                  QtWidgets.QWidget{
                                      background-color: lightblue;
                                      border: 1px solid #b0b0b0;
                                      border-radius: 4px;
                                      }
                                """)
        row_widget_layout = QtWidgets.QHBoxLayout(row_content)
     
        row_name = QtWidgets.QLabel(text)
        row_name.setAlignment(QtCore.Qt.AlignLeft)
        
        setIP = QtWidgets.QLabel("IP")
        setIP.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                 QtWidgets.QSizePolicy.Fixed)
        
        setIP_lineEdit = QtWidgets.QLineEdit()
        setIP_lineEdit.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                 QtWidgets.QSizePolicy.Fixed)
        setIP_lineEdit.setText(Ip)
        setPort = QtWidgets.QLabel("Port")
        setPort.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                 QtWidgets.QSizePolicy.Fixed)
        # setIpPortButton = QtWidgets.QPushButton("Set IP/Port")
        # setIpPortButton.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
        #                          QtWidgets.QSizePolicy.Fixed)
        # setIpPortButton.clicked.connect(lambda:self.setIpandPort(setIP_lineEdit.text(), setIP_lineEdit.text()))
        setPort_lineEdit = QtWidgets.QLineEdit()
        setPort_lineEdit.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                 QtWidgets.QSizePolicy.Fixed)
        setPort_lineEdit.setText(port)
        
        setPeriodicValue = QtWidgets.QLabel("Periodicity")
        setPeriodicValue.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                 QtWidgets.QSizePolicy.Fixed)
        setPeriodicValue_lineEdit = QtWidgets.QLineEdit()
        setPeriodicValue_lineEdit.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                 QtWidgets.QSizePolicy.Fixed)
        setPeriodicValue_lineEdit.setText(str(periodicity))
        
        row_send = QtWidgets.QPushButton('Send')
        row_send.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                 QtWidgets.QSizePolicy.Fixed)
        row_send.setCheckable(True)
        row_send.toggled.connect(lambda checked:self.send_clicked(checked, setIP_lineEdit.text(), setPort_lineEdit.text(), setPeriodicValue_lineEdit.text()))
        row_delete = QtWidgets.QPushButton('Delete')
        row_delete.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                                 QtWidgets.QSizePolicy.Fixed)
        row_delete.clicked.connect(lambda:self.delete_periodic_message(setIP_lineEdit.text(), setPort_lineEdit.text(), setPeriodicValue_lineEdit.text()))
        row_widget_layout.addWidget(row_name)
        row_widget_layout.addWidget(setIP)
        row_widget_layout.addWidget(setIP_lineEdit)
        row_widget_layout.addWidget(setPort)
        row_widget_layout.addWidget(setPort_lineEdit)
        row_widget_layout.addWidget(setPeriodicValue)
        row_widget_layout.addWidget(setPeriodicValue_lineEdit)
        # row_widget_layout.addWidget(setIpPortButton)          
        row_widget_layout.addWidget(row_send)
        row_widget_layout.addWidget(row_delete)
        self.scroll_area_layout.addWidget(row_content)
        self.stop_event_list.append(threading.Event())
    


    def send_clicked(self, checked, Ip, Port, periodicty):
        button = self.sender()
        row = button
        while row is not None and row.parent() != self.scroll_area.widget():
            row = row.parent()
        index = self.scroll_area.widget().layout().indexOf(row)
        
        try:
            self.periodic_message_list[index][5] = int(periodicty)
        except Exception as e:
            print(e)
        
        if checked:
            #print("lsl", self.periodic_message_list)
            
            self.sender().setText('Stop')
            self.stop_event_list[index].clear()
            self.sending_index_list.append(index)
            if index < len(self.senderIpPortList):
                self.senderIpPortList[index] = [Ip, Port]
            else:
                self.senderIpPortList.append([Ip, Port])
            t = threading.Thread(target=self.periodic_message_sender, args=(index, Ip, Port, ))
            t.start()
            self.threads.append(t)
            print("lsls")
            
        else:
            #print("lsl", self.periodic_message_list)
            print('ksll')
            self.sender().setText('Send')
            self.stop_event_list[index].set()
            self.sending_index_list.remove(index)
            #self.senderIpPortList.pop(index)

        
        
            
    def delete_periodic_message(self, Ip, Port, periodicity):
        layout = self.scroll_area.widget().layout()
        button = self.sender()
        row = button
        while row is not None and row.parent() != self.scroll_area.widget():
            row = row.parent()
        index = layout.indexOf(row)

        for i in self.stop_event_list:
            i.set()
        for i in self.threads:
            i.join()

        self.stop_event_list = []
        self.threads = []
        self.periodic_message_list.pop(index)
        if index in self.sending_index_list:
            self.sending_index_list.remove(index)
            self.senderIpPortList.pop(index)
        for i in range(len(self.sending_index_list)):
            if self.sending_index_list[i] > index:
                self.sending_index_list[i] -=1
            
                

        
        item = layout.takeAt(index)
        widget = item.widget()
        if widget:
            widget.deleteLater()
        for i in self.senderIpPortList:
            self.stop_event_list.append(threading.Event())
        for i in self.sending_index_list:
            t = threading.Thread(target=self.periodic_message_sender, args=(i, self.senderIpPortList[i][0], self.senderIpPortList[i][1], ))
            t.start()
            self.threads.append(t)
            
            


            
            
            
    def periodic_message_sender(self, index, Ip, Port):
        while not self.stop_event_list[index].is_set():
            # print('Sending--=-', self.periodic_message_list[index][0])
            #header_list = self.get_header_list(self.periodic_message_list[index][3])
            header_list = self.periodic_message_list[index][3]
            content_list = self.periodic_message_list[index][4]
            content_format = self.periodic_message_list[index][2]
            # crcPack = struct.pack(f'={self.periodic_message_list[index][1]} {content_format}', *tuple(header_list), *tuple(content_list)) # for CRC on header
            # # crcPack = struct.pack(f'= {content_format}', *tuple(content_list))
            # crc_data = crc_calulator.crc_32(crcPack)
            # content_list[-1] = crc_data
            # content_format = content_format
            # print(content_format)
            packet = struct.pack(f'={self.periodic_message_list[index][1]}{content_format}', *tuple(header_list), *tuple(content_list))
            try:
                self.send_packet(packet, Ip, Port, index)
            except Exception as e:
                self.error_signal.emit(str(e))
                item = self.scroll_area.widget().layout().itemAt(index)
                button = item.widget().findChild(QtWidgets.QPushButton)
     
                button.setChecked(False)
                # if button.text() == "Stop":
                #     button.setText("Send")
                #self.stop_event_list[index].set()
                # item = self.scroll_area.widget().layout().itemAt(index)
                # button = item.widget().findChild(QtWidgets.QPushButton)
                # if button.text() == "Stop":
                #     button.setText("Send")
                #     
                #     self.sending_index_list.remove(index)
                print('abc')
            time.sleep(self.periodic_message_list[index][5]/1000)
    # def setIpandPort(self, Ip, Port):
    #     config.sock_send_ip = Ip
    #     config.sock_send_port = Port
    
    def get_header_list(self, header_list): 
        datetime_now = datetime.datetime.now()
        header_list[8]  = datetime_now.day
        header_list[9]  = datetime_now.month
  	       # header_list[9] = 10
        header_list[10] = datetime_now.year
        header_list[11] = datetime_now.hour
        header_list[12] = datetime_now.minute
        header_list[13] = datetime_now.second
        header_list[14] = math.floor(datetime_now.microsecond / 1000)
        
        return header_list
        
        
        
    def send_packet(self, packet, Ip, Port, index):
        if config.comm_types_dictionary[self.periodic_message_list[index][0]] == 'M':
            # print('Going to multicast')
            # multicast_port = int(config.sock_multicast_send_port)
            # multicast_group = config.sock_multicast_group
            print(f"{self.periodic_message_list[index][0]} multicast sent to ",Ip,Port, self.periodic_message_list[index][5])
            address = (Ip, int(Port))
            # packedMsg = struct.pack('=BBHB IhBBB100s',3,3,18,0,3,1031,40,1,1,b'SOW')
            self.multicast_send_sock.sendto(packet, address)
            ##print('Multicast sent to Group',multicast_group, ': Port',multicast_port)
        else:
            print(f"{self.periodic_message_list[index][0]} unicast sent to ",Ip,Port, self.periodic_message_list[index][5])
            self.sock.sendto(packet, (Ip, int(Port)))
            


        
        

