from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import os
import time

class PointScraper :
    def __init__(self) :
        self.base_url = "https://www.findlatlng.org/"
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run browser in headless mode
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        self.result = {}
        self.not_found = []
        
        
        
    def search(self, names) :
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(5)
        
        search_input_xpath = '//*[@id="app"]/div/div[2]/div/div/input'
        search_input = self.driver.find_element(By.XPATH, search_input_xpath)
        
        search_button_xpath = '//*[@id="app"]/div/div[2]/div/div/button'
        search_button = self.driver.find_element(By.XPATH, search_button_xpath)
        
        for name in tqdm(names, desc = "위도 경도 검색 중...", ncols = 100) :
            try :
                search_input.send_keys(name)
                ActionChains(self.driver).click(search_button).perform()
                time.sleep(1)
                
                result_xpath = '//*[@id="app"]/div/div[4]'
                result = self.driver.find_element(By.XPATH, result_xpath).text
                lattitude, longitude = self.__parse_data(result)
                
                self.result[name] = (lattitude, longitude)
            except :
                self.not_found.append(name)
        self.driver.quit()
        
    def __parse_data(self, text) :
        point_data = text.split("\n")[1].split("/")
        latitude = float(point_data[0].split(":")[1])
        logitude = float(point_data[1].split(":")[1])
        
        return latitude, logitude
            
            