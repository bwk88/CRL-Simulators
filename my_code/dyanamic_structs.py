import pandas as pd
import json
# from debuggerFile import DBUG
csv_file = "config/message_details (copy).xlsx"
# csv_file_main = "config/message_details.xlsx"
csv_file_main = "config_test/API_details(temp).ods"
dyanamic_dict={}
attriute_irs = {}



def recursiveCall(df, index, dataTotalLength, currentStruct):
    # print(index, dataTotalLength)
    while(index<dataTotalLength):
        # print(df['ARGUMENT_NAME'][index], df['ATR_ARRAY_SIZE'][index], df['StructureName'][index])
        
        # 1: Find structure starting varible row, "no of rakes" >> "struct_rakes" and create new sturcture and go in recursion to add data
        # 
        # check if repeating structure or not
        if pd.notnull(df['ATR_ARRAY_SIZE'][index]):
            
            # check if is first iteration
            if currentStruct!='':
                
                # adding already found structure
                # check if structure is already added to dynamic_dict
                if currentStruct in dyanamic_dict:
                    # check if it is attribute or empty lines
                    if pd.notnull(df['StructureName'][index]):
                        attributeAndParents = df['StructureName'][index].split(".")
                        # check if current attribute is part of current structure or not 
                        if currentStruct in attributeAndParents:
                            temp = {}
                            temp = createRowData(df, index)
                            
                            attributeName = df["ARGUMENT_NAME"][index]
                            attributeStructures = df["StructureName"][index]
                                
                            if pd.isnull(df['ATR_ARRAY_SIZE'][index]):
                                attributeDynamicStructure = ''
                            else:
                                attributeDynamicStructure = df["ATR_ARRAY_SIZE"][index]
                                
                            if pd.isnull(df['STATIC_ARRAY_SIZE'][index]):
                                attributeStaticStructureSize = 0
                            else:
                                attributeStaticStructureSize = int(df["STATIC_ARRAY_SIZE"][index])
                            
                            
                            if pd.isnull(df['INPUT_VALUE'][index]):
                                defaultInput = 0
                                temp["defaultInput"] = 0
                            else:
                                temp["defaultInput"] = int(df['INPUT_VALUE'][index])

                            # attrVaribleData = (attributeName, attributeStructures, attributeDynamicStructure, attributeStaticStructureSize, defaultInput)
                            attrVaribleData = {
                                    "name": attributeName, 
                                    "structures": attributeStructures, 
                                    "dyanamicStruct": attributeDynamicStructure, 
                                    "staticStructSize": attributeStaticStructureSize, 
                                    "defaultInput": defaultInput
                                }
                            
                            # Add, add struct defining row to its own structure
                            dyanamic_dict[currentStruct].append(attrVaribleData)
                            
                            if attributeName not in attriute_irs:
                                attriute_irs[attributeName] = temp
                                
                            # Add new structure 
                            attrVaribleData = {
                                "name": "<<NestedStruct>>"+df['ATR_ARRAY_SIZE'][index]
                                }
                            dyanamic_dict[currentStruct].append(attrVaribleData)                                  
                            
            
            # else:
            nextStruct = df['ATR_ARRAY_SIZE'][index]
            dyanamic_dict[nextStruct] = []
            
            index+=1
            index = recursiveCall(df, index, dataTotalLength, nextStruct)
            # print("Current structure>>",currentStruct)
        else:
            # Processing of all rows other than where new structure is introduced (where attr_arr_size != empty)
            # skip empty lines
            if pd.notnull(df['StructureName'][index]):
                struct_contains = df['StructureName'][index].split(".")
                
                # Get out of recursion if the structure rows are finished
                if currentStruct!='' and currentStruct not in struct_contains:
                    return index-1
                
                # If reach here, check if structure is already added before if added add its elements
                if currentStruct in dyanamic_dict:
                        attributeAndParents = df['StructureName'][index].split(".")
                        
                        # check if current row is part of structure
                        if currentStruct in attributeAndParents:
                            
                            # add to dynamic structure
                            temp = createRowData(df, index)
                            
                            attributeName = df["ARGUMENT_NAME"][index]
                            attributeStructures = df["StructureName"][index]
                            
                            if pd.isnull(df['ATR_ARRAY_SIZE'][index]):
                                attributeDynamicStructure = ''
                            else:
                                attributeDynamicStructure = df["ATR_ARRAY_SIZE"][index]
                                
                            if pd.isnull(df['STATIC_ARRAY_SIZE'][index]):
                                attributeStaticStructureSize = 0
                            else:
                                attributeStaticStructureSize = int(df["STATIC_ARRAY_SIZE"][index])
                                
                            if pd.isnull(df['INPUT_VALUE'][index]):
                                defaultInput = 0
                                temp["defaultInput"] = 0
                            else:
                                temp["defaultInput"] = int(df['INPUT_VALUE'][index])

                            attrVaribleData = {
                                    "name": attributeName, 
                                    "structures": attributeStructures, 
                                    "dyanamicStruct": attributeDynamicStructure, 
                                    "staticStructSize": attributeStaticStructureSize, 
                                    "defaultInput": defaultInput
                                }
                            
                            dyanamic_dict[currentStruct].append(attrVaribleData)  
                            
                            if attributeName not in attriute_irs:
                                attriute_irs[attributeName] = temp

                    
        index+=1
        
    # print(dyanamic_dict)
    return index      

def createRowData(df, index):           
    temp = {}
         
    if pd.isnull(df['BitField'][index]):
        temp["bitField"] = 0
    else:
        temp["bitField"] = int(df['BitField'][index])
        
    if pd.isnull(df['FORMAT'][index]): 
        temp["AttributeFormat"] = ''
    else:
        temp["AttributeFormat"] = df['FORMAT'][index]
        
    if pd.isnull(df['IRS_VALUE'][index]):
        temp["irsValue"] = "NO COMMENTS AVALIBLE"
    else:
        temp["irsValue"] = df['IRS_VALUE'][index]
        
    if pd.isnull(df['ARGUMENT_SIZE'][index]):
        temp["arg_size"] = 0
    else:
        temp["arg_size"] = df['ARGUMENT_SIZE'][index]
    

        
    return temp


def generate_dyanamic_data(csv_file):
    df = pd.read_excel(csv_file)
    # print(df)
    msg_name = ""
    
    index=0
    currentStuct = ""
    dataTotalLength = len(df['ATR_ARRAY_SIZE'])
    index = recursiveCall(df, index, dataTotalLength, currentStuct)
    
    with open("dyanmaic_data.json", "w") as f:
        json.dump(dyanamic_dict, f, indent=4)
    
    with open("dyanmaic_irs.json", "w") as f:
        json.dump(attriute_irs, f, indent=4)

def loadDyanamic_data(struct_path, attribute_path ):
    DyanamicStructData = {}
    attriute_irs = {}
    with open(struct_path, "r") as f:
        DyanamicStructData=json.load(f)
    f.close()
    
    with open(attribute_path, "r") as fl:
        attriute_irs=json.load(fl)
    fl.close()
    
    #printStructAndAttributes(DyanamicStructData, "struct_rake_response_packet", attriute_irs)

    return DyanamicStructData, attriute_irs


def printStructAndAttributes(DyanamicStructData, printingStructure, attriute_irs):
    DBUG.printDebug("===============", printingStructure, "==============")
    i=1
    for items in DyanamicStructData[printingStructure]:
        # attr_struct = printattriute_irs(attriute_irs, items[0]).split(".")[-1]
        DBUG.printDebug("-----", i," : ", items["name"])
        i+=1
       
def printattriute_irs(attriute_irs, attribute):
    return attriute_irs[attribute]["AttributeFormat"]  

          
generate_dyanamic_data(csv_file_main) 
loadDyanamic_data("dyanmaic_data.json", "dyanmaic_irs.json")






