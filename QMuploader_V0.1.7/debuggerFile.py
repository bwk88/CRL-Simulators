#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  3 10:44:24 2025

@author: kuldeepsingh@Indigenous.com
"""
import difflib

class debuggerClass:
    def __init__(self):
        super().__init__()
        self.DebuggerMode = False
        
    def setDebuggingMode(self,isSet):
        if isSet == True:
            self.DebuggerMode = True
        if isSet == False:
            self.DebuggerMode = False
            
    def printWhere(self, functionName):
        print(f"=========================={functionName}================================")
    
    def printDebug(self, debugString):
        print(f"\n{debugString}")

    # compare the difference in two versions of code (diff_report.html shall be created)
    def openDifferences(self, file1, file2):
        with open(file1) as f1, open(file2) as f2:
            lines1 = f1.readlines()
            lines2 = f2.readlines()
            
            html_diff = difflib.HtmlDiff().make_file(lines1, lines2, fromdesc='Old Version', todesc='New Version')
        with open('diff_report.html', 'w') as out:
            out.write(html_diff)

            
debuggerInstance = debuggerClass()