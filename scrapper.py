import __syspath__

from src.scrapper import scrapper_functions
from src.scrapper import questions
from src.handlers import file_handler
from src.handlers import images_handler

import traceback
from tqdm import tqdm

if __name__ == "__main__":
    # Initial questions
    offers_type = questions.type_of_offers()

    # Ask if user wants to delete previously downloaded data
    questions.delete_previous_run()

    # Gets the data to download
    offers_to_download = scrapper_functions.get_offers_list_from_file()

    # Starts browser session and gets the data
    scrapper_functions.login()

    for offer in tqdm(offers_to_download):
        if scrapper_functions.input_to_searchbar(offer):
            try:
                scrapper_functions.get_offers_data(offers_type, offer)
            except Exception as e:
                print(e)
                scrapper_functions.logout()
                traceback.print_exc()
                exit(1)

    scrapper_functions.logout()
    scrapper_functions.statuses_summary()
    # images_handler.send_images_to_ssh()

