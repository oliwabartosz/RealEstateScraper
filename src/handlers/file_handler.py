import json
import os.path
from src.config import logger_cfg

FILE_PATH_INPUT = './data/input/input.txt'
FILE_PATH_OFFERS = './data/output/offers.json'
FILE_PATH_IMAGES = './data/output/images.json'
FILE_PATH_STATUSES = './data/output/statuses.json'
FILE_PATH_TEMPLATES = './src/scrapper/templates/chunks_templates.json'
FILE_PATH_FLATS_DICTIONARY = './src/scrapper/templates/flats_dictionary.json'
FILE_PATH_HOUSES_DICTIONARY = './src/scrapper/templates/houses_dictionary.json'
FILE_PATH_PLOTS_DICTIONARY = './src/scrapper/templates/plots_dictionary.json'


def load_json_file(file_path):
    # if file_path == FILE_PATH_OFFERS or file_path == FILE_PATH_STATUSES:
    #     _prepare_file_if_not_exists(file_path)

    with open(file_path, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def load_txt_file(file_path, split=False):
    with open(file_path, mode='r', encoding='utf-8') as file:
        if split:
            return file.read().split()
        else:
            return file.read()


def _prepare_file_if_not_exists(file_path):
    if not os.path.isfile(file_path):
        with open(file_path, mode='w', encoding='utf-8') as file:
            json.dump([], file)


def save_offer_to_file(offer_data: dict, file_name, file_name_str: str):
    offers_data_from_file = load_json_file(file_name)
    offers_data_from_file.append(offer_data)
    with open(file_name, mode='w', encoding='utf-8') as file:
        json.dump(offers_data_from_file, file)

    logger_cfg.logger1.info(f"File saved to {file_name_str}")


def save_images_links_to_file(images_dict):
    with open(FILE_PATH_IMAGES, mode='w', encoding='utf-8') as file:
        json.dump(images_dict, file)
