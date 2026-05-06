#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 10:44:24 2025

@author: kuldeepsingh@Indigenous.com
"""
import difflib
import inspect


class debuggerClass:
    def __init__(self):
        super().__init__()
        self.DebuggerMode = False
        self.InfoMode = False
        self.WhereMode = False
        self.COUNT = 0
    
    def setWhereMode(self, isSet):
        if isSet == True:
            self.WhereMode = True
        if isSet == False:
            self.WhereMode = False
    
    def setInfomationMode(self,isSet):
        if isSet == True:
            self.InfoMode = True
        if isSet == False:
            self.InfoMode = False
            
    def setDebuggingMode(self,isSet):
        if isSet == True:
            self.DebuggerMode = True
        if isSet == False:
            self.DebuggerMode = False
            
    def setCallerPrintMode(self, isSet):
        if isSet == True:
            self.CallerPrintMode = True
        if isSet == False:
            self.CallerPrintMode = False
    
    # To print when funtction is called
    def printWhere(self):
        if self.WhereMode == True:
            self.COUNT+=1
            caller = inspect.stack()[1].function
            print("\n")
            print("===================== Call Stack =========================")
            print("\t\t",self.COUNT,"\t",caller,"")
            print("==========================================================")
        else:
            pass
    
    # Use it to print IMPORTANT Information
    def printInfo(self, *args, isPrint=False):
        if self.InfoMode == True:
            if isPrint:  
                caller = inspect.stack()[1].function
                print("\n")
                print("------------------- INFO --------------------------")
                print(*args)
                print("---------------------------------------------------")

        else:
            pass
    
    # Use it to print anything
    def printDebug(self, *args, isPrint=False):  
        if self.DebuggerMode == True:
            if isPrint:
                if self.CallerPrintMode == True:
                    caller = inspect.stack()[1].function
                    print(caller,":\t",*args)
                else:
                    print(*args)
        else:
            pass
        

    # Use it to print anything
    def printDebugLine(self, *args, isPrint=False):   
        if self.DebuggerMode == True:
            if isPrint:
                if self.CallerPrintMode == True:
                    caller = inspect.stack()[1].function
                    print(caller,":\t",*args, end="")
                else:
                    print(*args, end="")
        else:
            pass


    # compare the difference in two versions of code (diff_report.html shall be created)
    def openDifferences(self, file1, file2):
        with open(file1) as f1, open(file2) as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            
            html_diff = difflib.HtmlDiff().make_file(lines1, lines2, fromdesc='Old Version', todesc='New Version')
        with open('diff_report.html', 'w') as out:
            out.write(html_diff)

            
DBUG = debuggerClass()