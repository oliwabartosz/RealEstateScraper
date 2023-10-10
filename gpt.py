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
list_of_id_in_gpt_database = [item['id'] for item in offers_gpt_data]

result = {}

for offer_record in offers_data:

    if offer_record not in list_of_id_in_gpt_database:
        if offer_record["description"] == ' ':
            offer_record["description"] = 'Brak opisu'

        # Assess parameters
        balcony_result = assess_offer_parameter_wrapper('flats', 'balcony', offer_record)
        lawStatus_result = assess_offer_parameter_wrapper('flats', 'lawStatus', offer_record)
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
            kitchenAns = {"kitchensGPT": offer_record['kitchenAns'],
                          "kitchen_summary": RATED_BY_USR_STR}

        result.update({'id': offer_record['id'],
                       'status': 1,
                       'qualityGPT': offer_record['qualityAns'] if 'qualityAns' in offer_record else -9})

        result.update(balcony_result)
        result.update(lawStatus_result)
        result.update(modernization_result)
        result.update(garage_result)
        result.update(garden)
        result.update(monitoring_result)
        result.update(outbuilding_result)
        result.update(technology_result)
        result.update(rent_result)

        # Translate results to pl
        with suppress(requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            result_pl = translate_result_to_pl(result, 'pl', 'id', 'technologyGPT', 'lawStatusGPT',
                                               'elevatorGPT', 'balconyGPT', 'basementGPT', 'garageGPT', 'gardenGPT',
                                               'modernizationGPT', 'monitoringGPT', 'kitchenGPT', 'outbuildingGPT',
                                               'qualityGPT', 'status', 'rentGPT')
        print(result_pl)
        api_handler.send_offer_to_api(result_pl, jwt_data['access_token'], 'flats', endpoint='gpt',
                                      check_if_exists=False)
