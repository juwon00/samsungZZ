from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

from collections import deque, defaultdict

class StationEdgeScraper :
    def __init__(self, start_url) :
        self.base_url = start_url
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")  # Run browser in headless mode
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        self.edges = defaultdict(list)
        
    def get_edges(self) :
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(5)
        
        name = self.__get_current_station_name()
        q = deque([(name, self.base_url)])
        while q :
            cur_station, cur_url = q.popleft()
            if self.driver.current_url != cur_url :
                self.driver.get(cur_url)
                self.driver.implicitly_wait(5)
            
            nxt_urls = self.__get_next_url()
            for nxt_station, nxt_url in nxt_urls :
                if nxt_station in self.edges[cur_station] :
                    continue
                self.edges[cur_station].append(nxt_station)
                q.append([nxt_station, nxt_url])
                
        self.driver.quit()

    def __get_current_station_name(self) :
        return self.driver.find_element(By.CLASS_NAME, "station_main_area").find_element(By.CLASS_NAME, "station").text + '역'
    
    def __get_next_url(self) :
        ret = []
        button = self.driver.find_element(By.CLASS_NAME, "subway_content_wrap").find_element(By.CLASS_NAME, "btn_next")
        next_station_count = len(button.find_element(By.CLASS_NAME, "station").find_elements(By.TAG_NAME, "span"))-1
        
        if next_station_count == 0 :
            return ret
        elif next_station_count == 1 :
            ActionChains(self.driver).click(button).perform()
            name = self.__get_current_station_name()
            ret.append((name, self.driver.current_url))
        
        else :
            for i in range(next_station_count) :
                button = self.driver.find_element(By.CLASS_NAME, "subway_content_wrap").find_element(By.CLASS_NAME, "btn_next")
                ActionChains(self.driver).click(button).perform()
                self.driver.implicitly_wait(5)
                
                buttons = self.driver.find_element(By.CLASS_NAME, "list_prev_next_station").find_elements(By.TAG_NAME, "button")
                ActionChains(self.driver).click(buttons[i]).perform()
                name = self.__get_current_station_name()
                ret.append((name, self.driver.current_url))
                self.driver.back()
                self.driver.implicitly_wait(5)
            
        return ret