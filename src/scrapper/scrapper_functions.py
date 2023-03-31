import json
import re
import scrapper_functions_aux
from src.config import selenium_cfg
from src.config import logger_cfg
from src.config import selectors
from src.handlers import file_handler
from src.handlers import api_handler
from selenium.webdriver import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


def get_login_data() -> tuple:
    with open('./data/input/config.json') as config_file:
        data = json.load(config_file)

    website_url = data['website']
    login_data = data['login']
    password_data = data['password']

    return website_url, login_data, password_data


def login() -> None:
    """Log in to website"""
    website_url, login_data, password_data = get_login_data()

    # Go to web and locate forms
    selenium_cfg.driver.get(website_url)
    login_form = selenium_cfg.driver.find_element("xpath", selectors.XPATH_LOGIN_INPUT)
    password_form = selenium_cfg.driver.find_element("xpath", selectors.XPATH_PASSWORD_INPUT)

    # Type data to forms and confirm it.
    login_form.send_keys(login_data)
    password_form.send_keys(password_data)
    sleep(selenium_cfg.SLEEP_TIME - 3)
    password_form.send_keys(Keys.ENTER)
    logger_cfg.logger1.info('Email & Password submitted.')
    sleep(selenium_cfg.SLEEP_TIME)
    logger_cfg.logger1.info(f'Logged in. Waiting {selenium_cfg.SLEEP_TIME}s.')


def logout() -> None:
    """Logouts from the website"""
    selenium_cfg.wait.until(EC.element_to_be_clickable(("xpath", selectors.XPATH_LOGOUT_BTN_ARROW)))
    selenium_cfg.driver.find_element("class name", selectors.CLASS_LOGOUT_BTN_ARROW).click()
    selenium_cfg.driver.find_element("xpath", selectors.XPATH_LOGOUT_BTN).click()
    logger_cfg.logger1.info('Logged out.')
    selenium_cfg.driver.quit()
    logger_cfg.logger1.info('Session ended.')


def quit_browser() -> None:
    """
    Quits Selenium's session.
    :return: None.
    """
    selenium_cfg.driver.quit()
    logger_cfg.logger1.info("Browser's session ended.")


def get_offers_list_from_file() -> list:
    # @TODO - HIGH: check if offer exists in offers or skipped jsons
    try:
        offers = open('./data/input/input.txt', 'r').read().split()
        logger_cfg.logger1.info(f"{len(offers)} offers will be downloaded.")

        statuses_of_offers = file_handler.load_file(file_handler.FILE_PATH_STATUSES)

        offers_to_remove = []
        for offer in offers:
            if file_handler.check_if_offer_was_downloaded(statuses_of_offers, offer):
                offers_to_remove.append(offer)

        offers_removed = list(filter(lambda x: x in offers_to_remove, offers))
        offers = list(filter(lambda x: x not in offers_to_remove, offers))
        logger_cfg.logger2.info(f"{len(offers_removed)} offers removed from input - based on statuses.json.")

        return offers

    except FileNotFoundError:
        logger_cfg.logger1.warning("Are you sure that input.txt exists?")
        try:
            logout()
            exit(1)
        except TimeoutException:
            quit_browser()
            exit(1)
    except:
        logger_cfg.logger1.warning('Something went wrong.')
        quit_browser()
        exit(1)


def input_to_searchbar(offer_id: str) -> bool:
    searchbar = scrapper_functions_aux.locate_searchbar()

    logger_cfg.logger1.info(f"{offer_id} will be downloaded.")

    for char in offer_id:
        searchbar.send_keys(char)
        sleep(.9)
    sleep(selenium_cfg.SLEEP_TIME)  # sometimes wrong offers hit, so sleep should help
    #@ TODO - now skipped.json has format: [{"downloaded": "31710212OMS"}], SHOULD BE: "31710212OMS":"downloaded"
    if scrapper_functions_aux.check_if_offer_exists():
        logger_cfg.logger1.info(f'The offer {offer_id} not found. Skipping it.')
        searchbar.clear()
        searchbar.send_keys(Keys.ESCAPE)
        file_handler.save_offer_to_file({"skipped": offer_id}, file_name=file_handler.FILE_PATH_STATUSES,
                                        file_name_str='statuses.json')
        return False
    else:
        searchbar.send_keys(Keys.RETURN)
        searchbar.clear()
        sleep(selenium_cfg.SLEEP_TIME)
        return True


def get_offers_data(offers_type: str, offer_id: str):
    if "/" in offer_id:
        offer_id = offer_id.replace("/", "")

    offer_data = {}

    keys_elements = selenium_cfg.driver.find_elements("xpath", selectors.XPATH_KEYS)
    values_elements = selenium_cfg.driver.find_elements("xpath", selectors.XPATH_VALUES)

    # Offer ID evaluation

    offer_number_value = selenium_cfg.driver.find_element("xpath", selectors.XPATH_OFFER_ID).text
    if "/" in offer_number_value:
        offer_number_value = offer_number_value.replace("/", "")

    offer_data['Numer oferty'] = offer_number_value
    offer_data['Numer oferty pożądany'] = offer_id

    # Getting the data
    for key, value in zip(keys_elements, values_elements):
        offer_data[key.text] = value.text

    logger_cfg.logger1.info(f"Got data from {len(keys_elements)} tables.")

    # Clear data from junk (by keys)
    offer_data = scrapper_functions_aux.clear_data_from_unnecessary_keys(offers_type, offer_data)

    # Clear values from junk (PLNs, whitespaces, etc.)
    offer_data = scrapper_functions_aux.clear_data_values_from_unnecessary_things(offer_data)

    # Create chunks of data
    offer_data = scrapper_functions_aux.make_chunks_from_description(offers_type, offer_data)

    # Translate data
    offer_data = scrapper_functions_aux.translate_keys(offers_type, offer_data)

    # Saving data
    #api_handler.send_offer_to_api(offer_data)  # @TODO - LOW: api handler
    file_handler.save_offer_to_file({"downloaded": offer_id}, file_name=file_handler.FILE_PATH_STATUSES,
                                    file_name_str='statuses.json')
    file_handler.save_offer_to_file(offer_data, file_name=file_handler.FILE_PATH_OFFERS, file_name_str='offers.json')


def get_images_links(offer_id) -> dict:
    offer_images_dict = {}
    offer_images_links = []

    images_elements = selenium_cfg.driver.find_elements("xpath", selectors.XPATH_IMAGES_FOR_OFFER)
    if images_elements:
        logger_cfg.logger1.info(f'Preparing list of images to download {len(images_elements)} images for {offer_id}')
        for image_element in images_elements:
            image_link = image_element.get_attribute('href')
            offer_images_links.append(image_link)
    else:
        logger_cfg.logger1.info(f'No images found for {offer_id}.')

    offer_images_dict.update({
        offer_id: offer_images_links
    })

    return offer_images_dict
