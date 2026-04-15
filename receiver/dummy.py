from PyQt5.QtWidgets import QApplication
import pyqtgraph as pg
import sys

from Configuration import config

app = QApplication(sys.argv)
print("graph data",config.graph_plot_data)

win = pg.GraphicsLayoutWidget(show=True, title="Advanced Layout")
plot = win.addPlot(title="My Plot")

plot.plot([1,2,3,4], [10,20,15,25], pen='r')

sys.exit(app.exec_())