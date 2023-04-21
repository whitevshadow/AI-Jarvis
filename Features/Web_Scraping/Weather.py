from time import sleep

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from Body.Speaker import Speak


def get_Weather(sentences):
    chrome_options = Options()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--headless')
    s = Service('Drivers\\chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.maximize_window()
    Website = f'https://www.google.com/search?q={sentences}'
    driver.get(Website)

    sleep(5)

    def City():
        try:
            City_ = driver.find_element(By.XPATH, '//*[@id="oFNiHe"]/div/div/div/div[1]').text
            return City_
        except selenium.common.exceptions.ElementNotInteractableException:
            City_Xpath = driver.find_element(By.XPATH, '/html/body/div[7]/div/div[10]/div/div[1]/div['
                                                       '1]/div/div/div/div[1]').text
            return City_Xpath

    def Temp():
        try:
            Temp_ = driver.find_element(By.XPATH, '//*[@id="wob_wc"]/div[1]/div[1]/div').text
            return Temp_
        except selenium.common.exceptions.ElementNotInteractableException:
            Temp_XPath = driver.find_element(By.XPATH,
                                             '/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div['
                                             '1]/div/div/div/div/div[1]/div[1]/div').text
            return Temp_XPath

    Temperature = Temp()
    Temperature = Temperature.replace("°F", "")

    def weather():
        try:
            Weather_ = driver.find_element(By.XPATH, '//*[@id="wob_dc"]').text
            return Weather_
        except selenium.common.exceptions.ElementNotInteractableException:
            Weather_XPath = driver.find_element(By.XPATH,
                                                '/html/body/div[7]/div/div[11]/div/div[2]/div[2]/div/div/div['
                                                '1]/div/div/div/div/div[2]/span/div[3]/span').text
            return Weather_XPath

    Weather = weather()

    def Precipitation():
        try:
            Precipitation_ = driver.find_element(By.XPATH, '//*[@id="wob_wc"]/div[1]/div[2]/div[1]').text
            return Precipitation_
        except selenium.common.exceptions.ElementNotInteractableException:
            Precipitation_XPath = driver.find_element(By.XPATH,
                                                      '/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div['
                                                      '1]/div/div/div/div/div[1]/div[2]/div[1]').text
            return Precipitation_XPath

    def Humidity():
        try:
            Humidity_ = driver.find_element(By.XPATH, '//*[@id="wob_wc"]/div[1]/div[2]/div[2]').text
            return Humidity_
        except selenium.common.exceptions.ElementNotInteractableException:
            Humidity_XPath = driver.find_element(By.XPATH,
                                                 '/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div['
                                                 '1]/div/div/div/div/div[1]/div[2]/div[2]').text
            return Humidity_XPath

    def Wind():
        try:
            Wind_ = driver.find_element(By.XPATH, '//*[@id="wob_wc"]/div[1]/div[2]/div[3]').text
            return Wind_
        except selenium.common.exceptions.ElementNotInteractableException:
            Wind_XPath = driver.find_element(By.XPATH,
                                             '/html/body/div[7]/div/div[10]/div/div[2]/div[2]/div/div/div['
                                             '1]/div/div/div/div/div[1]/div[2]/div[3]').text
            return Wind_XPath

    Precipitation = Precipitation()
    Humidity = Humidity()
    Wind = Wind()
    City = City().replace("Results for ","")

    Result = f''' Sir !! The Temperature in {City} is {Temperature}
                        The Overall Condition : {Weather}.
                        {Precipitation}
                        {Humidity}
                        {Wind}
    '''
    Speak(Result)

