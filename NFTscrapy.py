# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 19:34:18 2022

@author: Bill
"""


import time
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service as ChromeService
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pyautogui as p
import numpy as np

def storedataf(browser,list):
    #date
    list[1].append(WebDriverWait(browser,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layout"]/div/div/div[3]/div[1]/div[3]/div/div[2]/div[1]'))).text)
    #market cap
    list[2].append(WebDriverWait(browser,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layout"]/div/div/div[3]/div[1]/div[3]/div/div[2]/div[2]/span[2]'))).text)
    #volume
    list[3].append(WebDriverWait(browser,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layout"]/div/div/div[3]/div[1]/div[3]/div/div[2]/div[3]/span[2]'))).text)

def scrolldown(browser,x):
    browser.execute_script("window.scrollTo(0, {}*document.body.scrollHeight);".format(x))
    
if __name__ == "__main__":
    #setup the chrome selenium webdriver
    option = webdriver.ChromeOptions()
    driver_path = r'C:\Users\Bill\Desktop\HKU\7033\chrome\chromedriver.exe'
    service = ChromeService(executable_path=driver_path)
    browser = webdriver.Chrome(service=service,options = option)
    #go to the rank page to extract top 10 in 24h and store their name in a list()
    browser.get('https://nftgo.io/rank/collection')    
    time.sleep(3)
    listname = []
    listA = [[],[],[],[],[]]
    for i in range(0,10):
        nft = browser.find_element_by_xpath('*//div[contains(@id,"fixed-{}")]/div[2]/div/div[4]'.format(i)).text
        nft = nft.replace(' ','-')
        nft = nft.lower()
        listname.append(nft)
    #two of the collection have different names on ranking page and their urls so have to mannually replace it    
    listname.remove('clone-x---x-takashi-murakami')
    listname.remove('loot-(for-adventurers)')
    listname.insert(6,'rtfkt-clone-x-+-murakami')
    listname.insert(5,'loot-for-adventurers')
    browser.quit()
    #loop through the list to open a new page for a new NFT every time so that humanorrobot test can be avoided
    for name in listname:
        option = webdriver.ChromeOptions()
        driver_path = r'C:\Users\Bill\Desktop\HKU\7033\chrome\chromedriver.exe'
        service = ChromeService(executable_path=driver_path)
        browser = webdriver.Chrome(service=service,options = option)
        browser.get('https://nftgo.io/collection/{}/overview'.format(name))
        browser.maximize_window()
        #click on 30 days 
        x = browser.find_element_by_xpath('//*[@id="layout"]/div/div/div[3]/div[1]/div[1]/div[2]/div[3]')
        time.sleep(0.9)
        x.click()
        scrolldown(browser,0.1)
        time.sleep(0.5)
        #simulate the mouse movement by human to extract data from canvas
        for x in range(315,1610,44):
            p.moveTo(x,550)
            listA[0].append(name)
            try:
                storedataf(browser,listA)
            except:
                for index in (1,4):
                    listA[index].append('')
        #scrolldown to click 30days for price chart
        scrolldown(browser,0.2)
        time.sleep(1)
        y = browser.find_element_by_xpath('//*[@id="layout"]/div/div/div[3]/div[3]/div[1]/div[2]/div[3]')
        y.click()
        time.sleep(1.5)
        #extract data from price canvas chart
        for x in range(292,1643,46):
            p.moveTo(x,600)
            try:
                text = WebDriverWait(browser,2).until(EC.presence_of_element_located((By.XPATH,'//*[@id="layout"]/div/div/div[3]/div[3]/div[3]/div/div[2]/div[3]/span[2]'))).text
                if text != '':
                    listA[4].append(text)
                else:
                    listA[4].append(WebDriverWait(browser,2).until(EC.presence_of_element_located((By.XPATH,'//*[@id="layout"]/div/div/div[3]/div[3]/div[3]/div/div[2]/div[2]/span[2]'))).text)
            except:
                try:
                    p.moveTo(x,750)
                    listA[4].append(WebDriverWait(browser,2).until(EC.presence_of_element_located((By.XPATH,'//*[@id="layout"]/div/div/div[3]/div[3]/div[3]/div/div[2]/div[3]/span[2]'))).text)
                except:
                    try:
                        listA[4].append(WebDriverWait(browser,2).until(EC.presence_of_element_located((By.XPATH,'//*[@id="layout"]/div/div/div[3]/div[3]/div[3]/div/div[2]/div[2]/span[2]'))).text)
                    except:
                        listA[4].append('')
        browser.quit()
    #output data to csv, the data has not been trimmed so ending with ETH and UST will be seen, but easy transformation to float data with a little manipulation
    df = pd.DataFrame({'name':listA[0],'date':listA[1],'marketcap':listA[2],'volume':listA[3],'average price':listA[4]})
    df.to_csv(r'C:\Users\Bill\Desktop\HKU\New folder\result.csv')
        