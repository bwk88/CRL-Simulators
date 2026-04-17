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
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec    
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
import math
from global_data import data
from PyQt5.QtCore import pyqtSignal, QObject
from pathlib import Path
import sys
import json
import os

from utilityPrograms import cleanString

error_test_cases = []
options=Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--width=1920")
options.add_argument("--height=1080")
path = "error_log.txt"
pwd_path = Path.cwd()
service=Service(executable_path=f"{pwd_path}/geckodriver")

#time.sleep(2)





class QLM_Uploader(QObject):
    update_scrapper_signal = pyqtSignal(str)
    updated_uploader_progress_signal = pyqtSignal(str)
    error_signal_publish = pyqtSignal(str)
    force_stopped_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.progress_value = 0
    
    def quit(self):
        print("Quitting driver")
        self.update_scrapper_signal.emit("STOPPING DRIVER .............")
        self.driver.quit()
        self.force_stopped_signal.emit()
        
    def start_process(self, startProcessData):
        self.update_scrapper_signal.emit("INITIATING PROCESS..........")
        # with open(path, 'w') as file:
        #     pass
        # file.close()
        self.test_suites_list = []
        self.test_cases_list = []
        self.test_suite_case_dictionary = {}
        self.startProcessData = startProcessData
        self.df = pd.read_excel(self.startProcessData["excel_path"])
        self.driver=webdriver.Firefox(service=service,options=options)
        self.driver.get(self.startProcessData["Project_link"])
        
        self.wait = WebDriverWait(self.driver, 5)
        self.waitTwo = WebDriverWait(self.driver, 2)
        
        os.makedirs(f"{pwd_path}/data_log/{startProcessData['current_test_plan']}", exist_ok=True)
        # self.file_name = f"{startProcessData['current_test_plan']}_{startProcessData['job_id']}"    # atc_tvpr_1 atc_tvpr_2 
        # self.test_plan_name = f"{startProcessData['current_test_plan']}"
        # self.path = f"{pwd_path}/{startProcessData['current_test_plan']}/empty_test_case.txt"
        # self.file_path = f"{pwd_path}/{startProcessData['current_test_plan']}/{self.file_name}"
        
        self.test_suite_list_path = f"{pwd_path}/data_log/{startProcessData['current_test_plan']}/test_suite_list.json"
        self.test_case_list_path = f"{pwd_path}/data_log/{startProcessData['current_test_plan']}/test_case_list.json"
        
        self.test_suites_list, self.test_suite_case_dictionary = self.load_previous_data()
        print(self.test_suites_list)
        # print("---------------")
        # print(self.test_suite_case_dictionary)
        # test_suites_list = suites[-1]
        # test_cases_list = cases[-1]

        self.Login_process()
        self.update_test_suites()
        self.update_scrapper_signal.emit("PROCESS FINISHED !!!!!!!!")
        #self.driver.quit()
    
  
    
    def cleanTestSuitesList(self, listData):
        for i in range(len(listData)):
            listData[i] = cleanString(listData[i])
        return listData
            
    def cleanTestCaseDict(self, dictData):
        newDictData = {}
        for key,value in dictData.items():
            nkey = cleanString(key)
            nValue = []
            for items in value:
                items = cleanString(items)
                nValue.append(items)
            
            newDictData[nkey]=nValue
        return newDictData
    
    
    def load_previous_data(self):
        if not(os.path.exists(f"{self.test_suite_list_path}")):
            with open(f"{self.test_suite_list_path}", 'w') as f:
                temp_dict = []
                json.dump(temp_dict, f)
                
        if not(os.path.exists(f"{self.test_case_list_path}")):
            with open(f"{self.test_case_list_path}", 'w') as f:
                temp_dict = {}
                json.dump(temp_dict, f)
        #test_suites = []
        with open(f"{self.test_suite_list_path}", 'r') as f:
            for line in f:
                test_suites = json.loads(line.strip())
        #test_cases = []
        with open(f"{self.test_case_list_path}", 'r') as f:
            dic = json.load(f)
            
        test_suites = self.cleanTestSuitesList(test_suites)
        dic = self.cleanTestCaseDict(dic)
        print("Temporary file are loaded")
        return test_suites, dic
    
    
    
        
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
                        self.error_signal_publish.emit("button not found/clickable")
                        #self.driver.quit()
                        raise ValueError("button not found/clickable")
                    else:
                        time.sleep(1)
            
        if selector=="css":
            for i in range(3):
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
                        self.error_signal_publish.emit("button not found/clickable")
                        raise ValueError("button not found/clickable")
                        
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
                    self.error_signal_publish.emit("button not found/clickable")
                    raise ValueError("Cannot be able to scroll and click")
                    # self.driver.quit()
                else:
                    time.sleep(1)
        
    def scrollnclickVisible(self, x_path):           
        for i in range(3):
            try:
                element = WebDriverWait(self.driver, 20).until(ec.visibility_of_element_located((By.XPATH, x_path))) 
            
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
                    self.error_signal_publish.emit("button not found/clickable")
                    raise ValueError("Cannot be able to scroll and click")
                    # self.driver.quit()
                else:
                    time.sleep(1)
                    
    def create_test_plan(self):
        self.driver.find_element(By.XPATH,"//*[@title='Create Test Plan']").click()
        self.wait.until(ec.presence_of_element_located((By.ID,"com_ibm_asq_common_web_ui_internal_widgets_layout_ASQValidateTextBox_0"))).send_keys("TVPR ATC Testing")
        self.driver.find_element(By.CLASS_NAME,"enum-field").click()
        self.driver.find_element(By.XPATH,"//*[@title='iCBTC_ITP Test Plan Template']").click()
        # create test plan ok button
        self.driver.find_element(By.XPATH,"/html/body/div[16]/div[2]/div[3]/div/button[2]").click()
    
        
    def Login_process(self):
        self.update_scrapper_signal.emit("Logging in into the Quality Management")
        try:
            
            

            username = self.wait.until(ec.presence_of_element_located((By.NAME, "j_username")))
            password = self.wait.until(ec.presence_of_element_located((By.NAME, "j_password")))

            username.send_keys(self.startProcessData["Login_Username"])
            password.send_keys(self.startProcessData["Login_password"])


            
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
        self.update_scrapper_signal.emit("Login successfully into the Quality Management")
        
    
        
    def create_test_suite(self, test_suite_name):
        self.driver.refresh()
        
        try:
            button = self.wait.until(ec.presence_of_element_located((By.XPATH,"//div[@class='stationary-content-area com-ibm-asq-common-web-ui-directory-pane']//ul[@class='entries']//li[contains(@id,'com.ibm.rqm.planning.editor.section')]//a[@title='Test Suites' and span[normalize-space(text())='Test Suites']]")))
            button.click()
        except Exception:
            self.error_signal_publish.emit("test suite button not found")
            raise ValueError('Test suite button not found')
            
        path = f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and normalize-space(.) = '{test_suite_name}']"
        
        elem = self.driver.find_elements(By.XPATH,path)
        # create test case ok button
        #elem = WebDriverWait(self.driver, 1).until(ec.presence_of_element_located((By.XPATH,path)))
        while(True):        
            if elem:
            #self.driver.execute_script("arguments[0].scrollIntoView(true)", ele1)
            #self.driver.execute_script("arguments[0].click();", ele1)
                print("driver foudn")
                raise ValueError(f"Mismatch between storage log and elm log for '{test_suite_name}'")
                    
            else:
                next_xpath = "//span[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_pagerButton')]//a[@aria-disabled = 'false']//span[normalize-space(text())='Next']"

                try:
                    next_button = WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((By.XPATH, next_xpath)))
                    self.driver.execute_script("arguments[0].scrollIntoView(true)", next_button)
                    self.driver.execute_script("arguments[0].click();", next_button)
                except Exception:
                    break
        print("Creating test suite----")   
        for i in range(3):
            try: 
                element1 = self.wait.until(ec.presence_of_element_located((By.XPATH,"//span[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_')]//a[contains(@class, 'button') and @title='Create Test Suite']")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element1)
                self.driver.execute_script("arguments[0].click();", element1)
                self.wait.until(ec.presence_of_element_located((By.XPATH,"//input[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_layout_ASQValidateTextBox_') and @value='']"))).send_keys(test_suite_name)     
                self.wait.until(ec.presence_of_element_located((By.XPATH,"//*[@aria-label='select form field']"))).click()
                self.wait.until(ec.element_to_be_clickable(self.driver.find_element(By.XPATH,"//*[@title='iCBTC Test Suite Template']"))).click()
                break
            except (StaleElementReferenceException, TimeoutException):
                if i == 2:
                    self.error_signal_publish.emit("create test suite/new test suite creation window button not found")
                    raise ValueError("create test suite/new test suite creation window button not found")
                else:
                    time.sleep(1)

        
        for i in range(3):
            try:
                element = self.wait.until(ec.presence_of_element_located((By.XPATH,"//button[contains(text(),'OK')]")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element)
                break
            except (StaleElementReferenceException, TimeoutException):
                if i == 2:
                    self.error_signal_publish.emit("OK button not found")
                    raise ValueError("OK button not found")

                else:
                    time.sleep(1)
        self.scrollnclick("//button[contains(@class,'j-button-primary') and normalize-space(text())='OK']")
        for i in range(3):
            try:
                element1 = self.wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'right-action primary-button') and @title='Save' and contains(normalize-space(.), 'Save')]")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element1)
                break
            except (StaleElementReferenceException, TimeoutException):
                if i == 2:
                    self.error_signal_publish.emit("Save button not found")
                    raise ValueError("Save button not found")
                else:
                    time.sleep(1)
        self.scrollnclick("//button[contains(@class, 'right-action primary-button') and @title='Save' and contains(normalize-space(.), 'Save')]")
        
    
    def iframe_test_data_writer(self, row_data, editor_title):
        add_content_xpath = "//div[@class='content-empty']//a[@tabindex='0']"
        for i in range(3):
            try:
                element2 = WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((By.XPATH, add_content_xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element2)
                self.driver.execute_script("arguments[0].click();", element2)
                break
            except Exception:
                if i == 2:
                    raise ValueError("content empty not found. Mismatch between log data and elm data.")
                time.sleep(1)


      

        for _ in range(3):
            try:
                iframe = WebDriverWait(self.driver, 3).until(ec.presence_of_element_located((By.CSS_SELECTOR, f"iframe.cke_wysiwyg_frame[title='{editor_title}']")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", iframe)
                if iframe.is_displayed:
                    self.driver.switch_to.frame(iframe)
                break
            except Exception:
                time.sleep(1)
                


        for _  in range(3):
            try:
                text_box = WebDriverWait(self.driver, 3).until(ec.element_to_be_clickable((By.CSS_SELECTOR,"body.cke_editable")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", text_box)
                self.driver.execute_script("arguments[0].click();", text_box)        
                
                if text_box.is_displayed:
                    #text_box.click()
                    text_box.send_keys(row_data)
                break
            except Exception:
                time.sleep(1)


        self.driver.switch_to.default_content()
    
    
    def enter_test_case_data(self, row,case_name):
        #time.sleep(3)

        function_name_parent = str(row['Requirement']).strip()
        function_name = ' '.join(function_name_parent.split())
        test_case_name_parent  = str(row['Test Case Name']).strip()
        test_case_name = ' '.join(word.strip() for word in test_case_name_parent.split())
        
        
        
        next_button_available = 1
        while(next_button_available):
            next_xpath = "//span[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_pagerButton')]//a[@aria-disabled = 'false']//span[normalize-space(text())='Next']"

            try:
                next_button = WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((By.XPATH, next_xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", next_button)
                self.driver.execute_script("arguments[0].click();", next_button)
            except Exception:
                next_button_available = 0
                
        
        


        for i in range(5):
            try:
                element1 = self.wait.until(ec.presence_of_element_located((By.XPATH, f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and text() = '{test_case_name}']")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element1)
                self.driver.execute_script("arguments[0].click();", element1)
                #element1.click()
                break
            except Exception:
                if i == 4:
                    raise ValueError(f"{test_case_name} not found/clickable")
                time.sleep(1)
   
        # PUI
        #time.sleep(2)




        try:
            #test case PUI
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            pui_xpath = "//a[@title='TEST CASE PUI']"
            # try:
            self.scrollnclickParent(pui_xpath, "xpath", visible_section)
            self.iframe_test_data_writer(row['Test Case PUI'], "Editor, editor1")
        except Exception as e:
            self.driver.back()
            raise ValueError(f"Error {e} for section 'Test Case PUI' in '{test_case_name}'")
            return
            
        try:
            # precondition
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            precondition = "a[title='Pre-Condition']"
            # try:
            self.scrollnclickParent(precondition, "css", visible_section)
            print("clciked precondition")
            self.iframe_test_data_writer(row['Precondition'], "Editor, editor2")
        except Exception as e:
            self.driver.back()
            raise ValueError(f"Error {e} for section 'Pre-Condition' in '{test_case_name}'")
            return
    
        try:
            # input 
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            input_data = "a[title='Test Input']"
            # try:
            self.scrollnclickParent(input_data, "css", visible_section)
            print("clciked input")
            self.iframe_test_data_writer(row['Input'],"Editor, editor3")
        except Exception as e:
            self.driver.back()
            raise ValueError(f"Error {e} for section 'Test Input' in '{test_case_name}'")
            return
          
        try:
            # output
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            
            expected_result = "/html/body/div[1]/div/table/tbody/tr[1]/td[2]/div[2]/div/div[1]/div[5]/div/div[3]/div/div[3]/div[3]/div/div/div/div/table/tbody/tr/td[1]/div/div[1]/div/div[2]/ul[1]/li[7]/a"
            # try:
            self.scrollnclickParent(expected_result, "xpath", visible_section)
            print("expected result")
            self.iframe_test_data_writer(row['Expected output'], "Editor, editor4")
        except Exception as e:
            self.driver.back()
            raise ValueError(f"Error {e} for section 'Expected Output' in '{test_case_name}'")
            return
            
        try: 
            # Criteria for evaluating results
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            
            #criteria = "//li[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_DirectoryPane_)]//a[@title = 'Criteria for evaluating results'] and normalize-space(text())='Criteria for evaluating results']"
            #criteria = "/html/body/div[1]/div/table/tbody/tr[1]/td[2]/div[2]/div/div[1]/div[5]/div/div[3]/div/div[3]/div[5]/div/div/div/div/table/tbody/tr/td[1]/div/div[1]/div/div[2]/ul[1]/li[8]/a"
            # try:
            criteria = "//a[span[text()= 'Criteria for evaluating results']]"
            self.scrollnclickParent(criteria, "xpath", visible_section)
            print("Criteria for evaluating results")
            self.iframe_test_data_writer(row['CRITERIA FOR EVALUATING RESULTS'], "Editor, editor5") 
        except Exception as e:
            self.driver.back()
            raise ValueError(f"Error {e} for section 'Criteria for evaluating results' in '{test_case_name}'")
            return
        
        try:
            # INSTRUCTIONS FOR CONDUCTING PROCEDURE
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))          
        
            instruction = "//a[span[text()= 'Instructions for conducting procedure']]"
            # try:
            self.scrollnclickParent(instruction, "xpath", visible_section)
            print("Instructions for conducting procedure")
            self.iframe_test_data_writer(row['INSTRUCTIONS FOR CONDUCTING PROCEDURE'], "Editor, editor6") 
        except Exception as e:
            self.driver.back()
            raise ValueError(f"Error {e} for section 'Instructions for conducting procedure' in '{test_case_name}'")
            return
        
        time.sleep(1)
        try:
            print("********************************************************************************")
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            button_path = "button[title='Save'][tabindex='0']:not([disabled])"
            # try:
            self.scrollnclickParent(button_path, "css", visible_section)
    
            print("********************************************************************************")
        except Exception as e:
            self.driver.back()
            raise ValueError(f"Error {e} for section 'Save' in '{test_case_name}'")
            return

        #time.sleep(2)
        self.driver.back()


    def iframe_requirement_link_writer(self, row_data, editor_title):
        add_content_xpath = "//div[@class='jazz-ui-Dialog modal front front-modal is-visible']"
        for _ in range(3):
            try:
                element2 = WebDriverWait(self.driver, 30).until(ec.presence_of_element_located((By.XPATH, add_content_xpath)))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element2)
                self.driver.execute_script("arguments[0].click();", element2)
                break
            except Exception:
                print("Requirement linking Dialog not loaded")
                time.sleep(1)
               
        iframe = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR, 'iframe[name="https://icbtc-elm.indigenous.com/qm/web/dojo/resources/blank.html"]')))
    
        if iframe.is_displayed:        
            self.driver.switch_to.frame(iframe)
            print("Switched to iFrame")
            drop_down = self.wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,"select.projectInput")))
            dropdown = Select(drop_down)
            dropdown.select_by_visible_text("P4_SyRS_ATC")
            
            
            RadioButton = self.wait.until(ec.presence_of_element_located((By.XPATH,"//input[@id='dijit_form_RadioButton_1' and @type='radio' and @value='on']")))

            if not RadioButton.is_selected():
                RadioButton.click()
            
        
            searchModuleValue = "SyRS_ATC"
            searchModule = self.wait.until(ec.presence_of_element_located((By.XPATH,"//input[@id='com_ibm_rdm_web_common_ArtifactInstancesFilteringSelect_1']")))
            searchModule.clear()
            searchModule.send_keys(searchModuleValue)
            searchModule.send_keys(Keys.ENTER)
            # time.sleep(1)
            
            # try:
            loading_xpath = (By.XPATH, '//a[@class="entry" and contains(@aria-label, "Loading artifacts...")]')
            try:
                loading_module = self.waitTwo.until(ec.presence_of_element_located(loading_xpath))
                self.wait.until(ec.invisibility_of_element_located(loading_module))
                print("loading after module appered")
            except:
                print("loading after module not appered")
            finally:
                print("Continuing after loading search ")
                
            self.wait.until(ec.presence_of_all_elements_located((By.XPATH, "//td[@class='results-area']//div//div//div//a[contains(@aria-label, '&nbsp')]")))
            
            
            searchValue = int(row_data)
            searchBox = self.wait.until(ec.presence_of_element_located((By.XPATH,"//input[@placeholder='Type to filter artifacts by text or by ID']")))
            searchBox.send_keys(searchValue)
            searchBox.send_keys(Keys.ENTER)
            
            # time.sleep(1)
            
            try:
                loading_search = self.waitTwo.until(ec.presence_of_element_located(loading_xpath))
                self.wait.until(ec.invisibility_of_element_located(loading_search))
                print("loading after module appered")
            except:
                print("loading after module not appered")
            finally:
                print("Continuing after loading search ")
            
            # print(f'//a[@class="entry"]')
            # foundElement = self.wait.until(ec.presence_of_element_located((By.XPATH,"//a[contains(@id, 'jazz_ui_ResourceLink_') and normalize-space(text())='{searchValue}']")))
            foundElement = self.wait.until(ec.presence_of_element_located((By.XPATH,'//a[@class="entry"]')))
            foundElement.click()

            okButton = self.wait.until(ec.presence_of_element_located((By.XPATH,'//button[@class="j-button-primary" and text()="OK"]')))
            if okButton.is_enabled():
                okButton.click()
                print("ok clicked")
            else:
                print("ok button is disabled")  
                
            # time.sleep(3)
                    
            # except Exception as e:
            #     print("Error ", e)
            # finally:
            #     print("Done")
                
                
        else:
            print("Frame not found")
        print(row_data)
        self.driver.switch_to.default_content() 
        
        
        
    
    def iframe_test_data_writer_updation(self, row_data, editor_title):
        
        for i in range(3):
            try:        
                element2 = self.wait.until(ec.presence_of_element_located((By.XPATH, "//div[@class = 'content rqm-ck-rich-text rqm-rt-content']")))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", element2)
                self.driver.execute_script("arguments[0].click();", element2)
                break
            except Exception:
                if i == 2:
                    raise ValueError("Old/existing content not found")
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
        function_name_parent = str(row['Requirement']).strip()
        function_name = ' '.join(function_name_parent.split())
        test_case_name_parent  = str(row['Test Case Name']).strip()
        test_case_name = ' '.join(word.strip() for word in test_case_name_parent.split())

        
        
        next_button_available = 1
        while(next_button_available):
            next_xpath = "//span[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_pagerButton')]//a[@aria-disabled = 'false']//span[normalize-space(text())='Next']"

            try:
                WebDriverWait(self.driver, 1).until(ec.presence_of_element_located((By.XPATH, f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and text() = '{test_case_name}']")))
                break
                
            except Exception:
                try:
                    next_button = WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((By.XPATH, next_xpath)))
                    self.driver.execute_script("arguments[0].scrollIntoView(true)", next_button)
                    self.driver.execute_script("arguments[0].click();", next_button)
                except Exception:
                    next_button_available = 0
        
        if next_button_available == 0:
                
                
            self.wait.until(ec.presence_of_element_located((By.XPATH,"//*[@title='Create Test Case']"))).click()
    
            # if pop up window comes
            pop = self.wait.until(ec.presence_of_element_located((By.XPATH,"//button[contains(@class,'j-button-danger') and normalize-space(text())='OK']")))
            if pop:
                pop.click()
              
            
            # name_field.click()
            # name_field.send_keys(test_case_name)       
                                                     
            for i in range(3):
                try:
                    self.wait.until(ec.presence_of_element_located((By.XPATH,"//input[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_layout_ASQValidateTextBox_') and @value='']"))).send_keys(test_case_name)
                    
                    self.wait.until(ec.presence_of_element_located((By.XPATH, "//*[@aria-label='select form field']"))).click()
                    self.wait.until(ec.element_to_be_clickable(self.driver.find_element(By.XPATH,"//*[@title='iCBTC_Test Case Template']"))).click()
                    break
                except Exception:
                    if i == 2:
                        raise ValueError(f"{test_case_name} cannor be created.")
                    time.sleep(1)
            
            
    
            
            
            # create test case ok button
            self.driver.execute_script("arguments[0].scrollIntoView(true)", self.driver.find_element(By.XPATH,"//button[contains(text(),'OK')]"))
            self.driver.find_element(By.XPATH,"//button[contains(@class,'j-button-primary') and normalize-space(text())='OK']").click()
            #time.sleep(10)
            
            
            self.scrollnclick("//*[contains(@class, 'right-action primary-button') and @title='Save' and contains(normalize-space(.), 'Save')]")
            
            # self.test_suite_case_dictionary[function_name].append(test_case_name)
            # with open(f"{self.test_case_list_path}", 'w') as f:
            #     json.dump(self.test_suite_case_dictionary, f)
        

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
        
        if function_name in self.test_suite_case_dictionary:
            self.test_suite_case_dictionary[function_name].append(test_case_name)
        else:
            self.test_suite_case_dictionary[function_name] = []
            self.test_suite_case_dictionary[function_name].append(test_case_name)
        with open(f"{self.test_case_list_path}", 'w') as f:
            json.dump(self.test_suite_case_dictionary, f)
        return
        
        
    
    
    def updateRequirementLink(self, row, test_case_name):
        print("Linking process begining, sleep 2000")
        
        time.sleep(2)
        path = f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and normalize-space(text())='{test_case_name}']"
        while(True):        
            try:                                     
                ele1 = WebDriverWait(self.driver, 1).until(ec.presence_of_element_located((By.XPATH,path)))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", ele1)
                self.driver.execute_script("arguments[0].click();", ele1)
                break
            except Exception:
                next_xpath = "//span[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_pagerButton')]//a[@aria-disabled = 'false']//span[normalize-space(text())='Next']"

                try:
                    next_button = WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((By.XPATH, next_xpath)))
                    self.driver.execute_script("arguments[0].scrollIntoView(true)", next_button)
                    self.driver.execute_script("arguments[0].click();", next_button)
                except Exception:
                    self.error_signal_publish.emit("Function name not found/created")
                    return
        time.sleep(2)        
        
        # RequirementLinking
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        requirement_link_xpath = "//a[@title='Requirement Links']"
        self.scrollnclickParent(requirement_link_xpath, "xpath", visible_section)
    
        # Click add new and Perfrom requiremtnet linking
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        add_new_link_button = "//a[@title='Add new links']"
        self.scrollnclickParent(add_new_link_button, "xpath", visible_section)
        self.iframe_requirement_link_writer(row["Requirement Links"], "Editor, editor1")
    
        time.sleep(3)
        print("********************************************************************************")
        visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
        button_path = "button[title='Save'][tabindex='0']:not([disabled])"
        self.scrollnclickParent(button_path, "css", visible_section)
        print("********************************************************************************")
        
        
        
        # self.driver.back()
    
    
    
    def update_test_case(self, row):
        #time.sleep(3)
        print("Updating test case")
        ele = ""
        function_name_parent = str(row['Requirement']).strip()
        function_name = ' '.join(function_name_parent.split())
        #print(function_name)
    
        
        path = f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and normalize-space(.) = '{function_name}']"
       #path = f"//a[@id = 'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[@class = 'rich-hover-clip-cell clip-cell-nowrap-max-width') and //*[normalize-space() = '{function_name}']]"

        # create test case ok button
        
        while(True):        
            try:                                     
                ele1 = WebDriverWait(self.driver, 5).until(ec.presence_of_element_located((By.XPATH,path)))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", ele1)
                self.driver.execute_script("arguments[0].click();", ele1)
                break
            except Exception:
                next_xpath = "//span[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_pagerButton')]//a[@aria-disabled = 'false']//span[normalize-space(text())='Next']"

                try:
                    next_button = WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((By.XPATH, next_xpath)))
                    self.driver.execute_script("arguments[0].scrollIntoView(true)", next_button)
                    self.driver.execute_script("arguments[0].click();", next_button)
                except Exception:
                    self.error_signal_publish.emit("Function name not found/created")
                    raise ValueError(f"'{function_name}' not found/created")
        
        
        #self.scrollnclick(path)
        self.driver.refresh()
        ele = "//div[@class='dijitTabContainerTopChildWrapper dijitVisible']//div[@class='stationary-content-area com-ibm-asq-common-web-ui-directory-pane']//ul[@class='entries']//li[contains(@id,'com.ibm.rqm.execution.editor.section.testcases')]//a[@title='Test Cases' and span[normalize-space(text())='Test Cases']]"
        self.scrollnclickVisible(ele)
        
        test_case_name_parent  = str(row['Test Case Name']).strip()
        test_case_name = ' '.join(word.strip() for word in test_case_name_parent.split())
        updated_required = str(row['Updated']).strip()
        function_name_parent = str(row['Requirement']).strip()
        function_name = ' '.join(function_name_parent.split())

        print("Updated field value check : ",row['Updated'])
        if pd.notna(row['Updated']):
            updated_required = str(row['Updated'].strip())
            if updated_required.lower() == "updated":
                self.updateTestCaseNew(row, test_case_name)
            elif updated_required.lower() == "delete":
                self.delete_test_case(function_name, test_case_name)
            elif updated_required.lower() == "linking":
                self.updateRequirementLink(row, test_case_name)
            else:
                self.create_test_cases(row)
    
        else:
            self.create_test_cases(row)
            #time.sleep(3)
    
            # self.test_suite_case_dictionary[function_name].append(test_case_name)
            # self.test_cases_list.append(test_case_name)
            # with open(f"{self.test_case_list_path}", 'w') as f:
            #     json.dump(self.test_suite_case_dictionary, f)
        self.driver.back()
        # else:
        #      print("ALREADY PRESENT", row['Function'], row['Name'])
        # print("test case updated successfully")
        # return
    
    
    def delete_test_case(self, function_name, test_case_name):
        next_button_available = 1
        row_index = None
        while(next_button_available):
            next_xpath = "//span[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_pagerButton')]//a[@aria-disabled = 'false']//span[normalize-space(text())='Next']"

            try:
                WebDriverWait(self.driver, 1).until(ec.presence_of_element_located((By.XPATH, f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and text() = '{test_case_name}']")))
                path = "//table[contains(@class, 'content-table') and @summary = 'This is Test Cases in Test Suite table']/tbody"
                table_Body = self.wait.until(ec.presence_of_element_located((By.XPATH, f"{path}")))
                rows  = WebDriverWait(table_Body, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, "tr")))
                print("----------",len(rows))
                for index, row in enumerate(rows):
                    cells = WebDriverWait(row, 10).until(ec.presence_of_all_elements_located((By.TAG_NAME, "td")))
                    #cells = row.find_element(By.TAG_NAME, "td")
                    for cell in cells:
                        if cell.text.strip()==test_case_name:
                            print(cell.text.strip())
                            row_index = index
                            
                            break
                    if row_index is not None:
                        try:
                            self.wait.until(ec.element_to_be_clickable(cells[1])).click()
                            delete_button = self.wait.until(ec.presence_of_element_located((By.XPATH, "//td[contains(@class, 'dijitReset dijitMenuItemLabel') and text() = 'Remove Test Case']")))
                            # self.driver.execute_script("arguments[0].scrollIntoView(true)", delete_button)
                            # self.driver.execute_script("arguments[0].click();", delete_button)
                            delete_button.click()
                            self.scrollnclick("//button[contains(@class,'j-button-danger') and normalize-space(text())='OK']")
                            time.sleep(2)
                            save_button = self.wait.until(ec.presence_of_element_located((By.XPATH, "//button[contains(@class, 'right-action primary-button') and @title='Save' and contains(normalize-space(.), 'Save')]")))
                            save_button.click()

                            self.test_suite_case_dictionary[function_name].remove(test_case_name)
                            with open(f"{self.test_case_list_path}", 'w') as f:
                                json.dump(self.test_suite_case_dictionary, f)
                            break
                        except Exception:
                            self.error_signal_publish(f"{test_case_name} case not deleted")
                break
                
            except Exception:
                try:
                    next_button = WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((By.XPATH, next_xpath)))
                    self.driver.execute_script("arguments[0].scrollIntoView(true)", next_button)
                    self.driver.execute_script("arguments[0].click();", next_button)
                except Exception:
                    next_button_available = 0
                    
    def updateTestCaseNew(self, row, test_case_name):
        print("updateTestCaseNew")
        
        path = f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and contains(text(), '{test_case_name}')]"
        while(True):        
            try:                                     
                ele1 = WebDriverWait(self.driver, 1).until(ec.presence_of_element_located((By.XPATH,path)))
                self.driver.execute_script("arguments[0].scrollIntoView(true)", ele1)
                self.driver.execute_script("arguments[0].click();", ele1)
                break
            except Exception:
                next_xpath = "//span[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_pagerButton')]//a[@aria-disabled = 'false']//span[normalize-space(text())='Next']"

                try:
                    next_button = WebDriverWait(self.driver, 2).until(ec.presence_of_element_located((By.XPATH, next_xpath)))
                    self.driver.execute_script("arguments[0].scrollIntoView(true)", next_button)
                    self.driver.execute_script("arguments[0].click();", next_button)
                except Exception:
                    self.error_signal_publish.emit("Function name not found/created")
                    #raise ValueError("Function name not found/created")
                    return
                    
                    
        # for _ in range(5):
        #     try:
        #         element1 = self.wait.until(ec.element_to_be_clickable((By.XPATH, f"//a[contains(@id,'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[contains(@class, 'rich-hover-clip-cell clip-cell-nowrap-max-width') and text() = '{test_case_name}']")))
        #         self.driver.execute_script("arguments[0].scrollIntoView(true)", element1)
        #         self.driver.execute_script("arguments[0].click();", element1)
        #         break
        #     except Exception:
        #         time.sleep(1)
        
        time.sleep(3)
        
        # PUI
        
        
        try:
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            pui_xpath = "//a[@title='TEST CASE PUI']"
            self.scrollnclickParent(pui_xpath, "xpath", visible_section)
            self.iframe_test_data_writer_updation(row['Test Case PUI'], "Editor, editor1")
            
            time.sleep(3)
            
            # precondition
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            precondition = "a[title='Pre-Condition']"
            self.scrollnclickParent(precondition, "css", visible_section)
            print("clciked precondition")
            self.iframe_test_data_writer_updation(row['Precondition'], "Editor, editor2")
            
            time.sleep(3)
            # input
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            input_data = "a[title='Test Input']"
            self.scrollnclickParent(input_data, "css", visible_section)
            print("clciked input")
            self.iframe_test_data_writer_updation(row['Input'],"Editor, editor3")
            
            time.sleep(3)
            # output
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            expected_result = "/html/body/div[1]/div/table/tbody/tr[1]/td[2]/div[2]/div/div[1]/div[5]/div/div[3]/div/div[3]/div[3]/div/div/div/div/table/tbody/tr/td[1]/div/div[1]/div/div[2]/ul[1]/li[7]/a"
            self.scrollnclickParent(expected_result, "xpath", visible_section)
            print("expected result")    
            
            self.iframe_test_data_writer_updation(row['Expected output'], "Editor, editor4")
            
        
            time.sleep(3)
            print("********************************************************************************")
            visible_section = WebDriverWait(self.driver, 10).until(ec.visibility_of_element_located((By.CSS_SELECTOR,"div.dijitVisible")))
            button_path = "button[title='Save'][tabindex='0']:not([disabled])"
            self.scrollnclickParent(button_path, "css", visible_section)
            print("********************************************************************************")
        except Exception as e:
            raise ValueError(f"Error in {test_case_name}----{e}")
        
        self.driver.back()
       
    
    
    
    def update_test_suites(self):   
        
        #find testing plan
        self.update_scrapper_signal.emit("Selecting the project")
        path = f"//*[text()='{self.startProcessData['current_test_plan']}']"
        try:
            self.wait.until(ec.presence_of_element_located((By.XPATH, path))).click()  #ui_data
        except Exception:
            self.error_signal_publish.emit(f"{self.startProcessData['current_test_plan']} not found")
            return
        total_case = len(self.df)    
        #iterrate each row of the ITP/TVPR excel   
        print("iteration over df about to begin")

        print(total_case)
        for index,row in self.df.iterrows():
            # if row["Requirement"]=="VATC Self Monitoring":
            #     return
            # print(index, row)
            # print(row['Requirement'])
            print(f"Currently processing row: {index},{row['Test Case Name']}")                        
            function_name_parent = str(row['Requirement']).strip()
            function_name = ' '.join(function_name_parent.split())
            

            
            #check function name or test case name is empty
            if pd.isna(row['Requirement']) or pd.isna(row['Test Case Name']):
                continue
            #check function is already added or not
            elif function_name not in self.test_suites_list:
                #check function is already added in the previous program execution
                self.driver.refresh()
                try:
                    button1 = self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_MenuPopup_6")))
                    self.driver.execute_script("arguments[0].scrollIntoView(true)", button1)
                    self.driver.execute_script("arguments[0].click();", button1)
                except Exception:
                    self.error_signal_publish.emit("Planning button not found/clickable")
                    return
                try:
                    button2 = self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_menu_MenuItem_0_text")))
                    self.driver.execute_script("arguments[0].scrollIntoView(true)", button2)
                    self.driver.execute_script("arguments[0].click();", button2)
                except Exception:
                    self.error_signal_publish.emit("Test plans button not found/clickable")
                    return

                try:
                    test_plan_path = f"//a[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[@class='rich-hover-clip-cell clip-cell-nowrap-max-width' and normalize-space(text())=\"{self.startProcessData['current_test_plan']}\"]"
                    self.scrollnclick(test_plan_path)
    
                    for i in range(3):
                        try:
                            test_suites_button = self.wait.until(ec.element_to_be_clickable((By.XPATH,"//a[@title='Test Suites']")))
                            test_suites_button.click()
                            break
                        except Exception:
                            if i == 2:
                                self.error_signal_publish.emit("Test suite button not found/clickable")
                                return
                            else:
                                time.sleep(1)
              
                    self.create_test_suite(function_name)
                    self.test_suites_list.append(function_name)
                    with open(f"{self.test_suite_list_path}", 'w') as f:
                        json.dump(self.test_suites_list, f)
    
                    self.test_suite_case_dictionary[function_name] = []
                    time.sleep(1)
                    self.update_test_case(row)
                except Exception as e:
                    print(e)
                    return


            else:
                #update test case only when function is already present
                print("ALREADY PRESENT", row['Requirement'])
                test_case_name_parent  = str(row['Test Case Name']).strip()
                test_case_name = ' '.join(word.strip() for word in test_case_name_parent.split())
                print("---", test_case_name)
                
                if function_name in self.test_suite_case_dictionary:
                    # print(test_case_name, function_name, self.test_suite_case_dictionary[function_name])
                    # print("Updated", row['Updated'])
                    # print(f"1{type(test_case_name)}12{type(self.test_suite_case_dictionary[function_name][0])}2")
                    if test_case_name in self.test_suite_case_dictionary[function_name] and (pd.isna(row['Updated']) or row['Updated'].lower() != 'updated' or row['Updated'].lower() != 'delete' or row['Updated'].lower() != 'linking'):
                        print("Test case already present", test_case_name)
              
                        # time.sleep(10)
                
                    else:
                        print("else part")
                        self.driver.refresh()
                        try:
                            button1 = self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_MenuPopup_6")))
                            self.driver.execute_script("arguments[0].scrollIntoView(true)", button1)
                            self.driver.execute_script("arguments[0].click();", button1)
                        except Exception:
                            self.error_signal_publish.emit("Planning button not found/clickable")
                            return
                        try:
                            button2 = self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_menu_MenuItem_0_text")))
                            self.driver.execute_script("arguments[0].scrollIntoView(true)", button2)
                            self.driver.execute_script("arguments[0].click();", button2)
                        except Exception:
                            self.error_signal_publish.emit("Test plans button not found/clickable")
                            return
                        try:
                            test_plan_path = f"//a[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[@class='rich-hover-clip-cell clip-cell-nowrap-max-width' and normalize-space(text())='{self.startProcessData['current_test_plan']}']"
                            self.scrollnclick(test_plan_path)
        
                            for i in range(3):
                                try:
                                    test_suites_button = self.wait.until(ec.element_to_be_clickable((By.XPATH,"//a[@title='Test Suites']")))
                                    test_suites_button.click()
                                    break
                                except Exception:
                                    if i == 2:
                                        self.error_signal_publish.emit("Test suite button not found/clickable")
                                        return
                                    else:
                                        time.sleep(1)
                            time.sleep(1)
                            self.update_test_case(row)
                        except Exception as e:
                            print(e)
                            return
                else:
                    self.driver.refresh()
                    try:
                        button1 = self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_MenuPopup_6")))
                        self.driver.execute_script("arguments[0].scrollIntoView(true)", button1)
                        self.driver.execute_script("arguments[0].click();", button1)
                    except Exception:
                        self.error_signal_publish.emit("Planning button not found/clickable")
                        return
                    try:
                        button2 = self.wait.until(ec.presence_of_element_located((By.ID, "jazz_ui_menu_MenuItem_0_text")))
                        self.driver.execute_script("arguments[0].scrollIntoView(true)", button2)
                        self.driver.execute_script("arguments[0].click();", button2)
                    except Exception:
                        self.error_signal_publish.emit("Test plansbutton not found/clickable")
                        return
                    
                    try:
                        test_plan_path = f"//a[contains(@id, 'com_ibm_asq_common_web_ui_internal_widgets_tableViewer_ResourceLink')]//div[@class='rich-hover-clip-cell clip-cell-nowrap-max-width' and normalize-space(text())='{self.startProcessData['current_test_plan']}']"
                        self.scrollnclick(test_plan_path)
    
                        for i in range(3):
                            try:
                                test_suites_button = self.wait.until(ec.element_to_be_clickable((By.XPATH,"//a[@title='Test Suites']")))
                                test_suites_button.click()
                                break
                            except Exception:
                                if i == 2:
                                    self.error_signal_publish.emit("Test suite button not found/clickable")

                                    return
                                else:
                                    time.sleep(1)
    
                        self.update_test_case(row)
                    except Exception as e:
                        print(f"error in {test_case_name}",e)
                        return


            temp_string = f"Test Case No: {index+1}\nFunction Name: {row['Requirement']}\nTest Case Name:{row['Test Case Name']}\nStatus: Done"
            self.update_scrapper_signal.emit(temp_string)
            data.current_progress_value=int(((index+1)/total_case)*100)
            self.updated_uploader_progress_signal.emit(str(data.current_progress_value))
        
        
        
    
        



# start_time= time.perf_counter()

# uploader = QLM_Uploader()
# uploader.start_process()
# end_time = time.perf_counter()
# elapsed_time = end_time-start_time



# print(f"time taken is------{elapsed_time:.4f}")


