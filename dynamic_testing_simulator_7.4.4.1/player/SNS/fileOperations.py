#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 14 12:30:11 2025

@author: kuldeepsingh@Indigenous.com
"""
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QTimer, QThread
import time, os, json
import pandas as pd
from debuggerFile import DBUG
from SNS.utility import insertDataInbetweenCSV


class fileOperations(QObject):
    readProjectCSVSignal = pyqtSignal()
    readCounterJSONSignal = pyqtSignal()
    deleteFunctionSignal = pyqtSignal(object)
    deleteTestCaseSignal = pyqtSignal(object)
    deleteMessageSignal = pyqtSignal(object)
    deleteOutputMessageSignal = pyqtSignal(object)
    copyTestCaseSignal = pyqtSignal(object)

    
    finishedDeleteFunctionSignal = pyqtSignal(str)
    finishedDeleteTestCaseSignal = pyqtSignal(str)
    finishedDeleteMessageSignal = pyqtSignal(int)
    finishedDeleteOutputMessageSignal = pyqtSignal(int)
    finishedCopyTestCaseSignal = pyqtSignal(int, int, object, list)
    
    
    def __init__(self):
        super().__init__()
        self.SNS_FOLDER = "SNS/SAVEANDSEND"
        self.deleteFunctionSignal.connect(self.deleteFunction)
        self.deleteTestCaseSignal.connect(self.deleteTestCase)
        self.deleteMessageSignal.connect(self.deleteMessage)
        self.deleteOutputMessageSignal.connect(self.deleteOutputMessage)
        self.copyTestCaseSignal.connect(self.pasteTestCase)

  
    
    # @pyqtSlot()    
    def isFilePresent(self,project):
        DBUG.printWhere()
        if os.path.exists(f"{self.SNS_FOLDER}/{project}.csv"):
            return True
        else:
            return False
        
    
    # @pyqtSlot(object)    
    def deleteFunction(self, deleteData):
        DBUG.printWhere()
        print(deleteData)
        DBUG.printDebug("Deleting the Function: ", deleteData.functionName)
        start = False
        dropIndexes = []

        if self.isFilePresent(deleteData.project):
            for index, row in deleteData.df.iterrows():
                if row["Function_Name"] == deleteData.functionName:
                    start = True
                    dropIndexes.append(index)
                    continue
                
                if start == True:
                    if not pd.isna(row["Function_Name"]):
                        start = False
                        break
                    else:
                        print(index, " To be deleted", deleteData.project)
                        dropIndexes.append(index)
                        
            deleteData.df.drop(index=dropIndexes, inplace=True) 
            deleteData.df.reset_index(drop=True, inplace=True)

                    
            deleteData.df.to_csv(f"{self.SNS_FOLDER}/{deleteData.project}.csv", index=False)
            print(deleteData.df["Function_Name"])
        else:
            print("file not present")
        self.finishedDeleteFunctionSignal.emit(deleteData.functionName)
        
        
    # @pyqtSlot(object)    
    def deleteTestCase(self, deleteData):
        DBUG.printWhere()
        DBUG.printDebug("Deleting the TestCase: ", deleteData.testCaseName)
        start = False
        isFunc = False
        dropIndexes = []
        if self.isFilePresent(deleteData.project):
            for i, row in deleteData.df.iterrows():
                if row["Function_Name"] == deleteData.functionName:
                    isFunc = True
                    continue
                
                if isFunc and (row["Test_Case"] == deleteData.testCaseName):
                    start = True
                    dropIndexes.append(i)
                    continue
                
                if start == True:
                    if not(pd.isna(row["Test_Case"])) or not(pd.isna(row["Function_Name"])):
                        start = False
                        break 
                    else:
                        print(i, " To be deleted", deleteData.project)
                        dropIndexes.append(i)
                        
            deleteData.df.drop(index=dropIndexes, inplace=True)
            deleteData.df.reset_index(drop=True, inplace=True)
            
            deleteData.df.to_csv(f"{self.SNS_FOLDER}/{deleteData.project}.csv", index=False)
        else:
            print("file not present")
        self.finishedDeleteTestCaseSignal.emit(deleteData.testCaseName)
    
    
    # @pyqtSlot(object)    
    def deleteMessage(self, deleteData):
        DBUG.printWhere()
        DBUG.printDebug("Deleting the MessageID: ", deleteData.messageIdentifier)
        start = False
        isFunc = False
        isTC = False
        dropIndexes = []
        
        if self.isFilePresent(deleteData.project):
            for i, row in deleteData.df.iterrows():
                if row["Function_Name"] == deleteData.functionName:
                    print("Function foound")
                    isFunc = True
                    continue
                
                if isFunc and (row["Test_Case"] == deleteData.testCaseName):
                    print("TC foound")
                    isTC = True
                    continue
                                  
                if isTC == True and (row["Msg_Identifier"] == deleteData.messageIdentifier):
                    print("MSG foound")
                    start = True
                    dropIndexes.append(i)
                    continue
                
                if start == True:
                    print("Deleting")
                    if not(pd.isna(row["Msg_Identifier"])) or not(pd.isna(row["Test_Case"])) or not(pd.isna(row["Function_Name"])):
                        start = False
                        break 
                    else:
                        print(i, " To be deleted", deleteData.project)
                        dropIndexes.append(i)
                        
            print("Drop indexes: ", dropIndexes)         
            deleteData.df.drop(index=dropIndexes, inplace=True)
            deleteData.df.reset_index(drop=True, inplace=True)           
            deleteData.df.to_csv(f"{self.SNS_FOLDER}/{deleteData.project}.csv", index=False)
        else:
            print("file not present")
        self.finishedDeleteMessageSignal.emit(deleteData.messageIdentifier)


    # @pyqtSlot(object)    
    def deleteOutputMessage(self, deleteData):
        DBUG.printWhere()
        DBUG.printDebug("Deleting the MessageID: ", deleteData.messageIdentifier)
        start = False
        isFunc = False
        isInp = False
        isTC = False
        dropIndexes = []
        
        if self.isFilePresent(deleteData.project):
            for i, row in deleteData.df.iterrows():
                if row["Function_Name"] == deleteData.functionName:
                    print("Function foound")
                    isFunc = True
                    continue
                
                if isFunc and (row["Test_Case"] == deleteData.testCaseName):
                    print("TC foound")
                    isTC = True
                    continue
                                  
                if isTC == True and (row["Msg_Identifier"] == deleteData.messageIdentifier):
                    print("MSG foound")
                    isInp = True
                    continue
                
                if isInp == True and (row["expected_output_message_Identifier"] == deleteData.messageIdentifierOutput):
                    print("Output MSG foound")
                    start = True
                    dropIndexes.append(i)
                    continue
                
                if start == True:
                    print("Deleting")
                    if not(pd.isna(row["expected_output_message_Identifier"])) or not(pd.isna(row["Msg_Identifier"])) or not(pd.isna(row["Test_Case"])) or not(pd.isna(row["Function_Name"])):
                        start = False
                        break 
                    else:
                        print(i, " To be deleted", deleteData.project)
                        dropIndexes.append(i)
                        
            print("Drop indexes: ", dropIndexes)         
            deleteData.df.drop(index=dropIndexes, inplace=True)
            deleteData.df.reset_index(drop=True, inplace=True)           
            deleteData.df.to_csv(f"{self.SNS_FOLDER}/{deleteData.project}.csv", index=False)
        else:
            print("file not present")
        self.finishedDeleteOutputMessageSignal.emit(deleteData.messageIdentifierOutput)


    # @pyqtSlot(object)    
    def pasteTestCase(self, copyData):
        DBUG.printWhere()
        print("Paste LIST", copyData.copyDataList)
        counterInput = copyData.counterInput
        counterOutput = copyData.counterOutput
        DBUG.printWhere()
        DBUG.printDebug("Deleting the TestCase: ", copyData.testCaseName)
        copiedList = []
        
        
        
        if self.isFilePresent(copyData.project):
            for tc in copyData.copyDataList:
                isFunction = False
                start = False
                foundEnd = False
                insertEnd = False
                startIndex = -1
                endIndex = -1
                splitIndex = -1
                
                # Copy data from file
                print("COPYING >> ", tc," ######>>>>>>>>> is insertEnd?", insertEnd," splitIndex: ", splitIndex, "start,foundEnd,insertEnd,startIndex,endIndex,splitIndex", start,foundEnd,insertEnd,startIndex,endIndex,splitIndex)
                for i, row in copyData.df.iterrows(): 
                    # Find function first
                    print(row["Function_Name"], copyData.functionName, tc)
                    if row["Function_Name"] == copyData.functionName:
                        isFunction = True
                        continue
                        
                    # Found testcase inside function and starting index
                    print(row["Test_Case"], tc)
                    if (row["Test_Case"] == tc) and isFunction:
                        print("test case found")
                        start = True
                        startIndex = i
                        continue
                    
                    # Testcase end index to be found
                    if start == True and foundEnd == False:
                        if not(pd.isna(row["Test_Case"])) or not(pd.isna(row["Function_Name"])):
                            print("non empyt testcase or function")
                            foundEnd = True
                            endIndex = i
                        else:
                            pass
                        
                    if start == True and not(pd.isna(row["Function_Name"])):
                        splitIndex = i
                        start = False
                        break
                
                # if reach end: no test case or function below it
                if endIndex == -1:
                    insertEnd = True
                    endIndex = len(copyData.df)
                
                # Last function with multiple test case and not last one is to be copied
                if splitIndex == -1:
                    insertEnd = True
                    
                print("is insertEnd?", insertEnd," splitIndex: ", splitIndex, "[start,foundEnd,insertEnd,startIndex,endIndex,splitIndex]", start,foundEnd,insertEnd,startIndex,endIndex,splitIndex)
                
                
                #  Paste at the end
                extracted_df = copyData.df.iloc[startIndex:endIndex].copy()
                
                for i, row in extracted_df.iterrows():
                    if not pd.isna(row["Test_Case"]):
                        test_case_list = copyData.df["Test_Case"].to_list()
                        count = 0
                        newTestCaseName = row['Test_Case']
                        while True:
                            if newTestCaseName in test_case_list:
                                if ("COPY_") in newTestCaseName:
                                    # print(newTestCaseName.split("COPY_")[-1])
                                    count = int(newTestCaseName.split("COPY_")[-1])+1
                                    newTestCaseName = f"{newTestCaseName.split('COPY_')[0]}COPY_{count}"
                                else:
                                    newTestCaseName = f"{newTestCaseName} COPY_{count}"
                                    count+=1
                            else:
                                break
                        

                        extracted_df.loc[i,"Test_Case"] = newTestCaseName
                        copiedList.append(newTestCaseName)
                        
                    if not pd.isna(row["Msg_Identifier"]):
                        extracted_df.loc[i,"Msg_Identifier"] = counterInput
                        counterInput+=1
                    if not pd.isna(row["expected_output_message_Identifier"]):
                        extracted_df.loc[i,"expected_output_message_Identifier"] = counterOutput
                        counterOutput+=1
                
                
                
                if insertEnd == True:
                    copyData.df = pd.concat([copyData.df, extracted_df], ignore_index=True)
                else:
                    copyData.df = insertDataInbetweenCSV(splitIndex, copyData.df, extracted_df)
                
            copyData.df.to_csv(f"{self.SNS_FOLDER}/{copyData.project}.csv", index=False) 
            self.finishedCopyTestCaseSignal.emit(counterInput, counterOutput, copyData.df, copiedList)

        else:
            print("file not present")
        

    
 
      
    