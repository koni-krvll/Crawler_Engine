import json
import bs4

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    

def parsePageIntoJson(rawPage):
    soup = bs4.BeautifulSoup(rawPage)
    next = soup.find('script', {'id': '__NEXT_DATA__'}).decode_contents()
    data = json.loads(next)['props']['apolloState']
    data = dict.values(data)
    return data

def waitForNextData(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//script[@id='__NEXT_DATA__']")))