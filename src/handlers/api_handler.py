from operator import itemgetter

import requests
import json
from time import sleep
from src.config import logger_cfg, config_data
from src.config.config_data import get_config_data

data = config_data.get_config_data()
rer_url, jwt_api_login, jwt_api_password = itemgetter('rer_url',
                                                      'jwt_api_login',
                                                      'jwt_api_password')(data)


def get_jwt_token(url):
    r = requests.post(url, json={"username": jwt_api_login, "password": jwt_api_password})

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


def send_offer_to_api(offer_data, access_token, offers_type):
    sleep(5)

    # Checking if that offer exists in a database
    offer_ids: list = get_offers_list_from_api(access_token)
    if offer_data['offerId'] in offer_ids:
        logger_cfg.logger1.info('That offer already exists in the Database.')
        pass
    else:
        headers = {'authorization': f'Bearer {access_token}',
                   'Content-Type': 'application/json; charset=utf-8'}

        json_offer_data = json.dumps(offer_data,
                                     ensure_ascii=False)  # NOTE: Don't need to use json.dumps if request.post
        # use json=offer_data, it would be useful if in
        # request.post was used data=json_offer_data

        r = requests.post(f'{rer_url}/rer/api/{offers_type}/', json=offer_data, headers=headers)

        match r.status_code:
            case 202:
                logger_cfg.logger1.info('Response 202. Data has been sent to the Database.')
            case 500:
                logger_cfg.logger1.warning('Response 500. Data has NOT been sent to the Database')
            case 403:
                logger_cfg.logger1.warning('Response 403. Forbidden.')
            case 404:
                logger_cfg.logger1.warning('Response 404. Check the routers.')
            case _:
                logger_cfg.logger1.warning(
                    'Something bad happened while trying to post data. Data has NOT been sent to the Database')


def get_offers_data_from_api(access_token: str, *args) -> list:
    """
    :param access_token: JWT Token
    :param columns_to_get: A column from database to get into a list
    :return: A list of given column
    """
    headers = {'authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json; charset=utf-8'}

    r = requests.get(f'{rer_url}/rer/api/flats/', headers=headers)

    if args:
        # It returns columns that are not empty (they are being skipped) or also don't have the None value.
        return [{col: item[col] for col in args if col in item and item[col] is not None} for item in r.json()]
    else:
        return r.json()
