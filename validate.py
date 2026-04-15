from Configuration import config
from PyQt5 import QtCore, QtGui, QtWidgets
all_id = []
seen = set()

def validate_file():
    # print("Validate Clicked",config.dictionary_msg)
    for key,value in config.dictionary_msg.items():
            print(key,value,"keyy",config.id_dictionary[key])
            msg_id = config.id_dictionary[key]
            arr1 = [value[0],value[1],msg_id]
            all_id.append(arr1)
    
    for arr in all_id:
        t = tuple(arr)
        if t in seen:
            print("Duplicate Found",arr)
            msg = "Duplicate Data Present"
            show_error_message(msg)
            break
        else:
            seen.add(t)
    # print("all id",all_id)
    
    
def show_error_message(error_message):   
    print("Error",error_message)  
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText('Invalid File Structure')
    msg.setInformativeText(error_message)
    msg.setWindowTitle('Error')
    msg.exec_()