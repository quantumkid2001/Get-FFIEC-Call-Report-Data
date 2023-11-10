# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 20:03:33 2023

@author: quantumkid
"""

from Setup_Mngr import Setup_Mngr

#change to your download directory on your machine
download_url = "C:\\Users\\quantumkid\\Downloads\\"

#ensure work dir exists at C:\work\
#provide a project diretcory name
test = Setup_Mngr("work", "frbsf_code_sample3")

#supply date as mm/dd/yyyy format and ffiec bulk download url
#url up to date as of 11/9/23
test.get_cr_data_from_ffiec("03/31/2001", "06/30/2003","https://cdr.ffiec.gov/public/PWS/DownloadBulkData.aspx")

#endure dates are the same as entered for ffiec range except remove slashes
test.expand_in_project_dir("03312001", "06302003",download_url)