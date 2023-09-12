from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeDriverService
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from src.config import config_data
from operator import itemgetter

config_data = config_data.get_config_data()
web_browser_driver_from_config = itemgetter('web_browser_driver')(config_data)
web_driver_auto_install = itemgetter('web_driver_auto_install')(config_data)


def start_web_browser_driver(web_browser_driver: str, auto_install: bool):
    # @TODO: add to the config file
    sleep_time = 5

    options = Options()
    # service = ChromeDriverService('/drivers/chromedriver')

    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if web_browser_driver == 'chrome':
        if auto_install:
            webdriver.Chrome(ChromeDriverManager().install())
        chrome_driver = webdriver.Chrome(options=options)
        chrome_wait = WebDriverWait(chrome_driver, sleep_time)
        return chrome_driver, chrome_wait
    elif web_browser_driver == 'firefox':
        if web_driver_auto_install:
            webdriver.Firefox(executable_path=GeckoDriverManager().install())
        firefox_driver = webdriver.Firefox(options=options)
        firefox_wait = WebDriverWait(firefox_driver, sleep_time)
        return firefox_driver, firefox_wait


driver, wait = start_web_browser_driver(web_browser_driver_from_config, web_driver_auto_install)
SLEEP_TIME = 5
