import sys
import socket
import subprocess
import os, re, json
import select
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QLineEdit
from PyQt5.QtCore import pyqtSignal, QThread, QObject, pyqtSlot

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
    # def setupUi(self, MainWindow):     
        self.setWindowTitle("SIMULATOR CLIENT")
        # self.resize(1481, 786)
        self.setMaximumSize(600, 400)
        
        
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName("central_widget")
        self.setCentralWidget(self.central_widget)
        self.VBoxLayout = QVBoxLayout(self.central_widget)
        self.VBoxLayout.setObjectName("VBoxLayout")
        
        
        self.settingWidget = QWidget(self.central_widget)
        self.settingWidgetHLayout = QHBoxLayout(self.settingWidget)
        
        self.ServerSettingWidget = QWidget(self.settingWidget)
        self.ServerSettingWidgetVLayout = QVBoxLayout(self.ServerSettingWidget)
        
        self.serverSettingLabel = QLabel("FORWARDING SETTINGS")
        self.serverSettingLabel.setStyleSheet("""
                                              font-weight: bold;
                                              background-color: #e0e0e0;
                                              padding: 5px 5px;
                                              """)
        self.ServerSettingWidgetVLayout.addWidget(self.serverSettingLabel)
        
        
        self.serverIP = settingsFields("Receiver IP", "192.168.2.111")
        self.ServerSettingWidgetVLayout.addWidget(self.serverIP)
        self.serverPort = settingsFields("Receiver Port", "11095")
        self.ServerSettingWidgetVLayout.addWidget(self.serverPort)

        self.ServerSettingWidgetVLayout.addStretch()
        
        self.settingWidgetHLayout.addWidget(self.ServerSettingWidget)
        
        self.ModuleSettingWidget = QWidget(self.settingWidget)
        self.ModuleSettingWidgetVLayout = QVBoxLayout(self.ModuleSettingWidget)
        
        self.moduleSettingLabel = QLabel("LISTINING PORTS")
        self.moduleSettingLabel.setStyleSheet("""
                                              font-weight: bold;
                                              background-color: #e0e0e0;
                                              padding: 5px 2px;
                                              """)
        self.ModuleSettingWidgetVLayout.addWidget(self.moduleSettingLabel)

        self.modulePort = settingsFields("Receiving Port", "20061")
        self.ModuleSettingWidgetVLayout.addWidget(self.modulePort)
        
        self.tcpDumpHeaderLength = settingsFields("Header Length", "45")
        self.ModuleSettingWidgetVLayout.addWidget(self.tcpDumpHeaderLength)
        
        
        self.moduleNote = QLabel("*Use comma to seperate multiple ports (1009,2001)")
        self.moduleNote.setStyleSheet("""
                                  font-size:10px;
                                  color: #954535;
                                  """)
        self.ModuleSettingWidgetVLayout.addWidget(self.moduleNote)
        
        
        
        self.ModuleSettingWidgetVLayout.addStretch()
        
        self.settingWidgetHLayout.addWidget(self.ModuleSettingWidget)


        self.VBoxLayout.addWidget(self.settingWidget)
        self.button = QPushButton("Start")
        self.VBoxLayout.addWidget(self.button)
        self.button.clicked.connect(self.onButtonClicked)
        
        self.stopButton = QPushButton("Stop")
        self.VBoxLayout.addWidget(self.stopButton)
        self.stopButton.clicked.connect(self.onStopButtonClicked)
        self.stopButton.setEnabled(False)
        
        self.saveButton = QPushButton("Save Settings")
        self.VBoxLayout.addWidget(self.saveButton)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        
        self.Wthread = None
        self.dumpSnifferWorker = None
        self.settingsData = {
            "Interface": "any",
            "Server_IP": "",
            "Server_Port": "",
            "mode": "",
            "application_receiving_port": "",
            "tcp_header_length": ""
            }
        self.onUILoad()
        
        
    def onUILoad(self):
        if not os.path.exists("clientConfig.json"):
            return
        
        with open("clientConfig.json", "r") as f:
            self.settingsData = json.load(f)
            self.serverIP.setValue(self.settingsData["Server_IP"])
            self.serverPort.setValue(self.settingsData["Server_Port"])
            self.modulePort.setValue(self.settingsData["application_receiving_port"])
            self.tcpDumpHeaderLength.setValue(self.settingsData["tcp_header_length"])

    

    def onButtonClicked(self):
        if self.Wthread is not None :
            print("Already running cannot start again")
            return
        
        print("Starting Thread")
        self.Wthread = QThread()
        
        self.dumpSnifferWorker = sniffRerouter()
        self.dumpSnifferWorker.moveToThread(self.Wthread)
        
        self.dumpSnifferWorker.startWork.connect(self.dumpSnifferWorker.run)
        self.dumpSnifferWorker.progress.connect(self.updateProgress)
    
        
        self.Wthread.start()
        
        self.settingsData["Server_IP"] = self.serverIP.getText()
        self.settingsData["Server_Port"] = self.serverPort.getText()
        self.settingsData["application_receiving_port"] = self.modulePort.getText()
        self.settingsData["mode"] = "udp"
        self.settingsData["tcp_header_length"] = self.tcpDumpHeaderLength.getText()
        
        
        self.dumpSnifferWorker.startWork.emit(self.settingsData)
        self.dumpSnifferWorker.finished.connect(self.onProcessStopped)
        self.stopButton.setEnabled(True)
        self.button.setEnabled(False)

        
    def onStopButtonClicked(self):
        if self.dumpSnifferWorker:
            self.dumpSnifferWorker.stopProcess()
            self.button.setEnabled(True)
            self.stopButton.setEnabled(False)
           

    def updateProgress(self):
        pass

    def onProcessStopped(self):
        self.dumpSnifferWorker.deleteLater()
        self.Wthread.deleteLater()
        self.Wthread.quit()
        self.Wthread.wait()
        self.dumpSnifferWorker = None
        self.Wthread = None 

    def onSaveButtonClicked(self):
        self.settingsData["Server_IP"] = self.serverIP.getText().strip()    
        self.settingsData["Server_Port"] = self.serverPort.getText().strip() 
        self.settingsData["application_receiving_port"] = self.modulePort.getText().strip()  
        self.settingsData["tcp_header_length"] = self.tcpDumpHeaderLength.getText().strip()
        with open(f"clientConfig.json", "w") as f:
            json.dump(self.settingsData, f, indent=4)
        print("settings saved", self.serverIP.getText() , self.serverPort.getText(), self.modulePort.getText(), self.tcpDumpHeaderLength.getText())

class settingsFields(QWidget):
    back_clicked_signal = pyqtSignal()
    def __init__(self, labelValue, value, parent=None):
        super().__init__(parent)

        self.layout_outer = QHBoxLayout(self)
        self.layout_outer.setContentsMargins(0,0,0,0)
        self.label = QLabel(labelValue)
        self.label.setStyleSheet("""
                                  color: #954535;
                                  """)
        self.label.setMaximumWidth(100)
        self.label.setMinimumWidth(100)
        self.layout_outer.addWidget(self.label)
        
        self.labelValue = QLineEdit(value)
        self.labelValue.setMinimumWidth(150)
        self.labelValue.setMaximumWidth(600)
        self.labelValue.setStyleSheet("""
                                  padding: 0px;
                                  margin: 0px;
                                  """)
        self.layout_outer.addWidget(self.labelValue)   
    
    def setValue(self, value):
        self.labelValue.setText(str(value))
        
    def getText(self):
        return self.labelValue.text()


class sniffRerouter(QObject):
    startWork = pyqtSignal(object)
    progress = pyqtSignal()
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._running=True
        self.packet_size = 0
        self.calculated_size = 0
        
    
    def stopProcess(self):
        print("Stopping Process")
        self._running = False
        
        if self.process:
            try:
                self.process.terminate()
                self.process.wait() 
            except:
                pass
   
        self.sock.close()   
        self.finished.emit()
            


            
    @pyqtSlot(object)   
    def run(self, settingsData):
        print("capture packets start")
        self.network_interface = settingsData["Interface"]
        self.serverRIP = settingsData["Server_IP"].strip()
        self.serverRPort = settingsData["Server_Port"].strip()
        self.tcp_header_length = int(settingsData["tcp_header_length"].strip())
        self.bpf_filter = ""
        
        self.multipleAppPorts = settingsData['application_receiving_port'].split(",") 
        for i,ports in enumerate(self.multipleAppPorts):
            self.bpf_filter += f"{settingsData['mode']} port {ports.strip()}"
            if i!=len(self.multipleAppPorts)-1:
                self.bpf_filter += " or "
            
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
        
        # while self._running:
        print(type(self.serverRIP), type(self.serverRPort))
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",self._running)
        self.command = ["tcpdump", "-i", self.network_interface, "-xx", "-n", "-l"]

        if self.bpf_filter:
            self.command.append(self.bpf_filter)
        
        print(self.command)
        self.process = subprocess.Popen(self.command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        # for line in process.stdout:
        #     print(line.strip())
        self.hex_pattern= re.compile(r"^\s*([0-9a-f ]+)$")
        # hex_pattern= re.compile(r"^\s*(?:0x)?[0-9a-f]{4}:\s([0-9a-f ]+)$")
        
        print(f"Forwarding raw tcpdump bytes from {self.network_interface} to {self.serverRIP}:{self.serverRPort} (UDP)")
        
        try:
            hex_data = []
            while self._running:
                line = self.process.stdout.readline()
                
                if not line:
                    break
                
                if "length" in line:
                    print("\n\n================ NEW MESSAGE =======================")
                    self.packet_size = int(line.split("length")[-1].strip())
                    print("Message Length: ",self.packet_size)
                    continue
                    
                if self.packet_size == 0:
                    continue
                else:
                    print(line.strip().split(":  ")[-1])
                    match = self.hex_pattern.match(line.strip().split(":  ")[-1])
                    # .strip().split(":  ")[-1]
                    # print("Match", match)
                    if match:
                        hex_part = match.group(1).replace(" ","")
                        hex_data.append(hex_part)
                        self.calculated_size += int(len(hex_part)/2)
                        # print("hex data",hex_data)
                        # print("calculated_size AND packet_size+48",self.calculated_size, self.packet_size+self.tcp_header_length)
                    
                        
                    if self.calculated_size >= (self.packet_size+self.tcp_header_length):
                        self.packet_size = 0 
                        self.calculated_size = 0
                        
                        # temp_size = 2*self.packet_size
                        full_hex = "".join(hex_data)
                        # print("\n", "Packet size", len(full_hex),"  :  ", full_hex,"\n")
                        slice_indx = 2*self.tcp_header_length
                        full_hex = full_hex[slice_indx:]
                        # full_hex = full_hex[-temp_size:]
                        # print("\n", "Packet size", len(full_hex),"  :  ", full_hex,"\n")
                        
                        try:
                            raw_bytes = bytes.fromhex(full_hex)
                            self.sock.sendto(raw_bytes,(self.serverRIP, int(self.serverRPort)))
                            print("SENT>> ")
                            for i, cr in enumerate(full_hex):
                                if i%4 == 0:
                                    print(" ", end="")
                                
                                if i%32 == 0:
                                    print()
                                    
                                print(cr, end="")
                                
                        except Exception:
                            pass
                        
                        hex_data=[]
            # print("out of while loooooooooooooooooooooooop")
                        
        except Exception as e:
            print(e, "exception")
            if self.process:
                try:
                    self.process.terminate()
                    # self.sock.close()   
                    # self.finished.emit()
                    
                except:
                    pass

        # finally:
        #     print("Finnally enterer")
        #     if self.process:
        #         try:
        #             self.process.terminate()
        #         except:
        #             pass
                
        # self.sock.close()   
        # self.finished.emit()
                
                 
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())














# import socket
# import subprocess
# import os, re
# import select
# import binascii



# command = ["tcpdump", "-i", "any", "-xx", "-n", "-l", "udp"]
# process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
# isStart = False
# for line in process.stdout:
#     if "UDP" in line:
#         print()
#         continue
    
#     print(line.strip())
            

# def capture_packets(interface, isRunning=False, bpf_filter=None):
#     destIP = "192.168.2.111"
#     destPort = 11095
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    
#     while isRunning:
#         command = ["tcpdump", "-i", interface, "-xx", "-n", "-l"]

#         if bpf_filter:
#             command.append(bpf_filter)
        
        
#         process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
#         # for line in process.stdout:
#         #     print(line.strip())
            
#         hex_pattern= re.compile(r"^\s*([0-9a-f ]+)$")
        
#         # hex_pattern= re.compile(r"^\s*(?:0x)?[0-9a-f]{4}:\s([0-9a-f ]+)$")
        
        
#         print(f"Forwarding raw tcpdump bytes from {interface} to {destIP}:{destPort} (UDP)")
        
#         try:
#             hex_data = []
#             packet_size = 0
#             for line in process.stdout:
#                 if "length" in line:
#                     packet_size = int(line.split("length")[-1].strip())
#                 if packet_size == 0:
#                     continue
#                 else:
#                     print("Message Length: ",packet_size)
#                     print(line.strip().split(":  ")[-1])
                    
#                     match = hex_pattern.match(line.strip().split(":  ")[-1])
#                     # .strip().split(":  ")[-1]
#                     print("Match", match)
                    
                    
#                     if match:
#                         hex_part = match.group(1).replace(" ","")
#                         hex_data.append(hex_part)
                        
#                         # print("hex data",hex_data)
                        
#                     elif hex_data:
#                         temp_size = 2*packet_size
#                         full_hex = "".join(hex_data)
#                         full_hex = full_hex[-temp_size:]
#                         print("\n", "Packet size", len(full_hex),"  :  ", full_hex,"\n")
                        
#                         try:
#                             raw_bytes = bytes.fromhex(full_hex)
#                             sock.sendto(raw_bytes, (destIP, destPort))
#                             print("sent", raw_bytes)
#                         except Exception:
#                             pass
#                         hex_data=[]
#         except KeyboardInterrupt:
#             print("\n[*] Stopping....")
#             process.terminate()
#             sock.close()
#         finally:
#             process.terminate()
#             sock.close()


# capture_packets("any", True, "udp port 11055")




# from scapy.all import *

# def forward_to_ip(pkt):
#     destIP = "192.168.2.111"
#     destPort = 11095
#     if UDP in pkt and RAW in pkt:
#         data = bytes(pkt[RAW].load)
#         print(data)
#         new_pkt = IP(dst=destIP)//UDP(dport=destPort)/data
#         send(new_pkt, verbose=False)
        
# sniff(filter="udp", prn=forward_to_ip, store=False)

        


