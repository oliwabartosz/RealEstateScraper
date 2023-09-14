import os
from src.handlers import file_handler
from src.config import logger_cfg


def type_of_offers():
    answer = input("Please provide offers type that you want to download.\nType F for flats, H for houses, "
                   "P for plots: ").lower()

    match answer:
        case 'f':
            logger_cfg.logger_scrapper.info('Downloading: FLATS')
            return 'flats'
        case 'h':
            logger_cfg.logger_scrapper.info('Downloading: HOUSES')
            return 'houses'
        case 'p':
            logger_cfg.logger_scrapper.info('Downloading: PLOTS')
            return 'plots'
        case _:
            print("No information or information invalid. Cannot process further operations without this information.")
            exit(1)


def delete_previous_run():
    def _delete_files(file_path: str):
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File: {os.path.basename(file_path)} has been deleted.")

    def _delete_images(directory):
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            os.rmdir(directory)


    def _get_images_directories(directory):
        directories = []
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path):
                directories.append(item_path)
        return directories

    if os.path.exists(file_handler.FILE_PATH_OFFERS) or \
            os.path.exists(file_handler.FILE_PATH_STATUSES) or \
            os.path.exists(file_handler.FILE_PATH_IMAGES):

        if input(
                f"Files from previous run have been found. Delete these files and start as clean run?"
                f"(Y/N) ").lower() == "y":

            _delete_files(file_handler.FILE_PATH_OFFERS)
            _delete_files(file_handler.FILE_PATH_STATUSES)
            _delete_files(file_handler.FILE_PATH_IMAGES)

            # List of directories you want to delete contents from

            directories = _get_images_directories(os.path.abspath(file_handler.FILE_PATH_IMAGES_DIR))

            # Delete contents of each directory
            for directory in directories:
                _delete_images(directory)
            print('Images deleted.')

        else:
            print("File deletion has been cancelled.")
