from src.config import config_data
from operator import itemgetter

# Templates
from src.gpt.templates import gpt_translation, gpt_params, gpt_summaries, gpt_ratings

# Handlers
from src.handlers import api_handler

# Langchain imports
from langchain.llms import OpenAI
from langchain.chains import SequentialChain

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

# Get JWT AUTH TOKEN
jwt_data: dict = api_handler.get_jwt_token(f'{api_handler.rer_url}/rer/auth')

# Get all data from database based on number column
offers_data = api_handler.get_offers_data_from_api(
    jwt_data['access_token'],
    columns_to_get=['number', 'lawStatus', 'floorsNumber', 'rent', 'material', 'buildingType', 'yearBuilt', 'buildingQuality', 'balcony',
                    'balconyQuantity', 'terracesQuantity', 'loggiasQuantity', 'frenchBalconyQuantity', 'kitchenType',
                    'basement', 'storageRoom', 'attic', 'parkingPlace', 'priceParkingUnderground', 'priceParkingGround',
                    'garden', 'elevator', 'security', 'monitoring', 'guardedArea', 'guardedEstate', 'securityControl',
                    'description']
)

offer_record = offers_data[0]

# Filter out unnecessary keys for params
offer_params = {key: value for key, value in offer_record.items() if key not in ['number', 'description']}
offer_description = offer_record['description']

# Load model
config_data = config_data.get_config_data()
OPENAI_API_KEY = itemgetter('OPENAI_API_KEY')(config_data)

llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, temperature=0.0, )

# Chaining...

# 1. TRANSLATION

# Translating description from PL to EN
translate_desc_prompt = ChatPromptTemplate.from_template(gpt_translation.translate_description_prompt)
translate_desc_chain = LLMChain(llm=llm, prompt=translate_desc_prompt, output_key="real_estate_offer_en")

# Translating parameters from PL to EN
translate_params_prompt = ChatPromptTemplate.from_template(gpt_translation.translate_params_prompt)
translate_params_chain = LLMChain(llm=llm, prompt=translate_params_prompt, output_key="offer_parameters_en")

# PARAMETERS

# Year of the construction of the building
year_of_constr_prompt = ChatPromptTemplate.from_template(gpt_params.year_of_constr_prompt)
year_of_constr_chain = LLMChain(llm=llm, prompt=year_of_constr_prompt, output_key="year_of_constr")

# Building type
building_type_prompt = ChatPromptTemplate.from_template(gpt_params.building_type_prompt)
building_type_chain = LLMChain(llm=llm, prompt=building_type_prompt, output_key="building_type")

# Material of the building that have been constructed
material_prompt = ChatPromptTemplate.from_template(gpt_params.material_prompt)
material_chain = LLMChain(llm=llm, prompt=material_prompt, output_key="material")

# Number of floors that building have
number_floors_prompt = ChatPromptTemplate.from_template(gpt_params.number_floors_prompt)
number_floors_chain = LLMChain(llm=llm, prompt=number_floors_prompt, output_key="number_of_floors")

# Elevator
elevator_prompt = ChatPromptTemplate.from_template(gpt_params.elevator_prompt)
elevator_chain = LLMChain(llm=llm, prompt=elevator_prompt, output_key="elevator")

# SUMMARIES

# Technology
technology_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.technology_prompt)
technology_summary_chain = LLMChain(llm=llm, prompt=technology_summary_prompt, output_key="technology_summary")

# Law status
law_status_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.law_status_prompt)
law_status_summary_chain = LLMChain(llm=llm, prompt=law_status_summary_prompt, output_key="law_summary")

# Balcony
balcony_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.balcony_prompt)
balcony_summary_chain = LLMChain(llm=llm, prompt=balcony_summary_prompt, output_key="balcony_summary")

# Elevator
elevator_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.elevator_prompt)
elevator_summary_chain = LLMChain(llm=llm, prompt=elevator_summary_prompt, output_key="elevator_summary")

# Basement
basement_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.basement_prompt)
basement_summary_chain = LLMChain(llm=llm, prompt=basement_summary_prompt, output_key="basement_summary")

# Garage
garage_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.garage_prompt)
garage_summary_chain = LLMChain(llm=llm, prompt=garage_summary_prompt, output_key="garage_summary")

# Garden
garden_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.garden_prompt)
garden_summary_chain = LLMChain(llm=llm, prompt=garden_summary_prompt, output_key="garden_summary")

# Monitoring
monitoring_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.monitoring_prompt)
monitoring_summary_chain = LLMChain(llm=llm, prompt=monitoring_summary_prompt, output_key="monitoring_summary")

# Kitchen
kitchen_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.kitchen_prompt)
kitchen_summary_chain = LLMChain(llm=llm, prompt=kitchen_summary_prompt, output_key="kitchen_summary")

# Rent
rent_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.rent_prompt)
rent_summary_chain = LLMChain(llm=llm, prompt=rent_summary_prompt, output_key="rent_summary")

# Outbuilding
outbuilding_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.outbuilding_prompt)
outbuilding_summary_chain = LLMChain(llm=llm, prompt=outbuilding_summary_prompt, output_key="outbuilding_summary")

# Modernization
modernization_summary_prompt = ChatPromptTemplate.from_template(gpt_summaries.modernization_prompt)
modernization_summary_chain = LLMChain(llm=llm, prompt=modernization_summary_prompt, output_key="modernization_summary")

# RATINGS

# Technology
technology_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.technology_prompt)
technology_rating_chain = LLMChain(llm=llm, prompt=technology_rating_prompt, output_key="technology_rating")

# Law status
law_status_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.law_status_prompt)
law_status_rating_chain = LLMChain(llm=llm, prompt=law_status_rating_prompt, output_key="law_rating")

# Balcony
balcony_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.balcony_prompt)
balcony_rating_chain = LLMChain(llm=llm, prompt=balcony_rating_prompt, output_key="balcony_rating")

# Elevator
elevator_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.elevator_prompt)
elevator_rating_chain = LLMChain(llm=llm, prompt=elevator_rating_prompt, output_key="elevator_rating")

# Basement
basement_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.basement_prompt)
basement_rating_chain = LLMChain(llm=llm, prompt=basement_rating_prompt, output_key="basement_rating")

# Garage
garage_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.garage_prompt)
garage_rating_chain = LLMChain(llm=llm, prompt=garage_rating_prompt, output_key="garage_rating")

# Garden
garden_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.garden_prompt)
garden_rating_chain = LLMChain(llm=llm, prompt=garden_rating_prompt, output_key="garden_rating")

# Monitoring
monitoring_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.monitoring_prompt)
monitoring_rating_chain = LLMChain(llm=llm, prompt=monitoring_rating_prompt, output_key="monitoring_rating")

# Kitchen
kitchen_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.kitchen_prompt)
kitchen_rating_chain = LLMChain(llm=llm, prompt=kitchen_rating_prompt, output_key="kitchen_rating")

# Rent
rent_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.rent_prompt)
rent_rating_chain = LLMChain(llm=llm, prompt=rent_rating_prompt, output_key="rent_rating")

# Outbuilding
outbuilding_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.outbuilding_prompt)
outbuilding_rating_chain = LLMChain(llm=llm, prompt=outbuilding_rating_prompt, output_key="outbuilding_rating")

# Modernization
modernization_rating_prompt = ChatPromptTemplate.from_template(gpt_ratings.modernization_prompt)
modernization_rating_chain = LLMChain(llm=llm, prompt=modernization_rating_prompt, output_key="modernization_rating")

overall_chain = SequentialChain(
    chains=[
        translate_desc_chain, translate_params_chain,
        year_of_constr_chain, material_chain, building_type_chain, number_floors_chain,
        technology_summary_chain, technology_rating_chain,
        balcony_summary_chain, balcony_rating_chain,
        law_status_summary_chain, law_status_rating_chain,
        elevator_chain, elevator_summary_chain, elevator_rating_chain,
        basement_summary_chain, basement_rating_chain,
        garage_summary_chain, garage_rating_chain,
        garden_summary_chain, garden_rating_chain,
        monitoring_summary_chain, monitoring_rating_chain,
        kitchen_summary_chain, kitchen_rating_chain,
        rent_summary_chain, rent_rating_chain,
        outbuilding_summary_chain, outbuilding_rating_chain,
        modernization_summary_chain, modernization_rating_chain
    ],
    input_variables=["real_estate_offer", "offer_parameters"],
    output_variables=[
        "offer_parameters_en", "real_estate_offer_en",
        "technology_summary", "technology_rating",
        "balcony_summary", "balcony_rating",
        "law_summary", "law_rating",
        "elevator", "elevator_summary", "elevator_rating",
        "basement_summary", "basement_rating",
        "garage_summary", "garage_rating",
        "garden_summary", "garden_rating",
        "monitoring_summary", "monitoring_rating",
        "kitchen_summary", "kitchen_rating",
        "rent_summary", "rent_rating",
        "outbuilding_summary", "outbuilding_rating",
        "modernization_summary", "modernization_rating",
    ],
    verbose=True
)

overall_chain_result = overall_chain({'real_estate_offer': offer_description, "offer_parameters": offer_params})

# print(overall_chain_result, end='\n')

result = {
    'technologyGPT': overall_chain_result['technology_rating'],
    'technology_summary': overall_chain_result['technology_summary'],
    'lawStatusGPT': overall_chain_result['law_rating'],
    'law_summary':  overall_chain_result['law_summary'],
    'balconyGPT':  overall_chain_result['balcony_rating'],
    'balcony_summary': overall_chain_result['balcony_summary'],
    'elevatorGPT': overall_chain_result['elevator_rating'],
    'elevator_summary': overall_chain_result['elevator_summary'],
    'basementGPT': overall_chain_result['basement_rating'],
    'basement_summary': overall_chain_result['basement_summary'],
    'garageGPT': overall_chain_result['garage_rating'],
    'garage_summary': overall_chain_result['garage_summary'],
    'gardenGPT': overall_chain_result['garden_rating'],
    'garden_summary': overall_chain_result['garden_summary'],
    'modernizationGPT': overall_chain_result['modernization_rating'],
    'modernization_summary': overall_chain_result['modernization_summary'],
    'alarmGPT': overall_chain_result['monitoring_rating'],
    'alarm_summary': overall_chain_result['monitoring_summary'],
    'kitchenGPT': overall_chain_result['kitchen_rating'],
    'kitchen_summary': overall_chain_result['kitchen_summary'],
    'outbuildingGPT': overall_chain_result['outbuilding_rating'],
    'outbuilding_summary': overall_chain_result['outbuilding_summary'],
    'qualityGPT': '',
    'status': 1,
    'rentGPT': overall_chain_result['rent_rating'],
    'rent_summary': overall_chain_result['rent_summary'],

}

print(result)
print(offer_params)
print(offer_description)

#@TODO:
# 1. Pobrać dane z answers
# 2. Jeżeli kuchnia, modernizacja itp są ocenione to dać do ostatecznego rezulatu, ignorując przy tym części chainingu
# 3. Wysłać do bazy danych
# 4. Zloopować wszystko
# 5. Pobrać dane z status z tabeli flats_GPT - i dać if'a czy ściągać czy nie
# 5. Translate Google!

# KITCHEN!!!