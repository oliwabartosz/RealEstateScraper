from src.config import selenium_cfg
from src.config import logger_cfg
from src.config import selectors
from src.config import config_data
import paramiko
from operator import itemgetter
import socket


def get_images_links(offer_id) -> dict:
    images_links = []
    images_dict = {}

    images_count_per_offer = len(selenium_cfg.driver.find_elements("xpath", selectors.XPATH_IMAGES_COUNT))

    if images_count_per_offer > 0:
        logger_cfg.logger1.info(f'Images found. Preparing list of images to download for {offer_id}')

        for i in range(images_count_per_offer):
            image_link = selenium_cfg.driver.find_element("xpath", selectors.XPATH_IMAGES_COUNT + str([i + 1])) \
                .get_attribute('href')
            images_links.append(image_link)

        images_dict.update({offer_id: images_links})
    else:
        logger_cfg.logger1.info(f'No images found for {offer_id}.')

    return images_dict





def send_images_to_ssh():
    data = config_data.get_login_data()

    ssh_hostname, ssh_username, ssh_password, ssh_port = itemgetter('ssh_hostname',
                                                                    'ssh_username',
                                                                    'ssh_password',
                                                                    'ssh_port')(data)

    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(hostname=ssh_hostname, username=ssh_username, password=ssh_password, port=ssh_port)
        stdin, stdout, stderr = ssh_client.exec_command('ls')

        # TODO: add folder 'images' upload
        print(stdin, stdout, stderr)

    except socket.gaierror:
        raise ConnectionError('Connection to SSH Failed. Check hostname in config.json.')
    except paramiko.ssh_exception.AuthenticationException:
        raise ConnectionError('Connection to SSH Failed. Check if data (username, password or port) is correct in '
                              'config.json')
