import __syspath__

from src.scrapper import scrapper_functions
from src.handlers import file_handler


file_handler.delete_offer_file()
offers_to_download = scrapper_functions.get_offers_list_from_file()

# scrapper_functions.login()
# scrapper_functions.input_to_searchbar('TRALALA')
# scrapper_functions.input_to_searchbar('AWY20674')
# scrapper_functions.get_offers_data(offer_id='AWY20674')
# scrapper_functions.logout()
