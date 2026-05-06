from csv_dict import dict


def dynamic_struc(dynamic_content_format,no_of_struct_insert,idx,dict_idx):
    
    print("Dynamic strcut",dynamic_content_format)
    # print("Dynamic strcut fmt",fmt_tuple)
    print("struct Insert",no_of_struct_insert)
    print("CSV DICT",dict_idx[idx])
    
    format_string_to_be_repeated = dict_idx[idx][2]# 2 is index of dictionary
    print("repeat_struc_data ->",format_string_to_be_repeated)
    
    
    
    
    
    new_format_insert_pos = idx+1
    struct_format_to_be_inserted = []
    for i in range(new_format_insert_pos,len(dict_idx)):
        struc_contains = dict_idx[i][8].split('.')
        
        if format_string_to_be_repeated in struc_contains:
            struct_format_to_be_inserted.append(dict_idx[i][5])
            print(struc_contains)    

    
    # dynamic_content_format[insert_pos:insert_pos] = struc_format * (no_of_struct_insert - 1)
    if no_of_struct_insert > 1 and len(struct_format_to_be_inserted)!= 0:
        for i in range(no_of_struct_insert-1):
            print("Inserting------->",i)
            print("struct_format_to_be_inserted in loop",struct_format_to_be_inserted)
            dynamic_content_format.append(struct_format_to_be_inserted)
            # struct_format_to_be_inserted = struct_format_to_be_inserted * no_of_struct_insert
            # dynamic_content_format[insert_pos:insert_pos] = struct_format_to_be_inserted
    
    print("DYN FMT",len(dynamic_content_format),dynamic_content_format)
    
    return dynamic_content_format
    
  
        
        
    
    
    
    
    
    
    
    
    