import json
import os.path
from src.config import logger_cfg

FILE_PATH_OFFERS = './data/output/offers.json'
FILE_PATH_STATUSES = './data/output/statuses.json'


def load_file(file_path):
    _prepare_file_if_not_exists(file_path)

    with open(file_path, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def _prepare_file_if_not_exists(file_path):
    if not os.path.isfile(file_path):
        with open(file_path, mode='w', encoding='utf-8') as file:
            json.dump([], file)


def save_offer_to_file(offer_data: dict, file_name, file_name_str: str):
    # @TODO - MEDIUM: chceck if data encoding is correct for pandas
    offers_data_from_file = load_file(file_name)
    offers_data_from_file.append(offer_data)
    with open(file_name, mode='w', encoding='utf-8') as file:
        json.dump(offers_data_from_file, file)

    logger_cfg.logger1.info(f"File saved to {file_name_str}")


def check_if_offer_was_downloaded(offers_data: list, offer_id: str) -> bool:
    # @TODO - LOW: should be it for general purpose (file handler and api handler)?
    return any(offer_id in d.values() for d in offers_data)


def delete_offer_file(file_path):
    if os.path.exists(file_path):
        if input(
                f"File {file_path} has been found - this file can store previously downloaded data. Delete the file? "
                f"(Y/N) ").lower() == "y":
            os.remove(file_path)
            print(f"File {file_path} has been deleted.")
        else:
            print("File deletion has been cancelled.")


def statuses_summary():
    with open(FILE_PATH_STATUSES, mode='r', encoding='utf-8') as file:
        data = json.load(file)

    unique_data = list(set(tuple(d.items()) for d in data))

    skipped_count = 0
    downloaded_count = 0

    for item in unique_data:
        if "skipped" in item[0]:
            skipped_count += 1
        elif "downloaded" in item[0]:
            downloaded_count += 1

    logger_cfg.logger1.info(f"Summary: Total downloaded offers: {downloaded_count}; total skipped offers: {skipped_count}")

