#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 29 11:45:03 2025

@author: kuldeepsingh@Indigenous.com
"""

from dataclasses import dataclass, field
import pandas as pd

@dataclass
class snsMessageDetails:
    messageIdenitifer: int
    message: str
    HeaderData: list
    InputData: list
    HeaderFormat: str
    ContentFormat: str
    periodicity: int
    delay: int

@dataclass
class SNS_FileOperations_delete_data:
    df: pd.DataFrame
    project: str
    functionName: str
    testCaseName: str
    messageIdentifier: str
    messageIdentifierOutput: int

@dataclass
class SNS_FileOperations_copy_data:
    df: pd.DataFrame
    project: str
    functionName: str
    testCaseName: str
    messageIdentifier: str
    messageIdentifierOutput: int
    counterInput: int
    counterOutput: int
    copyDataList: list
    
@dataclass
class mainWindow_SNS_save_edit_data:
    input_or_output: str
    save_or_edit: str
    messageIdenitifer: int
    Message_Name: str
    Header_format: str
    content_format: str
    header_data: object
    content_data: object
    periodicity: int
    delay: int
    
    
@dataclass
class snsOutputMessageDetails:
    messageIdenitifer: int
    message: str
    HeaderData: list
    InputData: list
    Header_format: list
    Content_format: list
    periodicity: int  

@dataclass
class copyData:
    location: str = ""
    dataList: list = field(default_factory=list)
