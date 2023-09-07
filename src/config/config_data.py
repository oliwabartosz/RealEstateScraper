import json


def get_config_data() -> dict:
    with open('./data/input/config.json') as config_file:
        data = json.load(config_file)

    website_url = data['website']
    rer_url = data['rer_url']
    login_data = data['login']
    password_data = data['password']
    ssh_hostname = data['ssh_hostname']
    ssh_username = data['ssh_username']
    ssh_password = data['ssh_password']
    ssh_port = data['ssh_port']
    ssh_remote_dir = data['ssh_remote_dir']
    jwt_api_login = data['jwt_api_login']
    jwt_api_password = data['jwt_api_password']
    OPENAI_API_KEY = data['OPENAI_API_KEY']
    web_browser_driver = data['web_browser_driver']
    web_driver_auto_install = data["web_driver_auto_install"]

    return {
        'website_url': website_url,
        'rer_url': rer_url,
        'login_data': login_data,
        'password_data': password_data,
        'ssh_hostname': ssh_hostname,
        'ssh_username': ssh_username,
        'ssh_password': ssh_password,
        'ssh_port': ssh_port,
        'ssh_remote_dir': ssh_remote_dir,
        'jwt_api_login': jwt_api_login,
        'jwt_api_password': jwt_api_password,
        'OPENAI_API_KEY': OPENAI_API_KEY,
        'web_browser_driver': web_browser_driver,
        'web_driver_auto_install': web_driver_auto_install
    }
