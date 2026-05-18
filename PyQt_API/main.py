#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Basic PyQt5 Template for API Client Tool
----------------------------------------

Install:
pip install PyQt5 requests openpyxl

Optional:
pip install qtawesome

"""

import sys
import json
import requests
import os
from PyQt5.QtWidgets import QCompleter, QSizePolicy

from api_dict import API_CONFIG,ALL_DATA_APIS,GET_APIS

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QComboBox,
    QScrollArea,
    QFrame,
    QMessageBox,
    QTreeWidget,
    QTreeWidgetItem,
    QSpinBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal


# =========================================================
# API THREAD
# =========================================================

class APICallThread(QThread):

    finished_signal = pyqtSignal(dict)

    def __init__(self, url, payload):
        super().__init__()

        # self.method = method
        self.url = url
        self.payload = payload

    def run(self):

        try:
            response = requests.post(self.url, json=self.payload)
            # response = requests.request(
            #     # method=self.method,
            #     url=self.url,
            #     json=self.payload,
            #     # timeout=30
            # )

            try:
                data = response.json()
            except:
                data = response.text

            result = {
                "status_code": response.status_code,
                "response": data
            }

        except Exception as e:

            result = {
                "status_code": "ERROR",
                "response": str(e)
            }

        self.finished_signal.emit(result)


# =========================================================
# MAIN WINDOW
# =========================================================

class APIClientWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("🚀 API Client Dashboard")
        self.setGeometry(100, 100, 1000, 700)

        self.dynamic_inputs = {}

        self.setup_ui()

    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):

        # Main Widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Main Layout
        self.main_layout = QVBoxLayout()
        main_widget.setLayout(self.main_layout)

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        self.header_label = QLabel("🚀 API Client Dashboard")
        self.header_label.setAlignment(Qt.AlignCenter)

        self.header_label.setStyleSheet("""
            QLabel {
                background-color: #1f2a44;
                color: white;
                font-size: 22px;
                font-weight: bold;
                padding: 15px;
            }
        """)

        self.main_layout.addWidget(self.header_label)

        # -------------------------------------------------
        # API SELECTION
        # -------------------------------------------------

        api_frame = QFrame()
        api_frame.setFrameShape(QFrame.StyledPanel)

        api_layout = QFormLayout()

        self.api_dropdown = QComboBox()
        
        
        self.api_dropdown.setEditable(True)
        self.api_dropdown.setInsertPolicy(QComboBox.NoInsert)#prevents insertion of search text
        self.api_dropdown.completer().setCompletionMode(QCompleter.PopupCompletion)
        
        
        
        for key,value in API_CONFIG.items():
            print("key:::::::::",key)
            self.api_dropdown.addItem(key)
        
        # self.api_dropdown.addItems([
        #     "GET_CUSTOMERS",
        #     "POST_LOGIN",
        #     "DELETE_USER"
        # ])

        self.api_dropdown.currentIndexChanged.connect(
            self.on_api_selected
        )

        api_layout.addRow("Select API:", self.api_dropdown)

        api_frame.setLayout(api_layout)

        self.main_layout.addWidget(api_frame)

        # -------------------------------------------------
        # DYNAMIC INPUT AREA
        # -------------------------------------------------

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()

        self.form_layout = QFormLayout()

        self.scroll_widget.setLayout(self.form_layout)

        self.scroll_area.setWidget(self.scroll_widget)

        self.main_layout.addWidget(self.scroll_area)

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        button_layout = QHBoxLayout()

        self.call_button = QPushButton("▶ Call API")
        self.call_button.clicked.connect(self.call_api)

        self.load_button = QPushButton("📂 Load JSON")
        self.load_button.clicked.connect(self.load_json)

        self.save_button = QPushButton("💾 Save Response")
        self.save_button.clicked.connect(self.save_response)

        button_layout.addWidget(self.call_button)
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.save_button)

        self.main_layout.addLayout(button_layout)

        # -------------------------------------------------
        # STATUS LABEL
        # -------------------------------------------------

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
        """)

        self.main_layout.addWidget(self.status_label)

        # -------------------------------------------------
        # RESPONSE BOX
        # -------------------------------------------------

        self.response_box = QTextEdit()
        self.response_box.setReadOnly(True)

        self.main_layout.addWidget(self.response_box)

        # Load Initial Inputs
        selected_api = self.api_dropdown.currentText()
        arg_name_list = []
        for items in API_CONFIG[selected_api]['Request Cells']:  
            arg_name_list.append(items['text'])
        
        self.generate_inputs(arg_name_list)

    # =====================================================
    # DYNAMIC INPUTS
    # =====================================================

    def clear_inputs(self):

        while self.form_layout.rowCount():

            self.form_layout.removeRow(0)

        self.dynamic_inputs = {}

    def generate_inputs(self, fields):

        self.clear_inputs()

        for field in fields:

            entry = QLineEdit()

            self.form_layout.addRow(field, entry)

            self.dynamic_inputs[field] = entry

    # =====================================================
    # EVENTS
    # =====================================================

    def on_api_selected(self):
                
        curr_text = self.api_dropdown.currentText()
        print("curr_text",API_CONFIG[curr_text])
        selected_api = self.api_dropdown.currentText()
        arg_name_list = []
        for items in API_CONFIG[selected_api]['Request Cells']:  
            arg_name_list.append(items['text'])
     
        self.generate_inputs(arg_name_list)




    # =====================================================
    # BUILD PAYLOAD
    # =====================================================

    def build_payload(self):

        payload = {}

        for key, widget in self.dynamic_inputs.items():

            payload[key] = widget.text().strip()

        return payload

    # =====================================================
    # API CALL
    # =====================================================

    def load_config(self):
        config_path = "config/config.json"

        if not os.path.exists(config_path):
            raise FileNotFoundError("config.json not found")

        try:
            with open(config_path) as f:
                return json.load(f)
        except Exception as e:
            print("Error loading config:", e)
            return {}






    def call_api(self):

        payload = self.build_payload()

        selected_api = self.api_dropdown.currentText()
        CONFIG = self.load_config()
        BASE_URL = CONFIG.get("BASE_URL", "http://localhost:5000")
        api_data = API_CONFIG[selected_api]
        
        url = f"{BASE_URL}{api_data['URL']}"
        method = str(api_data["Method Type"]).upper()
        print("url----->",url,method,payload)
     
        self.status_label.setText("⏳ Calling API...")
        self.status_label.setStyleSheet("color: orange;")

        self.call_button.setEnabled(False)

        self.thread = APICallThread(
            # method,
            url,
            payload
        )

        self.thread.finished_signal.connect(
            self.handle_response
        )

        self.thread.start()

    # =====================================================
    # HANDLE RESPONSE
    # =====================================================

    def handle_response(self, result):

        self.call_button.setEnabled(True)

        status = result["status_code"]

        if status == "ERROR":

            self.status_label.setText("❌ API Call Failed")
            self.status_label.setStyleSheet("color: red;")

        else:

            self.status_label.setText(
                f"✅ Status Code: {status}"
            )

            self.status_label.setStyleSheet(
                "color: green;"
            )

        self.response_box.clear()

        self.response_box.setText(
            json.dumps(result, indent=4)
        )

    # =====================================================
    # FILE OPERATIONS
    # =====================================================

    def load_json(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open JSON File",
            "",
            "JSON Files (*.json)"
        )

        if not file_path:
            return

        with open(file_path, "r") as f:

            data = json.load(f)

        self.response_box.setText(
            json.dumps(data, indent=4)
        )

    def save_response(self):

        content = self.response_box.toPlainText()

        if not content:
            QMessageBox.warning(
                self,
                "Warning",
                "No response to save"
            )
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Response",
            "",
            "JSON Files (*.json)"
        )

        if not file_path:
            return

        with open(file_path, "w") as f:
            f.write(content)

        QMessageBox.information(
            self,
            "Saved",
            "Response saved successfully"
        )


# =========================================================
# MAIN
# =========================================================

def main():

    app = QApplication(sys.argv)

    window = APIClientWindow()

    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
