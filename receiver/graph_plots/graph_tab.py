from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg
import time,random

from PyQt5.QtCore import QTimer
from graph_plots.message_analytics import MessageAnalytics
from collections import deque

class GraphTab(QWidget):
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.rate_graph = pg.PlotWidget(title="Messsage Rate (msg/sec)")
        self.layout.addWidget(self.rate_graph)
        self.rate_curve = self.rate_graph.plot()
        
        self.time_history = deque(maxlen=60)
        self.rate_history = deque(maxlen=60)
            
        self.msg_counter = 0
        self.x = []
        self.y = []
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)
        
    def update_graph(self):
        # Todo    
        print("update_graph called")
        self.msg_counter += 1
        
        self.x.append(self.msg_counter)
        self.y.append(self.msg_counter * 2)
        
        # print("X value:" ,self.x,"Y Value",self.y)
        
        self.rate_curve.setData(self.x,self.y)
        
        
    