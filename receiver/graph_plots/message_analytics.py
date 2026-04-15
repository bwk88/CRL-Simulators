from PyQt5.QtCore import QObject

# import pyqtgraph as pg
import time
from collections import deque


class MessageAnalytics(QObject):
    print("MessageAnalytics Class called")
    
    def __init__(self,model):
        super().__init__()
        self.model = model
        print("Message Analytics Initial")
        self.model.rowsInserted.connect(self.on_rows_inserted)

        
    def on_rows_inserted(self,parent,start,end):
        count = end - start + 1
        self.msg_counter += count
        print("Message Analytics called",parent,start,end)
        
    def compute_message_rate(self):
        now =  time.time()
        
        self.time_history.append(now)
        self.rate_history.append(self.msg_counter)
        
        self.msg_counter = 0
        
        return list(self.time_history), list(self.rate_history)