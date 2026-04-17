# -*- coding: utf-8 -*-
"""
Spyder Editor
This is a temporary script file.
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
from global_data import data
from PyQt5.QtCore import pyqtSignal , QObject
from pathlib import Path


error_test_cases = []
options=Options()
options.add_argument("--width=1920")
options.add_argument("--height=1080")
path = "error_log.txt"
pwd_path = Path.cwd()
service=Service(executable_path=f"{pwd_path}/geckodriver")


#time.sleep(2)
test_suites_list = []
test_cases_list = []



class QLM_Uploader(QObject):
    update_signal = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.progress_value = 0
    
        
    def start_process(self, startProcessData):
        self.update_signal.emit("INITIATING PROCESS..........")
        # with open(path, 'w') as file:
        #     pass
        # file.close()
        self.startProcessData = startProcessData
        self.df = pd.read_excel(self.startProcessData["excel_path"])
        self.driver=webdriver.Firefox(service=service,options=options)
        self.driver.get(self.startProcessData["Project_link"])
        self.wait = WebDriverWait(self.driver, 30)
        self.Login_process()
        self.update_test_suites()
        self.update_signal.emit("PROCESS FINISHED !!!!!!!!")
        self.driver.quit()
        
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
        # for _ in range(3):
        #     try:
        element = WebDriverWait(self.driver, 20).until(ec.presence_of_element_located((By.XPATH, x_path))) 
    
        #element = driver.find_element(By.XPATH, x_path)
        self.driver.execute_script("""
                              arguments[0].style.visibility='visible';
                              arguments[0].style.display='block';
                              arguments[0].style.position='relative';
        """, element)
        self.driver.execute_script("arguments[0].click();", element)
            #     break
            # except (StaleElementReferenceException, TimeoutException):
            #     time.sleep(1)
        
    
    def create_test_plan(self):
        self.driver.find_element(By.XPATH,"//*[@title='Create Test Plan']").click()
        self.wait.until(ec.presence_of_element_located((By.ID,"com_ibm_asq_common_web_ui_internal_widgets_layout_ASQValidateTextBox_0"))).send_keys("TVPR ATC Testing")
        self.driver.find_element(By.CLASS_NAME,"enum-field").click()
        self.driver.find_element(By.XPATH,"//*[@title='iCBTC_ITP Test Plan Template']").click()
        # create test plan ok button
        self.driver.find_element(By.XPATH,"/html/body/div[16]/div[2]/div[3]/div/button[2]").click()
    
        
    def Login_process(self):
        self.update_signal.emit("Logging in into the Quality Management")
        username = self.wait.until(ec.presence_of_element_located((By.NAME, "j_username")))
        password = self.wait.until(ec.presence_of_element_located((By.NAME, "j_password")))
        
        username.send_keys(self.startProcessData["Login_Username"])
        password.send_keys(self.startProcessData["Login_password"])
        
        
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_MenuPopup_6"))).click()
        self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_menu_MenuItem_0_text"))).click()
        self.update_signal.emit("Login successfully into the Quality Management")
        
    
        
    def create_test_suite(self, test_suite_name):
        self.driver.refresh()
        button = self.wait.until(ec.presence_of_element_located((By.XPATH,"//div[@class='stationary-content-area com-ibm-asq-common-web-ui-directory-pane']//ul[@class='entries']//li[contains(@id,'com.ibm.rqm.planning.editor.section')]//a[@title='Test Suites' and span[normalize-space(text())='Test Suites']]")))
        button.click()
        for _ in range(3):
            try: 
                element1 = self.wait.until(ec.presence_of_element_located((By.XPATH,"//span[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_')]//a[contains(@class, 'button') and @title='Create Test Suite']")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element1)
                self.driver.execute_script("arguments[0].click();", element1)
                break
            except (StaleElementReferenceException, TimeoutException):
                time.sleep(1)

        self.wait.until(ec.presence_of_element_located((By.XPATH,"//input[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_layout_ASQValidateTextBox_') and @value='']"))).send_keys(test_suite_name)     
        self.wait.until(ec.presence_of_element_located((By.XPATH,"//*[@aria-label='select form field']"))).click()
    
        
    
        
        self.wait.until(ec.element_to_be_clickable(self.driver.find_element(By.XPATH,"//*[@title='iCBTC Test Suite Template']"))).click()
        for _ in range(3):
            try:
                element = self.wait.until(ec.presence_of_element_located((By.XPATH,"//button[contains(text(),'OK')]")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element)
                break
            except (StaleElementReferenceException, TimeoutException):
                time.sleep(1)
        self.scrollnclick("//button[contains(@class,'j-button-primary') and normalize-space(text())='OK']")
        for _ in range(3):
            try:
                element1 = self.wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'right-action primary-button') and @title='Save' and contains(normalize-space(.), 'Save')]")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element1)
                break
            except (StaleElementReferenceException, TimeoutException):
                time.sleep(1)
        self.scrollnclick("//button[contains(@class, 'right-action primary-button') and @title='Save' and contains(normalize-space(.), 'Save')]")
        
    
    def iframe_test_data_writer(self, row_data, editor_title):
        add_content_xpath = "//div[@class='content-empty']//a[@tabindex='0']"
        for _ in range(3):
            try:
                element2 = WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((By.XPATH, add_content_xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element2)
                self.driver.execute_script("arguments[0].click();", element2)
                break
            except Exception:
                time.sleep(1)


      
        # with open("page.html", "w", encoding="utf-8") as f:
        #         f.write(self.driver.page_source)
        for _ in range(3):
            try:
                iframe = WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((By.CSS_SELECTOR, f"iframe.cke_wysiwyg_frame[title='{editor_title}']")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", iframe)
                if iframe.is_displayed:
                    self.driver.switch_to.frame(iframe)
                break
            except Exception:
                time.sleep(1)
                

        #if iframe.is_displayed:        
        #self.driver.switch_to.frame(iframe)
        
        ##time.sleep(3)
        for _  in range(3):
            try:
                text_box = WebDriverWait(self.driver, 30).until(ec.element_to_be_clickable((By.CSS_SELECTOR,"body.cke_editable")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", text_box)
                self.driver.execute_script("arguments[0].click();", text_box)        
                
                if text_box.is_displayed:
                    #text_box.click()
                    text_box.send_keys(row_data)
                break
            except Exception:
                time.sleep(1)

        #text_box = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,"body.cke_editable")))
        
        # if text_box.is_displayed:
        #     text_box.click()
        #     text_box.send_keys(row_data)
           

        # else:
        #     print("Frame not found")
        print(row_data)
        self.driver.switch_to.default_content()
    
    
    def enter_test_case_data(self, row,case_name):
        #time.sleep(3)
        for _ in range(3):
            try:
                element1 = self.wait.until(ec.element_to_be_clickable((By.XPATH, f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and text() = '{case_name}']")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element1)
                self.driver.execute_script("arguments[0].click();", element1)
                #element1.click()
                break
            except (StaleElementReferenceException, TimeoutException):
                time.sleep(1)
                
        # PUI
        #time.sleep(2)
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        pui_xpath = "//a[@title='TEST CASE PUI']"
        # try:
        self.scrollnclickParent(pui_xpath, "xpath", visible_section)
        self.iframe_test_data_writer(row['PUI'], "Editor, editor1")
        # except Exception:
        #     with open(path, 'a') as file:
        #         print("1")
        #         file.write("\n" + case_name)

        
        # precondition
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        precondition = "a[title='Pre-Condition']"
        # try:
        self.scrollnclickParent(precondition, "css", visible_section)
        print("clciked precondition")
        self.iframe_test_data_writer(row['Scenario'], "Editor, editor2")
        # except Exception:
        #     with open(path, 'a') as file:
        #         print("2")
        #         file.write("\n" + case_name)
    
        #time.sleep(2)
        # input 
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        input_data = "a[title='Test Input']"
        # try:
        self.scrollnclickParent(input_data, "css", visible_section)
        print("clciked input")
        self.iframe_test_data_writer(row['Input'],"Editor, editor3")
        # except Exception:
        #     with open(path, 'a') as file:
        #         print("3")
        #         file.write("\n" + case_name)
        

        #time.sleep(2)
        # output
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        
        expected_result = "/html/body/div[1]/div/table/tbody/tr[1]/td[2]/div[2]/div/div[1]/div[5]/div/div[3]/div/div[3]/div[3]/div/div/div/div/table/tbody/tr/td[1]/div/div[1]/div/div[2]/ul[1]/li[7]/a"
        # try:
        self.scrollnclickParent(expected_result, "xpath", visible_section)
        print("expected result")
        self.iframe_test_data_writer(row['Expected output'], "Editor, editor4") 
        # except Exception:
        #     with open(path, 'a') as file:
        #         print("4")
        #         file.write("\n" + case_name)
                
        #time.sleep(2)
        print("********************************************************************************")
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        button_path = "button[title='Save'][tabindex='0']:not([disabled])"
        # try:
        self.scrollnclickParent(button_path, "css", visible_section)
        # except Exception:
        #     with open(path, 'a') as file:
        #         print("save not found")
        #         file.write("\n" + case_name)
        print("********************************************************************************")

        #time.sleep(2)
        self.driver.back()

        
    def iframe_test_data_writer_updation(self, row_data, editor_title):
        
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
            text_box.click()
            if text_box.is_displayed:
                text_box.clear()
                text_box.click()
                text_box.send_keys(row_data)
    
            else:
                print("Frame not found")
        print(row_data)
        self.driver.switch_to.default_content()
    
    def create_test_cases(self, row):
        #time.sleep(3)
        test_case_name_parent  = str(row['Name']).strip()
        test_case_name = ' '.join(test_case_name_parent.split())
        print(test_case_name)
        self.wait.until(ec.presence_of_element_located((By.XPATH,"//*[@title='Create Test Case']"))).click()

        # if pop up window comes
        pop = self.wait.until(ec.presence_of_element_located((By.XPATH,"//button[contains(@class,'j-button-danger') and normalize-space(text())='OK']")))
        if pop:
            pop.click()
          
        
        name_field = self.wait.until(ec.presence_of_element_located((By.XPATH,"//input[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_layout_ASQValidateTextBox_') and @value='']")))
        name_field.click()
        name_field.send_keys(test_case_name)       
                                                 
        for _ in range(3):
            try:
                description = self.wait.until(ec.presence_of_element_located((By.XPATH, "//*[@aria-label='select form field']"))).click()
                self.driver.execute_script("arguments[0].scrollIntoView(true)", description)
                self.driver.execute_script("arguments[0].click();", description)
                break
            except Exception:
                time.sleep(1)
        
        
        
        self.wait.until(ec.element_to_be_clickable(self.driver.find_element(By.XPATH,"//*[@title='iCBTC_Test Case Template']"))).click()
        # create test case ok button
        self.driver.execute_script("arguments[0].scrollIntoView(true)", self.driver.find_element(By.XPATH,"//button[contains(text(),'OK')]"))
        self.driver.find_element(By.XPATH,"//button[contains(@class,'j-button-primary') and normalize-space(text())='OK']").click()
        #time.sleep(10)
        
        
        self.scrollnclick("//*[contains(@class, 'right-action primary-button') and @title='Save' and contains(normalize-space(.), 'Save')]")
        

        while(True):
            self.enter_test_case_data(row, test_case_name)
            for _ in range(3):
                try:
                    element1 = self.wait.until(ec.element_to_be_clickable((By.XPATH, f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and text() = '{test_case_name}']")))
                    self.driver.execute_script("arguments[0].scrollIntoView(true)", element1)
                    self.driver.execute_script("arguments[0].click();", element1)
                    #element1.click()
                    break
                except Exception:
                    time.sleep(1)
                    
            # PUI
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            pui_xpath = "//a[@title='TEST CASE PUI']"
            # try:
            self.scrollnclickParent(pui_xpath, "xpath", visible_section)
            try:
                time.sleep(3)
                add_content_xpath = "//div[@class='content-empty']//a[@tabindex='0']"
                self.driver.find_element(By.XPATH, add_content_xpath)
                self.driver.back()
            except Exception:
                break

        print("test case added successfully")
        return
        
        
    
    
    def update_test_case(self, row):
        #time.sleep(3)
        print("Updating test case")
        ele = ""
        function_name_parent = str(row['Function']).strip()
        function_name = ' '.join(function_name_parent.split())
        #print(function_name)
    
        
        path = f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and contains(text(), '{function_name}')]"
        
        # create test case ok button
        for _ in range(3):
            try:
                ele1 = self.wait.until(ec.presence_of_element_located((By.XPATH,path)))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", ele1)
                self.driver.execute_script("arguments[0].click();", ele1)
                break
            except Exception:
                time.sleep(1)
        
        #self.scrollnclick(path)
        self.driver.refresh()
        ele = "//div[@class='stationary-content-area com-ibm-asq-common-web-ui-directory-pane']//ul[@class='entries']//li[contains(@id,'com.ibm.rqm.execution.editor.section')]//a[@title='Test Cases' and span[normalize-space(text())='Test Cases']]"
                                                                                                                                        
        
    
        self.scrollnclick(ele)
        test_case_name_parent  = str(row['Name']).strip()
        test_case_name = ' '.join(test_case_name_parent.split())
        updated_required = str(row['Updated']).strip()

        
        # for i in range(3):
        try:
           find_test_case_name = WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((By.XPATH,f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and text() = '{test_case_name}']")))
           self.driver.execute_script("arguments[0].scrollIntoView(true)", find_test_case_name)
           if pd.notna(row['Updated']):
               updated_required = str(row['Updated'].strip())
               if updated_required.lower() == "updated":
                   self.updateTestCaseNew(row, test_case_name)
               elif updated_required.lower() == "retry":
                   try:
                       
                       self.enter_test_case_data(row, test_case_name)
                   except Exception:
                       with open(path, 'a') as file:
                           print("7")
                           file.write("\n" + test_case_name)
               
           return
        except TimeoutException:
            if test_case_name not in test_cases_list:
                self.create_test_cases(row)
                #time.sleep(3)
                test_cases_list.append(test_case_name)
                self.driver.back()
            else:
                print("ALREADY PRESENT", row['Function'], row['Name'])
        print("test case updated successfully")
        return
    
    
    
    def updateTestCaseNew(self, row, test_case_name):
        for _ in range(5):
            try:
                element1 = self.wait.until(ec.element_to_be_clickable((By.XPATH, f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and text() = '{test_case_name}']")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element1)
                self.driver.execute_script("arguments[0].click();", element1)
                break
            except (StaleElementReferenceException, TimeoutException):
                time.sleep(1)
        
        
        
        # PUI
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        pui_xpath = "//a[@title='TEST CASE PUI']"
        self.scrollnclickParent(pui_xpath, "xpath", visible_section)
        self.iframe_test_data_writer_updation(row['PUI'], "Editor, editor1")
        
        
        # precondition
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        precondition = "a[title='Pre-Condition']"
        self.scrollnclickParent(precondition, "css", visible_section)
        print("clciked precondition")
        self.iframe_test_data_writer_updation(row['Scenario'], "Editor, editor2")
        
    
        # input
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        input_data = "a[title='Test Input']"
        self.scrollnclickParent(input_data, "css", visible_section)
        print("clciked input")
        self.iframe_test_data_writer_updation(row['Input'],"Editor, editor3")
        
        
        # output
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        expected_result = "/html/body/div[1]/div/table/tbody/tr[1]/td[2]/div[2]/div/div[1]/div[5]/div/div[3]/div/div[3]/div[3]/div/div/div/div/table/tbody/tr/td[1]/div/div[1]/div/div[2]/ul[1]/li[7]/a"
        self.scrollnclickParent(expected_result, "xpath", visible_section)
        print("expected result")    
        
        self.iframe_test_data_writer_updation(row['Expected output'], "Editor, editor4")
        
    
    
        print("********************************************************************************")
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        button_path = "button[title='Save'][tabindex='0']:not([disabled])"
        self.scrollnclickParent(button_path, "css", visible_section)
        print("********************************************************************************")
        
        
        
        self.driver.back()
       
    
    
    
    def update_test_suites(self):   
        
        #find testing plan
        self.update_signal.emit("Selecting the project")
        path = f"//*[text()='{self.startProcessData['current_test_plan']}']"
        print(path)
        self.wait.until(ec.presence_of_element_located((By.XPATH, path))).click()  #ui_data
        
        total_case = len(self.df)    
        #iterrate each row of the ITP/TVPR excel    
        for index,row in self.df.iterrows():
            self.driver.refresh()
            print("Currently processing row: ", row['Name'])
            self.driver.get('https://icbtc-elm.indigenous.com/qm/web/console/iCBTC_ATC/_W5EkWZD1Ee6mwccGoMIUKg#action=com.ibm.rqm.planning.home.actionDispatcher&subAction=viewTestPlan&id=42')
            test_suites_button = self.wait.until(ec.element_to_be_clickable((By.XPATH,"//a[@title='Test Suites']")))
            test_suites_button.click()
            function_name_parent = str(row['Function']).strip()
            function_name = ' '.join(function_name_parent.split())
            
            
            #check function name or test case name is empty
            if pd.isna(row['Function']) or pd.isna(row['Name']):
                continue
            #check function is already added or not
            elif str(row['Function']).strip() not in test_suites_list:
                #check function is already added in the previous program execution
                try:
                    find_test_suite_name = WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((By.XPATH,f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and contains(text(), '{function_name}')]")))
                    self.driver.execute_script("arguments[0].scrollIntoView(true)", find_test_suite_name)
                    self.update_test_case(row)
                #if function not present, create new test suite and test cases
                except TimeoutException:
                    test_name_parent = str(row['Function']).strip()
                    test_name = ' '.join(test_name_parent.split())
                    self.create_test_suite(test_name)
                    test_suites_list.append(str(row['Function']).strip())
                    self.update_test_case(row)
            else:
                #update test case only when function is already present
                print("ALREADY PRESENT", row['Function'])
                #time.sleep(10)
                self.update_test_case(row)   

            temp_string = f"Test Case No: {index+1}\nFunction Name: {row['Function']}\nTest Case Name:{row['Name']}\nStatus: Done"
            self.update_signal.emit(temp_string)
            data.current_progress_value=int(((index+1)/total_case)*100)                                                                
        
        
    
        



# start_time= time.perf_counter()

# uploader = QLM_Uploader()
# uploader.start_process()
# end_time = time.perf_counter()
# elapsed_time = end_time-start_time



# print(f"time taken is------{elapsed_time:.4f}")



