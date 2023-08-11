from operator import itemgetter
import requests
import json
from time import sleep
from src.config import logger_cfg, config_data

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


def _check_if_offer_exists_in_db(access_token: str, offer_data: dict, offers_type: str, endpoint: str) -> bool:
    offer_ids: list = get_offers_data_from_api(access_token, f'/rer/api/{offers_type}/{endpoint}', 'GET')
    if offer_data['offerId'] in offer_ids:
        return True
    else:
        return False


def send_offer_to_api(offer_data: dict, access_token: str, offers_type: str, endpoint: str, check_if_exists: bool) \
        -> None:
    """
    Sends data to API.
    :param offer_data: a dictionary with data
    :param access_token: JWT access token
    :param offers_type: can be flats, houses or plots
    :param endpoint: an endpoint of the route ex. rer/api/flats/gpt, where gpt is endpoint
    :param check_if_exists: boolean to check if offer exists in database (checked by just offerId)
    :return: Nothing to return -> sends data to database.
    """
    sleep(2)

    headers = {'authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json; charset=utf-8'}

    if check_if_exists:
        if _check_if_offer_exists_in_db(access_token, offer_data, offers_type, endpoint):
            logger_cfg.logger1.info('That offer already exists in the Database.')
        #@TODO: LOGIC NEEDS TO BE BETTER, ROUTER IN EXPRESS NEEDS TO BE MODIFIED
        else:
            logger_cfg.logger1.info('Sending data to database.')
            r = requests.post(f'{rer_url}/rer/api/{offers_type}/{endpoint}', json=offer_data, headers=headers)

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


def get_offers_data_from_api(access_token: str, path: str, method: str = 'GET', *columns_to_get: str) -> list:
    """
    :param access_token: JWT Token.
    :param path: route to API.
    :param method: GET is default. Information just for better reading.
    :param columns_to_get: A column from database to get.
    :return: A list of data.
    """
    headers = {'authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json; charset=utf-8'}

    r = requests.get(f'{rer_url}{path}', headers=headers)

    if columns_to_get:
        # It returns columns that are not empty (they are being skipped) or also don't have the None value.
        return [{col: item[col] for col in columns_to_get if col in item and item[col] is not None} for item in
                r.json()]
    else:
        return r.json()
