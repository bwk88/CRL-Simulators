#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 15 16:46:33 2025

@author: kuldeepsingh@Indigenous.com
"""


class global_data:
    def __init__(self):
        self.current_job_uploader = 0
        self.current_job_publisher = 0
        self.current_progress_value=0
        self.current_publisher_progress_value=0
        self.settingsData = {
                "Login_Username":"",
                "Login_password":"",
                "Project_link":"",
                "Current_Project":"",
                "Current_test_Plan":"",
                "Login_Username_publisher": "",
                "Login_password_publisher": "",
                "Project_link_publisher": "",
                "Current_Project_publisher": "",
                "Current_test_Plan_publisher":"",
                "Last_job_id":0,
                "Project_list":[],
                "Test_plan_list" : []
            }
        
        self.HistoryData = {
                "job_id":0,
                "job_type":"", #UPLOAD OR PUBLISH
                "Date":"",
                "Time":"",
                "ProgressStatus":0,
                "Status":"", #Finished/Ongoing
                "username":"",
                "password":"",
                "link":"",
                "Project":"",
                "TestPlan":""
            }
        
        self.DetailHistoryData = {
                #function_name : [test_case1, test_case2]
            }
        
        self.HistoryDataList = {
                #job_id = {History_data}
            }
        

data = global_data()