import os
from src.handlers import file_handler
from src.config import logger_cfg


def type_of_offers():
    answer = input("Please provide offers type that you want to download.\nType F for flats, H for houses, "
                   "P for plots: ").lower()

    match answer:
        case 'f':
            logger_cfg.logger1.info('Downloading: FLATS')
            return 'flats'
        case 'h':
            logger_cfg.logger1.info('Downloading: HOUSES')
            return 'houses'
        case 'p':
            logger_cfg.logger1.info('Downloading: PLOTS')
            return 'plots'
        case _:
            print("No information or information invalid. Cannot process further operations without this information.")
            exit(1)


def delete_previous_run():
    def _delete_files(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File: {os.path.basename(file_path)} has been deleted.")

    if os.path.exists(file_handler.FILE_PATH_OFFERS) or \
            os.path.exists(file_handler.FILE_PATH_STATUSES) or \
            os.path.exists(file_handler.FILE_PATH_IMAGES):

        if input(
                f"Files from previous run have been found. Delete these files and start as clean run?"
                f"(Y/N) ").lower() == "y":

            _delete_files(file_handler.FILE_PATH_OFFERS)
            _delete_files(file_handler.FILE_PATH_STATUSES)
            _delete_files(file_handler.FILE_PATH_IMAGES)

        else:
            print("File deletion has been cancelled.")
