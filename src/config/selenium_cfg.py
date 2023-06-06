from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeDriverService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def start_chrome_driver():
    sleep_time = 5

    options = ChromeOptions()
    # service = ChromeDriverService('/drivers/chromedriver')

    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    chrome_driver = webdriver.Chrome(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(options=options)
    chrome_wait = WebDriverWait(chrome_driver, sleep_time)

    return chrome_driver, chrome_wait


driver, wait = start_chrome_driver()
SLEEP_TIME = 5
