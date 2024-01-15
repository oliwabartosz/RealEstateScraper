from operator import itemgetter
import scrapper_functions_aux
from src.config import selenium_cfg
from src.config import logger_cfg
from src.config import selectors
from src.handlers import file_handler
from src.handlers import api_handler
from src.config import config_data
from selenium.webdriver import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from PIL import Image
import traceback
import asyncio
import aiohttp
import os
from tqdm import tqdm
import requests

# @TODO: make in function: images_data_to_json?
images_data_to_json = file_handler.load_json_file(file_handler.FILE_PATH_IMAGES) if os.path.exists(
    file_handler.FILE_PATH_IMAGES) else []

data = config_data.get_config_data()

website_url, login_data, password_data, save_to_database = itemgetter('website_url',
                                                                      'login_data',
                                                                      'password_data',
                                                                      'save_to_database'
                                                                      )(data)


def login() -> None:
    """Log in to website"""

    # Go to web and locate forms
    selenium_cfg.driver.get(website_url)
    login_form = selenium_cfg.driver.find_element("xpath", selectors.XPATH_LOGIN_INPUT)
    password_form = selenium_cfg.driver.find_element("xpath", selectors.XPATH_PASSWORD_INPUT)

    # Type data to forms and confirm it.
    login_form.send_keys(login_data)
    password_form.send_keys(password_data)
    sleep(selenium_cfg.SLEEP_TIME - 3)
    password_form.send_keys(Keys.ENTER)
    logger_cfg.logger_scrapper.info('Email & Password submitted.')
    sleep(selenium_cfg.SLEEP_TIME)
    logger_cfg.logger_scrapper.info(f'Logged in. Waiting {selenium_cfg.SLEEP_TIME}s.')

    # Close unwanted ads
    if scrapper_functions_aux.close_unwanted_ad():
        logger_cfg.logger_scrapper.info('Closed unwanted ad.')


def logout() -> None:
    """Logouts from the website"""
    selenium_cfg.wait.until(EC.element_to_be_clickable(("xpath", selectors.XPATH_LOGOUT_BTN_ARROW)))
    selenium_cfg.driver.find_element("class name", selectors.CLASS_LOGOUT_BTN_ARROW).click()
    selenium_cfg.driver.find_element("xpath", selectors.XPATH_LOGOUT_BTN).click()
    logger_cfg.logger_scrapper.info('Logged out.')
    selenium_cfg.driver.quit()
    logger_cfg.logger_scrapper.info('Session ended.')


def quit_browser() -> None:
    """
    Quits Selenium's session.
    :return: None.
    """
    selenium_cfg.driver.quit()
    logger_cfg.logger_scrapper.info("Browser's session ended.")


def get_offers_list_from_file() -> list:
    # Open data

    try:
        offers: list = file_handler.load_txt_file(file_handler.FILE_PATH_INPUT, split=True)
        logger_cfg.logger_scrapper.info(f"{len(offers)} offers is going to be downloaded.")

        # Handle statuses.json and returns offers_to_remove list
        offers_to_remove = scrapper_functions_aux.handle_statuses_json(offers)

        # Remove offers from input if were downloaded or skipped
        offers_removed = list(filter(lambda x: x in offers_to_remove, offers))
        offers = list(filter(lambda x: x not in offers_to_remove, offers))

        logger_cfg.logger_input.info(f"{len(offers_removed)} offers removed from input - based on statuses.json.")

        return offers

    except FileNotFoundError as e:
        file_name_from_error_message = str(e).split(": ")[-1].strip("'").split('/')[-1]
        logger_cfg.logger_scrapper.warning(f"Are you sure that {file_name_from_error_message} exists?")
        logger_cfg.logger_warnings.warning(f"{file_name_from_error_message} doesn't exists.")
        try:
            logout()
            exit(1)
        except TimeoutException:
            quit_browser()
            exit(1)
    except Exception as e:
        logger_cfg.logger_warnings.warning(f'Something went wrong: {e}')
        print(e)
        try:
            logout()
        except:
            pass
        quit_browser()
        traceback.print_exc()
        exit(1)


def input_to_searchbar(offer_id: str) -> bool:
    # Close unwanted ads
    if scrapper_functions_aux.close_unwanted_ad():
        logger_cfg.logger_scrapper.info('Closed unwanted ad.')

    # Input data
    searchbar = scrapper_functions_aux.locate_searchbar()

    logger_cfg.logger_scrapper.info(f"{offer_id} is going to be downloaded.")

    for char in offer_id:
        searchbar.send_keys(char)
        sleep(.9)
    sleep(selenium_cfg.SLEEP_TIME)  # sometimes wrong offers hit, so sleep should help

    if scrapper_functions_aux.check_if_offer_exists():
        logger_cfg.logger_scrapper.info(f'The offer {offer_id} not found. Skipping it.')
        searchbar.clear()
        searchbar.send_keys(Keys.ESCAPE)
        file_handler.save_offer_data_to_file({offer_id: "skipped"}, file_name=file_handler.FILE_PATH_STATUSES,
                                             file_name_str='statuses.json')
        return False
    else:
        searchbar.send_keys(Keys.RETURN)
        searchbar.clear()
        sleep(selenium_cfg.SLEEP_TIME)
        return True


def download_offers_data_from_web(offers_type: str, offer_id: str, access_token: str) -> bool:
    """
    Downloads the data from the webpage.
    :param offers_type: provided from user type of offers (F - Flats, H - Houses, P - Plots)
    :param offer_id: a string taken from input.txt
    :param access_token: JWT access token.
    :return: False when OfferId on the webpage is not the same as OfferId from input.txt.
    """
    offer_data = {}

    # Offer ID evaluation
    offer_id_value: str = selenium_cfg.driver.find_element("xpath", selectors.XPATH_OFFER_ID).text
    swo_number: str = scrapper_functions_aux.find_swo_id_value()
    evaluation_ids = [offer_id_value, swo_number]

    # Handle issue when offer id is not equal with the offer id on webpage
    if offer_id not in evaluation_ids:
        logger_cfg.logger_warnings.warning(
            f'Searched offer ({offer_id}) is not what has been found on website ({offer_id_value} or {swo_number}). ' +
            'This is not the offer supposed to download! Retrying.')
        return False

    # Clean '/' in offer_ids because it generates issues with downloading images, etc.
    cleaned_offer_id = offer_id.replace("/", "") if "/" in offer_id else None
    cleaned_offer_id_value = offer_id_value.replace("/", "") if "/" in offer_id_value else None

    # Get keys and values from the table from the webpage
    keys_elements = selenium_cfg.driver.find_elements("xpath", selectors.XPATH_KEYS)
    values_elements = selenium_cfg.driver.find_elements("xpath", selectors.XPATH_VALUES)

    offer_data['Numer oferty'] = cleaned_offer_id_value or offer_id_value
    offer_data['Numer oferty pożądany'] = cleaned_offer_id or offer_id

    # Getting the data
    for key, value in zip(keys_elements, values_elements):
        offer_data[key.text] = value.text

    logger_cfg.logger_scrapper.info(f"Got data from {len(keys_elements)} tables.")

    # Clear data from junk (by keys)
    offer_data = scrapper_functions_aux.clear_data_from_unnecessary_keys(offers_type, offer_data)

    # Clear values from junk (PLNs, whitespaces, etc.)
    offer_data = scrapper_functions_aux.clear_data_values_from_unnecessary_things(offer_data)

    # Create chunks of data
    offer_data = scrapper_functions_aux.make_chunks_from_description_regex_version(offers_type, offer_data)

    # Translate data
    offer_data = scrapper_functions_aux.translate_keys(offers_type, offer_data)

    # Remove unnecessary keys
    scrapper_functions_aux.remove_keys_with_empty_string(offer_data)

    # Change commas to dots in some data - necessary for SQL Database
    scrapper_functions_aux.change_comma_to_dot(offer_data)

    # Saving data
    if save_to_database:
        api_handler.send_offer_to_api(offer_data, access_token, offers_type, endpoint='', check_if_exists=True)

    file_handler.save_offer_data_to_file({offer_id: "downloaded"}, file_name=file_handler.FILE_PATH_STATUSES,
                                         file_name_str='statuses.json')
    file_handler.save_offer_data_to_file(offer_data, file_name=file_handler.FILE_PATH_OFFERS,
                                         file_name_str='offers.json')

    return True


def get_images_links(offer_id) -> dict:
    images_links = []
    images_dict = {}

    # Clean "/" from offer_id
    offer_id = offer_id.replace("/", "") if "/" in offer_id else offer_id

    images_elements = selenium_cfg.driver.find_elements("xpath", selectors.XPATH_IMAGES_COUNT)
    if images_elements:
        logger_cfg.logger_scrapper.info(
            f'Preparing list of images to download {len(images_elements)} images for {offer_id}')
        for image_element in images_elements:
            image_link = image_element.get_attribute('href')
            images_links.append(image_link)

    else:
        logger_cfg.logger_scrapper.info(f'No images found for {offer_id}.')

    images_dict.update({
        offer_id: images_links
    })

    images_data_to_json.append(images_dict)
    file_handler.save_images_links_to_file(images_data_to_json)

    return images_dict


async def download_image_async(url, folder):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(limit=1)) as session:
        async with session.get(url) as response:
            if response.status == 200:
                image_data = await response.read()
                filename = url.split("/")[-1]
                filepath = os.path.join(folder, filename)
                with open(filepath, "wb") as file:
                    file.write(image_data)
                    logger_cfg.logger_scrapper.info(f"Downloaded {url} to {filepath}")
            else:
                logger_cfg.logger_scrapper.warning(f"Failed to download {url}")
                logger_cfg.logger_warnings.warning(f"Failed to download {url}")
    await asyncio.sleep(10)


async def download_images_async(offer_id_and_images_links_dict: dict):
    tasks = []

    for item in tqdm(offer_id_and_images_links_dict, desc="Downloading images", colour='green'):
        for folder, urls in item.items():
            if "/" in folder:
                folder = folder.replace("/", "")

            if not os.path.exists(file_handler.FILE_PATH_IMAGES_DIR + folder):
                os.makedirs(file_handler.FILE_PATH_IMAGES_DIR + folder)

            for url in urls:
                # Check if image has been downloaded before
                if url.split('/')[-1] + '.webp' in os.listdir(file_handler.FILE_PATH_IMAGES_DIR + folder):
                    print(f"File {url.split('/')[-1]} has been downloaded previously.")
                else:
                    task = download_image_async(url, file_handler.FILE_PATH_IMAGES_DIR + folder)
                    tasks.append(task)

    await asyncio.gather(*tasks)

    # Convert downloaded images to WebP
    image_files = []
    for item in tqdm(offer_id_and_images_links_dict, desc="Converting images", colour='red'):
        for folder, urls in item.items():
            if "/" in folder:
                folder = folder.replace("/", "")

            for url in urls:
                filename = url.split("/")[-1]
                image_path = os.path.join(file_handler.FILE_PATH_IMAGES_DIR + folder, filename)
                image_files.append(image_path)

    for image_file in image_files:
        convert_to_webp(image_file)


def convert_to_webp(image_path):
    if f"{image_path.split('/')[-1]}.webp" not in os.listdir(os.path.dirname(image_path)):
        image = Image.open(image_path)
        webp_path = os.path.splitext(image_path)[0] + ".webp"
        image.save(webp_path, "WebP")
        os.remove(image_path)


def download_image(url: str, filepath: str):
    url_request = requests.get(url)

    if url_request.status_code == 200:
        filename = f'{os.path.basename(url)}'
        filename = f'{filepath}/{filename}'
        with open(filename, "wb") as file:
            file.write(url_request.content)
            logger_cfg.logger_scrapper.info(f"Downloaded {url} to {filepath}")
    else:
        logger_cfg.logger_scrapper.warning(f"Failed to download {url}")
        logger_cfg.logger_warnings.warning(f"Failed to download {url}")


def download_images(offer_id_and_images_links_dict: dict):
    for item in tqdm(offer_id_and_images_links_dict, desc="Downloading images", colour='green'):
        for folder, urls in item.items():
            # Get rid '/' from offers id (folder names)
            if "/" in folder:
                folder = folder.replace("/", "")

            if not os.path.exists(file_handler.FILE_PATH_IMAGES_DIR + folder):
                os.makedirs(file_handler.FILE_PATH_IMAGES_DIR + folder)

            for url in urls:
                # Check if image has been downloaded before
                check_images = scrapper_functions_aux.image_previous_download_check(url, folder, extension='')
                check_images_webp = scrapper_functions_aux.image_previous_download_check(url, folder, extension='.webp')
                if not check_images and not check_images_webp:
                    download_image(url, file_handler.FILE_PATH_IMAGES_DIR + folder)

    # @TODO: duplicated code -> make a function
    # Convert downloaded images to WebP
    image_files = []
    for item in tqdm(offer_id_and_images_links_dict, desc="Converting images", colour='red'):

        # Get rid '/' from offers id (folder names)
        for folder, urls in item.items():
            if "/" in folder:
                folder = folder.replace("/", "")

            for url in urls:
                filename = url.split("/")[-1]
                image_path = os.path.join(file_handler.FILE_PATH_IMAGES_DIR + folder, filename)
                image_files.append(image_path)

    for image_file in image_files:
        try:
            convert_to_webp(image_file)
            print(f"Converting {image_file}")
        except:
            print("Coś nie tak.")
            pass


def statuses_summary():
    summary_data = file_handler.load_json_file(file_handler.FILE_PATH_STATUSES)
    unique_data = list(set(tuple(d.items()) for d in summary_data))

    skipped_count = 0
    downloaded_count = 0

    for item in unique_data:
        if "skipped" in item[0]:
            skipped_count += 1
        elif "downloaded" in item[0]:
            downloaded_count += 1

    logger_cfg.logger_scrapper.info(
        f"Summary: Total downloaded offers: {downloaded_count}; total skipped offers: {skipped_count}")
