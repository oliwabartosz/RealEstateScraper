import translators as ts

from gpt import offer_record
from src.handlers import api_handler
from src.utils.utils import merge_dictionaries_by_id

# Get JWT AUTH TOKEN
jwt_data: dict = api_handler.get_jwt_token(f'{api_handler.rer_url}/rer/auth')

# Get all data from database based on selected columns
offers_data = api_handler.get_offers_data_from_api(
    jwt_data['access_token'],
    '/rer/api/flats/',
    'GET',
    'id', 'number', 'lawStatus', 'floorsNumber', 'rent', 'material', 'buildingType', 'yearBuilt', 'buildingQuality',
    'balcony', 'balconyQuantity', 'terracesQuantity', 'loggiasQuantity', 'frenchBalconyQuantity', 'kitchenType',
    'basement', 'storageRoom', 'attic', 'parkingPlace', 'priceParkingUnderground', 'priceParkingGround', 'garden',
    'elevator', 'security', 'monitoring', 'guardedArea', 'guardedEstate', 'securityControl', 'description'
)
# Get all the data pre-rated by the user from database based on selected columns
offers_gpt_data = api_handler.get_offers_data_from_api(
    jwt_data['access_token'],
    '/rer/api/flats/gpt',
    'GET',
    'id', 'technologyGPT', 'modernizationGPT', 'kitchenGPT', 'qualityGPT'
)

# Update data with information from another table get from the database
offers_data = merge_dictionaries_by_id(offers_data, offers_gpt_data)

# Filter out unnecessary keys for params
offer_params = {key: value for key, value in offer_record.items() if key not in ['id', 'number', 'description']}
offer_description = offer_record['description']

# Translate text
offer_parameters_en = ts.translate_text(str(offer_params), translator='google', to_language='en')
offer_description_en = ts.translate_text(offer_description, translator='google', to_language='en')