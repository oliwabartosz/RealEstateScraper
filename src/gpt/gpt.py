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


# Helps to skip reassessment if rated before and restart was needed


def start_gpt_assessment(start: int = 0, end: int = None, retry: bool = False,
                         data: list[dict] = offers_data[:2]) -> None:
    list_of_ids_statuses_in_gpt_db = [(item['id'], item.get('status', None)) for item in offers_gpt_data]
    list_of_ids_statuses_in_gpt_db = list_of_ids_statuses_in_gpt_db[:2]

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
        print(record)
        if record[1]["description"].strip == '':
            record["description"] = 'Brak opisu'
        _assess_by_gpt(record[1])


def _assess_by_gpt(offer_record: dict) -> None:
    print(f"{'-' * 30}\nAssessing {offer_record['id']}\n{'-' * 30}")
    result = {}

    # Assess parameters
    balcony_result = assess_offer_parameter_wrapper('flats', 'balcony', offer_record)
    law_status_result = assess_offer_parameter_wrapper('flats', 'lawStatus', offer_record)
    garage_result = assess_offer_parameter_wrapper('flats', 'garage', offer_record)
    garden = assess_offer_parameter_wrapper('flats', 'garden', offer_record)
    monitoring_result = assess_offer_parameter_wrapper('flats', 'monitoring', offer_record)
    outbuilding_result = assess_offer_parameter_wrapper('flats', 'outbuilding', offer_record)
    rent_result = assess_offer_parameter_wrapper('flats', 'rent', offer_record)

    if 'modernizationAns' not in offer_record:
        modernization_result = assess_offer_parameter_wrapper('flats', 'modernization', offer_record)
    else:
        modernization_result = {"modernizationGPT": offer_record['modernizationAns'],
                                "modernization_summary": RATED_BY_USR_STR}

    if 'technologyAns' not in offer_record:
        technology_result = assess_offer_parameter_wrapper('flats', 'technology', offer_record)
    else:
        technology_result = {"technologyGPT": offer_record['technologyAns'],
                             "technology_summary": RATED_BY_USR_STR}

    if 'kitchenAns' not in offer_record:
        kitchen_result = assess_offer_parameter_wrapper('flats', 'kitchen', offer_record)
    else:
        kitchen_result = {"kitchensGPT": offer_record['kitchenAns'],
                          "kitchen_summary": RATED_BY_USR_STR}

    result.update({'id': offer_record['id'],
                   'status': 1,
                   'qualityGPT': offer_record['qualityAns'] if 'qualityAns' in offer_record else -9})

    params_result = [balcony_result, law_status_result, modernization_result, garage_result, garden, monitoring_result,
                     technology_result, kitchen_result, rent_result]

    for param_result in params_result:
        result.update(param_result)

    # Translate results to pl
    with suppress(requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
        result_pl = translate_result_to_pl(result, 'pl', 'id', 'technologyGPT', 'lawStatusGPT',
                                           'elevatorGPT', 'balconyGPT', 'basementGPT', 'garageGPT', 'gardenGPT',
                                           'modernizationGPT', 'monitoringGPT', 'kitchenGPT', 'outbuildingGPT',
                                           'qualityGPT', 'status', 'rentGPT')
        print(result_pl)
    api_handler.send_offer_to_api(result_pl, jwt_data['access_token'], 'flats', endpoint='gpt',
                                  check_if_exists=False)


start_gpt_assessment(0, None, False)
