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
    offer_id = offer_data["Numer oferty"]
    offers_data_from_file = load_file()
    if not _check_if_offer_was_downloaded(offers_data_from_file, offer_id):
        offers_data_from_file.append(offer_data)

        with open(FILE_PATH, mode='w', encoding='utf-8') as file:
            json.dump(offers_data_from_file, file)

        logger_cfg.logger1.info("File saved to ./data/output/offers.json.")
    else:
        logger_cfg.logger1.info(f"{offer_id} has been downloaded previously. Skipping.")


def _check_if_offer_was_downloaded(offers_data: list, offer_id: str) -> bool:
    return any(offer_id in d.values() for d in offers_data)
    # return any(offer in tuple(d.items()) for d in offers_data)


def delete_offer_file():
    if os.path.exists(FILE_PATH):
        if input(f"File {FILE_PATH} has been found - this file can store previously downloaded data. Delete the file? "
                 f"(Y/N) ").lower() == "y":
            os.remove(FILE_PATH)
            print(f"File {FILE_PATH} has been deleted.")
        else:
            print("File deletion has been cancelled.")
