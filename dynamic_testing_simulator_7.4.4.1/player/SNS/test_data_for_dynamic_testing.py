#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 16:51:05 2025

@author: saritajangra@Indigenous.com
"""
import pandas as pd
import os
from collections import defaultdict



SNS_FOLDER = "SNS/SAVEANDSEND"

# df = pd.read_excel('testing_data.xlsx')
# print(df.iloc[1])
#print(df)


def data_extraction(projectName):
    functions_dictionary = {}
    test_case_dictionary = {}
    temp = {}
    temp_test = []
    current_function = ''
    current_test_case = ''
    previous_function = ''

    df = pd.read_csv(f"{SNS_FOLDER}/{projectName}.csv")
    for index, function_name in enumerate(df['Function_Name']):
        if not pd.isna(function_name) and function_name != current_function:
            if current_function:
                functions_dictionary[current_function] = test_case_dictionary
            test_case_dictionary = {}
            current_function = function_name
            if not pd.isna(df.at[index, 'Test_Case']):
                temp = {}
                temp_test = []
                #temp.append(df.at[index, 'Test Name'])
                current_test_case = df.at[index, 'Test_Case']
                preconditions = str(df.at[index, 'Preconditions'])

            
            if not pd.isna(df.at[index, 'Message']):
                

                temp_test.append(df.at[index, 'Message'])
                temp_header_data = str(df.at[index, 'Header_Data']).strip('[]')
                temp_header_data = [x.strip() for x in temp_header_data.split(",")]
                temp_test.append(temp_header_data[0:8])
                temp_input_data = str(df.at[index, 'Input_Data']).strip('[]')
                temp_test.append([x.strip() for x in temp_input_data.split(",")])
                temp_test.append(df.at[index, 'Periodicity'])
                temp_test.append(df.at[index, 'Delay'])
                content_format = str(df.at[index, 'content_format'])
                temp_test.append(content_format)
                test_case_dictionary[current_test_case] = []
                test_case_dictionary[current_test_case].append(preconditions)
                test_case_dictionary[current_test_case].append(temp_test)

                 
            
        elif pd.isna(function_name):
            if not pd.isna(df.at[index, 'Test_Case']):
                #temp.append(df.at[index, 'Test Name'])
                current_test_case = df.at[index, 'Test_Case']
                preconditions = str(df.at[index, 'Preconditions'])
                #test_case_dictionary = {}
            temp_test = []
            if not pd.isna(df.at[index, 'Message']):

                temp_test.append(df.at[index, 'Message'])
                temp_header_data = str(df.at[index, 'Header_Data']).strip('[]')
                temp_header_data = [x.strip() for x in temp_header_data.split(",")]
                temp_test.append(temp_header_data[0:8])                 
                temp_input_data = str(df.at[index, 'Input_Data']).strip('[]')
                temp_test.append([x.strip() for x in temp_input_data.split(",")])
                temp_test.append(df.at[index, 'Periodicity'])
                temp_test.append(df.at[index, 'Delay'])
                content_format = str(df.at[index, 'content_format'])
                temp_test.append(content_format)    
                if current_test_case in test_case_dictionary:
                    test_case_dictionary[current_test_case].append(temp_test)
                else:
                    test_case_dictionary[current_test_case] = []
                    test_case_dictionary[current_test_case].append(preconditions)
                    test_case_dictionary[current_test_case].append(temp_test)
                #temp.append(test_case_dictionary)
                     
                     
    functions_dictionary[current_function] = test_case_dictionary
    #print(functions_dictionary)
    return functions_dictionary

def output_extraction(projectName, function, test_case):
    output_dictionary = {}
    test_case_dictionary = {}
    temp = {}
    temp_test = []
    current_function = ''
    current_test_case = ''
    previous_function = ''

    df = pd.read_csv(f"{SNS_FOLDER}/{projectName}.csv")
    for index, function_name in enumerate(df['Function_Name']):
        if not pd.isna(function_name) and function_name != current_function:
            if current_function:
                output_dictionary[current_function] = test_case_dictionary
            test_case_dictionary = {}
            current_function = function_name
            if not pd.isna(df.at[index, 'Test_Case']):
                temp = {}
                temp_test = []
                #temp.append(df.at[index, 'Test Name'])
                current_test_case = df.at[index, 'Test_Case']
                test_case_dictionary[current_test_case] = []
                
            if not pd.isna(df.at[index, 'expected_output_message']):
                

                temp_test.append(df.at[index, 'expected_output_message'])
                temp_content_data = str(df.at[index, 'output_content']).strip('[]')
                temp_test.append([x.strip() for x in temp_content_data.split(",")])
                temp_test.append(df.at[index, 'output_periodicity'])
                content_format = str(df.at[index, 'output_content_format'])
                temp_test.append(content_format)  
                #test_case_dictionary[current_test_case] = []
                test_case_dictionary[current_test_case].append(temp_test)
                #temp.append(test_case_dictionary)
            
                 
            
        elif pd.isna(function_name):
            if not pd.isna(df.at[index, 'Test_Case']):
                current_test_case = df.at[index, 'Test_Case']
                test_case_dictionary[current_test_case] = []
                #test_case_dictionary = {}
            temp_test = []
            if not pd.isna(df.at[index, 'expected_output_message']):


                temp_test.append(df.at[index, 'expected_output_message'])
                temp_content_data = str(df.at[index, 'output_content_data']).strip('[]')
                temp_test.append([x.strip() for x in temp_content_data.split(",")])
                temp_test.append(df.at[index, 'output_periodicity'])
                content_format = str(df.at[index, 'output_content_format'])
                temp_test.append(content_format) 
                

                test_case_dictionary[current_test_case].append(temp_test)

                     
                     
    output_dictionary[current_function] = test_case_dictionary

    f1 = output_dictionary[function]
    t1 = f1[test_case]
    output_messages = []
    

    for i in t1:
        t = (i[0], i[1:])
        output_messages.append(t)
    return output_messages


#print(data_extraction('abc'))
#print(output_extraction("abc", 'f1', 't1'))
    





    
                    
            
            
    



        

        

 
    


