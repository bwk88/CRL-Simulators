from Configuration import config
import struct
import crc_calulator
from PyQt5 import QtCore, QtGui, QtWidgets

def getStringifiedMsgList(input_list):
    msg_list = []
    for x in range(len(input_list)):
        if(isinstance(input_list[x], bytes)):
            string = input_list[x].decode('utf-8').rstrip('\x00')
            msg_list.append(string)
        else:   
            msg_list.append(input_list[x])
    return msg_list

def send_and_log_message_and_update_gui(self, form, content_list):
    #if config.message_selected == "PSD_RATC_INFO_MSG":
    #    print(">>>>>>>>>>>>>>", form, header_list, content_list)
    #    form = "BBBHBIII"
    #    packet = struct.pack(f'={form}', *tuple(content_list))
    #else:
    print("-------",form,content_list)
    packet = struct.pack(f'={form}', *tuple(content_list))
    self.sender.send_packet(packet)

    if config.name_to_header_type[config.message_selected] != 'external':
        print("================================")
        
        # header_str = ' '.join(map(str,header_list))
        content_str = ' '.join(map(str, getStringifiedMsgList(content_list)))
        # self.update_header(header_str) 
        update_content(self,content_str) 
        config.log(f'{config.message_selected}{content_str}')
    return



def calculateByte(non_standard_bits_values, non_standard_bits_sizes):
    if sum(non_standard_bits_sizes) != 8:
        raise ValueError('Total bit size must be 8')
    packed_byte = 0
    current_bit_index = 8
    
    for number, size in zip(reversed(non_standard_bits_values), reversed(non_standard_bits_sizes)):
        if number >= (1 << size):
            raise ValueError(f'Number {number} exceeds maximum value for bit size {size}')
        current_bit_index -= size
        packed_byte |= (number << current_bit_index)
    return packed_byte


def send_clicked(self,ui):
    print("From Send Clicked File")
    # try:
    self.set_IP_and_socket()
    header_format = config.header_dictionary[config.message_selected]
    content_format_list = config.modified_content_dictionary[config.message_selected] 
    content_format = ' '.join(map(str,content_format_list[:]))
    if(content_format == 'not' or content_format == ' '):
        content_format = ''
    crc_format = config.crc_dictionary[config.message_selected]
    if(crc_format == 'not'  or crc_format == ' '):
        crc_format = ''
    print('header_format:', header_format, ', content_format:', content_format, ', crc_format:',crc_format)    
    bits_format = config.bits_dictionary[config.message_selected]
    header_list = []
    content_list = []
    crc_data = 0
    print("BITS FMT",bits_format)
    
    if bits_format == 'cbi_ratc_indication_bits' or bits_format == 'ratc_cbi_indication_bits':
        header_list = header_list + self.get_header_list()
        max_byte_number, records_list = self.get_num_records_and_records_list()
        content_list.append(max_byte_number)
        content_list = content_list + records_list
        print("content formats", content_format)
        crcPack = struct.pack(f'={header_format} {content_format}', *tuple(header_list), *tuple(content_list)) #for CRC on header
        #crcPack = struct.pack(f'= {content_format}', *tuple(content_list))
        crc_data = crc_calulator.crc_32(crcPack)
        content_list.append(crc_data)
        print("________________________________________",content_list)
        print("max_byte_number: ", max_byte_number)
        print("size of record: ", len(records_list))
        self.send_and_log_message_and_update_gui(content_format, content_list)
        
    elif bits_format == 'bytes':

        # temp_hdr_list = self.get_header_list()
        # print("hdr lst",temp_hdr_list)
        
        header_list = header_list 

        value_list = []
        format_list = config.content_dictionary[config.message_selected]
        format_list = self.dynamic_contentFormat
        print("LENNNN",len(self.listLineEdits))
        
        for i,lineEdit in enumerate(self.listLineEdits):
            value = lineEdit.text()
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
            
        print("VALUE LIST",value_list)
        # sizeForByte = 0
        # modified_value_list = []
        # non_standard_bits_values = []
        # non_standard_bits_sizes = []
        # bit_length_list = config.bits_list_dictionary[config.message_selected]
        # print("bit_length_list",bit_length_list)
        # for y,b in enumerate(bit_length_list):
        #     print('b = ', b)
        #     if b >= 8 :
        #         modified_value_list.append(value_list[y])
        #     else:
        #         sizeForByte = sizeForByte + b
        #         non_standard_bits_values.append(value_list[y])
        #         non_standard_bits_sizes.append(b)
        #         if sizeForByte == 8:
        #             # print('byte complete......')
        #             sizeForByte = 0
        #             byteValue = calculateByte(non_standard_bits_values, non_standard_bits_sizes)
        #             # print('byte = ',byteValue, 'bits:',bin(byteValue))
        #             modified_value_list.append(byteValue)
        #             non_standard_bits_values.clear()
        #             non_standard_bits_sizes.clear()
        # print('selected_byte_msg_formats: ', self.selected_byte_msg_formats)             
        # print('modified_selected_byte_msg_formats: ', self.modified_selected_byte_msg_formats)            
        # print('modified_value_list = ',modified_value_list)
        # # print('modified_content_format : ',modified_content_format)
        content_list = value_list[:]
    
            
        
        # print('header_format : ',header_format,crc_format)
        # print('content_format : ',content_format)
        # print('header_list : ',header_list)
        # print('content_list : ',content_list)
        # content_list.append(3)
        # content_list = 
        
        print("Dynamic Content Format List :",len(self.dynamic_contentFormat))
        
        content_format = ' '.join(map(str,self.dynamic_contentFormat))
        send_and_log_message_and_update_gui(self,content_format, content_list)
    # except Exception as e:
        # self.stop_periodic_sending_if_on()
        # show_error_message(str(e))
        
def show_error_message(error_message):     
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText('Error In Sending')
    msg.setInformativeText(error_message)
    msg.setWindowTitle('Error')
    msg.exec_()
    
def update_content(self,content):
    # self.lineEditContent.setText(content)
    self.ui.plainTextEditContent.setPlainText(content)