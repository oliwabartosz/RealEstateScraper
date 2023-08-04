import asyncio
import traceback
from operator import itemgetter
from tqdm import tqdm
import __syspath__
from src.config import config_data
from src.scrapper import scrapper_functions
from src.scrapper import questions
from src.scrapper.scrapper_functions import download_images
from src.handlers import file_handler, api_handler
from src.handlers.file_handler import load_json_file


if __name__ == "__main__":

    # Load important data from config file
    data = config_data.get_config_data()
    rer_url = itemgetter('rer_url')(data)

    # Initial questions
    offers_type = questions.type_of_offers()

    # Ask if user wants to delete previously downloaded data
    questions.delete_previous_run()

    # Gets the data to download
    offers_to_download = scrapper_functions.get_offers_list_from_file()

    # Starts browser session and gets the data
    scrapper_functions.login()

    # Get JWT AUTH TOKEN
    jwt_data = api_handler.get_jwt_token(f'{rer_url}/rer/auth')

    for offer_id in tqdm(offers_to_download):
        if scrapper_functions.input_to_searchbar(offer_id):
            try:
                scrapper_functions.get_offers_data(offers_type, offer_id, jwt_data['access_token'])
                scrapper_functions.get_images_links(offer_id)
            except Exception as e:
                print(e)
                scrapper_functions.logout()
                traceback.print_exc()
                exit(1)

    scrapper_functions.logout()

    # Download images
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download_images(load_json_file(file_handler.FILE_PATH_IMAGES)))

    # Send image to remote server using SSH
    file_handler.send_images_to_ssh()

    # End.
    scrapper_functions.statuses_summary()



