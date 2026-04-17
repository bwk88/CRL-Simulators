#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 16:46:40 2025

@author: kuldeepsingh@Indigenous.com
"""

def cleanString(stringValue):
    strList = stringValue.split()
    newString = ""
    for index, wrd in enumerate(strList):
        if index==0:
            newString = newString+wrd
        else:
            newString = newString+" "+wrd
    return newString

