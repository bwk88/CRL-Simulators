#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 26 10:29:23 2025

@author: kuldeepsingh@Indigenous.com
"""

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
#from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as ec    
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import time
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import math
#from global_data import data
from PyQt5.QtCore import pyqtSignal , QObject, QTimer
from openpyxl import load_workbook
import re
from global_data import data
import sys, os
import json



error_test_cases = []
options=Options()
#options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--width=1920")
options.add_argument("--height=1080")
driver_path = os.getcwd()
service=Service(executable_path=f"{driver_path}/geckodriver")


#time.sleep(2)
test_suites_list = []
test_cases_list = []








class QLM_Publisher(QObject):
    progress_signal = pyqtSignal(str)
    update_signal_publish = pyqtSignal(str)
    error_signal_publish = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.progress_value = 0
        
        
        
    def start_process(self, startPublishData):
        self.update_signal_publish.emit("INITIATING PROCESS..........")
        # with open(path, 'w') as file:
        #     pass
        # file.close()
        self.stop = 0
        self.flag1 = 0
        self.page_number = 0
        self.currently_publish_test_suite = {}
        self.currently_publish_test_case = []
        self.last_test_suite_found_flag = 0
        self.startPublishData = startPublishData
        #self.file_name = self.startPublishData["Current_test_Plan_publisher"]+"_"+str(self.startPublishData["job_id"])
        os.makedirs(f"{driver_path}/{startPublishData['Current_test_Plan_publisher']}", exist_ok=True)
        self.file_name = f"{startPublishData['Current_test_Plan_publisher']}_{startPublishData['job_id']}"    # atc_tvpr_1 atc_tvpr_2 
        self.test_plan_name = f"{startPublishData['Current_test_Plan_publisher']}"
        self.path = f"{driver_path}/{startPublishData['Current_test_Plan_publisher']}/empty_test_case.txt"
        self.file_path = f"{driver_path}/{startPublishData['Current_test_Plan_publisher']}/{self.file_name}"
        #self.df = pd.read_excel(self.startProcessData["excel_path"])
        self.driver=webdriver.Firefox(service=service,options=options)
        self.driver.get(self.startPublishData["Project_link_publisher"])
        self.wait = WebDriverWait(self.driver, 30)
        #self.error_signal_publish.emit("Demo error occured now clear this line in qlm_publisher to remove")
        self.Login_process()
        self.progress_signal.emit(str(-1)) 
        self.update_signal_publish.emit("PROCESS FINISHED !!!!!!!!")
        self.driver.quit()
        
    def scrollnclickParent(self, x_path, selector, parent_driver):   
        if selector=="xpath":
            for i in range(3):
                try:
                    element = WebDriverWait(parent_driver, 10).until(ec.presence_of_element_located((By.XPATH, x_path)))
                    #element = parent_driver.find_element(By.XPATH, x_path)
                    self.driver.execute_script("""
                                          arguments[0].style.visibility='visible';
                                          arguments[0].style.display='block';
                                          arguments[0].style.position='relative';
                    """, element)
                    self.driver.execute_script("arguments[0].click();", element)
                    break
                except Exception:
                    if i == 2:
                        return 1
                    else:
                        time.sleep(1)
            
        if selector=="css":
            for _ in range(3):
                try:
                    element1 = WebDriverWait(parent_driver, 10).until(ec.presence_of_element_located((By.CSS_SELECTOR, x_path)))
                    #element1 = parent_driver.find_element(By.CSS_SELECTOR, x_path)
                    self.driver.execute_script("""
                                          arguments[0].style.visibility='visible';
                                          arguments[0].style.display='block';
                                          arguments[0].style.position='relative';
                    """, element1)
                    self.driver.execute_script("arguments[0].click();", element1)
                    break
                except Exception:
                    if i == 2:
                        return 1
                    else:
                        time.sleep(1)
            
        
        
    def scrollnclick(self, x_path):           
        for i in range(3):
            try:
                element = WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.XPATH, x_path))) 
            
                #element = driver.find_element(By.XPATH, x_path)
                self.driver.execute_script("""
                                      arguments[0].style.visibility='visible';
                                      arguments[0].style.display='block';
                                      arguments[0].style.position='relative';
                """, element)
                self.driver.execute_script("arguments[0].click();", element)
                break
            except Exception:
                if i == 2:
                    self.error_signal_publish.emit("Button not found/clickable")
                else:
                    time.sleep(1)
        
    def Login_process(self):
        self.update_signal_publish.emit("Logging in into the Quality Management")
        
        try:
            username = self.wait.until(ec.presence_of_element_located((By.NAME, "j_username")))
            password = self.wait.until(ec.presence_of_element_located((By.NAME, "j_password")))
            
            username.send_keys(self.startPublishData["Login_Username_publisher"])
            password.send_keys(self.startPublishData["Login_password_publisher"])
            
            
            self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
            
        except Exception:
            self.error_signal_publish.emit("Webpage not found/login elements not found")
            return
        
        try:
            self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_MenuPopup_6"))).click()
            self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_menu_MenuItem_0_text"))).click()
        except Exception:
            self.error_signal_publish.emit("Wrong Log in credentials/project selection element not found")
            return
        
        self.update_signal_publish.emit("Login successfully into the Quality Management")
        try:
            self.wait.until(ec.presence_of_element_located((By.XPATH,f"//*[text()='{self.test_plan_name}']"))).click()
            test_suites_button = self.wait.until(ec.element_to_be_clickable((By.XPATH,"//a[@title='Test Suites']")))
            test_suites_button.click()
        except Exception:
            self.error_signal_publish.emit("Project name/test suites of project elements not found/clickable")
            return
        self.find_Test_Suites()

        
    def create_document_template(self, document_name):
        columns = ['Function Name', 'PUI', 'Test Case Name', 'Scenario', 'Input', 'Expected Output']
        df = pd.DataFrame(columns = columns)
        df.to_excel(f"{document_name}.xlsx", index=False)
        with open(self.path, 'w') as file:
            pass
        
    def load_perviously_added_data(self):
        if not(os.path.exists(f"{self.file_path}.json")):
            with open(f"{self.file_path}.json", 'w') as f:
                temp_dict = {}
                json.dump(temp_dict, f)

        with open(f"{self.file_path}.json", 'r') as f:
            loaded_dict = json.load(f)
            return loaded_dict
        
    def find_Test_Suites(self):
        self.driver.refresh()
        try:
            test_suites_button = self.wait.until(ec.element_to_be_clickable((By.XPATH,"//a[@title='Test Suites']")))
            test_suites_button.click()
        except Exception:
            self.find_Test_Suites()
            
        try:
            table_Body = self.wait.until(ec.presence_of_element_located((By.XPATH, "//table[contains(@class, 'content-table') and @summary = 'This is Test Suites table']/tbody")))
            rows  = WebDriverWait(table_Body, 3).until(ec.presence_of_all_elements_located((By.TAG_NAME, "tr")))
        #rows = table_Body.find_elements(By.TAG_NAME, "tr")
        except Exception:
            return
        
        previous_dict = self.load_perviously_added_data()
        
        if not previous_dict:
            last_test_suite = ""
            self.create_document_template(self.file_path)
            
        else:
            self.currently_publish_test_suite = previous_dict.copy()
            self.currently_publish_test_suite.popitem()
            last_test_suite = list(previous_dict.keys())[-1]
            df = pd.read_excel(f"{self.file_path}.xlsx")
            df = df[df['Function Name'] != f"{last_test_suite}"]
            df.to_excel(f"{self.file_path}.xlsx", index= False)
            

            
        for i in range(len(rows)):
            if self.page_number != 0:
                for _ in range(self.page_number):
                    next_xpath = "//span[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_pagerButton')]//a[@aria-disabled = 'false']//span[normalize-space(text())='Next']"
                    for j in range(3):
                        try:
                            next_button = WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((By.XPATH, next_xpath)))
                            self.driver.execute_script("arguments[0].scrollIntoView(true)", next_button)
                            self.driver.execute_script("arguments[0].click();", next_button)
                            break
                        except Exception:
                            time.sleep(1)
                  
            text = ""
            for k in range(3):
                try:
                    table_Body = self.wait.until(ec.presence_of_element_located((By.XPATH, "//table[contains(@class, 'content-table') and @summary = 'This is Test Suites table']/tbody")))
                    rows  = WebDriverWait(table_Body, 30).until(ec.presence_of_all_elements_located((By.TAG_NAME, "tr")))
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", rows[i])
                    cols = WebDriverWait(rows[i], 30).until(ec.presence_of_all_elements_located((By.TAG_NAME, "td")))                    
                    text = cols[4].text
                    print(text)
                    self.update_signal_publish.emit(f"Function Name: {text}")
                    break
                except Exception:
                    if k == 2:
                        return
                    else:
                        time.sleep(1)

            if last_test_suite and text != last_test_suite and self.flag1 == 0:
                continue
            else: 
                self.flag1 = 1
                try:
                    self.wait.until(ec.element_to_be_clickable(cols[2])).click()
                except Exception:
                    self.error_signal_publish.emit("rows of test suite table is not clickable")
                    return
                self.find_test_case(text)
                self.driver.back()
                for l in range(3):
                    try:
                        test_suites_button = self.wait.until(ec.element_to_be_clickable((By.XPATH,"//a[@title='Test Suites']")))
                        test_suites_button.click()
                        break
                    except Exception:
                        if l == 2:
                            self.error_signal_publish.emit("Test Suites element not found/clickable")
                        else:
                            time.sleep(1)

            
            # Progress
            temp_string = "## Function inserted: " + str( i+1)
            self.update_signal_publish.emit(temp_string)
            print(temp_string)
            data.current_publisher_progress_value=i+1 
            self.progress_signal.emit(str(i+1))
            
          
        next_xpath = "//span[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_pagerButton')]//a[@aria-disabled = 'false']//span[normalize-space(text())='Next']"
        try:
            next_button = WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((By.XPATH, next_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true)", next_button)
            self.driver.execute_script("arguments[0].click();", next_button)
            self.page_number+=1
            self.find_Test_Suites()
        except Exception:
            return
    
    
    
    def find_test_case(self, text):
        self.driver.refresh()
        ele = "//div[@class='stationary-content-area com-ibm-asq-common-web-ui-directory-pane']//ul[@class='entries']//li[contains(@id,'com.ibm.rqm.execution.editor.section')]//a[@title='Test Cases' and span[normalize-space(text())='Test Cases']]"
        self.scrollnclick(ele)
        for i in range(3):
            try:
                table_Body = self.wait.until(ec.presence_of_element_located((By.XPATH, "//table[contains(@class, 'content-table') and @summary = 'This is Test Cases in Test Suite table']/tbody")))
                rows  = WebDriverWait(table_Body, 3).until(ec.presence_of_all_elements_located((By.TAG_NAME, "tr")))
                break
            except Exception:
                if i == 2:
                    with open(self.path, 'a') as file:
                        file.write(f"\n{text}--No test case found")
                    return
                else:
                    time.sleep(1)
        self.currently_publish_test_case = []
        for i in range(len(rows)):
            test_case_data = []
            test_case_data.append(text)
            test_case_name = ""
            while(True):
               path = "//table[contains(@class, 'content-table') and @summary = 'This is Test Cases in Test Suite table']/tbody"
               cols = self.find_table_row(i, path)
               test_case_name = cols[5].text
               self.update_signal_publish.emit(f"Test Case: {test_case_name}")
               if test_case_name:
                   break
               else:
                   self.driver.refresh()
                   ele = "//div[@class='stationary-content-area com-ibm-asq-common-web-ui-directory-pane']//ul[@class='entries']//li[contains(@id,'com.ibm.rqm.execution.editor.section')]//a[@title='Test Cases' and span[normalize-space(text())='Test Cases']]"
                   self.scrollnclick(ele)
                       
                    
            self.currently_publish_test_case.append(test_case_name)
            test_case_data.append(test_case_name)
            print("**********")
            print(test_case_data)
            print("**********")
            
            cols[3].click()
                                     
            self.driver.refresh()

            self.publish_document(test_case_data)
            self.currently_publish_test_suite[text] = self.currently_publish_test_case
            with open(f"{self.file_path}.json", 'w') as f:        
                json.dump(self.currently_publish_test_suite, f, indent=4)

            self.driver.back()
            ele = "//div[@class='stationary-content-area com-ibm-asq-common-web-ui-directory-pane']//ul[@class='entries']//li[contains(@id,'com.ibm.rqm.execution.editor.section')]//a[@title='Test Cases' and span[normalize-space(text())='Test Cases']]"
            self.scrollnclick(ele)
            


    def find_table_row(self, i, path):
        for i in range(3):
            try:
                table_Body = self.wait.until(ec.presence_of_element_located((By.XPATH, f"{path}")))
                rows  = WebDriverWait(table_Body, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, "tr")))            
                cols = WebDriverWait(rows[i], 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, "td")))
                break
            except Exception:
                self.error_signal_publish.emit("Table element not found")
                time.sleep(1)
        return cols
    def publish_document(self, test_case_data):
        flag = 0
        count = 0
        ########
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        pui_xpath = "//a[@title='TEST CASE PUI']"
        # try:
        f = self.scrollnclickParent(pui_xpath, "xpath", visible_section)
        if f == 1:
            with open(self.path, 'a') as file:
                file.write(test_case_data[0]+'--'+test_case_data[1])
            return
        flag = self.iframe_test_data_writer(test_case_data, "Editor, editor1")
        if flag == 1:
            count+=1
            flag = 0
        
        # ########
        
        # ######precondition
        
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        precondition = "a[title='Pre-Condition']"
        # try:
        f = self.scrollnclickParent(precondition, "css", visible_section)
        if f == 1:
            with open(self.path, 'a') as file:
                file.write(test_case_data[0]+'--'+test_case_data[1])
            return
        print("clciked precondition")
        flag = self.iframe_test_data_writer(test_case_data, "Editor, editor2")
        if flag == 1:
            count+=1
            flag = 0
        ################
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        input_data = "a[title='Test Input']"
        # try:
        f = self.scrollnclickParent(input_data, "css", visible_section)
        if f == 1:
            with open(self.path, 'a') as file:
                file.write(test_case_data[0]+'--'+test_case_data[1])
            return
        print("clciked input")
        flag = self.iframe_test_data_writer(test_case_data, "Editor, editor3")
        if flag == 1:
            count+=1
            flag = 0
        ###########################
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        
        expected_result = "//ul[contains(@class, 'entries')]//li[contains(@id, 'com.ibm.rqm.planning.editor.section.testCaseExpectedResults')]//a[@title = 'Expected Results']"
        try:
            self.wait.until(ec.presence_of_element_located((By.XPATH, expected_result))).click()
        except Exception:
            with open(self.path, 'a') as file:
                file.write(test_case_data[0]+'--'+test_case_data[1])
            return
        #self.scrollnclickParent(expected_result, "xpath", visible_section)
        print("expected result")
        flag = self.iframe_test_data_writer(test_case_data, "Editor, editor4")
        if flag == 1:
            count+=1
            flag = 0
        if count == 4:
            with open(self.path, 'a') as file:
                file.write("\n"+test_case_data[0]+'--'+test_case_data[1])
            return
        ############################
        test_case_data[1], test_case_data[2] = test_case_data[2], test_case_data[1]
        wb = load_workbook(f"{self.file_path}.xlsx")
        ws = wb.active
        ws.append(test_case_data)
        
        wb.save(f"{self.file_path}.xlsx")
        # time.sleep(3)
        # self.driver.back()
        # time.sleep(3)
        
    def iframe_test_data_writer(self, test_case_data, editor_title):
        try:
            ele = WebDriverWait(self.driver, 1).until(ec.presence_of_element_located((By.XPATH, "//div[@class = 'content-empty']")))
            return 1
        except Exception:
            for _ in range(3):
                try:        
                    element2 = self.wait.until(ec.presence_of_element_located((By.XPATH, "//div[@class = 'content rqm-ck-rich-text rqm-rt-content']")))
                    self.driver.execute_script("arguments[0].scrollIntoView(true)", element2)
                    self.driver.execute_script("arguments[0].click();", element2)
                    break
                except Exception:
                    time.sleep(1)
                   
            # with open("page.html", "w", encoding="utf-8") as f:
            #        f.write(self.driver.page_source)
            try:       
                iframe = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, f"iframe.cke_wysiwyg_frame[title='{editor_title}']")))
            except Exception:
                with open(self.path, 'a') as file:
                    file.write(test_case_data[0]+test_case_data[2])
                    return 1
            if iframe.is_displayed:        
                self.driver.switch_to.frame(iframe)
        
                text_box = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,"body.cke_editable")))
                if text_box.is_displayed:
                    text = re.sub(r'^[\r\n\t\f\v\u2028\u2029\u200b\ufeff\s]+', ' ', text_box.text)
        
                    test_case_data.append(text)
                    print(text)
        
                else:
                    print("Frame not found")
                    
            self.driver.switch_to.default_content()
            return 0
        
                

        
# publisher = QLM_Publisher()
# publisher.start_process()