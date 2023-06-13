import json


def get_config_data() -> dict:
    with open('./data/input/config.json') as config_file:
        data = json.load(config_file)

    website_url = data['website']
    login_data = data['login']
    password_data = data['password']
    ssh_hostname = data['ssh_hostname']
    ssh_username = data['ssh_username']
    ssh_password = data['ssh_password']
    ssh_port = data['ssh_port']
    jwt_api_login = data['jwt_api_login']
    jwt_api_password = data['jwt_api_password']
    api_auth_token_url = data['api_auth_token_url']
    api_refresh_token_url = data['api_refresh_token_url']
    post_flats_data_url = data['post_flats_data_url']

    return {
        'website_url': website_url,
        'login_data': login_data,
        'password_data': password_data,
        'ssh_hostname': ssh_hostname,
        'ssh_username': ssh_username,
        'ssh_password': ssh_password,
        'ssh_port': ssh_port,
        'api_auth_token_url': api_auth_token_url,
        'api_refresh_token_url': api_refresh_token_url,
        'jwt_api_login': jwt_api_login,
        'jwt_api_password': jwt_api_password,
        'post_flats_data_url': post_flats_data_url
    }
