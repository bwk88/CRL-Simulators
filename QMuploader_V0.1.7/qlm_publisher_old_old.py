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
import time
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import math
#from global_data import data
from PyQt5.QtCore import pyqtSignal , QObject
from openpyxl import load_workbook
import re
from global_data import data

error_test_cases = []
options=Options()
options.add_argument("--width=1920")
options.add_argument("--height=1080")
path = "empty_test_case.txt"
service=Service(executable_path="/home/kuldeepsingh@Indigenous.com/Documents/ATC_TESTING/Selenium/IBMuploader/geckodriver")


#time.sleep(2)
test_suites_list = []
test_cases_list = []





class QLM_Publisher(QObject):
    update_signal_publish = pyqtSignal(str)
    error_signal_publish = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.progress_value = 0
    
        
    def start_process(self, startPublishData):
        #self.update_signal.emit("INITIATING PROCESS..........")
        # with open(path, 'w') as file:
        #     pass
        # file.close()
        self.startPublishData = startPublishData
        print(startPublishData)
        self.test_plan_name = self.startPublishData["Current_test_Plan_publisher"]
        print(self.test_plan_name)
        #self.df = pd.read_excel(self.startProcessData["excel_path"])
        self.driver=webdriver.Firefox(service=service,options=options)
        self.driver.get(self.startPublishData["Project_link_publisher"])
        self.wait = WebDriverWait(self.driver, 30)
        self.Login_process()
        #self.update_signal.emit("PROCESS FINISHED !!!!!!!!")
        #self.driver.quit()
        
    def scrollnclickParent(self, x_path, selector, parent_driver):   
        if selector=="xpath":
            for _ in range(3):
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
                except (StaleElementReferenceException, TimeoutException):
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
                except (StaleElementReferenceException, TimeoutException):
                    time.sleep(1)
            
        
        
    def scrollnclick(self, x_path):           
        for _ in range(3):
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
            except (StaleElementReferenceException, TimeoutException):
                time.sleep(1)
        
    def Login_process(self):
        self.update_signal_publish.emit("Logging in into the Quality Management")
        username = self.wait.until(ec.presence_of_element_located((By.NAME, "j_username")))
        password = self.wait.until(ec.presence_of_element_located((By.NAME, "j_password")))
        
        username.send_keys(self.startPublishData["Login_Username_publisher"])
        password.send_keys(self.startPublishData["Login_password_publisher"])
        
        
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_MenuPopup_6"))).click()
        self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_menu_MenuItem_0_text"))).click()
        path = f"//*[text()='{self.test_plan_name}']"
        print("-----------------",path)
        temp = self.wait.until(ec.presence_of_element_located((By.XPATH,f"//*[text()='{self.test_plan_name}']"))).click()
        self.create_document_template(self.test_plan_name)
        test_suites_button = self.wait.until(ec.element_to_be_clickable((By.XPATH,"//a[@title='Test Suites']")))
        test_suites_button.click()
        self.find_Test_Suites()
        self.update_signal_publish.emit("Login successfully into the Quality Management")
        
    def create_document_template(self, document_name):
        columns = ['Function Name', 'PUI', 'Test Case Name', 'Scenario', 'Input', 'Expected Output']
        df = pd.DataFrame(columns = columns)
        df.to_excel(f"{document_name}.xlsx", index=False)
        with open(path, 'w') as file:
            pass
    
        
    def find_Test_Suites(self):
        try:
            table_Body = self.wait.until(ec.presence_of_element_located((By.XPATH, "//table[contains(@class, 'content-table') and @summary = 'This is Test Suites table']/tbody")))
            rows  = WebDriverWait(table_Body, 3).until(ec.presence_of_all_elements_located((By.TAG_NAME, "tr")))
        #rows = table_Body.find_elements(By.TAG_NAME, "tr")
        except Exception:
            return
        
        for i in range(len(rows)):
            text = ""
            for _ in range(3):
                try:
                    table_Body = self.wait.until(ec.presence_of_element_located((By.XPATH, "//table[contains(@class, 'content-table') and @summary = 'This is Test Suites table']/tbody")))
                    rows  = WebDriverWait(table_Body, 30).until(ec.presence_of_all_elements_located((By.TAG_NAME, "tr")))
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", rows[i])
                    cols = WebDriverWait(rows[i], 30).until(ec.presence_of_all_elements_located((By.TAG_NAME, "td")))                    
                    text = cols[4].text
                    self.wait.until(ec.element_to_be_clickable(cols[2])).click()
                    break
                except Exception:
                    time.sleep(1)
            #cols[2].click()
            self.find_test_case(text)
            self.driver.back()
            test_suites_button = self.wait.until(ec.element_to_be_clickable((By.XPATH,"//a[@title='Test Suites']")))
            test_suites_button.click()
            # test_suite_element = WebDriverWait(test_suite_name, 30).until(ec.presence_of_element_located((By.XPATH, "//a[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width')]")))
            # self.driver.execute_script("arguments[0].scrollIntoView(true)", test_suite_element)
            # self.driver.execute_script("arguments[0].click();", test_suite_element)
            temp_string = "## Function inserted: " + str( i+1)
            self.update_signal_publish.emit(temp_string)
            print(temp_string)
            data.current_publisher_progress_value=i+1 
        
        next_xpath = "//span[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_pagerButton')]//a[@aria-disabled = 'false']//span[normalize-space(text())='Next']"
        try:
            next_button = WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((By.XPATH, next_xpath)))
            self.driver.execute_script("arguments[0].scrollIntoView(true)", next_button)
            self.driver.execute_script("arguments[0].click();", next_button)
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
                rows  = WebDriverWait(table_Body, 2).until(ec.presence_of_all_elements_located((By.TAG_NAME, "tr")))
                break
            except Exception:
                if i == 2:
                    with open(path, 'a') as file:
                        file.write(f"\n{text}--No test case found")
                    return
                else:
                    time.sleep(1)

        for i in range(len(rows)):
            test_case_data = []
            for _ in range(3):
                try:
                    table_Body = self.wait.until(ec.presence_of_element_located((By.XPATH, "//table[contains(@class, 'content-table') and @summary = 'This is Test Cases in Test Suite table']/tbody")))
                    rows  = WebDriverWait(table_Body, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, "tr")))            
                    cols = WebDriverWait(rows[i], 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, "td")))
                    test_case_data.append(text)
                    test_case_data.append(cols[5].text)
                    cols[3].click()
                    break
                except Exception:
                    time.sleep(1)                   
            self.driver.refresh()
            # ele = "//div[@class='stationary-content-area com-ibm-asq-common-web-ui-directory-pane']//ul[@class='entries']//li[contains(@id,'com.ibm.rqm.execution.editor.section')]//a[@title='Test Cases' and span[normalize-space(text())='Test Cases']]"
            # self.scrollnclick(ele)
            self.publish_document(test_case_data)
            # self.driver.refresh()
            # ele = "//div[@class='stationary-content-area com-ibm-asq-common-web-ui-directory-pane']//ul[@class='entries']//li[contains(@id,'com.ibm.rqm.execution.editor.section')]//a[@title='Test Cases' and span[normalize-space(text())='Test Cases']]"
            # self.scrollnclick(ele)
            self.driver.back()
            ele = "//div[@class='stationary-content-area com-ibm-asq-common-web-ui-directory-pane']//ul[@class='entries']//li[contains(@id,'com.ibm.rqm.execution.editor.section')]//a[@title='Test Cases' and span[normalize-space(text())='Test Cases']]"
            self.scrollnclick(ele)
            

        
            
    
    def publish_document(self, test_case_data):
        flag = 0
        ########
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        pui_xpath = "//a[@title='TEST CASE PUI']"
        # try:
        self.scrollnclickParent(pui_xpath, "xpath", visible_section)
        flag = self.iframe_test_data_writer(test_case_data, "Editor, editor1")
        if flag == 1:
            return
        
        # ########
        
        # ######precondition
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        precondition = "a[title='Pre-Condition']"
        # try:
        self.scrollnclickParent(precondition, "css", visible_section)
        print("clciked precondition")
        flag = self.iframe_test_data_writer(test_case_data, "Editor, editor2")
        if flag == 1:
            return
        ################
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        input_data = "a[title='Test Input']"
        # try:
        self.scrollnclickParent(input_data, "css", visible_section)
        print("clciked input")
        flag = self.iframe_test_data_writer(test_case_data, "Editor, editor3")
        if flag == 1:
            return 
        ###########################
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        
        expected_result = "//ul[contains(@class, 'entries')]//li[contains(@id, 'com.ibm.rqm.planning.editor.section.testCaseExpectedResults')]//a[@title = 'Expected Results']"
        self.wait.until(ec.presence_of_element_located((By.XPATH, expected_result))).click()
        #self.scrollnclickParent(expected_result, "xpath", visible_section)
        print("expected result")
        flag = self.iframe_test_data_writer(test_case_data, "Editor, editor4")
        if flag == 1:
            return
        ############################
        test_case_data[1], test_case_data[2] = test_case_data[2], test_case_data[1]
        print(test_case_data)
        wb = load_workbook(f"{self.test_plan_name}.xlsx")
        ws = wb.active
        ws.append(test_case_data)
        
        wb.save(f"{self.test_plan_name}.xlsx")
        # time.sleep(3)
        # self.driver.back()
        # time.sleep(3)
        
    def iframe_test_data_writer(self, test_case_data, editor_title):
        try:
            ele = WebDriverWait(self.driver, 1).until(ec.presence_of_element_located((By.XPATH, "//div[@class = 'content-empty']")))
            with open(path, 'a') as file:
                file.write("\n"+test_case_data[1])
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
                   
            iframe = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, f"iframe.cke_wysiwyg_frame[title='{editor_title}']")))
        
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