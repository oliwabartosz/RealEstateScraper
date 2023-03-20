import __syspath__

from src.scrapper import scrapper_functions
from src.scrapper import questions
from src.handlers import file_handler

if __name__ == "__main__":
    # Initial questions
    offers_type = questions.type_of_offers()

    # Ask if user wants to delete previously downloaded data
    file_handler.delete_offer_file(file_handler.FILE_PATH_OFFERS)
    file_handler.delete_offer_file(file_handler.FILE_PATH_STATUSES)

    # Gets the data to download
    offers_to_download = scrapper_functions.get_offers_list_from_file()

    # Starts browser session and gets the data
    scrapper_functions.login()

    # @TODO - LOW: tqdm
    for offer in offers_to_download:
        if scrapper_functions.input_to_searchbar(offer):
            scrapper_functions.get_offers_data(offer)
            scrapper_functions.get_chunks_from_description(offers_type, offer)

    scrapper_functions.logout()
    file_handler.statuses_summary()