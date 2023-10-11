from src.handlers import api_handler
from src.utils.utils import merge_dictionaries_by_id

# Get JWT AUTH TOKEN
jwt_data: dict = api_handler.get_jwt_token(f'{api_handler.rer_url}/rer/auth')

# Get all data from database based on selected columns
data = api_handler.get_offers_data_from_api(
    jwt_data['access_token'],
    '/rer/api/flats/',
    'GET',
    'id', 'number', 'lawStatus', 'floorsNumber', 'rent', 'material', 'buildingType', 'yearBuilt', 'buildingQuality',
    'balcony', 'balconyQuantity', 'terracesQuantity', 'loggiasQuantity', 'frenchBalconyQuantity', 'kitchenType',
    'basement', 'storageRoom', 'attic', 'parkingPlace', 'priceParkingUnderground', 'priceParkingGround', 'garden',
    'elevator', 'security', 'monitoring', 'guardedArea', 'guardedEstate', 'securityControl', 'description'
)
# Get all the data pre-rated by the user from database based on selected columns
offers_ans_data = api_handler.get_offers_data_from_api(
    jwt_data['access_token'],
    '/rer/api/flats/answers',
    'GET',
    'id', 'technologyAns', 'modernizationAns', 'kitchenAns', 'qualityAns'
)

offers_gpt_data = api_handler.get_offers_data_from_api(
    jwt_data['access_token'],
    '/rer/api/flats/gpt',
    'GET',
    'id', 'status')

# Update data with information from another table got from the database
offers_data: list[dict] = merge_dictionaries_by_id(data, offers_ans_data)

