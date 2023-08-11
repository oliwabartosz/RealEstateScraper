from operator import itemgetter

# Config data
from src.config import config_data

# Offers from database
from src.gpt.data.flats_offers import offer_record, offer_description_en, offer_parameters_en, offer_params, offers_data

# Langchain essentials
from langchain.llms import OpenAI
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI

# Langchain chains
from src.gpt.chain.chaning import year_of_constr_chain, material_chain, building_type_chain, \
    number_floors_chain, technology_summary_chain, technology_rating_chain, balcony_summary_chain, balcony_rating_chain, \
    law_status_summary_chain, law_status_rating_chain, elevator_summary_chain, elevator_rating_chain, \
    basement_summary_chain, basement_rating_chain, garage_summary_chain, garage_rating_chain, garden_summary_chain, \
    garden_rating_chain, monitoring_summary_chain, monitoring_rating_chain, rent_summary_chain, rent_rating_chain, \
    outbuilding_summary_chain, outbuilding_rating_chain, kitchen_summary_chain, kitchen_rating_chain, \
    modernization_summary_chain, modernization_rating_chain

# Utils
from src.utils.utils import translate_result_to_pl

# Load model
config_data = config_data.get_config_data()
OPENAI_API_KEY = itemgetter('OPENAI_API_KEY')(config_data)

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.0)

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

# TEST ONLY
offer_record = offers_data[0]

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

elevator_param = int(offer_params.get('floorsNumber', 0)) > 5 and offer_params.get('elevator') == 'Tak'
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
