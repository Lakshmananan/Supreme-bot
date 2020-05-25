# -*- coding: utf-8 -*-
"""
Created on Mon May 25 11:35:37 2020

@author: laksh
"""

print('00 - Starting up')
import config
from datetime import datetime
import time
import schedule
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
print('00 - Packages loaded')

class Supreme:

    def shopping():
        global time_start, driver
        time_start  = datetime.now()
        print('01 - Executed shopping')
        driver = webdriver.Chrome(executable_path=r"C:\Users\laksh\Desktop\Scrapers\Supreme\chromedriver.exe")
        driver.get('https://www.supremenewyork.com/shop/all')
        assert 'All - Shop - Supreme' in driver.title
        print('02 - Supreme loaded')
        
        driver.find_element_by_xpath('//*[@id="nav-categories"]/li[12]/a').click()
        print('03 - Targeted page loaded')
        time.sleep(1)
        
        items = driver.find_elements_by_class_name('inner-article')
        for item in items:
            if item.text == config.PRODUCT:
                item.click()
                print('04 - Targeted item loaded')
                time.sleep(1)
                break
        
        Select(driver.find_element_by_id('s')).select_by_visible_text(config.SIZE)
        time.sleep(0.5)
        print('05 - Targeted size loaded')
        
        driver.find_element_by_xpath('//*[@id="add-remove-buttons"]/input').submit()
        time.sleep(0.5)
        print('06 - Added to cart')
        
        driver.find_element_by_xpath('//*[@id="cart"]/a[2]').click()
        print('07 - Checking out now')
    
    
    def checkout():
        global time_start, driver
        driver.find_element_by_name('order[billing_name]').send_keys(config.NAME)
        driver.find_element_by_name('order[email]').send_keys(config.EMAIL)
        driver.find_element_by_name('order[tel]').send_keys(config.PHONE)
        driver.find_element_by_name('order[billing_address]').send_keys(config.ADDRESS)
        driver.find_element_by_name('order[billing_address_2]').send_keys(config.UNIT)
        driver.find_element_by_name('order[billing_city]').send_keys(config.CITY)
        Select(driver.find_element_by_name('order[billing_country]')).select_by_visible_text(config.COUNTRY)
        Select(driver.find_element_by_name('order[billing_state]')).select_by_visible_text(config.PROVINCE)
        driver.find_element_by_name('order[billing_zip]').send_keys(config.ZIP)
        
        time_end = datetime.now()
        time_total = time_end - time_start
        print(f'Total checkout time is {time_total}')
        driver.close()
    
    def execute():
        Supreme.shopping()
        Supreme.checkout()


    def run():
        schedule.every().minute.at(":00").do(Supreme.execute)
        schedule.every().minute.at(":15").do(Supreme.execute)
        schedule.every().minute.at(":30").do(Supreme.execute)
        schedule.every().minute.at(":45").do(Supreme.execute)

        while True:
            try: 
                schedule.run_pending()
                time.sleep(1)
            except:
                continue
            
Supreme.run()