#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 10:24:05 2025

@author: kuldeepsingh@Indigenous.com
"""

import timeit

setup_code = """
data = {"name":"python"}
"""

direct_code = """
print(data["name"])
for i in range(0,100):
    print(data["name"])
"""

variable_code = """
msg = data["name"]
for i in range(0,100):
    print(msg)
"""

direct_time = timeit.timeit(direct_code, setup = setup_code, number = 100000)
variable_time = timeit.timeit(variable_code, setup = setup_code, number = 100000)

print("Direct dictionary reference: ", direct_time)
print("Varible assignment reference: ", variable_time)

print("done")