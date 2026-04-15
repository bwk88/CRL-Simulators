from Configuration import config
import struct
import crc_calulator
from PyQt5 import QtCore, QtGui, QtWidgets
from Configuration import config


def getMsgListFromMsgTuple(msgTuple):
    msgList = []
    for x in range(len(msgTuple)):
        msgList.append(msgTuple[x])
    return msgList

def send_and_log_message_and_update_gui(self, form, content_list):
    print("-------",form, content_list)
    try:
        packet = struct.pack(f'={form}', *tuple(content_list))
    except Exception as e:
        print("PACKET UNPACK ERROR",e)
    self.sender.send_packet(packet)

def send_selected(self,datastore,ip,port):
    print("SENDDDDDDDDDDDDDDDDDd",ip.text(),port.text())
    
    config.sock_send_ip = ip.text()
    config.sock_send_port = port.text()
    print("selcted ROW",self.tableView.selectionModel().selectedIndexes())
    # print("FINAL FORMAT",config.final_format)
    selected_indexes = self.tableView.selectionModel().selectedIndexes()
    content_format = ''
    content_list = ''
    observation_str = ''

    try:
        data_row = 0
        for index in selected_indexes:
            row = index.row()
            data_row = row
            row_data = []
            for column in range(datastore.model.columnCount()):
                item = datastore.model.item(row, column)
                if item:
                    if(column == 9):
                        content_format = item.text()
                        print(item.text())
                    if(column == 6):
                        content_list = item.text()
                    if(column == 5):
                        observation_str = item.text()
                    if(column == 7):
                        data = item.text()
                        # for val in item.text():
                        #     print("VALL",val)
        
        # content_format = row_data[7]            
        format_list = content_format.split(' ')
        content_list = []
        parsed_data = self.data_index[data_row]
        # print("PARSED ",parsed_data)
        
        for x in range(0,len(parsed_data)):
            if(isinstance(parsed_data[x], bytes)):
                string = parsed_data[x].decode('utf-8').rstrip('\x00')
                content_list.append(string)
            else:
                content_list.append(parsed_data[x])
                
        value_list = []
        # print("CL",content_list)
    
        for i,value in enumerate(content_list):
            # value = lineEdit.text()
            if 's' in format_list[i]:
                value = bytes(value, 'utf-8')
            elif value == '' or value == ' ':
                # print('empty value')
                value = 0
            elif value == 'auto':
                value = 'auto'    
            else: 
                value = int(value)    
            value_list.append( value )
    except Exception as e:
        print("Error in search tab",e)
        
    # print("VALUE LIST",value_list)
    
    if('RCVD OK' in observation_str):
        send_and_log_message_and_update_gui(self,content_format,value_list)
    else:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText('Error In Sending')
        msg.setInformativeText('Select Correct Format Packet')
        msg.setWindowTitle('Error')
        msg.exec_()