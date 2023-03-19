import __syspath__

from src.scrapper import scrapper_functions
from src.handlers import file_handler

if __name__ == "__main__":

    # Ask if user wants to delete previously downloaded data
    file_handler.delete_offer_file()

    # Gets the data to download
    offers_to_download = scrapper_functions.get_offers_list_from_file()

    # Starts browser session and gets the data
    scrapper_functions.login()
    try:
        scrapper_functions.input_to_searchbar('TRALALA')
        scrapper_functions.input_to_searchbar('AWY20674')
        scrapper_functions.get_offers_data(offer_id='AWY20674')
    except:
        scrapper_functions.logout()
    finally:
        scrapper_functions.logout()
