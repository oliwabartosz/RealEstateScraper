from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.config import selenium_cfg
from src.config import selectors


def locate_searchbar():
    searchbar = selenium_cfg.wait.until(EC.element_to_be_clickable(
        (By.XPATH, selectors.XPATH_SEARCHBAR)))
    searchbar.click()
    searchbar.clear()
    return searchbar


def check_if_offer_exists() -> bool:
    return bool(selenium_cfg.driver.find_elements("xpath", selectors.XPATH_OFFER_NOT_EXISTS))
