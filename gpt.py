# Translator
import translators as ts
import requests

# Langchain chains
from langchain.chains import SequentialChain
from src.gpt.chain.chaning import year_of_constr_chain, material_chain, building_type_chain, \
    number_floors_chain, balcony_summary_chain, balcony_rating_chain, \
    law_status_summary_chain, law_status_rating_chain, elevator_summary_chain, elevator_rating_chain, \
    basement_summary_chain, basement_rating_chain, garage_summary_chain, garage_rating_chain, garden_summary_chain, \
    garden_rating_chain, monitoring_summary_chain, monitoring_rating_chain, rent_summary_chain, rent_rating_chain, \
    outbuilding_summary_chain, outbuilding_rating_chain, kitchen_summary_chain, kitchen_rating_chain, \
    modernization_summary_chain, modernization_rating_chain, technology_summary_chain, technology_rating_chain
from src.gpt.data.params_handler import handle_law_status_param, handle_rent_param, handle_elevator_param, \
    handle_kitchen_param
from src.gpt.data.result_handler import handle_result, TAKEN_FROM_PARAMS_STR, RATED_STR

# Handlers
from src.handlers import api_handler
from src.handlers.api_handler import get_offers_data_from_api

# Utils
from src.utils.utils import translate_result_to_pl

# Data
from src.gpt.data.get_or_send_GPT_data_to_database import offers_data, jwt_data, offers_gpt_data

main_chain = [
    year_of_constr_chain, material_chain, building_type_chain, number_floors_chain,
    technology_summary_chain, technology_rating_chain,
    balcony_summary_chain, balcony_rating_chain,
    law_status_summary_chain, law_status_rating_chain,
    elevator_summary_chain, elevator_rating_chain,
    basement_summary_chain, basement_rating_chain,
    garage_summary_chain, garage_rating_chain,
    garden_summary_chain, garden_rating_chain,
    monitoring_summary_chain, monitoring_rating_chain,
    rent_summary_chain, rent_rating_chain,
    outbuilding_summary_chain, outbuilding_rating_chain,
]

main_output_variables = [
    "balcony_summary", "balcony_rating",
    "technology_summary", "technology_rating",
    "law_summary", "law_rating",
    "elevator_summary", "elevator_rating",
    "basement_summary", "basement_rating",
    "garage_summary", "garage_rating",
    "garden_summary", "garden_rating",
    "monitoring_summary", "monitoring_rating",
    "rent_summary", "rent_rating",
    "outbuilding_summary", "outbuilding_rating",
]

list_of_id_in_gpt_database = [item['id'] for item in offers_gpt_data]

for offer_record in offers_data[6:7]:
    if offer_record not in list_of_id_in_gpt_database:

        print(offer_record)
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
        offer_parameters_en = ts.translate_text(str(offer_params), translator='baidu', to_language='en')
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
        rent_param = handle_rent_param(offer_params)
        elevator_param = handle_elevator_param(offer_params)
        kitchen_param = handle_kitchen_param(offer_params)

        # Create the result
        result = {
            'id': offer_record['id'],

            'lawStatusGPT': handle_result(overall_chain_result['law_rating'],
                                          overall_chain_result['law_summary'],
                                          law_param)[0],
            'law_summary': handle_result(overall_chain_result['law_rating'],
                                         overall_chain_result['law_summary'],
                                         law_param)[1],

            'balconyGPT': overall_chain_result['balcony_rating'],
            'balcony_summary': overall_chain_result['balcony_summary'],

            'elevatorGPT': handle_result(overall_chain_result['elevator_rating'],
                                         overall_chain_result['elevator_summary'],
                                         elevator_param)[0],

            'elevator_summary': handle_result(overall_chain_result['elevator_rating'],
                                              overall_chain_result['elevator_summary'],
                                              elevator_param)[1],

            'basementGPT': overall_chain_result['basement_rating'],
            'basement_summary': overall_chain_result['basement_summary'],

            'garageGPT': overall_chain_result['garage_rating'],
            'garage_summary': overall_chain_result['garage_summary'],

            'gardenGPT': overall_chain_result['garden_rating'],
            'garden_summary': overall_chain_result['garden_summary'],

            'modernizationGPT': offer_record['modernizationAns'] if 'modernizationAns' in offer_record else
            overall_chain_result['modernization_rating'],

            'modernization_summary': 'Rated by user.' if 'modernizationAns' in offer_record else
            overall_chain_result['modernization_summary'],

            'technologyGPT': offer_record['technologyAns'] if 'technologyAns' in offer_record else
            overall_chain_result['technology_rating'],
            'technology_summary': 'Rated by user.' if 'technologyAns' in offer_record else
            overall_chain_result['technology_summary'],

            'alarmGPT': overall_chain_result['monitoring_rating'],
            'alarm_summary': overall_chain_result['monitoring_summary'],

            'kitchenGPT': offer_record['kitchenAns'] if 'kitchenAns' in offer_record
            else handle_result(overall_chain_result['kitchen_rating'],
                               overall_chain_result['kitchen_summary'],
                               kitchen_param)[0],

            'kitchen_summary': RATED_STR if 'kitchenAns' in offer_record
            else handle_result(overall_chain_result['kitchen_rating'],
                               overall_chain_result['kitchen_summary'],
                               kitchen_param)[1],

            'outbuildingGPT': overall_chain_result['outbuilding_rating'],
            'outbuilding_summary': overall_chain_result['outbuilding_summary'],
            'qualityGPT': offer_record['qualityAns'] if 'qualityAns' in offer_record else -9,
            'status': 1,

            'rentGPT': rent_param if int(float(overall_chain_result['rent_rating'])) == -9 else overall_chain_result[
                'rent_rating'],

            'rent_summary': TAKEN_FROM_PARAMS_STR if rent_param != -9 and int(
                float(overall_chain_result['rent_rating'])) == -9 else
            overall_chain_result['rent_summary'],
        }

        # Translate results to pl
        try:
            result_pl = translate_result_to_pl(result, 'pl', 'id', 'technologyGPT', 'lawStatusGPT',
                                               'elevatorGPT', 'balconyGPT', 'basementGPT', 'garageGPT', 'gardenGPT',
                                               'modernizationGPT', 'alarmGPT', 'kitchenGPT', 'outbuildingGPT',
                                               'qualityGPT',
                                               'status', 'rentGPT')
        except requests.exceptions.HTTPError as http_error:
            result_pl = translate_result_to_pl(result, 'pl', 'id', 'technologyGPT', 'lawStatusGPT',
                                               'elevatorGPT', 'balconyGPT', 'basementGPT', 'garageGPT', 'gardenGPT',
                                               'modernizationGPT', 'alarmGPT', 'kitchenGPT', 'outbuildingGPT',
                                               'status', 'rentGPT')
        except requests.exceptions.ConnectionError as connection_error:
            result_pl = translate_result_to_pl(result, 'pl', 'id', 'technologyGPT', 'lawStatusGPT',
                                               'elevatorGPT', 'balconyGPT', 'basementGPT', 'garageGPT', 'gardenGPT',
                                               'modernizationGPT', 'alarmGPT', 'kitchenGPT', 'outbuildingGPT',
                                               'qualityGPT', 'status', 'rentGPT')

        print(result_pl)

        api_handler.send_offer_to_api(result_pl, jwt_data['access_token'], 'flats', endpoint='gpt',
                                      check_if_exists=False)
