import requests
import json
from time import sleep

from src.config import logger_cfg
from src.config.config_data import get_config_data


# from src.config import logger_cfg


def get_jwt_token(url):
    config_data = get_config_data()

    r = requests.post(url, json={"username": config_data["jwt_api_login"], "password": config_data["jwt_api_password"]})

    match r.status_code:
        case 401:
            raise Exception('401 - Wrong login or password')
        case 200:
            print('access_token', json.loads(r.content)['accessToken'], '\ncookie_jwt', r.cookies.get('jwt'))
            return {
                'access_token': json.loads(r.content)['accessToken'],
                'cookie_jwt': r.cookies.get('jwt')
            }
        case _:
            raise Exception('Something wrong happened while getting JWT TOKEN!')


def refresh_jwt_token(url, access_token, cookie_jwt):
    sleep(5)
    headers = {'authorization': f'Bearer {access_token}'}
    cookies = {
        'jwt': cookie_jwt,
    }
    r = requests.get(url, cookies=cookies, headers=headers)
    print(json.loads(r.content)['accessToken'])
    # logger_cfg.logger1.info(f"JWT Token refreshed: \nNew token{json.loads(r.content)['accessToken']}")


def send_offer_to_api(offer_data, access_token):
    sleep(5)
    headers = {'authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json; charset=utf-8'}

    json_offer_data = json.dumps(offer_data, ensure_ascii=False) # NOTE: Doesn't need to use json.dumps if request.post
                                                                 # use json=offer_data, it would be useful if in
                                                                 # request.post was used data=json_offer_data

    config_data = get_config_data()

    r = requests.post(config_data['post_flats_data_url'], json=offer_data, headers=headers)

    match r.status_code:
        case 202:
            logger_cfg.logger1.info('Response 202.')
        case 500:
            logger_cfg.logger1.warning('Response 500.')
        case _:
            logger_cfg.logger1.warning('Something bad happened while trying to post data.')


def get_offers_list_from_api():
    # @TODO -> LOW: get_offers_list_from_api()
    pass
