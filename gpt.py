# Translator
from contextlib import suppress

import requests
import translators as ts

# Langchain chains
from langchain.chains import SequentialChain
from src.gpt.chain.chaning import kitchen_summary_chain, kitchen_rating_chain, \
    modernization_summary_chain, modernization_rating_chain

# Data
from src.gpt.src.get_or_send_GPT_data_to_database import offers_data, jwt_data, offers_gpt_data
from src.gpt.src.params_handler import handle_law_status_param, handle_rent_param, handle_elevator_param, \
    handle_kitchen_param, handle_balcony_param, handle_monitoring_param, handle_basement_param, handle_garage_param, \
    handle_garden_param, handle_outbuilding_param
from src.gpt.src.result_handler import handle_result, TAKEN_FROM_PARAMS_STR, RATED_STR, assess_offer_parameter_wrapper
from src.gpt.src.langchain import main_chain, main_output_variables
from src.gpt.src.result_handler import assess_offer_parameter

# Handlers
from src.handlers import api_handler
from src.spacy.spacy import create_lemmatized_parameter_description

# Utils
from src.utils.utils import translate_result_to_pl

# Helps to skip reassessment if rated before and restart was needed
list_of_id_in_gpt_database = [item['id'] for item in offers_gpt_data]

result = {}

for offer_record in offers_data[10:11]:
    print(offers_data[10:11])

    if offer_record not in list_of_id_in_gpt_database:
        if offer_record["description"] == ' ':
            offer_record["description"] = 'Brak opisu'

        # Assess parameters
        balcony_result = assess_offer_parameter_wrapper('flats', 'balcony', offer_record)
        lawStatus_result = assess_offer_parameter_wrapper('flats', 'lawStatus', offer_record)
        modernization_result = assess_offer_parameter_wrapper('flats', 'modernization', offer_record)
        technology_result = assess_offer_parameter_wrapper('flats', 'technology', offer_record)

        result.update({'id': offer_record['id'],
                       'status': 1})
        result.update(balcony_result)
        result.update(lawStatus_result)
        result.update(modernization_result)
        result.update(technology_result)

        # Translate results to pl
        with suppress(requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            result_pl = translate_result_to_pl(result, 'pl', 'id', 'technologyGPT', 'lawStatusGPT',
                                               'elevatorGPT', 'balconyGPT', 'basementGPT', 'garageGPT', 'gardenGPT',
                                               'modernizationGPT', 'alarmGPT', 'kitchenGPT', 'outbuildingGPT',
                                               'qualityGPT', 'status', 'rentGPT')
        print(result_pl)
        api_handler.send_offer_to_api(result_pl, jwt_data['access_token'], 'flats', endpoint='gpt',
                                      check_if_exists=False)
        exit(1)

        # @TODO: handle kitchenAns, modernizationAns, technologyAns, qualityAns,

for offer_record in offers_data:
    if offer_record not in list_of_id_in_gpt_database:
        if offer_record["description"] == ' ':
            offer_record["description"] = 'Brak opisu'

        chain = main_chain.copy()
        output_variables = main_output_variables.copy()

        if 'kitchenAns' not in offer_record:
            chain.extend([kitchen_summary_chain, kitchen_rating_chain])
            output_variables.extend(["kitchen_summary", "kitchen_rating"])

        if 'modernizationAns' not in offer_record:
            chain.extend([modernization_summary_chain, modernization_rating_chain])
            output_variables.extend(["modernization_summary", "modernization_rating"])

        # Filter out unnecessary keys for params
        offer_params = {key: value for key, value in offer_record.items() if key not in ['id', 'number', 'description']}
        offer_description = offer_record['description']

        # Translate text
        offer_parameters_en = ts.translate_text(str(offer_params), translator='bing', to_language='en')
        offer_description_en = ts.translate_text(offer_description, translator='baidu', to_language='en')

        overall_chain = SequentialChain(
            chains=chain,
            input_variables=['real_estate_offer_en', 'offer_parameters_en'],
            output_variables=output_variables,
            verbose=True,
        )

        overall_chain_result = overall_chain({'real_estate_offer_en': offer_description_en,
                                              "offer_parameters_en": offer_parameters_en})

        # These parameters handlers help to manage data gathered by GPT. When GPT doesn't find the answer and therefore
        # returns -9, the final result gets the information from parameters below that are handled in 'hard-coded' way.
        law_param = handle_law_status_param(offer_params)
        elevator_param = handle_elevator_param(offer_params)
        kitchen_param = handle_kitchen_param(offer_params)
        balcony_param = handle_balcony_param(offer_params)
        monitoring_param = handle_monitoring_param(offer_params)
        basement_param = handle_basement_param(offer_params)
        garage_param = handle_garage_param(offer_params)
        garden_param = handle_garden_param(offer_params)
        outbuilding_param = handle_outbuilding_param(offer_params)
        rent_param = handle_rent_param(offer_params)

        # Create the result
        result = {
            'id': offer_record['id'],

            'lawStatusGPT': handle_result(overall_chain_result['law_rating'],
                                          overall_chain_result['law_summary'],
                                          law_param)[0],
            'law_summary': handle_result(overall_chain_result['law_rating'],
                                         overall_chain_result['law_summary'],
                                         law_param)[1],

            'balconyGPT': handle_result(overall_chain_result['balcony_rating'],
                                        overall_chain_result['balcony_summary'],
                                        balcony_param)[0],

            'balcony_summary': handle_result(overall_chain_result['balcony_rating'],
                                             overall_chain_result['balcony_summary'],
                                             balcony_param)[1],

            'elevatorGPT': handle_result(overall_chain_result['elevator_rating'],
                                         overall_chain_result['elevator_summary'],
                                         elevator_param)[0],

            'elevator_summary': handle_result(overall_chain_result['elevator_rating'],
                                              overall_chain_result['elevator_summary'],
                                              elevator_param)[1],

            'alarmGPT': handle_result(overall_chain_result['monitoring_rating'],
                                      overall_chain_result['monitoring_summary'],
                                      monitoring_param)[0],
            'alarm_summary': handle_result(overall_chain_result['monitoring_rating'],
                                           overall_chain_result['monitoring_summary'],
                                           monitoring_param)[1],

            'basementGPT': handle_result(overall_chain_result['basement_rating'],
                                         overall_chain_result['basement_summary'],
                                         basement_param)[0],

            'basement_summary': handle_result(overall_chain_result['basement_rating'],
                                              overall_chain_result['basement_summary'],
                                              basement_param)[1],

            'garageGPT': handle_result(overall_chain_result['garage_rating'],
                                       overall_chain_result['garage_summary'],
                                       garage_param)[0],
            'garage_summary': handle_result(overall_chain_result['garage_rating'],
                                            overall_chain_result['garage_summary'],
                                            garage_param)[1],

            'gardenGPT': handle_result(overall_chain_result['garden_rating'],
                                       overall_chain_result['garden_summary'],
                                       garden_param)[0],
            'garden_summary': handle_result(overall_chain_result['garden_rating'],
                                            overall_chain_result['garden_summary'],
                                            garden_param)[1],

            'outbuildingGPT': 1 if outbuilding_param == 1 else handle_result(overall_chain_result['outbuilding_rating'],
                                                                             overall_chain_result['outbuilding_rating'],
                                                                             outbuilding_param)[0],
            'outbuilding_summary': TAKEN_FROM_PARAMS_STR if outbuilding_param == 1 else
            handle_result(overall_chain_result['outbuilding_rating'],
                          overall_chain_result['outbuilding_rating'],
                          outbuilding_param)[1],

            'rentGPT': handle_result(overall_chain_result['rent_rating'],
                                     overall_chain_result['rent_summary'],
                                     rent_param)[0],

            'rent_summary': handle_result(overall_chain_result['rent_rating'],
                                          overall_chain_result['rent_summary'],
                                          rent_param)[1],

            'kitchenGPT': offer_record['kitchenAns'] if 'kitchenAns' in offer_record
            else handle_result(overall_chain_result['kitchen_rating'],
                               overall_chain_result['kitchen_summary'],
                               kitchen_param)[0],

            'kitchen_summary': RATED_STR if 'kitchenAns' in offer_record
            else handle_result(overall_chain_result['kitchen_rating'],
                               overall_chain_result['kitchen_summary'],
                               kitchen_param)[1],

            'modernizationGPT': offer_record['modernizationAns'] if 'modernizationAns' in offer_record else
            overall_chain_result['modernization_rating'],

            'modernization_summary': 'Rated by user.' if 'modernizationAns' in offer_record else
            overall_chain_result['modernization_summary'],

            'technologyGPT': offer_record['technologyAns'] if 'technologyAns' in offer_record else
            overall_chain_result['technology_rating'],
            'technology_summary': 'Rated by user.' if 'technologyAns' in offer_record else
            overall_chain_result['technology_summary'],

            'qualityGPT': offer_record['qualityAns'] if 'qualityAns' in offer_record else -9,

            'status': 1,
        }

        print('result', '-' * 100, '\n', result)

        # Translate results to pl

        with suppress(requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            result_pl = translate_result_to_pl(result, 'pl', 'id', 'technologyGPT', 'lawStatusGPT',
                                               'elevatorGPT', 'balconyGPT', 'basementGPT', 'garageGPT', 'gardenGPT',
                                               'modernizationGPT', 'alarmGPT', 'kitchenGPT', 'outbuildingGPT',
                                               'qualityGPT', 'status', 'rentGPT')

        print(result_pl)

        api_handler.send_offer_to_api(result_pl, jwt_data['access_token'], 'flats', endpoint='gpt',
                                      check_if_exists=False)
