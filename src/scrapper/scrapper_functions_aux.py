from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from src.config import selenium_cfg
from src.config import selectors
from src.handlers import file_handler
import re


def close_unwanted_ad():
    try:
        selenium_cfg.driver.find_element("xpath", selectors.XPATH_UNWANTED_AD).click()
        return True
    except NoSuchElementException:
        return False


def locate_searchbar():
    searchbar = selenium_cfg.wait.until(EC.element_to_be_clickable(
        (By.XPATH, selectors.XPATH_SEARCHBAR)))
    searchbar.click()
    searchbar.clear()
    return searchbar


def check_if_offer_exists() -> bool:
    return bool(selenium_cfg.driver.find_elements("xpath", selectors.XPATH_OFFER_NOT_EXISTS))


def check_if_offer_was_downloaded(offers_data: list, offer_id: str) -> bool:
    return any(offer_id in d.keys() for d in offers_data)


def _load_dictionary(offers_type):
    match offers_type:
        case 'flats':
            dictionary_flats = file_handler.load_json_file(file_handler.FILE_PATH_FLATS_DICTIONARY)
            return dictionary_flats
        case 'houses':
            dictionary_houses = file_handler.load_json_file(file_handler.FILE_PATH_HOUSES_DICTIONARY)
            return dictionary_houses
        case 'plots':
            dictionary_plots = file_handler.load_json_file(file_handler.FILE_PATH_PLOTS_DICTIONARY)
            return dictionary_plots
        case _:
            print("No information or information invalid. Cannot process further operations without this information.")
            exit(1)


def clear_data_from_unnecessary_keys(offers_type, offer_data) -> dict:
    dictionary = _load_dictionary(offers_type)

    for key in list(offer_data.keys()):
        if key not in dictionary:
            offer_data.pop(key)

    return offer_data


def clear_data_values_from_unnecessary_things(offer_data) -> dict:
    headers_parenthesis = {'Data aktualizacji'}
    headers_pln = {'Cena', 'Cena za m2', 'Czynsz administracyjny', 'Cena za parking podziemny (miejsce)',
                   'Cena za parking naziemny (miejsce)', 'Cena ofertowa', 'Cena za (m2/a/ha)'}

    for header in headers_parenthesis:
        if header in offer_data:
            offer_data[header] = re.sub(r'\s*\([^)]*\)', '', offer_data[header])

    for header in headers_pln:
        if header in offer_data:
            offer_data[header] = offer_data[header].replace("PLN", "").replace(" ", "")

    return offer_data


def translate_keys(offers_type, offer_data) -> dict:
    dictionary = _load_dictionary(offers_type)
    return {dictionary.get(key, key): value for key, value in offer_data.items()}


def remove_keys_with_empty_string(offer_data):
    keys_to_remove = [key for key, value in offer_data.items() if value == '']
    for key in keys_to_remove:
        del offer_data[key]


def change_comma_to_dot(offer_data):
    keys_to_update = ['price', 'priceM2', 'priceOffer', 'priceSold',
                      'rent', 'priceParkingUnderground', 'priceParkingGround']

    for key_to_update in keys_to_update:
        if key_to_update in offer_data:
            offer_data[key_to_update] = offer_data[key_to_update].replace(',', '.')


def make_chunks_from_description(offers_type, offers_data):
    # Load templates
    template_fields_from_json = file_handler.load_json_file(file_handler.FILE_PATH_TEMPLATES)
    description_fields = template_fields_from_json.get(offers_type)

    # Get rid of \n in a description
    offers_data['Opis'] = offers_data['Opis'].replace('\n', '')

    # Create chunks from description
    chunks = {}
    regex_builder = '(.{{0,60}}{0}.{{0,60}})'
    for description_field in description_fields:
        field_regex = re.compile(regex_builder.format(description_field), re.S | re.M)
        found_chunk = re.findall(field_regex, offers_data['Opis'])
        if found_chunk:
            chunks[description_field] = '\n'.join(found_chunk)
        else:
            chunks[description_field] = ''

    # Update offers data with created chunks
    offers_data.update(chunks)

    return offers_data
