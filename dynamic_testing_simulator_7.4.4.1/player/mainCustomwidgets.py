import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from SNS.utility import SafeListWidget, ui_ops
from PyQt5.QtGui import QFontMetrics, QFont, QPixmap

CWD = os.getcwd()

# Widget to display functions and testcases
class errorDisplay(QWidget):
    def show(parent, errorMessage):
        QMessageBox().critical(parent, "Error!", errorMessage, QMessageBox().Ok)