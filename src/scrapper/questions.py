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
    if os.path.exists(file_handler.FILE_PATH_OFFERS) or os.path.exists(file_handler.FILE_PATH_STATUSES):
        if input(
                f"Files from previus run have been found. Delete these files and start as clean run?"
                f"(Y/N) ").lower() == "y":

            if os.path.exists(file_handler.FILE_PATH_OFFERS):
                os.remove(file_handler.FILE_PATH_OFFERS)
                print(f"File: {os.path.basename(file_handler.FILE_PATH_OFFERS)} has been deleted.")

            if os.path.exists(file_handler.FILE_PATH_STATUSES):
                os.remove(file_handler.FILE_PATH_STATUSES)
                print(f"{os.path.basename(file_handler.FILE_PATH_STATUSES)} has been deleted.")

        else:
            print("File deletion has been cancelled.")
