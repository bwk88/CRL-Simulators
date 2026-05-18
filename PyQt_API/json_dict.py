import pandas as pd
import json

csv_file = "config/message_details.xlsx"

api_data = {}
names = []


def csv_dict_func(csv_file):

    df = pd.read_excel(csv_file)

    msg_name = ""

    for index, bitName in enumerate(df['MESSAGE_NAME']):

        # New message starts
        if pd.notnull(bitName):

            print(index, bitName)

            api_data[bitName] = {
                "fields": [],
                "json_schema": {}
            }

            msg_name = bitName

        else:

            arg_name = df.at[index, 'ARGUMENT_NAME']
            arg_type = df.at[index, 'ARGUMENT_TYPE']
            arg_size = df.at[index, 'ARGUMENT_SIZE']

            struct_name = df.at[index, 'StructureName']

            arr_size = df.at[index, 'ATR_ARRAY_SIZE']

            input_val = df.at[index, 'INPUT_VALUE']

            format_val = df.at[index, 'FORMAT']

            bit_field = df.at[index, 'BitField']

            irs_data = df.at[index, 'IRS_VALUE']

            static_array_length = df.at[index, 'STATIC_ARRAY_SIZE']

            # ----------------------------
            # NULL HANDLING
            # ----------------------------

            if pd.isnull(arg_name):
                continue

            if pd.isnull(struct_name):
                struct_name = ""

            if pd.isnull(arr_size):
                arr_size = ""

            if pd.isnull(arg_size):
                arg_size = 0

            if pd.isnull(input_val):
                input_val = "0"

            if pd.isnull(format_val):
                format_val = ""

            if pd.isnull(bit_field):
                bit_field = 8 * int(arg_size)

            if pd.isnull(irs_data):
                irs_data = ""

            if pd.isnull(static_array_length):
                static_array_length = 0

            # ----------------------------
            # FIELD OBJECT
            # ----------------------------

            field_obj = {

                "arg_name": arg_name,

                "arg_type": arg_type,

                "arg_size": int(arg_size),

                "input_val": input_val,

                "format_val": format_val,

                "bit_field": int(bit_field),

                "irs_data": irs_data,

                "full_path": struct_name,

                "array_size_field": arr_size,

                "static_array_length": int(static_array_length)
            }

            api_data[msg_name]["fields"].append(field_obj)

    print("CSV to DICT Successful")


# ============================================================
# BUILD NESTED JSON SCHEMA
# ============================================================

def build_json_schema(message_fields):

    root = {}

    array_map = {}

    # -----------------------------------
    # First pass -> detect arrays
    # -----------------------------------

    for field in message_fields:

        if field["array_size_field"] != "":

            array_map[field["array_size_field"]] = field["arg_name"]

    # -----------------------------------
    # Second pass -> build hierarchy
    # -----------------------------------

    for field in message_fields:

        full_path = field["full_path"]

        arg_name = field["arg_name"]

        path_parts = []

        if full_path != "":
            path_parts = full_path.split(".")

        current = root

        # Create nested structures
        for part in path_parts:

            if part not in current:
                current[part] = {}

            current = current[part]

        # -----------------------------------
        # ARRAY STRUCTURE
        # -----------------------------------

        if arg_name in array_map:

            current[arg_name] = [
                {
                    "_array_count_field":
                    array_map[arg_name]
                }
            ]

        else:

            current[arg_name] = ""

    return root


# ============================================================
# MAIN
# ============================================================

csv_dict_func(csv_file)

# Build JSON schemas
for msg_name in api_data:

    schema = build_json_schema(
        api_data[msg_name]["fields"]
    )

    api_data[msg_name]["json_schema"] = schema


# ============================================================
# PRINT EXAMPLE
# ============================================================

example_msg = list(api_data.keys())[10]

print("\n==============================")
print("MESSAGE:", example_msg)
print("==============================\n")

print(
    json.dumps(
        api_data[example_msg]["json_schema"],
        indent=4
    )
)