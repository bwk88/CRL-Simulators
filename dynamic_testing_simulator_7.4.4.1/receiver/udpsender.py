import socket
from Configuration import config
from PyQt5 import QtCore, QtGui, QtWidgets

class UdpSender:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.multicast_send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.multicast_send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def send_packet(self, packet):
        print("SENDING---------------")
        if config.comm_types_dictionary[config.message_selected] == 'M':
            print('Going to multicast')
            multicast_port = int(config.sock_multicast_send_port)
            multicast_group = config.sock_multicast_group
            address = (multicast_group, multicast_port)
            # packedMsg = struct.pack('=BBHB IhBBB100s',3,3,18,0,3,1031,40,1,1,b'SOW')
            self.multicast_send_sock.sendto(packet, address)
            print('Multicast sent to Group',multicast_group, ': Port',multicast_port)
        else:    
            try:
                self.sock.sendto(packet, (config.sock_send_ip, int(config.sock_send_port)))
            except Exception as e:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText('Error In Sending')
                msg.setInformativeText(str(e))
                msg.setWindowTitle('Error')
                msg.exec_()
            
            print("Packet sent to ",config.sock_send_ip,config.sock_send_port)
        