# api_dict.py

import pandas as pd


# ============================================================
# GLOBAL CONFIG
# ============================================================

EXCEL_FILE = "config/message_details.xlsx"

API_CONFIG = {}


# ============================================================
# LOAD EXCEL
# ============================================================

def load_excel_metadata():

    df = pd.read_excel(EXCEL_FILE)

    current_msg = None

    temp_fields = {}

    for index, row in df.iterrows():

        msg_name = row.get("MESSAGE_NAME")

        # ----------------------------------------------------
        # NEW MESSAGE
        # ----------------------------------------------------

        if pd.notnull(msg_name):

            current_msg = str(msg_name).strip()

            API_CONFIG[current_msg] = {

                "URL": f"/{current_msg.lower()}",

                "Method Type": "POST",

                "fields": [],

                "schema": {}
            }

            continue

        # ----------------------------------------------------
        # SKIP INVALID
        # ----------------------------------------------------

        if current_msg is None:
            continue

        arg_name = row.get("ARGUMENT_NAME")

        if pd.isnull(arg_name):
            continue

        arg_name = str(arg_name).strip()

        structure_name = row.get("StructureName")

        if pd.isnull(structure_name):
            structure_name = ""

        structure_name = str(structure_name).strip()

        arg_type = row.get("ARGUMENT_TYPE")

        if pd.isnull(arg_type):
            arg_type = "STRING"

        arg_type = str(arg_type).strip()

        arr_size = row.get("ATR_ARRAY_SIZE")

        if pd.isnull(arr_size):
            arr_size = ""

        arr_size = str(arr_size).strip()

        # ----------------------------------------------------
        # STORE FIELD
        # ----------------------------------------------------

        field_obj = {

            "arg_name": arg_name,

            "structure_name": structure_name,

            "arg_type": arg_type,

            "array_size_field": arr_size
        }

        API_CONFIG[current_msg]["fields"].append(
            field_obj
        )

    # --------------------------------------------------------
    # BUILD SCHEMAS
    # --------------------------------------------------------

    for msg_name in API_CONFIG:

        schema = build_schema(

            API_CONFIG[msg_name]["fields"]
        )

        API_CONFIG[msg_name]["schema"] = schema


# ============================================================
# BUILD SCHEMA
# ============================================================

def build_schema(fields):

    root = {}

    # --------------------------------------------------------
    # ARRAY MAP
    # --------------------------------------------------------

    array_map = {}

    for field in fields:

        if field["array_size_field"] != "":

            array_map[
                field["array_size_field"]
            ] = field["arg_name"]

    # --------------------------------------------------------
    # BUILD TREE
    # --------------------------------------------------------

    for field in fields:

        arg_name = field["arg_name"]

        structure_name = field["structure_name"]

        arg_type = field["arg_type"]

        path_parts = []

        if structure_name != "":

            path_parts = structure_name.split(".")

        current = root

        # ----------------------------------------------------
        # CREATE STRUCTURE PATH
        # ----------------------------------------------------

        for part in path_parts:

            if part not in current:

                current[part] = {}

            current = current[part]

        # ----------------------------------------------------
        # ARRAY NODE
        # ----------------------------------------------------

        if arg_name in array_map:

            current[arg_name] = {

                "_is_array": True,

                "_count_field": array_map[arg_name],

                "children": {}
            }

        # ----------------------------------------------------
        # INTEGER FIELD
        # ----------------------------------------------------

        else:

            if "INT" in arg_type.upper():

                current[arg_name] = 0

            else:

                current[arg_name] = ""

    # --------------------------------------------------------
    # FIX ARRAY CHILDREN
    # --------------------------------------------------------

    fix_array_children(root)

    return root


# ============================================================
# FIX ARRAY CHILDREN
# ============================================================

def fix_array_children(node):

    if not isinstance(node, dict):
        return

    keys = list(node.keys())

    for key in keys:

        value = node[key]

        # ----------------------------------------------------
        # ARRAY
        # ----------------------------------------------------

        if (

            isinstance(value, dict)

            and value.get("_is_array")

        ):

            children = {}

            sibling_keys = list(node.keys())

            index = sibling_keys.index(key)

            # ------------------------------------------------
            # MOVE FOLLOWING STRUCTS INSIDE ARRAY
            # ------------------------------------------------

            for sibling in sibling_keys[index + 1:]:

                children[sibling] = node[sibling]

            # Remove moved siblings
            for sibling in children:

                del node[sibling]

            value["children"] = children

            fix_array_children(children)

        # ----------------------------------------------------
        # NORMAL STRUCT
        # ----------------------------------------------------

        elif isinstance(value, dict):

            fix_array_children(value)


# ============================================================
# LOAD EVERYTHING
# ============================================================

load_excel_metadata()


# ============================================================
# DEBUG
# ============================================================

if __name__ == "__main__":

    import json

    for key in API_CONFIG:

        print("\n==============================")
        print("MESSAGE:", key)
        print("==============================")

        print(

            json.dumps(
                API_CONFIG[key]["schema"],
                indent=4
            )
        )