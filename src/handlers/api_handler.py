import requests
import json
from time import sleep
# from src.config import logger_cfg


def get_jwt_token(url):
    r = requests.post(url, json={"username": "test1", "password": "12345"})
    print('access_token', json.loads(r.content)['accessToken'], '\ncookie_jwt', r.cookies.get('jwt'))
    return {
        'access_token': json.loads(r.content)['accessToken'],
        'cookie_jwt': r.cookies.get('jwt')
    }


def refresh_jwt_token(url, access_token, cookie_jwt):
    sleep(5)
    headers = {'authorization': f'Bearer {access_token}'}
    cookies = {
        'jwt': cookie_jwt,
    }
    r = requests.get(url, cookies=cookies, headers=headers)
    print(json.loads(r.content)['accessToken'])
    # logger_cfg.logger1.info(f"JWT Token refreshed: \nNew token{json.loads(r.content)['accessToken']}")


def send_offer_to_api(url, offer_data):
    # @TODO -> LOW: make this when API will be ready
    pass


def get_offers_list_from_api():
    # @TODO -> LOW: get_offers_list_from_api()
    pass


# @TODO - make this, the code below works
# jwt_data = get_jwt_token('http://localhost:3000/re/auth')
# refresh_jwt_token('http://localhost:3000/re/refresh', access_token=jwt_data['access_token'],
#                   cookie_jwt=jwt_data['cookie_jwt'])
    