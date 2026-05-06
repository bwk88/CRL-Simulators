def byte_data_parsing(complete_tuple,rcvd_format):
    try:
        content_list = []
        for x in range(0,len(complete_tuple)):
            if(isinstance(complete_tuple[x], bytes)):
                string = complete_tuple[x].decode('utf-8').rstrip('\x00')
                content_list.append(string)
            else:
                content_list.append(complete_tuple[x])
        # print("CONNNN",content_list)
        value_list = []
        for i,value in enumerate(content_list):
            # value = lineEdit.text()
            if 's' in rcvd_format[i]:
                value = bytes(value, 'utf-8')
            elif value == '' or value == ' ':
                # print('empty value')
                value = 0
            elif value == 'auto':
                value = 'auto'    
            else: 
                value = int(value)    
            value_list.append( value )
    except Exception as e:
        print("Error at byte conversion",e)
    return value_list