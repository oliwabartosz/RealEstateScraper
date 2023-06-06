from src.config import config_data
import paramiko
from operator import itemgetter
import socket

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
