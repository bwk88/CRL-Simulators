from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
from debuggerFile import DBUG
import pandas as pd
import ast

# TO convert csv file read list type string to list '[1,23,4]' --> [1,23,4]

def insertDataInbetweenCSV(splitIndex, df, new_row):
    DBUG.printWhere()
    df_top = df.iloc[:splitIndex]
    # print(df_top.tail())
    
    df_bottom = df.iloc[splitIndex:]
    # print(df_bottom.head())
    df = pd.concat([df_top, new_row, df_bottom], ignore_index=True)
    return df


def toSuperScript(num):
    supMap = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    return str(num).translate(supMap)

def listStringToList(df):
    DBUG.printWhere()
    df["Header_Data"] = df["Header_Data"].apply(lambda x: ast.literal_eval(x) if not pd.isna(x) else x) 
    df["Input_Data"] = df["Input_Data"].apply(lambda x: ast.literal_eval(x)  if not pd.isna(x) else x) 
    df["output_header_data"] = df["output_header_data"].apply(lambda x: ast.literal_eval(x) if not pd.isna(x) else x) 
    df["output_content_data"] = df["output_content_data"].apply(lambda x: ast.literal_eval(x)  if not pd.isna(x) else x) 
    df["Preconditions"] = df["Preconditions"].apply(lambda x: ast.literal_eval(x)  if not pd.isna(x) else x) 


class SafeListWidget(QListWidget):
    dragDroppedItemSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QListWidget.InternalMove)
        # self.setDefaultDropAction(Qt.MoveAction)
    def add_Item(self, widget):
        item = QListWidgetItem(self)
        item.setSizeHint(widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, widget)
        
    def dropEvent(self, event):
        pos = event.pos()
        # print("Drop POSITION: ", pos)
        item = self.itemAt(pos)
        
        if item is None:
            event.ignore()
            return
        
        current_row = self.currentRow()
        index = self.indexAt(event.pos())
        row = index.row() if index.isValid() else self.count()
        position = self.dropIndicatorPosition()
        
        if position == self.OnItem:
            pass
            # print("ON", row)
            # print("POSITION and Initial POSITION", position, current_row)
        if position == self.AboveItem:
            # print("ABOVE", row)
            # print("POSITION and Initial POSITION", position, current_row, row)
            if current_row+1 == row:
                # print("igonring event")
                event.ignore()
                return
            
        if position == self.BelowItem:
            pass
            # print("BELOOW", row)
            # print("POSITION and Initial POSITION", position, current_row)
        if position == self.OnViewport:
            pass
            # print("ON VP", row)
            # print("POSITION and Initial POSITION", position, current_row)
            
        super().dropEvent(event)
        self.dragDroppedItemSignal.emit()
        for i in range(self.count()):
            item = self.item(i)
            w = self.itemWidget(item)
            if w is None:
                continue
            item.setSizeHint(w.sizeHint())
            
    def dragMoveEvent(self, event):
        # print("drag postiions: ", event.pos())
        target_row = self.row(self.itemAt(event.pos()))
        current_row = self.currentRow()
        # print("Target and current row and total count - 1  == >", target_row, current_row, (self.count() - 1))

        if target_row is None:
            if current_row:
                event.ignore()
                
        # if current_row == 0:     
        #     if target_row == current_row or target_row == current_row +1:
        #         event.ignore()
        #         return
        
        if target_row == -1 and current_row != self.count() - 1:
            event.ignore()
        else:
            event.accept()
        super().dragMoveEvent(event)
