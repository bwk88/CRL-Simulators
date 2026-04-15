import pandas as pd
import xml.etree.ElementTree as ET
import logging
# from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

tree = ET.parse('config/configuration.xml')
root = tree.getroot()
from pandas import DataFrame
from csv_dict import dict

class Configuration:
    __instance = None
         
    def __init__(self):
        self.sock_multicast_group = root.find('sock_multicast_group').text
        self.sock_multicast_send_port = root.find('sock_multicast_send_port').text
        self.sock_multicast_rcv_port = root.find('sock_multicast_rcv_port').text
        self.sock_send_ip = root.find('sock_send_ip').text
        self.sock_send_port = root.find('sock_send_port').text
        self.sock_rcv_port = root.find('sock_rcv_port').text
        print("--------------->",root, self.sock_multicast_group)
        
        self.live_max_samples_all = int(root.find('live_max_samples_all').text)
        self.live_max_samples_selected = int(root.find('live_max_samples_selected').text)

        # self.cbi_ratc_indication_bit_names = self.read_cbi_ratc_indication_bit_names()
        # self.ratc_cbi_indication_bit_names = self.read_ratc_cbi_indication_bit_names()
        logging.basicConfig(filename="sent_sim.log", format='%(asctime)s %(message)s', filemode='a')
        # self.logger.format ='%(asctime)s %(message)s'
        self.logger = logging.getLogger()
        handler = TimedRotatingFileHandler("logs/rcv.log", when = 'M', interval = 1, backupCount=120)
        handler.setLevel(logging.DEBUG)
        handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
        self.logger.addHandler(handler)

        # self.logger.filemode = 'a'
        self.logger.setLevel(logging.DEBUG)
        self.keepRunning = True
        self.isReceiving = False
        self.display = None
        self.read_messages()
        self.complete_data = ''
        self.msg_names = []
        self.msg_ids = []
        self.content_formats = []
        self.header_formats = []
        self.crc_formats = []
        self.header_values = []
        self.comm_types = []
        self.msg_bits = []
        self.message_id_index = 5
        self.message_len_index = 6
        self.src_id_index = 0
        self.dest_id_index = 1
        
        self.dictionary_msg = self.src_id_dictionary
        
        self.id_dictionary = {}
        self.header_dictionary = {}
        self.crc_dictionary = {}
        self.content_dictionary = {}
        
        self.dynamic_label_lsit = []
        self.graph_plot_data = []
        
        self.dynamic_header_format = []
        # self.final_format = ''
        
        self.modified_content_dictionary = {}
        self.bits_list_dictionary = {}
        self.labels_list_dictionary = {}
        self.labels_struct_list_dictionary={}
        self.name_to_header_type = {}
        self.header_types = []
        
        self.bits_dictionary = {}
        self.header_values_dictionary = {}
        self.comm_types_dictionary = {}
        self.saved_msg_names = []
        self.saved_msg_formats = []
        self.saved_msg_contents = []
        self.read_messages()
        self.message_selected = self.msg_names[0] #combo box selecetd messages
        self.read_saved_messages()
        self.udpate_bytes_format_considering_bits()
     
        
        #Rigzin 24/12/2024 Adding new datatype to store the header_str and content_str as dictionary where key is message_name
        self.header_str = {}
        self.content_str = {}
        self.fields_list = {}
        self.set_bit_list = {}
        self.set_bit_list_msg_id = 0
        self.selected_message_status_on_receiver = 0
        #End
        
        #self.header_str = ''
        #self.content_str = ''
        #self.fields_list = []

        self.message_selected_multi_samples = 'None' 
        self.mode = 'live'#live / replay
        # self.header_labels = ["src_node","src_app", "index", "dest_node", "dest_app", "msg_id", "msg_len", "msg_seq","Year","Month","Date","hr","min","sec","ms","uniq_code"]
        self.header_labels = {}
        # self.read_header_labels()

    def read_saved_messages(self):
        self.saved_msg_names.clear()
        self.saved_msg_formats.clear()
        self.saved_msg_contents.clear()
        df_saved_msgs = pd.read_excel("config/saved_messages.xlsx")
        
        for saved_msg_name in df_saved_msgs['Name']:
            self.saved_msg_names.append(saved_msg_name)   

        for saved_msg_format in df_saved_msgs['Format']:
            self.saved_msg_formats.append(saved_msg_format) 

        for saved_msg_content in df_saved_msgs['Content']:
            self.saved_msg_contents.append(saved_msg_content) 
            
    
    def write_saved_messages(self, name, form, content):
        print('name:', name, ' form:', form, ' content:', content)
        self.saved_msg_names.append(name)  
        self.saved_msg_formats.append(form)  
        self.saved_msg_contents.append(content)  
        write_df = DataFrame({'Name':self.saved_msg_names, 'Format':self.saved_msg_formats, 'Content':self.saved_msg_contents })
        write_df.to_excel('config/saved_messages.xlsx', sheet_name= 'saved_messages', index=False)


    def read_header_labels(self):
        df = pd.read_excel("config/sim_config.xlsx", "header")
        self.header_labels["Internal"] = df["Internal"].dropna()
        self.header_labels["External"] = df["External"].dropna()
        # print("Header :::::::::::::::::: Internal \n",self.header_labels["Internal"] )
        # print("Header :::::::::::::::::: External \n",self.header_labels["External"]  )          
        
    def read_messages(self):
        df = pd.read_excel("config/sim_config.xlsx", "messages")
        
        header_types = []
        for header_type in df['header_type']:
            header_types.append(header_type)
        
        msg_names = []
        for msg_name in df['message']:
            msg_names.append(msg_name)   
        print("MSG NAMES",msg_names)    
        
        
        msg_ids = []
        for msg_id in df['id']:
            msg_ids.append(msg_id)
            
        content_formats = []
        for content_format in df['content_format']:
            content_formats.append(content_format)
        
        header_formats = []
        for header_format in df['header_format']:
            header_formats.append(header_format) 
        
        crc_formats = []
        for crc_format in df['crc_format']:
            crc_formats.append(crc_format)     
            
        msg_bits = []
        for bit in df['bits']:
            msg_bits.append(bit)
            
        header_values = []
        for header_value in df['header_values']:
            header_values.append(header_value)
            
        comm_types = []
        for comm_type in df['comm_type']:
            comm_types.append(comm_type)

        src_ids = []
        for src_id in df['source_id']:
            src_ids.append(src_id)    
        
        dest_ids = []
        for dest_id in df['dest_id']:
            dest_ids.append(dest_id) 
            
        id_dictionary = {}
        for i in range(len(msg_names)):
            msg_name = msg_names[i]
            id_dictionary[msg_name] = msg_ids[i]
            
        print("ID DICT",id_dictionary)
        
        header_dictionary = {}
        for i in range(len(msg_names)):
            msg_name = msg_names[i]
            header_dictionary[msg_name] = header_formats[i] 
        
        crc_dictionary = {}
        for i in range(len(msg_names)):
            msg_name = msg_names[i]
            crc_dictionary[msg_name] = crc_formats[i]     
            
        content_dictionary = {}
        for i in range(len(msg_names)):
            msg_name = msg_names[i]
            content_dictionary[msg_name] = content_formats[i]
            
        bits_dictionary = {}
        for i in range(len(msg_names)):
            msg_name = msg_names[i]
            bits_dictionary[msg_name] = msg_bits[i]
        
        header_values_dictionary = {}
        for i in range(len(msg_names)):
            msg_name = msg_names[i]
            header_values_dictionary[msg_name] = header_values[i]
            
        comm_types_dictionary = {}
        for i in range(len(msg_names)):
            msg_name = msg_names[i]
            comm_types_dictionary[msg_name] = comm_types[i]

        src_id_dictionary = {}
        for i in range(len(msg_names)):
            msg_name = msg_names[i]
            src_id_dictionary[msg_name] = []
            src_id_dictionary[msg_name].append(src_ids[i])
            src_id_dictionary[msg_name].append(dest_ids[i])
        
        name_to_header_type = {}
        for i,j in zip(msg_names, header_types):
            name_to_header_type[i] = j
            
            
        self.id_dictionary      = id_dictionary
        self.src_id_dictionary  = src_id_dictionary 
        self.header_dictionary  = header_dictionary
        self.crc_dictionary     = crc_dictionary
        self.content_dictionary = content_dictionary
        self.bits_dictionary    = bits_dictionary
        self.header_values_dictionary = header_values_dictionary
        self.comm_types_dictionary    = comm_types_dictionary
        
        self.msg_names = msg_names
        self.msg_ids   = msg_ids
        self.content_formats = content_formats
        self.header_formats  = header_formats
        self.crc_formats     = crc_formats
        self.msg_bits        = msg_bits
        self.header_values   = header_values
        self.comm_types      = comm_types
        self.header_types = header_types
        self.name_to_header_type = name_to_header_type
        
        print(self.content_formats)
        
    def print_details(self): 
        print('Configuration Details:')
        print('sock_multicast_group:'+self.sock_multicast_group)
        print('sock_multicast_send_port:'+self.sock_multicast_send_port)
        print('sock_multicast_rcv_port:'+self.sock_multicast_rcv_port)
        print('sock_send_ip:'+self.sock_send_ip)
        print('sock_send_port:'+self.sock_send_port)
        print('sock_rcv_port:'+self.sock_rcv_port)
        
        print('BIT DETAILS:')
        for x,y in zip(self.bitNames,self.bitValues):
            print(x, y)

    def read_ratc_cbi_indication_bit_names(self):
        indication_bit_names = []
        df = pd.read_excel("config/sim_config.xlsx", "ratc_cbi_indication_bits")
        for bitName in df['Bit Relay Name']:
            if pd.notnull(bitName):
                indication_bit_names.append(bitName)  
        return indication_bit_names
    
    def read_cbi_ratc_indication_bit_names(self):
        indication_bit_names = []
        df = pd.read_excel("config/sim_config.xlsx", "cbi_ratc_indication_bits")
        for bitName in df['Bit Relay Name']:
            if pd.notnull(bitName):
                indication_bit_names.append(bitName)  
        return indication_bit_names     
    
    def log(self, msg):
        self.logger.info(msg)
        # self.log_sheet.write(msg)
        
    def set_display(self, display):
        print('set_display called')
        self.display = display
        
    def update_set_bit_list_msg_id_for_display(self, set_bit_list, msg_id):
        # self.display.update_gui(set_bit_list, msg_id)   
        self.set_bit_list = set_bit_list
        self.set_bit_list_msg_id = msg_id

        
    def update_display_content(self,content):
        print("CONTENT to DISPLAY",content)
        # self.display.update_content(content)
        self.content_str = content
        
    def update_display_header(self,header_dict):
        self.display.update_header(header_dict)
        self.header_str = header_dict
        
    def update_bytes_display_content(self, content_list):
        print("calling update_bytes_content")
        self.display.update_bytes_content(content_list)
        print("Displa Content",content_list)
        self.fields_list = content_list
    
    def update_table_entry(self, time, msg,hex_string,label_format,label_list, observation_string,content_format,hex_data,data):
        self.display.add_entry(time, msg,hex_string, label_format,label_list, observation_string,content_format,hex_data,data)
        
    def udpate_bytes_format_considering_bits(self):
        for msg in self.msg_names:
            # print('msg:', msg)
            listMessageContents = dict[f'{msg}']
            byte_msg_formats = []
            updatedMsgFormatList = []
            bit_lengths = []
            labels_list = []
            struct_list = []
            for i,x in enumerate(listMessageContents):
                # print(i,"-",x[0],"-",x[4], 'msg format:', x[5], 'bit len:', x[6])
                
                byte_msg_formats.append(x[5])
                bit_lengths.append(int(x[6]))
                labels_list.append(x[0])
                struct_list.append(x[8])
                
            self.content_dictionary[msg] = byte_msg_formats.copy()
            self.labels_list_dictionary[msg] = labels_list.copy()
            self.labels_struct_list_dictionary[msg] = struct_list.copy()
            

            sizeForByte = 0
            updatedMsgFormatList = []
            for y,b in enumerate(bit_lengths):
                # print('b = ', b)
                if b >= 8 :
                    updatedMsgFormatList.append(byte_msg_formats[y])
                else:
                    sizeForByte = sizeForByte + b
                    if sizeForByte == 8:
                        # print('byte complete')
                        updatedMsgFormatList.append('B')
                        sizeForByte = 0
            # content_format = ' '.join(map(str, updatedMsgFormatList))
            # print('Modified bytes content_format ', content_format)
            # print('self.selected_msg_bit_lengths ', self.selected_msg_bit_lengths[0:-1])   
        
            self.modified_content_dictionary[msg] = updatedMsgFormatList.copy()
            self.bits_list_dictionary[msg] = bit_lengths.copy()
            
            # contentFormatList = self.content_dictionary[msg]
            # bitsList = self.bits_list_dictionary[msg]
            # modifiedContentFormatList = self.modified_content_dictionary[msg]
            
            # print('contentFormatList: ',contentFormatList)
            # print('bitsList: ',bitsList)
            # print('modifiedContentFormatList: ',modifiedContentFormatList)
            
    def get_message_name(self, msg_id, src_id, dest_id):
        msg_name = 'UNKNOWN'
        print("getting",msg_id,src_id,dest_id)
        
        for key,val in self.src_id_dictionary.items():
            # print("src= ",val[0], "Dest=",val[1]) => 0 id src_id, 1 is dest_id
            if(val[0] == src_id) and (val[1] == dest_id):
                # print('key:Msgname:',key,' SRC Found:', src_id)
                v_msg_id = self.id_dictionary[key]
                if(v_msg_id == msg_id):
                    # print('key:Msgname:',key,' msg_id Found:', msg_id)
                    msg_name = key
                    return msg_name
        return msg_name
    
                
    def get_message_name_by_msgID(self,msg_id):
        print("getting",msg_id)
        msg_name = 'UNKNOWN'
        
        for key,value in self.id_dictionary.items():
            # print(key,value)
            
            # print("VALUE",value,"MSG ID",msg_id)
            
            if(value == msg_id):
                print("VALUE inside IF",value,"MSG ID",msg_id)
                msg_name = key
                return msg_name
        return msg_name

    def get_message_name_of_external(self, msg_id, src_id):
        msg_name = 'UNKNOWN'
        for key,val in self.src_id_dictionary.items():
            # print("src= ",val[0], "Dest=",val[1]) => 0 id src_id, 1 is dest_id
            if(val[0] == src_id):
                # print('key:Msgname:',key,' SRC Found:', src_id)
                v_msg_id = self.id_dictionary[key]
                if(v_msg_id == msg_id):
                    # print('key:Msgname:',key,' msg_id Found:', msg_id)
                    msg_name = key
                    return msg_name
        return msg_name
 
config = Configuration()


