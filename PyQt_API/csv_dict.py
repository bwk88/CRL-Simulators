import pandas as pd
csv_file = "config/API_details.xlsx"
dict={}
names = []

def csv_dict_func(csv_file):
    df = pd.read_excel(csv_file)
    msg_name = ""

    for index ,bitName in enumerate(df['API Name']):
        # print(index, bitName)
        if pd.notnull(bitName): #checking wether the cell is empty or not
            print(index, bitName)
            dict[bitName] = []
            msg_name = bitName
        else:
            api_name = df.at[index,'API Name']
            api_exposing_module = df.at[index,'API_EXPOSING_MODULE']
            method_type = df.at[index,'METHOD_TYPE']
            url = df.at[index,'URL']
            # arr_size = df.at[index,'ARRAY_SIZE']
            request_struct_name = df.at[index,'REQUEST_STRUCT_NAME']
            request_arg_name = df.at[index,'REQUEST_ARGUMENT_NAME']
            request_type_name = df.at[index, 'REQUEST_ARGUMENT_TYPE']
            request_arg_desc = df.at[index,'REQUEST_ARGUMENT_DESC']
            request_arr_size = df.at[index,'REQUEST_ARRAY_SIZE']
            request_format = df.at[index,'REQUEST_FORMAT']
            request_bitField = df.at[index,'REQUEST_BITFIELD'] 
            #struct_array_size = df.at[index,'STRUCT_ARRAY_SIZE']
            # if pd.isnull(arr_size):
            #     arr_size = ''
            # if pd.isnull(input_val):
            #     input_val = '0'
            # if pd.isnull(arg_size):
            #     arg_size = 0 
            # if pd.isnull(bit_field):
            #     bit_field = 8 * int(arg_size)
            # if pd.isnull(format_val):
            #     format_val = ' ' 
            # if pd.isnull(irs_data):
            #     irs_data = "NO COMMENTS AVALIBLE"

            # if pd.isnull(struct_name):
            #     struct_name = ''

            # bit_field = int(bit_field) 
            msg_lst = [api_name, api_exposing_module, method_type, url, request_struct_name, request_arg_name, request_type_name, request_type_name, request_arg_desc,request_arr_size,request_format,request_bitField]

            if pd.isnull(api_name):
                continue
            
            dict[msg_name].append(msg_lst)

    # for key,items in dict.items():
    #     names.append(key)
    print("DICTIONARY",dict['SaveISACdata'])
    print("CSV to DICT Successful")
    print_dict()

def print_dict():
    for key,items in dict.items():
        if key == 'ACCCS_FIRE_PLAN':
            print(key,":")
            for lst in items:
                print(lst)
        else:
            pass 


csv_dict_func(csv_file)
