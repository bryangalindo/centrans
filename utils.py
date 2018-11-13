import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from constants import DRIVERLOC


def make_soup(url):
    ''' Retrieves html code from url '''
    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko)'
                             ' Version/11.1.2 Safari/605.1.15'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print('Oops, you\'ve come across status code error: %s' % str(response.status_code))
    return BeautifulSoup(response.content, "lxml")


class Driver():
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(DRIVERLOC, options=options)

    def get_page(self, url):
        return self.driver.get(url)

    def find_xpath_elements(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, locator)))

    def find_xpath_element(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, locator)))

    def find_id_element(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, locator)))

    def find_id_elements(self, locator):
        pass

    def find_class_element(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, locator)))

    def find_class_elements(self, locator):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, locator)))

    def add_cookies(self, cookie_dict):
        self.driver.add_cookie(cookie_dict)

    def close(self):
        return self.driver.close()




