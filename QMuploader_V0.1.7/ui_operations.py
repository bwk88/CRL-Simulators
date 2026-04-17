#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 31 10:21:52 2025

@author: kuldeepsingh@Indigenous.com
"""


import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QSizePolicy, QListWidgetItem, QWidget, QGridLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage, QBrush, QIcon
from PyQt5.QtCore import Qt



class UI_Opreations(QWidget):
    def __init__(self):
        layout = QHBoxLayout()     
            
    # ICONS PROCESSING (Changing defalut color)
    def tint_pixmap(self, icon_pixmap, tint_color):
        resized_pixmap = icon_pixmap.scaled(45,45, Qt.KeepAspectRatio)
        image = resized_pixmap.toImage().convertToFormat(QImage.Format_ARGB32)
        painter = QPainter(image)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(image.rect(), tint_color)
        painter.end() 
        return QPixmap().fromImage(image)

ui_ops = UI_Opreations()