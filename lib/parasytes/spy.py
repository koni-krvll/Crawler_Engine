from os import getenv
from json import load
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
from dotenv import load_dotenv
from time import sleep

load_dotenv()

# Google cookies
COOKIES = [
    {'domain': '.google.com', 'expiry': 1676371033, 'httpOnly': True, 'name': 'NID', 'path': '/', 'sameSite': 'None', 'secure': True,
        'value': '511=FJH5J2uCzcHwg-SIL94xBXkL7H0zVQFgPIbZFLAIPtokbW_Kwff7gDhmkKPkC9tUdRLRyC0WYFBMGw6yWAfO6PcwjXY_QCFj8kHSKs02vTD4fb44WsTxTugNfbpE50_CtgqP_l-7Le1C1wpqxJzZ6xPqWktxxqc_O0mnT1DXV88'},
    {'domain': '.google.com', 'expiry': 1694687833, 'httpOnly': False, 'name': 'SOCS', 'path': '/', 'sameSite': 'Lax', 'secure': True,
        'value': 'CAISNQgEEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjIwODA5LjE0X3AwGgJlbiACGgYIgJnmlwY'},
    {'domain': '.google.com', 'expiry': 1695119830, 'httpOnly': False,
        'name': 'CONSENT', 'path': '/', 'secure': True, 'value': 'PENDING+934'}
]


def getSpy():
    # Set up the browser and initialize
    chrome_options = Options()
    # if __name__ == "__main__":
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.binary_location = getenv("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(
        executable_path=getenv("CHROMEDRIVER_PATH"),
        options=chrome_options
    )

    # Load cookies into browser (Used for bypassing Google)
    driver.execute_cdp_cmd('Network.enable', {})
    for cookie in COOKIES:
        driver.execute_cdp_cmd("Network.setCookie", cookie)
    driver.execute_cdp_cmd('Network.disable', {})

    # Call stealth module
    stealth(driver,
            languages=["en-US", "en-GB", "q=0.9", "en", "q=0.8"],
            vendor="Google Inc.",
            platform="macOS",
            webgl_vendor="Google Inc. (Apple)",
            renderer="ANGLE (Apple, Apple M1 Pro, OpenGL 4.1)",
            fix_hairline=True,
            )

    return driver
