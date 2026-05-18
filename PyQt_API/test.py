import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QLineEdit,
    QSpinBox
)

# ============================================================
# DYNAMIC SCHEMA
# ============================================================

schema = {

    "struct_message_header": {

        "src_agency_id": "",
        "dest_agency_id": "",
        "msg_id": ""
    },

    "struct_config_indri_input_source_list": {

        "no_of_indri": 1,

        "struct_config_indri_input_source": {

            "_is_array": True,
            "_count_field": "no_of_indri",

            "children": {

                "indri_id": "",
                "indri_name": "",

                "no_of_indri_input_source": 1,

                "struct_indri_input_source": {

                    "_is_array": True,
                    "_count_field": "no_of_indri_input_source",

                    "children": {

                        "indri_input_source": "",
                        "ip_address": ""
                    }
                }
            }
        }
    }
}


# ============================================================
# MAIN GUI
# ============================================================

class DynamicGUI(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("Dynamic Array GUI")

        self.resize(900, 700)

        layout = QVBoxLayout()

        self.tree = QTreeWidget()

        self.tree.setColumnCount(2)

        self.tree.setHeaderLabels(["Field", "Value"])

        layout.addWidget(self.tree)

        self.setLayout(layout)

        # Store references
        self.spinbox_map = {}

        # Build tree
        self.build_tree(schema, self.tree.invisibleRootItem())


    # ========================================================
    # MAIN RECURSIVE FUNCTION
    # ========================================================

    def build_tree(self, data, parent):

        for key, value in data.items():

            item = QTreeWidgetItem(parent)

            item.setText(0, key)

            # ------------------------------------------------
            # ARRAY STRUCTURE
            # ------------------------------------------------

            if isinstance(value, dict) and value.get("_is_array"):

                self.create_array_group(
                    parent_item=item,
                    array_name=key,
                    array_schema=value
                )

            # ------------------------------------------------
            # NORMAL STRUCTURE
            # ------------------------------------------------

            elif isinstance(value, dict):

                self.build_tree(value, item)

            # ------------------------------------------------
            # INTEGER FIELD -> SPINBOX
            # ------------------------------------------------

            elif isinstance(value, int):

                spin = QSpinBox()

                spin.setValue(value)

                spin.setMinimum(0)

                self.tree.setItemWidget(item, 1, spin)

                self.spinbox_map[key] = spin

            # ------------------------------------------------
            # NORMAL FIELD
            # ------------------------------------------------

            else:

                edit = QLineEdit()

                edit.setText(str(value))

                self.tree.setItemWidget(item, 1, edit)


    # ========================================================
    # CREATE ARRAY GROUP
    # ========================================================

    def create_array_group(
        self,
        parent_item,
        array_name,
        array_schema
    ):

        count_field = array_schema["_count_field"]

        children_schema = array_schema["children"]

        # Get count from corresponding spinbox
        count_spinbox = self.spinbox_map.get(count_field)

        if count_spinbox:

            count = count_spinbox.value()

        else:

            count = 1

        # Container item
        array_container = QTreeWidgetItem(parent_item)

        array_container.setText(0, f"{array_name}[]")

        # Initial render
        self.populate_array_items(
            array_container,
            children_schema,
            count
        )

        # Dynamic update connection
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


    # ========================================================
    # POPULATE ARRAY ITEMS
    # ========================================================

    def populate_array_items(
        self,
        container,
        schema,
        count
    ):

        for i in range(count):

            item = QTreeWidgetItem(container)

            item.setText(0, f"Item {i+1}")

            self.build_tree(schema, item)


    # ========================================================
    # UPDATE ARRAY ITEMS DYNAMICALLY
    # ========================================================

    def update_array_items(
        self,
        container,
        schema,
        count
    ):

        # Remove existing children
        while container.childCount() > 0:

            container.removeChild(
                container.child(0)
            )

        # Recreate
        self.populate_array_items(
            container,
            schema,
            count
        )


# ============================================================
# RUN
# ============================================================

app = QApplication(sys.argv)

window = DynamicGUI()

window.show()

sys.exit(app.exec_())