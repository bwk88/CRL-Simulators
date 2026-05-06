#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 10 12:46:32 2025

@author: kuldeepsingh@Indigenous.com
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QSizePolicy, QListWidgetItem, QWidget, QGridLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage, QBrush, QIcon
from PyQt5.QtCore import Qt, QSize



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
    
            
    def setPNG(self, btn, icon_path, width, height):
        addIcon =  QPixmap(icon_path)
        addIcon_pixmap = self.tint_pixmap(addIcon, QColor(76,175,80))
        btn.setIcon(QIcon(addIcon_pixmap))
        btn.setIconSize(QSize(width, height))   

    def setSVG(self, btn, icon_path, width, height):
        addIcon =  QPixmap(icon_path)
        btn.setIcon(QIcon(addIcon))
        btn.setIconSize(QSize(width, height)) 
        
ui_ops = UI_Opreations()