import json


def get_login_data() -> dict:
    with open('./data/input/config.json') as config_file:
        data = json.load(config_file)

    website_url = data['website']
    login_data = data['login']
    password_data = data['password']
    ssh_hostname = data['ssh_hostname']
    ssh_username = data['ssh_username']
    ssh_password = data['ssh_password']
    ssh_port = data['ssh_port']

    return {
        'website_url': website_url,
        'login_data': login_data,
        'password_data': password_data,
        'ssh_hostname': ssh_hostname,
        'ssh_username': ssh_username,
        'ssh_password': ssh_password,
        'ssh_port': ssh_port
    }
