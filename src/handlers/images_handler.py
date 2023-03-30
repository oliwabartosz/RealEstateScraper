from src.config import selenium_cfg
from src.config import logger_cfg
from src.config import selectors



def get_images_old(offer_id) -> dict:
    offer_images_dict = {}
    offer_images_links = []

    images_number_xpath = "(//a[contains(@class,'-images')])"

    how_many_images = len(selenium_cfg.driver.find_elements("xpath", images_number_xpath))
    if how_many_images > 0:
        logger_cfg.logger1.info(f'Preparing list of images to download for {offer_id}')
        for i in range(how_many_images):
            # i = str([i + 1]) @TODO - MEDIUM: test without it, if it works delete the line
            image_link = selenium_cfg.driver.find_element("xpath", images_number_xpath + str([i + 1])) \
                .get_attribute('href')
            offer_images_links.append(image_link)
    else:
        logger_cfg.logger1.info(f'No images found for {offer_id}.')

    offer_images_dict.update({offer_id: offer_images_links})

    return offer_images_dict


def save_images_links_to_file():
    # @TODO - MEDIUM: save_images_links_to_file():
    pass
