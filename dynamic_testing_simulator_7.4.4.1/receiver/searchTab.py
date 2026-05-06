from PyQt5 import QtGui
def searchTab(text):
    print(text)
    
def searchButtonHandle(self,datastore):
    print("search")
    # selected_indexes = self.tableView.selectionModel().selectedIndexes()
    # print("Text",self.searchFeild.text())
    # message_text = self.searchFeild.text()
    # print("row count",datastore.model.rowCount())
    
    # for row in range(datastore.model.rowCount()):
    #     item = datastore.model.item(row, 2)
    #     if item:
    #         if message_text.lower() == item.text().lower():
    #             print("Message Found",item.text())
    #             # item.setBackground(QtGui.QColor(0,255,255))
    #         else:
    #             datastore.model.removeRow(row)
                
    # for index in selected_indexes:
    #     row = index.row()
    #     row_data = []
    #     for column in range(datastore.model.columnCount()):
    #         item = datastore.model.item(row, column)
    #         if item:
    #             print("item",item.text())
    
    # for i in range(datastore.model.count()):
    #     widget = self.containerLayout.itemAt(i).widget()
    #     print("widget",widget)
        
        
    # for i in range(self.containerLayout.count()):
    #     widget = self.containerLayout.itemAt(i).widget()
        
        # if widget is not None and text.lower() !="":
        #     if text.lower() in widget.text().lower():
        #         widget.setStyleSheet("background-color: pink;")
        #         self.scrollArea.ensureWidgetVisible(widget,xMargin=10,yMargin=10)
        #     else:
        #         widget.setStyleSheet("")