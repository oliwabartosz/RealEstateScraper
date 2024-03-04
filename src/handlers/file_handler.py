import json
import os
import paramiko
from paramiko.client import SSHClient
from scp import SCPClient
from src.config import logger_cfg
from src.config import config_data
from operator import itemgetter
from tqdm import tqdm
from time import sleep

# Important paths that can be used in other .py files.
FILE_PATH_INPUT = './data/input/input.txt'
FILE_PATH_OFFERS = './data/output/offers.json'
FILE_PATH_STATUSES = './data/output/statuses.json'
FILE_PATH_IMAGES = './data/output/images.json'
FILE_PATH_IMAGES_DIR = './data/output/images/'
# Templates/dictionaries
FILE_PATH_TEMPLATES = './src/scrapper/templates/chunks_templates_regex_version.json'
FILE_PATH_LEMMATIZATION_TEMPLATES = './src/scrapper/templates/lemmatization_spacy.json'
FILE_PATH_FLATS_DICTIONARY = './src/scrapper/templates/flats_dictionary.json'
FILE_PATH_HOUSES_DICTIONARY = './src/scrapper/templates/houses_dictionary.json'
FILE_PATH_PLOTS_DICTIONARY = './src/scrapper/templates/plots_dictionary.json'

# spaCy
FILE_PATH_LEMMAS_DICT = './src/scrapper/templates/lemmatization_spacy.json'

# GPT
FILE_PATH_GPT_INPUT = './data/input/gpt.txt'
FILE_PATH_GPT_OUTPUT = './data/output/gpt_answer.txt'
# Logs
FILE_PATH_INPUT_LOG = './data/logs/input.log'
FILE_PATH_SCRAPPER_LOG = './data/logs/scrapper.log'
FILE_PATH_WARNINGS_LOG = './data/logs/warnings.log'

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


def save_txt_file(file_path, text_to_save):
    with open(file_path, 'w') as file:
        file.write(text_to_save)


def _prepare_file_if_not_exists(file_path, start=[]):
    if not os.path.isfile(file_path):
        with open(file_path, mode='w', encoding='utf-8') as file:
            json.dump(start, file)


def save_offer_data_to_file(offer_data: dict, file_name, file_name_str: str):
    offers_data_from_file = load_json_file(file_name)
    offers_data_from_file.append(offer_data)
    with open(file_name, mode='w', encoding='utf-8') as file:
        json.dump(offers_data_from_file, file)

    logger_cfg.logger_scrapper.info(f"File saved to {file_name_str}")


# @TODO: maybe delete this?? (images.json)
def save_images_links_to_file(images):
    _prepare_file_if_not_exists(FILE_PATH_IMAGES)
    with open(FILE_PATH_IMAGES, mode='w', encoding='utf-8') as file:
        json.dump(images, file)


def send_images_to_ssh():
    data = config_data.get_config_data()
    current_dir = os.getcwd()
    local_directory = os.path.join(current_dir, 'data', 'output', 'images/')

    ssh_host, ssh_username, ssh_password, ssh_port, ssh_remote_dir = itemgetter('ssh_hostname',
                                                                                'ssh_username',
                                                                                'ssh_password',
                                                                                'ssh_port',
                                                                                'ssh_remote_dir')(data)

    ssh = None

    while True:  # Start an infinite loop
        try:
            # Create an SSH client
            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

            # Create an SCP client
            scp = SCPClient(ssh.get_transport())

            # Iterate over files in the local directory
            logger_cfg.logger_scrapper.info('Sending images to SSH.')
            # Iterate over files in the local directory
            for root, dirs, files in tqdm(os.walk(local_directory), desc='Sending images via SSH', colour='blue'):
                for filename in files:
                    local_path = os.path.join(root, filename)
                    remote_path = os.path.join(ssh_remote_dir, root.replace(local_directory, ''), filename)

                    # Check if the file already exists on the remote server
                    sftp = ssh.open_sftp()
                    try:
                        sftp.stat(remote_path)
                        # print(f'Skipping {remote_path} - File already exists on the remote server.')
                        continue
                    except FileNotFoundError:
                        pass
                    finally:
                        sftp.close()

                    # Create the remote directory if it doesn't exist
                    remote_dir = os.path.dirname(remote_path)
                    ssh.exec_command('mkdir -p {}'.format(remote_dir))

                    # Upload the file to the remote directory
                    scp.put(local_path, remote_path)
                    # print(f'Copied {remote_path}.')

            # Close the SCP client
            scp.close()
            logger_cfg.logger_scrapper.info('Directory uploaded successfully!')
            break  # If successful, break out of the loop
        except Exception as e:
            print('An error occurred:', str(e))
            sleep(5)  # Sleep for 5 seconds before retrying
        finally:
            # Close the SSH connection
            if ssh is not None:
                ssh.close()
