from typing import Callable

from langchain.chains import SequentialChain

from src.gpt.chain.chaning import balcony_summary_chain, balcony_rating_chain, law_status_summary_chain, \
    law_status_rating_chain, elevator_summary_chain, elevator_rating_chain, monitoring_summary_chain, \
    monitoring_rating_chain, basement_summary_chain, basement_rating_chain, garage_summary_chain, garage_rating_chain, \
    garden_summary_chain, garden_rating_chain, rent_summary_chain, rent_rating_chain, kitchen_rating_chain, \
    kitchen_summary_chain, modernization_summary_chain, modernization_rating_chain, year_of_constr_chain, \
    material_chain, building_type_chain, technology_summary_chain, technology_rating_chain, number_floors_chain
import translators as ts

from src.gpt.src.params_handler import handle_law_status_param, handle_elevator_param, handle_kitchen_param, \
    handle_balcony_param, handle_monitoring_param, handle_basement_param, handle_garage_param, handle_garden_param, \
    handle_outbuilding_param, handle_rent_param
from src.spacy.spacy import create_lemmatized_parameter_description

TAKEN_FROM_PARAMS_STR = 'Information taken from parameters'
RATED_STR = 'Rated by user'


def handle_result(chain_result_rating_val: str, chain_result_summary_val: str, param: int) -> tuple[int, str]:
    if chain_result_rating_val == -9:
        if param == -9:
            return int(chain_result_rating_val), chain_result_summary_val
        else:
            return param, TAKEN_FROM_PARAMS_STR

    return int(chain_result_rating_val), chain_result_summary_val


# @TODO: rethink and delete eventually: handle_result_kwargs
def handle_result_kwargs(**kwargs) -> tuple[int, str]:
    rated_val = kwargs.get('rated_value', False)

    if not rated_val:

        # Check if the required keyword arguments are present
        required_args = ['rating', 'summary', 'param']
        for arg in required_args:
            if arg not in kwargs:
                raise ValueError(f"Missing required argument: {arg}")

            if kwargs['rating'] == -9:
                if kwargs['param'] == -9:
                    return int(kwargs['rating']), kwargs['summary']
                else:
                    return kwargs['param'], TAKEN_FROM_PARAMS_STR

            return int(kwargs['rating']), kwargs['summary']
        else:
            return int(rated_val), RATED_STR


def _retrieve_chain_and_output_vars(offer_parameter: str) -> tuple[list, list[str]]:
    match offer_parameter:
        case 'lawStatus':
            chain = [law_status_summary_chain, law_status_rating_chain]
            output_vars = ["lawStatus_summary", "lawStatus_rating", ]
        case 'elevator':
            chain = [elevator_summary_chain, elevator_rating_chain]
            output_vars = ["elevator_summary", "elevator_rating", ]
        case 'balcony':
            chain = [balcony_summary_chain, balcony_rating_chain]
            output_vars = ["balcony_summary", "balcony_rating"]
        case 'monitoring':
            chain = [monitoring_summary_chain, monitoring_rating_chain]
            output_vars = ["monitoring_summary", "monitoring_rating"]
        case 'basement':
            chain = [basement_summary_chain, basement_rating_chain]
            output_vars = ["basement_summary", "basement_rating"]
        case 'balcony':
            chain = [balcony_summary_chain, balcony_rating_chain]
            output_vars = ["balcony_summary", "balcony_rating"]
        case 'garage':
            chain = [garage_summary_chain, garage_rating_chain]
            output_vars = ["garage_summary", "garage_rating"]
        case 'garden':
            chain = [garden_summary_chain, garden_rating_chain]
            output_vars = ["garden_summary", "garden_rating"]
        case 'outbuilding':
            chain = [balcony_summary_chain, balcony_rating_chain]
            output_vars = ["outbuilding_summary", "outbuilding_rating"]
        case 'rent':
            chain = [rent_summary_chain, rent_rating_chain]
            output_vars = ["rent_summary", "rent_rating"]
        case 'kitchen':
            chain = [kitchen_summary_chain, kitchen_rating_chain]
            output_vars = ["kitchen_summary", "kitchen_rating"]
        case 'modernization':
            chain = [year_of_constr_chain, material_chain, building_type_chain, number_floors_chain,
                     technology_summary_chain, technology_rating_chain, modernization_summary_chain,
                     modernization_rating_chain]
            output_vars = ["modernization_summary", "modernization_rating"]
        case 'technology':
            chain = [year_of_constr_chain, material_chain, building_type_chain, number_floors_chain,
                     technology_summary_chain, technology_rating_chain]
            output_vars = ["technology_summary", "technology_rating"]
        case _:
            raise ValueError(f'{offer_parameter} - the name of that parameter is wrong.')

    return chain, output_vars


def _choose_params_handler(offer_parameter: str, offer_params: dict):
    match offer_parameter:
        case 'lawStatus':
            return handle_law_status_param(offer_params)
        case 'elevator':
            return handle_elevator_param(offer_params)
        case 'kitchen':
            return handle_kitchen_param(offer_params)
        case 'balcony':
            return handle_balcony_param(offer_params)
        case 'monitoring':
            return handle_monitoring_param(offer_params)
        case 'basement':
            return handle_basement_param(offer_params)
        case 'garage':
            return handle_garage_param(offer_params)
        case 'garden':
            return handle_garden_param(offer_params)
        case 'outbuilding':
            return handle_outbuilding_param(offer_params)
        case 'rent':
            return handle_rent_param(offer_params)


def assess_offer_parameter(offer_parameter: str, offer_data: dict, offer_description: str) -> dict[str]:
    print(offer_description)
    chain = _retrieve_chain_and_output_vars(offer_parameter)[0]
    output_vars = _retrieve_chain_and_output_vars(offer_parameter)[1]

    # Filter out unnecessary keys for params
    offer_params = {key: value for key, value in offer_data.items() if key not in ['id', 'number', 'description']}
    if not offer_description:
        if offer_parameter in ['modernization', 'technology']:
            result = {f'{offer_parameter}GPT': -9,
                      f'{offer_parameter}_summary': f'Couldn\'t find information about {offer_parameter} in text.'}
            return result
        else:
            parameter_result = _choose_params_handler(offer_parameter, offer_params)
            result = {f'{offer_parameter}GPT': parameter_result,
                      f'{offer_parameter}_summary': f'There were no information about {offer_parameter} in the text. ' +
                                                    'Tried to get information from the offers parameters.'}
            return result

    # Translate text
    offer_parameters_en = ts.translate_text(str(offer_params), translator='bing', to_language='en')
    offer_description_en = ts.translate_text(offer_description, translator='bing', to_language='en')

    llm_chain = SequentialChain(
        chains=chain,
        input_variables=['real_estate_offer_en', 'offer_parameters_en'],
        output_variables=output_vars,
        verbose=True,
    )

    llm_chain_result = llm_chain({'real_estate_offer_en': offer_description_en,
                                  "offer_parameters_en": offer_parameters_en})

    parameter_result = _choose_params_handler(offer_parameter, offer_params)

    result = {
        f'{offer_parameter}GPT': handle_result(llm_chain_result[f'{offer_parameter}_rating'],
                                               llm_chain_result[f'{offer_parameter}_summary'],
                                               parameter_result)[0],
        f'{offer_parameter}_summary': handle_result(llm_chain_result[f'{offer_parameter}_rating'],
                                                    llm_chain_result[f'{offer_parameter}_summary'],
                                                    parameter_result)[1]
    }

    return result


def assess_offer_parameter_wrapper(offer_type: str, offer_parameter: str, offers_data: dict) -> dict[str]:
    #@TODO: add technology to spacy.json
    lemmatized_description = create_lemmatized_parameter_description(offer_type,
                                                                     offers_data['description'],
                                                                     offer_parameter)
    return assess_offer_parameter(offer_parameter,
                                  offers_data,
                                  lemmatized_description)
