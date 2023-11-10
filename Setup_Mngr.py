# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 15:40:07 2023

@author: quantumkid
"""
import os
import numpy as np
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import zipfile


#creates list of dates base on an input range
#can create dashed-dashed dates and int-link dates
def generate_dates(sdate,edate,qvec_type):
    #qvec_type = 0 are in format: mm/dd/yyyy
    #qvec_type = 1 are in format: mmddyyyy
    syr = None
    eyr = None
    sqtr = None
    eqtr = None
    
    if qvec_type == 0:
        syr = int(sdate[6:10])
        eyr = int(edate[6:10]) + 1
        sqtr = sdate[0:5]
        eqtr = edate[0:5]
    elif qvec_type == 1:
        syr = int(sdate[4:8])
        print(sdate[4:8])
        eyr = int(edate[4:8]) + 1
        sqtr = sdate[0:4]
        eqtr = edate[0:4]
    
    print("Start Yr: " + str(syr))
    print("End Yr: " + str(eyr))
    print("Start Qtr: " + str(sqtr))
    print("End Qtr: " + str(eqtr))
    
    output = []
    qvec = None
    if qvec_type == 0:
        qvec = np.array(["03/31","06/30","09/30","12/31"])
    elif qvec_type == 1:
        qvec = np.array(["0331","0630","0930","1231"])
    sidx = np.where(qvec == sqtr)[0]
    eidx = np.where(qvec == eqtr)[0]

    if qvec_type == 0:
        for i in range(syr,eyr):
            for j in range(0,len(qvec)):
                tqtr = ""
                if i == syr:
                    if j >= sidx:
                        tqtr = qvec[j] + "/" + str(i)
                elif i < eyr - 1:
                    tqtr = qvec[j] + "/" + str(i)
                else:
                    if j <= eidx:
                        tqtr = qvec[j] + "/" + str(i)
                if tqtr != "":
                    output.append(tqtr)
    elif qvec_type == 1:
        for i in range(syr,eyr):
            for j in range(0,len(qvec)):
                tqtr = ""
                if i == syr:
                    if j >= sidx:
                        tqtr = qvec[j] + str(i)
                elif i < eyr - 1:
                    tqtr = qvec[j] + str(i)
                else:
                    if j <= eidx:
                        tqtr = qvec[j] + str(i)
                if tqtr != "":
                    output.append(tqtr)
    return(output)
        
class Setup_Mngr:
    def __init__(self,proj_dir,proj_nm):
        #proj_dir resides in C:
        #proj_name is a string for the project name
        
        #check if project dirs exists
        self.proj_dir = proj_dir
        self.proj_nm  = proj_nm
        self.wdir_pth = "C:\\" + self.proj_dir + "\\" + self.proj_nm + "\\"
        Path(self.wdir_pth).mkdir(parents=True, exist_ok=True)
        
        #create src, data, output dirs
        self.pth_src = self.wdir_pth + "src" + "\\"
        self.pth_data = self.wdir_pth + "data" + "\\"
        self.pth_output = self.wdir_pth + "output" + "\\"
        Path(self.pth_src).mkdir(parents=True, exist_ok=True)
        Path(self.pth_data).mkdir(parents=True, exist_ok=True)
        Path(self.pth_output).mkdir(parents=True, exist_ok=True)
        
    #automates inputation of form-fields for call report data
    #and triggers downloads for desired range
    def get_cr_data_from_ffiec(self,sdate,edate,ffiec_url):
        the_data_dir = os.listdir(self.pth_data)
        if len(the_data_dir) == 0:
            #hard-coded but should be configurable
            driver = webdriver.Chrome(executable_path="C:\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe")
            driver.maximize_window()
            
            driver.get(ffiec_url)
            driver.refresh()
            
            the_dates = generate_dates(sdate, edate, 0)
            print(the_dates)
            for i in range(0,len(the_dates)):
                #select call reports -- single period
                #hard-coded as of 11/9/23 but should be configurable
                select = Select(driver.find_element(By.XPATH, "/html/body/form/div[3]/div[4]/div[1]/div/div[3]/div/div/div[2]/div[2]/div[4]/div/select"))
                select.select_by_value("ReportingSeriesSinglePeriod")
            
                #select tab separated values
                #hard-coded as of 11/9/23 but should be configurable
                driver.find_element(By.XPATH,"/html/body/form/div[3]/div[4]/div[1]/div/div[3]/div/div/div[2]/div[2]/div[7]/div/span[2]/input").click()
            
                #select date from list
                #hard-coded as of 11/9/23 but should be configurable
                select = Select(driver.find_element(By.XPATH,'/html/body/form/div[3]/div[4]/div[1]/div/div[3]/div/div/div[2]/div[2]/div[6]/div/select'))
                select.select_by_visible_text(the_dates[i])
                
                #hard-coded as of 11/9/23 but should be configurable
                driver.find_element(By.XPATH,'/html/body/form/div[3]/div[4]/div[1]/div/div[2]/div/div/div/input[1]').click()
                WebDriverWait(driver, 10)
                
    #expands zip files and deletes them from download folder
    #places expanded data in data dir for project setup
    def expand_in_project_dir(self,sdate,edate,download_url):
        the_dates = generate_dates(sdate, edate, 1)
        fname = "FFIEC CDR Call Bulk All Schedules "
        
        for i in range(0, len(the_dates)):
            ifname = fname + the_dates[i]
            
            #downloads_path = str(Path.home() / "Downloads")
            dload_pth = download_url + ifname + ".zip"
            with zipfile.ZipFile(dload_pth, 'r') as zip_ref:
                zip_ref.extractall(self.pth_data+ifname)
            os.remove(dload_pth)
 
