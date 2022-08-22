from os import getenv
from dotenv import load_dotenv
from googlemaps import Client
from lib.parasytes.spy import getSpy

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

gmaps = Client(key=getenv("MAPS_API"), queries_per_second=32)


def waitForMapsData(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@class='g2BVhd eoFzo']")))


def getPlace(query):
    result = gmaps.find_place(
        input=query,
        input_type="textquery",
        location_bias='circle:20000@52.5200,13.4050'
    )
    results = result['candidates']
    place = results[0]
    return getPlaceId(place['place_id'])


def getPlaceId(id):
    return gmaps.place(place_id=id)


def getPopularTimes(id):
    spy = getSpy()
    spy.get(f'https://www.google.com/maps/place/?q=place_id:{id}')
    parent = spy.find_elements(
        by='xpath', value="//div[@class='g2BVhd eoFzo']")[0]
    children = parent.find_elements(by='xpath', value="div[@aria-label]")
    result = {'now': {}, 'hours': [None] * 24}
    for child in children:
        label = child.get_attribute('aria-label')
        if 'Currently' in label:
            (currently_line, usually_line) = label.split(',')
            currently = int(currently_line.split('%')[0].split(' ')[-1])
            usually = int(usually_line.split('%')[0].split(' ')[-1])
            result['now'].update({'currently': currently, 'usually': usually})
        else:
            number = int(label.split('%')[0])
            hour = int(label.split(' ')[-2])
            if 'pm' in label and hour != 12:
                hour += 12
            if 'am' in label and hour == 12:
                hour = 0
            result['hours'][hour] = number
    result['hours'] = [result['now']['usually']
                       if v is None else v for v in result['hours']]
    return result
