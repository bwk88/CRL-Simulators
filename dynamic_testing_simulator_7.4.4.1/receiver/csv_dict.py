import pandas as pd
csv_file = "config/message_details.xlsx"
dict={}
names = []

def csv_dict_func(csv_file):
    df = pd.read_excel(csv_file)
    msg_name = ""

    for index ,bitName in enumerate(df['MESSAGE_NAME']):
        # print(bitName)
        if pd.notnull(bitName): #checking wether the cell is empty or not
            print(index, bitName)
            dict[bitName] = []
            msg_name = bitName
        else:
            struct_name = df.at[index,'StructureName']
            arg_name = df.at[index,'ARGUMENT_NAME']
            arg_type = df.at[index,'ARGUMENT_TYPE']
            arr_size = df.at[index,'ARRAY_SIZE']
            # arr_size = df.at[index,'ARRAY_SIZE']
            arg_size = df.at[index,'ARGUMENT_SIZE']
            input_val = df.at[index,'INPUT_VALUE']
            format_val = df.at[index,'FORMAT']
            bit_field = df.at[index, 'BitField']
            irs_data = df.at[index,'IRS_VALUE']
            struct_array_size = df.at[index,'ARRAY_SIZE']
            static_array_length = df.at[index, 'STATIC_ARRAY_SIZE']
            
            if pd.isnull(arr_size):
                arr_size = ''
            if pd.isnull(input_val):
                input_val = '0'
            if pd.isnull(arg_size):
                arg_size = 1 
            if pd.isnull(bit_field):
                bit_field = 8 * int(arg_size)
            if pd.isnull(format_val): 
                format_val = ' ' 
            if pd.isnull(irs_data):
                irs_data = "NO COMMENTS AVALIBLE"

            if pd.isnull(struct_name):
                struct_name = ''

            if pd.isnull(struct_array_size):
                struct_array_size = ''
                
            if pd.isnull(static_array_length):
                static_array_length = 0

            bit_field = int(bit_field) 
            msg_lst = [arg_name, arg_type, arr_size, arg_size, input_val, format_val, bit_field, irs_data, struct_name, struct_array_size, int(static_array_length)]
            
            # if(msg_name == 'ATSS_DBA_VB_CMD_STATUS'):
            #     print("==============",index,struct_name)

            if pd.isnull(arg_name):
                continue
            
            dict[msg_name].append(msg_lst)

    # for key,items in dict.items():
    #     names.append(key)
    # print("DICTIONARY",dict['ATSS_PC_ATC_VIRTUAL_BLOCK_COMMAND_PACKET'],len(dict['ATSS_PC_ATC_VIRTUAL_BLOCK_COMMAND_PACKET']))
    print("CSV to DICT Successful")
    for i,item in enumerate(dict['ATSD_ATSS_HEADWAY_MODE_SETTING']):
        print(i,"-------------",item[0])
    # print_dict()

def print_dict():
    for key,items in dict.items():
        if key == 'ACCCS_FIRE_PLAN':
            print(key,":")
            for lst in items:
                print(lst)
        else:
            pass 


csv_dict_func(csv_file)

