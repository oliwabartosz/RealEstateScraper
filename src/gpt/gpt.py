# Translator
from contextlib import suppress
import requests
from src.utils.utils import translate_result_to_pl

# Data
from src.gpt.src.get_or_send_GPT_data_to_database import offers_data, jwt_data, offers_gpt_data
from src.gpt.src.result_handler import RATED_BY_USR_STR, \
    assess_offer_parameter_wrapper

# Handlers
from src.handlers import api_handler


def start_gpt_assessment(start: int = 0,
                         end: int = None,
                         retry: bool = False,
                         data: list[dict] = offers_data,
                         offers_type: str = 'flats',
                         api: bool = True,
                         take_result_from_offer_params: bool = True,
                         include_params: list = []) -> dict:
    """
    :param start: starting point,
    :param end: ending point, if None - it takes all.
    :param retry: if True it won't be assessing records rated before. If False it reassess everything from beginning.
    :param data: a data from database to analyze.
    :param offers_type: can be flats, houses or plots.
    :param api: if True the result will be sent to SQL database
    :param take_result_from_offer_params: if True it will try to get the data from offer parameters, if GPT won't find information in
    the text.
    :param include_params: specify which parameters of real estate to include in assessment. If empty it will take all
    the specified such as 'balcony', 'lawStatus', 'garage', 'garden', 'monitoring', 'outbuilding', 'rent',
    'modernization', 'technology', 'kitchen', 'basement'.
    :return: dictionary with assessed data in English.
    """
    list_of_ids_statuses_in_gpt_db = [(item['id'], item.get('status', None)) for item in offers_gpt_data]

    if retry:
        # Make a list of IDs that have status == 0
        ids_status_eq_one = [tup[0] for tup in list_of_ids_statuses_in_gpt_db if tup[1] == 0]
        # Create a list of dicts which ids statuses are equal to 0.
        data = [d for d in data if any(val in ids_status_eq_one for val in d.values())]
        list_of_ids = ids_status_eq_one
    else:
        list_of_ids = [item['id'] for item in offers_gpt_data]

    # Error handling
    if start > len(list_of_ids):
        raise ValueError(
            f'Your start parameter (value={start}) is out of scope. It should not be greater than' +
            f'{len(list_of_ids)}!')
    elif start < 0:
        raise ValueError('start end end parameters should be a positive numbers!')
    elif retry:
        if not data:
            print("Everything has been rated before.")
    elif not retry:
        if not data:
            raise KeyError("Isn't your database empty?")

    # GPT Assessment
    for record in enumerate(data[start:end]):
        if record[1]["description"].strip == '':
            record["description"] = 'Brak opisu'
        return _assess_by_gpt(record[1], offers_type, api, take_result_from_offer_params, include_params)


def _assess_by_gpt(offer_record: dict, offers_type: str, api: bool, take_result_from_offer_params: bool,
                   include_params=[]) -> dict:
    print(f"{'-' * 30}\nAssessing {offer_record['id']}\n{'-' * 30}")
    result = {}
    params_result = []

    # Assess parameters
    if not include_params:
        include_params = ['balcony', 'lawStatus', 'garage', 'garden', 'monitoring', 'outbuilding', 'rent',
                          'modernization', 'technology', 'kitchen', 'basement', 'elevator']

    if 'balcony' in include_params:
        params_result.append(
            assess_offer_parameter_wrapper(offers_type, 'balcony', offer_record, take_result_from_offer_params))
    if 'lawStatus' in include_params:
        params_result.append(
            assess_offer_parameter_wrapper(offers_type, 'lawStatus', offer_record, take_result_from_offer_params))
    if 'garage' in include_params:
        params_result.append(
            assess_offer_parameter_wrapper(offers_type, 'garage', offer_record, take_result_from_offer_params))
    if 'garden' in include_params:
        params_result.append(
            assess_offer_parameter_wrapper(offers_type, 'garden', offer_record, take_result_from_offer_params))
    if 'monitoring' in include_params:
        params_result.append(
            assess_offer_parameter_wrapper(offers_type, 'monitoring', offer_record, take_result_from_offer_params))
    if 'outbuilding' in include_params:
        params_result.append(
            assess_offer_parameter_wrapper(offers_type, 'outbuilding', offer_record, take_result_from_offer_params))
    if 'basement' in include_params:
        params_result.append(
            assess_offer_parameter_wrapper(offers_type, 'basement', offer_record, take_result_from_offer_params))
    if 'elevator' in include_params:
        params_result.append(
            assess_offer_parameter_wrapper(offers_type, 'elevator', offer_record, take_result_from_offer_params))
    if 'rent' in include_params:
        params_result.append(
            assess_offer_parameter_wrapper(offers_type, 'rent', offer_record, take_result_from_offer_params))
    if 'modernization' in include_params:
        if 'modernizationAns' not in offer_record:
            params_result.append(
                assess_offer_parameter_wrapper(offers_type, 'modernization', offer_record,
                                               take_result_from_offer_params))
        else:
            params_result.append({"modernizationGPT": offer_record['modernizationAns'],
                                  "modernization_summary": RATED_BY_USR_STR})
    if 'technology' in include_params:
        if 'technologyAns' not in offer_record:
            params_result.append(
                assess_offer_parameter_wrapper(offers_type, 'technology', offer_record, take_result_from_offer_params))
        else:
            params_result.append({"technologyGPT": offer_record['technologyAns'],
                                  "technology_summary": RATED_BY_USR_STR})
    if 'kitchen' in include_params:
        if 'kitchenAns' not in offer_record:
            params_result.append(
                assess_offer_parameter_wrapper(offers_type, 'kitchen', offer_record, take_result_from_offer_params))
        else:
            params_result.append({"kitchenGPT": offer_record['kitchenAns'],
                                  "kitchen_summary": RATED_BY_USR_STR})

    # Updating the results
    for param_result in params_result:
        result.update(param_result)

    result.update({'id': offer_record['id'],
                   'status': 1,
                   'qualityGPT': offer_record['qualityAns'] if 'qualityAns' in offer_record else -9})

    # Translating results into Polish
    with suppress(requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        result_pl = translate_result_to_pl(result, 'pl', 'id', 'technologyGPT', 'lawStatusGPT',
                                           'elevatorGPT', 'balconyGPT', 'basementGPT', 'garageGPT', 'gardenGPT',
                                           'modernizationGPT', 'monitoringGPT', 'kitchenGPT', 'outbuildingGPT',
                                           'qualityGPT', 'status', 'rentGPT')

    if api:
        api_handler.send_offer_to_api(result_pl, jwt_data['access_token'], offers_type, endpoint='gpt',
                                      check_if_exists=False)
    return result
