import spacy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from src.config import selenium_cfg
from src.config import selectors
from src.handlers import file_handler
import re
import os


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


def find_swo_id_value() -> str:
    """Return the value of SWO ID from offers data"""
    key_elements = selenium_cfg.driver.find_elements("xpath", selectors.XPATH_KEYS)
    for key_element in enumerate(key_elements):

        pattern = r"\b[A-Z]+\s+ID"
        matches = re.findall(pattern, key_element[1].text)

        if matches:
            if key_element[1].text == matches[0]:
                return selenium_cfg.driver.find_elements("xpath", selectors.XPATH_VALUES)[key_element[0]].text


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
    headers_pln = {'Cena', 'Cena transakcyjna', 'Cena za m2', 'Czynsz administracyjny',
                   'Cena za parking podziemny (miejsce)',
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


def make_chunks_from_description_spacy_version(offers_type: str, offers_data: dict) -> dict:
    """
    This function creates the abbreviated description for every feature. The result looks like:
    {balconyLemma: "description only about balcony" }
    :param offers_type: offer type specified by a user's input: flats, houses, plots
    :param offers_data: data scraped from web in dictionary type
    :return: a dictionary of {key: "sentences about feature from description"
    """
    chunks = {}

    # Load the templates for lemmatization
    template_fields_from_json = file_handler.load_json_file(file_handler.FILE_PATH_LEMMATIZATION_TEMPLATES)

    # Get rid newlines and replace by a dot for making lemmatization
    offers_data_copy = offers_data.copy()
    offers_data_copy['Opis'] = offers_data['Opis'].replace('\n', '.').replace('-', '.')

    # Load spacy
    nlp = spacy.load("pl_core_news_sm")
    doc = nlp(offers_data_copy['Opis'])

    # Create list of sentences
    sentence_list = []

    # Get the description based on the specified offer type (flats, houses, plots)
    for property_feature_key in template_fields_from_json[offers_type]:
        property_feature_lemmas = template_fields_from_json[offers_type].get(property_feature_key, [])


        for sentence in doc.sents:
            for lemma in property_feature_lemmas:
                if lemma in sentence.lemma_.lower():
                    sentence_list.append(sentence.text)
        sentence_result  = list(set(sentence_list))

        # Make sure that at the end of the sentence is a period (.)
        sentence_result = ('. '.join(sentence_result)).replace('..', '.')

        # Prepare data to append offers data dictionary
        chunks[property_feature_key] = sentence_result

        # Clear the sentences previously gathered
        sentence_list = []
        
        offers_data.update(chunks)
        return offers_data

def make_chunks_from_description_regex_version(offers_type, offers_data):
    # Load prompts
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


def handle_statuses_json(offers: list) -> list:
    """
    This function loads the data from statuses.json, then checks if data was downloaded (or skipped) before.
    It prevents of trying to re-download the offers in previous run. Returns the list of offers_to_remove.
    """
    # Load statuses
    statuses_of_offers = file_handler.load_json_file(file_handler.FILE_PATH_STATUSES)

    # Check if offers have statuses like downloaded or skipped
    offers_to_remove = []
    for offer in offers:
        if check_if_offer_was_downloaded(statuses_of_offers, offer):
            offers_to_remove.append(offer)

    return offers_to_remove


def image_previous_download_check(url: str, folder: str, extension='') -> bool:
    # Check if image has been downloaded before
    if url.split('/')[-1] + extension in os.listdir(file_handler.FILE_PATH_IMAGES_DIR + folder):
        # print(f"File {url.split('/')[-1]} has been downloaded previously.")
        return True
    else:
        return False
