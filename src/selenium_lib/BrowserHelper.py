from selenium_driverless import webdriver
from time import sleep
import os, random, sys,requests,threading
from selenium_driverless.types.by import By
from selenium_driverless.webdriver import WebElement

class Helper:
    def __init__(self,driver:webdriver.Chrome,config:str,headless:bool,proxy:str,index:int):
        self.browser = driver
        self.config=config
        self.index = index
        self.headless = headless
        self.proxy = proxy

    def execute_javascript(self,script):
        self.browser.execute_script(script=script)
        
    def safe_send(self,element:WebElement,text:str):
        try:
            for char in text:
                element.send_keys(char)
        except Exception as e:
            print(e)
    
    def safe_click(self,element:WebElement):
        element.click(timeout=15)
    
    def search_element(self,by:By,value:str):
        try:
            element = self.browser.find_element(by,value)
            if element:
                return element
        except:
            return ""
        
