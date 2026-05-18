#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import requests
import os
from dict import API_CONFIG

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
    QFrame,
    QMessageBox,
    QTreeWidget,
    QTreeWidgetItem,
    QSpinBox,
    QCompleter
)

from PyQt5.QtCore import Qt, QThread, pyqtSignal

# from api_dict import API_CONFIG


# =========================================================
# API THREAD
# =========================================================

class APICallThread(QThread):

    finished_signal = pyqtSignal(dict)

    def __init__(self, url, payload):

        super().__init__()

        self.url = url
        self.payload = payload

    def run(self):

        try:

            response = requests.post(
                self.url,
                json=self.payload
            )

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

        self.setWindowTitle("🚀 Dynamic API Client")

        self.setGeometry(100, 100, 1100, 750)

        self.widget_map = {}

        self.spinbox_map = {}

        self.current_schema = {}

        self.setup_ui()

    # =====================================================
    # UI
    # =====================================================

    def setup_ui(self):

        main_widget = QWidget()

        self.setCentralWidget(main_widget)

        self.main_layout = QVBoxLayout()

        main_widget.setLayout(self.main_layout)

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        self.header_label = QLabel(
            "🚀 Dynamic API Client"
        )

        self.header_label.setAlignment(
            Qt.AlignCenter
        )

        self.header_label.setStyleSheet("""
            QLabel {
                background-color: #1f2a44;
                color: white;
                font-size: 22px;
                font-weight: bold;
                padding: 15px;
            }
        """)

        self.main_layout.addWidget(
            self.header_label
        )

        # -------------------------------------------------
        # API SELECTION
        # -------------------------------------------------

        api_frame = QFrame()

        api_layout = QFormLayout()

        self.api_dropdown = QComboBox()

        self.api_dropdown.setEditable(True)

        self.api_dropdown.setInsertPolicy(
            QComboBox.NoInsert
        )

        self.api_dropdown.completer().setCompletionMode(
            QCompleter.PopupCompletion
        )

        for key in API_CONFIG.keys():

            self.api_dropdown.addItem(key)

        self.api_dropdown.currentIndexChanged.connect(
            self.on_api_selected
        )

        api_layout.addRow(
            "Select API:",
            self.api_dropdown
        )

        api_frame.setLayout(api_layout)

        self.main_layout.addWidget(api_frame)

        # -------------------------------------------------
        # TREE
        # -------------------------------------------------

        self.tree = QTreeWidget()

        self.tree.setColumnCount(2)

        self.tree.setHeaderLabels(
            ["Field", "Value"]
        )

        self.main_layout.addWidget(self.tree)

        # -------------------------------------------------
        # BUTTONS
        # -------------------------------------------------

        button_layout = QHBoxLayout()

        self.call_button = QPushButton(
            "▶ Call API"
        )

        self.call_button.clicked.connect(
            self.call_api
        )

        self.load_button = QPushButton(
            "📂 Load JSON"
        )

        self.load_button.clicked.connect(
            self.load_json
        )

        self.save_button = QPushButton(
            "💾 Save Response"
        )

        self.save_button.clicked.connect(
            self.save_response
        )

        button_layout.addWidget(
            self.call_button
        )

        button_layout.addWidget(
            self.load_button
        )

        button_layout.addWidget(
            self.save_button
        )

        self.main_layout.addLayout(
            button_layout
        )

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        self.status_label = QLabel("")

        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
            }
        """)

        self.main_layout.addWidget(
            self.status_label
        )

        # -------------------------------------------------
        # RESPONSE BOX
        # -------------------------------------------------

        self.response_box = QTextEdit()

        self.response_box.setReadOnly(True)

        self.main_layout.addWidget(
            self.response_box
        )

        # INITIAL LOAD

        self.on_api_selected()

    # =====================================================
    # TREE FUNCTIONS
    # =====================================================

    def clear_tree(self):

        self.tree.clear()

        self.widget_map = {}

        self.spinbox_map = {}

    # =====================================================

    def build_tree(self, data, parent):

        for key, value in data.items():

            item = QTreeWidgetItem(parent)

            item.setText(0, key)

            # ------------------------------------------------
            # ARRAY
            # ------------------------------------------------

            if (
                isinstance(value, dict)
                and value.get("_is_array")
            ):

                self.create_array_group(
                    parent_item=item,
                    array_name=key,
                    array_schema=value
                )

            # ------------------------------------------------
            # STRUCT
            # ------------------------------------------------

            elif isinstance(value, dict):

                self.build_tree(value, item)

            # ------------------------------------------------
            # INTEGER
            # ------------------------------------------------

            elif isinstance(value, int):

                spin = QSpinBox()

                spin.setMinimum(0)

                spin.setValue(value)

                self.tree.setItemWidget(
                    item,
                    1,
                    spin
                )

                self.spinbox_map[key] = spin

                self.widget_map[key] = spin

            # ------------------------------------------------
            # STRING
            # ------------------------------------------------

            else:

                line = QLineEdit()

                line.setText(str(value))

                self.tree.setItemWidget(
                    item,
                    1,
                    line
                )

                self.widget_map[key] = line

    # =====================================================

    def create_array_group(
        self,
        parent_item,
        array_name,
        array_schema
    ):

        count_field = array_schema[
            "_count_field"
        ]

        children_schema = array_schema[
            "children"
        ]

        count_spinbox = self.spinbox_map.get(
            count_field
        )

        if count_spinbox:

            count = count_spinbox.value()

        else:

            count = 1

        array_container = QTreeWidgetItem(
            parent_item
        )

        array_container.setText(
            0,
            f"{array_name}[]"
        )

        self.populate_array_items(
            array_container,
            children_schema,
            count
        )

        if count_spinbox:

            count_spinbox.valueChanged.connect(

                lambda value,
                container=array_container,
                schema=children_schema:

                self.update_array_items(
                    container,
                    schema,
                    value
                )
            )

    # =====================================================

    def populate_array_items(
        self,
        container,
        schema,
        count
    ):

        for i in range(count):

            item = QTreeWidgetItem(container)

            item.setText(
                0,
                f"Item {i+1}"
            )

            self.build_tree(schema, item)

    # =====================================================

    def update_array_items(
        self,
        container,
        schema,
        count
    ):

        while container.childCount() > 0:

            container.removeChild(
                container.child(0)
            )

        self.populate_array_items(
            container,
            schema,
            count
        )

    # =====================================================
    # EVENTS
    # =====================================================

    def on_api_selected(self):

        self.clear_tree()

        curr_text = self.api_dropdown.currentText()

        api_data = API_CONFIG[curr_text]

        schema = api_data["schema"]

        self.current_schema = schema

        self.build_tree(
            schema,
            self.tree.invisibleRootItem()
        )

        self.tree.expandAll()

    # =====================================================
    # BUILD PAYLOAD
    # =====================================================

    def build_payload(self):

        def extract(item):

            result = {}

            for i in range(item.childCount()):

                child = item.child(i)

                key = child.text(0)

                # ----------------------------------------
                # ARRAY
                # ----------------------------------------

                if key.endswith("[]"):

                    arr = []

                    for j in range(
                        child.childCount()
                    ):

                        arr.append(
                            extract(
                                child.child(j)
                            )
                        )

                    result[key[:-2]] = arr

                # ----------------------------------------
                # STRUCT
                # ----------------------------------------

                elif child.childCount() > 0:

                    result[key] = extract(child)

                # ----------------------------------------
                # FIELD
                # ----------------------------------------

                else:

                    widget = self.tree.itemWidget(
                        child,
                        1
                    )

                    if isinstance(
                        widget,
                        QLineEdit
                    ):

                        result[key] = widget.text()

                    elif isinstance(
                        widget,
                        QSpinBox
                    ):

                        result[key] = widget.value()

            return result

        return extract(
            self.tree.invisibleRootItem()
        )

    # =====================================================
    # CONFIG
    # =====================================================

    def load_config(self):

        config_path = "config/config.json"

        if not os.path.exists(config_path):

            raise FileNotFoundError(
                "config.json not found"
            )

        with open(config_path) as f:

            return json.load(f)

    # =====================================================
    # CALL API
    # =====================================================

    def call_api(self):

        payload = self.build_payload()

        selected_api = (
            self.api_dropdown.currentText()
        )

        CONFIG = self.load_config()

        BASE_URL = CONFIG.get(
            "BASE_URL",
            "http://localhost:5000"
        )

        api_data = API_CONFIG[selected_api]

        url = f"{BASE_URL}{api_data['URL']}"

        self.status_label.setText(
            "⏳ Calling API..."
        )

        self.status_label.setStyleSheet(
            "color: orange;"
        )

        self.call_button.setEnabled(False)

        self.thread = APICallThread(
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

            self.status_label.setText(
                "❌ API Call Failed"
            )

            self.status_label.setStyleSheet(
                "color: red;"
            )

        else:

            self.status_label.setText(
                f"✅ Status Code: {status}"
            )

            self.status_label.setStyleSheet(
                "color: green;"
            )

        self.response_box.setText(

            json.dumps(
                result,
                indent=4
            )
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

            json.dumps(
                data,
                indent=4
            )
        )

    # =====================================================

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