from src.config import config_data
from operator import itemgetter

# Templates
from src.gpt.templates import gpt_params, gpt_summaries, gpt_ratings

# Handlers
from src.handlers import api_handler

# Langchain imports
from langchain.llms import OpenAI
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI
from src.gpt.chain.chaning import create_llm_chain

# Translator
import translators as ts

# Utils
from src.utils.utils import merge_dictionaries_by_id, translate_result_to_pl

# Get JWT AUTH TOKEN
jwt_data: dict = api_handler.get_jwt_token(f'{api_handler.rer_url}/rer/auth')

# Get all data from database based on number column
offers_data = api_handler.get_offers_data_from_api(
    jwt_data['access_token'],
    '/rer/api/flats/',
    'GET',
    'id', 'number', 'lawStatus', 'floorsNumber', 'rent', 'material', 'buildingType', 'yearBuilt', 'buildingQuality',
    'balcony', 'balconyQuantity', 'terracesQuantity', 'loggiasQuantity', 'frenchBalconyQuantity', 'kitchenType',
    'basement', 'storageRoom', 'attic', 'parkingPlace', 'priceParkingUnderground', 'priceParkingGround', 'garden',
    'elevator', 'security', 'monitoring', 'guardedArea', 'guardedEstate', 'securityControl', 'description'
)

offers_gpt_data = api_handler.get_offers_data_from_api(
    jwt_data['access_token'],
    '/rer/api/flats/gpt',
    'GET',
    'id', 'technologyGPT', 'modernizationGPT', 'kitchenGPT', 'qualityGPT'
)

# Update data with information from another table get from the database
offers_data = merge_dictionaries_by_id(offers_data, offers_gpt_data)
# TEST ONLY
offer_record = offers_data[0]

# Filter out unnecessary keys for params
offer_params = {key: value for key, value in offer_record.items() if key not in ['id', 'number', 'description']}
offer_description = offer_record['description']

# Translate text
offer_parameters_en = ts.translate_text(str(offer_params), translator='google', to_language='en')
offer_description_en = ts.translate_text(offer_description, translator='google', to_language='en')

# Load model
config_data = config_data.get_config_data()
OPENAI_API_KEY = itemgetter('OPENAI_API_KEY')(config_data)

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.0)

# Chaining...

# PARAMETERS
# Year of the construction of the building
year_of_constr_chain = create_llm_chain(llm, gpt_params.year_of_constr_prompt, "year_of_constr")
# Building type
building_type_chain = create_llm_chain(llm, gpt_params.building_type_prompt, "building_type")
# Material of the building that have been constructed
material_chain = create_llm_chain(llm, gpt_params.material_prompt, "material")
# Number of floors that building have
number_floors_chain = create_llm_chain(llm, gpt_params.number_floors_prompt, "number_of_floors")

# SUMMARIES
# Technology
technology_summary_chain = create_llm_chain(llm, gpt_summaries.technology_prompt, "technology_summary")
# Law status
law_status_summary_chain = create_llm_chain(llm, gpt_summaries.law_status_prompt, "law_summary")
# Balcony
balcony_summary_chain = create_llm_chain(llm, gpt_summaries.balcony_prompt, "balcony_summary")
# Elevator
elevator_summary_chain = create_llm_chain(llm, gpt_summaries.elevator_prompt, "elevator_summary")
# Basement
basement_summary_chain = create_llm_chain(llm, gpt_summaries.basement_prompt, "basement_summary")
# Garage
garage_summary_chain = create_llm_chain(llm, gpt_summaries.garage_prompt, "garage_summary")
# Garden
garden_summary_chain = create_llm_chain(llm, gpt_summaries.garden_prompt, "garden_summary")
# Monitoring
monitoring_summary_chain = create_llm_chain(llm, gpt_summaries.monitoring_prompt, "monitoring_summary")
# Kitchen
kitchen_summary_chain = create_llm_chain(llm, gpt_summaries.kitchen_prompt, "kitchen_summary")
# Rent
rent_summary_chain = create_llm_chain(llm, gpt_summaries.rent_prompt, "rent_summary")
# Outbuilding
outbuilding_summary_chain = create_llm_chain(llm, gpt_summaries.outbuilding_prompt, "outbuilding_summary")
# Modernization
modernization_summary_chain = create_llm_chain(llm, gpt_summaries.modernization_prompt, "modernization_summary")

# RATINGS
# Technology
technology_rating_chain = create_llm_chain(llm, gpt_ratings.technology_prompt, "technology_rating")
# Law status
law_status_rating_chain = create_llm_chain(llm, gpt_ratings.law_status_prompt, "law_rating")
# Balcony
balcony_rating_chain = create_llm_chain(llm, gpt_ratings.balcony_prompt, "balcony_rating")
# Elevator
elevator_rating_chain = create_llm_chain(llm, gpt_ratings.elevator_prompt, "elevator_rating")
# Basement
basement_rating_chain = create_llm_chain(llm, gpt_ratings.basement_prompt, "basement_rating")
# Garage
garage_rating_chain = create_llm_chain(llm, gpt_ratings.garage_prompt, "garage_rating")
# Garden
garden_rating_chain = create_llm_chain(llm, gpt_ratings.garden_prompt, "garden_rating")
# Monitoring
monitoring_rating_chain = create_llm_chain(llm, gpt_ratings.monitoring_prompt, "monitoring_rating")
# Kitchen
kitchen_rating_chain = create_llm_chain(llm, gpt_ratings.kitchen_prompt, "kitchen_rating")
# Rent
rent_rating_chain = create_llm_chain(llm, gpt_ratings.rent_prompt, "rent_rating")
# Outbuilding
outbuilding_rating_chain = create_llm_chain(llm, gpt_ratings.outbuilding_prompt, "outbuilding_rating")
# Modernization
modernization_rating_chain = create_llm_chain(llm, gpt_ratings.modernization_prompt, "modernization_rating")

chain = [
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

output_variables = [
    "technology_summary", "technology_rating",
    "balcony_summary", "balcony_rating",
    "law_summary", "law_rating",
    "elevator_summary", "elevator_rating",
    "basement_summary", "basement_rating",
    "garage_summary", "garage_rating",
    "garden_summary", "garden_rating",
    "monitoring_summary", "monitoring_rating",
    "rent_summary", "rent_rating",
    "outbuilding_summary", "outbuilding_rating",
]

if 'kitchenGPT' not in offer_record:
    chain.extend([kitchen_summary_chain, kitchen_rating_chain])
    output_variables.extend(["kitchen_summary", "kitchen_rating"])

if 'modernizationGPT' not in offer_record:
    chain.extend([modernization_summary_chain, modernization_rating_chain])
    output_variables.extend(["modernization_summary", "modernization_rating"])

overall_chain = SequentialChain(
    chains=chain,
    input_variables=['real_estate_offer_en', 'offer_parameters_en'],
    output_variables=output_variables,
    verbose=True,
)

overall_chain_result = overall_chain({'real_estate_offer_en': offer_description_en,
                                      "offer_parameters_en": offer_parameters_en})

elevator_param = int(offer_params.get('floorsNumber', 0)) > 5
elevator_param = offer_params.get('elevator') == 'Tak'
rent_param = offer_params.get('rent', '')

result = {
    'id': offer_record['id'],
    'technologyGPT': offer_record['technologyGPT'] if 'technologyGPT' in offer_record else
    overall_chain_result['technology_rating'],

    'technology_summary': overall_chain_result['technology_summary'],
    'lawStatusGPT': overall_chain_result['law_rating'],
    'law_summary': overall_chain_result['law_summary'],
    'balconyGPT': overall_chain_result['balcony_rating'],
    'balcony_summary': overall_chain_result['balcony_summary'],
    'elevatorGPT': int(elevator_param) if overall_chain_result['elevator_rating'] == -9 else overall_chain_result[
        'elevator_rating'],

    'elevator_summary': overall_chain_result['elevator_summary'],
    'basementGPT': overall_chain_result['basement_rating'],
    'basement_summary': overall_chain_result['basement_summary'],
    'garageGPT': overall_chain_result['garage_rating'],
    'garage_summary': overall_chain_result['garage_summary'],
    'gardenGPT': overall_chain_result['garden_rating'],
    'garden_summary': overall_chain_result['garden_summary'],

    'modernizationGPT': offer_record['modernizationGPT'] if 'modernizationGPT' in offer_record else
    overall_chain_result['modernization_rating'],

    'modernization_summary': 'Rated by user.' if 'modernizationGPT' in offer_record else
    overall_chain_result['modernization_summary'],

    'alarmGPT': overall_chain_result['monitoring_rating'],
    'alarm_summary': overall_chain_result['monitoring_summary'],

    'kitchenGPT': offer_record['kitchenGPT'] if 'kitchenGPT' in offer_record else
    overall_chain_result['kitchen_rating'],

    'kitchen_summary': 'Rated by user.' if 'kitchenGPT' in offer_record else
    overall_chain_result['kitchen_summary'],

    'outbuildingGPT': overall_chain_result['outbuilding_rating'],
    'outbuilding_summary': overall_chain_result['outbuilding_summary'],
    'qualityGPT': offer_record['qualityGPT'] if 'qualityGPT' in offer_record else '',
    'status': 1,

    'rentGPT': rent_param if overall_chain_result['rent_rating'] == -9 else overall_chain_result['rent_rating'],
    'rent_summary': 'Information taken from parameters description.' if rent_param != '' and overall_chain_result
    ['rent_rating'] == -9 else overall_chain_result['rent_summary'],
}

# Translate results to pl
result_en = translate_result_to_pl(result, 'pl', 'id', 'technologyGPT', 'lawStatusGPT',
                                   'elevatorGPT', 'balconyGPT', 'basementGPT', 'garageGPT', 'gardenGPT',
                                   'modernizationGPT', 'alarmGPT', 'kitchenGPT', 'outbuildingGPT', 'qualityGPT',
                                   'status', 'rentGPT')
print(result_en)

# # @TODO:
# # 3. Wysłać do bazy danych
# # 4. Zloopować wszystko
#
# # KITCHEN CHAIN CHECK!!!
