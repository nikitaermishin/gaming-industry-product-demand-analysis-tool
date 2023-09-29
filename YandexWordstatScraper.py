import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc 
from datetime import datetime

class YandexWordstatScraper():
  class Locators():
    LOGIN_BUTTON = (By.XPATH, '/html/body/div[1]/table/tbody/tr/td[6]/table/tbody/tr[1]/td[2]/a')
    LOGIN_INPUT = (By.XPATH, '//*[@id="b-domik_popup-username"]')
    PASSWORD_INPUT = (By.XPATH, '//*[@id="b-domik_popup-password"]')
    LOGIN_SUBMIT = (By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/div/div[5]/span[1]/input')

    SEARCH_FIELD = (By.XPATH, '/html/body/div[1]/table/tbody/tr/td[4]/div/div/form/table/tbody/tr[1]/td[1]/span/span/input')
    QUERY_HISTORY_BUTTON = (By.XPATH, "/html/body/div[1]/table/tbody/tr/td[4]/div/div/form/table/tbody/tr[2]/td[1]/table/tbody/tr/td[1]/ul/li[3]/label/input")
    SEARCH_BUTTON = (By.XPATH, '/html/body/div[1]/table/tbody/tr/td[4]/div/div/form/table/tbody/tr[1]/td[2]/span/input')

    SPINNER = (By.XPATH, '/html/body/div[7]/div/div/table/tbody/tr/td/div')

    def GetCellLocator(row_idx, column_idx):
      return (By.XPATH, f'/html/body/div[2]/div/div/div[3]/div[3]/table/tbody/tr/td[{column_idx + 1}]/div/table/tbody/tr[{row_idx + 1}]')
    
  def __ToRecord(self, cell):
    period_str = cell.find_element(By.XPATH, ".//td[1]").get_attribute("innerHTML")
    absolute_str = cell.find_element(By.XPATH, ".//td[3]").get_attribute("innerText")
    #relative_str = cell.find_element(By.XPATH, ".//td[4]").get_attribute("innerText")

    period_str_arr = period_str.split("&nbsp;-&nbsp;")
    start_period = datetime.strptime(period_str_arr[0], "%d.%m.%Y")
    end_period = datetime.strptime(period_str_arr[1], "%d.%m.%Y")

    return (start_period, end_period, int(absolute_str), 0)#float(relative_str))

  def __init__(self, login, password):
    self.driver = uc.Chrome()
    self.login = login
    self.password = password
   
  def __DoAuth(self):
    self.driver.get("https://wordstat.yandex.com/")

    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.LOGIN_BUTTON)).click()
    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.LOGIN_INPUT)).send_keys(self.login)
    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.PASSWORD_INPUT)).send_keys(self.password)
    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.LOGIN_SUBMIT)).click()

  def __DoQuery(self, keyword):
    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.QUERY_HISTORY_BUTTON)).click()
    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.SEARCH_FIELD)).clear()
    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.SEARCH_FIELD)).send_keys(keyword)
    WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(self.Locators.SEARCH_BUTTON)).click()

  def __WaitForSpinner(self):
    WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located(self.Locators.SPINNER))

  def __ParseResult(self):
    WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located(self.Locators.GetCellLocator(0, 0)))
    records = []

    for column_idx in range(2):
      for row_idx in range(12):
          cell = self.driver.find_element(*self.Locators.GetCellLocator(row_idx, column_idx))
          records.append(self.__ToRecord(cell))

    return records

  def DoAuth(self):
    self.__DoAuth()

  def FetchInterestOverTime(self, keyword):
    self.__DoQuery(keyword)
    self.__WaitForSpinner()
    result = self.__ParseResult()

    return pd.DataFrame(result, columns=['start_date', 'end_date', 'absolute_pop', 'relative_pop'])
  
  def DoClose(self):
    self.driver.close()
    self.driver.quit()