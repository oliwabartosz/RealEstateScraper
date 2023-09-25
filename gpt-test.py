import json

# Translator
import translators as ts
import requests
from contextlib import suppress

# Langchain chains
from langchain.chains import SequentialChain
from src.gpt.chain.chaning import year_of_constr_chain, material_chain, building_type_chain, \
    number_floors_chain, balcony_summary_chain, balcony_rating_chain, \
    law_status_summary_chain, law_status_rating_chain, elevator_summary_chain, elevator_rating_chain, \
    basement_summary_chain, basement_rating_chain, garage_summary_chain, garage_rating_chain, garden_summary_chain, \
    garden_rating_chain, monitoring_summary_chain, monitoring_rating_chain, rent_summary_chain, rent_rating_chain, \
    outbuilding_summary_chain, outbuilding_rating_chain, kitchen_summary_chain, kitchen_rating_chain, \
    modernization_summary_chain, modernization_rating_chain, technology_summary_chain, technology_rating_chain

# Handlers
from src.handlers import api_handler
from src.gpt.data.utils.params_handler import handle_law_status_param, handle_rent_param, handle_elevator_param, \
    handle_kitchen_param, handle_balcony_param, handle_monitoring_param, handle_basement_param, handle_garage_param, \
    handle_garden_param, handle_outbuilding_param
from src.gpt.data.utils.result_handler import handle_result, TAKEN_FROM_PARAMS_STR, RATED_STR

# Utils
from src.utils.utils import translate_result_to_pl

# Load data
with open('./src/gpt/data/test-data/test-balcony.json', mode='r', encoding='utf-8') as file:
    balcony_data = json.load(file)

