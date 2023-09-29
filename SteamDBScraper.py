import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import os

class SteamDBScraper():
    class Locators():
        LOGIN_BUTTON_1 = (By.XPATH, '/html/body/div[1]/div[3]/a/')
        LOGIN_BUTTON_2 = (By.XPATH, '//*[@id="js-sign-in"]')

        LOGIN_INPUT = (By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input')
        PASSWORD_INPUT = (By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input')
        LOGIN_SUBMIT_1 = (By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[1]/div/div/div/div[2]/div/form/div[4]/button')
        LOGIN_SUBMIT_2 = (By.XPATH, '//*[@id="imageLogin"]')

        DOWNLOAD_BUTTON = (By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div[2]/div[4]/div[2]/div/div[2]/svg/g[6]/g/image')
        DOWNLOAD_CSV_OPT = (By.XPATH, '/html/body/div[5]/div[2]/div[2]/div/div[2]/div[4]/div[2]/div/div[2]/div/ul/li[1]')

    def __init__(self, login, password):
        options = Options()
        options.add_argument('--auto-open-devtools-for-tabs')

        self.driver = uc.Chrome(options=options)
        self.login = login
        self.password = password

        params = {
            "behavior": "allow",
            "downloadPath": os.getcwd() + '/tmp'
        }
        self.driver.execute_cdp_cmd("Page.setDownloadBehavior", params)

    def __DoAuth(self):
        self.driver.get("https://steamdb.info/")

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.LOGIN_BUTTON_1)).click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.LOGIN_BUTTON_2)).click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.LOGIN_INPUT)).send_keys(self.login)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.PASSWORD_INPUT)).send_keys(self.password)
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.LOGIN_SUBMIT_1)).click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.LOGIN_SUBMIT_2)).click()

    def DoAuth(self):
        self.__DoAuth()

    def FetchInterestOverTime(self, appid):
        self.driver.get(f"https://steamdb.info/app/{appid}/charts/")

        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.DOWNLOAD_BUTTON)).click()
        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.DOWNLOAD_CSV_OPT)).click()

        csv = pd.read_csv('tmp/chart.csv')
        os.remove('tmp/chart.csv')

        return csv
    
    def DoClose(self):
        self.driver.close()
        self.driver.quit()