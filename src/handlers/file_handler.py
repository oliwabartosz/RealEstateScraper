import json
import os.path
import paramiko
import socket
from src.config import logger_cfg
from src.config import config_data
from operator import itemgetter

FILE_PATH_INPUT = './data/input/input.txt'
FILE_PATH_OFFERS = './data/output/offers.json'
FILE_PATH_STATUSES = './data/output/statuses.json'
FILE_PATH_IMAGES = './data/output/images.json'
FILE_PATH_IMAGES_DIR = './data/output/images/'

FILE_PATH_TEMPLATES = './src/scrapper/templates/chunks_templates.json'
FILE_PATH_FLATS_DICTIONARY = './src/scrapper/templates/flats_dictionary.json'
FILE_PATH_HOUSES_DICTIONARY = './src/scrapper/templates/houses_dictionary.json'
FILE_PATH_PLOTS_DICTIONARY = './src/scrapper/templates/plots_dictionary.json'



def load_json_file(file_path):
    if file_path == FILE_PATH_OFFERS or file_path == FILE_PATH_STATUSES:
        _prepare_file_if_not_exists(file_path)

    with open(file_path, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def load_txt_file(file_path, split=False):
    with open(file_path, mode='r', encoding='utf-8') as file:
        if split:
            return file.read().split()
        else:
            return file.read()


def _prepare_file_if_not_exists(file_path, start=[]):
    if not os.path.isfile(file_path):
        with open(file_path, mode='w', encoding='utf-8') as file:
            json.dump(start, file)


def save_offer_to_file(offer_data: dict, file_name, file_name_str: str):
    offers_data_from_file = load_json_file(file_name)
    offers_data_from_file.append(offer_data)
    with open(file_name, mode='w', encoding='utf-8') as file:
        json.dump(offers_data_from_file, file)

    logger_cfg.logger1.info(f"File saved to {file_name_str}")


def save_images_links_to_file(images):
    _prepare_file_if_not_exists(FILE_PATH_IMAGES)
    with open(FILE_PATH_IMAGES, mode='w', encoding='utf-8') as file:
        json.dump(images, file)

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
