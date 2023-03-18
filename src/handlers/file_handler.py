import json
import os.path
from src.config import logger_cfg

FILE_PATH = './data/output/offers.json'


def load_file():
    _prepare_file_if_not_exists()

    with open(FILE_PATH, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def _prepare_file_if_not_exists():
    if not os.path.isfile(FILE_PATH):
        with open(FILE_PATH, mode='w', encoding='utf-8') as file:
            json.dump([], file)


def save_offer_to_file(offer_data: str):
    offers_data = load_file()
    if _check_if_offer_was_downloaded(offer_data):
        offers_data.append(offer_data)

        with open(FILE_PATH, mode='w', encoding='utf-8') as file:
            json.dump(offers_data, file)

        logger_cfg.logger1.info("File saved to ./data/output/offers.json.")
    else:
        logger_cfg.logger1.info("Has been downloaded previously. Skipping.")


def _check_if_offer_was_downloaded(offers_data: list, offer: str) -> bool:
    return any(offer in d for d in offers_data)


def delete_offer_file():
    if os.path.exists(FILE_PATH):
        if input(f"File {FILE_PATH} has been found - this file can store previously downloaded data. Delete the file? "
                 f"(Y/N) ").lower() == "y":
            os.remove(FILE_PATH)
            print(f"File {FILE_PATH} has been deleted.")
        else:
            print("File deletion has been cancelled.")
